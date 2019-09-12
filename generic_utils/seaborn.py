# https://stackoverflow.com/questions/31191063/using-with-sns-set-in-seaborn-plots/37365095
# https://github.com/mwaskom/seaborn/pull/932

"""
Usage example:

with Stylish(font_scale=2):
    sns.kdeplot(x, shade=True)
"""

import matplotlib

class Stylish(matplotlib.rc_context):
    def __init__(self, **kwargs):
        matplotlib.rc_context.__init__(self)
        sns.set(**kwargs)
