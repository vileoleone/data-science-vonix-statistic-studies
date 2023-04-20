from ..metrics import transform_array
import numpy as np

class StandardModel():
    def __init__(self, data_train: list[int], data_predict: list[int] ):
        self.__data = data_train
        self.__model = self.__construct_model(self.__data)
        self.__data_predict = data_predict
        
    def __construct_model(self, data):
        data_tr = transform_array(data, 90, 8, 5400)
        obj_model =  {i: round(np.mean(data_tr[i])) for i in data_tr}
        return obj_model
    
    def model(self):
        return  self.__model
    
    def __predict(self, model, data_to_predict ):
        
