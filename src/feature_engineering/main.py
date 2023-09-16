import datetime
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import logging
import pandas as pd
import fire

# get data from api
import requests
from yarl import URL


import cleaning, feature_store, validation
from utils import utils

def data_analyst(data: pd):
    # print ("Data Sharp: \n",  data.shape)
    # print ("Data Describe: \n",  data.describe())

    # plt.figure(figsize=(8,5))
    # sns.histplot(data['PriceArea'], kde=True)
    # plt.title('Price area', fontsize=20)
    # plt.savefig('PriceArea.png')
    # plt.close()

    # data = pd.get_dummies(data)
    print(data.isnull().sum())
    print(data.columns)



def transform(data: pd.DataFrame):
    data = cleaning.rename_columns(data)
    data = cleaning.cast_columns(data)
    data = cleaning.encode_area_column(data)
    data = cleaning.delete_missing_data(data)
    data = cleaning.remove_duplicate(data)

    return data

def run(export_start, export_end, datetime_format):
    data_f = utils.from_file_url(export_start,export_end)
    data_f = transform(data_f)
    feature_group_version = 1
    validation_expectation_suite = validation.build_expectation_suite()
    
    metadata = feature_store.to_feature_store(
        data_f,
        validation_expectation_suite=validation_expectation_suite,
        feature_group_version=feature_group_version,
    )
    
    metadata["export_start"] = export_start.strftime("%Y-%m-%d %H:%M")
    metadata["export_end"] = export_end.strftime("%Y-%m-%d %H:%M")
    file_name = "./data/metadata/feature_group/" + metadata["feature_group_name"] + "_" + str(metadata["feature_group_version"]) + ".json"
    utils.save_json(metadata, file_name=file_name)

    return metadata

if __name__=="__main__":

    # current = datetime.datetime.now()
    datetime_format = "%Y-%m-%d %H:%M"
    current = datetime.datetime.strptime("2023-06-30 22:00", datetime_format)
    export_start = datetime.datetime.strptime("2023-05-30 22:00",datetime_format)

    fire.Fire(run(export_start, current, datetime_format))
    