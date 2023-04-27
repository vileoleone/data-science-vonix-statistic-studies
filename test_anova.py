from src.vonixstatisc.models import (
    standardModel,
    compareStandardModel,
    compareStandardModelMetrics,
)
from src.vonixstatisc.functions import metricFunctions, comparison_striplot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# dataset_1 = ["a", "a", "b", "b"]
""" dataset_2 = {
    "1140": [
        36, 56, 74, 55, 77, 92, 186, 14, 50, 71, 64, 86, 984
    ],
    "data_to_predict": [
        63, 32, 104, 178, 72, 29, 62, 13, 53, 16, 93
    ],
}

d = compareStandardModel(dataset_2)
print(d)


""" compareStandardModelMetrics(
    "1003",
    dataset_2["1003"],
    dataset_2["queue"],
    data_to_predict=dataset_2["data_to_predict"],
)
 """ """