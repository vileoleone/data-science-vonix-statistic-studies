from src.vonixstatisc.configs import DBConfigs
from src.vonixstatisc.repository import CallRepository
from src.vonixstatisc.functions import (
    transform_agents_dict,
    prepare_to_compare
)
from src.vonixstatisc.models.standard_model import compareStandardModel

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
connection_configs = DBConfigs(
    database_manager="mysql",
    user="callcenter",
    password="callcenter",
    hostname="localhost",
    database="callcenter",
    port=3306,
)

connection = connection_configs.connect

data = pd.read_sql()

""" repository = CallRepository(connection, "call_table_name")

data = repository.select_agents(1680566400,1680739200)
queue = repository.select_queue(1680566400,1680739200)
data['queue'] = queue
data_prepare = transform_agents_dict(data, 120)

data_3 = prepare_to_compare(data_prepare, 1680566400,1680739200)

print(data_3)
d = compareStandardModel(data_3)

print(d)


sns.set_theme(style="darkgrid")
sns.stripplot(d, x="period", y="mean", hue="agents", jitter=False)
plt.show() """
