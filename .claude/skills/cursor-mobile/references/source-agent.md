# Source agent

This skill was requested from Cursor Mobile on 2026-08-27.

**Request (verbatim intent):** add the linked run’s work on a branch named
“cursor mobile skill.”

**Linked run:** [bc-01a04166-0796-727e-93d6-04dfd0978582](https://cursor.com/agents/bc-01a04166-0796-727e-93d6-04dfd0978582)

**This run:** [bc-01a0419f-0269-763a-a654-4ca04b0f32b1](https://cursor.com/agents/bc-01a0419f-0269-763a-a654-4ca04b0f32b1)
(name: “Cursor mobile skill”, `source: mobile`, repo `faraazxxx-ui/claude-`)

## Import attempt

`batch-fetch-details` for `bc-01a04166-0796-727e-93d6-04dfd0978582` returned
not found / not accessible. `list-cloud-agents` in this environment only
surfaced the current run. The linked conversation could not be copied.

## What was added instead

A durable **cursor-mobile** agent skill so every future iOS/cloud run in
this repo has:

- mobile operating defaults (branch + PR, short replies, artifacts)
- an import workflow for `cursor.com/agents/bc-…` links
- the iOS capability/limit map from Cursor’s published docs

If the linked agent later becomes readable, merge its specific files on
top of this skill rather than replacing the playbook.
