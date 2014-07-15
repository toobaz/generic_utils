# -*- coding: utf-8 -*-

import scipy

from collections import OrderedDict

class Tablerone(object):
    def __init__(self, summ=None, **kwargs):
        self._models = []
        if summ:
            self.add(summ, **kwargs)
    
    def format_name(self, name, substs={}):
        if name in substs:
            name = substs[name]
        else:
            name = str(name).replace('_', '\\_')
        
        return name
    
    def add(self, res, label='', stub_names=None):
        
        names = res.params.index
         
        sum_dict = {"obs_num"   : res.nobs,
                    "depvar"    : res.model.formula.split('~')[0].strip(),
                    "rsq"       : res.rsquared,
                    "label"     : label,
                    "variables" : OrderedDict()
                   }
        
        for idx, name in enumerate(names):
            varname = names[idx]
            if isinstance(stub_names, dict):
                if name in stub_names:
                    varname = stub_names[varname]
            elif (hasattr(stub_names, '__len__') and len(stub_names) > idx
                                             and stub_names[idx]):
                varname = stub_names[idx]
            
            vardict = {"name"   : varname,
                       "coeff"  : res.params[varname],
                       "stderr" : res.bse[varname],
                       "tval"   : res.tvalues[varname],
                       "pval"   : res.pvalues[varname]}
            
            sum_dict["variables"][varname] = vardict
        
        self._models.append(sum_dict)
    
    def table(self, show_depvar=True, dep_var_names={}, stub_names=None,
                    stub_positions=None):
        """
        @show_depvar: if True, shows the dependent variable (once if is always
        the same, on each column/group of columns otherwise.
        """
        # TODO: does it?
        
        sum_dict = self._models[0]
        cells_str = "c" * len(self._models)
        t = ('\\begin{tabular}'
             '{@{\\extracolsep{5pt}}l%s}\n \\\\') % cells_str
        t += ('[-1.8ex]\\hline\n'
              '\\hline \\\\[-1.8ex]\n')
        if show_depvar:
            if len(set([model["depvar"] for model in self._models])) == 1:
                # There is only one dependent variable - show it on same line:
                t += (' & \\multicolumn{%d}{c}'
                      '{\\textit{Dependent variable: %s}}'
                      ' \\\\ \n') % (len(cells_str),
                                     self.format_name(model["depvar"],
                                                      substs=dep_var_names))
            else:
                depvars = " & ".join([self.format_name(mod["depvar"],
                                      substs=dep_var_names) for mod in self._models])
                t += (' & \\multicolumn{%d}{c}'
                      '{\\textit{Dependent variable:}}'
                      ' \\\\ \n'
                      '\\cline{2-%d}\n \\\\'
                      '[-1.8ex] & %s \\\\ \n') % (len(cells_str),
                                                    len(cells_str) + 1,
                                                    depvars)
        
        labels = [self.format_name(model["label"]) for model in self._models]
        if any(labels):
            t += ' & %s \\\\ \n' % "&".join(labels)
        
        t += '\\hline \\\\[-1.8ex] \n'
        
        # Collect all appearing variables (identified by name)
        model = self._models[0]
        variables = [var["name"] for var in model["variables"].values()]
        for model in self._models[1:]:
            # Unfortunately there is no OrderedSet...
            for variable in model["variables"]:
                if not variable in variables:
                    variables.append(model["variables"][variable]["name"])

        if stub_positions:
            # Remove from list:
            removed = []
            for varname in stub_positions:
                if varname in variables:
                    variables.remove(varname)
                    removed.append(varname)
            
            # Put them back in the right order, processing them already ordered
            # by position;
            for var, pos in sorted(stub_positions.iteritems(),
                                   key=lambda v_p : v_p[1]):
                if var in removed:
                    variables.insert(pos, var)
        
        for idx, varname in enumerate(variables):
            coeff_txts = []
            pval_txts = []
            for model in self._models:
                if varname in model["variables"]:
                    vardict = model["variables"][varname]
                    asteriscs = ''
                    for threshold in (0.1, 0.05, 0.01):
#                        print(varname, vardict["pval"], threshold, vardict["pval"] < threshold)
                        if vardict["pval"] < threshold:
                            asteriscs += '*'
                        else:
                            break                
                    if asteriscs:
                        asteriscs = '^{%s}' % asteriscs
                    vardict["_asteriscs"] = asteriscs
                    coeff_txt = ' $%(coeff)0.3f%(_asteriscs)s$ ' % vardict
                    coeff_txts.append(coeff_txt)
                    pval_txts.append(' (%(stderr)0.3f) ' % vardict)
                else:
                    coeff_txts.append('')
                    pval_txts.append('')
            
            if isinstance(stub_names, dict):
                if varname in stub_names:
                    varname = stub_names[varname]
            elif (hasattr(stub_names, '__len__') and len(stub_names) > idx
                                             and stub_names[idx]):
                
                varname = stub_names[idx]
            
            t += "%s & " % self.format_name(varname)
            t += "&".join(coeff_txts)
            t += "\\\\ \n"
            t += " & "
            t += "&".join(pval_txts)
            t += "\\\\ \n "
                
        t += '\\hline \\\\[-1.5ex] \n '
        rsq_txts = [" $%(rsq)0.3f$ " % model for model in self._models]
        obs_num_txts = [" $%(obs_num)d$ " % model for model in self._models]
        
        t += 'R$^2$ & %s \\\\ \n' % "&".join(rsq_txts)
        t += 'Observations & %s \\\\ \n' % "&".join(obs_num_txts)
        
        t += '\\hline \\\\[-1.5ex] \n '
        t += '\\end{tabular}\n'
        return t

