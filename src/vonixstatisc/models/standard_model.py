from ..metrics import transform_array
import numpy as np

class StandardModel:
    def construct_model(self, data: list[int]):
        data_tr = transform_array(data, 90, 8, 5400)
        obj_model =  {i: round(np.mean(data_tr[i])) for i in data_tr}
        
        return obj_model

    def predict_response(self, data: dict[int, int]):
        pass
