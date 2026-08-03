#!/usr/bin/env python3
"""Build the two meeting artifacts (summary doc + interactive annotated transcript) from md + canon."""
import json, re, html, markdown, os, sys

WD = "/home/user/claude-/legal-war-room"
M = f"{WD}/meeting-2026-08-02"

TOKENS = """
:root{
  --paper:#FBFAF7; --ink:#23262B; --ink-soft:#565B63; --line:#DDD8CC;
  --navy:#1F3A5F; --navy-soft:#E8EDF4; --maroon:#8E2C2C; --maroon-soft:#F6E9E7;
  --card:#FFFFFF; --quote-bg:#F5F2EA;
  --t-discovery:#2C6E63; --t-damages:#9A6A1B; --t-mp:#8E2C2C; --t-pattern:#5B4A78;
  --t-admission:#2F6B2F; --t-evidence:#3A5F8A; --t-timeline:#6B5A2C; --t-health:#7A3E5E; --t-small:#8B8778;
}
@media (prefers-color-scheme: dark){:root{
  --paper:#15171B; --ink:#E6E3DA; --ink-soft:#A9ADB6; --line:#33373E;
  --navy:#8FB0D8; --navy-soft:#20293A; --maroon:#D98A80; --maroon-soft:#3A2422;
  --card:#1C1F25; --quote-bg:#22252C;
  --t-discovery:#6FBFB0; --t-damages:#D8AC5E; --t-mp:#D98A80; --t-pattern:#A995CC;
  --t-admission:#7FBF7F; --t-evidence:#82A8D8; --t-timeline:#C0A860; --t-health:#C787A8; --t-small:#8B8778;
}}
:root[data-theme="dark"]{
  --paper:#15171B; --ink:#E6E3DA; --ink-soft:#A9ADB6; --line:#33373E;
  --navy:#8FB0D8; --navy-soft:#20293A; --maroon:#D98A80; --maroon-soft:#3A2422;
  --card:#1C1F25; --quote-bg:#22252C;
  --t-discovery:#6FBFB0; --t-damages:#D8AC5E; --t-mp:#D98A80; --t-pattern:#A995CC;
  --t-admission:#7FBF7F; --t-evidence:#82A8D8; --t-timeline:#C0A860; --t-health:#C787A8; --t-small:#8B8778;
}
:root[data-theme="light"]{
  --paper:#FBFAF7; --ink:#23262B; --ink-soft:#565B63; --line:#DDD8CC;
  --navy:#1F3A5F; --navy-soft:#E8EDF4; --maroon:#8E2C2C; --maroon-soft:#F6E9E7;
  --card:#FFFFFF; --quote-bg:#F5F2EA;
  --t-discovery:#2C6E63; --t-damages:#9A6A1B; --t-mp:#8E2C2C; --t-pattern:#5B4A78;
  --t-admission:#2F6B2F; --t-evidence:#3A5F8A; --t-timeline:#6B5A2C; --t-health:#7A3E5E; --t-small:#8B8778;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:15px/1.55 "Segoe UI",system-ui,-apple-system,sans-serif;}
h1,h2,h3{font-family:"Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;color:var(--navy);text-wrap:balance}
.mono{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-variant-numeric:tabular-nums}
.banner{background:var(--maroon);color:#FBF6F0;text-align:center;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;padding:6px 10px}
.wrap{max-width:960px;margin:0 auto;padding:20px 20px 80px}
.clock{display:inline-flex;gap:7px;align-items:center;background:var(--maroon-soft);color:var(--maroon);
  border:1px solid var(--maroon);border-radius:4px;padding:4px 10px;font-weight:600;font-size:12.5px}
table{border-collapse:collapse;width:100%;margin:10px 0 18px;font-size:13px}
th{background:var(--navy);color:#F4F6FA;text-align:left;padding:7px 9px;font-weight:600}
:root[data-theme="dark"] th{background:var(--navy-soft);color:var(--navy)}
@media (prefers-color-scheme: dark){th{background:var(--navy-soft);color:var(--navy)}}
:root[data-theme="light"] th{background:var(--navy);color:#F4F6FA}
td{border:1px solid var(--line);padding:6px 9px;vertical-align:top}
tr:nth-child(even) td{background:var(--card)}
.tablebox{overflow-x:auto}
blockquote{border-left:3px solid var(--maroon);background:var(--quote-bg);margin:8px 0;
  padding:6px 12px;font-style:italic;color:var(--ink-soft)}
"""

