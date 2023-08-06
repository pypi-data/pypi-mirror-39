# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""
from fempy.models.heat import Heat


def test_p2():
    from fempy.geometry import Rectangle
    d = Rectangle(0.3, 0.1, elsize_factor=0.5).gmsh.domain(order=1)

    m = Heat(d)

    m.kij[:] = [[1., 0], [0, 1.]]

    m.alpha['left + bottom'] = 8.
    m.epsilon['left + bottom'] = 0.85
    m.Text['left + bottom'] = 293.15

    m.alpha['right + top'] = 25.
    m.epsilon['right + top'] = 0.85
    m.Text['right + top'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_s1():
    from fempy.geometry import Rectangle
    d = Rectangle(0.3, 0.1, elsize_factor=0.5).gmsh.domain(order=2)
    m = Heat(d)
    m.kij[:] = [[1., 0], [0, 1.]]

    m.alpha['left'] = 8.
    m.epsilon['left'] = 0.85
    m.Text['left'] = 293.15

    m.alpha['right'] = 25.
    m.epsilon['right'] = 0.85
    m.Text['right'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_p2_3D():
    from fempy.geometry import Gmsh
    from pygmsh.built_in import Geometry
    pg = Geometry()
    pg.add_box(0, 0.3, 0, 0.1, 0, 0.1, 0.0125)
    g = Gmsh(pg, entities={2: {19: 'right',
                               20: 'top',
                               21: 'front',
                               22: 'back',
                               23: 'bottom',
                               24: 'left'}})
    d = g.domain(order=1)
    m = Heat(d)
    m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

    m.alpha['left+bottom'] = 8.
    m.epsilon['left+bottom'] = 0.85
    m.Text['left+bottom'] = 293.15

    m.alpha['right+top'] = 25.
    m.epsilon['right+top'] = 0.85
    m.Text['right+top'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_s1_3D():
    from fempy.geometry import Gmsh
    from pygmsh.built_in import Geometry
    pg = Geometry()
    pg.add_box(0, 0.3, 0, 0.1, 0, 0.1, 0.0125)
    g = Gmsh(pg, entities={2: {19: 'right',
                               20: 'top',
                               21: 'front',
                               22: 'back',
                               23: 'bottom',
                               24: 'left'}})
    d = g.domain(order=1)
    m = Heat(d)
    m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

    m.alpha['left'] = 8.
    m.epsilon['left'] = 0.85
    m.Text['left'] = 293.15

    m.alpha['right'] = 25.
    m.epsilon['right'] = 0.85
    m.Text['right'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_3D():
    from fempy.geometry import Gmsh
    from pygmsh.built_in import Geometry
    pg = Geometry()
    pg.add_box(0, 0.3, 0, 0.1, 0, 0.1, 0.0125)
    g = Gmsh(pg, entities={2: {19: 'right',
                               20: 'top',
                               21: 'front',
                               22: 'back',
                               23: 'bottom',
                               24: 'left'}})
    d = g.domain(order=1)
    m = Heat(d)
    m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

    m.alpha['left + bottom + front'] = 8.
    m.epsilon['left + bottom + front'] = 0.85
    m.Text['left + bottom + front'] = 293.15

    m.alpha['right + top + back'] = 25.
    m.epsilon['right + top + back'] = 0.85
    m.Text['right + top + back'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_1D():
    from fempy.geometry import Point, Line
    A = Point([0, 0, 0], groups='left', elsize=0.0125)
    B = Point([0.3, 0, 0], groups='right', elsize=0.0125)
    AB = Line(A, B, groups='line')
    d = AB.gmsh.domain(2)

    m = Heat(d)
    m.kij[:] = [[1.]]

    m.alpha['left'] = 8.
    m.epsilon['left'] = 0.85
    m.Text['left'] = 293.15

    m.alpha['right'] = 25.
    m.epsilon['right'] = 0.85
    m.Text['right'] = 1273.15

    m.solve(verbose=True)
    m.preview()
    return m


def test_p2_time():
    from fempy.solvers import ivp
    from fempy.fields.operators import ongauss
    from fempy.geometry import Rectangle
    import numpy as np

    # Class
    class MyHeat(Heat):
        default_solver = ivp.BDFSolver

        def setup(self):
            m = self
            m.alpha['left + bottom'] = 8.
            m.epsilon['left + bottom'] = 0.85
            m.alpha['right + top'] = 25.
            m.epsilon['right + top'] = 0.85
            m.kij[:] = [[1, 0], [0, 1.]]
            m.rho[:] = 2300.
            m.cp[:] = 800.
            m.T[:] = 293.15
            m.Text[:] = 293.15
            m.time0 = 0.
            m.time1 = 120*60.
            self.bcs['left'] = True
            #self.bcseq = [['bottom_right', 'top_right']]

        def kij_update(self):
            T = ongauss(self.T)
            kij = self.kij
            T0 = 293.15
            k0 = 1.4
            T1 = 1273.15
            k1 = 1.0
            a = (k1 - k0) / (T1 - T0)
            I = np.eye(self.domain.ndime)

            kij[..., 0, 0] = k0 + a * (T - T0)
            kij[..., 1, 1] = k0 + a * (T - T0)
            kij[T <= T0] = I * k0
            kij[T >= T1] = I * k1

        def Text_update(self):
            t = self.time
            t0 = 0.
            Text0 = 293.15
            t1 = 60*120.
            Text1 = 1273.15
            a = (Text1 - Text0) / (t1 - t0)
            self.Text['left + bottom'] = Text0
            self.Text['right + top'] = Text0 + a*(t - t0)
            self.T['left'] = Text0 + t/9.

    # Initial state
    d = Rectangle(0.3, 0.1, elsize_factor=0.5).gmsh.domain(order=2)
    m = MyHeat(d)
    m.solve(verbose=True)
    m.preview()
    return m


test_s1()
test_p2()
test_s1_3D()
test_p2_3D()
test_3D()
test_1D()
m = test_p2_time()
