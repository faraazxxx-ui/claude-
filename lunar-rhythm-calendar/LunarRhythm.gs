/**
 * =====================================================================================
 *  LUNAR RHYTHM & INTENTIONAL BLOCKS — Google Apps Script maintenance tool  (v3.0)
 * =====================================================================================
 *  The calendar itself was populated directly through the Google Calendar API from
 *  timetable_engine.py (verified ISNA timings, 2026-10-11 → 2027-06-05).  This script is
 *  the OPTIONAL automation layer that only Google can run from inside your account:
 *
 *   1. setupTrackerSheet()              — adds the Status dropdown, colours and layout to the
 *                                          "40-Prayer Habit Tracker" Google Sheet.
 *   2. syncCalendarCheckmarksToSheet()   — reads prayer events you ticked off in the calendar
 *                                          ("[ ]" → "[x]" or "✅") and writes On-Time / Late /
 *                                          Missed into the Sheet (streak formula does the rest).
 *   3. installHourlyTrigger()            — schedules (2) to run every hour.
 *   4. extendCalendar("2027-06-06", "2027-07-05")
 *                                        — generates the same block system for any later range
 *                                          (e.g. into 1449 AH) with a duplicate guard.
 *   5. deleteLRIBEvents("2027-06-06", "2027-07-05")
 *                                        — removes events created by this system in a range.
 *
 *  Location  : Manhattan, NY (E 61st St & York Ave) 40.7610, -73.9590
 *  Method    : ISNA (Fajr 15°, Isha 15°, Maghrib = sunset, Asr standard) via Aladhan API
 *  Time zone : America/New_York  (set the project time zone to this in appsscript.json)
 * =====================================================================================
 */

const CONFIG = {
  CALENDAR_NAME: "Lunar Rhythm & Intentional Blocks",
  SHEET_URL: "PASTE_YOUR_TRACKER_SHEET_URL_HERE",
  LATITUDE: 40.7610,
  LONGITUDE: -73.9590,
  METHOD: 2,                          // Aladhan: ISNA
  TIMEZONE: "America/New_York",
  PRAYER_EVENT_MINUTES: 25,
  MISSED_GRACE_HOURS: 3,              // an un-ticked prayer is logged "Missed" this long after its window closes
  COLORS: {                           // Google Calendar event colorIds
    B0: "3", B1: "7", B2: "5", B3: "6", B4: "11", B5: "9", B6: "8",
    PRAYER: "10", ANCHOR: "2", HEADER: "1", MILESTONE: "4", NOTE: "8",
  },
};

const RULE_OF_3 =
  "🛑 RULE OF 3: PRE-BLOCK INTENTIONS 🛑\n" +
  "Before beginning this block, define exactly what you will do:\n" +
  "1. [ ] Task: _________________ (Est Time: ___ mins)\n" +
  "2. [ ] Task: _________________ (Est Time: ___ mins)\n" +
  "3. [ ] Task: _________________ (Est Time: ___ mins)";

const HIJRI_MONTHS = {
  1: "Muharram", 2: "Safar", 3: "Rabi' al-Awwal", 4: "Rabi' al-Thani", 5: "Jumada al-Ula",
  6: "Jumada al-Akhirah", 7: "Rajab", 8: "Sha'ban", 9: "Ramadan", 10: "Shawwal",
  11: "Dhul-Qi'dah", 12: "Dhul-Hijjah",
};

