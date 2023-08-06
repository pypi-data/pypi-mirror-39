# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 11:43:13 2018

@author: awitek, mwojc
"""
import numpy as np
from scipy import sparse
from fempy.models.model import Model
from fempy.fields.nfields import nScalar
from fempy.fields.gfields import gScalar, gTensor
from fempy.fields.operators import dot, grad, operator, onboundary, nabla
from fempy.fields.operators import qform, lform, integrate, ongauss, lformu
from fempy.solvers import ivp


class HeatAndMoisture(Model):
    """ Kunzel model """
    default_solver = ivp.BDFSolver

    def init(self, *args, **kwargs):
        d = self.domain
        b = self.domain.boundary
        # on domain nodes
        self.T = nScalar(d, 273.15)     # temperature [K]
        self.fi = nScalar(d, 0.5)       # relative humidity [-]
        self.bcsT = nScalar(d, False)   # Dirichlet boundary conditions mask
        self.bcsfi = nScalar(d, False)  # Dirichlet boundary conditions mask
        # on domain integration points
        # heat
        self.kij = gTensor(d)           # heat conductivity          [W/(m*K)]
        self.cp_s = gScalar(d, 1.)      # solid heat capac. (isob.)  [J/(kg*K)]
        self.rho_s = gScalar(d, 1.)     # material density           [kg/m**3]
        self.h = gScalar(d)             # heat source                [W/kg]
        # moisture
        self.Dfi = gTensor(d)           # liquid conduction coeff.   [kg/(m*s)]
        self.dp = gTensor(d)            # water vapour permeab.   [kg/(m*s*Pa)]
        self.w = gScalar(d)             # water vapour resistance factor [-]
        self.ksi = gScalar(d)           # moisture storage capacity  [kg/m**3]
        self.rho_w = gScalar(d, 1000.)  # water density              [kg/m**3]
        self.cp_w = gScalar(d, 4190.)   # water heat capac. (isob.)  [J/(kg*K)]
        # on boundary
        self.qT = gScalar(b)            # RHS explicit thermal flux  [W/m**2]
        self.qfi = gScalar(b)           # RHS exp. moisture flux  [kg/(m*s**2)]
        self.Text = gScalar(b, 273.15)  # external temperature on boundary [K]
        self.fiext = gScalar(b, 0.5)    # external r. humidity on boundary [-]
        self.alpha = gScalar(b)         # heat transfer coef.      [W/(m**2*K)]
        self.beta = gScalar(b)          # moisture transfer coef. [kg/(m**2*K)]
        # constants
        self.hv = 2257.e3               # evaporation enthalpy of water [J/kg]
        # self.sigma = 5.67036713131e-8   # Stefan-Boltzmann  [W/(m**2 * K**4)]
        # self.Mw = 0.01801528            # molar weight of water      [kg/mol]
        # self.R = 8.3144598              # universal gas constant  [J/(mol*K)]
        # self.PL = 101325.               # atmosferic pressure        [Pa]
        # solution related attributes
        self.mult = 1.0                 # multiplicator of humidity equation

    @property
    def lhs(self):
        return np.concatenate((self.T.ravel(), self.fi.ravel()))

    @lhs.setter
    def lhs(self, lhs):
        n = self.T.nsize
        shape = self.T.shape
        self.T[:] = lhs[:n].reshape(shape)
        self.fi[:] = lhs[n:].reshape(shape)

    @property
    def bcs(self):
        return np.concatenate((self.bcsT.ravel(), self.bcsfi.ravel()))

    @property
    def rhsT(self):
        T = self.T
        Tb = onboundary(T)
        # Assemble sources
        source = dot(self.rho_s, self.h)
        qs = lform(source, operator(T))
        # Assemble convective heat transfer on boundary
        transfer = dot(self.alpha, self.Text)
        qt = lform(transfer, operator(Tb))
        return lform(self.qT) + qs + qt

    @property
    def rhsfi(self):
        fi = self.fi
        fib = onboundary(fi)
        # Assemble convective moisture transfer on boundary
        transfer = dot(self.betaext, self.fiext)
        qt = lform(transfer, operator(fib))
        return (lform(self.qfi) + qt) * self.mult

    @property
    def rhs(self):
        return np.concatenate((self.rhsT.ravel(), self.rhsfi.ravel()))

    def _psat(self, T):
        return np.exp(77.3450 + 0.0057*T - 7235./T)/T**8.2

    @property
    def psat(self):  # TODO: for T<0
        T = ongauss(self.T)
        return self._psat(T)

    @property
    def psatsurf(self):
        T = ongauss(onboundary(self.T))
        return self._psat(T)

    @property
    def psatext(self):
        T = self.Text
        return self._psat(T)

    @property
    def betasurf(self):
        return self.beta*self.psatsurf

    @property
    def betaext(self):
        return self.beta*self.psatext

    @property
    def dpsatdT(self):
        return 7235./(ongauss(self.T))**2 + 0.0057

    @property
    def k11(self):
        c = self.hv * ongauss(self.fi) * self.dpsatdT
        return self.kij + dot(self.dp, c)

    @property
    def k12(self):
        c = self.hv * self.psat
        return dot(self.dp, c)

    @property
    def k21(self):
        c = ongauss(self.fi) * self.dpsatdT
        return dot(self.dp, c)

    @property
    def k22(self):
        c = self.psat
        return self.Dfi + dot(self.dp, c)

    @property
    def jac(self):
        K11 = qform(self.k11, nabla(self.T))
        K11 += qform(self.alpha, operator(onboundary(self.T)))
        K22 = qform(self.k22, nabla(self.fi))
        K22 += qform(self.betasurf, operator(onboundary(self.fi)))
        K12 = qform(self.k12, nabla(self.fi))
        K21 = qform(self.k21, nabla(self.T))
        K22 *= self.mult
        K21 *= self.mult
        return sparse.bmat([[K11, K12], [K21, K22]])

    @property
    def gradT(self):
        return grad(self.T)

    @property
    def gradfi(self):
        return grad(self.fi)

    @property
    def QT(self):
        return -dot(self.k11, self.gradT)

    @property
    def Qfi(self):
        return -dot(self.k22, self.gradfi)

    @property
    def QTfi(self):
        return -dot(self.k12, self.gradfi)

    @property
    def QfiT(self):
        return -dot(self.k21, self.gradT)

    @property
    def lopT(self):
        LT1 = -integrate(self.QT)
        LT2 = lform(dot(self.alpha, ongauss(onboundary(self.T))))
        LT3 = -integrate(self.QTfi)
        return (LT1 + LT2 + LT3).ravel()

    @property
    def lopfi(self):
        Lfi1 = -integrate(self.Qfi)
        Lfi2 = lform(dot(self.betasurf, ongauss(onboundary(self.fi))))
        Lfi3 = -integrate(self.QfiT)
        return (Lfi1 + Lfi2 + Lfi3).ravel() * self.mult

    @property
    def lop(self):
        return np.concatenate((self.lopT, self.lopfi))

    @property
    def jactT(self):
        return lformu(self.rho_s * self.cp_s + self.w * self.cp_w)

    @property
    def jactfi(self):
        return lformu(self.ksi) * self.mult

    @property
    def jact(self):
        return np.concatenate((self.jactT.ravel(), self.jactfi.ravel()))


if __name__ == '__main__':
    # from fempy.geometry.shapes import Rectangle
    # d = Rectangle().gmsh.domain()
    # m = HeatAndMoisture(d)
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
