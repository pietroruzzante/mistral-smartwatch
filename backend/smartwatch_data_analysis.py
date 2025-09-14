import numpy as np
import pandas as pd

def report(data: pd.DataFrame):
    """
    This function provides the main AGP metrics of a given glucose trace.
    @param trace:
        a Pandas dataframe
    @returns:
        a dictionary with a report of the main metrics
    """

    time = data["timestamp"].to_numpy()
    heart_rate = data["heart_rate_bpm"].to_numpy()
    steps = data["steps"].to_numpy()
    calories = data["calories"].to_numpy()
    spo2_percentage = data["spo2_percent"].to_numpy()
    stress_level = data["stress_level"].to_numpy()
    sleep_stage = data["sleep_stage"].to_numpy()

    avg_hr = heart_rate.mean()
    total_steps = steps.sum()
    avg_spo2_percentage = spo2_percentage.mean()
    avg_stress_level = stress_level.mean()
    max_stress_level = stress_level.max()
    time_max_stress_level = time[stress_level == max_stress_level]
    total_calories = calories.sum()

    print(f"avg_hr = {avg_hr}")
    print(f"total_steps = {total_steps}")
    print(f"avg_spo2_percentage = {avg_spo2_percentage}")
    print(f"avg_stress_level = {avg_stress_level}")
    print(f"max_stress_level = {max_stress_level}")
    print(f"time_max_stress_level = {time_max_stress_level}")
    print(f"total_calories = {total_calories}")


    return {"avg_hr": avg_hr,
            "total_steps": total_steps,
            "avg_spo2_percentage": avg_spo2_percentage,
            "avg_stress_level": avg_stress_level,
            "total_calories": total_calories
            }
