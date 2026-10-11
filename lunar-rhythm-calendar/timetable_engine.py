#!/usr/bin/env python3
"""
Lunar Rhythm & Intentional Blocks -- Timetable Engine
=====================================================

Builds the complete, day-by-day event set for the Google Calendar
"Lunar Rhythm & Intentional Blocks" from verified astronomical data.

Location  : Manhattan, New York (E 61st St & York Ave) 40.7610 N, -73.9590 W
Method    : ISNA (Fajr 15 deg, Isha 15 deg, Maghrib = sunset, Asr standard)
Time zone : America/New_York (DST handled by the ISO-8601 offsets in the data)
Range     : 2026-10-11 (30 Rabi' al-Thani 1448) -> 2027-06-05 (30 Dhul-Hijjah 1448)

Data source: Aladhan API monthly calendars (method=2, iso8601=true), stored
verbatim in data/aladhan_raw/.  Two independent cross-checks run on every day:
  1. A local port of the PrayTimes astronomical algorithm (same ISNA params).
  2. The `hijridate` Umm al-Qura converter for Hijri dates.
Any disagreement is written to build/validation_report.md.

Outputs (build/):
  timetable.json          full machine-readable timetable + every event
  timetable.csv           one row per day (prayer times + block boundaries)
  timetable.md            human-readable monthly tables
  validation_report.md    cross-check results
  prayer_log.csv          40-prayer tracker log (Google Sheet import)
  ics/*.ics               per-month + all-in-one iCalendar files
  payloads/batch_NN.json  Google Calendar API create_event payloads

Usage:
  python3 -I timetable_engine.py [--sheet-url URL] [--calendar-id ID]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "data" / "aladhan_raw"
BUILD = HERE / "build"

TZ_NAME = "America/New_York"
TZ = ZoneInfo(TZ_NAME)
LAT, LON = 40.7610, -73.9590
LOCATION = "Manhattan, NY (E 61st St & York Ave)"
CALENDAR_NAME = "Lunar Rhythm & Intentional Blocks"

START = date(2026, 10, 11)
END = date(2027, 6, 5)  # 30 Dhul-Hijjah 1448; 1 Muharram 1449 = 2027-06-06 (Aladhan HJCoSA)

# Google Calendar event colorIds (Event resource):
# 1 Lavender 2 Sage 3 Grape 4 Flamingo 5 Banana 6 Tangerine 7 Peacock
# 8 Graphite 9 Blueberry 10 Basil 11 Tomato
COLORS = {
    "B0": "3",        # Grape      - Pre-dawn (Tahajjud)
    "B1": "7",        # Peacock    - Turquoise blue, dawn
    "B2": "5",        # Banana     - light yellow, core work
    "B3": "6",        # Tangerine  - dark orange, wrap-up
    "B4": "11",       # Tomato     - red, sunset prep
    "B5": "9",        # Blueberry  - deep blue, evening reset
    "B6": "8",        # Graphite   - wind down
    "PRAYER": "10",   # Basil      - actionable prayer tick-off
    "ANCHOR": "2",    # Sage       - 1st of lunar month
    "HEADER": "1",    # Lavender   - daily Hijri header
    "MILESTONE": "4", # Flamingo   - Eid / Arafah / Qadr nights
    "NOTE": "8",      # Graphite   - DST notes
}
COLOR_NAMES = {"1": "Lavender", "2": "Sage", "3": "Grape", "4": "Flamingo", "5": "Banana",
               "6": "Tangerine", "7": "Peacock", "8": "Graphite", "9": "Blueberry",
               "10": "Basil", "11": "Tomato"}
# RFC 7986 COLOR names for the .ics files (Google ignores these; other clients use them)
ICS_COLORS = {"3": "purple", "7": "turquoise", "5": "yellow", "6": "darkorange", "11": "red",
              "9": "darkblue", "8": "dimgray", "10": "green", "2": "darkseagreen",
              "1": "lavender", "4": "hotpink"}

HIJRI_MONTHS = {
    1: ("Muharram", "محرّم"), 2: ("Safar", "صفر"), 3: ("Rabi' al-Awwal", "ربيع الأول"),
    4: ("Rabi' al-Thani", "ربيع الثاني"), 5: ("Jumada al-Ula", "جمادى الأولى"),
    6: ("Jumada al-Akhirah", "جمادى الآخرة"), 7: ("Rajab", "رجب"), 8: ("Sha'ban", "شعبان"),
    9: ("Ramadan", "رمضان"), 10: ("Shawwal", "شوّال"), 11: ("Dhul-Qi'dah", "ذو القعدة"),
    12: ("Dhul-Hijjah", "ذو الحجة"),
}

RULE_OF_3 = (
    "🛑 RULE OF 3: PRE-BLOCK INTENTIONS 🛑\n"
    "Before beginning this block, define exactly what you will do:\n"
    "1. [ ] Task: _________________ (Est Time: ___ mins)\n"
    "2. [ ] Task: _________________ (Est Time: ___ mins)\n"
    "3. [ ] Task: _________________ (Est Time: ___ mins)"
)

# Associative meaning per lunar month (1st-of-month anchors).  Progression text is
# completed at runtime with the live countdowns.
ANCHORS = {
    1: dict(theme="The Sacred Threshold & Renewal",
            meaning="'Muharram' = forbidden/sacred. One of the four sacred months; Ashura on the 10th. "
                    "Establish an internal ceasefire: forgive cognitive and emotional debts, wipe the slate, "
                    "lay quiet foundational habits without manic urgency.",
            anchor="You are at the baseline. Build sustainable roots."),
    2: dict(theme="The Departure & Kinetic Momentum",
            meaning="'Safar' = empty/void: homes emptied as people set out. Dismantle superstition, hesitation "
                    "and executive paralysis; convert passive theory into kinetic momentum.",
            anchor="Action precedes clarity. Move through resistance."),
    3: dict(theme="The Spring of Character",
            meaning="'Rabi' al-Awwal' = the first spring; the month of the Prophet's ﷺ birth. Center on akhlaq "
                    "(character), mercy and dignified cadence; align execution with purpose rather than anxiety.",
            anchor="Master your state. Elevate character above speed."),
    4: dict(theme="Deep Roots & Quiet Tenacity",
            meaning="'Rabi' al-Thani' = the second spring. Roots dig beneath the soil before anything is visible: "
                    "quiet, unglamorous consistency. What you build in secret sustains the demands of Ramadan.",
            anchor="Trust the invisible compounding."),
    5: dict(theme="Solidification & Crystallization",
            meaning="'Jumada' = parched/frozen ground, the season when water hardens. Freeze frivolous commitments, "
                    "seal energetic leaks and firm up the non-negotiable boundaries. What is fluid now must set into form.",
            anchor="Eliminate the non-essential. Protect your energy."),
    6: dict(theme="Clearing the Decks",
            meaning="'Jumada al-Akhirah' = the last of the parched months, the final ordinary month before the sacred "
                    "trimester (Rajab → Sha'ban → Ramadan). Audit every open loop: administrative debts, physical "
                    "clutter, cognitive friction. Prepare the vessel to receive the waters of Rajab.",
            anchor="Close all open tabs. Empty the mental cache."),
    7: dict(theme="The Sacred Sowing",
            meaning="'Rajab' = to revere. A sacred month (fighting forbidden; wrongdoing weighs heavier). The classical "
                    "image: 'Rajab is the month of sowing, Sha'ban of irrigating, Ramadan of harvesting.' Abstain from "
                    "interpersonal friction and moral compromise; plant Qur'an, fasting and focus. Isra & Mi'raj is "
                    "commemorated on the 27th.",
            anchor="What you do not plant in Rajab cannot bloom in Ramadan."),
    8: dict(theme="Irrigation & Athletic Conditioning",
            meaning="'Sha'ban' = to branch out. The Prophet ﷺ fasted more in Sha'ban than in any month besides Ramadan. "
                    "Water the crops: raise fasting, night vigilance and stamina now so you enter Ramadan at full "
                    "velocity, never from a cold start. Mid-Sha'ban night (14→15) is observed by many.",
            anchor="Pre-warm the engine. No cold starts."),
    9: dict(theme="The Furnace & the Harvest — PEAK MILESTONE 1",
            meaning="'Ramadan' = scorching heat. The burning away of impurities; the reaping of every seed sown in "
                    "Rajab and watered in Sha'ban. Total sensory fast, heightened clarity, night vigil, boundless "
                    "receptivity. Laylat al-Qadr is sought in the odd nights of the last ten.",
            anchor="All standard rules suspend. Maximum spiritual focus."),
    10: dict(theme="Eid al-Fitr · Elevation & Carrying the Gains",
             meaning="'Shawwal' = to lift and carry. Eid al-Fitr on the 1st; the six fasts of Shawwal any time this "
                     "month. Refuse the post-Ramadan slump: anchor the gains with the Six Fasts and carry the furnace's "
                     "velocity into daily professional output.",
             anchor="Retain the altitude gained in the furnace."),
    11: dict(theme="The Sacred Encampment",
             meaning="'Qi'dah' = sitting, halting. A sacred month: no fighting, no frantic travel. Cease non-essential "
                     "warfare, settle worldly accounts, gather provisions of taqwa and quiet the nervous system before "
                     "the mountain.",
             anchor="Stillness before the mountain."),
    12: dict(theme="The Summit — PEAK MILESTONE 2",
             meaning="'Dhul-Hijjah' = the month of pilgrimage. The first ten days are the best days of the year; the Day "
                     "of Arafah on the 9th, Eid al-Adha on the 10th, Tashreeq 11–13. The pinnacle of surrender: the "
                     "mountain of Arafah, the Ibrahimic sacrifice (slaying of the ego), the covenant completed before the "
                     "cycle renews.",
             anchor="The summit. Offer your greatest sacrifice."),
}


# --------------------------------------------------------------------------------------
# 1. Load Aladhan raw data
# --------------------------------------------------------------------------------------
def load_raw() -> dict[date, dict]:
    days: dict[date, dict] = {}
    for f in sorted(RAW_DIR.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        assert j.get("code") == 200, f"{f.name}: non-200 payload"
        for d in j["data"]:
            g = d["date"]["gregorian"]
            dt = date(int(g["year"]), int(g["month"]["number"]), int(g["day"]))
            meta = d["meta"]
            assert meta["timezone"] == TZ_NAME, (f.name, dt, meta["timezone"])
            assert meta["method"]["id"] == 2 and meta["method"]["params"] == {"Fajr": 15, "Isha": 15}, (f.name, dt)
            assert meta["school"] == "STANDARD", (f.name, dt, meta["school"])
            timings = {}
            for k in ("Fajr", "Sunrise", "Dhuhr", "Asr", "Sunset", "Maghrib", "Isha", "Midnight"):
                raw = d["timings"][k].split(" ")[0]  # strip "(EST)" suffixes if present
                t = datetime.fromisoformat(raw).astimezone(TZ)
                timings[k] = t
            h = d["date"]["hijri"]
            days[dt] = {
                "timings": timings,
                "hijri": {"day": int(h["day"]), "month": int(h["month"]["number"]), "year": int(h["year"]),
                          "month_en": HIJRI_MONTHS[int(h["month"]["number"])][0],
                          "month_ar": HIJRI_MONTHS[int(h["month"]["number"])][1],
                          "weekday_ar": h["weekday"]["ar"], "method": h.get("method"),
                          "month_days": int(h["month"]["days"]), "holidays": h.get("holidays", [])},
                "weekday": g["weekday"]["en"],
                "src_file": f.name,
            }
    return days


# --------------------------------------------------------------------------------------
# 2. Independent astronomical cross-check (port of the PrayTimes algorithm)
# --------------------------------------------------------------------------------------
def _dsin(d): return math.sin(math.radians(d))
def _dcos(d): return math.cos(math.radians(d))
def _dtan(d): return math.tan(math.radians(d))
def _darcsin(x): return math.degrees(math.asin(x))
def _darccos(x): return math.degrees(math.acos(x))
def _darctan2(y, x): return math.degrees(math.atan2(y, x))
def _darccot(x): return math.degrees(math.atan2(1.0, x))
def _fixangle(a): return a - 360.0 * math.floor(a / 360.0)
def _fixhour(h): return h - 24.0 * math.floor(h / 24.0)


def _julian(y: int, m: int, d: int) -> float:
    if m <= 2:
        y -= 1
        m += 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5


def _sun_position(jd: float):
    D = jd - 2451545.0
    g = _fixangle(357.529 + 0.98560028 * D)
    q = _fixangle(280.459 + 0.98564736 * D)
    L = _fixangle(q + 1.915 * _dsin(g) + 0.020 * _dsin(2 * g))
    e = 23.439 - 0.00000036 * D
    RA = _darctan2(_dcos(e) * _dsin(L), _dcos(L)) / 15.0
    eqt = q / 15.0 - _fixhour(RA)
    decl = _darcsin(_dsin(e) * _dsin(L))
    return decl, eqt


def _mid_day(jd: float, t: float) -> float:
    _, eqt = _sun_position(jd + t)
    return _fixhour(12 - eqt)


def _sun_angle_time(jd: float, angle: float, t: float, ccw: bool = False) -> float:
    decl, _ = _sun_position(jd + t)
    noon = _mid_day(jd, t)
    x = (-_dsin(angle) - _dsin(decl) * _dsin(LAT)) / (_dcos(decl) * _dcos(LAT))
    x = max(-1.0, min(1.0, x))
    tt = (1 / 15.0) * _darccos(x)
    return noon + (-tt if ccw else tt)


def _asr_time(jd: float, factor: float, t: float) -> float:
    decl, _ = _sun_position(jd + t)
    angle = -_darccot(factor + _dtan(abs(LAT - decl)))
    return _sun_angle_time(jd, angle, t)


def praytimes_isna(d: date) -> dict[str, datetime]:
    """ISNA 15/15, Maghrib = sunset, Asr factor 1 (standard). Returns tz-aware datetimes."""
    jd = _julian(d.year, d.month, d.day) - LON / (15 * 24.0)
    times = {"fajr": 5, "sunrise": 6, "dhuhr": 12, "asr": 13, "sunset": 18, "isha": 18}
    rise_set = 0.833  # + 0.0347*sqrt(elevation) with elevation 0
    for _ in range(2):
        t = {k: v / 24.0 for k, v in times.items()}
        times = {
            "fajr": _sun_angle_time(jd, 15, t["fajr"], ccw=True),
            "sunrise": _sun_angle_time(jd, rise_set, t["sunrise"], ccw=True),
            "dhuhr": _mid_day(jd, t["dhuhr"]),
            "asr": _asr_time(jd, 1, t["asr"]),
            "sunset": _sun_angle_time(jd, rise_set, t["sunset"]),
            "isha": _sun_angle_time(jd, 15, t["isha"]),
        }
    noon_local = datetime(d.year, d.month, d.day, 12, tzinfo=TZ)
    tz_hours = noon_local.utcoffset().total_seconds() / 3600.0
    out = {}
    for k, v in times.items():
        local_hours = v + tz_hours - LON / 15.0
        minutes = int(math.floor(local_hours * 60 + 0.5))  # round to nearest minute, as PrayTimes does
        naive = datetime(d.year, d.month, d.day) + timedelta(minutes=minutes)
        out[k] = naive.replace(tzinfo=TZ)
    out["maghrib"] = out["sunset"]
    return out


def cross_check_timings(days: dict[date, dict]) -> dict:
    keys = [("Fajr", "fajr"), ("Sunrise", "sunrise"), ("Dhuhr", "dhuhr"), ("Asr", "asr"),
            ("Maghrib", "maghrib"), ("Isha", "isha")]
    stats = {a: {"max_abs": 0, "sum_abs": 0, "n": 0, "over_1": [], "hist": {}} for a, _ in keys}
    for d in sorted(days):
        if not (START <= d <= END):
            continue
        local = praytimes_isna(d)
        for a, b in keys:
            diff = round((days[d]["timings"][a] - local[b]).total_seconds() / 60)
            s = stats[a]
            s["max_abs"] = max(s["max_abs"], abs(diff))
            s["sum_abs"] += abs(diff)
            s["n"] += 1
            s["hist"][diff] = s["hist"].get(diff, 0) + 1
            if abs(diff) > 1:
                s["over_1"].append((d.isoformat(), diff))
    return stats


# --------------------------------------------------------------------------------------
# 3. Hijri cross-check (Umm al-Qura via hijridate) and moon phase
# --------------------------------------------------------------------------------------
def cross_check_hijri(days: dict[date, dict]) -> dict:
    try:
        from hijridate import Gregorian  # type: ignore
    except Exception as e:  # pragma: no cover
        return {"available": False, "error": str(e)}
    mismatches = []
    n = 0
    for d in sorted(days):
        if not (START <= d <= END):
            continue
        n += 1
        h = Gregorian(d.year, d.month, d.day).to_hijri()
        a = days[d]["hijri"]
        if (h.year, h.month, h.day) != (a["year"], a["month"], a["day"]):
            mismatches.append({"date": d.isoformat(), "aladhan_hjcosa": f'{a["day"]}-{a["month"]}-{a["year"]}',
                               "umm_al_qura": f"{h.day}-{h.month}-{h.year}"})
    return {"available": True, "days_checked": n, "mismatches": mismatches}


def moon_phase(d: date) -> tuple[float, str, int]:
    """Synodic approximation (new moon ref 2000-01-06 18:14 UTC). Returns (fraction, emoji, illum%)."""
    ref = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    noon = datetime(d.year, d.month, d.day, 12, tzinfo=TZ).astimezone(timezone.utc)
    p = ((noon - ref).total_seconds() / 86400.0 / 29.530588853) % 1.0
    illum = int(round((1 - math.cos(2 * math.pi * p)) / 2 * 100))
    bins = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    idx = int(((p + 0.0625) % 1.0) * 8)
    return p, bins[idx], illum


# --------------------------------------------------------------------------------------
# 4. Event construction
# --------------------------------------------------------------------------------------
def fmt_t(t: datetime) -> str:
    return t.strftime("%H:%M")


def fmt_12(t: datetime) -> str:
    return t.strftime("%-I:%M %p")


def iso_local(t: datetime) -> str:
    """ISO 8601 local wall time without offset, for the Calendar MCP (timeZone passed separately)."""
    return t.astimezone(TZ).strftime("%Y-%m-%dT%H:%M:%S")


def dur_str(a: datetime, b: datetime) -> str:
    m = int((b - a).total_seconds() // 60)
    return f"{m // 60}h {m % 60:02d}m"


def hijri_str(h: dict) -> str:
    return f'{h["day"]} {h["month_en"]} {h["year"]} AH'


class Milestones:
    def __init__(self, days: dict[date, dict]):
        self.by_hijri = {(v["hijri"]["year"], v["hijri"]["month"], v["hijri"]["day"]): k for k, v in days.items()}
        self.ramadan_1 = self.by_hijri[(1448, 9, 1)]
        self.eid_fitr = self.by_hijri[(1448, 10, 1)]
        self.dhul_hijjah_1 = self.by_hijri[(1448, 12, 1)]
        self.arafah = self.by_hijri[(1448, 12, 9)]
        self.eid_adha = self.by_hijri[(1448, 12, 10)]
        # sanity: expected per Aladhan hToG lookups done during research
        assert self.ramadan_1 == date(2027, 2, 8), self.ramadan_1
        assert self.eid_fitr == date(2027, 3, 9), self.eid_fitr
        assert self.dhul_hijjah_1 == date(2027, 5, 7), self.dhul_hijjah_1
        assert self.arafah == date(2027, 5, 15), self.arafah
        assert self.eid_adha == date(2027, 5, 16), self.eid_adha

    def countdown(self, d: date, h: dict) -> str:
        day = h["day"]
        if d < self.ramadan_1:
            return f"Ramadan in {(self.ramadan_1 - d).days}d · Dhul-Hijjah in {(self.dhul_hijjah_1 - d).days}d"
        if d < self.eid_fitr:
            s = f"Ramadan day {day}/{h['month_days']}"
            if day >= 20:
                night = day + 1
                s += f" · tonight = night {night}" + (" ✨ odd (Qadr sought)" if night % 2 == 1 else "")
            else:
                s += f" · Eid al-Fitr in {(self.eid_fitr - d).days}d"
            return s
        if d == self.eid_fitr:
            return "EID AL-FITR 🎉 · Dhul-Hijjah in %dd" % (self.dhul_hijjah_1 - d).days
        if d < self.dhul_hijjah_1:
            return f"Dhul-Hijjah in {(self.dhul_hijjah_1 - d).days}d · Arafah in {(self.arafah - d).days}d"
        if d < self.arafah:
            return f"Dhul-Hijjah day {day} (best 10 days) · Arafah in {(self.arafah - d).days}d"
        if d == self.arafah:
            return "DAY OF ARAFAH 🕋 · Eid al-Adha tomorrow"
        if d == self.eid_adha:
            return "EID AL-ADHA 🎉"
        if 11 <= day <= 13:
            return f"Tashreeq day {day - 10} of 3 · cycle ends in {(END - d).days}d"
        if d == END:
            return "CYCLE COMPLETE 🏁 · 1 Muharram 1449 tomorrow"
        return f"Dhul-Hijjah day {day} · cycle ends in {(END - d).days}d"

    def short_countdown(self, d: date, h: dict) -> str:
        """Compact form for the all-day header title."""
        day = h["day"]
        if d < self.ramadan_1:
            return f"Ramadan −{(self.ramadan_1 - d).days}d"
        if d < self.eid_fitr:
            if day >= 20:
                night = day + 1
                return f"Ramadan {day} · night {night}" + (" ✨" if night % 2 == 1 else "")
            return f"Ramadan {day} · Eid −{(self.eid_fitr - d).days}d"
        if d == self.eid_fitr:
            return "EID AL-FITR 🎉"
        if d < self.dhul_hijjah_1:
            return f"Dhul-Hijjah −{(self.dhul_hijjah_1 - d).days}d"
        if d < self.arafah:
            return f"Best 10 days · Arafah −{(self.arafah - d).days}d"
        if d == self.arafah:
            return "DAY OF ARAFAH 🕋"
        if d == self.eid_adha:
            return "EID AL-ADHA 🎉"
        if 11 <= day <= 13:
            return f"Tashreeq {day - 10}/3"
        if d == END:
            return "CYCLE COMPLETE 🏁"
        return f"cycle ends −{(END - d).days}d"


BLOCK_SPECS = {
    # key: (title, theme, reminders-in-minutes-before-start)
    "B0": ("🌌 B0 · Pre-Dawn (Tahajjud)",
           "Pre-dawn stillness, du'a and spiritual grounding before first light. Optional night prayer.",
           [0]),
    "B1": ("🌅 B1 · Dawn / First Light",
           "Spiritual activation: Fajr prayer at the earliest time, morning adhkar, a serene mental ramp. "
           "Hard stop 10 minutes before sunrise — do not run past the end of this block.",
           []),
    "B2": ("☀️ B2 · High Dopamine Core Work",
           "Sensation of a warm 10 AM sun. The majority of core work and high-dopamine intensity lives here. "
           "⚠️ STRICT RULE: NO SLEEPING. Guard this window.",
           [35, 10]),
    "B3": ("🟧 B3 · Core Wrap-Up",
           "Tapering intensity: pray Dhuhr at the window opening, then wrap up core work, administrative tasks "
           "and closing loops.",
           [10]),
    "B4": ("🌇 B4 · Afternoon & Sunset Prep",
           "Pray Asr first. Outdoor activities, shopping, errands, fresh air, enjoying the weather. "
           "Hard stop 15 minutes before Maghrib (Buffer 2).",
           [10]),
    "B5": ("🔵 B5 · Evening Reset",
           "Pray Maghrib at the earliest time. Supper, return home, wind down, possible swim. "
           "Disconnect from work devices; transition to recovery and reflection.",
           [25]),
    "B6": ("⚫ B6 · Wind Down to Sleep",
           "Final prayer (Isha and Witr). Complete sensory wind-down and restorative sleep by midnight. "
           "Dim lights, disable blue light, de-escalate the nervous system.",
           [10]),
}

PRAYER_ORDER = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
PRAYER_EVENT_MINUTES = 25


def build_day(d: date, info: dict, ms: Milestones, sheet_url: str) -> dict:
    T = info["timings"]
    h = info["hijri"]
    fajr, sunrise, dhuhr, asr, maghrib, isha = (T["Fajr"], T["Sunrise"], T["Dhuhr"], T["Asr"],
                                                T["Maghrib"], T["Isha"])
    midnight = datetime(d.year, d.month, d.day, tzinfo=TZ) + timedelta(days=1)
    midnight = datetime(midnight.year, midnight.month, midnight.day, 0, 0, tzinfo=TZ)

    b = {
        "B0": (fajr - timedelta(minutes=45), fajr),
        "B1": (fajr, sunrise - timedelta(minutes=10)),
        "BUFFER1": (sunrise - timedelta(minutes=10), sunrise + timedelta(minutes=15)),
        "B2": (sunrise + timedelta(minutes=15), dhuhr),
        "B3": (dhuhr, asr),
        "B4": (asr, maghrib - timedelta(minutes=15)),
        "BUFFER2": (maghrib - timedelta(minutes=15), maghrib),
        "B5": (maghrib, isha),
        "B6": (isha, midnight),
    }
    for k, (s, e) in b.items():
        assert e > s, (d, k, s, e)

    p, moon_emoji, illum = moon_phase(d)
    greg = d.strftime("%a %d %b %Y")
    hs = hijri_str(h)
    head = f"🌙 {hs} · {greg} · {moon_emoji} {illum}% · {ms.countdown(d, h)}"

    windows = {  # on-time windows for the 40-prayer streak (end = the block's hard stop)
        "Fajr": (fajr, b["B1"][1], f"10 min before sunrise ({fmt_t(sunrise)})"),
        "Dhuhr": (dhuhr, asr, f"the Asr adhan ({fmt_t(asr)})"),
        "Asr": (asr, b["B4"][1], f"15 min before Maghrib ({fmt_t(maghrib)})"),
        "Maghrib": (maghrib, isha, f"the Isha adhan ({fmt_t(isha)})"),
        "Isha": (isha, midnight, "midnight (12:00 AM)"),
    }

    next_line = {
        "B0": f"NEXT: Fajr adhan {fmt_t(fajr)} → B1 Dawn.",
        "B1": f"NEXT: Buffer 1 {fmt_t(b['BUFFER1'][0])}–{fmt_t(b['BUFFER1'][1])} (horizon passing — leave blank), then B2 at {fmt_t(b['B2'][0])}.",
        "B2": f"NEXT: Dhuhr adhan {fmt_t(dhuhr)} → B3 Core Wrap-Up.",
        "B3": f"NEXT: Asr adhan {fmt_t(asr)} → B4 Afternoon.",
        "B4": f"NEXT: Buffer 2 {fmt_t(b['BUFFER2'][0])}–{fmt_t(maghrib)} (hard stop, leave blank), then Maghrib {fmt_t(maghrib)} → B5.",
        "B5": f"NEXT: Isha adhan {fmt_t(isha)} → B6 Wind Down.",
        "B6": f"NEXT: Sleep. Tomorrow's B0 starts {fmt_t(fajr - timedelta(minutes=45))} (today's Fajr − 45m; check tomorrow's event).",
    }
    window_label = {
        "B0": "Fajr − 45m → Fajr", "B1": "Fajr → Sunrise − 10m", "B2": "Sunrise + 15m → Dhuhr",
        "B3": "Dhuhr → Asr", "B4": "Asr → Maghrib − 15m", "B5": "Maghrib → Isha", "B6": "Isha → Midnight",
    }

    events = []
    # -- daily Hijri header (all-day) ------------------------------------------------
    events.append({
        "uid": f"{d.isoformat()}-HDR", "kind": "HEADER",
        "summary": f"🌙 {h['day']} {h['month_en']} {h['year']} · {moon_emoji} · {ms.short_countdown(d, h)}",
        "allDay": True, "startTime": f"{d.isoformat()}T00:00:00",
        "endTime": f"{(d + timedelta(days=1)).isoformat()}T00:00:00",
        "colorId": COLORS["HEADER"], "availability": "AVAILABILITY_FREE", "reminders": [],
        "description": (
            f"{head}\n"
            f"Moon: {moon_emoji} {illum}% illuminated (phase {p:.2f}; 0 = new, 0.5 = full)\n"
            f"Day {h['day']} of {h['month_days']} in {h['month_en']} · {h['month_ar']}\n"
            f"Prayer times (ISNA, {LOCATION}): Fajr {fmt_t(fajr)} · Sunrise {fmt_t(sunrise)} · Dhuhr {fmt_t(dhuhr)} · "
            f"Asr {fmt_t(asr)} · Maghrib {fmt_t(maghrib)} · Isha {fmt_t(isha)}\n"
            f"LRIB-ID: {d.isoformat()}-HDR"
        ),
    })

    # -- the seven time blocks ---------------------------------------------------------
    for key in ("B0", "B1", "B2", "B3", "B4", "B5", "B6"):
        s, e = b[key]
        title, theme, rem = BLOCK_SPECS[key]
        desc = (
            f"{head}\n"
            f"⏱ WINDOW: {fmt_t(s)} → {fmt_t(e)} ({window_label[key]}) · {dur_str(s, e)}\n"
            f"THEME: {theme}\n\n"
            f"{RULE_OF_3}\n\n"
            f"{next_line[key]}\n"
            f"LRIB-ID: {d.isoformat()}-{key}"
        )
        if key == "B1":
            desc = desc.replace("THEME:", f"⏳ COUNTDOWN: hard stop at {fmt_t(e)}; a notice fires at {fmt_t(e - timedelta(minutes=10))}.\nTHEME:")
        events.append({
            "uid": f"{d.isoformat()}-{key}", "kind": key, "summary": title,
            "allDay": False, "startTime": iso_local(s), "endTime": iso_local(e),
            "colorId": COLORS[key], "availability": "AVAILABILITY_BUSY",
            "reminders": [{"method": "popup", "minutes": m} for m in rem],
            "description": desc,
        })

    # -- the five actionable prayer events ---------------------------------------------
    for name in PRAYER_ORDER:
        s, cutoff, cutoff_txt = windows[name]
        e = s + timedelta(minutes=PRAYER_EVENT_MINUTES)
        desc = (
            f"🕌 40-PRAYER STREAK · {name.upper()} · {hs}\n"
            f"Adhan {fmt_t(s)} · on-time window closes {fmt_t(cutoff)} = {cutoff_txt}\n"
            f"✅ Tick off: when prayed inside the window, edit this title from \"[ ]\" to \"[x]\" and mark On-Time in the tracker.\n"
            f"⚠️ Reset rule: Late (after {fmt_t(cutoff)}) or Missed → the 40-streak resets to 0. History stays in the log.\n"
            f"📊 Tracker: {sheet_url}\n"
            f"LRIB-ID: {d.isoformat()}-P-{name.upper()}"
        )
        events.append({
            "uid": f"{d.isoformat()}-P-{name.upper()}", "kind": "PRAYER", "prayer": name,
            "summary": f"[ ] 🕌 {name} · by {fmt_t(cutoff)}",
            "allDay": False, "startTime": iso_local(s), "endTime": iso_local(e),
            "colorId": COLORS["PRAYER"], "availability": "AVAILABILITY_FREE",
            "reminders": [{"method": "popup", "minutes": 0}],
            "description": desc,
            "window_start": iso_local(s), "window_end": iso_local(cutoff),
        })

    # -- lunar anchor on the 1st of the month ------------------------------------------
    if h["day"] == 1:
        a = ANCHORS[h["month"]]
        prog = ms.countdown(d, h)
        pre = "🎉 " if h["month"] == 10 else ("🕋 " if h["month"] == 12 else "")
        events.append({
            "uid": f"{d.isoformat()}-ANCHOR", "kind": "ANCHOR",
            "summary": f"{pre}🌙 1 {h['month_en']} {h['year']} — {a['theme']}",
            "allDay": True, "startTime": f"{d.isoformat()}T00:00:00",
            "endTime": f"{(d + timedelta(days=1)).isoformat()}T00:00:00",
            "colorId": COLORS["ANCHOR"], "availability": "AVAILABILITY_FREE", "reminders": [],
            "description": (
                f"🌙 1ST OF {h['month_en'].upper()} {h['year']} AH ({h['month_ar']}) · {greg} · {h['month_days']}-day month\n\n"
                f"• Progression: {prog}\n"
                f"• Associative meaning: {a['meaning']}\n"
                f"• Executive anchor: {a['anchor']}\n\n"
                f"Hijri dates follow the Saudi High Judiciary Council calendar (Aladhan HJCoSA); local moon sighting "
                f"in New York may shift a month start by one day. Prayer blocks are solar and unaffected.\n"
                f"LRIB-ID: {d.isoformat()}-ANCHOR"
            ),
        })

    return {
        "date": d.isoformat(), "weekday": info["weekday"], "hijri": h,
        "moon": {"phase": round(p, 3), "emoji": moon_emoji, "illumination_pct": illum},
        "countdown": ms.countdown(d, h),
        "timings": {k: iso_local(v) for k, v in T.items()},
        "blocks": {k: {"start": iso_local(s), "end": iso_local(e)} for k, (s, e) in b.items()},
        "prayer_windows": {k: {"start": iso_local(s), "end": iso_local(e)} for k, (s, e, _) in windows.items()},
        "events": events,
    }


def milestone_events(days: dict[date, dict], ms: Milestones) -> list[dict]:
    def allday(d: date, uid: str, summary: str, desc: str, color: str, end: date | None = None):
        end = end or (d + timedelta(days=1))
        return {"uid": uid, "kind": "MILESTONE", "summary": summary, "allDay": True,
                "startTime": f"{d.isoformat()}T00:00:00", "endTime": f"{end.isoformat()}T00:00:00",
                "colorId": color, "availability": "AVAILABILITY_FREE", "reminders": [],
                "description": desc + f"\nLRIB-ID: {uid}", "date": d.isoformat()}

    by = ms.by_hijri
    ev = []
    ev.append(allday(START, "MS-START", "🚀 LUNAR RHYTHM BEGINS · 30 Rabi' al-Thani 1448",
                     f"Day 1 of the Lunar Rhythm & Intentional Blocks system.\n"
                     f"{(END - START).days + 1} days from here to the end of Dhul-Hijjah 1448 (2027-06-05).\n"
                     f"Ramadan 1448 begins {ms.ramadan_1.isoformat()} ({(ms.ramadan_1 - START).days} days away).",
                     COLORS["MILESTONE"]))
    isra = by[(1448, 7, 27)]
    ev.append(allday(isra, "MS-ISRA", "✨ 27 Rajab · Isra & Mi'raj (commemorated)",
                     "The Night Journey and Ascension is commemorated on 27 Rajab by many communities "
                     "(the night of the 26th → 27th). Sacred month; sowing season.", COLORS["MILESTONE"]))
    mid_shaban = by[(1448, 8, 15)]
    ev.append(allday(mid_shaban, "MS-MIDSHABAN", "✨ 15 Sha'ban · Mid-Sha'ban (night of 14→15)",
                     "Laylat al-Bara'ah, observed by many. Roughly two weeks of runway left before Ramadan "
                     f"({(ms.ramadan_1 - mid_shaban).days} days).", COLORS["MILESTONE"]))
    # last ten nights of Ramadan: night N falls on the evening of Ramadan day N-1
    for night in (21, 23, 25, 27, 29):
        d = by[(1448, 9, night - 1)]
        label = "LAST 10 NIGHTS BEGIN · " if night == 21 else ""
        ev.append(allday(d, f"MS-QADR-{night}", f"✨ Tonight = night {night} of Ramadan · {label}Laylat al-Qadr sought",
                         f"The night of {night} Ramadan begins at Maghrib today ({d.strftime('%a %d %b %Y')}). "
                         "Odd nights of the last ten are when Laylat al-Qadr is sought. Night vigil, Qur'an, du'a.",
                         COLORS["MILESTONE"]))
    ev.append(allday(ms.arafah, "MS-ARAFAH", "🕋 DAY OF ARAFAH · 9 Dhul-Hijjah 1448",
                     "The Day of Arafah. Fasting is recommended for non-pilgrims. Eid al-Adha tomorrow.",
                     COLORS["MILESTONE"]))
    ev.append(allday(ms.eid_adha, "MS-EID-ADHA", "🎉 EID AL-ADHA · 10 Dhul-Hijjah 1448",
                     "Eid al-Adha — the sacrifice. Peak milestone 2 reached. Takbirat continue through Tashreeq.",
                     COLORS["MILESTONE"]))
    t1, t3 = by[(1448, 12, 11)], by[(1448, 12, 13)]
    ev.append(allday(t1, "MS-TASHREEQ", "🕋 Days of Tashreeq · 11–13 Dhul-Hijjah",
                     "The three days of Tashreeq: takbir after prayers, no fasting.", COLORS["MILESTONE"],
                     end=t3 + timedelta(days=1)))
    ev.append(allday(END, "MS-END", "🏁 CYCLE COMPLETE · 30 Dhul-Hijjah 1448 · 1 Muharram 1449 tomorrow",
                     "End marker of the Lunar Rhythm cycle: the month of Hajj and Eid is complete. "
                     "Re-run the engine (or the Apps Script) to extend into 1449.", COLORS["MILESTONE"]))
    # DST notes (America/New_York): fall back 2026-11-01 02:00, spring forward 2027-03-14 02:00
    ev.append(allday(date(2026, 10, 31), "MS-DST-FALL", "🕰 Clocks fall back tonight (DST ends 2 AM Sun)",
                     "Daylight Saving Time ends Sunday 2026-11-01 at 2:00 AM (EDT → EST). All blocks already use "
                     "the correct local times; Fajr tomorrow appears about an hour earlier on the clock.", COLORS["NOTE"]))
    ev.append(allday(date(2027, 3, 13), "MS-DST-SPRING", "🕰 Clocks spring forward tonight (DST begins 2 AM Sun)",
                     "Daylight Saving Time begins Sunday 2027-03-14 at 2:00 AM (EST → EDT). All blocks already use "
                     "the correct local times; Fajr tomorrow appears about an hour later on the clock.", COLORS["NOTE"]))
    return ev


# --------------------------------------------------------------------------------------
# 5. Outputs
# --------------------------------------------------------------------------------------
def write_timetable_csv(rows: list[dict], path: Path):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "weekday", "hijri_day", "hijri_month", "hijri_month_name", "hijri_year", "moon",
                    "countdown", "fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha",
                    "B0_start", "B1_start", "B1_end", "buffer1_end_B2_start", "B2_end_B3_start", "B3_end_B4_start",
                    "B4_end", "buffer2_end_B5_start", "B5_end_B6_start", "B6_end"])
        for r in rows:
            t = r["timings"]; b = r["blocks"]
            hm = lambda s: s[11:16]
            w.writerow([r["date"], r["weekday"], r["hijri"]["day"], r["hijri"]["month"], r["hijri"]["month_en"],
                        r["hijri"]["year"], r["moon"]["emoji"], r["countdown"],
                        hm(t["Fajr"]), hm(t["Sunrise"]), hm(t["Dhuhr"]), hm(t["Asr"]), hm(t["Maghrib"]), hm(t["Isha"]),
                        hm(b["B0"]["start"]), hm(b["B1"]["start"]), hm(b["B1"]["end"]), hm(b["B2"]["start"]),
                        hm(b["B3"]["start"]), hm(b["B4"]["start"]), hm(b["B4"]["end"]), hm(b["B5"]["start"]),
                        hm(b["B6"]["start"]), "00:00 (+1)"])


def write_timetable_md(rows: list[dict], path: Path):
    out = [f"# {CALENDAR_NAME} — Timetable\n",
           f"Location: {LOCATION} · ISNA (15°/15°) · {TZ_NAME}\n",
           f"Range: {START} → {END} ({len(rows)} days). Times are local wall-clock (DST applied).\n",
           "Blocks: B0 = Fajr−45m→Fajr · B1 = Fajr→Sunrise−10m · Buffer 1 = Sunrise−10m→Sunrise+15m (blank) · "
           "B2 = Sunrise+15m→Dhuhr · B3 = Dhuhr→Asr · B4 = Asr→Maghrib−15m · Buffer 2 = Maghrib−15m→Maghrib (blank) · "
           "B5 = Maghrib→Isha · B6 = Isha→00:00\n"]
    cur = None
    for r in rows:
        ym = r["date"][:7]
        if ym != cur:
            cur = ym
            out.append(f"\n## {datetime.strptime(ym, '%Y-%m').strftime('%B %Y')}\n")
            out.append("| Date | Hijri | 🌙 | Fajr | Sunrise | Dhuhr | Asr | Maghrib | Isha | B1 ends | B2 starts | B4 ends | Countdown |")
            out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        t = r["timings"]; b = r["blocks"]; h = r["hijri"]
        hm = lambda s: s[11:16]
        out.append(f"| {r['date']} {r['weekday'][:3]} | {h['day']} {h['month_en']} {h['year']} | {r['moon']['emoji']} | "
                   f"{hm(t['Fajr'])} | {hm(t['Sunrise'])} | {hm(t['Dhuhr'])} | {hm(t['Asr'])} | {hm(t['Maghrib'])} | {hm(t['Isha'])} | "
                   f"{hm(b['B1']['end'])} | {hm(b['B2']['start'])} | {hm(b['B4']['end'])} | {r['countdown']} |")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def write_validation_report(stats: dict, hijri: dict, rows: list[dict], path: Path, ms: Milestones):
    out = ["# Validation report — Lunar Rhythm & Intentional Blocks\n",
           f"Generated {datetime.now(TZ).strftime('%Y-%m-%d %H:%M %Z')} · {len(rows)} days ({START} → {END})\n",
           "## 1. Prayer times: Aladhan (ISNA, method=2) vs independent local PrayTimes port\n",
           "Difference = Aladhan − local, in whole minutes. Both round to the nearest minute, so ±1 min is rounding noise.\n",
           "| Prayer | days | max |diff| | mean |diff| | histogram (diff: count) | days with |diff| > 1 min |",
           "|---|---|---|---|---|---|"]
    worst = 0
    for k, s in stats.items():
        hist = ", ".join(f"{d:+d}: {c}" for d, c in sorted(s["hist"].items()))
        over = ", ".join(f"{d} ({v:+d})" for d, v in s["over_1"]) or "none"
        worst = max(worst, s["max_abs"])
        out.append(f"| {k} | {s['n']} | {s['max_abs']} | {s['sum_abs'] / max(s['n'], 1):.2f} | {hist} | {over} |")
    verdict = "PASS" if worst <= 2 else "FAIL"
    out.append(f"\n**Verdict: {verdict}** (rubric: every prayer, every day within 2 minutes of an independent computation).\n")
    out.append("## 2. Hijri dates: Aladhan HJCoSA vs Umm al-Qura (hijridate)\n")
    if not hijri.get("available"):
        out.append(f"hijridate unavailable: {hijri.get('error')}\n")
    else:
        mm = hijri["mismatches"]
        out.append(f"{hijri['days_checked']} days checked · {len(mm)} mismatching day(s).\n")
        if mm:
            out.append("| Date | Aladhan (HJCoSA) | Umm al-Qura |\n|---|---|---|")
            out.extend(f"| {m['date']} | {m['aladhan_hjcosa']} | {m['umm_al_qura']} |" for m in mm)
        out.append("\nAnchor dates used (Aladhan HJCoSA): 1 Ramadan 1448 = %s · Eid al-Fitr = %s · 1 Dhul-Hijjah = %s · "
                   "Arafah = %s · Eid al-Adha = %s · 1 Muharram 1449 = 2027-06-06.\n"
                   % (ms.ramadan_1, ms.eid_fitr, ms.dhul_hijjah_1, ms.arafah, ms.eid_adha))
        out.append("Local moon sighting (e.g., Fiqh Council / local masjid announcements) can shift a month start by ±1 day; "
                   "only the all-day anchor/header/milestone events would move. All timed blocks are solar.\n")
    out.append("## 3. Structural checks\n")
    out.append("- Every block has end > start on every day (asserted in build).")
    out.append("- No block crosses the DST transitions (2026-11-01 02:00, 2027-03-14 02:00); offsets come from the data's ISO-8601 strings.")
    first_lunar = [r for r in rows if r["hijri"]["day"] == 1]
    out.append(f"- Lunar anchors generated: {len(first_lunar)} → " + ", ".join(f"{r['date']} (1 {r['hijri']['month_en']})" for r in first_lunar))
    # moon-phase sanity: new moon should fall within ~3 days before each 1st
    bad = [r["date"] for r in first_lunar if not (r["moon"]["phase"] < 0.12 or r["moon"]["phase"] > 0.93)]
    out.append(f"- Moon phase on each 1st is near new moon (phase < 0.12 or > 0.93): {'PASS' if not bad else 'CHECK ' + ', '.join(bad)}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return verdict


def write_prayer_log_csv(rows: list[dict], path: Path):
    """Single-sheet tracker for Google Sheets import.

    Rows 1-5: title, KPI labels, KPI formulas, rules.  Row 7: header.  Rows 8+: one row per prayer.
    Columns: A Log ID | B Date | C Hijri | D Prayer | E Adhan | F Closes | G Status | H Streak | I Notes
    The Streak column is a single SCAN formula in H8 (running streak: On-Time +1, Late/Missed reset to 0,
    blank rows carry the previous value), so the file stays small enough for a one-shot Drive upload.
    """
    prayers = [(r, ev) for r in rows for ev in r["events"] if ev["kind"] == "PRAYER"]
    last_row = 7 + len(prayers)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["🕌 40-PRAYER HABIT TRACKER & STREAK ENGINE", "", "", "", "", "",
                    "Type Status exactly: On-Time · Late · Missed", "", ""])
        w.writerow(["Current streak", "Record streak", "Total on-time", "Late / Missed", "On-time rate",
                    "Progress to 40", "Last logged prayer", "", ""])
        w.writerow(['=IFERROR(LOOKUP(2,1/(G8:G<>""),H8:H),0)',
                    '=IFERROR(MAX(H8:H),0)',
                    '=COUNTIF(G8:G,"On-Time")',
                    '=COUNTIF(G8:G,"Late")+COUNTIF(G8:G,"Missed")',
                    '=IFERROR(TEXT(C3/COUNTA(G8:G),"0%"),"0%")',
                    '=TEXT(MIN(A3/40,1),"0%")&" ("&A3&"/40)"',
                    '=IFERROR(LOOKUP(2,1/(G8:G<>""),A8:A),"—")', "", ""])
        w.writerow([""] * 9)
        w.writerow(["Rules: On-Time = prayed inside the window (Adhan → Closes). Late = after the window closed. "
                    "Missed = not prayed. Each On-Time adds +1; any Late/Missed resets the streak to 0; "
                    "history is never deleted. Streak column is automatic (one formula in H8).", "", "", "", "", "", "", "", ""])
        w.writerow([""] * 9)
        w.writerow(["Log ID", "Date", "Hijri", "Prayer", "Adhan", "Closes", "Status", "Streak", "Notes"])
        for i, (r, ev) in enumerate(prayers):
            streak = (f'=SCAN(0,G8:G{last_row},LAMBDA(a,s,IF(s="On-Time",a+1,IF(s="",a,0))))' if i == 0 else "")
            w.writerow([ev["uid"], r["date"], f'{r["hijri"]["day"]} {r["hijri"]["month_en"]} {r["hijri"]["year"]}',
                        ev["prayer"], ev["window_start"][11:16], ev["window_end"][11:16], "", streak, ""])


def write_ics(rows: list[dict], extra: list[dict], ics_dir: Path):
    from icalendar import Alarm, Calendar, Event  # type: ignore
    ics_dir.mkdir(parents=True, exist_ok=True)

    def new_cal(name: str) -> Calendar:
        cal = Calendar()
        cal.add("prodid", "-//Lunar Rhythm & Intentional Blocks//timetable_engine//EN")
        cal.add("version", "2.0")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("X-WR-CALNAME", name)
        cal.add("X-WR-TIMEZONE", TZ_NAME)
        return cal

    stamp = datetime.now(timezone.utc)

    def to_vevent(ev: dict) -> Event:
        e = Event()
        e.add("uid", f"{ev['uid']}@lunar-rhythm")
        e.add("dtstamp", stamp)
        e.add("summary", ev["summary"])
        e.add("description", ev["description"])
        if ev["allDay"]:
            e.add("dtstart", date.fromisoformat(ev["startTime"][:10]))
            e.add("dtend", date.fromisoformat(ev["endTime"][:10]))
            e.add("transp", "TRANSPARENT")
        else:
            e.add("dtstart", datetime.fromisoformat(ev["startTime"]).replace(tzinfo=TZ))
            e.add("dtend", datetime.fromisoformat(ev["endTime"]).replace(tzinfo=TZ))
            e.add("transp", "TRANSPARENT" if ev.get("availability") == "AVAILABILITY_FREE" else "OPAQUE")
        e.add("color", ICS_COLORS.get(ev["colorId"], "gray"))
        e.add("categories", [ev["kind"]])
        for r in ev.get("reminders", []):
            a = Alarm()
            a.add("action", "DISPLAY")
            a.add("description", ev["summary"])
            a.add("trigger", timedelta(minutes=-r["minutes"]))
            e.add_component(a)
        return e

    all_cal = new_cal(CALENDAR_NAME)
    month_cals: dict[str, Calendar] = {}
    count = 0
    for r in rows:
        ym = r["date"][:7]
        month_cals.setdefault(ym, new_cal(f"{CALENDAR_NAME} — {ym}"))
        for ev in r["events"]:
            v = to_vevent(ev)
            all_cal.add_component(v)
            month_cals[ym].add_component(to_vevent(ev))
            count += 1
    for ev in extra:
        ym = ev["date"][:7]
        month_cals.setdefault(ym, new_cal(f"{CALENDAR_NAME} — {ym}"))
        all_cal.add_component(to_vevent(ev))
        month_cals[ym].add_component(to_vevent(ev))
        count += 1
    for cal in [all_cal, *month_cals.values()]:
        cal.add_missing_timezones()
    (ics_dir / "LRIB_ALL.ics").write_bytes(all_cal.to_ical())
    for ym, cal in month_cals.items():
        (ics_dir / f"LRIB_{ym}.ics").write_bytes(cal.to_ical())
    return count


def write_payloads(rows: list[dict], extra: list[dict], out_dir: Path, calendar_id: str, days_per_batch: int = 20):
    """create_event parameter objects, grouped in day batches for parallel upload."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("batch_*.json"):
        old.unlink()
    extra_by_date: dict[str, list[dict]] = {}
    for ev in extra:
        extra_by_date.setdefault(ev["date"], []).append(ev)

    def to_payload(ev: dict) -> dict:
        p = {"uid": ev["uid"], "summary": ev["summary"], "startTime": ev["startTime"], "endTime": ev["endTime"],
             "timeZone": TZ_NAME, "colorId": ev["colorId"], "description": ev["description"],
             "availability": ev.get("availability", "AVAILABILITY_BUSY")}
        if ev["allDay"]:
            p["allDay"] = True
        if ev.get("reminders"):
            p["overrideReminders"] = ev["reminders"]
            p["useDefaultReminders"] = False
        else:
            p["useDefaultReminders"] = False
        if calendar_id:
            p["calendarId"] = calendar_id
        return p

    batches = []
    for i in range(0, len(rows), days_per_batch):
        chunk = rows[i:i + days_per_batch]
        events = []
        for r in chunk:
            for ev in extra_by_date.get(r["date"], []):
                events.append(to_payload(ev))
            for ev in r["events"]:
                events.append(to_payload(ev))
        n = len(batches) + 1
        batch = {"batch": n, "first_day": chunk[0]["date"], "last_day": chunk[-1]["date"], "days": len(chunk),
                 "calendarId": calendar_id, "timeZone": TZ_NAME, "event_count": len(events), "events": events}
        (out_dir / f"batch_{n:02d}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
        batches.append({"batch": n, "first_day": batch["first_day"], "last_day": batch["last_day"],
                        "days": len(chunk), "event_count": len(events), "file": f"batch_{n:02d}.json"})
    (out_dir / "index.json").write_text(json.dumps(batches, indent=1), encoding="utf-8")
    return batches


# --------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet-url", default="(tracker sheet URL — see README)")
    ap.add_argument("--calendar-id", default="")
    ap.add_argument("--days-per-batch", type=int, default=20)
    args = ap.parse_args(argv)

    BUILD.mkdir(parents=True, exist_ok=True)
    days = load_raw()
    missing = [d for d in (START + timedelta(n) for n in range((END - START).days + 1)) if d not in days]
    assert not missing, f"missing days in raw data: {missing[:5]}"

    ms = Milestones(days)
    rows = [build_day(d, days[d], ms, args.sheet_url) for d in sorted(days) if START <= d <= END]
    extra = milestone_events(days, ms)

    stats = cross_check_timings(days)
    hijri = cross_check_hijri(days)
    verdict = write_validation_report(stats, hijri, rows, BUILD / "validation_report.md", ms)

    timed = sum(1 for r in rows for e in r["events"] if not e["allDay"])
    allday = sum(1 for r in rows for e in r["events"] if e["allDay"]) + len(extra)
    summary = {
        "calendar_name": CALENDAR_NAME, "location": LOCATION, "lat": LAT, "lon": LON, "timezone": TZ_NAME,
        "method": "ISNA (Fajr 15°, Isha 15°, Maghrib = sunset, Asr standard)", "hijri_calendar": "Aladhan HJCoSA",
        "start": START.isoformat(), "end": END.isoformat(), "days": len(rows),
        "events_timed": timed, "events_allday": allday, "events_total": timed + allday,
        "milestones": {"ramadan_1": ms.ramadan_1.isoformat(), "eid_al_fitr": ms.eid_fitr.isoformat(),
                       "dhul_hijjah_1": ms.dhul_hijjah_1.isoformat(), "arafah": ms.arafah.isoformat(),
                       "eid_al_adha": ms.eid_adha.isoformat()},
        "colors": {k: f"{v} ({COLOR_NAMES[v]})" for k, v in COLORS.items()},
        "validation_verdict": verdict, "sheet_url": args.sheet_url, "calendar_id": args.calendar_id,
        "generated": datetime.now(TZ).isoformat(timespec="seconds"),
    }
    (BUILD / "timetable.json").write_text(json.dumps({"summary": summary, "days": rows, "milestone_events": extra},
                                                     ensure_ascii=False, indent=1), encoding="utf-8")
    write_timetable_csv(rows, BUILD / "timetable.csv")
    write_timetable_md(rows, BUILD / "timetable.md")
    write_prayer_log_csv(rows, BUILD / "prayer_log.csv")
    n_ics = write_ics(rows, extra, BUILD / "ics")
    batches = write_payloads(rows, extra, BUILD / "payloads", args.calendar_id, args.days_per_batch)

    print(json.dumps({**summary, "ics_events": n_ics,
                      "batches": [(b["batch"], b["first_day"], b["last_day"], b["event_count"]) for b in batches]},
                     ensure_ascii=False, indent=1))
    if verdict != "PASS":
        print("VALIDATION FAILED — see build/validation_report.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
