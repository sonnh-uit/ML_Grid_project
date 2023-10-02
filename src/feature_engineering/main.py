# =========================================
# Date    : 2023-09-30 14:41:55
# Author  : Son Nguyen-Hong (sonnh.uit@gmail.com)
# Link    : sonnh.net
# File    : main.py
# =========================================


import datetime
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import logging
import pandas as pd
import fire

# get data from api
import requests
from yarl import URL


import cleaning, feature_store, validation, standardize, vectorize, create_feature_1
from utils import utils

def transform(data: pd.DataFrame):
    data = cleaning.rename_columns(data)
    data = cleaning.cast_columns(data)
    data = cleaning.encode_area_column(data)
    data = cleaning.delete_missing_data(data)
    data = cleaning.remove_duplicate(data)

    return data

def run(feature: dict):
    datetime_format = feature['datetime_format']
    feature_name = feature['name']
    fgroup_version = feature['fgroup_version']
    export_start = datetime.datetime.strptime(feature['export_start'],datetime_format)
    export_end = datetime.datetime.strptime(feature['export_end'], datetime_format)
    feature_code = feature['feature_code']
    description = feature['description']


    data_f = utils.from_file_url(export_start,export_end)
    data_f = transform(data_f)
    
    # data_f = standardize.standardize_data(data_f)
    # data_f = vectorize.vectorize_data(data_f)
    if feature_code == 0 :
        validation_expectation_suite = validation.build_expectation_suite(feature_name)
    elif feature_code == 1:
        data_f = create_feature_1.create_feature_1(data_f)
        validation_expectation_suite = validation.build_expectation_feature_1(feature_name)
    
    metadata = feature_store.to_feature_store(
        feature_name,
        feature_code,
        data_f,
        description,
        validation_expectation_suite=validation_expectation_suite,
        feature_group_version=fgroup_version,
        
    )
    
    metadata["export_start"] = export_start.strftime("%Y-%m-%d %H:%M")
    metadata["export_end"] = export_end.strftime("%Y-%m-%d %H:%M")
    file_name = "./data/metadata/feature_group/" + metadata["feature_group_name"] + "_" + str(metadata["feature_group_version"]) + ".json"
    utils.save_json(metadata, file_name=file_name)

    return metadata

if __name__=="__main__":

    feature_groups = utils.load_yaml_env()
    for feature in feature_groups['feature_store']:
        fire.Fire(run(feature))