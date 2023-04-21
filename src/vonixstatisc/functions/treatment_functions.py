import numpy as np
from collections import OrderedDict


def z_clean_outliers(data: dict) -> list:
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


def iq_clean_outliers(data: list) -> list:
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


def transform_dict(data: dict, period: int) -> dict:
    seconds = period * 60
    arr = []
    beginning = 0
    data_frame_obj = {}
    end = beginning + period

    keys_array = list(data.keys())
    total = len(keys_array)
    last_timestamp = list(data.keys())[total - 1]
    limit = last_timestamp - seconds

    reverse_data = data(OrderedDict(reversed(list(dict.items()))))

    for key, value in reverse_data.items():
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


def transform_array(array: list, period: list, min_time: list, max_time: list):
    limit = period
    arr = []
    beginning = 0
    data_frame_obj = {}
    end = beginning + period
    sort_data = [
        time for time in sorted(array) if time >= min_time and time <= max_time
    ]
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
