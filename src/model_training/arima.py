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

from utils import utils
import train
import save_model

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
    
    start = datetime.datetime.now()

    model = ARIMA(y_train, order=(1,0,1)).fit()

    end = datetime.datetime.now()
    train_time = end - start

    train_metadata = {
        "model_name" : "arima",
        "time_to_train" : train_time.total_seconds(),
        "model_order": (1, 0, 1),
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
    
    model_metadata = {
        "feature_group_name" : dataset_metadata["feature_group_name"],
        "feature_group_version" : dataset_metadata["feature_group_version"],
        "dataset_name" : dataset_metadata["dataset_name"], 
        "dataset_version" : dataset_metadata["dataset_version"],
        "model_name" : train_metadata["model_name"],
        "time_to_train" : train_metadata["time_to_train"],
        "model_order": train_metadata["model_order"],
        "aic": train_metadata["aic"],
        "bic": train_metadata["bic"],
        "residuals_mean": train_metadata["residuals_mean"],
        "residuals_std": train_metadata["residuals_std"],
        "coefficients": train_metadata["coefficients"],
        # "summary" : train_metadata["summary"]
    }

    model_name = "./data/models/" + model_metadata["dataset_name"] + "_" + str(model_metadata["dataset_version"]) + "_"+ model_metadata["model_name"]+".pkl"
    
    model_metadata_name = "./data/models/" + model_metadata["dataset_name"] + "_" + str(model_metadata["dataset_version"]) + "_"+model_metadata["model_name"]+".json"



    train.pickle_save_model(model, model_name)
    utils.save_json(model_metadata, model_metadata_name)

if __name__=="__main__":
    fire.Fire(run())
    