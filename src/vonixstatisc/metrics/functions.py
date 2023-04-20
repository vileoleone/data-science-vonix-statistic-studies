import numpy as np
from collections import OrderedDict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def z_clean_outliers(data):
    outliers = {}
    clean_dataset = {}
    threshold = 3
    handling_time = list(data.values())
    mean = np.mean(handling_time)
    std = np.std(handling_time)

    for period_at, time in data.items():
        z_score = (time - mean) / std
        if np.abs(z_score) > threshold:
            outliers[period_at] = time
            continue

        clean_dataset[period_at] = time
    return [clean_dataset, outliers]


def iq_clean_outliers(data):
    outliers = []
    clean_dataset = []

    [q1, q3] = np.percentile(data, [25, 75])
    iqr_value = q3 - q1
    lower_bound_value = q1 - (1.5 * iqr_value)
    upper_bound_value = q3 + (1.5 * iqr_value)

    for time in data:
        if time > upper_bound_value or time < lower_bound_value:
            outliers.append(time)
            continue
        clean_dataset.append(time)
    return [clean_dataset, outliers]


def transform_object(object, period):
    seconds = period * 60
    arr = []
    beginning = 0
    data_frame_obj = {}
    end = beginning + period

    keys_array = list(object.keys())
    total = len(keys_array)
    last_timestamp = list(object.keys())[total - 1]
    limit = last_timestamp - seconds

    reverse_dict = dict(OrderedDict(reversed(list(object.items()))))

    for key, value in reverse_dict.items():
        # print({"key":key, "limit":limit, 'result' : key >= limit})
        if key >= limit:
            arr.append(value)
            continue

        if key < limit:
            data_frame_obj[f"{beginning}-{end}"] = arr

            arr = []
            arr.append(value)

            beginning += period
            end += period
            limit = key - period

    return data_frame_obj


def transform_array(array, period, min_number, max_number):
    limit = period
    arr = []
    beginning = 0
    data_frame_obj = {}
    end = beginning + period
    sort_data = [time for time in sorted(array) if time >= min_number and time <= max_number]
    for time in sort_data:
        if time <= limit:
            arr.append(time)
            continue

        if time > limit:
            if len(arr) > 0:
                data_frame_obj[limit] = arr

            arr = []
            arr.append(time)

            beginning += period
            end += period
            limit += period

    return data_frame_obj


def histogram_lineplot(data):
    x_plot_array = list(data.keys())
    y_plot_array = [len(data[i]) for i in data]
    data_plot = pd.DataFrame({"period": x_plot_array, "number_of_calls": y_plot_array})
    sns.lineplot(x="period", y="number_of_calls", data=data_plot)
    return plt.show()


def histogram_histplot(data):
    x_plot_array = data
    data_plot = pd.DataFrame({"talk_secs": x_plot_array})
    print(data_plot)
    sns.histplot(data=data_plot, x="talk_secs", kde=True)
    return plt.show()
