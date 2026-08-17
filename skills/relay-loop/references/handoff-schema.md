# Handoff state schema

One JSON file per mission (e.g. `<workdir>/data/handoff-state.json`), updated at every gate. A brand-new
agent or session must be able to resume from this file + the canon files alone.

```json
{
  "mission": "one sentence — what done looks like",
  "done": ["completed stages with one-line outcomes (include check verdicts)"],
  "in_progress": "current stage",
  "decisions": ["binding choices made along the way, with rationale — a new agent must not re-litigate these"],
  "canon_files": ["paths to the structured files that are the single source of truth"],
  "open_questions": ["unresolved items a later stage or the human must settle"],
  "next_actions": ["ordered; first item is what a resuming agent does immediately"],
  "critical_deadlines": {"name": "date + consequence"}
}
```

Rules:
- Compact. The handoff carries **pointers and verdicts**, never payloads.
- `decisions` is append-only. Reversing a decision is itself a decision (append it with the reason).
- Update BEFORE starting risky stages, not only after finishing — a crash mid-stage must not lose the map.
- On escalation to the human, the handoff file is the briefing: it must read standalone.
