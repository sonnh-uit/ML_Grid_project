# =========================================
# Date    : 2023-09-24 20:19:41
# Author  : Son Nguyen-Hong (sonnh.uit@gmail.com)
# Link    : sonnh.net
# =========================================

import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
import fire
import json
import hsml
from hsml.model_schema import ModelSchema
from utils import utils
import train


def get_dataset( dataset_name: str, dataset_version: int, fgroup_ver: int=1):

    dataset = utils.create_training_dataset(fgroup_ver)
    dataset["datetime_utc"] = pd.to_datetime(dataset.datetime_utc)

    dataset_metadata = {
        "feature_group_name" : "energy_consumption_denmark",
        "feature_group_version" : fgroup_ver,
        "dataset_name" : dataset_name, 
        "dataset_version" : dataset_version
    }

    train_data, test_data, valid_data = train.split_dataset(dataset)
    return train_data, test_data, valid_data, dataset_metadata
    
def arima(train_data: pd.DataFrame, test_data: pd.DataFrame, valid_data: pd.DataFrame):
    x_train = np.array(train_data.index).reshape(-1, 1)
    y_train = np.array(train_data['energy_consumption'])
    
    

    # This block bellow to get bes model metric order, the result 
    # is Best model:  ARIMA(5,0,0)(0,0,0)[0] intercept
    start = datetime.datetime.now()
    model_autoARIMA = auto_arima(y_train, start_p=0, start_q=0,
                           max_p=5, max_q=5, m=12,
                           start_P=0, seasonal=False,
                           d=0, D=0, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
    model_order = model_autoARIMA.order

    model = ARIMA(y_train, order=model_order).fit()
    
    end = datetime.datetime.now()
    train_time = end - start

    train_metadata = {
        "time_to_train" : train_time.total_seconds(),
        # "model_order": int("".join([str(item) for item in model_order])),
        "model_order" : model_order,
        "aic": model.aic,
        "bic": model.bic,
        "residuals_mean": model.resid.mean(),
        "residuals_std": model.resid.std(),
        "coefficients": model.params.tolist(),
    }

    return model, train_metadata

def run():
    
    train_data, test_data, valid_data, dataset_metadata = get_dataset("arima", 1, 1)
    model, train_metadata = arima( train_data, test_data, valid_data)
    
    model_name = "./data/models/" + dataset_metadata["dataset_name"] + "_" + str(dataset_metadata["dataset_version"]) + "_arima.pkl"
    
    model_metadata_name = "./data/models/" + dataset_metadata["dataset_name"] + "_" + str(dataset_metadata["dataset_version"]) + "_arima.json"

    train.pickle_save_model(model, model_name)
    utils.save_json(train_metadata, model_metadata_name)
    # utils.save_json(model_description, model_description_name)

if __name__=="__main__":
    fire.Fire(run())
    