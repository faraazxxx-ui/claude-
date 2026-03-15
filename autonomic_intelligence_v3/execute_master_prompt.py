#!/usr/bin/env python3
"""
AUTONOMIC INTELLIGENCE REPORT — Master Prompt Executor v3
Patient: Mohammed Faraaz Rahman MD, Age 32
Report Date: 2026-03-15
Version: 3.0

Computes:
1. Loop Scores (5-node: AN, SN, IN, PN, DN)
2. 3-Tier Alert System (CRITICAL, WATCH, POSITIVE)
3. 6-Panel Dark-Themed Dashboard
4. All 9 report sections data
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import json, os, glob, warnings
warnings.filterwarnings('ignore')

# ============================================================
# SETUP
# ============================================================
UPLOAD = "/home/ubuntu/upload"
OUT = "/home/ubuntu/work/v3"
os.makedirs(OUT, exist_ok=True)

# Baseline values (Q2 2024 – Q2 2025, n=166 days)
BASELINE = {
    'HRV': 20.4, 'RHR': 84.1, 'Recovery': 36.0,
    'Sleep_min': 300, 'Sleep_h': 5.0, 'Steps': 5406,
    'Hydration_adequate_pct': 9
}

print("=" * 70)
print("AUTONOMIC INTELLIGENCE REPORT — MASTER PROMPT EXECUTOR v3")
print("=" * 70)

# ============================================================
# 1. LOAD DATA (exact schemas from master prompt)
# ============================================================
print("\n[1] Loading data files...")

# FILE 1: physiological_cycles.csv
cycles = pd.read_csv(f'{UPLOAD}/physiological_cycles.csv',
                     parse_dates=['Cycle start time', 'Cycle end time',
                                  'Sleep onset', 'Wake onset'])
cycles_valid = cycles.dropna(subset=['Recovery score %']).copy()
cycles_valid = cycles_valid.sort_values('Cycle start time').reset_index(drop=True)
cycles_valid['date'] = cycles_valid['Cycle start time'].dt.date
print(f"  physiological_cycles.csv: {len(cycles)} rows ({len(cycles_valid)} valid)")

# FILE 2: Visible_Data_Export
vis = pd.read_csv(f'{UPLOAD}/Visible_Data_Export_2026-3-15.csv',
                  parse_dates=['observation_date'])
vis_wide = vis.pivot_table(index='observation_date', columns='tracker_name',
                           values='observation_value', aggfunc='first').reset_index()
vis_wide = vis_wide.sort_values('observation_date').reset_index(drop=True)
print(f"  Visible_Data_Export: {len(vis)} rows → {len(vis_wide)} days wide")

# FILE 3: sleeps.csv
sleeps = pd.read_csv(f'{UPLOAD}/sleeps.csv',
                     parse_dates=['Cycle start time', 'Sleep onset', 'Wake onset'])
sleeps_main = sleeps[sleeps['Nap'] == False].copy() if 'Nap' in sleeps.columns else sleeps.copy()
print(f"  sleeps.csv: {len(sleeps)} rows ({len(sleeps_main)} main sleep)")

# FILE 4: ring_data files
ring_files = glob.glob(f'{UPLOAD}/ring_data_*.csv')
if ring_files:
    ring = pd.concat([pd.read_csv(f) for f in ring_files], ignore_index=True)
    ring['datetime'] = pd.to_datetime(ring['timestamp_epoch'], unit='s')
    print(f"  ring_data files: {len(ring_files)} files, {len(ring)} rows")
else:
    ring = pd.DataFrame()
    print("  ring_data files: none found")

# ============================================================
# 2. COMPUTE LOOP SCORES
# ============================================================
print("\n[2] Computing Loop Scores...")

def compute_an(hrv, rhr):
    """Autonomic Node: 0-3"""
    hrv_score = 3 if hrv < 15 else (2 if hrv < 30 else (1 if hrv <= 50 else 0))
    rhr_score = 1 if rhr > 100 else (0.5 if rhr > 85 else 0)
    return min(3, hrv_score + rhr_score)

def compute_sn(dur_min, eff, con):
    """Sleep Node: 0-3"""
    if dur_min < 180 or eff < 50:
        return 3
    elif dur_min < 300 or eff < 70:
        return 2
    elif dur_min < 420 or eff < 85 or con < 50:
        return 1
    return 0

def compute_in(crash_val, fatigue_val, infection_val):
    """Inflammatory/PEM Node: 0-3"""
    return min(3, crash_val + round(fatigue_val / 3, 1) + infection_val)

def compute_pn(prop_taken, stim_taken):
    """Pharmacologic Node: 0-3"""
    return min(3, (1 - prop_taken) * 2 + stim_taken * 1)

def compute_dn(pacepoints):
    """Deconditioning Node: 0-3"""
    if pacepoints < 5:
        return 3
    elif pacepoints < 20:
        return 2
    elif pacepoints < 35:
        return 1
    return 0

def compute_loop_score(an, sn, in_node, pn, dn):
    """Loop Score: (AN+SN+IN+PN+DN)/15 * 10"""
    return (an + sn + in_node + pn + dn) / 15 * 10

def interpret_ls(ls):
    if ls <= 3: return "Stable"
    elif ls <= 5: return "Monitoring"
    elif ls <= 7: return "Warning"
    else: return "Critical"

# Get latest data for TODAY (2026-03-15)
today = pd.Timestamp('2026-03-15')

# Latest cycle data
latest_cycle = cycles_valid[cycles_valid['Cycle start time'].dt.date <= today.date()].iloc[-1]
latest_hrv = latest_cycle['Heart rate variability (ms)']
latest_rhr = latest_cycle['Resting heart rate (bpm)']
latest_recovery = latest_cycle['Recovery score %']
latest_sleep_min = latest_cycle['Asleep duration (min)']
latest_sleep_eff = latest_cycle['Sleep efficiency %']
latest_sleep_con = latest_cycle['Sleep consistency %'] if pd.notna(latest_cycle.get('Sleep consistency %')) else 50

# Latest Visible data
latest_vis = vis_wide[vis_wide['observation_date'] <= today].iloc[-1]
latest_vis_date = latest_vis['observation_date']

# Safe extraction of Visible values
def safe_get(row, col, default=0):
    val = row.get(col, default)
    return float(val) if pd.notna(val) else default

crash_val = safe_get(latest_vis, 'Crash', 0)
fatigue_val = safe_get(latest_vis, 'Fatigue', 0)
infection_val = safe_get(latest_vis, 'Infection', 0)
prop_taken = safe_get(latest_vis, 'Propanolol', 0)  # CSV spelling
stim_adderall = safe_get(latest_vis, 'Adderall', 0)
stim_vyvanse = safe_get(latest_vis, 'Vyvanse', 0)
stim_taken = max(stim_adderall, stim_vyvanse)
pacepoints = safe_get(latest_vis, 'PacePoints', 0)
vis_rhr = safe_get(latest_vis, 'Resting HR', 0)
vis_hrv = safe_get(latest_vis, 'HRV', 0)
stability = safe_get(latest_vis, 'Stability Score', 0)
sleep_vis = safe_get(latest_vis, 'Sleep', 0)

# Compute nodes
AN = compute_an(latest_hrv, latest_rhr)
SN = compute_sn(latest_sleep_min, latest_sleep_eff, latest_sleep_con)
IN = compute_in(crash_val, fatigue_val, infection_val)
PN = compute_pn(prop_taken, stim_taken)
DN = compute_dn(pacepoints)
LS = compute_loop_score(AN, SN, IN, PN, DN)
LS_interp = interpret_ls(LS)

print(f"  AN = {AN:.1f} (HRV {latest_hrv}ms, RHR {latest_rhr}bpm)")
print(f"  SN = {SN:.1f} (Sleep {latest_sleep_min}min, Eff {latest_sleep_eff}%, Con {latest_sleep_con}%)")
print(f"  IN = {IN:.1f} (Crash {crash_val}, Fatigue {fatigue_val}, Infection {infection_val})")
print(f"  PN = {PN:.1f} (Propranolol {prop_taken}, Stimulant {stim_taken})")
print(f"  DN = {DN:.1f} (PacePoints {pacepoints})")
print(f"  LS = {LS:.2f} / 10 → {LS_interp}")

# Compute daily Loop Scores for the full timeline
print("\n  Computing daily Loop Scores for timeline...")
daily_ls = []
for _, row in cycles_valid.iterrows():
    d = row['Cycle start time'].date()
    hrv = row['Heart rate variability (ms)']
    rhr = row['Resting heart rate (bpm)']
    sleep_min = row['Asleep duration (min)']
    sleep_eff = row['Sleep efficiency %'] if pd.notna(row.get('Sleep efficiency %')) else 70
    sleep_con = row.get('Sleep consistency %', 50)
    sleep_con = sleep_con if pd.notna(sleep_con) else 50
    
    an = compute_an(hrv, rhr)
    sn = compute_sn(sleep_min, sleep_eff, sleep_con)
    
    # Try to get Visible data for this date
    vis_day = vis_wide[vis_wide['observation_date'].dt.date == d]
    if len(vis_day) > 0:
        vr = vis_day.iloc[0]
        cr = safe_get(vr, 'Crash', 0)
        ft = safe_get(vr, 'Fatigue', 0)
        inf = safe_get(vr, 'Infection', 0)
        pr = safe_get(vr, 'Propanolol', 0)
        st = max(safe_get(vr, 'Adderall', 0), safe_get(vr, 'Vyvanse', 0))
        pp = safe_get(vr, 'PacePoints', 0)
    else:
        cr, ft, inf, pr, st, pp = 0, 0, 0, 0, 0, 15  # defaults
    
    in_n = compute_in(cr, ft, inf)
    pn_n = compute_pn(pr, st)
    dn_n = compute_dn(pp)
    ls = compute_loop_score(an, sn, in_n, pn_n, dn_n)
    
    daily_ls.append({
        'date': d, 'AN': an, 'SN': sn, 'IN': in_n, 'PN': pn_n, 'DN': dn_n,
        'LS': ls, 'interpretation': interpret_ls(ls)
    })

ls_df = pd.DataFrame(daily_ls)
ls_df['date'] = pd.to_datetime(ls_df['date'])
ls_df.to_csv(f'{OUT}/loop_scores.csv', index=False)
print(f"  Saved {len(ls_df)} daily Loop Scores")

# ============================================================
# 3. ALERT SYSTEM
# ============================================================
print("\n[3] Running 3-Tier Alert System...")

alerts = {'critical': [], 'watch': [], 'positive': []}

# CRITICAL alerts
if vis_rhr > 105:
    alerts['critical'].append(f"Cardiac decompensation: Visible Resting HR = {vis_rhr} bpm. Take propranolol, rest horizontal.")
if latest_recovery < 10 and crash_val >= 1:
    alerts['critical'].append(f"PEM cascade: Recovery = {latest_recovery}% AND Crash active. No exertion, horizontal rest protocol.")

# Check SpO2
spo2_col = 'Blood oxygen %'
if spo2_col in cycles_valid.columns:
    latest_spo2 = latest_cycle[spo2_col]
    if pd.notna(latest_spo2) and latest_spo2 < 93:
        alerts['critical'].append(f"Hypoxemia: SpO₂ = {latest_spo2:.1f}%. Pulse-ox confirm, emergency if symptoms.")

# Check skin temp + infection
skin_col = 'Skin temp (celsius)'
if skin_col in cycles_valid.columns:
    latest_skin = latest_cycle[skin_col]
    if pd.notna(latest_skin) and latest_skin > 34.5 and infection_val >= 1:
        alerts['critical'].append(f"Active VZV febrile episode: Skin temp = {latest_skin:.1f}°C + Infection active. Valacyclovir dose, hydration.")

# Propranolol consecutive missed
prop_col = 'Propanolol'
if prop_col in vis_wide.columns:
    recent_prop = vis_wide.sort_values('observation_date').tail(14)
    prop_vals = recent_prop[prop_col].dropna()
    consec_missed = 0
    for v in reversed(prop_vals.values):
        if v == 0:
            consec_missed += 1
        else:
            break
    if consec_missed >= 5 and latest_rhr > 95:
        alerts['critical'].append(f"ICD risk window: Propranolol missed {consec_missed} consecutive days AND RHR {latest_rhr} bpm. Take dose now, cardiology contact.")

# WATCH alerts
# HRV spike > 2x 7-day mean
last_7d = cycles_valid.tail(7)
hrv_7d_mean = last_7d['Heart rate variability (ms)'].mean()
if latest_hrv > 2 * hrv_7d_mean:
    alerts['watch'].append(f"Vagal surge dysregulation: HRV {latest_hrv}ms > 2× 7-day mean ({hrv_7d_mean:.1f}ms). Not recovery, monitor.")

if skin_col in cycles_valid.columns and pd.notna(latest_skin) and latest_skin < 31:
    alerts['watch'].append(f"Peripheral vasoconstriction: Skin temp = {latest_skin:.1f}°C. VZV/autonomic flag.")

if latest_recovery < 20:
    alerts['watch'].append(f"Red zone: Recovery = {latest_recovery}%. Pacing budget <15, no exertion.")

if pacepoints < 5:
    alerts['watch'].append(f"Energy envelope critically depleted: PacePoints = {pacepoints}.")

if spo2_col in cycles_valid.columns and pd.notna(latest_spo2) and 93 <= latest_spo2 <= 95:
    alerts['watch'].append(f"Borderline hypoxemia: SpO₂ = {latest_spo2:.1f}%. Hydration + elevation, recheck.")

# POSITIVE alerts
if latest_recovery >= 70:
    alerts['positive'].append(f"Green day: Recovery = {latest_recovery}%. Managed exertion permitted with POTS protocol.")
if prop_taken >= 1:
    alerts['positive'].append("Propranolol adherence maintained today.")
if pacepoints > 35:
    alerts['positive'].append(f"Energy envelope stable: PacePoints = {pacepoints}.")

print(f"  CRITICAL: {len(alerts['critical'])} alerts")
print(f"  WATCH: {len(alerts['watch'])} alerts")
print(f"  POSITIVE: {len(alerts['positive'])} alerts")

for a in alerts['critical']:
    print(f"    🔴 {a}")
for a in alerts['watch']:
    print(f"    🟡 {a}")
for a in alerts['positive']:
    print(f"    🟢 {a}")

# Save alerts
with open(f'{OUT}/alerts.json', 'w') as f:
    json.dump(alerts, f, indent=2)

# ============================================================
# 4. TODAY'S SNAPSHOT
# ============================================================
print("\n[4] Building Today's Snapshot...")

# 7-day averages
last7 = cycles_valid[cycles_valid['Cycle start time'] >= today - pd.Timedelta(days=7)]
avg7_hrv = last7['Heart rate variability (ms)'].mean()
avg7_rhr = last7['Resting heart rate (bpm)'].mean()
avg7_rec = last7['Recovery score %'].mean()
avg7_sleep = last7['Asleep duration (min)'].mean()

snapshot = {
    'HRV': {'today': latest_hrv, 'source': 'physiological_cycles.csv', '7d_avg': round(avg7_hrv, 1),
            'baseline': BASELINE['HRV'], 'delta': round(latest_hrv - BASELINE['HRV'], 1)},
    'RHR': {'today': latest_rhr, 'source': 'physiological_cycles.csv', '7d_avg': round(avg7_rhr, 1),
            'baseline': BASELINE['RHR'], 'delta': round(latest_rhr - BASELINE['RHR'], 1)},
    'Recovery': {'today': latest_recovery, 'source': 'physiological_cycles.csv', '7d_avg': round(avg7_rec, 1),
                 'baseline': BASELINE['Recovery'], 'delta': round(latest_recovery - BASELINE['Recovery'], 1)},
    'Sleep': {'today': round(latest_sleep_min / 60, 1), 'source': 'physiological_cycles.csv',
              '7d_avg': round(avg7_sleep / 60, 1), 'baseline': BASELINE['Sleep_h'],
              'delta': round(latest_sleep_min / 60 - BASELINE['Sleep_h'], 1)},
    'Visible_HRV': {'today': vis_hrv, 'source': 'Visible_Data_Export', '7d_avg': 'N/A',
                    'baseline': 'N/A', 'delta': 'N/A'},
    'Visible_RHR': {'today': vis_rhr, 'source': 'Visible_Data_Export', '7d_avg': 'N/A',
                    'baseline': 'N/A', 'delta': 'N/A'},
    'Stability': {'today': stability, 'source': 'Visible_Data_Export', '7d_avg': 'N/A',
                  'baseline': 'N/A', 'delta': 'N/A'},
}

with open(f'{OUT}/snapshot.json', 'w') as f:
    json.dump(snapshot, f, indent=2, default=str)
print("  Snapshot saved")

# ============================================================
# 5. Q1 2026 QUARTERLY COMPARISON
# ============================================================
print("\n[5] Computing Q1 2026 Quarterly Comparison...")

q1 = cycles_valid[cycles_valid['Cycle start time'] >= '2026-01-01'].copy()
q1_stats = {
    'mean_recovery': round(q1['Recovery score %'].mean(), 1),
    'mean_hrv': round(q1['Heart rate variability (ms)'].mean(), 1),
    'mean_rhr': round(q1['Resting heart rate (bpm)'].mean(), 1),
    'green_pct': round((q1['Recovery score %'] >= 70).sum() / len(q1) * 100, 1),
    'red_pct': round((q1['Recovery score %'] < 33).sum() / len(q1) * 100, 1),
    'mean_sleep_min': round(q1['Asleep duration (min)'].mean(), 1),
    'n_days': len(q1),
}

# SpO2 < 94% events
if spo2_col in q1.columns:
    q1_stats['spo2_low_events'] = int((q1[spo2_col] < 94).sum())
else:
    q1_stats['spo2_low_events'] = 'N/A'

# Crash rate from Visible
vis_q1 = vis_wide[vis_wide['observation_date'] >= '2026-01-01']
if 'Crash' in vis_q1.columns:
    crash_days = vis_q1['Crash'].apply(pd.to_numeric, errors='coerce').fillna(0)
    q1_stats['crash_rate_pct'] = round((crash_days >= 1).sum() / len(vis_q1) * 100, 1) if len(vis_q1) > 0 else 0
else:
    q1_stats['crash_rate_pct'] = 'N/A'

with open(f'{OUT}/quarterly_comparison.json', 'w') as f:
    json.dump(q1_stats, f, indent=2)
print(f"  Q1 2026: {q1_stats['n_days']} days, HRV {q1_stats['mean_hrv']}ms, RHR {q1_stats['mean_rhr']}bpm, Recovery {q1_stats['mean_recovery']}%")

# ============================================================
# 6. MEDICATION ADHERENCE (PHARMACOLOGIC SAFETY)
# ============================================================
print("\n[6] Computing Medication Adherence...")

meds = {}
march_vis = vis_wide[vis_wide['observation_date'] >= '2026-03-01']

for med_name in ['Propanolol', 'Duloxetine', 'Gabapentin', 'Vyvanse', 'Adderall', 'Clonopine', 'GLP']:
    if med_name in vis_wide.columns:
        # March only
        march_data = march_vis[med_name].apply(pd.to_numeric, errors='coerce').dropna()
        taken = (march_data >= 1).sum()
        total = len(march_data)
        pct = round(taken / total * 100, 1) if total > 0 else 0
        
        # Last dose date
        all_data = vis_wide[['observation_date', med_name]].dropna(subset=[med_name])
        all_data[med_name] = pd.to_numeric(all_data[med_name], errors='coerce')
        taken_days = all_data[all_data[med_name] >= 1]
        last_dose = str(taken_days['observation_date'].max().date()) if len(taken_days) > 0 else 'Never'
        
        meds[med_name] = {
            'march_adherence_pct': pct,
            'march_taken': int(taken),
            'march_total': int(total),
            'last_dose': last_dose
        }
        print(f"  {med_name}: {pct}% ({taken}/{total} March days), last dose: {last_dose}")

with open(f'{OUT}/medication_adherence_v3.json', 'w') as f:
    json.dump(meds, f, indent=2)

# ============================================================
# 7. 7-DAY TREND (Mar 9-15)
# ============================================================
print("\n[7] Computing 7-Day Trend (Mar 9-15)...")

trend_7d = cycles_valid[
    (cycles_valid['Cycle start time'].dt.date >= pd.Timestamp('2026-03-09').date()) &
    (cycles_valid['Cycle start time'].dt.date <= pd.Timestamp('2026-03-15').date())
].copy()

trend_data = []
for _, row in trend_7d.iterrows():
    d = {
        'date': str(row['Cycle start time'].date()),
        'HRV_ms': row['Heart rate variability (ms)'],
        'RHR_bpm': row['Resting heart rate (bpm)'],
        'Recovery_pct': row['Recovery score %'],
        'Sleep_min': row['Asleep duration (min)'],
        'SWS_min': row.get('Deep (SWS) duration (min)', None),
        'REM_min': row.get('REM duration (min)', None),
        'Strain': row.get('Day Strain', None),
        'SpO2': row.get(spo2_col, None),
        'Skin_temp': row.get(skin_col, None),
    }
    # Check for open cycle
    if pd.isna(row.get('Cycle end time')):
        d['note'] = 'OPEN/INCOMPLETE CYCLE'
    # Check HRV anomaly
    if d['HRV_ms'] > 60:
        d['note'] = d.get('note', '') + ' VAGAL SURGE DYSREGULATION (HRV > 60ms)'
    trend_data.append(d)

with open(f'{OUT}/trend_7d.json', 'w') as f:
    json.dump(trend_data, f, indent=2, default=str)

for t in trend_data:
    note = t.get('note', '')
    print(f"  {t['date']}: HRV={t['HRV_ms']}ms, RHR={t['RHR_bpm']}bpm, Rec={t['Recovery_pct']}%, Sleep={t['Sleep_min']}min {note}")

# ============================================================
# 8. GLP-1 READINESS CHECKPOINT
# ============================================================
print("\n[8] GLP-1 Readiness Checkpoint...")

# Criterion 1: Propranolol adherence >= 80% (last 14 days)
last_14d_vis = vis_wide[vis_wide['observation_date'] >= today - pd.Timedelta(days=14)]
if 'Propanolol' in last_14d_vis.columns:
    prop_14d = last_14d_vis['Propanolol'].apply(pd.to_numeric, errors='coerce').dropna()
    prop_adh_14d = round((prop_14d >= 1).sum() / len(prop_14d) * 100, 1) if len(prop_14d) > 0 else 0
else:
    prop_adh_14d = 0
crit1 = prop_adh_14d >= 80

# Criterion 2: No crash in last 5 consecutive days
last_5d_vis = vis_wide[vis_wide['observation_date'] >= today - pd.Timedelta(days=5)]
if 'Crash' in last_5d_vis.columns:
    crash_5d = last_5d_vis['Crash'].apply(pd.to_numeric, errors='coerce').fillna(0)
    crit2 = (crash_5d >= 1).sum() == 0
else:
    crit2 = True
    
# Criterion 3: RHR < 95 bpm (7-day average)
crit3 = avg7_rhr < 95

# Criterion 4: Hydration protocol (cannot verify from data — mark as unknown)
crit4 = False  # Cannot verify from available data

# Criterion 5: Duloxetine QTc baseline obtained (cannot verify from data)
crit5 = False  # Cannot verify from available data

glp1_criteria = {
    'propranolol_adherence_14d': {'value': prop_adh_14d, 'threshold': 80, 'met': crit1},
    'no_crash_5d': {'value': f"{(crash_5d >= 1).sum() if 'Crash' in last_5d_vis.columns else 'N/A'} crash days", 'threshold': 0, 'met': crit2},
    'rhr_7d_avg': {'value': round(avg7_rhr, 1), 'threshold': 95, 'met': crit3},
    'hydration_protocol': {'value': 'Cannot verify from data', 'threshold': '>=2.5L + 3g NaCl', 'met': crit4},
    'duloxetine_qtc_baseline': {'value': 'Cannot verify from data', 'threshold': 'Obtained', 'met': crit5},
}
criteria_met = sum([crit1, crit2, crit3, crit4, crit5])
glp1_status = 'Safe' if criteria_met == 5 else ('Hold' if criteria_met >= 3 else 'Contraindicated')

glp1_criteria['summary'] = {'criteria_met': f"{criteria_met}/5", 'status': glp1_status}

# Convert numpy bools to Python bools for JSON
def convert_bools(obj):
    if isinstance(obj, dict):
        return {k: convert_bools(v) for k, v in obj.items()}
    elif isinstance(obj, (np.bool_, )):
        return bool(obj)
    elif isinstance(obj, (np.integer, )):
        return int(obj)
    elif isinstance(obj, (np.floating, )):
        return float(obj)
    return obj

with open(f'{OUT}/glp1_readiness.json', 'w') as f:
    json.dump(convert_bools(glp1_criteria), f, indent=2)

print(f"  Criteria met: {criteria_met}/5 → {glp1_status}")
for k, v in glp1_criteria.items():
    if k != 'summary':
        status = "✅" if v['met'] else "❌"
        print(f"    {status} {k}: {v['value']} (threshold: {v['threshold']})")

# ============================================================
# 9. GENERATE 6-PANEL DARK-THEMED DASHBOARD
# ============================================================
print("\n[9] Generating 6-Panel Dark-Themed Dashboard...")

q1_data = cycles_valid[cycles_valid['Cycle start time'] >= '2026-01-01'].copy()
q1_dates = pd.to_datetime(q1_data['Cycle start time'])

fig = plt.figure(figsize=(16, 14), facecolor='#0f172a')
gs = GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

ACCENT = '#38bdf8'
RED    = '#f87171'
YELLOW = '#fbbf24'
GREEN  = '#4ade80'
BG     = '#1e293b'

def style_ax(ax, title):
    ax.set_facecolor(BG)
    ax.tick_params(colors='white', labelsize=8)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color(ACCENT)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    for spine in ax.spines.values():
        spine.set_color('#334155')

# Panel 1: HRV with anomaly flag
ax1 = fig.add_subplot(gs[0, 0])
hrv_vals = q1_data['Heart rate variability (ms)']
ax1.fill_between(q1_dates, hrv_vals, alpha=0.3, color=ACCENT)
ax1.plot(q1_dates, hrv_vals, color=ACCENT, lw=1.5)
ax1.axhline(30, color=YELLOW, lw=1, ls='--', label='Threshold 30ms')
anomaly_mask = hrv_vals > 60
if anomaly_mask.any():
    ax1.scatter(q1_dates[anomaly_mask], hrv_vals[anomaly_mask],
                color=RED, s=80, zorder=5, label='Vagal surge anomaly')
ax1.set_ylabel('HRV (ms)', color='white')
ax1.legend(fontsize=7, facecolor=BG, labelcolor='white')
style_ax(ax1, 'HRV (ms) — Q1 2026 | ⚠️ Spikes = Dysregulation')

# Panel 2: RHR with danger zone
ax2 = fig.add_subplot(gs[0, 1])
rhr_vals = q1_data['Resting heart rate (bpm)']
colors_rhr = [RED if v > 100 else YELLOW if v > 85 else GREEN for v in rhr_vals]
ax2.bar(q1_dates, rhr_vals, color=colors_rhr, width=0.8, alpha=0.85)
ax2.axhline(100, color=RED, lw=1.5, ls='--', label='Critical >100')
ax2.axhline(85, color=YELLOW, lw=1, ls=':', label='Watch >85')
ax2.set_ylabel('RHR (bpm)', color='white')
ax2.legend(fontsize=7, facecolor=BG, labelcolor='white')
style_ax(ax2, 'Resting Heart Rate (bpm) — Q1 2026')

# Panel 3: Recovery % colored by zone
ax3 = fig.add_subplot(gs[1, 0])
rec_vals = q1_data['Recovery score %']
rec_colors = [GREEN if v >= 70 else (YELLOW if v >= 33 else RED) for v in rec_vals]
ax3.bar(q1_dates, rec_vals, color=rec_colors, width=0.8, alpha=0.85)
ax3.axhline(70, color=GREEN, lw=1, ls='--')
ax3.axhline(33, color=RED, lw=1, ls='--')
ax3.set_ylabel('Recovery %', color='white')
style_ax(ax3, 'Recovery Score — Q1 2026 | Green ≥70 | Red <33')

# Panel 4: Sleep architecture
ax4 = fig.add_subplot(gs[1, 1])
sws_vals = q1_data.get('Deep (SWS) duration (min)', pd.Series([0]*len(q1_data)))
rem_vals = q1_data.get('REM duration (min)', pd.Series([0]*len(q1_data)))
light_vals = q1_data.get('Light sleep duration (min)', pd.Series([0]*len(q1_data)))

ax4.bar(q1_dates, sws_vals, label='SWS', color='#818cf8', alpha=0.9)
ax4.bar(q1_dates, rem_vals, bottom=sws_vals, label='REM', color='#c084fc', alpha=0.9)
if light_vals.sum() > 0:
    ax4.bar(q1_dates, light_vals, bottom=sws_vals + rem_vals, label='Light', color='#475569', alpha=0.7)
ax4.axhline(420, color=GREEN, lw=1, ls='--', label='7h target')
ax4.set_ylabel('Sleep (min)', color='white')
ax4.legend(fontsize=7, facecolor=BG, labelcolor='white')
style_ax(ax4, 'Sleep Architecture — Q1 2026')

# Panel 5: Skin temp + SpO2 anomalies
ax5 = fig.add_subplot(gs[2, 0])
if skin_col in q1_data.columns:
    skin_vals = q1_data[skin_col].dropna()
    skin_dates = q1_dates[q1_data[skin_col].notna()]
    ax5.plot(skin_dates, skin_vals, color='#fb923c', lw=1.5, label='Skin Temp °C')
    ax5.axhline(34.5, color=RED, lw=1, ls='--', label='Fever flag >34.5°C')
    ax5.axhline(31.0, color=ACCENT, lw=1, ls='--', label='Cold flag <31°C')
    ax5.set_ylabel('°C', color='white')
    ax5.legend(fontsize=7, facecolor=BG, labelcolor='white')
style_ax(ax5, 'Skin Temperature — Infection/Vasoconstriction Flags')

# Panel 6: Propranolol adherence
ax6 = fig.add_subplot(gs[2, 1])
if 'Propanolol' in vis_wide.columns:
    prop_data = vis_wide[['observation_date', 'Propanolol']].dropna()
    prop_data = prop_data[prop_data['observation_date'] >= '2026-01-01']
    prop_data['Propanolol'] = pd.to_numeric(prop_data['Propanolol'], errors='coerce')
    taken = prop_data[prop_data['Propanolol'] >= 1]
    missed = prop_data[prop_data['Propanolol'] == 0]
    ax6.scatter(taken['observation_date'], [1]*len(taken),
                color=GREEN, s=60, label='Taken', marker='o', zorder=3)
    ax6.scatter(missed['observation_date'], [0]*len(missed),
                color=RED, s=60, label='Missed', marker='x', zorder=3)
    adherence_pct = (len(taken) / len(prop_data) * 100) if len(prop_data) > 0 else 0
    ax6.set_title(f'Propranolol Adherence — {adherence_pct:.0f}% of logged days',
                  color=ACCENT, fontsize=10, fontweight='bold')
ax6.set_ylabel('Taken (1) / Missed (0)', color='white')
ax6.legend(fontsize=7, facecolor=BG, labelcolor='white')
for spine in ax6.spines.values():
    spine.set_color('#334155')
ax6.set_facecolor(BG)
ax6.tick_params(colors='white', labelsize=8)
ax6.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax6.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')

fig.suptitle(
    'DR. FARAAZ RAHMAN — AUTONOMIC INTELLIGENCE DASHBOARD — 2026-03-15',
    color='white', fontsize=13, fontweight='bold', y=0.98
)
plt.savefig(f'{OUT}/autonomic_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#0f172a')
plt.close()
print("  Dashboard saved: autonomic_dashboard.png")

# ============================================================
# 10. LOOP SCORE TIMELINE CHART
# ============================================================
print("\n[10] Generating Loop Score Timeline Chart...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor='#0f172a')

# Top: Loop Score over time
ls_dates = ls_df['date']
ls_vals = ls_df['LS']
ls_colors = [RED if v >= 7 else (YELLOW if v >= 5 else (ACCENT if v >= 3 else GREEN)) for v in ls_vals]

ax1.set_facecolor(BG)
ax1.bar(ls_dates, ls_vals, color=ls_colors, width=1.0, alpha=0.85)
ax1.axhline(7, color=RED, lw=1.5, ls='--', label='Critical (7)')
ax1.axhline(5, color=YELLOW, lw=1, ls=':', label='Warning (5)')
ax1.axhline(3, color=GREEN, lw=1, ls=':', label='Monitoring (3)')
ax1.set_ylabel('Loop Score (0-10)', color='white', fontsize=11)
ax1.set_title('LOOP SCORE TIMELINE — Full Dataset', color=ACCENT, fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, facecolor=BG, labelcolor='white')
ax1.tick_params(colors='white', labelsize=8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
for spine in ax1.spines.values():
    spine.set_color('#334155')

# Bottom: Node breakdown (stacked area) for Q1 2026
ls_q1 = ls_df[ls_df['date'] >= '2026-01-01']
ax2.set_facecolor(BG)
ax2.stackplot(ls_q1['date'], 
              ls_q1['AN'] / 15 * 10,
              ls_q1['SN'] / 15 * 10,
              ls_q1['IN'] / 15 * 10,
              ls_q1['PN'] / 15 * 10,
              ls_q1['DN'] / 15 * 10,
              labels=['AN (Autonomic)', 'SN (Sleep)', 'IN (Inflammatory)', 'PN (Pharmacologic)', 'DN (Deconditioning)'],
              colors=['#38bdf8', '#818cf8', '#f87171', '#fbbf24', '#4ade80'],
              alpha=0.7)
ax2.set_ylabel('Node Contribution to LS', color='white', fontsize=11)
ax2.set_title('LOOP SCORE NODE BREAKDOWN — Q1 2026', color=ACCENT, fontsize=12, fontweight='bold')
ax2.legend(fontsize=8, facecolor=BG, labelcolor='white', loc='upper left')
ax2.tick_params(colors='white', labelsize=8)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
for spine in ax2.spines.values():
    spine.set_color('#334155')

fig.suptitle('LOOP SCORE ANALYSIS — DR. FARAAZ RAHMAN', color='white', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'{OUT}/loop_score_timeline.png', dpi=150, bbox_inches='tight', facecolor='#0f172a')
plt.close()
print("  Loop Score timeline saved")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*70}")
print("ALL v3 OUTPUT FILES:")
for f in sorted(os.listdir(OUT)):
    fpath = os.path.join(OUT, f)
    size = os.path.getsize(fpath)
    print(f"  {f} ({size:,} bytes)")
print(f"{'='*70}")
