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
stmt = "select agent_id, queue_id, direction, locality_id, call_type_id, hold_secs, ring_secs, initial_position, trunking_id, carrier_id, DATE_FORMAT(created_At, '%w') as 'week_day', DATE_FORMAT(created_At, '%M') as 'month', DATE_FORMAT(created_At, '%Y-%d-%m') as 'date', DATE_FORMAT(created_At, '%H:%m:%s') as 'day_time', created_at as 'datetime',  UNIX_TIMESTAMP(created_at) as 'timestamp', talk_secs as handling_time from calls where talk_secs > 0 and talk_secs < 200 and agent_id IS NOT NULL;"
data = pd.read_sql(stmt, connection)

data.to_csv('src/vonixstatisc/data/pandas_data/data_fluency_queue_200.csv', index = False, encoding='utf-8')