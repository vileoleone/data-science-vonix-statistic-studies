import configs
import repository
import matplotlib.pyplot as plt
import functions
import seaborn as sns
import pandas as pd

def histogram(data):
    x_plot = list()
    prepare_data =  {i: [len(data[i])] for i in data}
    return prepare_data

connection_configs = configs.DBConfigs(
    database_manager="mysql",
    user="callcenter",
    password="callcenter",
    hostname="localhost",
    database="callcenter",
    port=3306,
)

connection = connection_configs.connect

repository = repository.CallRepository(connection, "call_table_name")

data = repository.select()

[dataset, outliers] = functions.z_clean_outliers(data)

print(histogram(functions.transform_object(dataset, 60)))

dataframe =pd.DataFrame(histogram(functions.transform_object(dataset, 60)))

print(dataframe)



#sns.distplot(dataset, x = 'average_handling_time', binwidth = 5)


   
    
    