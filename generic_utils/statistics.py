#-*- coding:utf-8 -*-

import numpy
numpy.set_printoptions(precision=4, suppress=True)
from statsmodels.stats.sandwich_covariance import cov_cluster

def robust_reg(fit_result, dataframe, cluster_field):
    # Fails: 
    #clustered = cov_cluster(fit, dfreg['city'])
    # TODO: submit bug.
    try:
        clustered = cov_cluster(fit_result, dataframe[cluster_field], use_correction=True)
    except:
        print fit_result.resid.shape, dataframe[cluster_field].shape, set(dataframe[cluster_field].values)
        raise
    
    # From https://github.com/spillz/sci-comp/blob/master/statsmodels-fun/clustered_se.py (def clustered_output(fit_results,group)):
    cse = numpy.diag(clustered)**0.5
    scse = pandas.Series(cse,index=fit.params.index)
    outp = pandas.DataFrame([fit.params,fit.bse,scse]).transpose()
    outp.columns = ['Coef', 'SE', 'C1. S']
    #print outp
    # OK, è identica al risultato con STATA, mancano solo i p-value.
    
    # Translation of http://www.stata.com/statalist/archive/2006-08/msg00840.html
    
    from scipy.stats import t as students_t
    
    deg_f = 2
    outp['tstat'] = abs(outp['Coef'] / outp['C1. S'])
    outp['pval'] = 2 * (1-students_t.cdf(outp['tstat'], deg_f))
    # OK, è identica al risultato con STATA.
    return outp
