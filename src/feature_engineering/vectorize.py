import pandas as pd
import numpy as np

def vectorize_data(df: pd.DataFrame):
    # mean of every single column in df
    df=df.apply(np.mean)
    return df