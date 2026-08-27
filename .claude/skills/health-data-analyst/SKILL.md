---
name: health-data-analyst
description: >
  Analyzes personal health and wearable data (Oura, WHOOP, Visible) for a physician with Long COVID, POTS, and autonomic dysfunction. Use when the user provides new health data files and asks for analysis, trend identification, or visualization related to their ongoing medical conditions. This skill synthesizes physiological data with a deep, pre-existing medical context to provide longitudinal tracking.
---

# Health Data Analyst Skill

This skill provides a structured workflow for analyzing and reporting on the user's personal health data. The user is a physician with a known history of Long COVID, POTS, and autonomic dysfunction. The goal is to provide ongoing, progressive analysis that incorporates new data into a unified, long-term understanding of their health.

## Core Principles

1.  **Narrative First**: The user is a verbal thinker. All output MUST be a progressive clinical narrative that tells the story of what is happening to his body, not just tables of numbers. Always explain the *why*, not just the *what*.
2.  **Integrated Analysis**: NEVER analyze data sources in isolation. ALWAYS cross-reference WHOOP physiology, Oura ring data, Visible app symptoms, medication logs, and life event notes by date to build a unified picture.
3.  **Event-Aware**: ALWAYS check for life events, stressors, and context notes in the Visible app data. These are often the primary explanation for physiological changes. Never say "investigate triggers" when the triggers are in the data.
4.  **Context is King**: All analysis MUST be performed through the lens of the user's specific, complex medical history. The foundational medical context is stored in the `references/` directory.

## Workflow

### Step 1: Ingest and Process New Data

Run the v2 integrated processing script. This script cross-references ALL data sources, detects medication changes, computes period comparisons, flags anomalies, and builds a unified daily timeline.

```bash
python3 /home/ubuntu/skills/health-data-analyst/scripts/process_health_data.py
```

The script outputs to `/home/ubuntu/work/v2/`:
- `unified_timeline.csv` — All data merged by date
- `period_comparison.csv` — Statistics for key time periods
- `medication_adherence.json` — Adherence rates per medication
- `anomalies.csv` — Flagged clinical anomalies (RHR >130, HRV <10, etc.)
- `life_events.csv` — Extracted from Visible app notes
- `monthly_trends.csv` — Month-over-month metrics
- `symptom_correlations.json` — Symptom-physiology correlations

### Step 2: Load Medical Context

```python
default_api.file(action="read", path="/home/ubuntu/skills/health-data-analyst/references/unified_model.md")
default_api.file(action="read", path="/home/ubuntu/skills/health-data-analyst/references/compass_artifact.md")
```

### Step 3: Perform Integrated Analysis

With the processed data and medical context loaded, perform analysis following this order:

1.  **Life Events & Context**: Start by reading the life events and notes. These often explain everything else.
2.  **Medication Adherence**: Check for changes in medication patterns. Correlate with physiological changes.
3.  **Autonomic Balance**: Analyze HRV and RHR trends through the lens of identified events and medication changes.
4.  **Sleep & Circadian**: Examine sleep duration, onset timing chaos, and architecture.
5.  **Symptom-Physiology Correlation**: Cross-reference Visible symptoms with WHOOP/Oura metrics.
6.  **Period Comparison**: Compare current period to historical baseline AND the patient's best period (Jul-Aug 2025).

**Critical Red-Team Lessons:**
- The recovery score paradox: WHOOP recovery can be paradoxically HIGH during crashes if stimulant use decreases. Do not trust recovery scores in isolation.
- Always compute pre-event vs post-event statistics for any identified stressor.
- Flag any Visible RHR >120 bpm as a possible POTS episode.
- The patient's sleep onset SD of ~5.75 hours is equivalent to chronic shift work.

### Step 4: Generate Visualizations

Generate clinically annotated charts. Every time-series chart MUST include:
- Vertical lines for life events (color-coded by severity)
- Shaded regions for key periods (e.g., Ramadan, best period)
- Medication adherence overlay where relevant
- Baseline reference lines

Required charts:
1. **The Full Arc** — Monthly HRV/RHR with period annotations
2. **The Crisis** — Event-annotated 30-day deep dive (4-panel: HRV, RHR, Recovery, Medications)
3. **Symptom Heatmap** — Daily symptom severity with event markers
4. **Medication Adherence** — Horizontal bar chart with adherence % and context
5. **Period Comparison** — Multi-metric comparison across key periods
6. **Sleep & Circadian** — Duration trends + onset timing chaos

### Step 5: Write the Narrative Report

Structure the report as a progressive story, NOT a domain-by-domain analysis:
1. **The Peak**: What the patient's system is capable of at its best
2. **The Fall**: What changed and when the decline began
3. **The Crash**: The specific sequence of events that caused the acute crisis
4. **The Paradox**: Explain any confusing patterns (e.g., high recovery during crash)
5. **The Path Forward**: Actionable clinical priorities

### Step 6: Deliver the Final Output

Deliver the report as a markdown file with embedded chart references. Attach all charts as separate PNG files.
