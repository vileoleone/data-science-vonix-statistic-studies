from src.vonixstatisc.models import standardModel, compareStandardModel
from src.vonixstatisc.functions import metricFunctions
import pandas as pd

dataset_1 = ["a", "a", "b", "b"]
dataset_2 = [23, 25, 54, 65]
dataset_3 = [90, 180, 90, 180]

obj = {"agentes": dataset_1, "cv": dataset_2, "period": dataset_3}
""" model = standardModel(dataset_1, dataset_2)
model_s = model.model() """
# print(model_s)
""" dataset_1 = model.predict_results """
##print(sorted(dataset_1['y_predict']))
# print(len(dataset_1['y_predict']))
# print(model.calculate_rsd())
df = pd.DataFrame(obj)
""" metricFunctions(dataset_1["y_predict"], dataset_1["y_true"], 1).print_table() """
print(df)
