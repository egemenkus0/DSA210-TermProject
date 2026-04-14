# this code is solely for converting the burnout dataset's risk levels
# and genders to a more humanly readable 0-1-2's. 

import os
import pandas as pd

# selecitng data raw and setting the out path
current_dir = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(current_dir, "student_mental_health_burnout_1M.csv")
OUT = os.path.join(current_dir, "burnout_processed.csv")


if not RAW.exists():
    raise FileNotFoundError(f'Dataset not found at {RAW}')

# loading the data
print(f'Loading {RAW} ...')
df = pd.read_csv(RAW)
print(f'  Shape: {df.shape}')

df['risk_level_encoded'] = df['risk_level'].map({'Low': 0, 'Medium': 1, 'High': 2})
df['gender_encoded'] = df['gender'].map({'Male': 0, 'Female': 1, 'Other': 2})

# saving it as csv
df.to_csv(OUT, index=False)
print(f'Saved -> {OUT}')
