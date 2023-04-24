import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def histogram_lineplot(data: dict) -> None:
    x_plot_array = list(data.keys())
    y_plot_array = [len(data[i]) for i in data]
    data_plot = pd.DataFrame({"period": x_plot_array, "number_of_calls": y_plot_array})
    sns.lineplot(x="period", y="number_of_calls", data=data_plot)
    return plt.show()

def histogram_histplot(data: dict) -> None:
    x_plot_array = data
    data_plot = pd.DataFrame({"talk_secs": x_plot_array})
    print(data_plot)
    sns.histplot(data=data_plot, x="talk_secs", kde=True)
    return plt.show()

def comparison_striplot(data: dict)-> None:
    data_to_plot = pd.DataFrame(data)
    sns.set_theme(style="whitegrid")
    sns.stripplot(data_to_plot, x="period", y="rsd", hue="agents", jitter=False)
    plt.show()
