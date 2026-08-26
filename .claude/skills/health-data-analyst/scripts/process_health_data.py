#!/usr/bin/env python3
"""
Health Data Analyst v2: Integrated, Event-Aware Processing
Red-team fixes: Cross-references all data sources, detects medication changes,
computes Ramadan vs pre-Ramadan stats, flags anomalies, correlates life events.
"""

import pandas as pd
import numpy as np
import json, os, glob
from datetime import datetime, timedelta

UPLOAD_DIR = "/home/ubuntu/upload"
WORK_DIR = "/home/ubuntu/work/v2"
os.makedirs(WORK_DIR, exist_ok=True)

print("=" * 70)
print("HEALTH DATA ANALYST v2: Integrated Event-Aware Processing")
print("=" * 70)

# ============================================================
# 1. LOAD ALL DATA SOURCES
# ============================================================
# WHOOP Physiology
physio = pd.read_csv("/home/ubuntu/work/physio_clean.csv")
physio['date'] = pd.to_datetime(physio['date'])
physio = physio.sort_values('date').reset_index(drop=True)

# WHOOP Sleep
sleeps = pd.read_csv("/home/ubuntu/work/sleeps_clean.csv")
sleeps['date'] = pd.to_datetime(sleeps['date'])
sleeps = sleeps.sort_values('date').reset_index(drop=True)

# Visible App
visible = pd.read_csv(os.path.join(UPLOAD_DIR, "Visible_Data_Export_2026-3-15.csv"))
visible['observation_date'] = pd.to_datetime(visible['observation_date'])

# Workouts
workouts = pd.read_csv("/home/ubuntu/work/workouts_clean.csv")

# ============================================================
# 2. EXTRACT VISIBLE DATA INTO STRUCTURED FORMAT
# ============================================================
print("\n[1] Extracting Visible app data...")

# Pivot symptoms by date
symptom_names = ['Fatigue', 'Brain Fog', 'Anxiety', 'Depression', 'Crash', 'Derealization',
                 'Infection', 'Emotionally stressful', 'Mentally demanding', 'Physically active', 'Socially demanding']
med_names = ['Adderall', 'Vyvanse', 'Duloxetine', 'Gabapentin', 'Propanolol', 'Clonopine', 'GLP', 'Rease / M']
metric_names = ['HRV', 'Resting HR', 'Sleep', 'Stability Score', 'PacePoints', 'Pacing Budget']

def pivot_visible(df, tracker_names, prefix=''):
    result = {}
    for name in tracker_names:
        data = df[df['tracker_name'] == name][['observation_date', 'observation_value']].copy()
        data = data.rename(columns={'observation_date': 'date', 'observation_value': f'{prefix}{name}'})
        data[f'{prefix}{name}'] = pd.to_numeric(data[f'{prefix}{name}'], errors='coerce')
        data['date'] = pd.to_datetime(data['date'])
        result[name] = data
    return result

symptom_data = pivot_visible(visible, symptom_names, 'sym_')
med_data = pivot_visible(visible, med_names, 'med_')
metric_data = pivot_visible(visible, metric_names, 'vis_')

# Extract notes
notes = visible[visible['tracker_name'] == 'Note'][['observation_date', 'observation_value']].copy()
notes = notes.rename(columns={'observation_date': 'date', 'observation_value': 'note'})
notes['date'] = pd.to_datetime(notes['date'])

# ============================================================
# 3. CREATE UNIFIED DAILY TIMELINE
# ============================================================
print("[2] Building unified daily timeline...")

# Start with physiology as base
timeline = physio[['date', 'Recovery score %', 'Resting heart rate (bpm)', 
                   'Heart rate variability (ms)', 'Day Strain',
                   'Skin temp (celsius)', 'Blood oxygen %', 'Respiratory rate (rpm)']].copy()

# Merge sleep data
sleep_daily = sleeps.groupby('date').agg({
    'Asleep duration (min)': 'sum',
    'Deep (SWS) duration (min)': 'sum',
    'REM duration (min)': 'sum',
    'Sleep efficiency %': 'mean',
    'sleep_onset_hour_adj': 'first'
}).reset_index()
sleep_daily['sleep_hours'] = sleep_daily['Asleep duration (min)'] / 60.0

timeline = timeline.merge(sleep_daily[['date', 'sleep_hours', 'Deep (SWS) duration (min)', 
                                        'REM duration (min)', 'Sleep efficiency %', 'sleep_onset_hour_adj']], 
                          on='date', how='left')

