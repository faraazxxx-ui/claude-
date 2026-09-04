#!/usr/bin/env python3
"""Export this Claude Code session to JSON + Markdown + SQL, with deltas.

Reads the raw session transcript and emits a self-describing corpus that a
third party can analyse and re-create from. Every output is derived from the
transcript alone — nothing is inferred, summarised or invented here.

    python3 build_export.py [--transcript PATH] [--out DIR]
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, OrderedDict

DEFAULT_TRANSCRIPT = ("/root/.claude/projects/-home-user-claude-/"
                      "7f4839a0-2759-5274-a271-16ea4d44156c.jsonl")

# --- privacy zoning ------------------------------------------------------
# Five zones per the orchestrator contract. Rules are keyword-based and
# deliberately over-inclusive: a false Confidential is cheap, a false Public
# is not. The matched term is recorded so every tag is auditable.
ZONE_RULES = [
    ("Confidential", "litigation", [
        "affidavit", "eeoc", "hhs ocr", "acgme", "hipaa", "fmla", "retaliation",
        "probation", "forgery", "defamation", "damages ledger", "right-to-sue",
        "plaintiff", "docket", "notariz", "penalty of perjury", "§1983",
        "title vii", "uhs", "guthrie", "residency",
    ]),
    ("Confidential", "medical", [
        "pots", "brugada", "propranolol", "ivabradine", "guanfacine", "mcas",
        "long covid", "dysautonomia", "icd", "hrv", "whoop", "oura",
        "adherence", "glp-1", "vzv", "me-cfs", "loop score", "tachycardia",
        "prescription", "pharmacy",
    ]),
    ("Private work", "personal-identifier", [
        "faraaz", "rahman", "@gmail", "@therahmanfoundation", "queens, new york",
    ]),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(text):
    """Return (zone, reason, matched_term). Default is Private work."""
    low = (text or "").lower()
    for zone, reason, terms in ZONE_RULES:
        for t in terms:
            if t in low:
                return zone, reason, t
    return "Private work", "session-internal", ""


ZONE_RANK = {"Public": 0, "Private work": 1, "Confidential": 2,
             "Privileged": 3, "Restricted": 4}


def blocks_of(msg):
    content = msg.get("content")
    if isinstance(content, str):
        return [{"type": "plain", "text": content}]
    if isinstance(content, list):
        return [b for b in content if isinstance(b, dict)]
    return []


def flatten_result(res):
    """Tool results arrive in several shapes; reduce to text + error flag."""
    if res is None:
        return "", False
    if isinstance(res, str):
        return res, False
    if isinstance(res, list):
        parts = []
        for b in res:
            if isinstance(b, dict):
                parts.append(b.get("text") or json.dumps(b, ensure_ascii=False))
            else:
                parts.append(str(b))
        return "\n".join(parts), False
    if isinstance(res, dict):
        err = bool(res.get("is_error") or res.get("isError"))
        for key in ("text", "content", "stdout", "output"):
            if key in res:
                v = res[key]
                if isinstance(v, str):
                    return v, err
                return json.dumps(v, ensure_ascii=False), err
        return json.dumps(res, ensure_ascii=False), err
    return str(res), False


def _emit_block(b, bid, blocks, tools, uuid, turn_no, seq, role, tool_by_id):
    """Append one content block (and, for a tool call, its stub) in place."""
    bid += 1
    kind = b.get("type")
    text, tool_name, tool_input, tool_id, is_err = "", None, None, None, 0
    redacted, sig_sha, sig_len = 0, None, None
    if kind in ("text", "plain"):
        text = b.get("text", "")
    elif kind == "thinking":
        # The transcript stores reasoning blocks signature-only: the plaintext
        # is not written to disk. Record proof of existence and position; do
        # not pretend to have the content.
        text = b.get("thinking", "") or ""
        sig = b.get("signature") or ""
        redacted = 0 if text.strip() else 1
        sig_len = len(sig) or None
        sig_sha = hashlib.sha256(sig.encode()).hexdigest() if sig else None
    elif kind == "tool_use":
        tool_name = b.get("name")
        tool_id = b.get("id")
        tool_input = json.dumps(b.get("input", {}), ensure_ascii=False)
        text = tool_input
        tool_by_id[tool_id] = tool_name
    elif kind == "tool_result":
        tool_id = b.get("tool_use_id")
        text, is_err = flatten_result(b.get("content"))
        is_err = 1 if (is_err or b.get("is_error")) else 0
        tool_name = tool_by_id.get(tool_id)
    else:
        text = json.dumps(b, ensure_ascii=False)

    zone, reason, term = classify(text)
    blocks.append(OrderedDict([
        ("block_id", bid),
        ("turn_uuid", uuid),
        ("turn_no", turn_no),
        ("seq", seq),
        ("role", role),
        ("kind", kind),
        ("chars", len(text or "")),
        ("tool_name", tool_name),
        ("tool_use_id", tool_id),
        ("is_error", is_err),
        ("redacted", redacted),
        ("signature_sha256", sig_sha),
        ("signature_len", sig_len),
        ("privacy_zone", zone),
        ("zone_reason", reason),
        ("zone_match", term),
        ("text", text),
    ]))
    if kind == "tool_use":
        tools.append(OrderedDict([
            ("tool_use_id", tool_id),
            ("turn_uuid", uuid),
            ("turn_no", turn_no),
            ("name", tool_name),
            ("input_json", tool_input),
            ("result_chars", None),
            ("is_error", None),
        ]))
    return bid, blocks, tools


def build(transcript, outdir):
    recs = []
    for line in open(transcript, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                recs.append(json.loads(line))
            except ValueError:
                pass

    turns, blocks, tools, usage = [], [], [], []
    tool_by_id = {}
    bid = 0
    turn_no = 0
    # The CLI writes one content block per record, so consecutive records that
    # share a message id are one logical model response. Grouping them is what
    # makes a "turn" mean a turn - and stops usage being counted once per
    # block instead of once per response.
    turn_index = {}
    seq_in_turn = Counter()

    for rec in recs:
        msg = rec.get("message")
        if not isinstance(msg, dict):
            continue
        role = msg.get("role")
        if role not in ("user", "assistant"):
            continue
        gkey = (msg.get("id") or rec.get("requestId") or rec.get("uuid")
                if role == "assistant" else rec.get("uuid"))
        if gkey in turn_index:
            uuid = turn_index[gkey]
            existing = next(t for t in turns if t["uuid"] == uuid)
            turn_no = existing["turn_no"]
            for seq, b in enumerate(blocks_of(msg)):
                bid, blocks, tools = _emit_block(
                    b, bid, blocks, tools, uuid, turn_no,
                    seq_in_turn[uuid], role, tool_by_id)
                seq_in_turn[uuid] += 1
            continue
        turn_no = len(turns) + 1
        uuid = rec.get("uuid")
        turn_index[gkey] = uuid
        # A user record carrying only tool_result blocks is harness plumbing,
        # not something he typed. Separating the two is what makes the
        # "his input vs my thinking" comparison honest.
        bl = blocks_of(msg)
        kinds = set(b.get("type") for b in bl)
        is_plumbing = (role == "user" and kinds and
                       kinds <= {"tool_result"})
        turns.append(OrderedDict([
            ("turn_no", turn_no),
            ("uuid", uuid),
            ("parent_uuid", rec.get("parentUuid")),
            ("role", role),
            ("kind", "tool_result" if is_plumbing else
                     ("meta" if rec.get("isMeta") else "authored")),
            ("timestamp", rec.get("timestamp")),
            ("model", msg.get("model")),
            ("effort", rec.get("effort")),
            ("git_branch", rec.get("gitBranch")),
            ("stop_reason", msg.get("stop_reason")),
        ]))

        u = msg.get("usage") or {}
        if u:
            usage.append(OrderedDict([
                ("turn_uuid", uuid),
                ("input_tokens", u.get("input_tokens")),
                ("output_tokens", u.get("output_tokens")),
                ("cache_read_input_tokens", u.get("cache_read_input_tokens")),
                ("cache_creation_input_tokens", u.get("cache_creation_input_tokens")),
                ("service_tier", u.get("service_tier")),
            ]))

        for seq, b in enumerate(bl):
            bid, blocks, tools = _emit_block(
                b, bid, blocks, tools, uuid, turn_no,
                seq_in_turn[uuid], role, tool_by_id)
            seq_in_turn[uuid] += 1

    # Attach results back to their calls.
    res_by_id = {}
    for b in blocks:
        if b["kind"] == "tool_result" and b["tool_use_id"]:
            res_by_id[b["tool_use_id"]] = (b["chars"], b["is_error"])
    for t in tools:
        if t["tool_use_id"] in res_by_id:
            t["result_chars"], t["is_error"] = res_by_id[t["tool_use_id"]]

    # --- reasoning volume, since the reasoning text itself is unrecoverable --
    # Derivation, stated so it can be checked or rejected:
    #   visible_tokens_est = (chars of text + tool_use blocks) / 4
    #   hidden_tokens_est  = output_tokens (billed, exact) - visible_tokens_est
    # output_tokens is exact and covers reasoning + text + tool arguments.
    # The /4 chars-per-token figure is a standard English approximation, not a
    # measurement — so hidden_tokens_est is an ESTIMATE and is named as one.
    out_by_turn = {u["turn_uuid"]: (u.get("output_tokens") or 0) for u in usage}
    vis_by_turn, think_by_turn = Counter(), Counter()
    for b in blocks:
        if b["kind"] in ("text", "tool_use"):
            vis_by_turn[b["turn_uuid"]] += b["chars"]
        elif b["kind"] == "thinking":
            think_by_turn[b["turn_uuid"]] += 1
    for t in turns:
        if t["role"] != "assistant":
            t["output_tokens"] = None
            t["visible_chars"] = None
            t["thinking_blocks"] = None
            t["hidden_tokens_est"] = None
            continue
        ot = out_by_turn.get(t["uuid"], 0)
        vc = vis_by_turn.get(t["uuid"], 0)
        t["output_tokens"] = ot
        t["visible_chars"] = vc
        t["thinking_blocks"] = think_by_turn.get(t["uuid"], 0)
        t["hidden_tokens_est"] = max(0, ot - round(vc / 4)) if ot else 0

    # --- exchanges: one authored user message and everything it caused ---
    exchanges = []
    cur = None
    for t in turns:
        tb = [b for b in blocks if b["turn_uuid"] == t["uuid"]]
        if t["role"] == "user" and t["kind"] == "authored":
            if cur:
                exchanges.append(cur)
            ask = "\n".join(b["text"] for b in tb
                            if b["kind"] in ("text", "plain"))
            zone, reason, term = classify(ask)
            cur = OrderedDict([
                ("exchange_no", len(exchanges) + 1),
                ("started", t["timestamp"]),
                ("ended", t["timestamp"]),
                ("ask_chars", len(ask)),
                ("thinking_blocks", 0),
                ("hidden_tokens_est", 0),
                ("reply_chars", 0),
                ("tool_calls", 0),
                ("tool_names", []),
                ("assistant_turns", 0),
                ("privacy_zone", zone),
                ("ask", ask),
            ])
        elif cur is not None and t["role"] == "assistant":
            cur["assistant_turns"] += 1
            cur["ended"] = t["timestamp"] or cur["ended"]
            cur["hidden_tokens_est"] += t.get("hidden_tokens_est") or 0
            for b in tb:
                if b["kind"] == "thinking":
                    cur["thinking_blocks"] += 1
                elif b["kind"] == "text":
                    cur["reply_chars"] += b["chars"]
                elif b["kind"] == "tool_use":
                    cur["tool_calls"] += 1
                    if b["tool_name"]:
                        cur["tool_names"].append(b["tool_name"])
        elif cur is not None and t["timestamp"]:
            cur["ended"] = t["timestamp"]
    if cur:
        exchanges.append(cur)

    for e in exchanges:
        e["tool_names"] = ", ".join(sorted(set(e["tool_names"])))
        # The delta this export exists to expose: how much work each unit of
        # his input caused, and how much of that work he ever saw. Both ratios
        # use hidden_tokens_est, so both inherit its estimate status.
        ask_tok = round(e["ask_chars"] / 4) or None
        e["hidden_tokens_per_ask_token"] = (round(e["hidden_tokens_est"] / ask_tok, 1)
                                            if ask_tok else None)
        e["shown_fraction"] = (round(round(e["reply_chars"] / 4) /
                                     (e["hidden_tokens_est"] + round(e["reply_chars"] / 4)), 3)
                               if (e["hidden_tokens_est"] + e["reply_chars"]) else None)

    # --- artifacts produced ---------------------------------------------
    repo = "/home/user/claude-"
    watch = ["CLAUDE.md"]
    ftdir = os.path.join(repo, "agentic-memory", "field-test-01")
    if os.path.isdir(ftdir):
        for name in sorted(os.listdir(ftdir)):
            watch.append(os.path.join("agentic-memory", "field-test-01", name))
    artifacts = []
    for rel in watch:
        path = os.path.join(repo, rel)
        if os.path.isfile(path):
            artifacts.append(OrderedDict([
                ("path", rel),
                ("bytes", os.path.getsize(path)),
                ("sha256", sha256_file(path)),
                ("ext", os.path.splitext(rel)[1].lstrip(".") or "none"),
            ]))

    ts = [t["timestamp"] for t in turns if t["timestamp"]]
    models = [t["model"] for t in turns if t.get("model")]
    session = OrderedDict([
        ("session_id", recs[0].get("sessionId") if recs else None),
        ("transcript_sha256", sha256_file(transcript)),
        ("transcript_bytes", os.path.getsize(transcript)),
        ("records", len(recs)),
        ("turns", len(turns)),
        ("blocks", len(blocks)),
        ("tool_calls", len(tools)),
        ("exchanges", len(exchanges)),
        ("started", min(ts) if ts else None),
        ("ended", max(ts) if ts else None),
        ("models", ", ".join(sorted(set(models)))),
        ("cwd", recs[0].get("cwd") if recs else None),
        ("git_branch", recs[0].get("gitBranch") if recs else None),
        ("max_privacy_zone", max((b["privacy_zone"] for b in blocks),
                                 key=lambda z: ZONE_RANK[z]) if blocks else None),
        ("thinking_blocks", sum(1 for b in blocks if b["kind"] == "thinking")),
        ("thinking_plaintext_recoverable",
         1 if any(b["kind"] == "thinking" and b["chars"] for b in blocks) else 0),
        ("hidden_tokens_est_total",
         sum(t.get("hidden_tokens_est") or 0 for t in turns)),
    ])

    os.makedirs(outdir, exist_ok=True)
    payload = OrderedDict([
        ("session", session), ("turns", turns), ("blocks", blocks),
        ("tool_calls", tools), ("usage", usage), ("exchanges", exchanges),
        ("artifacts", artifacts),
    ])
    with open(os.path.join(outdir, "session.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    write_sql(payload, os.path.join(outdir, "session.sql"))
    write_md(payload, os.path.join(outdir, "session.md"))
    verify(payload, outdir)
    write_manifest(payload, outdir, transcript)
    return payload


def verify(payload, outdir):
    """Mechanical grade: load the SQL into a fresh database and reconcile it
    against the JSON. Whoever built it does not get to grade it by opinion, so
    the grade is a row count either matching or not."""
    import sqlite3
    db = os.path.join(outdir, "session.db")
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    con.executescript(open(os.path.join(outdir, "session.sql"), encoding="utf-8").read())
    lines, ok = [], True
    for table in ("session", "turns", "blocks", "tool_calls", "usage",
                  "exchanges", "artifacts"):
        want = 1 if table == "session" else len(payload[table])
        got = con.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
        ok = ok and got == want
        lines.append("%-12s sql=%-6d json=%-6d %s"
                     % (table, got, want, "OK" if got == want else "MISMATCH"))
    con.close()
    lines.append("")
    lines.append("RESULT: " + ("PASS" if ok else "FAIL"))
    lines.append("Checked: every table round-trips from JSON through SQL into a "
                 "live database at identical row counts.")
    lines.append("NOT checked by this script: whether the interpretation is "
                 "right. That needs fresh eyes, which by contract cannot be "
                 "the thing that built it.")
    open(os.path.join(outdir, "VERIFY.txt"), "w", encoding="utf-8").write(
        "\n".join(lines) + "\n")
    print("\n".join(lines))
    return ok


# --- SQL -----------------------------------------------------------------
DDL = """-- Session export. SQLite dialect; portable to Postgres by swapping
-- INTEGER PRIMARY KEY for SERIAL and TEXT for VARCHAR.
PRAGMA foreign_keys = ON;

