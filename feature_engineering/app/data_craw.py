import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import logging
import pandas as pd
import requests
from yarl import URL

logger = logging.getLogger(__name__)

def from_file_url(file_path: str, export_start: datetime.datetime, export_end: datetime.datetime, datetime_format: str) -> Optional[pd.DataFrame]:

    data = pd.read_csv(file_path, delimiter=";")
    records = data[(data["HourUTC"] >= export_start.strftime(datetime_format)) & (data["HourUTC"] < export_end.strftime(datetime_format))]

    return records

def from_api_url(datetime_format: str, export_end: datetime.datetime, days_export: int = 30, api_url: str="https://api.energidataservice.dk/dataset/ConsumptionDE35Hour") -> Optional[pd.DataFrame]:

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


if __name__=="__main__":
    data_path = "./data/data_for_project.csv"
    datetime_format = "%Y-%m-%d %H:%M"
    # current = datetime.datetime.now()
    current = datetime.datetime.strptime("2023-05-30 23:00", datetime_format)
    export_start = datetime.datetime.strptime("2022-10-27 14:00",datetime_format)

    print(from_file_url(data_path,export_start,current,datetime_format))
    print(from_api_url("%Y-%m-%dT%H:%M",current,3))



