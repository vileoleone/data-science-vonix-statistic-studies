import numpy as np
import pandas as pd
from ...models import StandardModel
from ..metrics_function import MetricFunctions


def z_clean_outliers(data:list) -> list:
    """method to clean outliers of dict
    { 90: [12,24,56,12], 180: [165,235,12,9], ... interval of three minutes}
    for standard model based on z-score method"""

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
    return clean_dataset


def iq_clean_outliers(data: list) -> list:
    """method to clean outliers of dict
    { 90: [12,24,56,12], 180 [165,235,12,9], ... interval of three minutes}
    for standard model based on interval quarterlines method"""

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


def transform_array(array: list, interval: list, min_time: list, max_time: list):
    """Used inside StandardModel : loops using transform_dict to create dicts for the standard model
     - receives array [talk_secs from a chosen 15min, 30min 1hr period] ex : [194,30303,21,1,0,3,1231,6547,8869]
     - for standard model, interval = 180 secs, min_time = 8 secs, max_time = 5400 secs
     - filters data between min and max time [194,503,21,1231]
    {180: [21,194], 360 [303], ... interval of three minutes}"""

    limit = interval
    arr = []
    beginning = 0
    return_dict = {}
    end = beginning + interval

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

            beginning += interval
            end += interval
            limit += interval

        if time == last_time:
            return_dict[limit] = arr

    return return_dict


def transform_agents_dict(data: dict, period: int) -> dict:
    """loops using transform_dict to create dicts for each agent in the data dict
    {agent: {last_timestamp: [12,24,56,12, 90, 100], last_timestamp - period:[195,235,201,300], ... interval of three minutes for standard model}}
    """

    return_dict = {}
    for agent, value in data.items():
        if len(value) > 0:
            return_dict[str(agent)] = transform_dict(value, period)
    return return_dict


def transform_dict(data: dict, period: int) -> dict:
    """method that receives dict from database query
    {start_at(timestamp): talk_secs(seconds), ...} and create
    another dict based on the period (15, 30, 1hr) chosen
    {last_timestamp: [12,24,56,12, 90, 100], last_timestamp - period:[195,235,201,300], ... interval of three minutes for standard model}
    For standard model the data from the last period( 15 min, 30 min, 1h) is used to construct forecast for the next period so the return_dict begins with the last timestamp to the first
    """

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


def prepare_to_compare(data: dict, from_period: int, to_period: int) -> dict[str, list]:
    """prepare dict from transform_agents_dict to format that can be used in prepare_to_compare function.
    Aggregates all talk secs from a chosen period of a timestamp. to a dict
    {agent: [talk_secs...]}"""

    return_obj = {}

    for agent, tals_secs_array in data.items():
        talk_secs_array = []

        if len(tals_secs_array) > 0:
            for timestamp, array in tals_secs_array.items():
                time = int(timestamp)
                if time <= to_period or time > from_period:
                    talk_secs_array.extend(array)

        if len(talk_secs_array) > 0:
            return_obj[agent] = talk_secs_array
    return return_obj


def compareStandardModel(data: dict[str, list]) -> dict:
    """Generates Standard Model dataframe for comparison of differents agents and possibly queue"""

    rsd_dict = {}
    agents = []
    rsd = []
    period = []
    mean = []
    number_of_samples = []
    for agent, array_data_train in data.items():
        model = StandardModel(data_train=array_data_train, data_predict=[])
        model_count = model.count_samples()
        model_rsd = model.calculate_rsd()
        model_mean = model.model()

        agents.extend([str(agent)] * len(model_mean.values()))
        rsd.extend(list(model_rsd.values()))
        period.extend(list(model_rsd.keys()))
        mean.extend(list(model_mean.values()))
        number_of_samples.extend(list(model_count.values()))

    rsd_dict["agents"] = agents
    rsd_dict["rsd"] = rsd
    rsd_dict["period"] = period
    rsd_dict["mean"] = mean
    rsd_dict["number_of_samples"] = number_of_samples
    return pd.DataFrame(rsd_dict)


def compareStandardModelMetrics(agent:str, agent_data_train: list, queue_data_train: list, data_to_predict: list) -> dict:
    """Generates Standard Models of an agent and the correponding queue for comparison of the metrics generated for a given period of time"""

    rsd_dict = {}

    agent_data_model = StandardModel(
        data_train=agent_data_train, data_predict=data_to_predict
    ).predict_results
    agent_metrics = MetricFunctions(
        agent, agent_data_model["y_predict"], agent_data_model["y_true"], 1
    )

    queue_data_model = StandardModel(
        data_train=queue_data_train, data_predict=data_to_predict
    ).predict_results
    queue_metrics = MetricFunctions(
        "queue", queue_data_model["y_predict"], queue_data_model["y_true"], 1
    )

    agent_metrics.print_table()
    queue_metrics.print_table()

    return pd.DataFrame(rsd_dict)