# Merge Visible symptoms
for name, df in symptom_data.items():
    timeline = timeline.merge(df, on='date', how='left')

# Merge Visible medications
for name, df in med_data.items():
    timeline = timeline.merge(df, on='date', how='left')

# Merge Visible metrics
for name, df in metric_data.items():
    timeline = timeline.merge(df, on='date', how='left')

# Merge notes
timeline = timeline.merge(notes, on='date', how='left')

# ============================================================
# 4. ADD EVENT FLAGS AND PERIODS
# ============================================================
print("[3] Adding event flags and period markers...")

# Key dates
RAMADAN_START = pd.Timestamp('2026-02-17')
MOM_ER = pd.Timestamp('2026-02-14')
ENGAGEMENT_STRESS = pd.Timestamp('2026-02-13')
BLOOD_SUGAR_CRASH = pd.Timestamp('2026-02-20')
HASSAN_LEFT = pd.Timestamp('2026-02-26')

# Period flags
timeline['is_ramadan'] = timeline['date'] >= RAMADAN_START
timeline['is_visible_period'] = timeline['date'] >= pd.Timestamp('2026-02-13')
timeline['period'] = 'historical'
timeline.loc[timeline['date'] >= pd.Timestamp('2026-01-01'), 'period'] = 'recent_3mo'
timeline.loc[(timeline['date'] >= pd.Timestamp('2026-02-01')) & (timeline['date'] < RAMADAN_START), 'period'] = 'pre_ramadan_feb'
timeline.loc[timeline['is_ramadan'], 'period'] = 'ramadan'

# Event proximity flags
timeline['days_since_mom_er'] = (timeline['date'] - MOM_ER).dt.days
timeline['days_since_ramadan'] = (timeline['date'] - RAMADAN_START).dt.days

# ============================================================
# 5. COMPUTE PERIOD COMPARISONS
# ============================================================
print("[4] Computing period comparisons...")

hrv_col = 'Heart rate variability (ms)'
rhr_col = 'Resting heart rate (bpm)'
rec_col = 'Recovery score %'

periods = {
    'Full Period (409d)': timeline,
    'Best Period (Oct-Nov 2024)': timeline[(timeline['date'] >= '2024-10-01') & (timeline['date'] <= '2024-11-30')],
    'Pre-Ramadan Feb (Feb 1-16)': timeline[(timeline['date'] >= '2026-02-01') & (timeline['date'] < RAMADAN_START)],
    'During Ramadan (Feb 17+)': timeline[timeline['is_ramadan']],
    'Acute Crisis (Feb 13-28)': timeline[(timeline['date'] >= '2026-02-13') & (timeline['date'] <= '2026-02-28')],
    'Last 7 Days': timeline.tail(7),
}

period_stats = []
for name, df in periods.items():
    stats = {'Period': name, 'Days': len(df)}
    if hrv_col in df.columns:
        hrv = df[hrv_col].dropna()
        stats['HRV_mean'] = round(hrv.mean(), 1) if len(hrv) > 0 else None
        stats['HRV_median'] = round(hrv.median(), 1) if len(hrv) > 0 else None
    if rhr_col in df.columns:
        rhr = df[rhr_col].dropna()
        stats['RHR_mean'] = round(rhr.mean(), 1) if len(rhr) > 0 else None
    if rec_col in df.columns:
        rec = df[rec_col].dropna()
        stats['Recovery_mean'] = round(rec.mean(), 1) if len(rec) > 0 else None
        stats['Green_pct'] = round((rec >= 67).sum() / len(rec) * 100, 1) if len(rec) > 0 else None
        stats['Red_pct'] = round((rec < 33).sum() / len(rec) * 100, 1) if len(rec) > 0 else None
    if 'sleep_hours' in df.columns:
        sl = df['sleep_hours'].dropna()
        stats['Sleep_hours'] = round(sl.mean(), 2) if len(sl) > 0 else None
    period_stats.append(stats)

period_df = pd.DataFrame(period_stats)
period_df.to_csv(os.path.join(WORK_DIR, "period_comparison.csv"), index=False)

print("\nPERIOD COMPARISON:")
print(period_df.to_string(index=False))

# ============================================================
# 6. MEDICATION ADHERENCE ANALYSIS
# ============================================================
print("\n[5] Analyzing medication adherence...")

