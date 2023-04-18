import configs
import repository
import matplotlib.pyplot as plt
import functions
import seaborn as sns
import pandas as pd

def period_histogram(data):
    x_plot_array = list(data.keys())
    y_plot_array = [len(data[i]) for i in data]
    data_plot = pd.DataFrame({"period": x_plot_array, "number_of_calls": y_plot_array})
    
    sns.lineplot(x = "period", y = "number_of_calls", data=data_plot)
    return plt.show()

def dis

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

period_histogram(functions.transform_object(dataset, 120))




#sns.distplot(dataset, x = 'average_handling_time', binwidth = 5)


   
    
    