const ANCHORS = {
  1:  { theme: "The Sacred Threshold & Renewal", anchor: "You are at the baseline. Build sustainable roots.",
        meaning: "'Muharram' = forbidden/sacred. Establish an internal ceasefire: forgive cognitive and emotional debts, wipe the slate, lay quiet foundational habits." },
  2:  { theme: "The Departure & Kinetic Momentum", anchor: "Action precedes clarity. Move through resistance.",
        meaning: "'Safar' = empty: homes emptied as people set out. Dismantle hesitation and executive paralysis; convert theory into kinetic momentum." },
  3:  { theme: "The Spring of Character", anchor: "Master your state. Elevate character above speed.",
        meaning: "'Rabi' al-Awwal' = first spring; the Prophet's ﷺ birth month. Center on akhlaq, mercy and dignified cadence." },
  4:  { theme: "Deep Roots & Quiet Tenacity", anchor: "Trust the invisible compounding.",
        meaning: "'Rabi' al-Thani' = second spring. Roots dig beneath the soil before anything is visible: quiet, unglamorous consistency." },
  5:  { theme: "Solidification & Crystallization", anchor: "Eliminate the non-essential. Protect your energy.",
        meaning: "'Jumada' = parched/frozen ground. Freeze frivolous commitments, seal energetic leaks, firm up non-negotiable boundaries." },
  6:  { theme: "Clearing the Decks", anchor: "Close all open tabs. Empty the mental cache.",
        meaning: "Last ordinary month before the sacred trimester (Rajab → Sha'ban → Ramadan). Audit every open loop and prepare the vessel." },
  7:  { theme: "The Sacred Sowing", anchor: "What you do not plant in Rajab cannot bloom in Ramadan.",
        meaning: "'Rajab' = to revere; a sacred month. 'Rajab is the month of sowing, Sha'ban of irrigating, Ramadan of harvesting.' Plant Qur'an, fasting and focus." },
  8:  { theme: "Irrigation & Athletic Conditioning", anchor: "Pre-warm the engine. No cold starts.",
        meaning: "'Sha'ban' = to branch out. The Prophet ﷺ fasted most in Sha'ban after Ramadan. Raise fasting, night vigilance and stamina now." },
  9:  { theme: "The Furnace & the Harvest — PEAK MILESTONE 1", anchor: "All standard rules suspend. Maximum spiritual focus.",
        meaning: "'Ramadan' = scorching heat. Burning away impurities; reaping every seed sown in Rajab and watered in Sha'ban. Laylat al-Qadr in the odd nights of the last ten." },
  10: { theme: "Eid al-Fitr · Elevation & Carrying the Gains", anchor: "Retain the altitude gained in the furnace.",
        meaning: "'Shawwal' = to lift and carry. Eid on the 1st; the six fasts any time this month. Refuse the post-Ramadan slump." },
  11: { theme: "The Sacred Encampment", anchor: "Stillness before the mountain.",
        meaning: "'Qi'dah' = sitting, halting. Sacred month: settle worldly accounts, gather provisions of taqwa, quiet the nervous system." },
  12: { theme: "The Summit — PEAK MILESTONE 2", anchor: "The summit. Offer your greatest sacrifice.",
        meaning: "The month of pilgrimage. The first ten days are the best of the year; Arafah on the 9th, Eid al-Adha on the 10th, Tashreeq 11–13." },
};

// =====================================================================================
// 1. TRACKER SHEET SETUP  (dropdown + colours on the Sheet created from prayer_log.csv)
// =====================================================================================
function setupTrackerSheet() {
  const ss = SpreadsheetApp.openByUrl(CONFIG.SHEET_URL);
  const sh = ss.getSheets()[0];
  sh.setName("Prayer_Log");
  const lastRow = sh.getLastRow();
  const statusRange = sh.getRange(8, 7, Math.max(lastRow - 7, 1), 1);   // G8:G
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["On-Time", "Late", "Missed"], true).setAllowInvalid(false).build();
  statusRange.setDataValidation(rule);

  sh.setFrozenRows(7);
  sh.getRange("A1").setFontSize(14).setFontWeight("bold");
  sh.getRange("A2:G2").setFontWeight("bold").setFontColor("#64748b").setFontSize(9);
  sh.getRange("A3:G3").setFontSize(20).setFontWeight("bold").setHorizontalAlignment("center");
  sh.getRange("A3").setFontColor("#0ea5e9");
  sh.getRange("B3").setFontColor("#22c55e");
  sh.getRange("D3").setFontColor("#ef4444");
  sh.getRange("A7:I7").setFontWeight("bold").setBackground("#1e293b").setFontColor("#f8fafc");
  const widths = [190, 100, 190, 80, 70, 70, 100, 70, 260];
  widths.forEach((w, i) => sh.setColumnWidth(i + 1, w));

  const rules = sh.getConditionalFormatRules().filter(r => true);
  const mk = (text, bg) => SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(text)
    .setBackground(bg).setRanges([statusRange]).build();
  sh.setConditionalFormatRules([...rules, mk("On-Time", "#bbf7d0"), mk("Late", "#fde68a"), mk("Missed", "#fecaca")]);
  Logger.log("✅ Tracker sheet formatted: dropdown, colours, frozen header. Rows: " + lastRow);
}

