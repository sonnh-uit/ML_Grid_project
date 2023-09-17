import pandas as pd
from StandardScaler import sklearn.preprocessing

def standardize_data(data: pd.DataFrame):
    # define standard scaler
    scaler = StandardScaler()
    df_dropcolunm = data.drop(columns=['HourUTC', 'HourDK', 'PriceArea', 'HourUTC_', 'HourDK_'])
    # transform data
    df_standardize = scaler.fit_transform(df_dropcolunm)
    return df_standardize


