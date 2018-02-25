import pandas as pd
import numpy as np

def r_to_pandas(robj, names=None):
    """
    Reconstruct pandas object from R matrix/vector.
    pandas2ri.ri2py_dataframe does not set labels.
    """
    if names is None:
        try:
            names = robj.names
        except AttributeError:
            names = None if len(robj.shape) == 1 else (None, None)
    data = np.array(robj)
    if len(data.shape) > 2:
        raise NotImplementedError
    if len(data.shape) == 1 or min(data.shape) == 1:
        # 1-dimensional
        return pd.Series(data.flatten(), index=names)
    else:
        # 2-dimensional
        return pd.DataFrame(data,
                            index=names[0], columns=names[1])
