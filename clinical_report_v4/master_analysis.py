#!/usr/bin/env python3
"""
Master Prompt Executor v4 — Full 5-Step Analysis
Patient: Dr. Mohammed Faraaz Rahman, Age 32
Report Date: 2026-03-15

Executes the exact analysis workflow from Pasted_content_03.txt:
  Step 0: Data Validation
  Step 1: Autonomic Balance (HRV, RHR)
  Step 2: Sleep Architecture & Circadian Rhythm
  Step 3: Recovery & Strain (PEM Signal)
  Step 4: Symptom-Physiology Correlation
  Step 5: Longitudinal Trend Synthesis
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
from scipy import stats
import json, os, glob, warnings
warnings.filterwarnings('ignore')

UPLOAD = "/home/ubuntu/upload"
OUT = "/home/ubuntu/work/v4"
os.makedirs(f"{OUT}/charts", exist_ok=True)

# Historical Baseline from medical_context.md
BASELINE = {
    'HRV_ms': 20.4,
    'RHR_bpm': 84.1,
    'Recovery_pct': 36.0,
    'Red_pct': 49.0,
    'Green_pct': 10.0,
    'Sleep_h': 5.0,
    'Sleep_onset_SD_h': 5.6,
    'Steps': 5406,
    'Fatigue_pct': 75.0,
    'Palpitation_pct': 75.0,
}

# Dark theme
BG_DARK = '#0f172a'
BG_PANEL = '#1e293b'
ACCENT = '#38bdf8'
RED = '#f87171'
YELLOW = '#fbbf24'
GREEN = '#4ade80'
PURPLE = '#c084fc'
ORANGE = '#fb923c'

print("=" * 70)
print("MASTER PROMPT EXECUTOR v4 — FULL 5-STEP ANALYSIS")
print("=" * 70)

# ============================================================
# STEP 0: DATA VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("STEP 0: DATA VALIDATION")
print("=" * 70)

validation_results = {}

# Validate physiological_cycles.csv
try:
    cycles = pd.read_csv(f'{UPLOAD}/physiological_cycles.csv')
    required_cols = ['Cycle start time', 'Recovery score %', 'Heart rate variability (ms)',
                     'Resting heart rate (bpm)', 'Asleep duration (min)']
    missing = [c for c in required_cols if c not in cycles.columns]
    if missing:
        validation_results['physiological_cycles.csv'] = f"MISSING COLUMNS: {missing}"
    else:
        cycles['Cycle start time'] = pd.to_datetime(cycles['Cycle start time'])
        cycles = cycles.dropna(subset=['Recovery score %']).sort_values('Cycle start time').reset_index(drop=True)
        validation_results['physiological_cycles.csv'] = f"OK — {len(cycles)} valid rows, {cycles['Cycle start time'].min().date()} to {cycles['Cycle start time'].max().date()}"
    print(f"  physiological_cycles.csv: {validation_results['physiological_cycles.csv']}")
except Exception as e:
    validation_results['physiological_cycles.csv'] = f"ERROR: {e}"
    print(f"  physiological_cycles.csv: ERROR — {e}")

# Validate sleeps.csv
try:
    sleeps = pd.read_csv(f'{UPLOAD}/sleeps.csv')
    required_cols_sleep = ['Cycle start time', 'Asleep duration (min)', 'Sleep onset']
    missing = [c for c in required_cols_sleep if c not in sleeps.columns]
    if missing:
        validation_results['sleeps.csv'] = f"MISSING COLUMNS: {missing}"
    else:
        sleeps['Sleep onset'] = pd.to_datetime(sleeps['Sleep onset'])
        sleeps['Cycle start time'] = pd.to_datetime(sleeps['Cycle start time'])
        sleeps_main = sleeps[sleeps['Nap'] == False].copy() if 'Nap' in sleeps.columns else sleeps.copy()
        validation_results['sleeps.csv'] = f"OK — {len(sleeps_main)} main sleep records"
    print(f"  sleeps.csv: {validation_results['sleeps.csv']}")
except Exception as e:
    validation_results['sleeps.csv'] = f"ERROR: {e}"
    print(f"  sleeps.csv: ERROR — {e}")

# Validate Visible data
try:
    vis = pd.read_csv(f'{UPLOAD}/Visible_Data_Export_2026-3-15.csv')
    required_cols_vis = ['observation_date', 'tracker_name', 'observation_value']
    missing = [c for c in required_cols_vis if c not in vis.columns]
    if missing:
        validation_results['Visible_Data_Export'] = f"MISSING COLUMNS: {missing}"
    else:
        vis['observation_date'] = pd.to_datetime(vis['observation_date'])
        vis_wide = vis.pivot_table(index='observation_date', columns='tracker_name',
                                   values='observation_value', aggfunc='first').reset_index()
        vis_wide = vis_wide.sort_values('observation_date').reset_index(drop=True)
        trackers = list(vis_wide.columns[1:])
        validation_results['Visible_Data_Export'] = f"OK — {len(vis_wide)} days, trackers: {trackers}"
    print(f"  Visible_Data_Export: {validation_results['Visible_Data_Export']}")
except Exception as e:
    validation_results['Visible_Data_Export'] = f"ERROR: {e}"
    print(f"  Visible_Data_Export: ERROR — {e}")

# Validate ring_data files
ring_files = sorted(glob.glob(f'{UPLOAD}/ring_data_*.csv'))
try:
    if ring_files:
        sample = pd.read_csv(ring_files[0])
        validation_results['ring_data_*.csv'] = f"OK — {len(ring_files)} files, sample cols: {list(sample.columns[:5])}"
    else:
        validation_results['ring_data_*.csv'] = "NO FILES FOUND"
    print(f"  ring_data_*.csv: {validation_results['ring_data_*.csv']}")
except Exception as e:
    validation_results['ring_data_*.csv'] = f"ERROR: {e}"

# Validate workouts.csv
try:
    workouts = pd.read_csv(f'{UPLOAD}/workouts.csv')
    validation_results['workouts.csv'] = f"OK — {len(workouts)} rows"
    print(f"  workouts.csv: {validation_results['workouts.csv']}")
except Exception as e:
    validation_results['workouts.csv'] = f"ERROR: {e}"

with open(f'{OUT}/validation.json', 'w') as f:
    json.dump(validation_results, f, indent=2)

# ============================================================
# STEP 1: AUTONOMIC BALANCE
# ============================================================
print("\n" + "=" * 70)
print("STEP 1: AUTONOMIC BALANCE (HRV & RHR)")
print("=" * 70)

hrv = cycles['Heart rate variability (ms)']
rhr = cycles['Resting heart rate (bpm)']
dates = cycles['Cycle start time']

# Full period stats
hrv_mean = hrv.mean()
hrv_median = hrv.median()
rhr_mean = rhr.mean()
rhr_median = rhr.median()

# 7-day trend (last 7 days)
last7 = cycles[dates >= dates.max() - pd.Timedelta(days=7)]
hrv_7d = last7['Heart rate variability (ms)']
rhr_7d = last7['Resting heart rate (bpm)']

# 7-day trend direction (linear regression)
if len(last7) >= 3:
    x = np.arange(len(last7))
    hrv_slope, _, _, _, _ = stats.linregress(x, hrv_7d.values)
    rhr_slope, _, _, _, _ = stats.linregress(x, rhr_7d.values)
    hrv_trend_dir = "IMPROVING" if hrv_slope > 0.5 else ("DETERIORATING" if hrv_slope < -0.5 else "STABLE")
    rhr_trend_dir = "IMPROVING" if rhr_slope < -0.5 else ("DETERIORATING" if rhr_slope > 0.5 else "STABLE")
else:
    hrv_slope = rhr_slope = 0
    hrv_trend_dir = rhr_trend_dir = "INSUFFICIENT DATA"

# Consecutive crisis streaks: HRV < 15 AND RHR > 90 for 3+ days
crisis_mask = (hrv < 15) & (rhr > 90)
streaks = []
current_streak = 0
streak_start = None
for i, (is_crisis, dt) in enumerate(zip(crisis_mask, dates)):
    if is_crisis:
        if current_streak == 0:
            streak_start = dt
        current_streak += 1
    else:
        if current_streak >= 3:
            streaks.append({
                'start': str(streak_start.date()),
                'end': str(dates.iloc[i-1].date()),
                'days': current_streak
            })
        current_streak = 0
if current_streak >= 3:
    streaks.append({
        'start': str(streak_start.date()),
        'end': str(dates.iloc[-1].date()),
        'days': current_streak
    })

autonomic = {
    'hrv': {
        'mean': round(hrv_mean, 1), 'median': round(hrv_median, 1),
        '7d_mean': round(hrv_7d.mean(), 1), '7d_slope': round(hrv_slope, 2),
        '7d_trend': hrv_trend_dir,
        'baseline': BASELINE['HRV_ms'],
        'delta_pct': round((hrv_mean - BASELINE['HRV_ms']) / BASELINE['HRV_ms'] * 100, 1)
    },
    'rhr': {
        'mean': round(rhr_mean, 1), 'median': round(rhr_median, 1),
        '7d_mean': round(rhr_7d.mean(), 1), '7d_slope': round(rhr_slope, 2),
        '7d_trend': rhr_trend_dir,
        'baseline': BASELINE['RHR_bpm'],
        'delta_pct': round((rhr_mean - BASELINE['RHR_bpm']) / BASELINE['RHR_bpm'] * 100, 1)
    },
    'crisis_streaks': streaks,
    'crisis_days_total': int(crisis_mask.sum()),
    'crisis_pct': round(crisis_mask.sum() / len(crisis_mask) * 100, 1)
}

print(f"  HRV: mean={autonomic['hrv']['mean']}ms, median={autonomic['hrv']['median']}ms, 7d={autonomic['hrv']['7d_mean']}ms ({hrv_trend_dir})")
print(f"  RHR: mean={autonomic['rhr']['mean']}bpm, median={autonomic['rhr']['median']}bpm, 7d={autonomic['rhr']['7d_mean']}bpm ({rhr_trend_dir})")
print(f"  Crisis streaks (HRV<15 & RHR>90): {len(streaks)} streaks, {autonomic['crisis_days_total']} total days ({autonomic['crisis_pct']}%)")
for s in streaks:
    print(f"    {s['start']} → {s['end']} ({s['days']} days)")

# ============================================================
# STEP 2: SLEEP ARCHITECTURE & CIRCADIAN RHYTHM
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: SLEEP ARCHITECTURE & CIRCADIAN RHYTHM")
print("=" * 70)

# Total sleep from cycles
sleep_min = cycles['Asleep duration (min)']
sleep_h = sleep_min / 60

# Deep sleep (SWS), REM, Light
sws_col = 'Deep (SWS) duration (min)'
rem_col = 'REM duration (min)'
light_col = 'Light sleep duration (min)'
eff_col = 'Sleep efficiency %'

sws = cycles[sws_col] if sws_col in cycles.columns else pd.Series([np.nan]*len(cycles))
rem = cycles[rem_col] if rem_col in cycles.columns else pd.Series([np.nan]*len(cycles))
light = cycles[light_col] if light_col in cycles.columns else pd.Series([np.nan]*len(cycles))
eff = cycles[eff_col] if eff_col in cycles.columns else pd.Series([np.nan]*len(cycles))

# Sleep onset SD from sleeps.csv
onset_times = sleeps_main['Sleep onset'].dropna()
onset_hours = onset_times.dt.hour + onset_times.dt.minute / 60
# Handle wrap-around (e.g., 23:00 and 01:00 should be close)
onset_rad = onset_hours * 2 * np.pi / 24
onset_sin = np.sin(onset_rad)
onset_cos = np.cos(onset_rad)
mean_sin = onset_sin.mean()
mean_cos = onset_cos.mean()
mean_angle = np.arctan2(mean_sin, mean_cos)
mean_hour = (mean_angle * 24 / (2 * np.pi)) % 24
# Circular SD
R = np.sqrt(mean_sin**2 + mean_cos**2)
circular_sd_rad = np.sqrt(-2 * np.log(R)) if R > 0 else 0
circular_sd_hours = circular_sd_rad * 24 / (2 * np.pi)

sleep_analysis = {
    'total_sleep_h': {'mean': round(sleep_h.mean(), 2), 'median': round(sleep_h.median(), 2),
                      'baseline': BASELINE['Sleep_h'],
                      'delta_pct': round((sleep_h.mean() - BASELINE['Sleep_h']) / BASELINE['Sleep_h'] * 100, 1)},
    'deep_sleep_min': {'mean': round(sws.mean(), 1), 'median': round(sws.median(), 1)},
    'rem_sleep_min': {'mean': round(rem.mean(), 1), 'median': round(rem.median(), 1)},
    'light_sleep_min': {'mean': round(light.mean(), 1), 'median': round(light.median(), 1)},
    'sleep_efficiency': {'mean': round(eff.mean(), 1), 'median': round(eff.median(), 1)},
    'sleep_onset_mean_hour': round(mean_hour, 1),
    'sleep_onset_SD_hours': round(circular_sd_hours, 2),
    'baseline_onset_SD': BASELINE['Sleep_onset_SD_h'],
    'nights_below_4h': int((sleep_h < 4).sum()),
    'nights_below_4h_pct': round((sleep_h < 4).sum() / len(sleep_h) * 100, 1),
    'nights_above_7h': int((sleep_h >= 7).sum()),
    'nights_above_7h_pct': round((sleep_h >= 7).sum() / len(sleep_h) * 100, 1),
}

print(f"  Total Sleep: mean={sleep_analysis['total_sleep_h']['mean']}h, median={sleep_analysis['total_sleep_h']['median']}h (baseline: {BASELINE['Sleep_h']}h)")
print(f"  Deep Sleep: mean={sleep_analysis['deep_sleep_min']['mean']}min")
print(f"  REM Sleep: mean={sleep_analysis['rem_sleep_min']['mean']}min")
print(f"  Sleep Efficiency: mean={sleep_analysis['sleep_efficiency']['mean']}%")
print(f"  Sleep Onset Mean: {sleep_analysis['sleep_onset_mean_hour']:.1f}h (24h clock)")
print(f"  Sleep Onset SD: {sleep_analysis['sleep_onset_SD_hours']}h (baseline: {BASELINE['Sleep_onset_SD_h']}h)")
print(f"  Nights <4h: {sleep_analysis['nights_below_4h']} ({sleep_analysis['nights_below_4h_pct']}%)")
print(f"  Nights ≥7h: {sleep_analysis['nights_above_7h']} ({sleep_analysis['nights_above_7h_pct']}%)")

# ============================================================
# STEP 3: RECOVERY & STRAIN (PEM SIGNAL)
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: RECOVERY & STRAIN (POST-EXERTIONAL MALAISE SIGNAL)")
print("=" * 70)

recovery = cycles['Recovery score %']
strain_col = 'Day Strain'
strain = cycles[strain_col] if strain_col in cycles.columns else pd.Series([np.nan]*len(cycles))

# Next-day recovery correlation
if strain.notna().sum() > 10:
    strain_shifted = strain.iloc[:-1].reset_index(drop=True)
    recovery_next = recovery.iloc[1:].reset_index(drop=True)
    valid = strain_shifted.notna() & recovery_next.notna()
    if valid.sum() > 10:
        corr, p_val = stats.pearsonr(strain_shifted[valid], recovery_next[valid])
    else:
        corr, p_val = np.nan, np.nan
else:
    corr, p_val = np.nan, np.nan

# Mean strain on days preceding Red recovery (<33%)
red_days = recovery < 33
red_indices = red_days[red_days].index
preceding_strain = []
for idx in red_indices:
    if idx > 0 and pd.notna(strain.iloc[idx - 1]):
        preceding_strain.append(strain.iloc[idx - 1])

# Recovery distribution
green_pct = round((recovery >= 67).sum() / len(recovery) * 100, 1)
yellow_pct = round(((recovery >= 33) & (recovery < 67)).sum() / len(recovery) * 100, 1)
red_pct = round((recovery < 33).sum() / len(recovery) * 100, 1)

# Consecutive red days
consec_red = 0
max_consec_red = 0
for v in recovery:
    if v < 33:
        consec_red += 1
        max_consec_red = max(max_consec_red, consec_red)
    else:
        consec_red = 0

pem_analysis = {
    'recovery': {
        'mean': round(recovery.mean(), 1), 'median': round(recovery.median(), 1),
        'baseline': BASELINE['Recovery_pct'],
        'delta_pct': round((recovery.mean() - BASELINE['Recovery_pct']) / BASELINE['Recovery_pct'] * 100, 1),
        'green_pct': green_pct, 'yellow_pct': yellow_pct, 'red_pct': red_pct,
    },
    'strain_recovery_correlation': {
        'pearson_r': round(corr, 3) if not np.isnan(corr) else 'N/A',
        'p_value': round(p_val, 4) if not np.isnan(p_val) else 'N/A',
        'interpretation': 'Significant' if (not np.isnan(p_val) and p_val < 0.05) else 'Not significant'
    },
    'mean_strain_before_red': round(np.mean(preceding_strain), 1) if preceding_strain else 'N/A',
    'mean_strain_overall': round(strain.mean(), 1) if strain.notna().sum() > 0 else 'N/A',
    'max_consecutive_red_days': max_consec_red,
}

print(f"  Recovery: mean={pem_analysis['recovery']['mean']}%, Green={green_pct}%, Yellow={yellow_pct}%, Red={red_pct}%")
print(f"  Baseline: Recovery={BASELINE['Recovery_pct']}%, Red={BASELINE['Red_pct']}%, Green={BASELINE['Green_pct']}%")
print(f"  Strain→Next-day Recovery correlation: r={pem_analysis['strain_recovery_correlation']['pearson_r']}, p={pem_analysis['strain_recovery_correlation']['p_value']}")
print(f"  Mean strain before Red days: {pem_analysis['mean_strain_before_red']}")
print(f"  Mean strain overall: {pem_analysis['mean_strain_overall']}")
print(f"  Max consecutive Red days: {max_consec_red}")

# ============================================================
# STEP 4: SYMPTOM-PHYSIOLOGY CORRELATION
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: SYMPTOM-PHYSIOLOGY CORRELATION")
print("=" * 70)

# Merge Visible with WHOOP by date
cycles['date'] = cycles['Cycle start time'].dt.date
vis_wide['date'] = vis_wide['observation_date'].dt.date

merged = pd.merge(
    cycles[['date', 'Heart rate variability (ms)', 'Resting heart rate (bpm)',
            'Recovery score %', 'Asleep duration (min)', 'Day Strain']],
    vis_wide,
    on='date', how='inner'
)

# Convert Visible columns to numeric
symptom_cols = [c for c in vis_wide.columns if c not in ['observation_date', 'date']]
for col in symptom_cols:
    if col in merged.columns:
        merged[col] = pd.to_numeric(merged[col], errors='coerce')

# Compute correlations between physiology and symptoms
physio_cols = ['Heart rate variability (ms)', 'Resting heart rate (bpm)',
               'Recovery score %', 'Asleep duration (min)']
correlations = {}
for symptom in symptom_cols:
    if symptom in merged.columns and merged[symptom].notna().sum() > 5:
        for physio in physio_cols:
            if physio in merged.columns and merged[physio].notna().sum() > 5:
                valid = merged[[symptom, physio]].dropna()
                if len(valid) > 5:
                    r, p = stats.pearsonr(valid[symptom], valid[physio])
                    key = f"{symptom} ↔ {physio}"
                    correlations[key] = {'r': round(r, 3), 'p': round(p, 4), 'n': len(valid)}

# Sort by absolute correlation
sorted_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]['r']), reverse=True)
top_predictors = sorted_corrs[:10]

print(f"  Merged dataset: {len(merged)} overlapping days")
print(f"  Top symptom-physiology correlations:")
for name, vals in top_predictors:
    sig = "*" if vals['p'] < 0.05 else ""
    print(f"    {name}: r={vals['r']}{sig} (n={vals['n']})")

# ============================================================
# STEP 5: LONGITUDINAL TREND SYNTHESIS
# ============================================================
print("\n" + "=" * 70)
print("STEP 5: LONGITUDINAL TREND SYNTHESIS")
print("=" * 70)

# Monthly trends
cycles['month'] = cycles['Cycle start time'].dt.to_period('M')
monthly = cycles.groupby('month').agg({
    'Heart rate variability (ms)': 'mean',
    'Resting heart rate (bpm)': 'mean',
    'Recovery score %': 'mean',
    'Asleep duration (min)': 'mean',
}).reset_index()
monthly.columns = ['Month', 'HRV_ms', 'RHR_bpm', 'Recovery_pct', 'Sleep_min']
monthly['Sleep_h'] = monthly['Sleep_min'] / 60

# Trend classification
def classify_trend(current_mean, baseline, metric_name):
    delta_pct = (current_mean - baseline) / baseline * 100
    # For HRV and Recovery: higher is better
    # For RHR: lower is better
    if metric_name in ['RHR']:
        if delta_pct < -5: return 'IMPROVING'
        elif delta_pct > 5: return 'DETERIORATING'
        else: return 'STABLE'
    else:
        if delta_pct > 5: return 'IMPROVING'
        elif delta_pct < -5: return 'DETERIORATING'
        else: return 'STABLE'

# Recent 30-day period
recent_30d = cycles[cycles['Cycle start time'] >= cycles['Cycle start time'].max() - pd.Timedelta(days=30)]
r30_hrv = recent_30d['Heart rate variability (ms)'].mean()
r30_rhr = recent_30d['Resting heart rate (bpm)'].mean()
r30_rec = recent_30d['Recovery score %'].mean()
r30_sleep = recent_30d['Asleep duration (min)'].mean() / 60

trends = {
    'HRV': {
        'current_period_mean': round(r30_hrv, 1),
        'full_period_mean': round(hrv_mean, 1),
        'baseline': BASELINE['HRV_ms'],
        'delta_vs_baseline': round(r30_hrv - BASELINE['HRV_ms'], 1),
        'delta_pct': round((r30_hrv - BASELINE['HRV_ms']) / BASELINE['HRV_ms'] * 100, 1),
        'trend': classify_trend(r30_hrv, BASELINE['HRV_ms'], 'HRV')
    },
    'RHR': {
        'current_period_mean': round(r30_rhr, 1),
        'full_period_mean': round(rhr_mean, 1),
        'baseline': BASELINE['RHR_bpm'],
        'delta_vs_baseline': round(r30_rhr - BASELINE['RHR_bpm'], 1),
        'delta_pct': round((r30_rhr - BASELINE['RHR_bpm']) / BASELINE['RHR_bpm'] * 100, 1),
        'trend': classify_trend(r30_rhr, BASELINE['RHR_bpm'], 'RHR')
    },
    'Sleep': {
        'current_period_mean': round(r30_sleep, 2),
        'full_period_mean': round(sleep_h.mean(), 2),
        'baseline': BASELINE['Sleep_h'],
        'delta_vs_baseline': round(r30_sleep - BASELINE['Sleep_h'], 2),
        'delta_pct': round((r30_sleep - BASELINE['Sleep_h']) / BASELINE['Sleep_h'] * 100, 1),
        'trend': classify_trend(r30_sleep, BASELINE['Sleep_h'], 'Sleep')
    },
    'Recovery': {
        'current_period_mean': round(r30_rec, 1),
        'full_period_mean': round(recovery.mean(), 1),
        'baseline': BASELINE['Recovery_pct'],
        'delta_vs_baseline': round(r30_rec - BASELINE['Recovery_pct'], 1),
        'delta_pct': round((r30_rec - BASELINE['Recovery_pct']) / BASELINE['Recovery_pct'] * 100, 1),
        'trend': classify_trend(r30_rec, BASELINE['Recovery_pct'], 'Recovery')
    },
}

for metric, data in trends.items():
    print(f"  {metric}: current 30d={data['current_period_mean']}, baseline={data['baseline']}, Δ={data['delta_vs_baseline']} ({data['delta_pct']}%) → {data['trend']}")

# ============================================================
# RED FLAGS
# ============================================================
print("\n" + "=" * 70)
print("RED FLAGS")
print("=" * 70)

red_flags = []

# HRV < 10ms events
hrv_critical = cycles[hrv < 10]
if len(hrv_critical) > 0:
    red_flags.append(f"HRV < 10ms on {len(hrv_critical)} days — severe autonomic suppression")
    print(f"  🔴 HRV < 10ms: {len(hrv_critical)} days")

# RHR > 100 events
rhr_critical = cycles[rhr > 100]
if len(rhr_critical) > 0:
    red_flags.append(f"RHR > 100 bpm on {len(rhr_critical)} days — persistent tachycardia")
    print(f"  🔴 RHR > 100: {len(rhr_critical)} days")

# Visible RHR > 120 (POTS episodes)
if 'Resting HR' in vis_wide.columns:
    vis_rhr = pd.to_numeric(vis_wide['Resting HR'], errors='coerce')
    pots_episodes = vis_wide[vis_rhr > 120]
    if len(pots_episodes) > 0:
        red_flags.append(f"Visible RHR > 120 bpm on {len(pots_episodes)} days — possible POTS episodes")
        for _, ep in pots_episodes.iterrows():
            print(f"  🔴 POTS episode: {ep['observation_date'].date()} — Visible RHR = {ep['Resting HR']} bpm")

# SpO2 < 93%
spo2_col = 'Blood oxygen %'
if spo2_col in cycles.columns:
    spo2_critical = cycles[cycles[spo2_col] < 93]
    if len(spo2_critical) > 0:
        red_flags.append(f"SpO₂ < 93% on {len(spo2_critical)} days — hypoxemia")
        print(f"  🔴 SpO₂ < 93%: {len(spo2_critical)} days")

# Sleep < 2h
sleep_critical = cycles[sleep_h < 2]
if len(sleep_critical) > 0:
    red_flags.append(f"Sleep < 2 hours on {len(sleep_critical)} days — severe sleep deprivation")
    print(f"  🔴 Sleep < 2h: {len(sleep_critical)} days")

# Consecutive Red days > 5
if max_consec_red > 5:
    red_flags.append(f"Maximum {max_consec_red} consecutive Red recovery days — sustained PEM")
    print(f"  🔴 Max consecutive Red days: {max_consec_red}")

# Crisis streaks
if len(streaks) > 0:
    total_crisis = sum(s['days'] for s in streaks)
    red_flags.append(f"{len(streaks)} crisis streaks (HRV<15 & RHR>90) totaling {total_crisis} days")
    print(f"  🔴 Crisis streaks: {len(streaks)} streaks, {total_crisis} total days")

if not red_flags:
    print("  No red flags detected.")

# ============================================================
# SAVE ALL ANALYSIS DATA
# ============================================================
all_analysis = {
    'validation': validation_results,
    'autonomic': autonomic,
    'sleep': sleep_analysis,
    'pem': pem_analysis,
    'correlations': {k: v for k, v in top_predictors},
    'trends': trends,
    'red_flags': red_flags,
    'monthly': monthly.to_dict(orient='records'),
}

# Convert Period objects to strings for JSON serialization
for m in all_analysis['monthly']:
    m['Month'] = str(m['Month'])

with open(f'{OUT}/analysis_results.json', 'w') as f:
    json.dump(all_analysis, f, indent=2, default=str)

# ============================================================
# GENERATE VISUALIZATIONS
# ============================================================
print("\n" + "=" * 70)
print("GENERATING VISUALIZATIONS")
print("=" * 70)

# --- CHART 1: Autonomic Balance (HRV + RHR dual-axis) ---
fig, ax1 = plt.subplots(figsize=(16, 6), facecolor=BG_DARK)
ax1.set_facecolor(BG_PANEL)

ax1.fill_between(dates, hrv, alpha=0.3, color=ACCENT)
ax1.plot(dates, hrv, color=ACCENT, lw=1.2, label='HRV (ms)')
ax1.axhline(BASELINE['HRV_ms'], color=ACCENT, lw=1, ls='--', alpha=0.5, label=f'HRV Baseline ({BASELINE["HRV_ms"]}ms)')
ax1.set_ylabel('HRV (ms)', color=ACCENT, fontsize=11)
ax1.tick_params(axis='y', labelcolor=ACCENT)

ax2 = ax1.twinx()
ax2.plot(dates, rhr, color=RED, lw=1.2, alpha=0.7, label='RHR (bpm)')
ax2.axhline(BASELINE['RHR_bpm'], color=RED, lw=1, ls='--', alpha=0.5, label=f'RHR Baseline ({BASELINE["RHR_bpm"]}bpm)')
ax2.set_ylabel('RHR (bpm)', color=RED, fontsize=11)
ax2.tick_params(axis='y', labelcolor=RED)

# Mark crisis streaks
for s in streaks:
    ax1.axvspan(pd.Timestamp(s['start']), pd.Timestamp(s['end']),
                alpha=0.15, color=RED, label='Crisis streak' if s == streaks[0] else '')

ax1.set_title('AUTONOMIC BALANCE — HRV & RHR Time Series', color='white', fontsize=13, fontweight='bold')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax1.tick_params(axis='x', colors='white', labelsize=8, rotation=45)
for spine in ax1.spines.values():
    spine.set_color('#334155')
for spine in ax2.spines.values():
    spine.set_color('#334155')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, facecolor=BG_PANEL, labelcolor='white', loc='upper left')

plt.tight_layout()
plt.savefig(f'{OUT}/charts/01_autonomic_balance.png', dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()
print("  Chart 1: Autonomic Balance saved")

# --- CHART 2: Sleep Architecture ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor=BG_DARK)

# Top: Sleep duration with architecture
ax1.set_facecolor(BG_PANEL)
sws_vals = sws.fillna(0)
rem_vals = rem.fillna(0)
light_vals = light.fillna(0)

ax1.bar(dates, sws_vals, label='Deep (SWS)', color='#818cf8', alpha=0.9, width=1.5)
ax1.bar(dates, rem_vals, bottom=sws_vals, label='REM', color=PURPLE, alpha=0.9, width=1.5)
ax1.bar(dates, light_vals, bottom=sws_vals + rem_vals, label='Light', color='#475569', alpha=0.7, width=1.5)
ax1.axhline(420, color=GREEN, lw=1.5, ls='--', label='7h target')
ax1.axhline(BASELINE['Sleep_h'] * 60, color=YELLOW, lw=1, ls=':', label=f'Baseline ({BASELINE["Sleep_h"]}h)')
ax1.set_ylabel('Sleep (min)', color='white', fontsize=11)
ax1.set_title('SLEEP ARCHITECTURE — Full Timeline', color='white', fontsize=13, fontweight='bold')
ax1.legend(fontsize=8, facecolor=BG_PANEL, labelcolor='white')
ax1.tick_params(colors='white', labelsize=8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
for spine in ax1.spines.values():
    spine.set_color('#334155')

# Bottom: Sleep onset chaos
ax2.set_facecolor(BG_PANEL)
onset_dates = sleeps_main['Sleep onset'].dropna()
onset_hour_vals = onset_dates.dt.hour + onset_dates.dt.minute / 60
# Adjust for display (shift so midnight = 24)
onset_display = onset_hour_vals.copy()
onset_display[onset_display < 12] += 24  # Show early morning as 24-36

ax2.scatter(sleeps_main.loc[onset_dates.index, 'Cycle start time'],
            onset_display, s=15, alpha=0.6, color=ORANGE)
ax2.axhline(mean_hour if mean_hour > 12 else mean_hour + 24, color=ACCENT, lw=2, ls='--',
            label=f'Mean onset: {int(mean_hour)}:{int((mean_hour % 1) * 60):02d}')
ax2.set_ylabel('Sleep Onset (hour)', color='white', fontsize=11)
ax2.set_title(f'CIRCADIAN CHAOS — Sleep Onset SD = {circular_sd_hours:.1f}h (Baseline: {BASELINE["Sleep_onset_SD_h"]}h)',
              color='white', fontsize=13, fontweight='bold')
ax2.set_yticks([18, 20, 22, 24, 26, 28, 30, 32, 34])
ax2.set_yticklabels(['6PM', '8PM', '10PM', '12AM', '2AM', '4AM', '6AM', '8AM', '10AM'])
ax2.legend(fontsize=8, facecolor=BG_PANEL, labelcolor='white')
ax2.tick_params(colors='white', labelsize=8)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
for spine in ax2.spines.values():
    spine.set_color('#334155')

plt.tight_layout()
plt.savefig(f'{OUT}/charts/02_sleep_architecture.png', dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()
print("  Chart 2: Sleep Architecture saved")

# --- CHART 3: Recovery & Strain (PEM) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor=BG_DARK)

# Top: Recovery colored by zone
ax1.set_facecolor(BG_PANEL)
rec_colors = [GREEN if v >= 67 else (YELLOW if v >= 33 else RED) for v in recovery]
ax1.bar(dates, recovery, color=rec_colors, width=1.5, alpha=0.85)
ax1.axhline(67, color=GREEN, lw=1, ls='--', alpha=0.7)
ax1.axhline(33, color=RED, lw=1, ls='--', alpha=0.7)
ax1.axhline(BASELINE['Recovery_pct'], color=ACCENT, lw=1.5, ls=':', label=f'Baseline ({BASELINE["Recovery_pct"]}%)')
ax1.set_ylabel('Recovery %', color='white', fontsize=11)
ax1.set_title(f'RECOVERY DISTRIBUTION — Green {green_pct}% | Yellow {yellow_pct}% | Red {red_pct}% (Baseline Red: {BASELINE["Red_pct"]}%)',
              color='white', fontsize=13, fontweight='bold')
ax1.legend(fontsize=8, facecolor=BG_PANEL, labelcolor='white')
ax1.tick_params(colors='white', labelsize=8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
for spine in ax1.spines.values():
    spine.set_color('#334155')

# Bottom: Strain vs next-day recovery scatter
ax2.set_facecolor(BG_PANEL)
if strain.notna().sum() > 10:
    valid_mask = strain_shifted.notna() & recovery_next.notna()
    s_vals = strain_shifted[valid_mask]
    r_vals = recovery_next[valid_mask]
    colors_scatter = [GREEN if v >= 67 else (YELLOW if v >= 33 else RED) for v in r_vals]
    ax2.scatter(s_vals, r_vals, c=colors_scatter, s=20, alpha=0.6)
    # Regression line
    z = np.polyfit(s_vals, r_vals, 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(s_vals.min(), s_vals.max(), 100)
    ax2.plot(x_range, p_line(x_range), color=ACCENT, lw=2, ls='--',
             label=f'r={corr:.3f}, p={p_val:.4f}')
ax2.set_xlabel('Day Strain (previous day)', color='white', fontsize=11)
ax2.set_ylabel('Next-Day Recovery %', color='white', fontsize=11)
ax2.set_title('PEM SIGNAL — Day Strain vs. Next-Day Recovery', color='white', fontsize=13, fontweight='bold')
ax2.legend(fontsize=8, facecolor=BG_PANEL, labelcolor='white')
ax2.tick_params(colors='white', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#334155')

plt.tight_layout()
plt.savefig(f'{OUT}/charts/03_recovery_pem.png', dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()
print("  Chart 3: Recovery & PEM saved")

# --- CHART 4: Longitudinal Trends (Monthly) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=BG_DARK)

metrics = [
    ('HRV_ms', 'HRV (ms)', ACCENT, BASELINE['HRV_ms']),
    ('RHR_bpm', 'RHR (bpm)', RED, BASELINE['RHR_bpm']),
    ('Recovery_pct', 'Recovery (%)', GREEN, BASELINE['Recovery_pct']),
    ('Sleep_h', 'Sleep (hours)', PURPLE, BASELINE['Sleep_h']),
]

month_dates = [pd.Timestamp(str(m)) for m in monthly['Month']]

for ax, (col, label, color, baseline) in zip(axes.flat, metrics):
    ax.set_facecolor(BG_PANEL)
    vals = monthly[col]
    ax.bar(month_dates, vals, color=color, alpha=0.8, width=20)
    ax.axhline(baseline, color=YELLOW, lw=1.5, ls='--', label=f'Baseline: {baseline}')
    ax.set_title(f'{label} — Monthly Trend', color='white', fontsize=11, fontweight='bold')
    ax.set_ylabel(label, color='white', fontsize=10)
    ax.legend(fontsize=7, facecolor=BG_PANEL, labelcolor='white')
    ax.tick_params(colors='white', labelsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    for spine in ax.spines.values():
        spine.set_color('#334155')

fig.suptitle('LONGITUDINAL TRENDS — Monthly Averages vs. Baseline', color='white', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(f'{OUT}/charts/04_longitudinal_trends.png', dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()
print("  Chart 4: Longitudinal Trends saved")

# --- CHART 5: Symptom-Physiology Heatmap ---
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_DARK)
ax.set_facecolor(BG_PANEL)

# Build correlation matrix
corr_matrix_data = {}
for symptom in symptom_cols:
    if symptom in merged.columns:
        row = {}
        for physio in physio_cols:
            if physio in merged.columns:
                valid = merged[[symptom, physio]].dropna()
                if len(valid) > 5:
                    r, _ = stats.pearsonr(valid[symptom], valid[physio])
                    row[physio] = round(r, 2)
                else:
                    row[physio] = np.nan
        if any(not np.isnan(v) for v in row.values()):
            corr_matrix_data[symptom] = row

if corr_matrix_data:
    corr_df = pd.DataFrame(corr_matrix_data).T
    # Rename columns for readability
    col_rename = {
        'Heart rate variability (ms)': 'HRV',
        'Resting heart rate (bpm)': 'RHR',
        'Recovery score %': 'Recovery',
        'Asleep duration (min)': 'Sleep'
    }
    corr_df = corr_df.rename(columns=col_rename)
    
    im = ax.imshow(corr_df.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    ax.set_xticks(range(len(corr_df.columns)))
    ax.set_xticklabels(corr_df.columns, color='white', fontsize=9)
    ax.set_yticks(range(len(corr_df.index)))
    ax.set_yticklabels(corr_df.index, color='white', fontsize=9)
    
    # Add text annotations
    for i in range(len(corr_df.index)):
        for j in range(len(corr_df.columns)):
            val = corr_df.iloc[i, j]
            if not np.isnan(val):
                color = 'white' if abs(val) > 0.3 else 'gray'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=9)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Pearson r', color='white')

ax.set_title('SYMPTOM-PHYSIOLOGY CORRELATION MATRIX', color='white', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUT}/charts/05_symptom_correlation.png', dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()
print("  Chart 5: Symptom Correlation saved")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*70}")
print("ALL v4 OUTPUT FILES:")
for f in sorted(os.listdir(OUT)):
    fpath = os.path.join(OUT, f)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath)
        print(f"  {f} ({size:,} bytes)")
for f in sorted(os.listdir(f'{OUT}/charts')):
    fpath = os.path.join(OUT, 'charts', f)
    size = os.path.getsize(fpath)
    print(f"  charts/{f} ({size:,} bytes)")
print(f"{'='*70}")
