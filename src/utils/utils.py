import logging
import json
import hopsworks
from dotenv import load_dotenv
import os
import datetime
from typing import Any, Dict, Tuple, Optional
import pandas as pd
from pathlib import Path
import hsfs
import hsml

import wandb
# logger = getLogger(__name__)

def load_env_vars() -> dict:
    load_dotenv("./utils/.env-template")
    load_dotenv("./utils/.env", override=True)
    return dict(os.environ)

def getLogger(name: str) -> logging.Logger:

    logging.basicConfig(filename='../all.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    log = logging.getLogger(name)

    return log

def save_json(data: dict, file_name: str):
    
    data_path = Path(file_name) 
    with open(data_path, "w") as f:
        json.dump(data, f)

def wandb_login():
    return wandb.login(key=load_env_vars()["WANDB_API_KEY"])


def hopsworks_feature_login ():
    project = hopsworks.login(
        api_key_value=load_env_vars()["FS_API_KEY"], project=load_env_vars()["FS_PROJECT_NAME"]
    )

    return project.get_feature_store()

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

def load_json(data_path: str) -> dict:


    with open(data_path, "r") as f:
        return json.load(f)

def create_feature_view(fview_name: str, fgroup_ver: int):
    feature_store = hopsworks_feature_login()

    try:
        feature_views = feature_store.get_feature_views(name=fview_name)
    except hsfs.client.exceptions.RestAPIError:
        print("No feature views found for energy_consumption_denmark_view.")

        feature_views = []

    for feature_view in feature_views:
        try:
            feature_view.delete_all_training_datasets()
        except hsfs.client.exceptions.RestAPIError:
            print(
                f"Failed to delete training datasets for feature view {feature_view.name} with version {feature_view.version}."
            )

        try:
            feature_view.delete()
        except hsfs.client.exceptions.RestAPIError:
            print(
                f"Failed to delete feature view {feature_view.name} with version {feature_view.version}."
            )

    feature_group = feature_store.get_feature_group("energy_consumption_denmark", fgroup_ver)



    feature_view = feature_store.create_feature_view(
        name=fview_name,
        query=feature_group.select_all(),
        labels=[],    
    )

    metadata = {
        "feature_group" : feature_group.name,
        "feature_group_version" : fgroup_ver,
        "feature_view" : fview_name,
        "feature_view_version" : feature_view.version,
        "time_create" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }


    return feature_view, metadata

def create_training_dataset(fgroup_ver: int, fgroup_name: str = "energy_consumption_denmark") -> pd.DataFrame:
    feature_store = hopsworks_feature_login()
    try: 
        feature_group = feature_store.get_feature_group(fgroup_name, fgroup_ver)
    except:
        print("Feature group energy_consumption_denmark with version {fgroup_ver} is not exist.")
        raise 

    dataframe = feature_group.read(wallclock_time=None, online=False, dataframe_type="pandas", read_options={})
    return dataframe
    