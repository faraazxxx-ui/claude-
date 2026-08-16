---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
week: <% tp.date.now("YYYY-[W]WW") %>
tags: [daily-note, health-log]
cssclasses: [health-daily]
aliases: [<% tp.date.now("YYYY-MM-DD") %>]
prev: "[[<% tp.date.now('YYYY-MM-DD', -1) %>]]"
next: "[[<% tp.date.now('YYYY-MM-DD', 1) %>]]"
---

# <% tp.date.now("ddd MMM D") %> — [[<% tp.date.now("YYYY-[W]WW") %>|Week <% tp.date.now("WW") %>]]

> ← [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>]] →

---

## ⚡ Quick Log *(60 seconds — do this every day, even on red days)*

recovery:: <%* const r = await tp.system.suggester(["🔴 Red","🟡 Yellow","🟢 Green"], ["🔴","🟡","🟢"]); tR += r; %>
pem_risk:: <%* const p = await tp.system.suggester(["High","Mod","Low"], ["high","mod","low"]); tR += p; %>
functional_capacity:: /10
bed_time:: 
wake_time:: 
sleep_hrs:: 

stimulant:: ✅❌
antihypertensive:: ✅❌
nicotine_count:: 
hydration_oz:: 
sodium_g:: 

day_summary:: >  

---

## 🩺 Subjective State *(skip on red days if needed)*

*Rate 0–10. Only log what's notable — zeros don't need entries.*

fatigue:: /10
palpitations:: /10
brain_fog:: /10
orthostatic:: /10
anxiety:: /10
gi:: /10
focus:: /10
mood:: 
stress:: /10

worst_symptom:: 
worst_symptom_trigger:: 

---

## 📊 Context *(the "why" — this is what your wearables can't capture)*

*Dictate via Wispr Flow / Superwhisper. Raw voice > silence.*

**Sleep context** — what time in bed, what disrupted it:
> 

**Triggers / stressors today**:
> 

**Diet** — anything notable (meal timing, caffeine, alcohol):
> 

**Deviations from routine**:
> 

---

## 💊 Medication Detail *(expand if timing matters today)*

| Med | Time | Dose | Note |
|-----|------|------|------|
| Stimulant | | | |
| Antihypertensive | | | |
| GLP-1 | | | |
| Other | | | |

last_nicotine_time:: 
last_stimulant_time:: 

---

## 🌙 Wind-Down *(fill ~90 min before target sleep)*

target_lights_out:: 
- [ ] Screens off
- [ ] Room cool (65–68°F)
- [ ] Last nicotine >3 hrs ago
- [ ] Last stimulant >6 hrs ago
- [ ] Water logged
- [ ] Antihypertensive taken (if evening dose)
tomorrow_wake:: 

---

## 📝 Notes

> 

---

## 🤖 Analysis Trigger

*Accumulate 7+ days, then dictate or paste into Claude / @health-data-analyst:*

> Analyze my last [N] days. Flags: antihypertensive adherence [X/Y], hydration adequate [X/Y], PEM crashes [describe], nicotine trend [up/down/stable]. Run against [[prompts/medical_context|medical_context.md]] baseline. Attach: WHOOP CSVs, Oura export, Visible export.

---

*v2.0 — Red-team rebuilt for compliance. Optimized for ADHD + fatigue + voice-first workflow.*
*Dataview-queryable via inline fields. Weekly summary auto-generated — see [[weekly_review_template]].*
*Context: [[prompts/medical_context]] | Skill: [[skill/health-data-analyst/SKILL]]*
