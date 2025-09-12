from py_agata import time_in_ranges, variability
import numpy as np
import pandas as pd

def agp_analysis(trace: pd.DataFrame):
    """
    This function provides the main AGP metrics of a given glucose trace.
    @param trace:
        a Pandas dataframe with a column `glucose`
    @returns:
        a dictionary with the main glucose metrics
    """
    trace["t"] = pd.to_datetime(trace["t"]) #convert timestamps from string to datetime

    #Compute metrics using py_agata functions
    tir = time_in_ranges.time_in_target(trace, glycemic_target="diabetes")
    tar1 = time_in_ranges.time_in_l1_hyperglycemia(trace, glycemic_target="diabetes")
    tar2 = time_in_ranges.time_in_l2_hyperglycemia(trace, glycemic_target="diabetes")
    tbr1 = time_in_ranges.time_in_l1_hypoglycemia(trace, glycemic_target="diabetes")
    tbr2 = time_in_ranges.time_in_l2_hypoglycemia(trace, glycemic_target="diabetes")
    glucose_variability = variability.cv_glucose(trace)

    return {"tir": tir, "tar1": tar1, "tar2": tar2, "tbr1": tbr1, "tbr2": tbr2, "glucose_variability": glucose_variability}


