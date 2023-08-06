# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:07:58 2016

@author: mwojc
"""
from fempy.models.model import Model
from fempy.fields.nfields import nScalar
from fempy.fields.gfields import gScalar, gTensor
from fempy.fields.operators import dot, grad, operator, onboundary, nabla
from fempy.fields.operators import qform, lform, integrate, ongauss, lformu
# import numpy as np

#from fempy.domain.tools import cached_property
#property = cached_property


class Heat(Model):
    def init(self, **kwargs):
        d = self.domain
        b = self.domain.boundary
        # on domain nodes
        self.T = nScalar(d, 273.15)     # temperature [K]
        self.bcs = nScalar(d, False)    # Dirichlet boundary conditions mask
        # on domain integration points
        self.kij = gTensor(d)           # heat conductivity        [W/m*K]
        self.cp = gScalar(d, 1.)        # heat capacity (isobaric) [J/kg*K]
        self.rho = gScalar(d, 1.)       # material density         [kg/m**3]
        self.h = gScalar(d)             # heat source              [W/kg]
        # on boundary
        self.q = gScalar(b)             # RHS explicit flux        [W/m**2]
        self.Text = gScalar(b, 273.15)  # external temperature on boundary [K]
        self.alpha = gScalar(b)         # heat transfer coefficient [W/m**2*K]
        self.beta = 5.67036713131e-8    # W/(m**2 * K**4) - Stefan-Boltzmann
        self.epsilon = gScalar(b)       # surface emissivity [-]

        # temperature is our unknown, the rest we define as properties
        self.lhs = self.T

    @property
    def gamma(self):
        Tb = ongauss(onboundary(self.T))
        Te = self.Text
        b = self.beta
        e = self.epsilon
        return (Tb**3 + Te*(Tb**2) + (Te**2)*Tb + Te**3) * b * e

    @property
    def rhs(self):
        T = self.T
        Tb = onboundary(T)
        # Assemble sources
        source = dot(self.rho, self.h)
        qs = lform(source, operator(T))
        # Assemble convective heat transfer on boundary
        transfer = dot(self.alpha, self.Text)  # ongauss(Tb) - self.Text)
        qt = lform(transfer, operator(Tb))
        # Assemble radiation at boundary
        radiation = dot(self.gamma, self.Text)
        qr = lform(radiation, operator(Tb))
        return lform(self.q) + qs + qt + qr

    @property
    def lop(self):
        L1 = -integrate(self.Q)
        L2 = lform(dot(self.alpha, ongauss(onboundary(self.T))))
        L3 = lform(dot(self.gamma, ongauss(onboundary(self.T))))
        return L1 + L2 + L3

    @property
    def jac(self):
        K1 = qform(self.kij, nabla(self.T))  # the same trial and test
        K2 = qform(self.alpha, operator(onboundary(self.T)))
        K3 = qform(self.gamma, operator(onboundary(self.T)))
        return K1 + K2 + K3

    @property
    def jact(self):
        return lformu(self.rho * self.cp)

    @property
    def gradT(self):
        return grad(self.T)

    @property
    def Q(self):
        return -dot(self.kij, self.gradT)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
#    from fempy.geometry import Rectangle
#    d = Rectangle(0.3, 0.1, elsize_factor=0.5).gmsh.domain(order=1)
#
#    m = Heat(d)
#
#    # m.k[:] = 1. #[[1., 0], [0, 1.]]
#    m.kij[:] = [[1., 0], [0, 1.]]
#
#    m.alpha['left + bottom'] = 8.
#    m.epsilon['left + bottom'] = 0.85
#    m.Text['left + bottom'] = 293.15
#
#    m.alpha['right + top'] = 25.
#    m.epsilon['right + top'] = 0.85
#    m.Text['right + top'] = 1273.15
#
##    from fempy.solvers import ivp
##    m.solver = ivp.ODESolver
##    m.time0 = 0.
##    m.time1 = 1
##    m.T[:] = 293.15
#    m.solve(verbose=True)
#    m.preview()