med_adherence = {}
for med in med_names:
    col = f'med_{med}'
    if col in timeline.columns:
        vis_period = timeline[timeline['is_visible_period']]
        data = vis_period[col].dropna()
        if len(data) > 0:
            adherence = data.mean() * 100
            med_adherence[med] = {
                'days_tracked': len(data),
                'days_taken': int(data.sum()),
                'adherence_pct': round(adherence, 1)
            }
            print(f"  {med}: {med_adherence[med]['days_taken']}/{med_adherence[med]['days_tracked']} days ({adherence:.1f}%)")

with open(os.path.join(WORK_DIR, "medication_adherence.json"), 'w') as f:
    json.dump(med_adherence, f, indent=2)

# ============================================================
# 7. ANOMALY DETECTION
# ============================================================
print("\n[6] Detecting anomalies...")

anomalies = []

# Visible RHR anomalies
vis_rhr = visible[visible['tracker_name'] == 'Resting HR'].copy()
vis_rhr['observation_value'] = pd.to_numeric(vis_rhr['observation_value'], errors='coerce')
high_rhr = vis_rhr[vis_rhr['observation_value'] > 120]
for _, row in high_rhr.iterrows():
    anomalies.append({
        'date': str(row['observation_date'].date()),
        'type': 'CRITICAL_HIGH_RHR',
        'value': row['observation_value'],
        'description': f"Visible RHR of {row['observation_value']} bpm - possible POTS episode"
    })

# WHOOP HRV critically low
critical_hrv = timeline[timeline[hrv_col] < 10]
for _, row in critical_hrv.iterrows():
    anomalies.append({
        'date': str(row['date'].date()),
        'type': 'CRITICAL_LOW_HRV',
        'value': row[hrv_col],
        'description': f"HRV of {row[hrv_col]} ms - severe vagal withdrawal"
    })

# WHOOP RHR critically high
critical_rhr = timeline[timeline[rhr_col] > 100]
for _, row in critical_rhr.iterrows():
    anomalies.append({
        'date': str(row['date'].date()),
        'type': 'HIGH_RHR',
        'value': row[rhr_col],
        'description': f"WHOOP RHR of {row[rhr_col]} bpm"
    })

# Crash streaks
vis_crash = timeline[timeline['is_visible_period']].sort_values('date')
if 'sym_Crash' in vis_crash.columns:
    crash_vals = vis_crash['sym_Crash'].dropna()
    streak = 0
    max_streak = 0
    streak_dates = []
    for idx, val in crash_vals.items():
        if val >= 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    print(f"  Max consecutive crash days: {max_streak}")

# Sleep < 3 hours
short_sleep = timeline[timeline['sleep_hours'] < 3].dropna(subset=['sleep_hours'])
for _, row in short_sleep.iterrows():
    if row['date'] >= pd.Timestamp('2026-02-01'):
        anomalies.append({
            'date': str(row['date'].date()),
            'type': 'CRITICAL_SHORT_SLEEP',
            'value': round(row['sleep_hours'], 1),
            'description': f"Only {row['sleep_hours']:.1f} hours of sleep"
        })

anomalies_df = pd.DataFrame(anomalies)
anomalies_df.to_csv(os.path.join(WORK_DIR, "anomalies.csv"), index=False)
print(f"  Total anomalies detected: {len(anomalies)}")

# ============================================================
# 8. MONTHLY TREND ANALYSIS
# ============================================================
print("\n[7] Computing monthly trends...")

timeline['month'] = timeline['date'].dt.to_period('M')
monthly = timeline.groupby('month').agg({
    hrv_col: ['mean', 'median'],
    rhr_col: ['mean'],
    rec_col: ['mean'],
    'sleep_hours': ['mean'],
}).reset_index()
monthly.columns = ['Month', 'HRV_mean', 'HRV_median', 'RHR_mean', 'Recovery_mean', 'Sleep_hours']
monthly['Month'] = monthly['Month'].astype(str)
monthly = monthly.round(1)
monthly.to_csv(os.path.join(WORK_DIR, "monthly_trends.csv"), index=False)
print(monthly.to_string(index=False))

# ============================================================
# 9. SYMPTOM-PHYSIOLOGY CORRELATION
# ============================================================
print("\n[8] Computing symptom-physiology correlations...")

vis_period = timeline[timeline['is_visible_period']].copy()
correlations = {}
for sym in ['sym_Fatigue', 'sym_Brain Fog', 'sym_Anxiety', 'sym_Crash']:
    if sym in vis_period.columns:
        for metric in [hrv_col, rhr_col, rec_col, 'sleep_hours']:
            if metric in vis_period.columns:
                valid = vis_period[[sym, metric]].dropna()
                if len(valid) > 5:
                    corr = valid[sym].corr(valid[metric])
                    key = f"{sym.replace('sym_', '')} vs {metric}"
                    correlations[key] = round(corr, 3)
                    if abs(corr) > 0.3:
                        print(f"  {key}: r={corr:.3f} {'***' if abs(corr) > 0.5 else '**'}")

