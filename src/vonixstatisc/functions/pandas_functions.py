""" import pandas as pd
connection = ''
stmt = "select agent_id, queue_id, direction, locality_id, call_type_id, hold_secs, ring_secs, initial_position, trunking_id, carrier_id, DATE_FORMAT(created_At, '%d') as 'day', DATE_FORMAT(created_At, '%M') as 'month', DATE_FORMAT(created_At, '%H') as 'hour', talk_secs as handling_time from calls where talk_secs > 0 and agent_id IS NOT NULL;"
data = pd.read_sql(stmt, connection)

data.to_csv('/Users/victoroliveira/Desktop/vonix-py-statistic/src/vonixstatisc/data/data_fluency_queue.csv', index = False, encoding='utf-8')

 """