// =====================================================================================
// 2. CALENDAR CHECKMARK → SHEET SYNC
// =====================================================================================
function syncCalendarCheckmarksToSheet() {
  const cal = getCalendar_();
  const ss = SpreadsheetApp.openByUrl(CONFIG.SHEET_URL);
  const sh = ss.getSheets()[0];
  const data = sh.getDataRange().getValues();
  const rowById = {};
  for (let r = 7; r < data.length; r++) if (data[r][0]) rowById[String(data[r][0])] = r + 1;

  const now = new Date();
  const from = new Date(now.getTime() - 4 * 24 * 3600 * 1000);
  const events = cal.getEvents(from, now);
  let updated = 0;
  events.forEach(ev => {
    const title = ev.getTitle();
    if (title.indexOf("🕌") < 0) return;
    const m = (ev.getDescription() || "").match(/LRIB-ID:\s*(\S+-P-[A-Z]+)/);
    if (!m) return;
    const id = m[1];
    const row = rowById[id];
    if (!row) return;
    const current = String(data[row - 1][6] || "");
    if (current) return;                                   // never overwrite a logged value
    const closes = (ev.getDescription() || "").match(/window closes (\d{2}):(\d{2})/);
    const start = ev.getStartTime();
    let windowEnd = new Date(start.getTime() + 60 * 60 * 1000);
    if (closes) {
      windowEnd = new Date(start);
      windowEnd.setHours(parseInt(closes[1], 10), parseInt(closes[2], 10), 0, 0);
      if (windowEnd <= start) windowEnd = new Date(windowEnd.getTime() + 24 * 3600 * 1000);   // Isha → midnight
    }
    const ticked = /^\s*(\[x\]|\[X\]|✅)/.test(title);
    let status = "";
    if (ticked) {
      status = ev.getLastUpdated() <= windowEnd ? "On-Time" : "Late";
    } else if (now.getTime() > windowEnd.getTime() + CONFIG.MISSED_GRACE_HOURS * 3600 * 1000) {
      status = "Missed";
    }
    if (!status) return;
    sh.getRange(row, 7).setValue(status);
    sh.getRange(row, 9).setValue((ticked ? "Ticked in calendar at " : "Auto-logged (no tick by) ") +
      Utilities.formatDate(ticked ? ev.getLastUpdated() : now, CONFIG.TIMEZONE, "yyyy-MM-dd HH:mm"));
    updated++;
  });
  Logger.log(`🔄 Sync complete: ${updated} prayer row(s) updated.`);
}

function installHourlyTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === "syncCalendarCheckmarksToSheet") ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger("syncCalendarCheckmarksToSheet").timeBased().everyHours(1).create();
  Logger.log("⏰ Hourly sync trigger installed.");
}

// =====================================================================================
// 3. EXTEND THE CALENDAR (same block logic as timetable_engine.py)
// =====================================================================================
function extendCalendar(startDateStr, endDateStr) {
  const cal = getCalendar_();
  let d = parseDate_(startDateStr || Utilities.formatDate(new Date(), CONFIG.TIMEZONE, "yyyy-MM-dd"));
  const end = parseDate_(endDateStr || Utilities.formatDate(addDays_(new Date(), 29), CONFIG.TIMEZONE, "yyyy-MM-dd"));
  const t0 = Date.now();
  let created = 0, skipped = 0;
  while (d <= end) {
    if (Date.now() - t0 > 270000) { Logger.log("⏱ Near the 6-minute limit — re-run extendCalendar from " + fmtDate_(d)); break; }
    const day = getAladhanDay_(d);
    if (!day) { Logger.log("⚠️ No timing data for " + fmtDate_(d)); d = addDays_(d, 1); continue; }
    const dateKey = fmtDate_(d);
    const existing = cal.getEvents(d, addDays_(d, 1)).filter(e => (e.getDescription() || "").indexOf("LRIB-ID: " + dateKey) >= 0);
    if (existing.length) { skipped++; d = addDays_(d, 1); continue; }
    created += createDay_(cal, d, day);
    d = addDays_(d, 1);
  }
  Logger.log(`✅ extendCalendar: ${created} events created, ${skipped} day(s) skipped (already present).`);
}

