# Why filenames must not claim to be final

**The short version: 12% of the files in this repository assert in their own name that they are the
last word — `FINAL`, `PERFECTED`, `MASTER`, `_v4`. Every one of those claims has already been
falsified by a later file. The naming convention is not cosmetic; it is what makes the corpus
unusable, because when five files claim to be canonical, none of them is.**

---

## The measurement

From `brain/_forensics/files_report.md`, computed over this repository:

| Signal | Count |
|---|---|
| Files carrying a finality or version token | 29 of 242 (12.0%) |
| Byte-identical duplicates at different paths | 3 groups |
| Version families (one idea, several competing files) | 5, covering 14 files |

The health analysis exists as `health_analysis/`, `health_analysis_v2/`,
`autonomic_intelligence_v3/`, and `clinical_report_v4/`. Four generations, four directories, each
one written by a session that could not find the previous one.

`red_team_analysis` exists in four places. `PERFECTED_MASTER_REPORT.md` and `PERFECTED_REPORT.md`
and `master_report.md` are three different documents.

## Why it happens

It is not carelessness. It is the rational local move.

A new session cannot find the old file. Overwriting something you cannot fully read feels
dangerous. So you write a new one — and to signal that *this* one is the good one, you put the claim
in the name. `PERFECTED_`. `FINAL_`. `_v2`.

Every one of those names is a message to a future reader saying *stop looking, this is the one*. And
every one is wrong within a month, because the next session cannot find it either and writes
`_v3`.

**The finality claim is a symptom of a missing address, not of poor discipline.** Fix the address
and the symptom goes.

## The rule

Plain noun. No version. No adjective.

| Instead of | Write |
|---|---|
| `PERFECTED_HEALTH_REPORT_v4.md` | `health-analysis.md` |
| `FINAL_OPTIMIZED_PROMPTS.md` | `prompts.md` |
| `red_team_analysis_v2.md` | `red-team-review.md` |
| `SECOND_BRAIN_ARCHITECTURE.md` | `second-brain.md` |

The page is always current, because it is always the page. History lives in `git log`, which is what
git is for and does better than a filename ever will.

## What to do with the ones that already exist

**Do not delete them.** They contain real work, some of it is cited elsewhere, and deleting is
irreversible in a way that promoting is not.

Promote instead:

1. Pick the best copy in the family.
2. Create the canonical page in `brain/` with the plain-noun name.
3. In that page, state what it supersedes and link to the originals.
4. Leave the originals where they are, as history.

The originals stop being competing claims the moment one page outranks them and says so.
`brain/_forensics/files_report.md` lists every family that still needs this treatment.

## Enforcement

`CLAUDE.md` forbids finality tokens in new filenames, so every future session inherits the rule
without you having to restate it. `tools/corpus_forensics.py files .` re-measures the rate, so the
number is visible rather than vibes.

If the 12% is not falling over the next few months, the rule is not being read — check that
`CLAUDE.md` is at the repository root, since that is what makes Claude Code load it automatically.

## Links

- [[index]] · [[wiki-method]] · [[adhd-operating-system]] · [[second-brain]]
