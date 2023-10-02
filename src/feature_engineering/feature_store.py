import hopsworks
import pandas as pd
from great_expectations.core import ExpectationSuite
from hsfs.feature_group import FeatureGroup
import datetime
# import utils
from utils import utils

def to_feature_store(
    fgroup_name,
    feature_code: int,
    data: pd.DataFrame,
    fgroup_description,
    validation_expectation_suite: ExpectationSuite,
    feature_group_version: int,
    
) -> FeatureGroup:

    feature_store = utils.hopsworks_feature_login()

    # Create feature group.
    energy_feature_group = feature_store.get_or_create_feature_group(
        name=fgroup_name,
        version=feature_group_version,
        description=fgroup_description,
        primary_key=["area", "consumer_type"],
        event_time="datetime_utc",
        online_enabled=False,
        expectation_suite=validation_expectation_suite,
    )
    # Upload data.
    energy_feature_group.insert(
        features=data,
        overwrite=False,
        write_options={
            "wait_for_job": True,
        },
    )


    # Update statistics.
    energy_feature_group.statistics_config = {
        "enabled": True,
        "histograms": True,
        "correlations": True,
    }
    energy_feature_group.update_statistics_config()
    energy_feature_group.compute_statistics()

    metadata = {
        "feature_group_name" : energy_feature_group.name,
        "feature_group_version" :  energy_feature_group.version,
        "feature_primary_keys" : ["area", "consumer_type"],
        "time_create_feature": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    return metadata
