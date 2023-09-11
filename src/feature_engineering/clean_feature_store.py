import fire
import hopsworks

import feature_store

# import utils
from utils import utils

def clean():
    fs = utils.hopsworks_feature_login()

    print("Deleting feature views and training datasets...")
    try:
        feature_views = fs.get_feature_views(name="energy_consumption_denmark_view")

        for feature_view in feature_views:
            try:
                feature_view.delete()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

    print("Deleting feature groups...")
    try:
        feature_groups = fs.get_feature_groups(name="energy_consumption_denmark")
        for feature_group in feature_groups:
            try:
                feature_group.delete()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    fire.Fire(clean)
