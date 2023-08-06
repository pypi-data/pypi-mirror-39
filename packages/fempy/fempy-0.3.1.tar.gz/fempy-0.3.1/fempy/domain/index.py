# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:07:43 2017

@author: mwojc
"""
import numpy as np
import collections
import ast


def is_valid_variable_name(name):
    if '.' in name:  # or name.startswith('__'):  # or name in banned_keys:
        return False
    try:
        ast.parse('{} = None'.format(name))
        return True
    except:
        return False


def get_names_from_expression(expr):
    symbols = ['+', '-', '*', '/', '^',
               '**',
               '~',
               '==', '!=', '<', '<=', '>', '>=',
               '(', ')']
    for s in symbols:
        expr = expr.replace(s, ' ')
    evars = []
    for ev in expr.split():
        ev = ev.strip()
        if is_valid_variable_name(ev):
            evars.append(ev)
    return evars


def masked_index(n=None, lst=None):
    assert n is not None or lst is not None, "Please, give me 'n' or 'lst'"
    # Compute nlist, npos, nmask
    if lst is None:
        lst = np.arange(n)
    else:
        if isinstance(lst, np.ndarray):
            lst = [lst]
        lst = [np.asarray(l).ravel() for l in lst]
        lst = np.unique(np.concatenate(lst))
        if n is None:
            n = max(lst) + 1  # len(lst)
    pos = np.zeros(n, dtype=np.int) - 1
    pos[lst] = np.arange(lst.shape[0])
    mask = pos >= 0
    return lst, pos, mask


class Index(collections.MutableMapping):
    def _bool(self, value):
        mask = np.zeros(self.n, dtype=bool)
        if not isinstance(value, slice):
            value = np.asarray(value)
            if value.dtype != np.bool and value.dtype != np.int:
                value = value.astype(np.int)
        mask[value] = True
        return mask

    def _expr(self, key):
        # key = key.replace('-', '^')  # from numpy 1.14 '-' does not work
        names = get_names_from_expression(key)
        vdict = {'np': np}
        for n in names:
            v = self._get_value(n)
            if v is not None:
                vdict[n] = v
        try:
            value = eval(key, vdict)
        except Exception as e:
            raise KeyError("Processing key '%s' returned the following error: "
                           "%s: %s" % (key, type(e).__name__, e.args[0]))
        if not isinstance(value, np.ndarray) or \
            not value.dtype == np.bool or \
                not value.shape == (self.n,):
            raise KeyError("Key expression does not evaluate "
                           "to proper boolean mask: '%s, %s'" % (key, value))
        return value

    def _get_value_from_masks(self, key):
        if key in self._masks:
            return self._masks[key] * self.msk  # else None

    def _get_value_from_vars(self, key):
        if key in self._vars:
            return self._vars[key]  # else None

    def _get_value(self, key):
        # key is assumed to be a variable name
        value = self._get_value_from_masks(key)
        if value is None:
            value = self._get_value_from_vars(key)
        return value

    def __getitem__(self, key):
        if not isinstance(key, str):
            value = self._bool(key)
        else:
            value = self._get_value_from_masks(key)
            if value is None:
                value = self._expr(key)
        if len(value) == len(self.msk):  # TODO: only in global index
            value = value * self.msk
        return value

    def update(self, *E, **F):
        if len(E) and E[0] is None:
            return
        else:
            super(Index, self).update(*E, **F)


class GlobalNIndex(Index):
    def __init__(self, coors, lst=None):
        self.coors = coors
        self.lst, self.pos, self.msk = masked_index(len(coors), lst)
        self._masks = {}
        self._vars = {}
        for i in range(coors.shape[1]):
            self._vars['xyz'[i]] = coors[:, i]
        self.ng = len(coors)
        self.na = len(self.lst)
        self.n = self.ng

    def __setitem__(self, key, value):
        if not is_valid_variable_name(key):
            raise KeyError("Key not allowed: '%s'" % key)
        self._masks[key] = self._bool(value)

    # __getitem__ is defined in super class

    def __delitem__(self, key):
        del self._masks[key]

    def __iter__(self):
        return iter(self._masks)

    def __len__(self):
        return len(self._masks)


class NIndex(Index):
    def __init__(self, g, lst=None):  # lst is global!
        """
        Local node index
        """
        if isinstance(g, NIndex):
            raise ValueError("Sorry, you must use 'subindex' method "
                             "for creating NIndex from another one.")
        if isinstance(g, np.ndarray):
            g = GlobalNIndex(g, lst)
        self.g = g
        if lst is None:
            lst = self.g.lst
        lst = np.nonzero(self.g[lst])[0]  # ensures global msk is applied
        self.lst, self.pos, self.msk = masked_index(self.g.ng, lst)
        self.n = len(self.lst)
        # self.n = self.nd
        self._masks = {}
        self._vars = {}

    def __setitem__(self, key, value):
        self.g[key] = self.lst[value]

    def __delitem__(self, key):
        del self.g[key]

    def __iter__(self):
        return iter(self.g._masks)

    def __len__(self):
        return len(self.g._masks)

    def _get_value_from_masks(self, key):
        if key in self._masks:
            return self._masks[key]
        else:
            if key in self.g._masks:
                return self.g[key][self.msk]
        # return self.g._get_value_from_masks(key)[self.msk]

    def _get_value_from_vars(self, key):
        if key in self._vars:
            return self._vars[key]
        else:
            if key in self.g._vars:
                value = self.g._vars[key]
                if isinstance(value, np.ndarray):
                    value = value[self.msk]
                return value

    def set_local_mask(self, key, value):
        self._masks[key] = self._bool(value)

    def subindex(self, key=None, gkey=None):
        if key is None:  # if key is None returns a copy
            lst = self.lst
        else:
            lst = self.lst[self[key]]
        if gkey is not None:
            glst = np.nonzero(self.g[gkey])[0]
            lst = np.intersect1d(lst, glst, assume_unique=True)
        return self.__class__(self.g, lst)


class GlobalEIndex(GlobalNIndex):
    def __init__(self, conec, nidx, lst=None):
        self.conec = conec
        lst, pos, msk = masked_index(len(conec), lst)
        # but something can be shadowed by nidx
        if isinstance(nidx, NIndex):
            nidx = nidx.subindex(gkey=conec[lst])
        else:
            nidx = NIndex(nidx, conec[lst])
        lst = np.nonzero(nidx.msk[conec].all(1))[0]
        # ok, now we can assign
        self.lst, self.pos, self.msk = masked_index(len(conec), lst)
        self.nidx = nidx.subindex(gkey=conec[self.lst])
        self._masks = {}
        self._vars = {}
        self.ng = len(conec)
        self.na = len(lst)
        self.n = self.ng

    def __setitem__(self, key, value):
        super(GlobalEIndex, self).__setitem__(key, value)
        self.nidx.g[key] = self.conec[self._masks[key] * self.msk]

    def __getitem__(self, key):
        try:
            value = super(GlobalEIndex, self).__getitem__(key)
        except KeyError as e:
            try:  # this can potentially lead to unexpected results!
                value = self.nidx.g[key] * self.nidx.msk
                value = value[self.conec].all(1)
            except KeyError:
                raise e
        return value

    def __delitem__(self, key):
        del self._masks[key]
        try:
            del self.nidx[key]
        except KeyError:
            pass

    def __iter__(self):
        return iter(set(self._masks.keys() + self.nidx.keys()))

    def __len__(self):
        return len(set(self._masks.keys() + self.nidx.keys()))

    def _get_value_from_masks(self, key):
        if key in self._masks:
            return super(GlobalEIndex, self)._get_value_from_masks(key)
        else:
            if key in self.nidx.g._masks:
                return self.nidx.g[key][self.conec].all(1) * self.msk

    @property
    def nelem(self):
        return self.n

    @property
    def nenod(self):
        return self.conec.shape[1]


class EIndex(NIndex):
    """
    Local element index
    g       - GlobalEIndex instance or conec array
    lst     - list of elements from global index to be used
    nidx    - global or local node index, used only when 'g' is given as
              conec array (must be not None then)
    """
    def __init__(self, g, lst=None, nidx=None):
        # lst global!
        if isinstance(g, EIndex):
            raise ValueError("Sorry, use 'subindex' method "
                             "for creating EIndex from another one.")
        if isinstance(g, np.ndarray):
            if nidx is None:
                raise ValueError("'nidx' cannot be None if 'g' is a conec")
            g = GlobalEIndex(g, nidx, lst)
        self.g = g
        if lst is None:
            lst = self.g.lst
        lst = np.nonzero(self.g[lst])[0]  # ensures global msk is applied
        self.lst, self.pos, self.msk = masked_index(self.g.ng, lst)
        self.nidx = self.g.nidx.subindex(gkey=g.conec[self.lst])
        self.n = len(self.lst)
        # self.n = self.nd
        self._masks = {}
        self._vars = {}

    def __getitem__(self, key):
        try:
            value = super(EIndex, self).__getitem__(key)
        except KeyError as e:
            try:  # this can potentially lead to unexpected results!
                value = self.nidx.g[key] * self.nidx.msk
                value = value[self.g.conec[self.msk]].all(1)
            except KeyError:
                raise e
        return value

    def __delitem__(self, key):
        del self.g._masks[key]
        try:
            del self.nidx[key]
        except KeyError:
            pass

    def __iter__(self):
        return iter(set(self.g._masks.keys()).union(self.nidx.keys()))

    def __len__(self):
        return len(set(self.g._masks.keys()).union(self.nidx.keys()))

    def _get_value_from_masks(self, key):
        if (key in self.g._masks) or (key in self._masks):
            return super(EIndex, self)._get_value_from_masks(key)
        else:
            if (key in self.nidx.g._masks) or (key in self.nidx._masks):
                return self.nidx[key][self.conec].all(1)

    def set_local_mask(self, key, value):
        self._masks[key] = self._bool(value)
        # self.nidx[key] = self.conec[self._masks[key] * self.msk]
        self.nidx.set_local_mask(key, self.conec[self[key]])
        # .conec[self._masks[key] * self.msk])

    @property
    def conec_g(self):
        return self.g.conec[self.msk]

    @property
    def conec_a(self):
        return self.g.nidx.pos[self.conec_g]

    @property
    def conec(self):
        return self.nidx.pos[self.conec_g]

    @property
    def coors_g(self):
        return self.nidx.g.coors

    @property
    def coors_a(self):
        return self.nidx.g.coors[self.nidx.g.lst]

    @property
    def coors(self):
        return self.nidx.g.coors[self.nidx.lst]

    @property
    def nelem(self):
        return self.g.nelem

    @property
    def nenod(self):
        return self.g.nenod


class EGroups(collections.MutableMapping):
    def __init__(self, domain):
        self.domain = domain

    def __getitem__(self, key):
        if 'boundary' in key or 'BOUNDARY' in key or 'CUT' in key:
            self.domain.boundary  # creates boundary if possible and necessary
        group = self.domain.eidx[key]
        return group

    def __setitem__(self, key, value):
        d = self.domain
        d.eidx[key] = value
        f = d._faces
        if f is not None:  # and d.etype.ndime >= 2:
            v = d.eidx[key]
            ef = d.etype.faces
            fconec1 = f.conec
            fconec2 = d.conec[v][:, ef].reshape(-1, ef.shape[1])
            from fempy.domain.tools import find_faces
            fvalue = find_faces(fconec1, fconec2, sort=True)
            f.egroups[key] = fvalue  # recurrence
        d.eidx[key] = value     # TODO: recovers ngroups overwritten in faces

    def __delitem__(self, key):
        d = self.domain
        del d.eidx[key]
        f = d._faces
        if f is not None:
            del f.egroups[key]  # recurrence

    def __iter__(self):
        return iter(self.domain.eidx)

    def __len__(self):
        return len(self.domain.eidx)

    def update_global(self, *E, **F):
        if len(E) and E[0] is None:
            return
        EF = {}
        EF.update(*E, **F)
        for k, v in EF.iteritems():
            self.domain.eidx.g[k] = v  # set global eindex
            v = self.domain.egroups[k]     # get local
            self[k] = v  # set again, but face groups are also set now

    def set_group_by_conec(self, key, conec, glob=False):
        from fempy.domain.tools import find_faces
        d = self.domain
        if glob is False:
            dconec = d.eidx.conec
            vbool = find_faces(dconec, conec, sort=True)
            self[key] = vbool
        else:
            dconec = d.eidx.conec_g
            vbool = find_faces(dconec, conec, sort=True)
            self[key] = vbool
            # self.update_global({key: vbool})


class NGroups(collections.MutableMapping):
    def __init__(self, domain):
        self.domain = domain

    def __getitem__(self, key):
        if isinstance(key, str):
            if 'boundary' in key or 'BOUNDARY' in key or 'CUT' in key:
                self.domain.boundary  # creates boundary if not exists...
        return self.domain.eidx.nidx[key]

    def __setitem__(self, key, value):
        self.domain.eidx.nidx[key] = value

    def __delitem__(self, key):
        del self.domain.eidx.nidx[key]

    def __iter__(self):
        return iter(self.domain.eidx.nidx)

    def __len__(self):
        return len(self.domain.eidx.nidx)

    def update_global(self, *E, **F):
        if len(E) and E[0] is None:
            return
        EF = {}
        EF.update(*E, **F)
        for k, v in EF.iteritems():
            self.domain.eidx.nidx.g[k] = v  # set global eindex
            # v = self.domain.egroups[k]     # get local
            # self[k] = v  # set again, but face groups are also set now

    def nums(self, key=None, sortby=None, reverse=False):
        # Valid keys are: str and array-like of bool or int type
        # idx = np.nonzero(self[key])[0]
        if key is None:
            idx = np.arange(self.domain.nnode)
        elif isinstance(key, str):
            idx = np.nonzero(self[key])[0]
        else:
            key = np.asarray(key)
            if key.dtype == np.bool:
                idx = np.nonzero(self[key])[0]
            else:  # integer array
                idx = key
        if sortby is not None:
            coors = self.domain.coors[idx]
            for sc in sortby:
                c = 0 if sc in (0, 'x') else None
                c = 1 if c is None and sc in (1, 'y') else c
                c = 2 if c is None and sc in (2, 'z') else c
                assert c is not None, "Wrong sorting definition"
                assert c < coors.shape[1], "Sorry, cannot sort by {}-th "
                "dimension".format(c)
                si = coors[:, c].argsort()
                idx = idx[si]
                coors = coors[si]
        if reverse:
            idx = idx[::-1]
        return idx


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
