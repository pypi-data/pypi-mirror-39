# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 13:49:09 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.fields import Field
from fempy.fields.nfields import nField


class gField(Field):
    def __new__(cls, domain, data):
        if isinstance(data, gField):
            if domain is data.domain:
                return data
        if isinstance(data, nField):
            if domain is data.domain:
                from fempy.fields.operators import ongauss
                return ongauss(data)
        ne = domain.nelem
        ng = domain.etype.ngauss
        nd = domain.ndime
        data = np.asarray(data)
        prefix = 2
        if not data.shape[:prefix] == (ne, ng):
            default = data
            data = np.empty((ne, ng) + data.shape, dtype=data.dtype)
            data[:] = default
        # Field factory
        sshape = data.shape[prefix:]
        if sshape == ():
            cls = gScalar
        elif len(sshape) == 1 and sshape == (nd,):
            cls = gVector
        elif len(sshape) == 1 and sshape != (nd,):
            cls = gList
        elif len(sshape) == 2 and sshape == (nd,)*2:
            cls = gTensor
        elif len(sshape) == 2 and sshape != (nd,)*2:
            cls = gMatrix
        elif sshape == (nd,)*3:
            cls = gTensor3
        elif sshape == (nd,)*4:
            cls = gTensor4
        else:
            pass
        #
        f = Field.__new__(cls, data, prefix=prefix)
        f.domain = domain
        return f

    def __array_finalize__(self, field):
        if field is None:
            return
        Field.__array_finalize__(self, field)
        self.domain = getattr(field, 'domain', None)

    @property
    def groups(self):
        return self.domain.egroups

    def factory(self, data):
        return gField(self.domain, data)


class gScalar(gField):
    def __new__(cls, domain, data=None):
        ne = domain.nelem
        ng = domain.etype.ngauss
        if data is None:
            data = np.zeros((ne, ng))
        data = np.asarray(data)
        assert data.shape == (ne, ng) or data.shape == ()
        return gField.__new__(cls, domain, data)


class gList(gField):
    def __new__(cls, domain, data):
        ne = domain.nelem
        ng = domain.etype.ngauss
        if isinstance(data, int):
            data = np.zeros((ne, ng, data))
        else:
            data = np.asarray(data)
            assert len(data.shape) in (1, 3)
            if len(data.shape) == 3:
                assert data.shape[:2] == (ne, ng)
        return gField.__new__(cls, domain, data)


class gVector(gList):
    def __new__(cls, domain, data=None):
        ne = domain.nelem
        ng = domain.etype.ngauss
        nd = domain.ndime
        if data is None:
            data = np.zeros((ne, ng, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, nd)
        assert data.shape == (ne, ng, nd) or data.shape == (nd,)
        return gField.__new__(cls, domain, data)


class gMatrix(gField):
    def __new__(cls, domain, data):
        ne = domain.nelem
        ng = domain.etype.ngauss
        if isinstance(data, int):
            data = np.zeros((ne, ng, data, data))
        else:
            data = np.asarray(data)
            assert len(data.shape) in (1, 2, 4)
            if len(data.shape) == 1:
                assert data.dtype == int and data.shape[0] == 2
                data = np.zeros(tuple(data))
            if len(data.shape) == 4:
                assert data.shape[:2] == (ne, ng)
        return gField.__new__(cls, domain, data)


class gTensor(gMatrix):
    def __new__(cls, domain, data=None):
        ne = domain.nelem
        ng = domain.etype.ngauss
        nd = domain.ndime
        if data is None:
            data = np.zeros((ne, ng, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd))
        assert data.shape == (ne, ng, nd, nd) or data.shape == (nd,)*2
        return gField.__new__(cls, domain, data)


class gTensor3(gField):
    def __new__(cls, domain, data=None):
        ne = domain.nelem
        ng = domain.etype.ngauss
        nd = domain.ndime
        if data is None:
            data = np.zeros((ne, ng, nd, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd, nd))
        assert data.shape == (ne, ng, nd, nd, nd) or data.shape == (nd,)*3
        return gField.__new__(cls, domain, data)


class gTensor4(gField):
    def __new__(cls, domain, data=None):
        ne = domain.nelem
        ng = domain.etype.ngauss
        nd = domain.ndime
        if data is None:
            data = np.zeros((ne, ng, nd, nd, nd, nd))
        data = np.asarray(data)
        if data.shape == ():
            data = np.tile(data, (nd, nd, nd, nd))
        assert data.shape == (ne, ng, nd, nd, nd, nd) or data.shape == (nd,)*4
        return gField.__new__(cls, domain, data)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
