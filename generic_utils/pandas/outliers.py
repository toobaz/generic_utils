import pandas as pd
import numpy as np


def _condition_extreme(based_on, tails):
    quants = based_on.quantile([tails, 1-tails])
    return (based_on >= quants.iloc[0]) & (based_on <= quants.iloc[1])

def filter_extreme(data, based_on=None, tails=0.01):
    """
    Filter away extreme observations.
    "based_on" can be
    - a 1d object of same length than "data"
    - if "data" is a DataFrame, a key specifiying a column
    - a list of the above to filter on multiple variables.

    Return data excluding "tail"% extreme observations on each side on given
    column in df, on both sides.
    
    """
    if based_on == None:
        based_on = [data]
    elif not isinstance(based_on, list):
        based_on = [based_on]

    condition = pd.Series(True, index=data.index)
    for sub_cond in based_on:
        if isinstance(based_on, np.ndarray):
            based_on_s = pd.Series(based_on, index=data.index)
        elif not isinstance(based_on, pd.Series):
            based_on_s = data[sub_cond]
        condition &= _condition_extreme(based_on_s, tails)

    return data.loc[condition]

pd.DataFrame.filter_extreme = filter_extreme
pd.Series.filter_extreme = filter_extreme
