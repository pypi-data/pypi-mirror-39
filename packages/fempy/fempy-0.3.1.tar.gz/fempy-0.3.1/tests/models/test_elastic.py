# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:17:33 2016

@author: mwojc
"""
from fempy.domain.domain import Domain
import fempy.models.elastic as elastic
from fempy.solvers.tools import model_test
from fempy.testing import testdata
import common
import numpy as np


class Test_Elastic(object):
    def test_mesh1_strain(self):
        coors = np.loadtxt(testdata + '/elastic/mesh1.coors')
        conec = np.loadtxt(testdata + '/elastic/mesh1.conec',
                           dtype=int)
        sol = np.loadtxt(testdata + '/elastic/mesh1.pstrain.sol')

        d = Domain(coors, conec)
        d.eidx.nidx.g._vars['tol'] = 1e-7
        m = elastic.PlaneStrain(d)
        # material
        m.ev(30000., 0.2)
        m.gravity[:] = [0., -9.80665]
        m.rho[:] = 20./9.80665
        # boundary conditions
        m.bcs['x<tol', 0] = True       # left
        m.bcs['x>2-tol', 0] = True     # right
        m.bcs['y<tol'] = True          # bottom
        # load
        m.p['(y>1-tol)*(x>1-tol)'] = -100.

        m.solve()
        # m.preview()

        assert np.allclose(m.lhs, sol)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_mesh1_axisym(self):
        coors = np.loadtxt(testdata + '/elastic/mesh1.coors')
        conec = np.loadtxt(testdata + '/elastic/mesh1.conec',
                           dtype=int)
        sol = np.loadtxt(testdata + '/elastic/mesh1.axisym.sol')

        d = Domain(coors, conec)
        d.eidx.nidx.g._vars['tol'] = 1e-7
        m = elastic.Axisymmetry(d)
        # material
        m.ev(30000., 0.2)
        m.gravity[:] = [0., -9.80665]
        m.rho[:] = 20./9.80665
        # boundary conditions
        m.bcs['x<tol', 0] = True       # left
        m.bcs['x>2-tol', 0] = True     # right
        m.bcs['y<tol'] = True          # bottom
        # load
        m.p['(y>1-tol)*(x>1-tol)'] = -100.

        m.solve()
        # m.preview()

        assert np.allclose(m.lhs, sol)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_mesh2_pstrain(self):
        coors = np.loadtxt(testdata + '/elastic/mesh2.coors')
        conec = np.loadtxt(testdata + '/elastic/mesh2.conec',
                           dtype=int)
        sol = np.loadtxt(testdata + '/elastic/mesh2.pstrain.sol')

        d = Domain(coors, conec)
        d.eidx.nidx.g._vars['tol'] = 1e-7
        d.eidx.nidx.g._vars['r'] = 2./2.
        m = elastic.PlaneStrain(d)
        m.ev(30000, 0.2)
        # boundary conditions
        m.bcs['(np.abs(x)<tol)*(np.abs(y)<r+tol)', 0] = True
        m.bcs['(np.abs(y)<tol)*(np.abs(x)<r+tol)', 1] = True
        # load
        m.p['(x<x.min()+tol)'] = 100.  # bottom
        m.p['(x>x.max()-tol)'] = 100.  # top

        m.solve()
        # m.preview()

        assert np.allclose(m.lhs, sol)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_simple_pstrain(self):
        sol = np.loadtxt(testdata + '/elastic/simple.pstrain.sol')
        d = common.Simple2D().domain2Dmv([0.1, 0.1])
        m = elastic.PlaneStrain(d)
        m.ev(1000., 0.25)
        m.bcs['l', 0] = True
        m.bcs['c1'] = True
        m.p['r'] = 5.
        m.solve()
        # m.preview()
        assert np.allclose(m.lhs, sol, atol=1e-7)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_simple_pstress(self):
        sol = np.loadtxt(testdata + '/elastic/simple.pstress.sol')
        d = common.Simple2D().domain2Dmv([0.1, 0.1])
        m = elastic.PlaneStress(d)
        m.domain.thickness[:] = 0.1
        m.domain.boundary.thickness[:] = 0.1
        m.ev(1000., 0.25)
        m.bcs['l', 0] = True
        m.bcs['c1'] = True
        m.p['r'] = 5.
        m.solve()
        # m.preview()
        assert np.allclose(m.lhs, sol)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_simple_axisym(self):
        sol = np.loadtxt(testdata + '/elastic/simple.axisym.sol')
        d = common.Simple2D().domain2Dmv([0.1, 0.1])
        m = elastic.Axisymmetry(d)
        m.ev(1000., 0.25)
        m.bcs['l', 0] = True
        m.bcs['c1'] = True
        m.p['r'] = 5.
        m.solve()
        # m.preview()
        assert np.allclose(m.lhs, sol)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_simple_3D(self):
        sol = np.loadtxt(testdata + '/elastic/simple.3D.sol')
        d = common.Simple3D().domain3D
        m = elastic.LinearElastic3D(d)
        m.ev(1000., 0.25)
        m.bcs['left', 1] = True
        m.bcs['bottom*left'] = True
        m.p['right'] = 5.
        m.solve()
#        m.preview()
        assert np.allclose(m.lhs, sol, atol=1e-7)
        assert np.allclose(m.jac_times_lhs, m.lop)
        model_test(m, x0=sol)

    def test_thermal_plane_strain(self):
        class Thermal3D(elastic.LinearElastic3D):
            def setup_domain(self):
                from fempy.geometry.shapes import Box
                self.geometry = Box(10, 1, 10, elsize=0.5)
                self.domain = self.geometry.gmsh.domain()

            def setup_model(self):
                self.bcs['left'] = [False, True, False]
                self.bcs['right'] = [False, True, False]
                self.bcs['back*left*bottom'] = [True, True, True]
                self.bcs['front*left*bottom'] = [False, True, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 3.

        class Thermal2DPlaneStrain(elastic.PlaneStrain):
            def setup_domain(self):
                from fempy.geometry.shapes import Rectangle
                self.geometry = Rectangle(10, 10, lb=(0, 0), elsize=0.5)
                self.domain = self.geometry.gmsh.domain()

            def setup_model(self):
                self.bcs['bottom_left'] = [True, True]
                self.bcs['bottom_right'] = [False, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 3.

        m3D = Thermal3D()
        m3D.solve()
#        from fempy.geometry.gmsh_io import preview_field
#        preview_field(m3D.sigma[..., 1, 1], name='sigmaz', d=m3D.domain)
        assert np.allclose(m3D.sigma[..., 1, 1], -6.)
        assert np.allclose(m3D.res.sum(), 0.)
        assert np.allclose(m3D.res['~(left+right)'], 0.)

        m2D = Thermal2DPlaneStrain()
        m2D.solve()
        # from fempy.geometry.gmsh_io import preview_field
        # preview_field(m2D.sigmaz, name='sigmaz', d=m2D.domain)
        assert np.allclose(m2D.sigmaz, -6.)
        assert np.allclose(m2D.res.sum(), 0.)
        assert np.allclose(m2D.res['~(bottom_left+bottom_right)'], 0.)

    def test_thermal_plane_strain_dist(self):
        class Thermal3D(elastic.LinearElastic3D):
            def setup_domain(self):
                from fempy.geometry.shapes import Box
                self.geometry = Box(10, 1, 10, elsize=0.5)
                self.domain = self.geometry.gmsh.domain(1)

            def setup_model(self):
                self.bcs['left'] = [False, True, False]
                self.bcs['right'] = [False, True, False]
                self.bcs['back*left*bottom'] = [True, True, True]
                self.bcs['front*left*bottom'] = [False, True, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 1*self.domain.gcoors[..., 0]

        class Thermal2DPlaneStrain(elastic.PlaneStrain):
            def setup_domain(self):
                from fempy.geometry.shapes import Rectangle
                self.geometry = Rectangle(10, 10, lb=(0, 0), elsize=0.5)
                self.domain = self.geometry.gmsh.domain(1)

            def setup_model(self):
                self.bcs['bottom_left'] = [True, True]
                self.bcs['bottom_right'] = [False, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 1*self.domain.gcoors[..., 0]

        m3D = Thermal3D()
        m3D.solve()
#        from fempy.geometry.gmsh_io import preview_field
#        preview_field(m3D.sigma[..., 1, 1], name='sigmaz', d=m3D.domain)
        assert np.allclose(m3D.res.sum(), 0.)
        assert np.allclose(m3D.res['~(left+right)'], 0.)

        m2D = Thermal2DPlaneStrain()
        m2D.solve()
#        from fempy.geometry.gmsh_io import preview_field
#        preview_field(m2D.sigmaz, name='sigmaz', d=m2D.domain)
        assert np.allclose(m2D.res.sum(), 0.)
        assert np.allclose(m2D.res['~(bottom_left+bottom_right)'], 0.)

        # Solutions should be close
        assert np.allclose(m2D.u.max(), m3D.u.max(), 4)

    def test_thermal_plane_stress(self):
        class Thermal3D(elastic.LinearElastic3D):
            def setup_domain(self):
                from fempy.geometry.shapes import Box
                self.geometry = Box(10, 1, 10, elsize=0.5)
                self.domain = self.geometry.gmsh.domain()

            def setup_model(self):
                # self.bcs['left'] = [False, True, False]
                # self.bcs['right'] = [False, True, False]
                self.bcs['back*left*bottom'] = [True, True, True]
                self.bcs['front*left*bottom'] = [False, False, True]
                self.bcs['back*right*bottom'] = [True, False, False]
                self.bcs['back*left*top'] = [False, True, False]
                # self.bcs['abc'] = [True, True, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 3.

        class Thermal2DPlaneStress(elastic.PlaneStress):
            def setup_domain(self):
                from fempy.geometry.shapes import Rectangle
                self.geometry = Rectangle(10, 10, lb=(0, 0), elsize=0.5)
                self.domain = self.geometry.gmsh.domain()

            def setup_model(self):
                self.bcs['bottom_left'] = [True, True]
                self.bcs['bottom_right'] = [False, True]
                self.ev(20000., 0.3)
                self.alpha(1e-4)
                self.T[:] += 3.

        m3D = Thermal3D()
        m3D.solve()
#        from fempy.geometry.gmsh_io import preview_field
#        preview_field(m3D.eps[..., 1, 1], name='epsz', d=m3D.domain)
        assert np.allclose(m3D.eps[..., 1, 1], 0.0003)

        m2D = Thermal2DPlaneStress()
        m2D.solve()
#        from fempy.geometry.gmsh_io import preview_field
#        preview_field(m2D.epsz, name='epsz', d=m2D.domain)
        assert np.allclose(m2D.epsz, 0.0003)


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
