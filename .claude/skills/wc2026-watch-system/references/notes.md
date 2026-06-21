# WC2026 Watch System — reference notes

## Color scheme (escalating by stage, with elevation overrides)

| Stage | Google colorId | Name / xlsx fill |
|---|---|---|
| Group (A–L) | 2 | Sage — calm green (`33B679`) |
| Round of 32 | 5 | Banana — yellow (`F6BF26`) |
| Round of 16 | 6 | Tangerine — orange (`F4511E`) |
| Quarter-final | 3 | Grape — purple (`8E24AA`) |
| Semi-final | 9 | Blueberry — deep blue (`3F51B5`) |
| Third place | 8 | Graphite — distinct/somber (`616161`) |
| Final | 11 | Tomato — red, most distinct (`D50000`) |

**Elevation overrides** (applied after stage color):
- **Any USA match** → colorId **4 Flamingo** (`E67C73`) so the host nation pops at
  every stage. Exception: if the USA reaches the **Final**, the Final stays Tomato —
  it is the single most-distinct event.
- **MetLife / NY-NJ matches** get a "📍 Local to you (NY/NJ)" line in the description
  (color unchanged).

## Time handling
- `kickoff_utc` is the only time stored (ISO-8601, `Z`). ET is derived with
  `zoneinfo("America/New_York")`, so summer DST (UTC−4) is automatic — never
  hand-enter Eastern times. End = +2h (group) / +2.5h (knockout).

## Idempotent calendar sync
- Each event carries a hidden marker `WC2026-Mnnn` in its description and the `.ics`
  uses `UID:wc2026-mnnn@rahman`. The sync matches existing events by this marker
  (falling back to title+date for events created by other tools, e.g. an earlier
  Le Chat/Mistral run) and updates in place, creating only what's missing and
  deleting true duplicates.

## Sources (record retrieval date on every refresh)
See `sources` and `retrieved` fields inside `scripts/wc2026_data.json`.
Priority: FIFA.com / official Canada-Mexico-USA 2026 site → ESPN → host-city pages,
cross-checked against the Wikipedia "2026 FIFA World Cup" fixture table.
