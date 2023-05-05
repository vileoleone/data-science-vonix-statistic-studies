
fluxo para standard model

```
from src.vonixstatisc.configs import DBConfigs
from src.vonixstatisc.repository import CallRepository
from src.vonixstatisc.functions import transform_agents_dict, prepare_to_compare
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

repository = CallRepository(connection, "call_table_name"

data = repository.select_agents(1680566400,1680739200)
queue = repository.select_queue(1680566400,1680739200)

data['queue'] = queue

data_prepare = transform_agents_dict(data, 15)

data_compare = prepare_to_compare(data_prepare, 1680566400,1680739200)

compareStandardModel(data_compare)
```

Para anàlise de séries temporais:



select IFNULL(agent_id, 0), queue_id, direction, created_at, locality_id, call_type_id, hold_secs, ring_secs, initial_position, trunking_id, carrier_id, talk_secs as handling_time from calls where talk_secs > 0;

select agent_id, queue_id, direction, locality_id, call_type_id, hold_secs, ring_secs, initial_position, trunking_id, carrier_id, DATE_FORMAT(created_At, '%d') as 'day', DATE_FORMAT(created_At, '%M') as 'month', DATE_FORMAT(created_At, '%H') as 'hour', talk_secs as handling_time from calls where talk_secs > 0 and tak_secs < 90 and agent_id IS NOT NULL limit 1;


Estudos realizados

1) Modelagem com series temporais:  Nao foi possivel nenhuma modelagem com ARIMA, HOLSTERWINTER, ou tratamentos estatisticos para series temporais. mesmo utilizando intervalos pequenos ou estudando filtros diferentes para construcao de series temporais observou-se que a complexidade das operacoes e resultados nao viabilizam tais modelagens:

Foi estudado modelagens filtrando/isolando para peridos de 15, 30 1 hora:
- fila
- agente/fila
- agente/fila/periodo(intervalo de tempo para agrupamento de chamadas)
- agente/fila/periodo/intervalo isolado de tempo das chamadas
- agente/fila/periodo/intervalo isolado de tempo das chamadas/dia
- agente/fila/periodo/intervalo isolado de tempo das chamadas/dia-da-semana 
- agente/fila/periodo/intervalo isolado de tempo das chamadas/dia-da-semana 

Em funcao da alta frequencia e da aleatoriedade dos pontos da serie tambem optou-se por trabalhar apenas com medias das chamadas em cada intervalo.

No entanto foi observado que o número de chamadas de agentes menor que 200 segundos representa mais de 80 % das chamadas totais.

// "select agent_id, queue_id, direction, locality_id, call_type_id, hold_secs, ring_secs, initial_position, trunking_id, carrier_id, DATE_FORMAT(created_At, '%w') as 'week_day', DATE_FORMAT(created_At, '%M') as 'month', DATE_FORMAT(created_At, '%Y-%d-%m') as 'date', DATE_FORMAT(created_At, '%H:%m:%s') as 'day_time', created_at as 'datetime',  UNIX_TIMESTAMP(created_at) as 'timestamp', talk_secs as handling_time from calls where talk_secs > 0 and UNIX_TIMESTAMP(created_at) > 1682370210	and agent_id IS NOT NULL;"

// "select agent_id, queue_id, DATE_FORMAT(created_at, '%w') as 'week_day', DATE_FORMAT(created_at, '%H') as 'hour', DATE_FORMAT(created_at, '%i') as 'minute',  UNIX_TIMESTAMP(created_at) as 'timestamp', talk_secs as handling_time from calls where talk_secs > 0 and UNIX_TIMESTAMP(created_at) > 1682370210	and agent_id IS NOT NULL;"