# =========================================
# Date    : 2023-10-02 19:49:54
# Author  : Son Nguyen-Hong (sonnh.uit@gmail.com)
# Link    : sonnh.net
# File    : create_feature_1.py
# =========================================


import pandas as pd

def create_feature_1(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
  
    data['hour'] = pd.to_datetime(data['datetime_utc']).dt.hour
    data['avg_energy_per_area'] = data.groupby('area')['energy_consumption'].transform('mean')
 
    return data