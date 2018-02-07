import pandas as pd
import numpy as np


def filter_extreme(data, based_on=None, tails=0.01):
    """
    Filter away extreme observations.
    "based_on" can be a 1d object of same length than "data", or, if "data" is
    DataFrame, a key specifiying a column.

    Return binary mask which excludes "tail" % extreme observations on each
    side on given column in df, on both sides.
    
    """
    if based_on == None:
        based_on = data
    elif isinstance(based_on, np.ndarray):
        based_on = pd.Series(based_on, index=data.index)
    elif not isinstance(based_on, pd.Series):
        based_on = data[based_on]

    quants = based_on.quantile([tails, 1-tails])
    return data.loc[(based_on >= quants.iloc[0]) &
                    (based_on <= quants.iloc[1])]

