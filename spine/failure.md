# Failure

What went wrong, what it cost, and what would have caught it. Append only.

The entry that matters is the third column. A failure log that only records what broke turns into a list of grievances; one that records the missing check turns into the next gate.

---

## 2026-08-29 — A briefing doc gave install instructions that could not work

**What happened.** A prior session produced a confident setup guide for local voice dictation. Eight of its claims were wrong: the install method (`git clone` + `pip install` for something that installs through a plugin marketplace), the hotkey, the prerequisite, the model, the platform scope, and a caveat imported wholesale from a different tool. It also omitted that the thing runs as a daemon and does nothing until started.

**What it cost.** An afternoon, and — worse — trust in instructions that cannot be self-audited. Dr. Rahman does not code. He cannot tell a working command from a broken one before it fails, which means a confident wrong instruction costs him strictly more than an admitted uncertainty would have.

**Root cause.** Answered from recall, presented as verified. No source was consulted for any of the eight wrong claims. The tone carried no signal that recall was all it was.

**What would have caught it.** Reading the project's own README before writing a single command. That is now the standing rule at the top of `skills/voice-capture-setup/SKILL.md`, with a dated ledger in `references/verified_facts.md` so the check is inherited rather than repeated.

---

## 2026-08-29 — Gate 0 ran ungated, twice, without stopping

**What happened.** The orchestrator's first gate reads `hub.md`, `goal.md`, and `verify.md` before dispatch. None existed. Two full tasks ran anyway.

**What it cost.** Little this time — both tasks were verification work that happened to fit any reasonable goal. That is luck, not design.

**Root cause.** The gate specified files to read but no behaviour for their absence, so "not found" silently degraded to "proceed."

**What would have caught it.** Nothing in the system. A missing gate is invisible by construction — it does not fail, it just does not run. The files now exist, and `goal.md` announces its own UNSET status rather than sitting empty, so the next session sees a stated gap instead of an absence it has to notice on its own.