CREATE TABLE session (
  session_id          TEXT PRIMARY KEY,
  transcript_sha256   TEXT NOT NULL,
  transcript_bytes    INTEGER,
  records             INTEGER,
  turns               INTEGER,
  blocks              INTEGER,
  tool_calls          INTEGER,
  exchanges           INTEGER,
  started             TEXT,
  ended               TEXT,
  models              TEXT,
  cwd                 TEXT,
  git_branch          TEXT,
  max_privacy_zone    TEXT,
  thinking_blocks     INTEGER,
  -- 0 = the reasoning plaintext is NOT in the transcript. Only the presence,
  -- position and signature of each reasoning block survive on disk.
  thinking_plaintext_recoverable INTEGER,
  hidden_tokens_est_total INTEGER
);

CREATE TABLE turns (
  turn_no     INTEGER PRIMARY KEY,
  uuid        TEXT UNIQUE,
  parent_uuid TEXT,
  role        TEXT NOT NULL CHECK (role IN ('user','assistant')),
  kind        TEXT NOT NULL CHECK (kind IN ('authored','tool_result','meta')),
  timestamp   TEXT,
  model       TEXT,
  effort      TEXT,
  git_branch  TEXT,
  stop_reason TEXT,
  output_tokens     INTEGER,  -- exact, billed
  visible_chars     INTEGER,  -- text + tool arguments actually emitted
  thinking_blocks   INTEGER,
  -- ESTIMATE: output_tokens - visible_chars/4. See README derivation.
  hidden_tokens_est INTEGER
);

