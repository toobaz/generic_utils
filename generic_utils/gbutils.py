import numpy as np
from subprocess import Popen, PIPE, check_output
import sys

TOOLS = ['acorr', 'bin', 'boot', 'convtable', 'dist', 'dummyfy', 'env',
'filternear', 'fun', 'gcorr', 'get', 'glreg', 'grid', 'hill', 'histo',
'histo2d', 'interp', 'ker', 'ker2d', 'kreg', 'kreg2d', 'lreg', 'mave', 'modes',
'mstat', 'near', 'nlmult', 'nlpanel', 'nlpolyit', 'nlprobit', 'nlqreg',
'nlreg', 'plot', 'quant', 'rand', 'stat', 'test', 'xcorr']


class GBCommand:
    """
    Run gbutils tool on numpy arrays.
    
    Example:
    
    import numpy as np
    from gbutils import gbglreg, gbkreg
    from matplotlib import pyplot as plt
    
    x = np.arange(100)
    y = x ** 2 - 10
    
    coeff, stderr = gbglreg(x, y, O=1)
    
    plt.plot(*gbkreg(x, y).transpose())
    """
    def __init__(self, execname):
        self.execname = execname
        self._doc = None

    def __call__(self, *args, **kwargs):
        kwargstr = {('-%s' % var) : str(kwargs[var]) for var in kwargs}
        kwargslist = [i for k_v in kwargstr.items() for i in k_v]
        
        proc = Popen([self.execname] + kwargslist,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE,
                     env={'LANG' : 'C'})

        np.savetxt(proc.stdin, np.column_stack(args))

        proc.stdin.close()
        
        res = np.loadtxt(proc.stdout)

        return res

    def doc(self):
        """
        Load and print documentation for the tool.
        """
        # Setting __doc__ of a single instance is useless (see PEP 257)
        if self._doc is None:
            self._doc = check_output([self.execname, '-h']).decode('utf-8')
        print(self._doc)

for tool in TOOLS:
    gbtool = 'gb%s' % tool
    setattr(sys.modules[__name__], gbtool , GBCommand(gbtool))
