from ..configs import DBconnectionHandler

from sqlalchemy import text

from sqlalchemy import (
    Column,
    Table,
    Integer,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()


class CallRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("call_id", VARCHAR(128), primary_key=True),
            Column("queue_id", VARCHAR(128), primary_key=True, index=True),
            Column("direction", VARCHAR(12)),
            Column("offers", Integer, default=0),
            Column("caller_id", VARCHAR(30), index=True),
            Column("caller_info", VARCHAR(30)),
            Column("hold_secs", Integer, default=0),
            Column("talk_secs", Integer, default=0),
            Column("ring_secs", Integer, default=0),
            Column("status", VARCHAR(16), index=True),
            Column("status_cause", VARCHAR(255)),
            Column("locality", VARCHAR(256), default=""),
            Column("call_type", VARCHAR(256)),
            Column("trunking", VARCHAR(256)),
            Column("carrier", VARCHAR(256)),
            Column("exit_key", Integer),
            Column("initial_position", Integer),
            Column("abandon_position", Integer),
            Column("start_time", DateTime, index=True),
            Column("answer_time", DateTime),
            Column("hangup_time", DateTime),
            Column("transferred_to", VARCHAR(255)),
            Column("agent_id", Integer, index=True),
        )

    def select_queue(self, from_period=0, to_period=None):
        if to_period is None:
            stmt = f"SELECT talk_secs, UNIX_TIMESTAMP(start_time) as time_at FROM {self.__table_name} WHERE talk_secs > 0 ORDER BY time_at DESC LIMIT 1;"
            with self.__database as db:
                for row in db.session.execute(text(stmt)):
                    to_period = row._mapping.time_at
            db.session.commit()

        with self.__database as db:
            stmt = f"SELECT talk_secs, UNIX_TIMESTAMP(start_time) as time_at FROM {self.__table_name} WHERE talk_secs > 0 AND UNIX_TIMESTAMP(start_time) BETWEEN {from_period} AND {to_period} ORDER BY time_at DESC;"
            arr = {}
            for row in db.session.execute(text(stmt)):
                arr[row._mapping.time_at] = row._mapping.talk_secs
            db.session.commit()
            return arr
    
    def select_agents(self, from_period=0, to_period=None):
        list_agents = []
        stmt_list_agents = f"select distinct agent_id from {self.__table_name} where agent_id IS NOT NULL;"
        if to_period is None:
            stmt = f"SELECT talk_secs, UNIX_TIMESTAMP(start_time) as time_at FROM {self.__table_name} WHERE talk_secs > 0 ORDER BY time_at DESC LIMIT 1;"
            
            with self.__database as db:
                for row in db.session.execute(text(stmt)):
                    to_period = row._mapping.time_at
            db.session.commit()
            
        with self.__database as db:
            dict_from_db = {}

            for row in db.session.execute(text(stmt_list_agents)):
                list_agents.append(row._mapping.agent_id)
            for agent in list_agents:
                agent_dict = {}
                stmt = f"SELECT talk_secs, UNIX_TIMESTAMP(start_time) as time_at FROM {self.__table_name} WHERE agent_id = {agent} AND talk_secs > 0 AND UNIX_TIMESTAMP(start_time) BETWEEN {from_period} AND {to_period} ORDER BY time_at DESC;"
                for row in db.session.execute(text(stmt)):
                    agent_dict[row._mapping.time_at] = row._mapping.talk_secs
                dict_from_db[agent] = agent_dict

            db.session.commit()
            return dict_from_db
