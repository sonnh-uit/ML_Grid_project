# =========================================
# Date    : 2023-09-25 10:27:01
# Author  : Son Nguyen-Hong (sonnh.uit@gmail.com)
# Link    : sonnh.net
# =========================================

import pandas as pd
import hopsworks
import fire
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse, mean_absolute_error as mae, r2_score as r2
import pickle 
import hsfs
import datetime
from typing import Any, Dict, Tuple, Optional

from utils import utils

logger = utils.getLogger(__name__)

def split_dataset(dataset: pd.DataFrame, test_size: int=1, valid_size: int=0.1):

    test_split_idx = int(dataset.shape[0] * (1-test_size))
    valid_split_idx = int(dataset.shape[0] * (1-(valid_size+test_size)))

    return dataset[:valid_split_idx], dataset[valid_split_idx:test_split_idx+1], dataset[test_split_idx+1:]


def pickle_save_model(model, model_path: str):

    return pickle.dump(model, open(model_path, 'wb'))

def evaluate(test_data,prediction_data,validate_data,prediction_validate_data):

    mean_absolute_error = mean_absolute_error(test_data, prediction_data)
    test_ape = np.abs((test_data - prediction_data) / test_data)
    test_mape = np.mean(test_ape) * 100
    test_mse = mean_squared_error(test_data, prediction_data)
    test_rmse = np.sqrt(test_mse)

    val_mae = mean_absolute_error(validate_data, prediction_validate_data)
    val_ape = np.abs((validate_data - prediction_validate_data) / validate_data)
    val_mape = np.mean(val_ape) * 100
    val_mse = mean_squared_error(validate_data, prediction_validate_data)
    val_rmse = np.sqrt(val_mse)
    
    metadata = {
        "test_result" : {
            "mean_absolute_error" : mean_absolute_error,
            "mean_absolute_percentage_error" : test_mape,
            "root_mean_squared_error" : test_rmse,
        },
        "validate_result" : {
            "mean_absolute_error" : val_mae,
            "mean_absolute_percentage_error" : val_mape,
            "root_mean_squared_error" : val_rmse
        }
    }

    return metadata

# def run():

#     model, metadata = linear_regression("linear_regression", 1)
#     model_name = "./data/models/" + metadata["dataset_name"] + "_" + str(metadata["dataset_version"]) + ".pkl"
#     pickle_save_model(model, model_name)
    # save_model.save_model(model_name,"test_save_arima_model",1)

if __name__=="__main__":
    fire.Fire(run())
    # dataset = utils.create_training_dataset(1)
    # print(dataset.info())


