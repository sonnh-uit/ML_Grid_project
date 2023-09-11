import logging
import json
import hopsworks
from dotenv import load_dotenv
import os
import datetime
from typing import Any, Dict, Tuple, Optional
import pandas as pd

logger = logging.getLogger(__name__)

def load_env_vars() -> dict:
    load_dotenv("./utils/.env-template")
    load_dotenv("./utils/.env", override=True)
    return dict(os.environ)

def get_logger(name: str) -> logging.Logger:

    logging.basicConfig(filename='all.log',
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(name)

    return logger

def save_json(data: dict, file_name: str):
    
    data_path = Path(file_name) 
    with open(data_path, "w") as f:
        json.dump(data, f)

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

