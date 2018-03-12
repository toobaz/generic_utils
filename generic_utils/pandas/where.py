import pandas as pd
from types import MethodType

def _operator(op):
    def func(self, *args, **kwargs):
        self._operations.append((op, args, kwargs))
        return self
    return func

class Where(object):
    """
    Usage examples:

    from generic_utils.pandas.where import Where as W
    df = pd.DataFrame([[1, 2, True],
                       [3, 4, False], 
                       [5, 7, True]],
                      index=range(3), columns=['a', 'b', 'c'])
    # On specific column:
    print(df.loc[W('a') > 2])
    print(df.loc[-W('a') == C('b')])
    print(df.loc[~W('c')])
    # On entire DataFrame:
    print(df.loc[W().sum(axis=1) > 3])
    print(df.loc[W(['a', 'b']).diff(axis=1)['b'] > 1])

    """
    _method = None

    def __init__(self, key=None):
        self._key = key
        self._operations = []

    def __getattr__(self, attr):
        return MethodType(_operator(attr), self)

    def _evaluate(self, obj):
        if self._key is None:
            res = obj
        else:
            res = obj[self._key]
        for method, args, kwargs in self._operations:
            args = list(args)
            for idx, arg in enumerate(args):
                if isinstance(arg, Where):
                    args[idx] = arg._evaluate(obj)
            for key in kwargs:
                if isinstance(kwargs[key], Where):
                    kwargs[key] = kwargs[key]._evaluate(obj)
            res = getattr(res, method)(*args, **kwargs)
        return res

# Since Python checks "hasattr" for these to understand wether an operation is
# supported, the "__getattr__" above is not sufficient:
for op in ('lt', 'le', 'eq', 'ne', 'ge', 'gt',
           'invert',
           'and', 'or', 'xor',
           'add', 'sub', 'mul', 'floordiv', 'truediv', 'pow'
           'mod',
           'neg', 'pos',
           'getitem'):
    op_label = '__{}__'.format(op)
    setattr(Where, op_label, _operator(op_label))


# Monkey patching:
_old_getitem_axis = pd.core.indexing._LocIndexer._getitem_axis
def _new_getitem_axis(self, key, axis=None):
    if isinstance(key, Where):
        new_key = key._evaluate(self.obj)
        return _old_getitem_axis(self, new_key, axis=axis)
    return _old_getitem_axis(self, key, axis=axis)

pd.core.indexing._LocIndexer._getitem_axis = _new_getitem_axis

