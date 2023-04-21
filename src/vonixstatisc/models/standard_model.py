from ..functions import transform_array
import numpy as np
import pandas as pd


class StandardModel:
    def __init__(self, data_train: list[int], data_predict: list[int]) -> None:
        self.__data = data_train
        self.__model = self.__construct_model()
        self.predict_results = pd.DataFrame(self.predict(data_predict))
        self.data_transform = transform_array(self.__data, 90, 8, 5400)
        self.df_result = self.predict_results

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

    def predict(self, data_to_predict) -> dict:
        y_predict = []
        y_true = data_to_predict
        for time in data_to_predict:
            for key, value in self.__model.items():
                if time <= key:
                    y_predict.append(value)
                    break

        return {"y_predict": y_predict, "y_true": y_true}
