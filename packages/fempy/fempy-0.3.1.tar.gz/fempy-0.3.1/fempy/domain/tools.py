# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:03:58 2017

@author: mwojc
"""
import numpy as np


class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/
        commit/fa7733e075da0d790d809aa3d2f53071897e6f76

    This class can be used as a decorator replacing the built-in python
    'property'
    """
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def invalidate_caches(obj, names=None):
    """
    Searches for cached_properties in 'obj' and resets them.
    """
    # get all names in model class and object
    c = obj.__class__
    d = obj.__dict__
    cdir = dir(c) if names is None else names
    dkeys = d.keys()
    for n in cdir:
        # invalidate cached_properties if they have been used...
        if isinstance(getattr(c, n), cached_property) and n in dkeys:
            # property has been cached so we invalidate it
            del d[n]


def renumber(coors, conec):
    """
    Checks which coors are used by conec, and then renumber conec.

    Returns a tuple: (new_coors, new_conec, nlist), where nlist contains
    node numbers in original coors used by new_conec. The following is true
    for the returned values:
        new_coors = coors[nlist]
        conec = nlist[new_conec]
    """
    maxn = conec.max()
    if maxn > len(coors) - 1:
        raise ValueError("No such node: %i" % maxn)
    nlist = np.unique(conec)
    if len(nlist) < len(coors):
        cnlist = np.zeros(len(coors), dtype=int) - 1
        cnlist[nlist] = np.arange(len(nlist), dtype=int)
        coors = coors[nlist]
        conec = cnlist[conec]
    return coors, conec, nlist


def uneven_sum(arr, mask, keepshape=False):
    """
    Sums 'arr' along 0-th axis with slices defined by boolean
    'mask'. If 'keepshape' is True the return array has the
    same dimension as 'arr' (with repeated entries)

    Note: similar functionality is achieved with

    >>> np.add.reduceat(arr, np.nonzero(mask)[0])
    """
    idx = np.cumsum(mask) - 1
    res_shape = (mask.sum(),) + arr.shape[1:]
    res = np.zeros(res_shape, dtype=arr.dtype)
    np.add.at(res, idx, arr)
    if keepshape:
        return res[idx]
    return res


def unique_rows_lex(a, sort=False, strict=True):
    """
    Sorts lexically 2D integer array and searches for duplicate rows

    Arguments:
        a       - 2D integer array
        sort    - if True, rows in 'a' are sorted first (default is False)
        strict  - if True (default) only the rows which appear once in 'a' are
                  treated as uniqe, if False, also the first occurence of
                  duplicated rows is added to the resulting mask

    Returns tuple (idx, mask) is returned where 'idx' are indices of lexical
    sort of 'a' and 'mask' is a boolean array pointing out the unique rows
    numbers in idx.
    """
    if len(a) == 0:
        return np.array([], dtype=np.int), np.array([], dtype=np.bool)
    a = np.asarray(a)
    if sort:
        a = np.sort(a)      # sort rows
    idx = np.lexsort(a.T)   # find indices which sort along last axis
    sa = a[idx]             # get lexically sorted version of a
    # mask is False if previous entry in sa is the same
    mask = np.append([True, ], np.any(np.diff(sa, axis=0), axis=1))
    if strict:
        # if mask entry is False make also previous entry False
        mask[np.nonzero(~mask)[0] - 1] = False
        # now only entries which appear once are marked True in mask
    return idx, mask


def unique_rows(a, sort=False, strict=True):
    """
    Compute unique rows in 2D integer array

    Arguments like in unique_rows_lex.

    Returns boolean mask which points the unique rows in 'a'.
    """
    idx, mask = unique_rows_lex(a, sort=sort, strict=strict)
    # recover mask for original array from its lexical sort
    idx = idx[mask]
    mask[:] = False
    mask[idx] = True
    return mask


def duplicate_rows(a, sort=False):
    """
    Computes tags for the duplicate rows in 2D array

    Arguments like in unique_rows_lex.

    Returns 'dups' - an integer array with the same integer tag for duplicate
    rows in 'a'. Tags are numbered from 1 to the number of strictly unique
    (possibly sorted first). The order of tags is ruled by lexical sort
    of 'a.T'
    """
    idx, mask = unique_rows_lex(a, sort=sort, strict=False)
    # mark duplicates with subsequent integers
    dups = np.cumsum(mask)
    d = np.zeros_like(dups)
    d[idx] = dups
    return d


