from src.vonixstatisc.models import standardModel, compareStandardModel
from src.vonixstatisc.functions import metricFunctions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#dataset_1 = ["a", "a", "b", "b"]
dataset_2 = {"a":[23, 25, 54, 65], "b":[90, 180, 90, 180]}

d = compareStandardModel(dataset_2)
""" obj = {"agentes": dataset_1, "cv": dataset_2, "period": dataset_3} """
""" model = standardModel(dataset_1, dataset_2)
model_s = model.model() """
# print(model_s)
""" dataset_1 = model.predict_results """
##print(sorted(dataset_1['y_predict']))
# print(len(dataset_1['y_predict']))
""" # print(model.calculate_rsd())
df = pd.DataFrame(obj) """
""" metricFunctions(dataset_1["y_predict"], dataset_1["y_true"], 1).print_table() """
print(df)

#sns.set_theme(style="darkgrid")
#sns.stripplot(df, x="period", y="cv", hue="agentes", jitter=False),
#plt.show()
