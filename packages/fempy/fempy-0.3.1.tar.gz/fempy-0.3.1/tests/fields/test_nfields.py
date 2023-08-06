# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 11:05:58 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.nfields import nField, nScalar, nVector, nList
from fempy.fields.nfields import nTensor, nMatrix, nTensor3, nTensor4
from fempy.fields.algebra import dot, tensordot
from fempy.testing import testdir
from common import Simple3D
import pytest


class Test_nField(Simple3D):
    @property
    def domain(self):
        return self.domain3D

    @property
    def field(self):
        return nTensor(self.domain, np.random.rand(len(self.coors), 3, 3))

    def test_getitem(self):
        d = self.domain
        f = nTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        for k, v in d.ngroups.items():
            assert (v == f.groups[k]).all()
        d.ngroups['test2'] = slice(1, 6, 2)
        assert (f['test2'] == f[1:6:2]).all()
        assert np.allclose(f['tope'], f[d.eidx.nidx['tope']])

        with pytest.raises(AttributeError):
            f.groups = {}
        eg = d.ngroups
        d.ngroups = {}
        assert f.groups == {}
        d.ngroups = eg

    def test_setitem(self):
        d = self.domain
        f = nTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        f['tope'] = 5.
        assert np.allclose(f[7, 0], [5., 5., 5.])
        assert np.allclose(f[0, 0], [1., 1., 0.])
        assert np.allclose(f['tope', 0, 0], [5.]*9)

    def test_scalar_field_creation(self):
        d = self.domain
        f = nScalar(d)
        assert type(f) == nScalar
        assert f.shape == (d.nnode,)
        assert np.allclose(f, 0.)
        assert f.domain is d
        f = nScalar(d, 1.)
        assert type(f) == nScalar
        assert f.shape == (d.nnode,)
        assert np.allclose(f, 1.)
        f = nScalar(d, f)
        assert type(f) == nScalar
        with pytest.raises(AssertionError):
            f = nScalar(d, [2.])
        with pytest.raises(AssertionError):
            f = nScalar(d, [[2.], [1]])
        f = nScalar(d, 'test')
        assert f.dtype in ('S4', '<U4')

    def test_vector_field_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nVector(d)
        assert type(f) == nVector
        assert f.shape == (nn, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nVector(d, 1.)
        assert f.shape == (nn, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        f = nVector(d, [1., 1., 0.])
        assert f.shape == (nn, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = nVector(d, f)
        assert f.shape == (nn, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = nVector(d, [2., 2.])
        with pytest.raises(AssertionError):
            f = nVector(d, [[2.], [1]])
        f = nVector(d, 'test')
        assert f.dtype in ('S4', '<U4')

    def test_tensor_field_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nTensor(d)
        assert type(f) == nTensor
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nTensor(d, 1.)
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        f = nTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f[..., -1, 0], 2.)
        assert f.domain is d

        f = nTensor(d, f)
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f[..., 0, 0], 1.)
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = nTensor(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = nTensor(d, [[2., 1]])
        f = nTensor(d, 3)
        assert f.dtype == int

    def test_tensor3_field_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nTensor3(d)
        assert type(f) == nTensor3
        assert f.shape == (nn, nd, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nTensor3(d, 1.)
        assert f.shape == (nn, nd, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        r = np.random.rand(3, 3, 3)
        f = nTensor3(d, r)
        assert f.shape == (nn, nd, nd, nd)
        assert np.allclose(f[..., 1, 1, 1], r[1, 1, 1])
        assert f.domain is d

        f = nTensor3(d, f)
        assert f.shape == (nn, nd, nd, nd)
        assert np.allclose(f[..., 0, 0, 0], r[0, 0, 0])
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = nTensor3(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = nTensor3(d, [[2., 1]])
        f = nTensor3(d, 3)
        assert f.dtype == int

    def test_tensor4_field_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nTensor4(d)
        assert type(f) == nTensor4
        assert f.shape == (nn, nd, nd, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nTensor4(d, 1.)
        assert f.shape == (nn, nd, nd, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        r = np.random.rand(3, 3, 3, 3)
        f = nTensor4(d, r)
        assert f.shape == (nn, nd, nd, nd, nd)
        assert np.allclose(f[..., 1, 1, 1, 1], r[1, 1, 1, 1])
        assert f.domain is d

        f = nTensor4(d, f)
        assert f.shape == (nn, nd, nd, nd, nd)
        assert np.allclose(f[..., 0, 0, 0, 0], r[0, 0, 0, 0])
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = nTensor4(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = nTensor4(d, [[2., 1]])
        f = nTensor4(d, 3)
        assert f.dtype == int

    def test_list_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nList(d, [1., 1., 0.])
        assert type(f) == nVector
        assert f.shape == (nn, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = nList(d, nVector(d, [1., 1., 0.]))
        assert type(f) == nVector
        assert f.shape == (nn, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = nList(d, 5)
        assert type(f) == nList
        assert f.shape == (nn, 5)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nList(d, [3, 2])
        assert type(f) == nList
        assert f.shape == (nn, 2)
        assert np.allclose(f[..., 0], 3)
        assert f.domain is d
        assert f.dtype == int

        with pytest.raises(AssertionError):
            f = nList(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = nList(d, [[2., 1]])
        with pytest.raises(AssertionError):
            f = nList(d, 1.)

    def test_matrix_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        f = nMatrix(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert type(f) == nTensor
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f[..., -1, 0], 2.)
        assert f.domain is d

        f = nMatrix(d, nTensor(d))
        assert type(f) == nTensor
        assert f.shape == (nn, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nMatrix(d, (5, 2))
        assert type(f) == nMatrix
        assert f.shape == (nn, 5, 2)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = nMatrix(d, [[3, 2], [2, 1]])
        assert type(f) == nMatrix
        assert f.shape == (nn, 2, 2)
        assert np.allclose(f[..., 0, 0], 3)
        assert f.domain is d
        assert f.dtype == int

        with pytest.raises(AssertionError):
            f = nMatrix(d, [2., 1])
        with pytest.raises(AssertionError):
            f = nMatrix(d, [[[2., 1]]])
        with pytest.raises(AssertionError):
            f = nMatrix(d, 1.)

    def test_nfield_creation(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime

        with pytest.raises(TypeError):
            f = nField(d)

        f = nField(d, 2.)
        assert type(f) == nScalar

        f = nField(d, [1, 2, 3])
        assert type(f) == nVector
        assert f.dtype == int

        f = nField(d, [1, 2, 3, 4.])
        assert type(f) == nList

        f = nField(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert type(f) == nTensor

        f = nField(d, [[1., 1., 0.], [1., 1., 0.]])
        assert type(f) == nMatrix

        r = np.random.rand(3, 3, 3)
        f = nField(d, r)
        assert type(f) == nTensor3

        r = np.random.rand(3, 3, 3, 3)
        f = nField(d, r)
        assert type(f) == nTensor4

        r = np.random.rand(3, 2, 3, 4)
        f = nField(d, r)
        assert type(f) == nField

        r = np.random.rand(nn, nd, nd)
        f = nField(d, r)
        assert type(f) == nTensor

    def test_tensordot_dot(self):
        d = self.domain
        t4 = nTensor4(d, 1.)
        t2 = nTensor(d, 3.)
        v = nVector(d, 4.)

        assert type(tensordot(t4, t2)) == nTensor
        assert type(tensordot(t2, t2)) == nScalar
        assert type(dot(t2, v)) == nVector
        assert type(dot(v, v)) == nScalar
        assert type(dot(t2, t2)) == nTensor

    def test_ufuncs(self):
        d = self.domain
        f = nField(d, [2, 3, 4.])  # scalar
        assert isinstance(np.sum(f), float)
        f = nField(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])  # tensor
        assert isinstance(np.sum(f, 2), nVector)
        assert isinstance(np.sum(f, f.saxes), nScalar)
        assert isinstance(np.sum(f, 0), np.ndarray)


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
