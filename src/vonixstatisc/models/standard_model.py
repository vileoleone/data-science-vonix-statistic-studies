import numpy as np
import pandas as pd
from ..functions.standard_model.treatment_functions import transform_array


class StandardModel:

    """Standard model used currently for forecasting of average handling time"""

    def __init__(self, data_train: list[int], data_predict: list[int]) -> None:
        self.__data = data_train
        self.__model = self.__construct_model()
        self.predict_results = self.predict(data_predict)
        self.data_transform = transform_array(self.__data, 90, 8, 5400)
        self.df_result = pd.DataFrame(self.predict(data_predict))

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
