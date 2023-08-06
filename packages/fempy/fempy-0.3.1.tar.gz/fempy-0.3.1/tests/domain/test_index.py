# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 22:47:46 2014

@author: mwojc
"""

import numpy as np
from fempy.domain.index import GlobalNIndex, NIndex, GlobalEIndex, EIndex
from common import Simple2D
import pytest


class TestSimple2DIndex(Simple2D):
    """
      6 __7__ 8
       |\ |\ |
      3|_\4_\|5
       |\ |\ |
       |_\|_\|__
      0   1  2  9

    """
    def test_global_nidx_full(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalNIndex(self.coors)
            gi.update(self.ngroups)
        assert allc(nnz(gi[:]), np.arange(10))
        assert allc(nnz(gi['cline']), [3, 4, 5])
        assert allc(nnz(gi['cline*cpoint']), [4])
        assert allc(nnz(gi['~(cline*cpoint)']), [0, 1, 2, 3, 5, 6, 7, 8, 9])
        assert allc(nnz(gi['cpoint+opoint']), [4, 9])
        assert allc(nnz(gi['cline^cpoint']), [3, 5])
        assert allc(nnz(gi['x>1.01']), [2, 5, 8, 9])
        assert allc(nnz(gi['(x>1.01) * (y>1.01)']), [8])
        with pytest.raises(KeyError):
            gi['aaa']
        with pytest.raises(KeyError):
            gi['x']
        with pytest.raises(KeyError):
            gi['x*[1,2]']

    def test_global_nidx_conec2D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalNIndex(self.coors, self.conec2D)
            gi.update(self.ngroups)
        assert len(gi[:]) == 10
        assert allc(nnz(gi[:]), np.arange(9))
        assert allc(gi.pos, [0, 1, 2, 3, 4, 5, 6, 7, 8, -1])
        assert allc(nnz(gi['cline']), [3, 4, 5])
        assert allc(nnz(gi['cline*cpoint']), [4])
        assert allc(nnz(gi['~(cline*cpoint)']), [0, 1, 2, 3, 5, 6, 7, 8])
        assert allc(nnz(gi['cpoint+opoint']), [4])
        assert allc(nnz(gi['cline^cpoint']), [3, 5])
        assert allc(nnz(gi['x>1.01']), [2, 5, 8])
        assert allc(nnz(gi['(x>1.01) * (y>1.01)']), [8])

    def test_global_nidx_conec1D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalNIndex(self.coors, self.conec1D)
            gi.update(self.ngroups)
        assert allc(nnz(gi[:]), [0, 1, 2, 3, 5, 6, 7, 8, 9])
        assert allc(gi.pos, [0, 1, 2, 3, -1, 4, 5, 6, 7, 8])
        assert allc(nnz(gi['cline']), [3, 5])
        assert allc(nnz(gi['cline*cpoint']), [])
        assert allc(nnz(gi['~(cline*cpoint)']), [0, 1, 2, 3, 5, 6, 7, 8, 9])
        assert allc(nnz(gi['cpoint+opoint']), [9])
        assert allc(nnz(gi['cline^cpoint']), [3, 5])
        assert allc(nnz(gi['x>1.01']), [2, 5, 8, 9])
        assert allc(nnz(gi['(x>1.01) * (y>1.01)']), [8])

    def test_global_nidx_conec0D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalNIndex(self.coors, self.conec0D)
            gi.update(self.ngroups)
        assert allc(nnz(gi[:]), [0, 2, 6, 8, 9])
        assert allc(gi.pos, [0, -1, 1, -1, -1, -1, 2, -1, 3, 4])
        assert allc(nnz(gi['cline']), [])
        assert allc(nnz(gi['cline*cpoint']), [])
        assert allc(nnz(gi['~(cline*cpoint)']), [0, 2, 6, 8, 9])
        assert allc(nnz(gi['cpoint+opoint']), [9])
        assert allc(nnz(gi['cline^cpoint']), [])
        assert allc(nnz(gi['x>1.01']), [2, 8, 9])
        assert allc(nnz(gi['(x>1.01) * (y>1.01)']), [8])

    def test_nidx_create_from_coors(self):
        allc = np.allclose

        ni = NIndex(self.coors)
        ni.g.update(self.ngroups)
        assert allc(ni.lst, ni.g.lst)
        assert set(ni.keys()) == set(ni.g.keys())
        self.test_global_nidx_full(ni.g)

        ni = NIndex(self.coors, self.conec1D)
        ni.g.update(self.ngroups)
        assert allc(ni.lst, ni.g.lst)
        assert set(ni.keys()) == set(ni.g.keys())
        self.test_global_nidx_conec1D(ni.g)

    def test_nidx_create_from_global(self):
        allc = np.allclose
        gi = GlobalNIndex(self.coors)
        gi.update(self.ngroups)
        ni = NIndex(gi)
        assert gi is ni.g
        assert allc(ni.lst, ni.g.lst)
        assert set(ni.keys()) == set(ni.g.keys())
        self.test_global_nidx_full(ni.g)

        ni = NIndex(gi, self.conec1D)
        assert gi is ni.g
        assert allc(ni.lst, [0, 1, 2, 3, 5, 6, 7, 8, 9])
        assert allc(ni.pos, [0, 1, 2, 3, -1, 4, 5, 6, 7, 8])
        assert set(ni.keys()) == set(ni.g.keys())
        self.test_global_nidx_full(ni.g)

    def test_nidx_create_from_local(self):
        gi = GlobalNIndex(self.coors)
        gi.update(self.ngroups)
        ni = NIndex(gi)
        with pytest.raises(ValueError):
            NIndex(ni, [0, 1, 2])

    def test_nidx_full(self, ni=None):
        if ni is None:
            ni = NIndex(self.coors)
            ni.g.update(self.ngroups)
        self.test_global_nidx_full(ni)

    def test_nidx_conec2D(self, ni=None):
        nnz = np.nonzero
        allc = np.allclose
        if ni is None:
            ni = NIndex(self.coors, self.conec2D)
            ni.g.update(self.ngroups)
        assert len(ni[:]) == 9
        assert allc(nnz(ni[:]), np.arange(9))
        assert allc(ni.pos, [0, 1, 2, 3, 4, 5, 6, 7, 8, -1])
        assert allc(nnz(ni['cline']), [3, 4, 5])
        assert allc(nnz(ni['cline*cpoint']), [4])
        assert allc(nnz(ni['~(cline*cpoint)']), [0, 1, 2, 3, 5, 6, 7, 8])
        assert allc(nnz(ni['cpoint+opoint']), [4])
        assert allc(nnz(ni['cline^cpoint']), [3, 5])
        assert allc(nnz(ni['x>1.01']), [2, 5, 8])
        assert allc(nnz(ni['(x>1.01) * (y>1.01)']), [8])

    def test_nidx_conec1Da(self, ni=None):
        nnz = np.nonzero
        allc = np.allclose
        if ni is None:
            ni = NIndex(self.coors, self.conec1D)
            ni.g.update(self.ngroups)
        assert allc(nnz(ni[:]), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        assert allc(ni.pos, [0, 1, 2, 3, -1, 4, 5, 6, 7, 8])
        assert allc(ni.g.pos, [0, 1, 2, 3, -1, 4, 5, 6, 7, 8])
        assert allc(nnz(ni['cline']), [3, 4])
        assert allc(nnz(ni['~cline']), [0, 1, 2, 5, 6, 7, 8])
        assert allc(nnz(ni['cline*cpoint']), [])
        assert allc(nnz(ni['~(cline*cpoint)']), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        assert allc(nnz(ni['cpoint+opoint']), [8])
        assert allc(nnz(ni['cline^cpoint']), [3, 4])
        assert allc(nnz(ni['x>1.01']), [2, 4, 7, 8])
        assert allc(nnz(ni['(x>1.01) * (y>1.01)']), [7])

    def test_nidx_conec1Db(self, ni=None):
        nnz = np.nonzero
        allc = np.allclose
        if ni is None:
            gi = GlobalNIndex(self.coors)
            gi.update(self.ngroups)
            ni = NIndex(gi, self.conec1D)
        assert allc(nnz(ni[:]), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        assert allc(ni.pos, [0, 1, 2, 3, -1, 4, 5, 6, 7, 8])
        assert allc(ni.g.pos, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert allc(nnz(ni['cline']), [3, 4])
        assert allc(nnz(ni['~cline']), [0, 1, 2, 5, 6, 7, 8])
        assert allc(nnz(ni['cline*cpoint']), [])
        assert allc(nnz(ni['~(cline*cpoint)']), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        assert allc(nnz(ni['cpoint+opoint']), [8])
        assert allc(nnz(ni['cline^cpoint']), [3, 4])
        assert allc(nnz(ni['x>1.01']), [2, 4, 7, 8])
        assert allc(nnz(ni['(x>1.01) * (y>1.01)']), [7])

    def test_nidx_conec0D(self, ni=None):
        nnz = np.nonzero
        allc = np.allclose
        if ni is None:
            gi = GlobalNIndex(self.coors)
            gi.update(self.ngroups)
            ni = NIndex(gi, self.conec0D)
        assert allc(nnz(ni[:]), [0, 1, 2, 3, 4])
        assert allc(ni.pos, [0, -1, 1, -1, -1, -1, 2, -1, 3, 4])
        assert allc(nnz(ni['cline']), [])
        assert allc(nnz(ni['cline*cpoint']), [])
        assert allc(nnz(ni['~(cline*cpoint)']), [0, 1, 2, 3, 4])
        assert allc(nnz(ni['cpoint+opoint']), [4])
        assert allc(nnz(ni['cline^cpoint']), [])
        assert allc(nnz(ni['x>1.01']), [1, 3, 4])
        assert allc(nnz(ni['(x>1.01) * (y>1.01)']), [3])

    def test_nidx_subindex(self):
        nnz = np.nonzero
        allc = np.allclose
        gi = GlobalNIndex(self.coors)
        gi.update(self.ngroups)
        ni = NIndex(gi, self.conec1D)
        subni = ni.subindex()
        allc(ni.lst, subni.lst)
        subni = ni.subindex('cline')
        allc(subni.lst, [3, 5])
        assert allc(nnz(subni[:]), [0, 1])
        subni = ni.subindex(gkey=self.conec0D)
        allc(subni.lst, [0, 2, 6, 8, 9])

        gi = GlobalNIndex(self.coors, self.conec2D)
        gi.update(self.ngroups)
        ni = NIndex(gi, self.conec1D)
        assert allc(ni.lst, [0, 1, 2, 3, 5, 6, 7, 8])
        subni = ni.subindex(gkey=self.conec0D)
        assert allc(subni.lst, [0, 2, 6, 8])

    def test_global_eidx_create(self):
        allc = np.allclose
        # create from coors as nindex
        gei = GlobalEIndex(self.conec2D, self.coors)
        gei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec2D(gei.nidx.g)
        self.test_nidx_conec2D(gei.nidx)
        # create from global nindex
        gni = GlobalNIndex(self.coors)
        gei = GlobalEIndex(self.conec2D, gni)
        gei.nidx.g.update(self.ngroups)
        self.test_global_nidx_full(gei.nidx.g)
        self.test_nidx_conec2D(gei.nidx)
        # create from local nindex
        ni = NIndex(self.coors, self.conec1D)
        gei = GlobalEIndex(self.conec2D, ni)
        gei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec1D(gei.nidx.g)
        assert allc(gei.nidx.lst, [0, 1, 3, 5, 7, 8])
        assert allc(gei.lst, [0, 7])  # do we really need this?

    def test_global_eidx_conec2D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalEIndex(self.conec2D, self.coors)
            gi.nidx.g.update(self.ngroups)
            self.test_global_nidx_conec2D(gi.nidx.g)
            self.test_nidx_conec2D(gi.nidx)
            gi.update(self.egroups2D)
        assert len(gi[:]) == 8
        assert allc(nnz(gi[:]), np.arange(8))
        assert allc(gi.pos, [0, 1, 2, 3, 4, 5, 6, 7])
        assert allc(nnz(gi['q2']), [2, 3])
        assert allc(nnz(gi.nidx['q2']), [1, 2, 4, 5])
        assert allc(nnz(gi['q1+q2']), [0, 1, 2, 3])
        assert allc(nnz(gi['q3+q4']), [4, 5, 6, 7])
        assert allc(nnz(gi['~(q1+q2)']), [4, 5, 6, 7])
        assert allc(nnz(gi['q1*cline']), [])     # do we really need this?
        gi.nidx.g['conec1D'] = self.conec1D
        assert allc(nnz(gi['conec1D']), [0, 7])  # do we really need this?
        assert allc(nnz(gi['conec1D*q4']), [7])  # do we really need this?
        assert allc(nnz(gi['x>0.99']), [2, 3, 6, 7])
        assert allc(nnz(gi['(x>0.99) * (y>0.99)']), [6, 7])
        assert allc(nnz(gi['(x>0.99) * (y>0.99) * conec1D']), [7])

    def test_global_eidx_conec1D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalEIndex(self.conec1D, self.coors)
            gi.nidx.g.update(self.ngroups)
            self.test_global_nidx_conec1D(gi.nidx.g)
            self.test_nidx_conec1Da(gi.nidx)
            gi.update(self.egroups1D)
            assert allc(nnz(gi.nidx.g['r*cline']), [5])
            assert allc(nnz(gi.nidx['r*cline']), [4])
        assert len(gi[:]) == 9
        assert allc(nnz(gi[:]), np.arange(9))
        assert allc(gi.pos, [0, 1, 2, 3, 4, 5, 6, 7, 8])
        with pytest.raises(KeyError):
            assert allc(nnz(gi['q2']), [2, 3])
        assert allc(nnz(gi['l']), [6, 7])
        assert allc(nnz(gi['t+l']), [4, 5, 6, 7])
        assert allc(nnz(gi['b+r']), [0, 1, 2, 3])
        assert allc(nnz(gi['~(b+r)']), [4, 5, 6, 7, 8])
        assert allc(nnz(gi['l*cline']), [])     # do we really need this?
        gi.nidx.g['conec0D'] = self.conec0D
        assert allc(nnz(gi['conec0D']), [8])  # do we really need this?
        assert allc(nnz(gi['conec0D*l']), [])  # do we really need this?
        assert allc(nnz(gi['x>0.99']), [1, 2, 3, 4, 8])
        assert allc(nnz(gi['(x>0.99) * (y>0.99)']), [3, 4])
        assert allc(nnz(gi['(x>0.99) * (y>0.99) * r']), [3])

    def test_global_eidx_conec0D(self, gi=None):
        nnz = np.nonzero
        allc = np.allclose
        if gi is None:
            gi = GlobalEIndex(self.conec0D, self.coors)
            gi.nidx.g.update(self.ngroups)
            self.test_global_nidx_conec0D(gi.nidx.g)
            self.test_nidx_conec0D(gi.nidx)
            gi.update(self.egroups0D)
            assert allc(nnz(gi.nidx.g['c5*opoint']), [9])
            assert allc(nnz(gi.nidx['c5*opoint']), [4])
        assert len(gi[:]) == 5
        assert allc(nnz(gi[:]), np.arange(5))
        assert allc(gi.pos, [0, 1, 2, 3, 4])
        with pytest.raises(KeyError):
            assert allc(nnz(gi['o']), [2, 3])
        assert allc(nnz(gi['c5']), [4])
        assert allc(nnz(gi['c1+c5']), [0, 4])
        assert allc(nnz(gi['c2+c3+c4']), [1, 2, 3])
        assert allc(nnz(gi['~(c2+c3+c4)^c5']), [0])
        assert allc(nnz(gi['c5*opoint']), [4])     # do we really need this?
        gi.nidx.g['conec2D'] = self.conec2D
        assert allc(nnz(gi['conec2D']), [0, 1, 2, 3])  # do we need this?
        assert allc(nnz(gi['conec2D*(c1+c2)']), [0, 1])  # do we need this?
        assert allc(nnz(gi['x>0.99']), [1, 3, 4])
        assert allc(nnz(gi['(x>0.99) * (y>0.99)']), [3])
        assert allc(nnz(gi['(x>0.99) * (y>0.99) * opoint']), [])

    def test_global_eidx_all(self):
        nnz = np.nonzero
        allc = np.allclose
        if not None:
            ni = GlobalNIndex(self.coors, self.conec2D)
            gi2D = GlobalEIndex(self.conec2D, ni)
            gi1D = GlobalEIndex(self.conec1D, ni)
            gi0D = GlobalEIndex(self.conec0D, ni)
            ni.update(self.ngroups)
            self.test_global_nidx_conec2D(ni)
            self.test_nidx_conec2D(gi2D.nidx)
            # self.test_nidx_conec1Da(gi1D.nidx)
            # self.test_nidx_conec0D(gi0D.nidx)
            gi2D.update(self.egroups2D)
            gi1D.update(self.egroups1D)
            gi0D.update(self.egroups0D)
        # test 2D
        assert allc(nnz(gi2D['q1*b + q1*l']), [])  # do we need this?
        # test 1D
        assert len(gi1D[:]) == 9
        assert allc(nnz(gi1D[:]), np.arange(8))
        assert allc(gi1D.pos, [0, 1, 2, 3, 4, 5, 6, 7, -1])
        assert allc(nnz(gi1D['q1*b + q1*l']), [0, 7])  # yes, we need this
        assert allc(nnz(gi1D['q1*o']), [])  # do we need this?
        assert allc(nnz(gi1D['c4+o']), [])  # do we need this?
        # test 0D
        assert len(gi0D[:]) == 5
        assert allc(nnz(gi0D[:]), np.arange(4))
        assert allc(gi0D.pos, [0, 1, 2, 3, -1])
        assert allc(nnz(gi0D['q1*c1']), [0])  # yes, we need this
        assert allc(nnz(gi0D['b*c1']), [0])  # yes, we need this
        assert allc(nnz(gi0D['b+opoint']), [0, 1])  # yes, we need this

    def test_eidx_create(self):
        allc = np.allclose
        nnz = np.nonzero
        # create from conec and coors
        with pytest.raises(ValueError):
            ei = EIndex(self.conec2D)
        ei = EIndex(self.conec2D, nidx=self.coors)
        ei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec2D(ei.nidx.g)
        self.test_nidx_conec2D(ei.nidx)
        ei.g.update(self.egroups2D)
        self.test_global_eidx_conec2D(ei.g)
        # create from conec and nindex
        ni = NIndex(self.coors, self.conec1D)
        ni.g.update(self.ngroups)
        ei = EIndex(self.conec2D, nidx=ni)
        self.test_global_nidx_conec1D(ei.nidx.g)
        assert allc(ei.nidx.lst, [0, 1, 3, 5, 7, 8])
        assert allc(ei.lst, [0, 7])
        ei.g.update(self.egroups2D)
        assert allc(nnz(ei['q4']), [1])
        assert allc(ei.subindex('q4').lst, [7])
        # create from conec and global nindex
        gni = GlobalNIndex(self.coors, self.conec1D)
        gni.update(self.ngroups)
        ei = EIndex(self.conec2D, nidx=gni)
        self.test_global_nidx_conec1D(ei.nidx.g)
        assert allc(ei.nidx.lst, [0, 1, 3, 5, 7, 8])
        assert allc(ei.lst, [0, 7])
        ei.g.update(self.egroups2D)
        assert allc(nnz(ei['q4']), [1])
        assert allc(ei.subindex('q4').lst, [7])
        # create from global eindex
        gei = GlobalEIndex(self.conec2D, gni)
        ei = EIndex(gei)
        self.test_global_nidx_conec1D(ei.nidx.g)
        assert allc(ei.nidx.lst, [0, 1, 3, 5, 7, 8])
        assert allc(ei.lst, [0, 7])
        ei.g.update(self.egroups2D)
        assert allc(nnz(ei['q4']), [1])
        assert allc(ei.subindex('q4').lst, [7])
        # create from global eindex and shadowing lst
        gei = GlobalEIndex(self.conec2D, gni)
        ei = EIndex(gei, lst=[0, 1, 2])
        self.test_global_nidx_conec1D(ei.nidx.g)
        assert allc(ei.nidx.lst, [0, 1, 3])
        assert allc(ei.lst, [0])
        ei.g.update(self.egroups2D)
        assert allc(nnz(ei['q1']), [0])
        assert allc(ei.subindex('q1').lst, [0])
        # create from global eindex and shadowing lst
        gei = GlobalEIndex(self.conec2D, gni)
        ei = EIndex(gei, lst=[0, 1, 2])
        self.test_global_nidx_conec1D(ei.nidx.g)
        assert allc(ei.nidx.lst, [0, 1, 3])
        assert allc(ei.lst, [0])
        ei.g.update(self.egroups2D)
        assert allc(nnz(ei['q1']), [0])
        assert allc(ei.subindex('q1').lst, [0])
        # create from local eindex
        with pytest.raises(ValueError):
            EIndex(ei, [0, 1, 2])

    def test_eidx_conec2D(self):
        nnz = np.nonzero
        allc = np.allclose
        ei = EIndex(self.conec2D, nidx=self.coors)
        ei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec2D(ei.nidx.g)
        self.test_nidx_conec2D(ei.nidx)
        ei.g.update(self.egroups2D)
        ei = ei.subindex([0, 1, 2, 4, 5, 6, 7])
        self.test_global_eidx_conec2D(ei.g)
        assert len(ei[:]) == 7
        assert allc(nnz(ei[:]), np.arange(7))
        assert allc(ei.pos, [0, 1, 2, -1, 3, 4, 5, 6])
        assert allc(nnz(ei['q2']), [2])
        # assert allc(nnz(ei.nidx['q2']), [1, 2, 4])   ##???
        assert allc(nnz(ei['q1+q2']), [0, 1, 2])
        assert allc(nnz(ei['q3+q4']), [3, 4, 5, 6])
        assert allc(nnz(ei['~(q1+q2)']), [3, 4, 5, 6])
        assert allc(nnz(ei['q1*cline']), [])     # do we really need this?
        ei.nidx.g['conec1D'] = self.conec1D
        assert allc(nnz(ei['conec1D']), [0, 6])  # do we really need this?
        assert allc(nnz(ei['conec1D*q4']), [6])  # do we really need this?
        assert allc(nnz(ei['x>0.99']), [2, 5, 6])
        assert allc(nnz(ei['(x>0.99) * (y>0.99)']), [5, 6])
        assert allc(nnz(ei['(x>0.99) * (y>0.99) * conec1D']), [6])

    def test_eidx_conec1D(self):
        nnz = np.nonzero
        allc = np.allclose
        ei = EIndex(self.conec1D, nidx=self.coors)
        ei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec1D(ei.nidx.g)
        self.test_nidx_conec1Da(ei.nidx)
        ei.update(self.egroups1D)
        ei = ei.subindex([0, 1, 2, 4, 5, 6, 7])
        self.test_global_eidx_conec1D(ei.g)
        assert allc(nnz(ei.nidx.g['r*cline']), [5])
        assert allc(nnz(ei.nidx['r*cline']), [4])
        assert len(ei[:]) == 7
        assert allc(nnz(ei[:]), np.arange(7))
        assert allc(ei.pos, [0, 1, 2, -1, 3, 4, 5, 6, -1])
        with pytest.raises(KeyError):
            assert allc(nnz(ei['q2']), [2, 3])
        assert allc(nnz(ei['l']), [5, 6])
        assert allc(nnz(ei['t+l']), [3, 4, 5, 6])
        assert allc(nnz(ei['b+r']), [0, 1, 2])
        assert allc(nnz(ei['~(b+r)']), [3, 4, 5, 6])
        assert allc(nnz(ei['l*cline']), [])     # do we really need this?
        ei.nidx.g['conec0D'] = self.conec0D
        assert allc(nnz(ei['conec0D']), [])  # do we really need this?
        assert allc(nnz(ei['conec0D*l']), [])  # do we really need this?
        assert allc(nnz(ei['x>0.99']), [1, 2, 3])
        assert allc(nnz(ei['(x>0.99) * (y>0.99)']), [3])
        assert allc(nnz(ei['(x>0.99) * (y>0.99) * t']), [3])

    def test_eidx_conec0D(self):
        nnz = np.nonzero
        allc = np.allclose
        ei = EIndex(self.conec0D, nidx=self.coors)
        ei.nidx.g.update(self.ngroups)
        self.test_global_nidx_conec0D(ei.nidx.g)
        self.test_nidx_conec0D(ei.nidx)
        ei.g.update(self.egroups0D)
        ei = ei.subindex([0, 1, 2, 4])
        self.test_global_eidx_conec0D(ei.g)
        assert allc(nnz(ei.nidx.g['c5*opoint']), [9])
        assert allc(nnz(ei.nidx['c5*opoint']), [3])
        assert len(ei[:]) == 4
        assert allc(nnz(ei[:]), np.arange(4))
        assert allc(ei.pos, [0, 1, 2, -1, 3])
        with pytest.raises(KeyError):
            assert allc(nnz(ei['o']), [2, 3])
        assert allc(nnz(ei['c5']), [3])
        assert allc(nnz(ei['c1+c5']), [0, 3])
        assert allc(nnz(ei['c2+c3+c4']), [1, 2])
        assert allc(nnz(ei['~(c2+c3+c4)^c5']), [0])
        assert allc(nnz(ei['c5*opoint']), [3])     # do we really need this?
        ei.nidx.g['conec2D'] = self.conec2D
        assert allc(nnz(ei['conec2D']), [0, 1, 2])  # do we need this?
        assert allc(nnz(ei['conec2D*(c1+c2)']), [0, 1])  # do we need this?
        assert allc(nnz(ei['x>0.99']), [1, 3])
        assert allc(nnz(ei['(x>0.99) * (y>0.99)']), [])
        assert allc(nnz(ei['(x>0.99) * (y>0.99) * opoint']), [])

    def test_eidx_all(self):
        nnz = np.nonzero
        allc = np.allclose
        if not None:
            gni = GlobalNIndex(self.coors, self.conec2D)
            gni.update(self.ngroups)
            gei2D = GlobalEIndex(self.conec2D, gni)
            gei1D = GlobalEIndex(self.conec1D, gni)
            gei0D = GlobalEIndex(self.conec0D, gni)
            gei2D.update(self.egroups2D)
            gei1D.update(self.egroups1D)
            gei0D.update(self.egroups0D)
            ei2D = EIndex(gei2D)
            ei1D = EIndex(gei1D)
            ei0D = EIndex(gei0D)
        # test 2D
        assert allc(nnz(ei2D['q1*b + q1*l']), [])  # do we need this?
        ei = ei2D.subindex([1, 2, 3])
        assert allc(nnz(ei['q1*b + q1*l']), [])  # do we need this?
        ei = ei2D.subindex('q1+q2')
        assert allc(nnz(ei['q1+q3']), [0, 1])  # do we need this?
        # test 1D
        assert len(ei1D[:]) == 8
        assert allc(nnz(ei1D[:]), np.arange(8))
        assert allc(ei1D.pos, [0, 1, 2, 3, 4, 5, 6, 7, -1])
        assert allc(nnz(ei1D['q1*b + q1*l']), [0, 7])  # yes, we need this
        assert allc(nnz(ei1D['q1*o']), [])  # do we need this?
        assert allc(nnz(ei1D['c4+o']), [])  # do we need this?
        ei = ei1D.subindex('b')
        assert allc(ei.pos, [0, 1, -1, -1, -1, -1, -1, -1, -1])
        assert allc(nnz(ei['q1*b + q1*l']), [0])  # yes, we need this
        # test 0D
        assert len(ei0D[:]) == 4
        assert allc(nnz(ei0D[:]), np.arange(4))
        assert allc(ei0D.pos, [0, 1, 2, 3, -1])
        assert allc(nnz(ei0D['q1*c1']), [0])  # yes, we need this
        assert allc(nnz(ei0D['b*c1']), [0])  # yes, we need this
        assert allc(nnz(ei0D['b+opoint']), [0, 1])  # yes, we need this

    def test_empty_key(self):
        nnz = np.nonzero
        allc = np.allclose
        ei = EIndex(self.conec2D, nidx=self.coors)
        assert allc(nnz(~ei[[]]), np.arange(ei.n))
        assert allc(nnz(~ei.nidx[[]]), np.arange(ei.nidx.n))
        assert allc(nnz(~ei.g[[]]), np.arange(ei.g.n))
        assert allc(nnz(~ei.nidx.g[[]]), np.arange(ei.nidx.g.n))

    def test_global_nidx_assign(self):
        i = GlobalNIndex(self.coors, self.conec2D)
        i['aaa'] = [0, 1]
        i['bbb'] = np.ones(i.n, dtype=np.bool)


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
