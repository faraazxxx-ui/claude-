---
name: legal-endeavors
description: Comprehensive litigation support for Mohammed Faraaz Rahman, M.D. v. United Health Services Hospitals, Inc. et al., Case No. 3:26-CV-00197 (AJB/ML). Use when the user requests help with legal filings, motions, discovery, strategy, deadline tracking, evidence management, damages calculations, or any task referencing "the case," "UHS," or the named defendants.
---

# Legal Endeavors: Rahman v. UHS et al.

Comprehensive litigation support skill for the federal civil rights and tort action **Mohammed Faraaz Rahman, M.D. v. United Health Services Hospitals, Inc. et al.**, Case No. 3:26-CV-00197 (AJB/ML), Northern District of New York.

## When to Use This Skill

Use this skill when the user requests assistance with any of the following:

- Drafting, reviewing, or editing legal filings, motions, or correspondence for the Rahman v. UHS case
- Analyzing defendants' filings, motions, or discovery responses
- Tracking deadlines, evidence, or case milestones
- Researching legal theories, case law, or statutory authority relevant to the claims
- Preparing discovery requests, deposition outlines, or trial preparation materials
- Calculating or updating damages figures
- Generating status reports or strategy updates
- Any task referencing "the case," "UHS," "legal," or the named defendants

## Case Summary

Dr. Mohammed Faraaz Rahman, an Internal Medicine physician who graduated from UHS (Binghamton, NY) in June 2024, was subjected to fabricated criminal charges arising from a personal vendetta by a fellow resident (Dr. Sundas Rashid), facilitated by institutional discrimination at UHS. Despite complete vindication via a NOT GUILTY verdict (August 2025), the 18-month ordeal destroyed his career trajectory, forced his father to provide over $84,000 in emergency financial support, and caused cascading damages exceeding $4.2 million.

**Current Posture**: Verified Complaint filed January 2026 (state court); removed to federal court February 2026; Defendants answered March 9, 2026. Case is in early litigation / pre-discovery phase.

## Workflow

Legal tasks for this case follow this general workflow:

1. **Context Loading** — Read the relevant reference file(s) below before drafting or analyzing
2. **Research** — If the task requires case law or statutory research, conduct it using search tools
3. **Drafting** — Use the templates and filing generator script as starting points
4. **Review** — Cross-check all factual claims against the case-context reference
5. **Deadline Check** — Run the deadline tracker to verify no deadlines are missed

## Reference Files

Read these files as needed based on the task at hand. Do NOT read all files for every task.

| File | When to Read | Contents |
|------|-------------|----------|
| [case-context.md](references/case-context.md) | **Always read first** for any case-related task | Parties, timeline, causes of action, evidence inventory, damages, defendants' answers, deadlines |
| [defense-analysis.md](references/defense-analysis.md) | When analyzing or countering defendants' arguments | All 17 affirmative defenses with counter-strategies; counter-strategy matrix |
| [litigation-playbook.md](references/litigation-playbook.md) | When planning next steps, motions, or strategy | Three-phase strategy; discovery priorities; motion roadmap; settlement framework |

## Scripts

| Script | Usage | Command |
|--------|-------|---------|
| `deadline_tracker.py` | Track and manage case deadlines | `python3 scripts/deadline_tracker.py` |
| `deadline_tracker.py --urgent` | Show only deadlines within 30 days | `python3 scripts/deadline_tracker.py --urgent` |
| `deadline_tracker.py --add` | Add a new deadline | `python3 scripts/deadline_tracker.py --add "Description" "YYYY-MM-DD" "category"` |
| `generate_filing.py` | Generate filing templates | `python3 scripts/generate_filing.py --type motion --title "Title" --output file.md` |
| `generate_filing.py --list` | List available templates | `python3 scripts/generate_filing.py --list` |

Run all scripts from the skill directory: `cd /home/ubuntu/skills/legal-endeavors && python3 scripts/<script>.py`

## Templates

| Template | Purpose |
|----------|---------|
| [evidence_checklist.md](templates/evidence_checklist.md) | Track collection, authentication, and filing status of all evidence |
| [discovery_requests.md](templates/discovery_requests.md) | Pre-drafted interrogatories, RFPs, and RFAs organized by defendant |

## Key Legal Theories

These are the primary legal frameworks driving the case strategy:

1. **Cat's Paw Liability** (Staub v. Proctor Hospital): UHS adopted a personal vendetta as institutional policy without independent investigation
2. **Apex Doctrine Defeat**: FMLA email proves Program Director Ali had unique personal knowledge, defeating claims of ignorance
3. **Business Judgment Piercing**: Forcing a septic resident to work with a PICC line violates medical standards of care
4. **Division of Guilt**: Naming individuals forces UHS to choose between defending them (owning misconduct) or abandoning them (validating claims)
5. **Continuing Violation Doctrine**: Discriminatory acts continued through post-graduation record obstruction (July 2024+)

## Critical Deadlines

**URGENT**: Malicious Prosecution SOL expires approximately August/September 2026 (1 year from acquittal). Run `python3 scripts/deadline_tracker.py --urgent` for current status.

## Important Rules

1. **Never delete case files.** Move completed items to archive.
2. **Cite specific evidence** from the case-context reference when drafting any filing.
3. **Verify all dates** against the chronological timeline before including in any document.
4. **Check deadlines** before recommending any action that involves filing or service.
5. **Maintain attorney-client privilege** — mark all work product as "Attorney Work Product — Privileged & Confidential."
6. **Cross-reference defendants' answers** when drafting discovery or motions — use their specific denials and admissions.
