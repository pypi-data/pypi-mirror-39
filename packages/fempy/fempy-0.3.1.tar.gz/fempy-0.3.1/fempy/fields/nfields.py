# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 13:49:09 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.fields import Field


class nField(Field):
    def __new__(cls, domain, data):
        if isinstance(data, nField):
            if domain is data.domain:
                return data
        nn = domain.nnode
        nd = domain.ndime
        data = np.asarray(data)
        prefix = 1
        if not data.shape[:prefix] == (nn,):
            default = data
            data = np.empty((nn,) + data.shape, dtype=data.dtype)
            data[:] = default
        # Field factory
        sshape = data.shape[prefix:]
        if sshape == ():
            cls = nScalar
        elif len(sshape) == 1 and sshape == (nd,):
            cls = nVector
        elif len(sshape) == 1 and sshape != (nd,):
            cls = nList
        elif len(sshape) == 2 and sshape == (nd,)*2:
            cls = nTensor
        elif len(sshape) == 2 and sshape != (nd,)*2:
            cls = nMatrix
        elif sshape == (nd,)*3:
            cls = nTensor3
        elif sshape == (nd,)*4:
            cls = nTensor4
        else:
            pass
        f = Field.__new__(cls, data, prefix=prefix)
        f.domain = domain
        return f

    def __array_finalize__(self, field):
        if field is None:
            return
        Field.__array_finalize__(self, field)
        self.domain = getattr(field, 'domain', None)

    @property
    def ndofs(self):
        return np.prod(self.sshape, dtype=int)

    @property
    def edofs(self):
        return self.domain.etype.nnode * self.ndofs

    @property
    def nsize(self):
        return self.domain.eidx.nidx.g.na * self.ndofs

    @property
    def _nipos(self):
        idx = self.domain.nlist
        return np.arange(self.nsize).reshape(-1, self.ndofs)[idx]

    @property
    def nipos(self):
        return self.factory(self._nipos)

    @property
    def eipos(self):
        return self._nipos[self.domain.conec].reshape(-1, self.edofs)

    @property
    def eij(self):
        as_strided = np.lib.stride_tricks.as_strided
        eipos = self.eipos
        m, n = eipos.shape
        sz = eipos.itemsize
        ei = as_strided(eipos, shape=(m, n, n), strides=(n*sz, sz, 0))
        ej = as_strided(eipos, shape=(m, n, n), strides=(n*sz, 0, sz))
        return ei, ej

    @property
    def groups(self):
        return self.domain.ngroups

    def __add__(self, other):
        if isinstance(other, nField):
            sd = self.domain
            od = other.domain
            if sd.eidx.nidx.g is od.eidx.nidx.g:  # the same space
                nlist = np.intersect1d(sd.eidx.nidx.lst,
                                       od.eidx.nidx.lst, assume_unique=True)
                sidx = sd.eidx.nidx.pos[nlist]
                oidx = od.eidx.nidx.pos[nlist]
                res = self.copy()
                res[sidx] += other[oidx]
                return res
            raise ValueError("Fields are defined of different point spaces")
        return Field.__add__(self, other)

    def __iadd__(self, other):
        if isinstance(other, nField):
            sd = self.domain
            od = other.domain
            if sd.eidx.nidx.g is od.eidx.nidx.g:  # the same space
                nlist = np.intersect1d(sd.eidx.nidx.lst,
                                       od.eidx.nidx.lst, assume_unique=True)
                sidx = sd.eidx.nidx.pos[nlist]
                oidx = od.eidx.nidx.pos[nlist]
                res = self
                res[sidx] += other[oidx]
                return res
            raise ValueError("Fields are defined of different point spaces")
        return Field.__add__(self, other)

    def factory(self, data=None, superdomain=False):
        if data is None:
            data = np.zeros(self.sshape)
        if superdomain:
            return nField(self.domain.superdomain, data)
        return nField(self.domain, data)


class nScalar(nField):
    def __new__(cls, domain, data=None):
        nn = domain.nnode
        if data is None:
            data = np.zeros((nn,))
        data = np.asarray(data)
        assert data.shape == (nn,) or data.shape == ()
        return nField.__new__(cls, domain, data)


class nList(nField):
    def __new__(cls, domain, data):
        nn = domain.nnode
        if isinstance(data, int):
            data = np.zeros((nn, data))
        else:
            data = np.asarray(data)
            assert len(data.shape) in (1, 2)
            if len(data.shape) == 2:
                assert data.shape[0] == nn
        return nField.__new__(cls, domain, data)


class nVector(nList):
    def __new__(cls, domain, data=None):
        nn = domain.nnode
        nd = domain.ndime
        if data is None:
            data = np.zeros((nn, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, nd)
        assert data.shape == (nn, nd) or data.shape == (nd,)
        return nField.__new__(cls, domain, data)


class nMatrix(nField):
    def __new__(cls, domain, data):
        nn = domain.nnode
        if isinstance(data, int):
            data = np.zeros((nn, data, data))
        else:
            data = np.asarray(data)
            assert len(data.shape) in (1, 2, 3)
            if len(data.shape) == 1:
                assert data.dtype == int and data.shape[0] == 2
                data = np.zeros(tuple(data))
            if len(data.shape) == 3:
                assert data.shape[0] == nn
        return nField.__new__(cls, domain, data)


class nTensor(nMatrix):
    def __new__(cls, domain, data=None):
        nn = domain.nnode
        nd = domain.ndime
        if data is None:
            data = np.zeros((nn, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd))
        assert data.shape == (nn, nd, nd) or data.shape == (nd,)*2
        return nField.__new__(cls, domain, data)


class nTensor3(nField):
    def __new__(cls, domain, data=None):
        nn = domain.nnode
        nd = domain.ndime
        if data is None:
            data = np.zeros((nn, nd, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd, nd))
        assert data.shape == (nn, nd, nd, nd) or data.shape == (nd,)*3
        return nField.__new__(cls, domain, data)


class nTensor4(nField):
    def __new__(cls, domain, data=None):
        nn = domain.nnode
        nd = domain.ndime
        if data is None:
            data = np.zeros((nn, nd, nd, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd, nd, nd))
        assert data.shape == (nn, nd, nd, nd, nd) or data.shape == (nd,)*4
        return nField.__new__(cls, domain, data)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
