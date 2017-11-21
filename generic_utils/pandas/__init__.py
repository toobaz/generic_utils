import pandas as pd

# Stands for "WhatEver", for indexing with nested slicing
WE = slice(None)

def pd_fill_diagonal(df, value):
    idces = df.index.intersection(df.columns)
    stacked = df.stack(dropna=False)
    stacked.update(pd.Series(value,
                             index=pd.MultiIndex.from_arrays([idces,
                                                              idces])))
    df.loc[:, :] = stacked.unstack()

def invert_series(s):
    return pd.Series(s.index, index=s.values,
                     name=s.index.name).rename_axis(s.name)

def loc_single_value_as_slice(obj, value):
    """
    Retrieve all rows corresponding to given value.
    Work around GH #9519 (behavior depends on whether "value" appears multiple
    times) without incurring in GH #9466 (.loc[list] slow on non-unique
    indexes).
    """
    if isinstance(obj.index, pd.MultiIndex):
        # GH #9519 does not apply
        return obj.loc[value]
    return obj.loc[obj.index == value]


def convolve_with_index(a, v):
    """
    Like np.convolve, but respects indices of a and v, returning a Series.
    Both a and v must be indexed with integers, and any missing values will be
    filled with zeros.
    """
    
    import numpy as np
    args = [a, v]
    for idx in 0, 1:
        s = args[idx]
        assert(isinstance(s.index,
                          (pd.Int64Index,
                           pd.RangeIndex))), ("Input number {} has index of "
                                              "class {}".format(idx,
                                                            s.index.__class__))
        if not(s.index.is_monotonic_increasing and
               len(s) == s.index.max() - s.index.min() + 1):
            args[idx] = s.reindex(range(s.index.min(),
                                        s.index.max() + 1),
                                  fill_value=0)
    
    out_idx = pd.RangeIndex(sum((s.index.min() for s in args)),
                            sum((s.index.max() for s in args)) + 1)
    return pd.Series(np.convolve(*args), index=out_idx)


def outer_sum(s1, s2):
    """
    Sum two series, implicitly replacing missing elements in either with 0.
    """
    new_idx = s1.index.union(s2.index)
    return (s1.reindex(new_idx, fill_value=0) +
            s2.reindex(new_idx, fill_value=0))


def reverse_series(s):
    """
    Take any series and invert the order of its data (leaving the index
    untouched).
    """
    res = s.copy()
    res[:] = res.values[::-1]
    return res
