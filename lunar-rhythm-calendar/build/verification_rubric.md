# Verification rubric — Google Calendar population

Graded pass/fail per line by a separate verifier that did not build the events.
Source of truth: `build/timetable.json` (per-day events) and `build/payloads/index.json` (expected counts).

| # | Line | How to check | Pass condition |
|---|---|---|---|
| 1 | Per-batch counts | For each batch in `payloads/index.json`, `list_events` on the target calendar from `first_day 00:00` to `last_day+1 00:00` (America/New_York), paging through all pages, counting only events whose description contains `LRIB-ID:`. | Count equals `event_count` for every batch; total equals 3,116. |
| 2 | No duplicates | Within each batch listing, collect the `LRIB-ID` values. | Every `LRIB-ID` appears exactly once. |
| 3 | Block times to the minute | Sample days: 2026-10-11, 2026-10-31, 2026-11-01, 2026-12-10, 2027-02-08, 2027-03-13, 2027-03-14, 2027-05-16, 2027-06-05. Compare each B0–B6 start/end with `timetable.json` `blocks`. | All starts/ends match exactly (local wall time). |
| 4 | Prayer events | Same sample days: five `[ ] 🕌` events start at the adhan times in `timetable.json` `timings`, each 25 min long, title ends with `by HH:MM` equal to `prayer_windows.<name>.end`. | All five per sample day correct. |
| 5 | Colours | Same sample days: colorId B0=3, B1=7, B2=5, B3=6, B4=11, B5=9, B6=8, prayers=10, header=1, anchors=2, milestones=4 (DST notes 8). | No mismatches. |
| 6 | Reminders | Same sample days: B0 [0]; B1 none; B2 [35,10]; B3 [10]; B4 [10]; B5 [25]; B6 [10]; prayers [0]; all-day events none. `useDefaultReminders` false everywhere. | No mismatches. |
| 7 | All-day structure | Daily header exists on every sample day; anchors exist on 2026-10-12, 2026-11-11, 2026-12-10, 2027-01-09, 2027-02-08, 2027-03-09, 2027-04-08, 2027-05-07; milestones on 2026-10-11, 2027-01-05, 2027-01-23, 2027-02-27, 2027-03-01, 03-03, 03-05, 03-07, 2027-05-15, 05-16, 05-17 (3-day), 2027-06-05, DST notes 2026-10-31 and 2027-03-13. | All present, as all-day events, free availability. |
| 8 | Time zone | Sample events' `start.timeZone` is `America/New_York`; the EDT/EST offsets flip between 2026-10-31 and 2026-11-01 and between 2027-03-13 and 2027-03-14. | Offsets correct on both sides of each DST change. |
| 9 | Descriptions intact | Sample B2 description contains the Rule of 3 template, the Hijri header line, the WINDOW line and the `LRIB-ID`; newlines preserved (not collapsed). | Present and readable. |

Rules for the verifier: report each line as PASS or FAIL with the evidence (counts, the mismatching IDs), no percentages or confidence scores. Any FAIL must name the exact `LRIB-ID`s or batch numbers so the fix is mechanical.
