# Validation report — Lunar Rhythm & Intentional Blocks

Generated 2026-10-11 18:31 EDT · 238 days (2026-10-11 → 2027-06-05)

## 1. Prayer times: Aladhan (ISNA, method=2) vs independent local PrayTimes port

Difference = Aladhan − local, in whole minutes. Both round to the nearest minute, so ±1 min is rounding noise.

| Prayer | days | max |diff| | mean |diff| | histogram (diff: count) | days with |diff| > 1 min |
|---|---|---|---|---|---|
| Fajr | 238 | 1 | 0.05 | -1: 11, +0: 226, +1: 1 | none |
| Sunrise | 238 | 1 | 0.03 | -1: 5, +0: 231, +1: 2 | none |
| Dhuhr | 238 | 0 | 0.00 | +0: 238 | none |
| Asr | 238 | 1 | 0.62 | -1: 106, +0: 90, +1: 42 | none |
| Maghrib | 238 | 1 | 0.03 | -1: 3, +0: 231, +1: 4 | none |
| Isha | 238 | 1 | 0.07 | -1: 16, +0: 222 | none |

**Verdict: PASS** (rubric: every prayer, every day within 2 minutes of an independent computation).

## 2. Hijri dates: Aladhan HJCoSA vs Umm al-Qura (hijridate)

238 days checked · 0 mismatching day(s).


Anchor dates used (Aladhan HJCoSA): 1 Ramadan 1448 = 2027-02-08 · Eid al-Fitr = 2027-03-09 · 1 Dhul-Hijjah = 2027-05-07 · Arafah = 2027-05-15 · Eid al-Adha = 2027-05-16 · 1 Muharram 1449 = 2027-06-06.

Local moon sighting (e.g., Fiqh Council / local masjid announcements) can shift a month start by ±1 day; only the all-day anchor/header/milestone events would move. All timed blocks are solar.

## 3. Structural checks

- Every block has end > start on every day (asserted in build).
- No block crosses the DST transitions (2026-11-01 02:00, 2027-03-14 02:00); offsets come from the data's ISO-8601 strings.
- Lunar anchors generated: 8 → 2026-10-12 (1 Jumada al-Ula), 2026-11-11 (1 Jumada al-Akhirah), 2026-12-10 (1 Rajab), 2027-01-09 (1 Sha'ban), 2027-02-08 (1 Ramadan), 2027-03-09 (1 Shawwal), 2027-04-08 (1 Dhul-Qi'dah), 2027-05-07 (1 Dhul-Hijjah)
- Moon phase on each 1st is near new moon (phase < 0.12 or > 0.93): PASS