function createDay_(cal, d, day) {
  const T = {};
  ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"].forEach(k => { T[k] = new Date(day.timings[k].split(" ")[0]); });
  const midnight = addDays_(parseDate_(fmtDate_(d)), 1);
  const h = day.date.hijri;
  const hijri = `${parseInt(h.day, 10)} ${HIJRI_MONTHS[parseInt(h.month.number, 10)]} ${h.year} AH`;
  const head = `🌙 ${hijri} · ${Utilities.formatDate(d, CONFIG.TIMEZONE, "EEE dd MMM yyyy")}`;
  const dateKey = fmtDate_(d);
  const blocks = [
    ["B0", "🌌 B0 · Pre-Dawn (Tahajjud)", addMin_(T.Fajr, -45), T.Fajr, "Pre-dawn stillness, du'a and spiritual grounding.", [0]],
    ["B1", "🌅 B1 · Dawn / First Light", T.Fajr, addMin_(T.Sunrise, -10), "Fajr at the earliest time, morning adhkar. Hard stop 10 min before sunrise.", []],
    ["B2", "☀️ B2 · High Dopamine Core Work", addMin_(T.Sunrise, 15), T.Dhuhr, "Warm 10 AM sun. Core work, high dopamine. ⚠️ NO SLEEPING.", [35, 10]],
    ["B3", "🟧 B3 · Core Wrap-Up", T.Dhuhr, T.Asr, "Pray Dhuhr, then taper: wrap up core work and close loops.", [10]],
    ["B4", "🌇 B4 · Afternoon & Sunset Prep", T.Asr, addMin_(T.Maghrib, -15), "Pray Asr. Outdoors, errands, fresh air. Hard stop 15 min before Maghrib.", [10]],
    ["B5", "🔵 B5 · Evening Reset", T.Maghrib, T.Isha, "Pray Maghrib at the earliest time. Supper, home, wind down, possible swim.", [25]],
    ["B6", "⚫ B6 · Wind Down to Sleep", T.Isha, midnight, "Isha & Witr. Full wind-down; sleep by midnight.", [10]],
  ];
  let n = 0;
  blocks.forEach(([key, title, s, e, theme, rem]) => {
    const ev = cal.createEvent(title, s, e, {
      description: `${head}\n⏱ WINDOW: ${fmtTime_(s)} → ${fmtTime_(e)}\nTHEME: ${theme}\n\n${RULE_OF_3}\nLRIB-ID: ${dateKey}-${key}`,
    });
    ev.setColor(CONFIG.COLORS[key]);
    ev.removeAllReminders();
    rem.forEach(m => ev.addPopupReminder(m));
    n++;
  });
  const windows = { Fajr: addMin_(T.Sunrise, -10), Dhuhr: T.Asr, Asr: addMin_(T.Maghrib, -15), Maghrib: T.Isha, Isha: midnight };
  Object.keys(windows).forEach(name => {
    const s = T[name], cutoff = windows[name];
    const ev = cal.createEvent(`[ ] 🕌 ${name} · by ${fmtTime_(cutoff)}`, s, addMin_(s, CONFIG.PRAYER_EVENT_MINUTES), {
      description: `🕌 40-PRAYER STREAK · ${name.toUpperCase()} · ${hijri}\nAdhan ${fmtTime_(s)} · on-time window closes ${fmtTime_(cutoff)}\n` +
        `✅ Tick off: edit the title "[ ]" → "[x]" when prayed inside the window.\n📊 Tracker: ${CONFIG.SHEET_URL}\nLRIB-ID: ${dateKey}-P-${name.toUpperCase()}`,
    });
    ev.setColor(CONFIG.COLORS.PRAYER);
    ev.removeAllReminders();
    ev.addPopupReminder(0);
    n++;
  });
  const hd = cal.createAllDayEvent(`🌙 ${parseInt(h.day, 10)} ${HIJRI_MONTHS[parseInt(h.month.number, 10)]} ${h.year}`, d,
    { description: `${head}\nFajr ${fmtTime_(T.Fajr)} · Sunrise ${fmtTime_(T.Sunrise)} · Dhuhr ${fmtTime_(T.Dhuhr)} · Asr ${fmtTime_(T.Asr)} · Maghrib ${fmtTime_(T.Maghrib)} · Isha ${fmtTime_(T.Isha)}\nLRIB-ID: ${dateKey}-HDR` });
  hd.setColor(CONFIG.COLORS.HEADER); hd.removeAllReminders(); n++;
  if (parseInt(h.day, 10) === 1) {
    const a = ANCHORS[parseInt(h.month.number, 10)];
    const an = cal.createAllDayEvent(`🌙 1 ${HIJRI_MONTHS[parseInt(h.month.number, 10)]} ${h.year} — ${a.theme}`, d,
      { description: `• Associative meaning: ${a.meaning}\n• Executive anchor: ${a.anchor}\nLRIB-ID: ${dateKey}-ANCHOR` });
    an.setColor(CONFIG.COLORS.ANCHOR); an.removeAllReminders(); n++;
  }
  return n;
}

