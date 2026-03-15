---
name: health-data-analyst
description: >
  Analyzes personal health and wearable data (Oura, WHOOP, Visible) for a physician with Long COVID, POTS, and autonomic dysfunction. Use when the user provides new health data files and asks for analysis, trend identification, or visualization related to their ongoing medical conditions. This skill synthesizes physiological data with a deep, pre-existing medical context to provide longitudinal tracking.
---

# Health Data Analyst Skill

This skill provides a structured workflow for analyzing and reporting on the user's personal health data. The user is a physician with a known history of Long COVID, POTS, and autonomic dysfunction. The goal is to provide ongoing, progressive analysis that incorporates new data into a unified, long-term understanding of their health.

## Core Principles

1.  **Context is King**: All analysis MUST be performed through the lens of the user's specific, complex medical history. The foundational medical context is stored in the `references/` directory.
2.  **Automation First**: Use the provided script to process raw data into a clean, unified format before analysis.
3.  **Structured Analysis**: Follow a consistent, multi-step analytical process to ensure all key areas are covered.
4.  **Longitudinal View**: Frame all findings in the context of long-term trends, comparing new data to historical baselines.

## Workflow

### Step 1: Ingest and Process New Data

When the user uploads new health data files (typically CSVs from Oura, Visible, etc.), your first action is to run the processing script. This script will read the new raw data, merge it with historical data if necessary, and generate a single, unified Markdown report in the `/home/ubuntu/work/` directory.

```bash
python3 /home/ubuntu/skills/health-data-analyst/scripts/process_health_data.py
```

This script is designed to handle the various formats of the user's data exports and consolidate them into a clean, table-based format suitable for analysis.

### Step 2: Load Medical Context

Before analyzing the processed data, you MUST load the user's detailed medical context. These documents provide the pathophysiological framework for understanding the data.

```python
default_api.file(action="read", path="/home/ubuntu/skills/health-data-analyst/references/unified_model.md")
default_api.file(action="read", path="/home/ubuntu/skills/health-data-analyst/references/compass_artifact.md")
```

Reading these files will provide you with the necessary background on the user's condition, including the core "self-amplifying loop" model of their illness.

### Step 3: Perform Structured Analysis

With the processed data and medical context loaded, perform a structured analysis. Address the following areas in order, using the insights from the reference documents to guide your interpretation.

1.  **Autonomic Balance**: Analyze HRV and RHR trends. Correlate periods of low HRV / high RHR with activity levels and subjective symptoms.
2.  **Sleep Quality & Architecture**: Examine sleep duration, efficiency, and stages (Deep, REM). Look for correlations between poor sleep and next-day recovery or symptom severity.
3.  **Activity vs. Recovery**: Analyze the relationship between Day Strain (or equivalent activity metric) and next-day Recovery scores. Identify potential thresholds for post-exertional malaise (PEM).
4.  **Symptom Correlation**: Cross-reference subjective symptom logs (from Visible app data) with physiological data to identify potential triggers.

### Step 4: Generate Report and Visualizations

Synthesize your findings into a concise, professional report for the user. The report should follow the user's preferred format: final answer first, followed by a detailed breakdown in a markdown table.

*   **Summary**: Begin with a high-level summary of the key findings from the new data.
*   **Detailed Analysis**: Provide a section for each of the analytical areas from Step 3.
*   **Visualizations**: Where appropriate, generate charts (e.g., using Python's matplotlib/seaborn) to visualize key trends, such as HRV over time or the correlation between strain and recovery. Save charts as PNG files and embed them in your final report.
*   **Longitudinal Comparison**: Conclude by comparing the new data period to the user's historical baseline, noting any significant improvements or deteriorations.

### Step 5: Deliver the Final Output

Deliver the final report as a markdown file (`.md`). Attach any generated charts as separate image files.
