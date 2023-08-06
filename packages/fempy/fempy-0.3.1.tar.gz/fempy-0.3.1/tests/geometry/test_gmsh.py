# -*- coding: utf-8 -*-
import os
import pytest
import tempfile
import numpy as np
from fempy.geometry import *
import fempy.testing as testing

testdata = testing.testdata  # dir for test data
tempdir = tempfile.gettempdir()


# WRITE BETTER TESTS PLEASE!
class TestGmsh:
    def test_save_read(self):
        #from fempy.geometry import Rectangle
        R = Rectangle()
        R.gmsh.save(tempdir + '/rectangle')
        GR = Gmsh((tempdir + '/rectangle.geo', tempdir + '/rectangle.msh'))
        # GR.preview()
        GR = Gmsh(tempdir + '/rectangle.geo')
        # GR.preview()
        GR = Gmsh(tempdir + '/rectangle.msh')
        # GR.preview()
        GR.domain()

    def test_geo_input(self):
        for name in os.listdir(testdata + '/gmsh'):
            n = testdata + '/gmsh/' + name
            if name.endswith('.geo'):
                gm = Gmsh(n)
                d = gm.domain()
                assert d.nelem > 0

    def test_msh_input(self):
        for name in os.listdir(testdata + '/gmsh'):
            n = testdata + '/gmsh/' + name
            if name.endswith('.geo'):
                gm = Gmsh(n)
                d1 = gm.domain()
                mn = tempdir + '/' + name[:-4] + '.msh'
                gm.save(mn)
                # re-read msh and test
                gm = Gmsh(mn)
                d2 = gm.domain()
                assert np.allclose(d1.conec, d2.conec)
            elif name.endswith('.msh'):
                gm = Gmsh(n)
                d = gm.domain()
                assert d.nelem > 0

    def test_brep_input(self):
        for name in os.listdir(testdata + '/gmsh'):
            n = testdata + '/gmsh/' + name
            if name.endswith('.brep'):
                gm = Gmsh(n)
                d = gm.domain()
                assert d.nelem > 0

    def test_iges_input(self):
        for name in os.listdir(testdata + '/gmsh'):
            n = testdata + '/gmsh/' + name
            if name.endswith('.iges'):
                gm = Gmsh(n)
                d = gm.domain()
                assert d.nelem > 0

    def test_pygmsh_input(self):
        pytest.importorskip("pygmsh")
        from fempy.models.elastic import LinearElastic
        # 3D
        from fempy.geometry import Gmsh
        from pygmsh.built_in import Geometry
        pg = Geometry()
        pg.add_box(0, 0.3, 0, 0.1, 0, 0.1, 0.025)
        g = Gmsh(pg, entities={2: {19: 'right',
                                   20: 'top',
                                   21: 'front',
                                   22: 'back',
                                   23: 'bottom',
                                   24: 'left'}})
        d = g.domain(order=1)
        assert d.nelem > 0

    def test_geometry_input(self):
        R = Rectangle()
        gm = Gmsh(R)
        d = gm.domain()
        assert d.nelem > 0

    def test_multiple_physical_names(self):
        d = testing.common.SquareWithCircle()
        assert np.allclose(d.vol, 1.)
        assert np.allclose(d.boundary.vol, 4.)
        assert d['r'].nelem + d['c'].nelem == d.nelem
        assert d['domain'].nelem == d.nelem


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
