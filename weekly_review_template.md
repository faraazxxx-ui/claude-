---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("YYYY-[W]WW") %>
tags: [weekly-review, health-log]
cssclasses: [health-weekly]
---

# Week <% tp.date.now("WW") %> Review — <% tp.date.now("MMM D, YYYY") %>

> Auto-computed from daily notes via Dataview. Manual override cells marked with ✏️.

---

## 📊 Weekly Metrics (Dataview Auto-Summary)

```dataview
TABLE
  recovery AS "Recovery",
  sleep_hrs AS "Sleep",
  stimulant AS "Stim",
  antihypertensive AS "AH",
  nicotine_count AS "Nic",
  hydration_oz AS "H₂O",
  functional_capacity AS "Func",
  fatigue AS "Fat",
  palpitations AS "Palp"
FROM #daily-note
WHERE week = this.week
SORT date ASC
```

---

## 📈 Aggregates vs. Baseline

*Baselines from [[prompts/medical_context]] (400+ days, 2024–2026). Update if baseline shifts.*

| Metric | This Week | Historical Baseline | Δ | Trend |
|--------|-----------|---------------------|---|-------|
| Antihypertensive adherence | /7 | 2.5/7 (36%) | | |
| Hydration adequate (≥84 oz) | /7 | 0.6/7 (9%) | | |
| Green recovery days | /7 | 0.7/7 (10%) | | |
| Mean nicotine count | | — | | |
| Mean functional capacity | /10 | — | | |
| PEM crashes | | — | | |

---

## 🔑 Pattern Recognition

**Best day this week (and why)**:
> 

**Worst day this week (and why)**:
> 

**Emerging pattern** (correlation you noticed):
> 

---

## 🎯 Single Priority

**Last week's target**: 
**Result**: ✅ Hit / ❌ Missed / 🟡 Partial

**This week's single highest-priority intervention**:
> 

---

*Context: [[prompts/medical_context]] | Daily template: [[daily_note_template]]*
