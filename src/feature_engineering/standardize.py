import pandas as pd
from sklearn.preprocessing import StandardScaler

def standardize_data(df: pd.DataFrame):
    #print(df.head())
    df['HourUTC_'] = pd.to_datetime(df['datetime_utc']).astype('int64')
    max_a = df.HourUTC_.max()
    min_a = df.HourUTC_.min()
    min_norm = -1
    max_norm =1
    df['HourUTC_NORMA'] = (df.HourUTC_- min_a) *(max_norm - min_norm) / (max_a-min_a) + min_norm
    df['datetime_utc']=df['HourUTC_NORMA']
    # define standard scaler
    scaler = StandardScaler()
    df_a=df[['datetime_utc','area','consumer_type','energy_consumption']]
    # transform data
    df_standardize = scaler.fit_transform(df_a)
    df = pd.DataFrame(df_standardize, columns = ['datetime_utc','area','consumer_type','energy_consumption'])
    return df