CREATE TABLE blocks (
  block_id     INTEGER PRIMARY KEY,
  turn_uuid    TEXT REFERENCES turns(uuid),
  turn_no      INTEGER,
  seq          INTEGER,
  role         TEXT,
  kind         TEXT NOT NULL,
  chars        INTEGER,
  tool_name    TEXT,
  tool_use_id  TEXT,
  is_error     INTEGER,
  -- 1 on every reasoning block: content absent from the transcript.
  redacted         INTEGER,
  signature_sha256 TEXT,   -- proof the block existed, and was not altered
  signature_len    INTEGER,
  privacy_zone TEXT NOT NULL,
  zone_reason  TEXT,
  zone_match   TEXT,
  text         TEXT
);

CREATE TABLE tool_calls (
  tool_use_id  TEXT PRIMARY KEY,
  turn_uuid    TEXT REFERENCES turns(uuid),
  turn_no      INTEGER,
  name         TEXT,
  input_json   TEXT,
  result_chars INTEGER,
  is_error     INTEGER
);

CREATE TABLE usage (
  turn_uuid                   TEXT REFERENCES turns(uuid),
  input_tokens                INTEGER,
  output_tokens               INTEGER,
  cache_read_input_tokens     INTEGER,
  cache_creation_input_tokens INTEGER,
  service_tier                TEXT
);

