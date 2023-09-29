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

def run():
    
    train_data, test_data, valid_data, dataset_metadata = get_dataset("arima", 1, 1)
    model, train_metadata = arima( train_data)
    evaluate = model_evaluate(model, test_data, valid_data)

    model_name = "./data/models/" + dataset_metadata["dataset_name"] + "_" + str(dataset_metadata["dataset_version"]) + "_arima.pkl"
    
    model_metadata_name = "./data/models/" + dataset_metadata["dataset_name"] + "_" + str(dataset_metadata["dataset_version"]) + "_arima.json"
    model_evaluate_name = "./data/models/eval_" + dataset_metadata["dataset_name"] + "_" + str(dataset_metadata["dataset_version"]) + "_arima.json"

    train.pickle_save_model(model, model_name)
    utils.save_json(train_metadata, model_metadata_name)
    utils.save_json(evaluate, model_evaluate_name)

if __name__=="__main__":
    fire.Fire(run())
  
    