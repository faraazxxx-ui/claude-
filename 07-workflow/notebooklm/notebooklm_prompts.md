# NotebookLM Prompts for Progressive Health Analysis

This document contains a series of structured prompts designed to be used with the `health_data_source.md` file in Google NotebookLM. These prompts follow a layered approach, moving from high-level summaries to specific, correlational analyses.

---

### Prompt 1: High-Level Health Summary

**Goal**: Get a quick overview of the most critical health metrics.

```
Based on the provided health data, summarize the following key metrics from the last 30 days:

*   Average, minimum, and maximum Heart Rate Variability (HRV).
*   Average, minimum, and maximum Resting Heart Rate (RHR).
*   Average sleep duration and sleep efficiency.
*   Trend in Day Strain over the last month.

Present the summary in a table.
```

---

### Prompt 2: Sleep Pattern Analysis

**Goal**: Dive deeper into sleep quality and identify potential issues.

```
Analyze the sleep data in detail. Focus on the following aspects:

*   Identify the nights with the lowest deep sleep and REM sleep durations. Are there any corresponding notes or events on those days?
*   Chart the variability in sleep onset and wake onset times. How consistent is the sleep schedule?
*   Is there a correlation between sleep efficiency and the reported 'Recovery' score the next day? Provide specific examples.
```

---

### Prompt 3: Autonomic Nervous System (ANS) Balance

**Goal**: Assess the state of the autonomic nervous system, which is critical for POTS and dysautonomia.

```
Using the HRV and RHR data, assess the balance of the autonomic nervous system. 

*   Plot the daily HRV and RHR on the same chart. Are they inversely correlated as expected?
*   Identify periods (3 or more consecutive days) of sustained low HRV (< 25ms) and high RHR (> 80bpm). 
*   Correlate these periods of poor ANS balance with the 'Day Strain' and subjective symptom reports if available.
```

---

### Prompt 4: Activity vs. Recovery Analysis

**Goal**: Understand the impact of physical activity on recovery, a key aspect of managing post-exertional malaise (PEM).

```
Analyze the relationship between 'Day Strain' and the next day's 'Recovery' score.

*   Are there instances where a high Day Strain is followed by a significantly lower Recovery score?
*   What is the average Day Strain on days preceding a 'Red' recovery day (Recovery < 33%)?
*   Based on the data, what appears to be a sustainable level of Day Strain that does not negatively impact next-day recovery?
```

---

### Prompt 5: Longitudinal Trend Analysis (Progressive Prompt)

**Goal**: Track progress and changes over a longer timeframe. This prompt is designed to be used repeatedly as new data is added.

```
Compare the most recent week of data (provide dates) to the monthly average for the following metrics:

*   Heart Rate Variability (HRV)
*   Resting Heart Rate (RHR)
*   Total Sleep Duration
*   Day Strain

Has there been a statistically significant improvement, decline, or no change in these key indicators? Visualize the weekly trend against the monthly baseline.
```
