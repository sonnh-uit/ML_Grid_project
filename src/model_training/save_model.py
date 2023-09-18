import hsml
import fire
import hopsworks
import hopsworks
import pickle 


from utils import utils

def save_model(model_path: str, model_name: str, model_version: int):
    #  = utils.hopsworks_model_registry_login()
    pickle.dump(rf, open(model_path, "wb"))
    # connection = hsml.connection()
    mr = utils.hopsworks_model_registry_login()
    model_artifact = hsml.model.load_model_artifact(model_path)
    mr.save_model_artifact(model_artifact, model_name, model_version)
    connection.close()

def run():

    model_path = "./data/models/arima_1_arima.pkl"
    model_name = "test_arima_same_model"
    model_version = 1
    save_model(model_path,model_name,model_version)

if __name__=="__main__":
    fire.Fire(run())