def summary_page():
    md_text = open(f"{M}/MEETING_SUMMARY.md").read()
    body = markdown.markdown(md_text, extensions=["tables","sane_lists","smarty"])
    body = body.replace("<table>", '<div class="tablebox"><table>').replace("</table>", "</table></div>")
    return f"""<title>Meeting Summary — Drazen · Aug 2 2026</title>
<style>{TOKENS}
.wrap h1{{font-size:26px;margin:18px 0 4px;border-bottom:3px solid var(--maroon);padding-bottom:8px}}
.wrap h2{{font-size:19px;margin:26px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}}
.wrap p{{max-width:72ch}}
</style>
<div class="banner">Attorney Work Product — Privileged &amp; Confidential</div>
<div class="wrap">{body}</div>"""

TAG_MAP = {
  "discovery":("discovery","var(--t-discovery)"), "damages":("damages","var(--t-damages)"),
  "malicious":("prosecution","var(--t-mp)"), "prosecution":("prosecution","var(--t-mp)"),
  "pattern":("pattern","var(--t-pattern)"), "admission":("admission","var(--t-admission)"),
  "evidence":("evidence","var(--t-evidence)"), "timeline":("timeline","var(--t-timeline)"),
  "health":("health","var(--t-health)"), "action":("action","var(--t-evidence)"),
  "mediation":("mediation","var(--t-timeline)"), "smalltalk":("smalltalk","var(--t-small)"),
}

def classify(tags):
    out = []
    for t in tags:
        for k,(label,_) in TAG_MAP.items():
            if k in t and label not in [o[0] for o in out]:
                out.append((label, TAG_MAP[k][1]))
    return out or [("timeline", TAG_MAP["timeline"][1])]

