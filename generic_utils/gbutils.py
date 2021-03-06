import numpy as np
from subprocess import Popen, PIPE, check_output
import sys
import errno

TOOLS = {
'gb' : ('acorr', 'bin', 'boot', 'convtable', 'dist', 'dummyfy', 'env',
'filternear', 'fun', 'gcorr', 'get', 'glreg', 'grid', 'hill', 'histo',
'histo2d', 'interp', 'ker', 'ker2d', 'kreg', 'kreg2d', 'lreg', 'mave', 'modes',
'mstat', 'near', 'nlmult', 'nlpanel', 'nlpolyit', 'nlprobit', 'nlqreg',
'nlreg', 'plot', 'quant', 'rand', 'stat', 'test', 'xcorr'),
'subbo' : ('afish', 'fit', 'agen', 'fish', 'fit', 'gen', 'lafit', 'show')}


class GBCommand:
    """
    Run gbutils tool on numpy arrays.
    
    Example:
    
    import numpy as np
    from gbutils import gbglreg, gbkreg
    from matplotlib import pyplot as plt
    
    x = np.arange(100)
    y = x ** 2 - 10
    
    coeff, stderr = gbglreg(x, y, 'w', O=1)
    
    plt.plot(*gbkreg(x, y).transpose())
    """
    def __init__(self, execname):
        self.execname = execname
        self._doc = None

    def __call__(self, *args, **kwargs):
        args = list(args)
        argstr = [('-%s' % args.pop(idx)) for idx, arg in enumerate(args)
                  if isinstance(arg, str)]

        kwargstr = {('-%s' % var) : str(kwargs[var]) for var in kwargs}
        kwargslist = [i for k_v in kwargstr.items() for i in k_v]

        proc = Popen([self.execname] + argstr + kwargslist,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE,
                     env={'LANG' : 'C'})

        try:
            np.savetxt(proc.stdin, np.column_stack(args))
            proc.stdin.close()
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise
            print("Broken pipe")
        
        err = proc.stderr.read().decode('utf-8')
        if err:
            print("Error %s" % err)

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

for family in TOOLS:
    for tool in TOOLS[family]:
        gbtool = '%s%s' % (family, tool)
        setattr(sys.modules[__name__], gbtool , GBCommand(gbtool))
