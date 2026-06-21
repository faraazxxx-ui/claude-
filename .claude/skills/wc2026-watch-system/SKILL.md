---
name: wc2026-watch-system
description: >
  Stands up and refreshes a personal FIFA World Cup 2026 watch system for the user
  (Upper East Side, NYC; non-drinker; calendar dr.faraaz.rahman@gmail.com). Produces
  a verified 104-match schedule (xlsx), color-coded Google Calendar events for every
  upcoming match, an importable .ics backup, and an NYC non-drinker watch guide with
  live standings + bracket. Use when the user wants the World Cup schedule, calendar,
  or watch guide created OR refreshed as the knockout bracket fills in.
---

# FIFA World Cup 2026 Watch System

A reusable, **idempotent** pipeline. Re-running it as results come in updates the
artifacts and the calendar in place — it never creates duplicate events.

## Files
- `scripts/wc2026_data.json` — single source of truth: all 104 matches
  (`kickoff_utc`, stage, teams/placeholders, city, stadium), current `standings`,
  `venues_guide`, `fan_festival`, `sources`, and `retrieved` date.
- `scripts/generate.py` — reads the JSON; writes `outputs/wc2026_schedule.xlsx`,
  `outputs/wc2026.ics`, `outputs/wc2026_events.json`, `outputs/nyc_watch_guide.md`.
  Converts UTC→America/New_York with `zoneinfo` (DST-safe) and assigns colors.
- `scripts/requirements.txt` — `openpyxl`.
- `references/notes.md` — color scheme + sync/marker conventions.

## Refresh workflow

1. **Update the data** (`scripts/wc2026_data.json`). Re-research results since the
   last run using the source priority **FIFA.com / official CMA 2026 site → ESPN →
   host-city pages**, cross-checked against Wikipedia's fixture table. Update group
   `standings`, fill in knockout `team_a`/`team_b` as the bracket resolves, and set
   `retrieved` to today plus the `sources` URLs. Keep `kickoff_utc` authoritative;
   never hand-enter Eastern times.

2. **Generate artifacts**:
   ```bash
   pip install -r scripts/requirements.txt
   python scripts/generate.py           # writes into ../../../outputs by default
   ```
   The script asserts the match set is exactly 1..104 and that the `.ics` VEVENT
   count equals the upcoming-match count.

3. **Sync Google Calendar (idempotent)** on `dr.faraaz.rahman@gmail.com` using
   `outputs/wc2026_events.json`:
   - `list_events` over the tournament window (next event date → 2026-07-19).
   - Build an index of existing events that look like WC2026 events: key first by the
     hidden `WC2026-Mnnn` marker in the description; for events created by other tools
     (e.g. a prior Le Chat/Mistral run, which won't have the marker) fall back to
     matching on normalized title or (teams + date).
   - For each event in `wc2026_events.json`: if a match exists, `update_event`
     (title, description, start/end in `America/New_York`, `location`, `colorId`);
     otherwise `create_event`. If several existing events map to the same match,
     keep one and `delete_event` the rest.
   - Result invariant: **exactly one** correctly-colored event per upcoming match,
     no duplicates. Re-running must produce zero new events.

## Color scheme
Group=Sage(2) → R32=Banana(5) → R16=Tangerine(6) → QF=Grape(3) → SF=Blueberry(9) →
3rd=Graphite(8) → Final=Tomato(11). USA matches elevated to Flamingo(4) at every
stage (except the Final, which stays Tomato). MetLife/NY-NJ matches flagged
"📍 Local to you" in the description. See `references/notes.md`.

## Self-check before finishing
- xlsx has 104 rows; match numbers unique and complete.
- Spot-check ET conversions (opener Mexico vs South Africa 3:00 PM ET Jun 11;
  Final 3:00 PM ET Jul 19) — no off-by-one.
- After sync: one event per upcoming match, correct color; re-run yields no new dupes.
- Standings/bracket cite the retrieval date; venues genuinely suit a non-drinker.
