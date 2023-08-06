# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""
from fempy.geometry.shapes import Rectangle
from fempy.models.elastic import PlaneStrain
from fempy.solvers import nonlin
import numpy as np


class MyModel(PlaneStrain):
    default_solver = nonlin.SimpleIterationSolver

    def setup(self):
        self.ev(20000, 0.3)
        self.rho[:] = 2.
        self.gravity[:] = [0., -9.81]
        self.p0 = -10.
        self.utop = -0.0005
        self.time0 = 0.
        self.time1 = 1.
        self.time = 0.

    def pressures_update(self):
        t = self.time
        p0 = self.p0
        p = np.interp(t,
                      [0, 0.25, 0.5,  1.],
                      [0, p0,   2*p0, -p0])
        self.p['left'] = p

    def displacement_update(self):
        t = self.time
        utop = self.utop
        u = np.interp(t,
                      [0, 0.5,  1.],
                      [0, utop, 0])
        self.u['top', 1] = u

    def bcs_update(self):
        # where we update bcs
        where = ('right', 0)
        # get current bcs, u and r
        bcs = self.bcs[where]
        u = self.u[where]
        r = self.res[where]
        # update bcs and u
        bcs[u > 1e-4] = True
        bcs[r > 0.] = False
        u[bcs] = 1e-4
        # assign bcs and u
        self.u[where] = u
        self.bcs[where] = bcs
        # assign other necessary bcs
        self.bcs['top', 1] = True
        self.bcs['bottom'] = True
        self.u['bottom'] = 0.


d = Rectangle(elsize=0.05).gmsh.domain(order=2)
m = MyModel(d)
m.solve(steps=50, verbose=True)
m.preview('all')