def in2d(a, b, sort=False):
    """
    Test whether 'b' rows are present in 'a'.

    Returns boolean array of the same length as 'a' that is True where the
    row of 'a' is in 'b'. If sort=True the rows in both arrays are sorted
    first.
    """
    n = len(a)
    dp = duplicate_rows(np.concatenate([a, b]), sort=sort)
    return np.in1d(dp[:n], dp[n:])


find_faces = in2d


def agree_rows(a, b):
    """
    Agree indices of same rows in a and b (which are 2D arrays).

    For a given 'a' and 'b' computes index arrays 'aidx', 'bidx', such that
    a[aidx] == b[bidx]. Input arrays must be of the same lengts and all 'a'
    rows must be present in 'b' otherwise ValueError is raised

    Returns tuple (aidx, bidx)
    """
    aidx = np.lexsort(a.T)
    bidx = np.lexsort(b.T)
    if np.allclose(a[aidx], b[bidx]):
        return aidx, bidx
    else:
        raise ValueError("Rows indices cannot be agreed")

# def find_faces(fconec1, fconec2, edges=None, sort=False):
#    """
#    Finds positions of faces2 in faces1 as boolean array
#    If sort is given then orientation is also unified
#    """
#    n = len(fconec1)
#    join = np.concatenate
#    if edges is None or sort is True:
#        dp = duplicate_rows(join([fconec1, fconec2]), sort=sort)
#        return np.in1d(dp[:n], dp[n:])
#    e1 = fconec1[:, edges].reshape(-1, edges.shape[1])
#    e2 = fconec2[:, edges].reshape(-1, edges.shape[1])
#    dp = duplicate_rows(join([e1, e2]))
#    return np.in1d(dp[:n], dp[n:]).reshape(n, -1).all(1)


def normal_sign(domain):
    """
    +1 out, -1 in
    """
    d = domain
    if d.etype.btype is None or d.etype.ndime < 2:
        return
    from index import EIndex
    fconec = d.eidx.conec_g[:, d.etype.faces[0]]  # global face conec
    fidx = EIndex(fconec, nidx=d.eidx.nidx.g)
    faces = d.btype(fidx, d.etype.btype)
    n = faces.normal[:, 0]           # normal, only first Gauss point
    p = faces.ecoors[:, 0]           # any (first) face point
    v = d.ecoors_mean                # element center point
    s = np.sign(np.einsum('ij,ij->i', n, v-p)).astype(int)  # +1 out, -1 in
    return s


def create_faces(domain):
    d = domain
    # Do nothing if there are no boundary elements
    if d.etype.btype is None:
        return
    # Create all faces conec
    fconec0 = d.eidx.conec_g[:, d.etype.faces]         # global fconec
    fconec = fconec0.reshape(-1, fconec0.shape[-1])    # reshape to 2D
    fconec = fconec[unique_rows(fconec, strict=False)]
    # Create faces index
    from fempy.domain.index import EIndex
    fidx = EIndex(fconec, nidx=d.eidx.nidx)  # should fconec be unique?
    # Add the groups to the index
    for k, v in d.eidx.items():
        vcon = fconec0[v].reshape(-1, fconec0.shape[-1])  #
        vbool = find_faces(fconec, vcon, sort=True)
        # TODO: below, nvbool recovers ngroups overwritten by setting fidx[k]
        # they are overwritten because we use the same global node index for
        # domain and faces and when setting element groups this global node
        # index is also updated (in a hard way). We need a kind of dynamic
        # __getitem__ to always compute the result when eidx.nidx[k]
        # is called with 'k' present in eidx only
        if k in d.eidx.nidx:
            nvbool = d.eidx.nidx.g[k]  # [fidx.nidx.lst]
        fidx[k] = vbool
        if k in d.eidx.nidx:
            fidx.nidx.g[k] = nvbool
        # d.eidx[k] = v  # TODO: recovers ngroups overwritten in faces
    # Now handle boundary
    bbool = unique_rows(fconec, sort=True)
    if 'BOUNDARY' not in fidx.g:  # add global boundary...
        fidx['BOUNDARY'] = bbool
    # add locally to faces domain
    fidx.set_local_mask('boundary', bbool)
    fidx.set_local_mask('CUT', fidx['boundary^BOUNDARY'])
    # add locally to domain nidx
    d.eidx.nidx.set_local_mask('boundary', fidx.conec[bbool])
    d.eidx.nidx.set_local_mask('CUT', fidx.conec[fidx['CUT']])
    # Create faces
    faces = d.btype(fidx, d.etype.btype)
    return faces


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
