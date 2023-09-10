import datetime
from pathlib import Path
import json
from json import JSONDecodeError
from typing import Any, Dict, Tuple, Optional
import logging
import pandas as pd
import fire

# get data from api
import requests
from yarl import URL

# data_analyst
import matplotlib.pyplot as plt
import seaborn as sns


# import 

import cleaning, feature_store, validation

logger = logging.getLogger(__name__)

def from_file_url(export_start: datetime.datetime, export_end: datetime.datetime, datetime_format: str="%Y-%m-%d %H:%M",file_path: str="./data/data_for_project.csv") -> Optional[pd.DataFrame]:

    data = pd.read_csv(file_path, delimiter=";")
    records = data[(data["HourUTC"] >= export_start.strftime(datetime_format)) & (data["HourUTC"] < export_end.strftime(datetime_format))]

    return records

def from_api_url(export_end: datetime.datetime, days_export: int = 30, api_url: str="https://api.energidataservice.dk/dataset/ConsumptionDE35Hour",datetime_format: str="%Y-%m-%dT%H:%M") -> Optional[pd.DataFrame]:

    export_start = export_end - datetime.timedelta(days=days_export)

    query_params = {
        "offset": 0,
        "start": export_start.strftime(datetime_format),
        "end": export_end.strftime(datetime_format),
        "sort": "HourUTC",
        "timezone": "utc"
    }
    url = URL(api_url) % query_params
    url = str(url)

    response = requests.get(url)
    logger.info(f"Response received from API with status code: {response.status_code} ")

    try:
        response = response.json()
    except JSONDecodeError:
        logger.error(f"Response status = {response.status_code}. Could not decode response from API with URL: {url}")

        return None

    records = response["records"]
    records = pd.DataFrame.from_records(records)

    return records

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

    return data

def save_json(data: dict, file_name: str):

    data_path = Path(file_name) 
    with open(data_path, "w") as f:
        json.dump(data, f)
    

def run(export_start, export_end, datetime_format):
    data_f = from_file_url(export_start,export_end)
    data_f = transform(data_f)
    feature_group_version = 1
    validation_expectation_suite = validation.build_expectation_suite()
    
    feature_store.to_feature_store(
        data_f,
        validation_expectation_suite=validation_expectation_suite,
        feature_group_version=feature_group_version,
    )
    
    metadata = {
        "export_start": export_start.strftime("%Y-%m-%d %H:%M"),
        "export_end": export_end.strftime("%Y-%m-%d %H:%M"),
        "time_create_feature": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    metadata["feature_group_version"] = feature_group_version
    metadata_name = datetime.datetime.now().strftime("%Y%m%d%H%M") + "_featurecleaning_pipeline.json"
    save_json(metadata, file_name=metadata_name)

    return metadata

if __name__=="__main__":

    # current = datetime.datetime.now()
    datetime_format = "%Y-%m-%d %H:%M"
    current = datetime.datetime.strptime("2020-10-30 22:00", datetime_format)
    export_start = datetime.datetime.strptime("2020-06-30 22:00",datetime_format)

    fire.Fire(run(export_start, current, datetime_format))
    
    

    

    
    
    