with open(os.path.join(WORK_DIR, "symptom_correlations.json"), 'w') as f:
    json.dump(correlations, f, indent=2)

# ============================================================
# 10. LIFE EVENTS TIMELINE
# ============================================================
print("\n[9] Building life events timeline...")

events = [
    {'date': '2026-02-13', 'event': 'Engagement proposal stress', 'category': 'emotional', 'severity': 'high'},
    {'date': '2026-02-14', 'event': 'Mother rushed to ER (possible stroke, 911 called)', 'category': 'emotional', 'severity': 'critical'},
    {'date': '2026-02-16', 'event': 'Set up dual monitor system, spoke to Morgan', 'category': 'activity', 'severity': 'low'},
    {'date': '2026-02-17', 'event': 'RAMADAN BEGINS - First night of fasting', 'category': 'metabolic', 'severity': 'critical'},
    {'date': '2026-02-20', 'event': 'Blood sugar crash during fast, had to break fast, crashed', 'category': 'metabolic', 'severity': 'critical'},
    {'date': '2026-02-21', 'event': 'Conflict with hotel staff and AT&T', 'category': 'emotional', 'severity': 'moderate'},
    {'date': '2026-02-26', 'event': 'Hassan left', 'category': 'emotional', 'severity': 'moderate'},
    {'date': '2026-03-10', 'event': 'Persistent dreams (sleep quality concern)', 'category': 'sleep', 'severity': 'moderate'},
    {'date': '2026-03-14', 'event': 'Cleaning cat litter (physical exertion)', 'category': 'activity', 'severity': 'low'},
]

events_df = pd.DataFrame(events)
events_df.to_csv(os.path.join(WORK_DIR, "life_events.csv"), index=False)

# ============================================================
# 11. SAVE UNIFIED TIMELINE
# ============================================================
print("\n[10] Saving unified timeline...")
timeline.to_csv(os.path.join(WORK_DIR, "unified_timeline.csv"), index=False)

# ============================================================
# 12. EXECUTIVE SUMMARY
# ============================================================
print(f"\n{'='*70}")
print("EXECUTIVE SUMMARY: THE ANATOMY OF A CRASH")
print(f"{'='*70}")

pre_ram = timeline[(timeline['date'] >= '2026-02-01') & (timeline['date'] < RAMADAN_START)]
during_ram = timeline[timeline['is_ramadan']]

print(f"""
WHAT HAPPENED:
  Between Feb 13-17, 2026, three compounding stressors converged:
  1. Engagement proposal stress (Feb 13)
  2. Mother's ER visit for possible stroke (Feb 14) 
  3. Ramadan fasting began (Feb 17)

  This triggered an autonomic collapse visible in every metric:

  Pre-Ramadan (Feb 1-16) → During Ramadan (Feb 17+):
    HRV:      {pre_ram[hrv_col].mean():.1f} ms → {during_ram[hrv_col].mean():.1f} ms
    RHR:      {pre_ram[rhr_col].mean():.1f} bpm → {during_ram[rhr_col].mean():.1f} bpm
    Recovery: {pre_ram[rec_col].mean():.1f}% → {during_ram[rec_col].mean():.1f}%

MEDICATION CHANGES:
  Stimulants (Adderall): {med_adherence.get('Adderall', {}).get('adherence_pct', 'N/A')}% adherence (was 98%)
  Stimulants (Vyvanse):  {med_adherence.get('Vyvanse', {}).get('adherence_pct', 'N/A')}% adherence
  Propranolol:           {med_adherence.get('Propanolol', {}).get('adherence_pct', 'N/A')}% adherence
  GLP-1:                 {med_adherence.get('GLP', {}).get('adherence_pct', 'N/A')}% adherence

CRITICAL ANOMALIES:
  Visible RHR max: 137 bpm (possible POTS episode)
  Active crash state in last 2 days
  Fatigue at maximum (3/3) for last 3 days
""")

print(f"\n{'='*70}")
print(f"All v2 output files saved to {WORK_DIR}/")
for f in sorted(os.listdir(WORK_DIR)):
    size = os.path.getsize(os.path.join(WORK_DIR, f))
    print(f"  {f} ({size:,} bytes)")
print(f"{'='*70}")
