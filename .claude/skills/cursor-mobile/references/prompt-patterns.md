# Prompt patterns (voice, links, photos)

The user is a verbal thinker. Mobile prompts are often dictated, incomplete,
or a screenshot plus a sentence. Translate, then execute.

## Extract, then go

From the raw message, write (internally):

- **Core idea** — one sentence
- **Implied tasks** — branch, PR, files, skill name
- **Named nouns** — agent URLs, repo, branch name, people, case numbers

Do not play back a long “I heard…” block on a phone unless one fact is
actually blocking. Prefer doing the work.

## Pattern: “Add this” + agent URL

```
Can you add this in a branch called <name>.
https://cursor.com/agents/bc-…
```

Meaning:

1. Open branch `<name>` (mapped to the required `cursor/…-32b1` form).
2. Import the linked agent’s deliverable (skill, docs, code, PR contents).
3. If the transcript cannot be fetched, still create the named artifact
   from the request title + this repo’s conventions, and record the URL.

## Pattern: voice dump

Rambling medical, legal, or ops thoughts. Use the same split as the
voice-first verbal-thinker skill: core idea / implied tasks / one blocker.
Then route:

- Code or repo change → this cloud agent (this skill)
- Multi-platform prompt rewrite → `verbal-prompt-optimizer`
- Health export analysis → `health-data-analyst`
- Case strategy → `apex-legal-strategy`

## Pattern: camera / Design Mode

A photo of a UI, a whiteboard, a lab printout, or a marked-up screenshot
**is** the spec. Implement against the image. Do not ask them to retype it.

## Pattern: “put it on a branch so I can merge from here”

They are staying on the phone. Branch + PR is mandatory even for a single
markdown file.

## Phone-friendly prompts the user can reuse

**New skill from a thought**

> Add a Cursor skill called \<name\> in `.cursor/skills/\<name\>/` and open a
> PR. I’ll review on my phone.

**Continue another agent**

> Here’s the agent. Finish what it started and put it on branch \<name\>.
> https://cursor.com/agents/bc-…

**Hands-free bug**

> (photo attached) This is broken. Fix it, verify, open a PR.

**Keep working after I lock the phone**

> Open a draft PR as soon as you have a first commit. I’ll follow from
> Live Activities. Keep going until the PR is ready to merge.
