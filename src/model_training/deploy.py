# =========================================
# Date    : 2023-09-24 20:19:20
# Author  : Son Nguyen-Hong (sonnh.uit@gmail.com)
# Link    : sonnh.net
# =========================================

import hsml
import fire
import hopsworks
import hopsworks
import wandb
import random

from utils import utils


def model_deploy(model_path: str, model_metric: dict):
    
    PROJECT_NAME = utils.load_env_vars()["WANDB_PROJECT"]
    run = wandb.init(project=PROJECT_NAME)

    model = wandb.Artifact(
        "first_test_energy_consumer",
        type = "model",
        description = "This is first test for upload model to wandb",
        metadata = model_metric,
    )
    model.add_file(model_path)

    run.log_artifact(model)
    run.finish()


def run():
    # ARIMA MODEL
    # Begin deploy model, model metric must be save as json with just string or number
    utils.wandb_login()
    model_path = "./data/models/arima_1_arima.pkl"

    model_train = utils.load_json("./data/models/arima_1_arima.json")
    model_evaluate = utils.load_json("./data/models/eval_arima_1_arima.json")
    model_metric = {**model_train, **model_evaluate}
    model_version = 1
    model_deploy(model_path, model_metric)
    print(model_metric)
    
    

if __name__=="__main__":
    fire.Fire(run())