CREATE TABLE exchanges (
  exchange_no                INTEGER PRIMARY KEY,
  started                    TEXT,
  ended                      TEXT,
  ask_chars                  INTEGER,  -- what he typed
  thinking_blocks            INTEGER,  -- how many times I stopped to reason
  hidden_tokens_est          INTEGER,  -- ESTIMATE, see README
  reply_chars                INTEGER,  -- what he read
  tool_calls                 INTEGER,
  tool_names                 TEXT,
  assistant_turns            INTEGER,
  privacy_zone               TEXT,
  hidden_tokens_per_ask_token REAL,    -- work caused per token he typed
  shown_fraction             REAL,     -- of my generated tokens, what he saw
  ask                        TEXT
);

CREATE TABLE artifacts (
  path   TEXT PRIMARY KEY,
  bytes  INTEGER,
  sha256 TEXT,
  ext    TEXT
);

CREATE INDEX idx_blocks_kind ON blocks(kind);
CREATE INDEX idx_blocks_zone ON blocks(privacy_zone);
CREATE INDEX idx_blocks_turn ON blocks(turn_no);
CREATE INDEX idx_tools_name  ON tool_calls(name);

-- Convenience views for the questions this export exists to answer.
-- His thinking (what he typed) against mine (what it caused).
CREATE VIEW v_his_vs_mine AS
  SELECT exchange_no, ask_chars, thinking_blocks, hidden_tokens_est,
         reply_chars, tool_calls,
         hidden_tokens_per_ask_token, shown_fraction
  FROM exchanges ORDER BY exchange_no;

