from ..functions import transform_array, metricFunctions
import numpy as np
import pandas as pd

class standardModel:
    def __init__(self, data_train: list[int], data_predict: list[int]) -> None:
        self.__data = data_train
        self.__model = self.__construct_model()
        self.predict_results = self.predict(data_predict)
        self.data_transform = transform_array(self.__data, 90, 8, 5400)
        self.df_result =  pd.DataFrame(self.predict(data_predict))

    def __construct_model(self) -> dict:
        data = transform_array(self.__data, 90, 8, 5400)
        dict_model = {i: round(np.mean(data[i])) for i in data}
        return dict_model

    def calculate_rsd(self):
        data = transform_array(self.__data, 90, 8, 5400)
        dict_rsd = {i: round(np.std(data[i]) / np.mean(data[i]), 3) for i in data}
        return dict_rsd

    def model(self):
        return self.__model

    def count_samples(self):
        data = transform_array(self.__data, 90, 8, 5400)
        dict_model = {i: len(data[i]) for i in data}
        return dict_model

    def predict(self, data_to_predict) -> dict:
        y_predict = []
        y_true = data_to_predict
        for time in data_to_predict:
            for three_minute_interval, mean in self.__model.items():
                if time <= three_minute_interval:
                    y_predict.append(mean)
                    break

        return {"y_predict": y_predict, "y_true": y_true}


def compareStandardModel(data: dict[str, list]) -> dict:
    rsd_dict = {}
    agents = []
    rsd = []
    period = []
    mean = []
    number_of_samples = []
    for agent, array_data_train in data.items():
        
        model = standardModel(data_train=array_data_train, data_predict=[])
        model_count = model.count_samples()
        model_rsd = model.calculate_rsd()
        model_mean = model.model()
        
        agents.extend([str(agent)] * len(model_mean.values()))
        rsd.extend(list(model_rsd.values()))
        period.extend(list(model_rsd.keys()))
        mean.extend(list(model_mean.values()))
        number_of_samples.extend(list(model_count.values()))

    rsd_dict["agents"] = agents
    rsd_dict["rsd"] = rsd
    rsd_dict["period"] = period
    rsd_dict["mean"] = mean
    rsd_dict["number_of_samples"] = number_of_samples
    return pd.DataFrame(rsd_dict)

def compareStandardModelMetrics(agent, agent_data_train: list, queue_data_train: list, data_to_predict: list)-> dict:
    rsd_dict = {}

    agent_data_model = standardModel(data_train= agent_data_train, data_predict = data_to_predict).predict_results
    agent_metrics = metricFunctions(agent,  agent_data_model['y_predict'], agent_data_model['y_true'], 1)    
    
    queue_data_model =  standardModel(data_train=queue_data_train, data_predict=data_to_predict).predict_results
    queue_metrics = metricFunctions('queue', queue_data_model['y_predict'], queue_data_model['y_true'], 1)  
    
    agent_metrics.print_table()
    queue_metrics.print_table()
    
    return pd.DataFrame(rsd_dict)