"""
Compare data structures, recursing on lists and dictionaries.

Usage:

gendiff({'a' : 3}, {'a' : 4})
"""

def listdiff(l1, l2, level=0):
    if len(l1) != len(l2):
        return("{}Left has {} levels, right has {}".format("  "*level,
                                                           len(l1), len(l2)))
        return True
    any_diff = False
    ret = ""
    for idx, (o1, o2) in enumerate(zip(l1, l2)):
        diff = gendiff(o1, o2, level=level+1)
        if diff is not None:
             ret += "{}-> item {}\n{}\n".format("  "*level, idx, diff)
    if ret != "":
        return ret
    return None


def dictdiff(d1, d2, level=0):
    k_diffs = set(d1) - set(d2), set(d2) - set(d1)
    if any(k_diffs):
        return "{}Keys {} only in left, keys {} only in right".format("  "*level,
                                                                      *k_diffs)
    ret = ""
    for k in set().union(d1, d2):
        diff = gendiff(d1[k], d2[k], level=level+1)
        if diff is not None:
            ret += "{}-> key {}\n{}\n".format("  "*level, k, diff)
    if ret != "":
        return ret
    return None

            
methods = {list : listdiff,
           dict : dictdiff}
            
def gendiff(o1, o2, level=0):
    if type(o1) != type(o2):
        diff = ("{}Left has type {}, right has type{}".format("  "*level,
                                                              type(o1), type(o2)))
    elif type(o1) in methods:
        method = methods[type(o1)]
        diff = method(o1, o2, level=level)
    elif o1 != o2:
        diff = ("{}{} different from {}".format('  '*level, o1, o2))
    else:
        diff = None

    if level:
        return diff
    if diff:
        print(diff)
    else:
        print("No difference")

