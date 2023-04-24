import numpy as np
from collections import OrderedDict
from datetime import datetime


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


def transform_agents_dict(data:dict, period: int)->dict:
    return_dict = {}
    for agent, value in data.items():
        if len(value) >0:
            return_dict[str(agent)] = transform_dict(value, period)
    return return_dict

def transform_dict(data: dict, period: int) -> dict:
    seconds = period * 60
    arr = []
    return_dict = {}

    keys_array = list(data.keys())
    beginning = keys_array[0]
    end = beginning - seconds

    for key, value in data.items():
        if key >= end:
            arr.append(value)
            continue

        if key < end:
            return_dict[f"{end}"] = arr

            arr = []
            arr.append(value)

            beginning -= seconds
            end -= seconds

    return return_dict


def transform_array(array: list, period: list, min_time: list, max_time: list):
    limit = period
    arr = []
    beginning = 0
    return_dict = {}
    end = beginning + period

    sort_data = [
        time for time in np.sort(array) if time >= min_time and time <= max_time
    ]
   
    for time in sort_data:
        last_time = sort_data[-1]
        if time <= limit:
            arr.append(time)
            

        if time > limit:
            if len(arr) > 0:
                return_dict[limit] = arr

            arr = []
            arr.append(time)

            beginning += period
            end += period
            limit += period
            
        if time == last_time:
            return_dict[limit] = arr
            
    return return_dict

def prepare_to_compare(data: dict, from_period:int, to_period:int)-> dict[str,list]:
    return_obj = {}
    
    for agent, period_array in data.items():
        talk_secs_array = []
        
        if len(period_array) > 0:
            for timestamp, array in period_array.items():
                
                time = int(timestamp)
                if time <= to_period or time > from_period:
                    talk_secs_array.extend(array)
                    
        if len(talk_secs_array) > 0:            
            return_obj[agent] =talk_secs_array 
    return return_obj                