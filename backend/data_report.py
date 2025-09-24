import numpy as np
import pandas as pd

def report(data: pd.DataFrame):
    """
    This function provides the main AGP metrics of a given glucose trace.
    :param data:
        a Pandas dataframe
    :return:
        a dictionary with a report of the main metrics
    """

    # extract columns from dataframe
    time = data["timestamp"].to_numpy()
    heart_rate = data["heart_rate_bpm"].to_numpy()
    steps = data["steps"].to_numpy()
    calories = data["calories"].to_numpy()
    spo2_percentage = data["spo2_percent"].to_numpy()
    stress_level = data["stress_level"].to_numpy()
    sleep_stage = data["sleep_stage"].to_numpy()

    # calculate metrics
    avg_hr = heart_rate.mean()
    total_steps = steps.sum()
    avg_spo2_percentage = spo2_percentage.mean()
    avg_stress_level = stress_level.mean()
    max_stress_level = stress_level.max()
    total_calories = calories.sum()
    vals, count = np.unique(sleep_stage, return_counts=True)

    return {
        "avg_hr": int(avg_hr),
        "total_steps": int(total_steps),
        "avg_spo2_percentage": float(avg_spo2_percentage),
        "avg_stress_level": int(avg_stress_level),
        "max_stress_level": int(max_stress_level),
        "total_calories": int(total_calories),
        "sleep_stage": vals.astype(str).tolist(),
        "sleep_count": count.astype(int).tolist()
    }

