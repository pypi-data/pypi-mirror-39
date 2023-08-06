# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 11:25:01 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.gfields import gField, gScalar, gVector, gList
from fempy.fields.gfields import gTensor, gMatrix, gTensor3, gTensor4
from fempy.fields.algebra import dot, tensordot
from fempy.testing import testdata
from common import Simple3D
import pytest


class Test_gField(Simple3D):
    @property
    def domain(self):
        return self.domain3D

    def test_getitem(self):
        d = self.domain
        f = gTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        for k, v in d.egroups.items():
            assert (v == f.groups[k]).all()
        d.egroups['test2'] = slice(1, 6, 2)
        assert (f['test2'] == f[1:6:2]).all()

        with pytest.raises(AttributeError):
            f.groups = {}
        eg = d.egroups
        d.egroups = {}
        assert f.groups == {}
        d.egroups = eg

    def test_setitem(self):
        d = self.domain
        f = gTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        f['bottome'] = 5.
        assert np.allclose(f['bottome', 0, 0], [[5., 5., 5.]]*4)

    def test_scalar_field_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        f = gScalar(d)
        assert type(f) == gScalar
        assert f.shape == (ne, ng)
        assert np.allclose(f, 0.)
        assert f.domain is d
        f = gScalar(d, 1.)
        assert type(f) == gScalar
        assert f.shape == (ne, ng)
        assert np.allclose(f, 1.)
        f = gScalar(d, f)
        assert type(f) == gScalar
        with pytest.raises(AssertionError):
            f = gScalar(d, [2.])
        with pytest.raises(AssertionError):
            f = gScalar(d, [[2.], [1]])
        f = gScalar(d, 'test')
        assert f.dtype in ('S4', '<U4')

    def test_vector_field_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gVector(d)
        assert type(f) == gVector
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gVector(d, 1.)
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        f = gVector(d, [1., 1., 0.])
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = gVector(d, f)
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = gVector(d, [2., 2.])
        with pytest.raises(AssertionError):
            f = gVector(d, [[2.], [1]])
        f = gVector(d, 'test')
        assert f.dtype in ('S4', '<U4')

    def test_tensor_field_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gTensor(d)
        assert type(f) == gTensor
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gTensor(d, 1.)
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        f = gTensor(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f[..., -1, 0], 2.)
        assert f.domain is d

        f = gTensor(d, f)
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f[..., 0, 0], 1.)
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = gTensor(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = gTensor(d, [[2., 1]])
        f = gTensor(d, 3)
        assert f.dtype == int

    def test_tensor3_field_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gTensor3(d)
        assert type(f) == gTensor3
        assert f.shape == (ne, ng, nd, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gTensor3(d, 1.)
        assert f.shape == (ne, ng, nd, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        r = np.random.rand(3, 3, 3)
        f = gTensor3(d, r)
        assert f.shape == (ne, ng, nd, nd, nd)
        assert np.allclose(f[..., 1, 1, 1], r[1, 1, 1])
        assert f.domain is d

        f = gTensor3(d, f)
        assert f.shape == (ne, ng, nd, nd, nd)
        assert np.allclose(f[..., 0, 0, 0], r[0, 0, 0])
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = gTensor3(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = gTensor3(d, [[2., 1]])
        f = gTensor3(d, 3)
        assert f.dtype == int

    def test_tensor4_field_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gTensor4(d)
        assert type(f) == gTensor4
        assert f.shape == (ne, ng, nd, nd, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gTensor4(d, 1.)
        assert f.shape == (ne, ng, nd, nd, nd, nd)
        assert np.allclose(f, 1.)
        assert f.domain is d

        r = np.random.rand(3, 3, 3, 3)
        f = gTensor4(d, r)
        assert f.shape == (ne, ng, nd, nd, nd, nd)
        assert np.allclose(f[..., 1, 1, 1, 1], r[1, 1, 1, 1])
        assert f.domain is d

        f = gTensor4(d, f)
        assert f.shape == (ne, ng, nd, nd, nd, nd)
        assert np.allclose(f[..., 0, 0, 0, 0], r[0, 0, 0, 0])
        assert f.domain is d

        with pytest.raises(AssertionError):
            f = gTensor4(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = gTensor4(d, [[2., 1]])
        f = gTensor4(d, 3)
        assert f.dtype == int

    def test_list_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gList(d, [1., 1., 0.])
        assert type(f) == gVector
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = gList(d, gVector(d, [1., 1., 0.]))
        assert type(f) == gVector
        assert f.shape == (ne, ng, nd)
        assert np.allclose(f[..., -1], 0.)
        assert f.domain is d

        f = gList(d, 5)
        assert type(f) == gList
        assert f.shape == (ne, ng, 5)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gList(d, [3, 2])
        assert type(f) == gList
        assert f.shape == (ne, ng, 2)
        assert np.allclose(f[..., 0], 3)
        assert f.domain is d
        assert f.dtype == int

        with pytest.raises(AssertionError):
            f = gList(d, [[2., 2.], [1., 1.]])
        with pytest.raises(AssertionError):
            f = gList(d, [[2., 1]])
        with pytest.raises(AssertionError):
            f = gList(d, 1.)

    def test_matrix_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        f = gMatrix(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert type(f) == gTensor
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f[..., -1, 0], 2.)
        assert f.domain is d

        f = gMatrix(d, gTensor(d))
        assert type(f) == gTensor
        assert f.shape == (ne, ng, nd, nd)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gMatrix(d, (5, 2))
        assert type(f) == gMatrix
        assert f.shape == (ne, ng, 5, 2)
        assert np.allclose(f, 0.)
        assert f.domain is d

        f = gMatrix(d, [[3, 2], [2, 1]])
        assert type(f) == gMatrix
        assert f.shape == (ne, ng, 2, 2)
        assert np.allclose(f[..., 0, 0], 3)
        assert f.domain is d
        assert f.dtype == int

        with pytest.raises(AssertionError):
            f = gMatrix(d, [2., 1])
        with pytest.raises(AssertionError):
            f = gMatrix(d, [[[2., 1]]])
        with pytest.raises(AssertionError):
            f = gMatrix(d, 1.)

    def test_gfield_creation(self):
        d = self.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        with pytest.raises(TypeError):
            f = gField(d)

        f = gField(d, 2.)
        assert type(f) == gScalar

        f = gField(d, [1, 2, 3])
        assert type(f) == gVector
        assert f.dtype == int

        f = gField(d, [1, 2, 3, 4.])
        assert type(f) == gList

        f = gField(d, [[1., 1., 0.], [1., 1., 0.], [2., 2., 1.]])
        assert type(f) == gTensor

        f = gField(d, [[1., 1., 0.], [1., 1., 0.]])
        assert type(f) == gMatrix

        r = np.random.rand(3, 3, 3)
        f = gField(d, r)
        assert type(f) == gTensor3

        r = np.random.rand(3, 3, 3, 3)
        f = gField(d, r)
        assert type(f) == gTensor4

        r = np.random.rand(3, 2, 3, 4)
        f = gField(d, r)
        assert type(f) == gField

        r = np.random.rand(ne, ng, nd, nd)
        f = gField(d, r)
        assert type(f) == gTensor

    def test_nfield_creation(self):
        coors = np.loadtxt(testdata + 'paraboloid6n.coors')
        conec = np.loadtxt(testdata + 'paraboloid6n.conec', dtype=int)
        from fempy.domain.domain import Surface3D
        d = Surface3D((coors, conec), 'tria6')
        ne = d.nelem
        ng = d.etype.ngauss
        nd = d.ndime

        from fempy.fields.nfields import nVector
        v = nVector(d)
        f = gField(d, v)

        assert type(f) == gVector
        assert f.shape == (ne, ng, nd)

    def test_tensordot_dot(self):
        d = self.domain
        t4 = gTensor4(d, 1.)
        t2 = gTensor(d, 3.)
        v = gVector(d, 4.)

        assert type(tensordot(t4, t2)) == gTensor
        assert type(tensordot(t2, t2)) == gScalar
        assert type(dot(t2, v)) == gVector
        assert type(dot(v, v)) == gScalar
        assert type(dot(t2, t2)) == gTensor


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
