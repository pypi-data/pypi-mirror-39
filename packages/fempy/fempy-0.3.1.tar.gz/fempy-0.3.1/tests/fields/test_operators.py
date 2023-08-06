# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 11:15:18 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.operators import onnodes, onelems, ongauss, onboundary
from fempy.fields.operators import grad, div, integrate, lform, qform
from fempy.fields.operators import operator, nabla
from fempy.fields.operators import small_strain, small_rotation, divergence
from fempy.fields.algebra import transpose
from fempy.fields.nfields import nField, nScalar, nVector, nList
from fempy.fields.nfields import nTensor, nMatrix, nTensor3, nTensor4
from fempy.fields.gfields import gField, gScalar, gVector, gList
from fempy.fields.gfields import gTensor, gMatrix, gTensor3, gTensor4
from fempy.testing import testdata
from common import Simple2D


class Test_Operators_nField:
    coors = np.loadtxt(testdata + 'paraboloid6n.coors')
    conec = np.loadtxt(testdata + 'paraboloid6n.conec', dtype=int)
    from fempy.domain.domain import Surface3D
    domain = Surface3D((coors, conec), 'tria6')

    def get_fields(self):
        d = self.domain
        s = nScalar(d)
        v = nVector(d)
        l = nList(d, [1, 2, 3, 4, 5])
        t = nTensor(d)
        m = nMatrix(d, (2, 3))
        t3 = nTensor3(d)
        t4 = nTensor4(d, 1.)
        gf = m.view(nField)
        return s, v, l, t, m, t3, t4, gf

    def get_dims(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime
        ng = d.etype.ngauss
        ne = d.nelem
        return nn, nd, ne, ng

    def test_onboundary(self):
        d = Simple2D().domain2D
        u = nVector(d, 1.)
        ub = nVector(d.boundary, 1.)
        np.allclose(onboundary(u), ub)
        u = nVector(d, np.random.rand(9, 2))
        np.allclose(onboundary(u), u['boundary'])
        np.allclose(u['BOUNDARY'], u['boundary'])
        d = self.domain
        u = nVector(d)
        u[:] = np.random.rand(*u.shape)
        np.allclose(onboundary(u), u['boundary'])
        np.allclose(u['BOUNDARY'], u['boundary'])

    def test_onnodes(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()

        for f in fields:
            assert np.allclose(f, onnodes(f))

    def test_ongauss(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()
        s, v, l, t, m, t3, t4, gf = [ongauss(f) for f in fields]

        assert s.shape == (ne, ng)
        assert v.shape == (ne, ng, nd)
        assert l.shape == (ne, ng, 5)
        assert t.shape == (ne, ng, nd, nd)
        assert m.shape == (ne, ng, 2, 3)
        assert t3.shape == (ne, ng, nd, nd, nd)
        assert t4.shape == (ne, ng, nd, nd, nd, nd)
        assert type(s) == gScalar
        assert type(v) == gVector
        assert type(l) == gList
        assert type(t) == gTensor
        assert type(m) == gMatrix
        assert type(t3) == gTensor3
        assert type(t4) == gTensor4

        assert np.allclose(t4, 1.)

    def test_grad(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()
        s, v, l, t, m, t3, t4, gf = [grad(f) for f in fields]

        assert s.shape == (ne, ng, nd)
        assert v.shape == (ne, ng, nd, nd)
        assert l.shape == (ne, ng, 5, nd)
        assert t.shape == (ne, ng, nd, nd, nd)
        assert m.shape == (ne, ng, 2, 3, nd)
        assert t3.shape == (ne, ng, nd, nd, nd, nd)
        assert t4.shape == (ne, ng, nd, nd, nd, nd, nd)
        assert type(s) == gVector
        assert type(v) == gTensor
        assert type(l) == gMatrix
        assert type(t) == gTensor3
        assert type(m) == gField
        assert type(t3) == gTensor4
        assert type(t4) == gField

        assert np.allclose(t4, 0.)

    def test_div(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()
        v, t, t3, t4 = [div(f) for f in (v, t, t3, t4)]

        assert v.shape == (ne, ng)
        assert t.shape == (ne, ng, nd)
        assert t3.shape == (ne, ng, nd, nd)
        assert t4.shape == (ne, ng, nd, nd, nd)
        assert type(v) == gScalar
        assert type(t) == gVector
        assert type(t3) == gTensor
        assert type(t4) == gTensor3

        import pytest
        for f in s, l, m:
            with pytest.raises(AssertionError):
                div(f)

        assert np.allclose(t4, 0.)

    def test_integrate(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()
        s, v, l, t, m, t3, t4, gf = [integrate(grad(f)) for f in fields]

        assert s.shape == (nn,)
        assert v.shape == (nn, nd)
        assert l.shape == (nn, 5)
        assert t.shape == (nn, nd, nd)
        assert m.shape == (nn, 2, 3)
        assert t3.shape == (nn, nd, nd, nd)
        assert t4.shape == (nn, nd, nd, nd, nd)
        assert type(s) == nScalar
        assert type(v) == nVector
        assert type(l) == nList
        assert type(t) == nTensor
        assert type(m) == nMatrix
        assert type(t3) == nTensor3
        assert type(t4) == nTensor4

        assert np.allclose(t4, 0.)
        assert np.allclose(integrate(t4).sum(), 0.)

    def test_operator(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        for f in s, v, l, t, m, t3, t4:
            f[:] = np.random.rand(*f.shape)
            i = 'ijklmopq'[:f.sufix]
            j = 'rstuvwxy'[:f.sufix]
            feg = np.einsum('egn%s%s,en%s->eg%s' % (i, j, j, i),
                            operator(f), onelems(f))
            assert np.allclose(feg, ongauss(f))

    def test_nabla(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        for f in s, v, l, t, m, t3, t4:
            i = 'ijklmopq'[:f.sufix]
            j = 'rstuvwxy'[:f.sufix]
            fegk = np.einsum('egn%s%sd,en%s->eg%sd'
                             % (i, j, j, i), nabla(f), onelems(f))
            assert np.allclose(fegk, grad(f))

    def test_small_strain(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        v[:] = np.random.rand(*v.shape)
        g = grad(v)
        ss1 = 0.5*(g + transpose(g))
        ss2 = small_strain(v).gfield
        assert np.allclose(ss1, ss2)

        import pytest
        for f in s, l, t, m, t3, t4:
            with pytest.raises(AssertionError):
                small_strain(f)

    def test_small_rotation(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        v[:] = np.random.rand(*v.shape)
        g = grad(v)
        ss1 = 0.5*(g - transpose(g))
        ss2 = small_rotation(v).gfield
        assert np.allclose(ss1, ss2)

        import pytest
        for f in s, l, t, m, t3, t4:
            with pytest.raises(AssertionError):
                small_rotation(f)

    def test_divergence(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        for f in v, t, t3, t4:
            f[:] = np.random.rand(*f.shape)
            d1 = div(f)
            d2 = divergence(f).gfield
            assert np.allclose(d1, d2)

        import pytest
        for f in s, l, m:
            with pytest.raises(AssertionError):
                divergence(f)

    def test_lform(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        s[:] = 1.
        assert np.allclose(lform(s).sum(), s.domain.vol)
        v[:] = 1.
        assert np.allclose(lform(v).sum(), v.domain.vol*nd)
        t[:] = 1.
        assert np.allclose(lform(t).sum(), t.domain.vol*nd**2)
        l[:] = 1.
        assert np.allclose(lform(l).sum(), l.domain.vol*5)
        m[:] = 1.
        assert np.allclose(lform(m).sum(), m.domain.vol*6)
        # assert type(lform(m)) == nMatrix
        t3[:] = 1.
        assert np.allclose(lform(t3).sum(), t3.domain.vol*nd**3)
        t4[:] = 1.
        assert np.allclose(lform(t4).sum(), t4.domain.vol*nd**4)

        v[:] = np.random.rand(*v.shape)
        V = lform(v)
        r = V.sum(0)
        for i in range(nd):
            s[:] = v[..., i]
            assert np.allclose(lform(s).sum(), r[i])

    def test_qform(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4, gf = self.get_fields()

        u = nabla(s)
        A = t
        K = qform(A, u)
        assert K.shape == (nn,)*2

        u = nabla(v)
        A = t4
        K = qform(A, u)
        assert K.shape == (nn*nd,)*2

        u = nabla(t)
        A = gField(t.domain, np.random.rand(*(nd,)*6))  # sixth order
        K = qform(A, u)
        assert K.shape == (nn*nd*nd,)*2


class Test_Operators_gField:
    coors = np.loadtxt(testdata + 'paraboloid6n.coors')
    conec = np.loadtxt(testdata + 'paraboloid6n.conec', dtype=int)
    from fempy.domain.domain import Surface3D
    domain = Surface3D((coors, conec), 'tria6')

    def get_fields(self):
        d = self.domain
        s = gScalar(d)
        v = gVector(d)
        l = gList(d, [1, 2, 3, 4, 5])
        t = gTensor(d)
        m = gMatrix(d, (2, 3))
        t3 = gTensor3(d)
        t4 = gTensor4(d, 1.)
        return s, v, l, t, m, t3, t4

    def get_dims(self):
        d = self.domain
        nn = d.nnode
        nd = d.ndime
        ng = d.etype.ngauss
        ne = d.nelem
        return nn, nd, ne, ng

    def test_ongauss(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()

        for f in fields:
            assert np.allclose(f, ongauss(f))

    def test_onnodes(self):
        nn, nd, ne, ng = self.get_dims()
        fields = self.get_fields()
        s, v, l, t, m, t3, t4 = [onnodes(f) for f in fields]

        assert s.shape == (nn,)
        assert v.shape == (nn, nd)
        assert l.shape == (nn, 5)
        assert t.shape == (nn, nd, nd)
        assert m.shape == (nn, 2, 3)
        assert t3.shape == (nn, nd, nd, nd)
        assert t4.shape == (nn, nd, nd, nd, nd)
        assert type(s) == nScalar
        assert type(v) == nVector
        assert type(l) == nList
        assert type(t) == nTensor
        assert type(m) == nMatrix
        assert type(t3) == nTensor3
        assert type(t4) == nTensor4

        assert np.allclose(t4, 1.)

    def test_integrate(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4 = self.get_fields()
        v, t, t4 = [integrate(f) for f in (v, t, t4)]

        assert v.shape == (nn,)
        assert t.shape == (nn, nd)
        assert t4.shape == (nn, nd, nd, nd)
        assert type(v) == nScalar
        assert type(t) == nVector
        assert type(t4) == nTensor3

        assert np.allclose(t4.sum(), 0)

    def test_lform_default(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4 = self.get_fields()

        s[:] = 1.
        assert np.allclose(lform(s).sum(), s.domain.vol)
        v[:] = 1.
        assert np.allclose(lform(v).sum(), v.domain.vol*nd)
        t[:] = 1.
        assert np.allclose(lform(t).sum(), t.domain.vol*nd**2)
        l[:] = 1.
        assert np.allclose(lform(l).sum(), l.domain.vol*5)
        m[:] = 1.
        assert np.allclose(lform(m).sum(), m.domain.vol*6)
        # assert type(lform(m)) == nMatrix
        t3[:] = 1.
        assert np.allclose(lform(t3).sum(), t3.domain.vol*nd**3)
        t4[:] = 1.
        assert np.allclose(lform(t4).sum(), t4.domain.vol*nd**4)

        v[:] = np.random.rand(*v.shape)
        V = lform(v)
        r = V.sum(0)
        for i in range(nd):
            s[:] = v[..., i]
            np.allclose(lform(s).sum(), r[i])

    def test_qform_default(self):
        nn, nd, ne, ng = self.get_dims()
        s, v, l, t, m, t3, t4 = self.get_fields()

        A = t
        K = qform(A)
        assert K.shape == (nn,)*2

        A = t4
        K = qform(A)
        assert K.shape == (nn*nd,)*2

        A = gField(t.domain, np.random.rand(*(nd,)*6))  # sixth order
        K = qform(A)
        assert K.shape == (nn*nd*nd,)*2

    def test_assemble(self):
        d = Simple2D().domain2D
        dt = d['q3+q4']
        u = nVector(d)
        cijkl = gTensor4(d, 1.)
        K1 = qform(cijkl, nabla(u))
        ut = nVector(dt)
        cijklt = gTensor4(dt, 1.)
        K2 = qform(cijklt, nabla(ut))
        ub = nVector(d.boundary)
        cijklb = gTensor4(d.boundary, 1.)
        K3 = qform(cijklb, nabla(ub))
        K = K1 + K2 + K3
        assert K.shape == (18, 18)

        L1 = lform(u)
        assert L1.shape == (9, 2)

    def test_assemble_subdomain(self):
        d = Simple2D().domain2D
        dt = d['q3+q4']
        from fempy.domain.domain import Domain
        # CHANGE SUPERDOMAIN AGINST WHICH THINGS ARE ASSEMBLED
        dt2 = Domain(dt.coors, dt.conec, etype=dt.etype, egroups=dt.egroups,
                     ngroups=dt.ngroups)
        ut = nVector(dt2)
        cijklt = gTensor4(dt2, 1.)
        K2 = qform(cijklt, nabla(ut))
        ub = nVector(dt2.boundary)
        cijklb = gTensor4(dt2.boundary, 1.)
        K3 = qform(cijklb, nabla(ub))
        K = K2 + K3
        assert K.shape == (12, 12)

    def test_assemble_orphaned_point(self):
        s = Simple2D()
        from fempy.domain.index import NIndex, EIndex
        from fempy.domain.domain import Surface
        nidx = NIndex(s.coors)
        eidx = EIndex(s.conec2D, nidx=nidx)
        sd = Surface(eidx)
        # sd = Simple2D().domain2D
        # sd.coors = np.concatenate((sd.domain.coors, [[3, 3]]))  # add point
        u = nVector(sd)
        cijkl = gTensor4(sd, 1.)
        K1 = qform(cijkl, nabla(u))
        assert K1.shape == (20, 20)

        L1 = lform(u)
        assert L1.shape == (10, 2)


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
