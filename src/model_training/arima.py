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
import fire
import json
import hsml
from hsml.model_schema import ModelSchema
import time

from utils import utils
import train


def get_dataset( fgroup_name: str, fgroup_ver: int,ds_test_size, ds_valid_size):

    dataset = utils.create_training_dataset(fgroup_ver, fgroup_name)
    dataset["datetime_utc"] = pd.to_datetime(dataset.datetime_utc)

    print(dataset.head())

    dataset_metadata = {
        "feature_group_name" : fgroup_name,
        "feature_group_version" : fgroup_ver,
    }

    train_data, test_data, valid_data = train.split_dataset(dataset,ds_test_size,ds_valid_size)
    return train_data, test_data, valid_data, dataset_metadata
    
def arima(train_data: pd.DataFrame):

    train_column = "energy_consumption"

    x_train = np.array(train_data.index).reshape(-1, 1)
    y_train = np.array(train_data[train_column])
    
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
        "train_result" : {
            "time_to_train" : train_time.total_seconds(),
            "model_order" : model_order,
            "aic": model.aic,
            "bic": model.bic,
            "residuals_mean": model.resid.mean(),
            "residuals_std": model.resid.std(),
            "coefficients": model.params.tolist(),
        }
        
    }

    return model, train_metadata

def model_evaluate(model: ARIMA, test_data: pd.DataFrame, valid_data: pd.DataFrame):

    train_column = "energy_consumption"

    x_test = np.array(test_data.index).reshape(-1, 1)
    y_test = np.array(test_data[train_column])
    y_pred = model.predict(start=int(x_test[0]), end=int(len(x_test)+x_test[0]-1))

    x_val= np.array(valid_data.index).reshape(-1, 1)
    y_val = np.array(valid_data[train_column])
    y_pred_val =  model.predict(start=int(x_val[0]), end=int(len(x_val)+x_val[0]-1))

    evaluate_result = train.evaluate(y_test,y_pred,y_val,y_pred_val)
    return evaluate_result

def run(model: dict):
    
    fgroup_name = model['fgroup_name'] 
    fgroup_ver =  model['fgroup_version']
    ds_test_size = model['ds_test_size']
    ds_valid_size = model['ds_valid_size']

    train_data, test_data, valid_data, dataset_metadata = get_dataset(fgroup_name, fgroup_ver,ds_test_size,ds_valid_size)
    model_trained, train_metadata = arima( train_data)
    evaluate = model_evaluate(model_trained, test_data, valid_data)

    model_root_directory = "./data/models/"

    model_name = model['name'] + ".pkl"
    model_metadata_name = model['name'] + ".json"
    model_evaluate_name = model['name'] + "_eval.json"

    train.pickle_save_model(model_trained, model_root_directory + model_name)
    utils.save_json(train_metadata, model_root_directory + model_metadata_name)
    utils.save_json(evaluate, model_root_directory + model_evaluate_name)

if __name__=="__main__":
    models = utils.load_yaml_env()
    for model in models['model_training']:
        if model['name'].startswith('arima'):
            fire.Fire(run(model))
            time.sleep(30)
            # print(model['name'] + ".pkl") 
  
    