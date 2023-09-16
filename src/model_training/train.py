import pandas as pd
import hopsworks
import fire
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse, mean_absolute_error as mae, r2_score as r2
import pickle 
import hsfs
import datetime


from utils import utils

logger = utils.getLogger(__name__)
    
def linear_regression(dataset_name: str, dataset_version: int) -> LinearRegression:

    feature_group_version = 1
    dataset = utils.create_training_dataset(feature_group_version)

    dataset["datetime_utc_new"] = pd.to_datetime(dataset['datetime_utc'], format='%Y-%m-%d %H:%M')

    dataset.drop(columns=['datetime_utc'], inplace=True)

    X = dataset.iloc[:, :-1] 
    y = dataset.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=1)

    LR = LinearRegression()
    start = datetime.datetime.now()
    LR.fit(X_train, y_train)
    end = datetime.datetime.now()
    train_time = end - start


    y_pred = LR.predict(X_test)
    r2_score = r2(y_test, y_pred)
    mean_squared_error = mse(y_test, y_pred)
    mean_absolute_error = mae(y_test,y_pred)


    print("r2 score: ", r2_score)

    metadata = {
        "feature_group_name" : "energy_consumption_denmark",
        "feature_group_version" : feature_group_version,
        "dataset_name" : dataset_name, 
        "dataset_version" : dataset_version,
        "time_to_train" : train_time.total_seconds(),
        # "r2_score" : r2(y_test, y_pred),
        # "mse_value" : mse(y_test, y_pred),
        # "mae_value" : mae(y_test,y_pred)
    }

    filename = "./data/metadata/models/" + metadata["dataset_name"] + "_" + str(metadata["dataset_version"]) + ".json"
    utils.save_json(metadata, file_name=filename)
    return LR, metadata
    

def pickle_save_model(model, model_path: str):

    return pickle.dump(model, open(model_path, 'wb'))

def run():

    model, metadata = linear_regression("linear_regression", 1)
    model_name = "./data/models/" + metadata["dataset_name"] + "_" + str(metadata["dataset_version"]) + ".pkl"
    pickle_save_model(model, model_name)

if __name__=="__main__":
    # fire.Fire(run())
    dataset = utils.create_training_dataset(1)
    print(dataset.info())


