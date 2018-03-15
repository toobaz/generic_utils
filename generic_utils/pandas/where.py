import pandas as pd
from types import MethodType

ATTRIBUTES = {'loc', 'iloc', 'ix', 'index', 'shape', 'values'}

def _operator(op):
    def func(self, *args, **kwargs):
        operations = self._operations + [(op, args, kwargs)]
        return Where(operations)
    return func

class Where(object):
    """
    Usage examples:

    from generic_utils.pandas.where import where as W
    df = pd.DataFrame([[1, 2, True],
                       [3, 4, False], 
                       [5, 7, True]],
                      index=range(3), columns=['a', 'b', 'c'])
    # On specific column:
    print(df.loc[W['a'] > 2])
    print(df.loc[-W['a'] == W['b']])
    print(df.loc[~W['c']])

    # On entire  - or subset of a - DataFrame:
    print(df.loc[W.sum(axis=1) > 3])
    print(df.loc[W[['a', 'b']].diff(axis=1)['b'] > 1])

    # Reusable conditions:
    increased = (W['a'] > W.loc[0, 'a']) | (W['b'] > W.loc[0, 'b'])
    print("Increased:\n", df.loc[increased])
    print("Decreased:\n", (-df).loc[increased])

    # Filter based on index:
    to_keep = ((W.index % 3 == 1) &
               (W.index % 2 == 1))
    print("Non-multiples:\n", df.loc[to_keep])
    """

    def __init__(self, operations=[]):
        self._operations = operations

    def __getattr__(self, attr):
        if attr in ATTRIBUTES:
            # Just transform this into something callable, for uniformity:
            return Where(self._operations + [('__getattribute__',
                                             (attr,), {})])
        return MethodType(_operator(attr), self)

    def _evaluate(self, obj):
        res = obj
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
           'add', 'sub', 'mul', 'floordiv', 'truediv', 'pow',
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

where = Where()
