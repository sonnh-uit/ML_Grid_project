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
import time
from utils import utils


def model_deploy(model_config: dict):
    
    model_root_directory = "./data/models/"
    model_path = model_root_directory + model_config['name'] + ".pkl"
    train_result_path = model_root_directory + model_config['name'] + ".json"
    evaluate_result_path = model_root_directory + model_config['name'] + "_eval.json"

    train_result = utils.load_json(train_result_path)
    evaluate_result = utils.load_json(evaluate_result_path)
    model_metric = {**train_result, **evaluate_result}


    PROJECT_NAME = utils.load_env_vars()["WANDB_PROJECT"]
    run = wandb.init(project=PROJECT_NAME)

    model = wandb.Artifact(
        model_config['name'],
        type = "model",
        description = model_config['model_description'],
        metadata = model_metric,
    )

    model.add_file(model_path)
    run.log_artifact(model)
    run.finish()


def run(model: dict):
    # ARIMA MODEL
    utils.wandb_login()
    model_deploy(model)
 
if __name__=="__main__":
    models = utils.load_yaml_env()
    for model in models['model_training']:
        # if model['name'].startswith('arima'):
        fire.Fire(run(model))
        time.sleep(30)

