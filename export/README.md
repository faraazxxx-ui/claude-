# Export

A point-in-time export of this repository's full contents plus the output of
every agent chat session that has run against it.

| File | Size | Format |
|---|---|---|
| `REPO_AND_CHAT_EXPORT.md` | ~4.4 MB | Human-readable, single document |
| `REPO_AND_CHAT_EXPORT.json` | ~4.7 MB | Machine-readable, same data |

Both files carry identical information. The Markdown version is for reading and
diffing; the JSON version is for programmatic use — feeding a NotebookLM/Obsidian
import, an embedding pipeline, or any other tooling that wants structured input.

## What's inside

| Part | Contents |
|---|---|
| 1 — Repository snapshot | Every file on `main`: 226 text files inlined verbatim, 22 binary assets manifested with size + SHA-256 |
| 2 — Chat session outputs | One section per branch (29 sessions). Each carries the session's pull-request description, its commits, and the full text of every file it added or changed relative to its merge base |
| 3 — Live session transcript | The Claude Code conversation that produced the export — prompts, replies, tool calls, tool results |
| 4 — Commit history | All commits reachable from `main` |
| 5 — Pull request index | Every PR with its full description |

Each branch under `claude/…` or `copilot/…` is one agent chat session, so "every
chat" and "every branch" are the same list. Sessions whose work was already merged
show zero output files — their content appears in Part 1 instead.

### Binary assets

PNG charts and `PowerToys_AI_Workflow.pptx` are listed with size and SHA-256 but
not base64-inlined, which keeps the export readable and diffable. Retrieve any of
them with:

```bash
git show <ref>:<path>
```

### Prior exports are never inlined

This exporter's own output files are manifested with size and SHA-256 but never
inlined, so regenerating does not fold the previous export into the new one and
grow it without bound. They appear as `kind: "export-artifact"`. The paths are
derived from `--out-dir` and `--basename`, or set explicitly with `--self-path`.

Note that `tools/export_repo_and_chats.py` *is* inlined and contains the export's
own header as a template string. That is the generator's source, not recursion.

## Relationship to `exports/`

There are two export directories, from two sessions that answered the same request
in parallel on 2026-08-05:

| Directory | Origin | Contents |
|---|---|---|
| `export/` (this one) | Claude Code, PR #22 | Complete — every file's full text, every session's outputs, verified against git |
| `exports/` | a parallel multi-agent session, on `main` | Interim — a structure summary and a clarification-branch document; it did not inline file contents |

They do not overlap or conflict. If the complete export is the one worth keeping,
`exports/` can be removed; that is a call for the repository owner, not something
done here.

## Regenerating

```bash
# Pull request metadata is optional but fills in Part 5 and each session's summary.
gh pr list --state all --limit 100 \
  --json number,title,body,state,merged,url,user,headRefName,baseRefName,\
createdAt,mergedAt,closedAt,additions,deletions,changedFiles > /tmp/prs.json

git fetch origin --prune

python3 tools/export_repo_and_chats.py \
  --out-dir export \
  --ref origin/main \
  --prs /tmp/prs.json \
  --transcript-dir ~/.claude/projects/<project-slug> \
  --repository faraazxxx-ui/claude- \
  --visibility public
```

Every flag except `--out-dir` is optional. With no `--prs` the PR index is empty
and sessions fall back to their commit messages; with no `--transcript-dir` Part 3
is omitted. Git data alone is enough for a complete file export.

Note: `--prs` expects GitHub's REST shape (`head.ref`, `html_url`, `created_at`).
The `gh` command above uses GraphQL field names, so map them across, or export the
same data from the GitHub API / MCP `list_pull_requests`, which already matches.

## Verifying fidelity

Every inlined file records its SHA-256, so the export can be checked against git:

```bash
python3 - <<'PY'
import json, hashlib, subprocess
d = json.load(open('export/REPO_AND_CHAT_EXPORT.json'))
bad = 0
for f in d['repository_snapshot']['files']:
    blob = subprocess.check_output(['git', 'show', f"origin/main:{f['path']}"])
    if hashlib.sha256(blob).hexdigest() != f['sha256']:
        print('MISMATCH', f['path']); bad += 1
print(f"{len(d['repository_snapshot']['files'])} files checked, {bad} mismatches")
PY
```

## A note on contents

This repository is **public**, and this export concentrates everything in it into
two files — including active litigation strategy, medical and health records, and
personal financial material. Consolidation makes that material considerably easier
to find and read in bulk than it is when scattered across 248 files and 29
branches. Worth deciding deliberately whether these two files belong in a public
repository, and whether the repository itself should stay public.
