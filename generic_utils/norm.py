def norm(what, how='avg'):
    if how in ('avg', 'average'):
        return what / what.mean()
    elif how in ('norm', 'normalized'):
        return what / what.sum()
    elif how in ('std', 'stdev'):
        return what / what.std()
    else:
        return what / what.max()
