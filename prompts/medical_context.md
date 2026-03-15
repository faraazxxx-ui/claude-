# Master Medical Context for Dr. Mohammed Rahman

**Last Updated**: March 15, 2026

This document serves as the single source of truth for the patient's medical history, pathophysiological model, and historical data baseline. All AI analysis should be grounded in this context.

---

## 1. Patient Profile

*   **Name**: Dr. Mohammed Rahman
*   **Age**: 32
*   **Gender**: Male
*   **Occupation**: Physician
*   **Timezone**: America/New_York
*   **Diagnoses**: Long COVID (onset ~2023), Postural Orthostatic Tachycardia Syndrome (POTS), Autonomic Dysfunction.
*   **Medications**: ADHD Stimulant (adherence ~98%), Antihypertensive (adherence ~36%).
*   **Substances**: Nicotine (daily user).
*   **Key Lifestyle Factors**: Chronic sleep deprivation, chronic dehydration.

---

## 2. Unified Pathophysiological Model

The patient's condition is understood as a complex, self-amplifying system of five interconnected vicious cycles. Each node in the system exacerbates the others, leading to a state of autonomic collapse and persistent symptoms.

**The Five Vicious Cycles:**

1.  **Autonomic Collapse**: The initial insult from Long COVID (hypothesized to be vagal neuropathy and/or GPCR autoantibodies) created a foundational autonomic dysfunction. This is the core of the entire system.
2.  **Pharmacological Sympathetic Siege**: The compromised autonomic nervous system, with a weak parasympathetic "brake," is then overwhelmed by the daily sympathetic drive from ADHD stimulant medication and nicotine.
3.  **Cortisol-Visceral Fat Loop**: Chronic stress from poor sleep, dehydration, and the underlying illness elevates cortisol. This promotes the accumulation of visceral fat, which itself becomes an inflammatory organ, secreting adipokines that further suppress autonomic function.
4.  **Deconditioning Spiral**: POTS symptoms (orthostatic intolerance, palpitations) and fatigue lead to exercise intolerance and inactivity. This physical deconditioning worsens cardiac efficiency, which in turn exacerbates POTS symptoms, creating a downward spiral.
5.  **Sleep-Metabolic Cascade**: Extreme circadian disruption (high variability in sleep onset) and chronic sleep deprivation suppress critical hormones like melatonin and growth hormone, accelerating metabolic dysfunction and contributing to the cortisol loop.

**Key Insight**: No single node can be treated in isolation. Any effective intervention must address multiple nodes of this interconnected system simultaneously.

---

## 3. Historical Data Baseline (Dynamic)

This baseline represents the long-term average of key biometrics. It should be dynamically updated as new data becomes available. The current baseline is calculated from over 400 days of data from 2024 to early 2026.

| Metric | Value | Notes |
|---|---|---|
| **HRV (RMSSD)** | 20.4 ms | Mean. (2nd-5th percentile for age) |
| **Resting Heart Rate** | 84.1 bpm | Mean. |
| **Recovery Score** | 36% | Mean. (WHOOP metric) |
| **Red Recovery Days** | 49% | Percentage of days with recovery < 33% |
| **Green Recovery Days**| 10% | Percentage of days with recovery > 66% |
| **Total Sleep** | 5.0 hours | Mean per night. |
| **Sleep Onset SD** | 5.6 hours | Standard deviation of sleep start time. |
| **Daily Steps** | 5,406 | Mean. |
| **Fatigue Reports** | 75% | Percentage of days with subjective fatigue. |
| **Palpitation Reports**| 75% | Percentage of days with subjective palpitations. |

---

## 4. Data Sources

*   **WHOOP**: `physiological_cycles.csv`, `sleeps.csv`
*   **Oura Ring**: `Oura*.pdf`, `ring_data_*.csv`
*   **Visible App**: `Visible_Data_Export_*.csv` (for symptom tracking)
*   **Manual Logs**: Any `.md` or `.txt` files provided by the user.