def transcript_page():
    canon = json.load(open(f"{WD}/data/transcript_master.json"))
    blocks = canon["blocks"] if isinstance(canon, dict) else canon
    tag_by_ts = { b["timestamp"]: b.get("legal_tags") or b.get("tags") or [] for b in blocks }

    md_text = open(f"{M}/ANNOTATED_TRANSCRIPT.md").read()
    # split into preamble + blocks on '## <ts heading>'
    parts = re.split(r"\n## (?=.*?\d{2}:\d{2}:\d{2})", md_text)
    pre = parts[0]
    pre_html = markdown.markdown(re.sub(r"^# .*\n", "", pre, count=1), extensions=["tables","smarty"])

    cards, all_labels = [], set()
    for chunk in parts[1:]:
        first_nl = chunk.find("\n")
        heading = chunk[:first_nl].strip()
        body_md = chunk[first_nl:]
        ts_m = re.search(r"(\d{2}:\d{2}:\d{2})", heading)
        ts = ts_m.group(1) if ts_m else ""
        title = re.sub(r"^\d{2}:\d{2}:\d{2}\s*[—–-]?\s*", "", heading)
        tags = classify([t.lower() for t in tag_by_ts.get(ts, [])])
        labels = [t[0] for t in tags]
        all_labels.update(labels)
        body_html = markdown.markdown(body_md, extensions=["tables","smarty"])
        body_html = body_html.replace("⚖ SIGNIFICANCE:", "<b>⚖</b>")
        body_html = re.sub(r"<p>(<b>⚖</b>.*?)</p>", r'<p class="sig">\1</p>', body_html, flags=re.S)
        chips = "".join(f'<span class="chip" style="--c:{c}">{l}</span>' for l,c in tags)
        small = " small" if labels == ["smalltalk"] else ""
        cards.append(f'''<article class="blk{small}" data-tags="{' '.join(labels)}" data-text="{html.escape(re.sub(r'<[^>]+>',' ',body_html).lower()[:1500], quote=True)}">
<header><a class="ts mono" id="t{ts.replace(':','')}" href="#t{ts.replace(':','')}">{ts}</a><h3>{html.escape(title)}</h3>{chips}</header>
<div class="body">{body_html}</div></article>''')

    filter_chips = "".join(
        f'<button class="fchip" data-f="{l}" style="--c:{TAG_MAP.get(l if l!="prosecution" else "malicious", TAG_MAP["timeline"])[1]}">{l}</button>'
        for l in sorted(all_labels) if l != "smalltalk")

    return f"""<title>Annotated Transcript — Drazen · Aug 2 2026</title>
<style>{TOKENS}
.top{{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:2px solid var(--navy);padding:10px 16px}}
.top h1{{font-size:17px;margin:0 0 6px}}
.clockrow{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}}
.controls{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.fchip{{border:1px solid var(--c);color:var(--c);background:transparent;border-radius:14px;
  padding:2px 11px;font-size:12px;cursor:pointer}}
.fchip.on{{background:var(--c);color:var(--paper)}}
#q{{flex:1;min-width:140px;max-width:280px;background:var(--card);color:var(--ink);
  border:1px solid var(--line);border-radius:6px;padding:5px 9px;font-size:13px}}
#smalltoggle{{font-size:12px;color:var(--ink-soft);display:flex;gap:5px;align-items:center;cursor:pointer}}
.blk{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy);
  border-radius:6px;margin:12px 0;padding:12px 16px}}
.blk.small{{opacity:.62;border-left-color:var(--t-small)}}
.blk header{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:4px}}
.blk h3{{font-size:15px;margin:0;flex:1;min-width:200px}}
.ts{{color:var(--maroon);font-weight:700;font-size:13px;text-decoration:none}}
.chip{{border:1px solid var(--c);color:var(--c);border-radius:12px;padding:1px 9px;font-size:11px;white-space:nowrap}}
.sig{{border-left:3px solid var(--navy);background:var(--navy-soft);padding:5px 10px;border-radius:0 4px 4px 0}}
.body p{{max-width:78ch}}
.hidden{{display:none}}
.count{{font-size:12px;color:var(--ink-soft);margin-left:auto}}
.pre{{font-size:13.5px;color:var(--ink-soft);border:1px dashed var(--line);border-radius:6px;padding:4px 14px;margin:14px 0}}
@media (prefers-reduced-motion: no-preference){{.blk{{transition:opacity .15s}}}}
</style>
<div class="banner">Attorney Work Product — Privileged &amp; Confidential</div>
<div class="top">
<h1>Annotated Transcript — Drazen // Rahman, Aug 2 2026 <span class="mono" style="color:var(--ink-soft);font-size:12px">3:26-cv-00197 NDNY</span></h1>
<div class="clockrow"><span class="clock">🚨 Malicious-prosecution SoL ≈ Sept 2026</span>
<span class="clock">⏰ Mediation deadline Nov 2026</span></div>
<div class="controls">{filter_chips}
<input id="q" type="search" placeholder="search the record…">
<label id="smalltoggle"><input type="checkbox" id="sm"> smalltalk</label>
<span class="count" id="n"></span></div>
</div>
<div class="wrap">
<details class="pre"><summary>Provenance, attribution caveats &amp; critical flags</summary>{pre_html}</details>
{''.join(cards)}
</div>
<script>
const blks=[...document.querySelectorAll('.blk')],chips=[...document.querySelectorAll('.fchip')],
q=document.getElementById('q'),sm=document.getElementById('sm'),n=document.getElementById('n');
let active=new Set();
function apply(){{
  const s=q.value.toLowerCase().trim();let vis=0;
  blks.forEach(b=>{{
    const tags=b.dataset.tags.split(' ');
    let ok=(!active.size||tags.some(t=>active.has(t)));
    if(tags.includes('smalltalk')&&!sm.checked&&!active.has('smalltalk'))ok=false;
    if(s&&!b.dataset.text.includes(s))ok=false;
    b.classList.toggle('hidden',!ok);if(ok)vis++;
  }});
  n.textContent=vis+' / '+blks.length+' blocks';
}}
chips.forEach(c=>c.onclick=()=>{{const f=c.dataset.f;
  c.classList.toggle('on');active.has(f)?active.delete(f):active.add(f);apply();}});
q.oninput=apply;sm.onchange=apply;apply();
</script>"""

if __name__ == "__main__":
    open(f"{M}/meeting-summary.artifact.html","w").write(summary_page())
    open(f"{M}/annotated-transcript.artifact.html","w").write(transcript_page())
    for f in ["meeting-summary.artifact.html","annotated-transcript.artifact.html"]:
        print("OK", f, os.path.getsize(f"{M}/{f}")//1024, "KB")