// =====================================================================================
// 4. CLEANUP
// =====================================================================================
function deleteLRIBEvents(startDateStr, endDateStr) {
  const cal = getCalendar_();
  const s = parseDate_(startDateStr), e = addDays_(parseDate_(endDateStr), 1);
  let n = 0;
  cal.getEvents(s, e).forEach(ev => { if ((ev.getDescription() || "").indexOf("LRIB-ID:") >= 0) { ev.deleteEvent(); n++; } });
  Logger.log(`🧹 Deleted ${n} LRIB events between ${startDateStr} and ${endDateStr}.`);
}

// =====================================================================================
// Helpers
// =====================================================================================
function getCalendar_() {
  const cals = CalendarApp.getCalendarsByName(CONFIG.CALENDAR_NAME);
  if (!cals.length) throw new Error(`Calendar "${CONFIG.CALENDAR_NAME}" not found — create it in Google Calendar first.`);
  return cals[0];
}
const ALADHAN_CACHE_ = {};
function getAladhanDay_(d) {
  const y = d.getFullYear(), m = d.getMonth() + 1, key = `${y}-${m}`;
  if (!ALADHAN_CACHE_[key]) {
    const url = `https://api.aladhan.com/v1/calendar/${y}/${m}?latitude=${CONFIG.LATITUDE}&longitude=${CONFIG.LONGITUDE}&method=${CONFIG.METHOD}&iso8601=true`;
    const res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) throw new Error("Aladhan API error " + res.getResponseCode());
    ALADHAN_CACHE_[key] = JSON.parse(res.getContentText()).data;
  }
  const dd = d.getDate();
  return ALADHAN_CACHE_[key].find(x => parseInt(x.date.gregorian.day, 10) === dd) || null;
}
function parseDate_(s) { return Utilities.parseDate(s + " 00:00:00", CONFIG.TIMEZONE, "yyyy-MM-dd HH:mm:ss"); }
function fmtDate_(d) { return Utilities.formatDate(d, CONFIG.TIMEZONE, "yyyy-MM-dd"); }
function fmtTime_(d) { return Utilities.formatDate(d, CONFIG.TIMEZONE, "HH:mm"); }
function addDays_(d, n) { return new Date(d.getTime() + n * 86400000); }
function addMin_(d, n) { return new Date(d.getTime() + n * 60000); }
