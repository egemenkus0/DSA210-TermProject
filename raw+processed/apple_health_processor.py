# this code is solely for converting the apple health's impossible xml stuff
# to a humanly readable csv and adding extra columns

import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd
import os

# selecitng data raw and setting the out path
current_dir = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(current_dir, "apple_health_export", "export.xml")
OUT = os.path.join(current_dir, "health_processed.csv")

# exam period at sabanci university (for me)
EXAM_PERIODS = [
    ('2025-01-02', '2025-01-12'),
    ('2025-05-24', '2025-06-04'),
    ('2026-01-04', '2026-01-14'),
    ('2026-06-01', '2026-06-10'),
    ('2024-11-15', '2024-12-15'),
    ('2025-03-15', '2025-04-15'),
    ('2025-11-15', '2025-12-15'),
    ('2026-03-15', '2026-04-15'),
]

# apple health data with help of ai to figure it out
RECORD_TYPES = {
    'HKQuantityTypeIdentifierStepCount':                'steps',
    'HKQuantityTypeIdentifierHeartRate':                'heart_rate',
    'HKQuantityTypeIdentifierRestingHeartRate':         'resting_hr',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': 'hrv',
    'HKQuantityTypeIdentifierActiveEnergyBurned':       'active_calories',
    'HKQuantityTypeIdentifierAppleExerciseTime':        'exercise_minutes',
    'HKQuantityTypeIdentifierDistanceWalkingRunning':   'distance_km',
}

# start date of the exams.
START_DATE = '2024-09-01'

# checking if the file exists using os
if not os.path.exists(RAW):
    raise FileNotFoundError(f'export.xml not found at {RAW}')

# xml parse
print(f'Parsing {RAW} ...')
root = ET.parse(RAW).getroot()

# a dict of daily apple health data
daily = {}

for rec in root.iter('Record'):
    rtype = rec.attrib.get('type', '')
    if rtype not in RECORD_TYPES:
        continue
    
    date_str = rec.attrib.get('startDate', '')[:10]
    if date_str < START_DATE:
        continue
    
    try:
        val = float(rec.attrib['value'])
        metric = RECORD_TYPES[rtype]

        # date key.
        if date_str not in daily:
            daily[date_str] = {}
        
        # Mmetric data of daily dates
        if metric not in daily[date_str]:
            daily[date_str][metric] = []
            
        daily[date_str][metric].append(val)
        
    except (ValueError, KeyError):
        continue

rows = []
for date_str in sorted(daily.keys()):
    d = daily[date_str]
    rows.append({
        'date':               date_str,
        'daily_steps':        sum(d.get('steps', [0])),
        'avg_heart_rate':     sum(d['heart_rate']) / len(d['heart_rate']) if d.get('heart_rate') else None,
        'resting_heart_rate': sum(d['resting_hr']) / len(d['resting_hr']) if d.get('resting_hr') else None,
        'hrv':                sum(d['hrv']) / len(d['hrv']) if d.get('hrv') else None,
        'active_calories':    sum(d.get('active_calories', [0])),
        'exercise_minutes':   sum(d.get('exercise_minutes', [0])),
        'distance_km':        sum(d.get('distance_km', [0])),
    })

df = pd.DataFrame(rows)
df['date'] = pd.to_datetime(df['date'])
df['is_exam_period'] = 0
for start, end in EXAM_PERIODS:
    df.loc[(df['date'] >= start) & (df['date'] <= end), 'is_exam_period'] = 1

# this is the important part. for analyzing and combining with
# the other data, we are converiting the data into a 1-7 scale of physical activity
# which the other list has


# activity normalization
p95 = df['daily_steps'].quantile(0.95)
df['physical_activity_normalized'] = (df['daily_steps'] / p95 * 7).clip(upper=7)

# then converting it into csv.

df.to_csv(OUT, index=False)
print(f'Saved { len(df) } rows -> { OUT }')
print(f'  Exam days: { df["is_exam_period"].sum() } | Normal: { (df["is_exam_period"]==0).sum() }')