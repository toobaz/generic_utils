import tables as tb
from numpy import array
from scipy import sparse

def store_array(obj, obj_name, store='store.h5'):
    """
    Store a scipy array in an HDF5 store, overriding any object with the same
    name, and inferring the atom from the dtype.
    """
    with tb.open_file(store, 'a') as f:
        try:
            n = getattr(f.root, obj_name)
            n._f_remove()
        except AttributeError:
            pass
        atom = tb.Atom.from_dtype(obj.dtype)
        ds = f.createCArray(f.root, obj_name, atom, obj.shape)
        ds[:] = obj

def load_array(obj_name, store='store.h5'):
    with tb.open_file(store) as f:
        m = getattr(f.root, obj_name).read()
        return m

def store_sparse_mat(m, name, store='store.h5'):
    with tb.open_file(store,'a') as f:
        for par in ('data', 'indices', 'indptr', 'shape'):
            full_name = '%s_%s' % (name, par)
            try:
                n = getattr(f.root, full_name)
                n._f_remove()
            except AttributeError:
                pass
            
            arr = array(getattr(m, par))
            atom = tb.Atom.from_dtype(arr.dtype)
            ds = f.createCArray(f.root, full_name, atom, arr.shape)
            ds[:] = arr

def load_sparse_mat(name, store='store.h5'):
    with tb.open_file(store) as f:
        pars = []
        for par in ('data', 'indices', 'indptr', 'shape'):
            pars.append(getattr(f.root, '%s_%s' % (name, par)).read())
    m = sparse.csr_matrix(tuple(pars[:3]), shape=pars[3])
    return m