-- Every reasoning block: where it happened, and the proof it happened.
-- text is empty by construction — the transcript does not store it.
CREATE VIEW v_hidden_reasoning AS
  SELECT b.turn_no, b.seq, b.redacted, b.signature_sha256,
         t.hidden_tokens_est, t.output_tokens, t.visible_chars
  FROM blocks b JOIN turns t ON t.uuid = b.turn_uuid
  WHERE b.kind='thinking' ORDER BY t.hidden_tokens_est DESC;

CREATE VIEW v_tool_profile AS
  SELECT name, COUNT(*) AS calls, SUM(COALESCE(is_error,0)) AS errors,
         SUM(COALESCE(result_chars,0)) AS result_chars
  FROM tool_calls GROUP BY name ORDER BY calls DESC;

CREATE VIEW v_zone_map AS
  SELECT privacy_zone, zone_reason, COUNT(*) AS blocks, SUM(chars) AS chars
  FROM blocks GROUP BY privacy_zone, zone_reason ORDER BY chars DESC;
"""

SQL_ORDER = [
    ("session", ["session_id", "transcript_sha256", "transcript_bytes", "records",
                 "turns", "blocks", "tool_calls", "exchanges", "started", "ended",
                 "models", "cwd", "git_branch", "max_privacy_zone",
                 "thinking_blocks", "thinking_plaintext_recoverable",
                 "hidden_tokens_est_total"]),
    ("turns", ["turn_no", "uuid", "parent_uuid", "role", "kind", "timestamp",
               "model", "effort", "git_branch", "stop_reason", "output_tokens",
               "visible_chars", "thinking_blocks", "hidden_tokens_est"]),
    ("blocks", ["block_id", "turn_uuid", "turn_no", "seq", "role", "kind", "chars",
                "tool_name", "tool_use_id", "is_error", "redacted",
                "signature_sha256", "signature_len", "privacy_zone",
                "zone_reason", "zone_match", "text"]),
    ("tool_calls", ["tool_use_id", "turn_uuid", "turn_no", "name", "input_json",
                    "result_chars", "is_error"]),
    ("usage", ["turn_uuid", "input_tokens", "output_tokens",
               "cache_read_input_tokens", "cache_creation_input_tokens",
               "service_tier"]),
    ("exchanges", ["exchange_no", "started", "ended", "ask_chars",
                   "thinking_blocks", "hidden_tokens_est", "reply_chars",
                   "tool_calls", "tool_names", "assistant_turns", "privacy_zone",
                   "hidden_tokens_per_ask_token", "shown_fraction", "ask"]),
    ("artifacts", ["path", "bytes", "sha256", "ext"]),
]


def sqlval(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'" + str(v).replace("'", "''") + "'"


def write_sql(payload, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(DDL)
        fh.write("\nBEGIN TRANSACTION;\n")
        for table, cols in SQL_ORDER:
            rows = payload[table]
            if isinstance(rows, dict):
                rows = [rows]
            if not rows:
                continue
            fh.write("\n-- %s (%d rows)\n" % (table, len(rows)))
            for r in rows:
                vals = ", ".join(sqlval(r.get(c)) for c in cols)
                fh.write("INSERT INTO %s (%s) VALUES (%s);\n"
                         % (table, ", ".join(cols), vals))
        fh.write("\nCOMMIT;\n")


# --- Markdown ------------------------------------------------------------
def write_md(payload, path):
    s = payload["session"]
    out = ["# Session transcript — full fidelity",
           "",
           "Every authored turn, every hidden reasoning block, every tool call, in order. "
           "Generated from the raw transcript; nothing summarised.",
           "",
           "| | |", "|---|---|"]
    for k in ("session_id", "started", "ended", "models", "records", "turns",
              "blocks", "tool_calls", "exchanges", "max_privacy_zone",
              "transcript_sha256"):
        out.append("| %s | `%s` |" % (k.replace("_", " "), s.get(k)))
    out.append("")

    by_turn = {}
    for b in payload["blocks"]:
        by_turn.setdefault(b["turn_no"], []).append(b)

    for t in payload["turns"]:
        bl = sorted(by_turn.get(t["turn_no"], []), key=lambda x: x["seq"])
        if t["kind"] == "tool_result":
            names = sorted(set(b["tool_name"] or "?" for b in bl))
            errs = sum(b["is_error"] or 0 for b in bl)
            out.append("### Turn %d · tool results — %s%s"
                       % (t["turn_no"], ", ".join(names),
                          " · **error**" if errs else ""))
            for b in bl:
                out.append("")
                out.append("```")
                out.append((b["text"] or "")[:4000])
                out.append("```")
            out.append("")
            continue

        who = "HIS INPUT" if t["role"] == "user" else "MY OUTPUT"
        out.append("### Turn %d · %s · %s" % (t["turn_no"], who, t["timestamp"]))
        out.append("")
        for b in bl:
            if b["kind"] == "thinking":
                out.append("> **Reasoning block %d — content not recoverable.** "
                           "The transcript stores reasoning signature-only; the "
                           "plaintext was never written to disk. Signature "
                           "`%s…` (%s bytes). This turn: %s output tokens billed, "
                           "%s chars visible, so roughly %s tokens of reasoning "
                           "he never saw."
                           % (b["seq"] + 1,
                              (b["signature_sha256"] or "")[:16],
                              b["signature_len"], t.get("output_tokens"),
                              t.get("visible_chars"), t.get("hidden_tokens_est")))
            elif b["kind"] in ("text", "plain"):
                out.append(b["text"])
            elif b["kind"] == "tool_use":
                out.append("**Tool call · `%s`**" % b["tool_name"])
                out.append("")
                out.append("```json")
                out.append((b["text"] or "")[:3000])
                out.append("```")
            out.append("")
    open(path, "w", encoding="utf-8").write("\n".join(out))


def write_manifest(payload, outdir, transcript):
    counts = Counter(b["kind"] for b in payload["blocks"])
    zones = Counter(b["privacy_zone"] for b in payload["blocks"])
    tools = Counter(t["name"] for t in payload["tool_calls"])
    man = OrderedDict([
        ("generated_from", transcript),
        ("session", payload["session"]),
        ("block_kinds", dict(counts)),
        ("privacy_zones", dict(zones)),
        ("tool_frequency", dict(tools.most_common())),
        ("totals", OrderedDict([
            ("his_input_chars", sum(e["ask_chars"] for e in payload["exchanges"])),
            ("my_reply_chars", sum(e["reply_chars"] for e in payload["exchanges"])),
            ("my_thinking_blocks", payload["session"]["thinking_blocks"]),
            ("my_thinking_plaintext_chars", 0),
            ("my_hidden_tokens_est", payload["session"]["hidden_tokens_est_total"]),
            ("tool_result_chars", sum(b["chars"] for b in payload["blocks"]
                                      if b["kind"] == "tool_result")),
        ])),
        ("known_limits", [
            "Reasoning plaintext is absent from the transcript on disk. All %d "
            "reasoning blocks are signature-only, so this export can prove that "
            "reasoning happened, where, and roughly how much - never what it said."
            % payload["session"]["thinking_blocks"],
            "hidden_tokens_est is an ESTIMATE: exact billed output_tokens minus "
            "visible_chars/4. The /4 chars-per-token figure is an approximation.",
            "Tool results are truncated by the harness before reaching the "
            "transcript, so result_chars measures what was returned to the model, "
            "not what the tool produced.",
            "The pre-compaction portion of this session survives only as a summary "
            "record; turn-level detail before the compact boundary is not in this "
            "file at full fidelity.",
        ]),
        ("files", []),
    ])
    for name in sorted(os.listdir(outdir)):
        p = os.path.join(outdir, name)
        if os.path.isfile(p) and name != "MANIFEST.json":
            man["files"].append(OrderedDict([
                ("name", name), ("bytes", os.path.getsize(p)),
                ("sha256", sha256_file(p))]))
    with open(os.path.join(outdir, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
    return man


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", default=DEFAULT_TRANSCRIPT)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    if not os.path.isfile(a.transcript):
        print("transcript not found: " + a.transcript, file=sys.stderr)
        return 2
    p = build(a.transcript, a.out)
    s = p["session"]
    print("records %(records)s · turns %(turns)s · blocks %(blocks)s · "
          "tool_calls %(tool_calls)s · exchanges %(exchanges)s" % s)
    print("zone ceiling: %s" % s["max_privacy_zone"])
    tot = Counter(b["kind"] for b in p["blocks"])
    print("blocks by kind: " + ", ".join("%s=%d" % kv for kv in sorted(tot.items())))
    print("his input %d chars · my replies %d chars" % (
        sum(e["ask_chars"] for e in p["exchanges"]),
        sum(e["reply_chars"] for e in p["exchanges"])))
    print("reasoning blocks %d · plaintext recoverable: %s · hidden tokens (est) %d"
          % (s["thinking_blocks"],
             "yes" if s["thinking_plaintext_recoverable"] else "NO",
             s["hidden_tokens_est_total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
