# vonixsync

vonixsync is a python library for syncronization/database mirroring of the vonix database

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vonixsync.

```bash
pip install vonixsync
```

## Usage

```python
import vonixsync
from vonixsync import DBConfigs
from vonixsync import Syncronizer

#Import the DBConfigs class. Provide the parameters used to construct the string used to connect to the database, according to its singular dialect.
connection_configs = DBConfigs(
    database_manager="postgres",
    user="postgres",
    password="postgres",
    hostname="localhost",
    database="postgres",
    port=5432,
)

connection = connection_configs.connect

# Declare your token as a string type
token = "token_provided_by_vonix_support"

#Import the Syncronizer Class to effectively syncronize the data to your database and name all tables 
Syncronizer(
    
    token=token,
    
    connection=connection,

    agents="agent",
    agent_event = "agent_event",
    agent_pause="agent_pause",
    agent_summary="agent_summary",
    
    calls="call",
    call_ratings="call_rating",
    
    chats="chat",
    chat_message="chat_message",
    
    profilers="profiler",
    trees="trees",
    
    queues="queue",
    queue_summary= "queue_summary",
    
    fromPeriod=1678449585,
    
    echo=True

).syncronize()

```
Now run the code.
#
## Syncronizer Options

Besides the obligatory token, database_string parameters and names of the tables to be syncronized, the Syncronizer has other options:
#
### fromPeriod
#
The timestamp parameter must be declared in timestamp format. It is an obligatory filter for the summary tables.

- the syncronizer will look for the most recent inserted row in the mirrored database and mirror from this row's date on. 

- If no data is found in the mirrored database the syncronizer will mirror data using the fromPeriod timestamp value provided to the Syncronizer.

- If no timestamp parameter was provided, the Syncronizer will use the timestamp from the day before the current date.

```python
Syncronizer(token, database, agents= "agent", fromPeriod = 1679067723 ).syncronize()
```
#
### echo
#
The echo parameter by default is False. But if declared as True, it will enable the logging of all SQL commands during the active phase of the syncronizer.
This a feature provided by the SQLAlchemy library. It can be set with or without other optional parameters.

```python
Syncronizer(token, database, queues = "queue", echo = True ).syncronize()
```