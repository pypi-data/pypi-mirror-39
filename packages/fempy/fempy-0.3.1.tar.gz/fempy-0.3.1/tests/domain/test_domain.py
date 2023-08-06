# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 22:47:46 2014

@author: mwojc
"""

import numpy as np
from fempy.domain.domain import Domain
from fempy.domain.domain import Volume, Surface, Curve, Curve2D, Surface3D, Curve3D
from fempy.testing import testdata
from common import Simple2D, Simple3D
import pytest


class TestDomain(object):
    def call_attributes(self, e):
        e.faces
        e.boundary
        e.ndime
        e.nnode
        e.nedim
        e.nelem
        e.nenod
        e.ndeg
        e.coors
        e.conec
        e.ecoors
        e.gcoors
        e.gjac
        e.gdet
        e.gvol
        e.evol
        e.vol
        e.gijac
        e.egn
        e.egnk


class TestVolume(TestDomain):
    def test_tetr4(self):
        coors = np.loadtxt(testdata + 'cylinder4n.coors')
        conec = np.loadtxt(testdata + 'cylinder4n.conec', dtype=int)
        c = Volume((coors, conec))  # , 'tetr4')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Volume)
        self.call_attributes(d)

    def test_tetr10(self):
        coors = np.loadtxt(testdata + 'cylinder10n.coors')
        conec = np.loadtxt(testdata + 'cylinder10n.conec', dtype=int)
        c = Volume((coors, conec), 'tetr10')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Volume)
        self.call_attributes(d)


class TestSurface(TestDomain):
    def test_tria3(self):
        coors = np.loadtxt(testdata + 'circle3n.coors')
        conec = np.loadtxt(testdata + 'circle3n.conec', dtype=int)
        c = Surface((coors, conec), 'tria3')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Surface)
        self.call_attributes(d)

    def test_tria6(self):
        coors = np.loadtxt(testdata + 'circle6n.coors')
        conec = np.loadtxt(testdata + 'circle6n.conec', dtype=int)
        c = Surface((coors, conec), 'tria6')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Surface)
        self.call_attributes(d)


class TestCurve(TestDomain):
    def test_line2(self):
        coors = np.loadtxt(testdata + 'line2n.coors')
        coors.shape += (1,)
        conec = np.loadtxt(testdata + 'line2n.conec', dtype=int)
        c = Curve((coors, conec), 'line2')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Curve)
        self.call_attributes(d)

    def test_line3(self):
        coors = np.loadtxt(testdata + 'line3n.coors')
        coors.shape += (1,)
        conec = np.loadtxt(testdata + 'line3n.conec', dtype=int)
        c = Curve((coors, conec), 'line3')
        self.call_attributes(c)
        d = Domain(coors, conec)
        assert isinstance(d, Curve)
        self.call_attributes(d)


class TestCurve2D(TestDomain):
    def test_line2(self):
        coors = np.loadtxt(testdata + 'circum2n.coors')
        conec = np.loadtxt(testdata + 'circum2n.conec', dtype=int)
        c = Curve2D((coors, conec), 'line2')
        self.call_attributes(c)
        # More attributes
        c.tangent
        c.normal
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Curve2D)
        self.call_attributes(d)

    def test_line3(self):
        coors = np.loadtxt(testdata + 'circum3n.coors')
        conec = np.loadtxt(testdata + 'circum3n.conec', dtype=int)
        c = Curve2D((coors, conec), 'line3')
        self.call_attributes(c)
        c.tangent
        c.normal
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Curve2D)
        self.call_attributes(d)


class TestSurface3D(TestDomain):
    def test_tria3(self):
        coors = np.loadtxt(testdata + 'paraboloid3n.coors')
        conec = np.loadtxt(testdata + 'paraboloid3n.conec', dtype=int)
        c = Surface3D((coors, conec), 'tria3')
        self.call_attributes(c)
        c.tangent
        c.normal
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Surface3D)
        self.call_attributes(d)

    def test_tria6(self):
        coors = np.loadtxt(testdata + 'paraboloid6n.coors')
        conec = np.loadtxt(testdata + 'paraboloid6n.conec', dtype=int)
        c = Surface3D((coors, conec), 'tria6')
        self.call_attributes(c)
        c.tangent
        c.normal
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Surface3D)
        self.call_attributes(d)


class TestCurve3D(TestDomain):
    def test_line2(self):
        coors = np.loadtxt(testdata + 'spiral2n.coors')
        conec = np.loadtxt(testdata + 'spiral2n.conec', dtype=int)
        c = Curve3D((coors, conec), 'line2')
        self.call_attributes(c)
        c.tangent
        c.normal
        c.orient
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Curve3D)
        self.call_attributes(d)

    def test_line3(self):
        coors = np.loadtxt(testdata + 'spiral3n.coors')
        conec = np.loadtxt(testdata + 'spiral3n.conec', dtype=int)
        c = Curve3D((coors, conec), 'line3')
        self.call_attributes(c)
        c.tangent
        c.normal
        c.orient
        c.gjac
        d = Domain(coors, conec)
        assert isinstance(d, Curve3D)
        self.call_attributes(d)


class TestSimpleDomain2D(Simple2D):
    def test_boundary(self):
        c1 = self.conec1D[:-1]  # without last element
        c2 = self.domain2D.boundary.eidx.conec_g
        b1 = np.lexsort(c1.T)
        b2 = np.lexsort(c2.T)
        assert np.allclose(c1[b1], c2[b2])

    def test_indexing(self):
        allc = np.allclose
        nnz = np.nonzero
        d = self.domain2D
        # b = self.boundary
        assert allc(nnz(d.eidx['q2']), [2, 3])
        assert allc(nnz(d.eidx.nidx['q2']), [1, 2, 4, 5])
        assert allc(d['q2'].eidx.lst, [2, 3])
        assert allc(d['q2'].eidx.nidx.lst, [1, 2, 4, 5])
        assert d.eidx.nidx.g is d['q2'].eidx.nidx.g
        assert d.eidx.g is d['q2'].eidx.g

    def test_subdomain(self):
        allc = np.allclose
        nnz = np.nonzero
        d = self.domain2D
        d.faces.egroups['left'] = [1, 3, 4]
        q4 = d['q4']
        assert d.faces.eidx.g is q4.faces.eidx.g
        assert allc(nnz(q4.eidx.msk), [6, 7])
        assert allc(nnz(q4.eidx.nidx.msk), [4, 5, 7, 8])
        assert allc(q4.eidx.lst[q4.egroups['boundary']], [6, 7])
        assert allc(q4.eidx.lst[q4.egroups['BOUNDARY']], [7])
        assert allc(q4.eidx.lst[q4.egroups['CUT']], [6])
        assert allc(q4.faces.coors['left'], d.coors['left*q4'])
        assert allc(q4.boundary.coors['left'], d.coors['left*q4'])
        assert allc(q4.coors['q2'], d.coors['q2*q4'])
        assert allc(q4.boundary.vol, 4.)
        assert allc(q4.vol, 1.)
        assert allc(q4.boundary['q2*q4'].conec.shape[0], 1)
        assert allc(q4.faces['q2*q4'].conec.shape[0], 1)

    def test_ngroups_numbers(self):
        from fempy.fields.nfields import nScalar
        d = self.domain2D
        u = nScalar(d, np.arange(d.nnode))
        assert len(u) == 9

        b = d.boundary
        bu = nScalar(b, np.arange(b.nnode))
        assert len(bu) == 8

        bu[:] = 1
        uu = u + bu
        assert len(uu) == 9
        assert uu[0] == 1
        assert uu[4] == 4
        assert uu[5] == 6

        u[:] = 3
        buu = bu + u
        assert len(buu) == 8
        assert np.allclose(buu, 4)

        u += bu
        assert len(u) == 9
        assert u[0] == 4
        assert u[4] == 3
        assert u[5] == 4

        bu += u
        assert len(bu) == 8
        assert np.allclose(bu, 5)

    def test_ngroups_nums_indices(self):
        allc = np.allclose
        d = self.domain2D
        assert allc(d.ngroups.nums('l'), [0, 3, 6])
        assert allc(d.ngroups.nums('l', reverse=True), [6, 3, 0])
        assert allc(d.ngroups.nums('l', 'y', reverse=False), [0, 3, 6])
        assert allc(d.ngroups.nums('cross'), [2, 4, 6])
        assert allc(d.ngroups.nums('cross', 'x'), [6, 4, 2])
        assert allc(d.ngroups.nums('cross', 'y'), [2, 4, 6])
        assert allc(d.ngroups.nums('cross', 'xy'), [2, 4, 6])
        assert allc(d.ngroups.nums('cross', 'yx'), [6, 4, 2])

    def test_cached_properties(self):
        d = self.domain2D
        f = d.faces
        b = d.boundary
        d.coors
        d.gvol
        d.boundary.normal
        assert d.coors is d.__dict__['coors']
        assert d.gijac is d.__dict__['gijac']
        assert d.boundary.normal is d.boundary.__dict__['normal']
        d.invalidate_caches()
        with pytest.raises(KeyError):
            d.__dict__['coors']
        with pytest.raises(KeyError):
            d.__dict__['gijac']
        with pytest.raises(KeyError):
            d.boundary.__dict__['normal']
        assert f is d.faces
        assert b is d.boundary

    def test_update(self):
        d = self.domain2D
        coors = d.coors
        disp = np.random.rand(*coors.shape)*0.01
        d.update(disp)
        assert np.allclose(d.coors, coors+disp)
        d.update(-disp)  # recover original coors

    def test_axisymmetry(self):
        allc = np.allclose
        nnz = np.nonzero
        d = self.domain2D
        b = d.boundary

        d.axis = 'auto'
        assert allc(d.axis, 0.)
        assert allc(d.radius, d.gcoors[..., 0])
        assert allc(d.radiusn, d.coors[..., 0])
        assert allc(d.gvol, 2*np.pi*d.radius*(0.5*1*1))
        assert allc(nnz(d.ngroups['axis']), [0, 3, 6])
        assert allc(b.axis, 0.)
        assert allc(b.radius, b.gcoors[..., 0])
        assert allc(b.radiusn, b.coors[..., 0])
        assert allc(b.gvol, 2*np.pi*b.radius*(1))
        assert allc(nnz(b.eidx.nidx.g['axis']), [0, 3, 6])

        d.axis = -1.
        assert allc(d.axis, -1.)
        assert allc(d.radius, d.gcoors[..., 0]+1.)
        assert allc(d.radiusn, d.coors[..., 0]+1.)
        assert allc(d.gvol, 2*np.pi*d.radius*(0.5*1*1))
        assert allc(d.ngroups['axis'], False)
        assert allc(b.axis, -1)
        assert allc(b.radius, b.gcoors[..., 0]+1)
        assert allc(b.radiusn, b.coors[..., 0]+1)
        assert allc(b.gvol, 2*np.pi*b.radius*(1))
        assert allc(b.eidx.nidx.g['axis'], False)

        d.axis = None
        assert d.axis is None
        assert d.radius is None
        assert d.radiusn is None
        assert allc(d.gvol, (0.5*1*1))
        with pytest.raises(KeyError):
            d.ngroups['axis']
        with pytest.raises(AssertionError):
            d.axis = 1.

    def test_thickness(self):
        d = self.domain2D
        gvol = d.gvol
        d.thickness[:] = 0.1
        assert np.allclose(gvol, 10*d.gvol)
        # assert np.allclose(d.boundary.thickness, 0.1)

        d = self.domain1D
        gvol = d.gvol
        d.thickness[:] = 0.1
        assert np.allclose(gvol, 10*d.gvol)
        d.width[:] = 0.1
        assert np.allclose(gvol, 100*d.gvol)
        # assert np.allclose(d.boundary.thickness, 0.1)


class TestSimple3D(Simple3D):
    def test_boundary(self):
        idx = []
        for k in ['left', 'right', 'bottom', 'top', 'front', 'back']:
            idx += self.egroups2D[k]
        c1 = self.conec2D[idx]
        c2 = self.domain3D.boundary.eidx.conec_g
        c1.sort(1)
        c2.sort(1)
        b1 = np.lexsort(c1.T)
        b2 = np.lexsort(c2.T)
        assert np.allclose(c1[b1], c2[b2])


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
