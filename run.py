from src.vonixstatisc.configs import DBConfigs
from src.vonixstatisc.repository import CallRepository

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
stmt = "select agent_id, queue_id, DATE_FORMAT(created_at, '%w') as 'week_day', DATE_FORMAT(created_at, '%H') as 'hour', DATE_FORMAT(created_at, '%i') as 'minute',  UNIX_TIMESTAMP(created_at) as 'timestamp', talk_secs as handling_time from calls where talk_secs > 0 and UNIX_TIMESTAMP(created_at) > 1682370210 and agent_id IS NOT NULL;"
data = pd.read_sql(stmt, connection)

data.to_csv('src/vonixstatisc/data/pandas_data/data_fluency_queue_april_after_24.csv', index = False, encoding='utf-8')