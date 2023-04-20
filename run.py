from src.vonixstatisc.configs import DBConfigs
from src.vonixstatisc.repository import CallRepository
from src.vonixstatisc.metrics import (
    z_clean_outliers,
    transform_object,
    histogram_histplot,
)

connection_configs = DBConfigs(
    database_manager="mysql",
    user="callcenter",
    password="callcenter",
    hostname="localhost",
    database="callcenter",
    port=3306,
)

connection = connection_configs.connect

repository = CallRepository(connection, "call_table_name")

data = repository.select()

[dataset, outliers] = z_clean_outliers(data)

print(transform_object(dataset, 120))
