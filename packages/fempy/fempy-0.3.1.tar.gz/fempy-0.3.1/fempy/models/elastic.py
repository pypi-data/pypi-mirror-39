# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:07:58 2016

@author: mwojc
"""
from fempy.models.model import Model
from fempy.fields.nfields import nVector, nScalar
from fempy.fields.gfields import gField, gScalar, gVector
from fempy.fields.gfields import gTensor, gTensor3, gTensor4
from fempy.fields.operators import dot, grad, operator, onboundary, nabla
from fempy.fields.operators import qform, lform, integrate, ongauss
from fempy.fields.operators import BaseOperator
from fempy.fields.algebra import transpose, tensordot
import fempy.solvers.linear as linear
import numpy as np


def lame2cijkl(lam, mu, ndime=3):
    """
    Works for 3D and plain strain
    """
    lam = np.asarray(lam, dtype=np.float)
    mu = np.asarray(mu, dtype=np.float)
    assert lam.shape == mu.shape
    cijkl = np.zeros(lam.shape + (ndime,)*4)
    for i in range(ndime):
        for j in range(ndime):
            cijkl[..., i, i, j, j] += lam
            cijkl[..., j, i, j, i] += mu
            cijkl[..., j, i, i, j] += mu
    return cijkl


def ev2cijkl(E, v, ndime=3):
    """
    Works for 3D and plain strain
    """
    E = np.asarray(E, dtype=np.float)
    v = np.asarray(v, dtype=np.float)
    assert E.shape == v.shape
    lam = (E*v)/((1.+v)*(1.-2.*v))
    mu = E/(2*(1.+v))
    return lame2cijkl(lam, mu, ndime)


class LinearElastic(Model):
    default_solver = linear.DirectSolver

    def init(self, **kwargs):
        d = self.domain
        b = self.domain.boundary
        # on domain nodes
        self.u = nVector(d)             # displacement
        self.f = nVector(d)             # explicit right hand side forces
        self.bcs = nVector(d, False)    # Dirichlet boundary conditions
        # on domain integration points
        self.cijkl3D = gTensor4(d)      # material tensor
        self.aij3D = gTensor(d)         # thermal expansion [1/K]
        self.rho = gScalar(d)           # material density
        self.gravity = gVector(d)       # gravity vector
        self.gravity[..., -1] = -9.80655
        self.Tref = gScalar(d, 293.15)  # reference temperature
        self.T = gScalar(d, 293.15)     # current temperature
        # on boundary integration points
        self.p = gScalar(b)             # normal pressures on boundary
        self.t = gScalar(b)             # tangential pressures on boundary
        if d.ndime == 3:
            self.t = gField(b, [0, 0.])
        self.pij = gTensor(b)           # boundary stresses - element CS
        self.pi = gVector(b)            # boundary surface forces - elemet CS
        self.qi = gVector(b)            # boundary surface forces - global CS

        # displacement is our unknown
        self.lhs = self.u

    def lame(self, lam, mu, egroups=None):
        cijkl = lame2cijkl(lam, mu)
        if egroups is None:
            self.cijkl3D[:] = cijkl
        else:
            self.cijkl3D[egroups] = cijkl

    def ev(self, E, v, egroups=None):
        cijkl = ev2cijkl(E, v)
        if egroups is None:
            self.cijkl3D[:] = cijkl
        else:
            self.cijkl3D[egroups] = cijkl

    def alpha(self, alpha, egroups=None):
        aij = np.eye(3) * alpha
        if egroups is None:
            self.aij3D[:] = aij
        else:
            self.aij3D[egroups] = aij

    @property
    def cijkl(self):
        return self.cijkl3D

    @property
    def aij(self):
        return self.aij3D

    @property
    def rhs(self):
        u = self.u
        b = self.domain.boundary
        # Assemble body forces - weight
        weight = dot(self.rho, self.gravity)
        fw = lform(weight, operator(u))
        # Assemble boundary surface forces
        qi = dot(self.pij, b.normal)
        qi += dot(b.normal, self.p)
        qi += dot(b.tangent, self.t)
        qi += dot(transpose(b.uvw), self.pi)
        qi += self.qi
        fb = lform(qi, operator(onboundary(u)))
        # Assemble thermal load
        fdT = integrate(self.sigma_dT)  # should be lform(sigma_dT, bu)
        return self.f + fw + fb + fdT

    @property
    def jac(self):
        # Assemble stiffness matrix
        u = self.u
        nu = nabla(u)
        bu = 0.5*(nu + transpose(nu))     # small strain operator
        return qform(self.cijkl, bu, bu)  # the same trial and test

    @property
    def eps(self):
        du = grad(self.u)
        eps = 0.5*(du + transpose(du))
        return eps

    @property
    def rot(self):
        du = grad(self.u)
        rot = 0.5*(du - transpose(du))
        return rot

    @property
    def dT(self):
        return self.T - self.Tref

    @property
    def eps_dT(self):
        return dot(self.aij, self.dT)

    @property
    def sigma_dT(self):
        sigma_dT = tensordot(self.cijkl, self.eps_dT)
        return sigma_dT

    @property
    def sigma(self):
        sigma = tensordot(self.cijkl, self.eps - self.eps_dT)
        return sigma

    @property
    def lop(self):
        sigma_tot = tensordot(self.cijkl, self.eps)
        return integrate(sigma_tot)


class LinearElastic3D(LinearElastic):
    def init(self, *args, **kwargs):
        nd = self.domain.ndime
        ed = self.domain.etype.ndime
        assert nd == 3 and ed == 3, "3D domain is required"
        LinearElastic.init(self, **kwargs)


class LinearElastic2D(LinearElastic):
    def init(self, *args, **kwargs):
        nd = self.domain.ndime
        ed = self.domain.etype.ndime
        assert nd == 2 and ed == 2, "2D domain is required"
        LinearElastic.init(self, **kwargs)
        self.cijkl3D = gField(self.domain, np.zeros((3, 3, 3, 3)))
        self.aij3D = gField(self.domain, np.zeros((3, 3)))

    @property
    def cijkl(self):
        return gTensor4(self.domain, self.cijkl3D[..., :2, :2, :2, :2])

    @property
    def aij(self):
        return gTensor(self.domain, self.aij3D[..., :2, :2])

    @property
    def c2222(self):
        return gScalar(self.domain, self.cijkl3D[..., 2, 2, 2, 2])

    @property
    def c0022(self):
        return gScalar(self.domain, self.cijkl3D[..., 0, 0, 2, 2])

    @property
    def c1122(self):
        return gScalar(self.domain, self.cijkl3D[..., 1, 1, 2, 2])

    @property
    def aij22(self):
        return gScalar(self.domain, self.aij3D[..., 2, 2])


class PlaneStrain(LinearElastic2D):
    @property
    def sigma_dT(self):
        sigma_dT = super(PlaneStrain, self).sigma_dT
        sigma_dT[..., 0, 0] += self.c0022 * self.aij22 * self.dT
        sigma_dT[..., 1, 1] += self.c1122 * self.aij22 * self.dT
        return sigma_dT

    @property
    def sigmaz(self):
        eps = self.eps - self.eps_dT
        c0011 = self.cijkl[..., 0, 0, 1, 1]
        c0000 = self.cijkl[..., 0, 0, 0, 0]
        eps00 = eps[..., 0, 0]
        eps11 = eps[..., 1, 1]
        sig33 = c0011 * (eps00 + eps11) - c0000*self.eps_dT[..., 0, 0]
        return gScalar(self.domain, sig33)


class PlaneStress(LinearElastic2D):
    @property
    def cijkl(self):
        cijkl = gTensor4(self.domain, self.cijkl3D[..., :2, :2, :2, :2].copy())
        c0011 = cijkl[..., 0, 0, 1, 1]
        c0000 = cijkl[..., 0, 0, 0, 0]
        corr = (c0011**2)/c0000
        cijkl[..., 0, 0, 0, 0] -= corr
        cijkl[..., 0, 0, 1, 1] -= corr
        cijkl[..., 1, 1, 0, 0] -= corr
        cijkl[..., 1, 1, 1, 1] -= corr
        return cijkl

    @property
    def epsz(self):
        eps_dT = self.eps_dT
        eps = self.eps - eps_dT
        c0000 = self.cijkl[..., 0, 0, 0, 0]
        c0011 = self.cijkl[..., 0, 0, 1, 1]
        eps00 = eps[..., 0, 0]
        eps11 = eps[..., 1, 1]
        eps33 = -(c0011/c0000) * (eps00 + eps11) + eps_dT[..., 0, 0]  # isotropic
        return gScalar(self.domain, eps33)


class Axisymmetry(PlaneStrain):
    def init(self, **kwargs):
        PlaneStrain.init(self, **kwargs)
        axis = kwargs.pop('axis', 'auto')
        self.domain.axis = axis
        self.bcs['axis', 0] = True  # fix horizontal disp

    @property
    def radius(self):
        return self.domain.radius

    @property
    def epsz(self):
        epsz = ongauss(self.u)[..., 0] / self.radius
        return gScalar(self.domain, epsz)

    @property
    def sigmaz(self):
        eps = self.eps
        epsx = eps[..., 0, 0]
        epsy = eps[..., 1, 1]
        epsz = self.epsz
        sigmaz = self.cijkl[..., 0, 0, 1, 1] * (epsx + epsy) + \
            self.cijkl[..., 1, 1, 1, 1] * epsz
        return gScalar(self.domain, sigmaz)

    @property
    def sigma(self):
        sigma = tensordot(self.cijkl, self.eps)
        dsigma = self.cijkl[..., 0, 0, 1, 1] * self.epsz
        sigma[..., 0, 0] += dsigma
        sigma[..., 1, 1] += dsigma
        return sigma

    @property
    def lop(self):
        # Integrate in-plane stresses
        sigma = self.sigma
        integral = integrate(sigma)
        # Must add sigmaz contribution to first equation
        integralz = lform(self.sigmaz/self.radius)
        integral[..., 0] += integralz
        return integral

    @property
    def jac(self):
        # Plane strain part (non-linar solver works with this part only :))
        u = self.lhs
        nu = nabla(u)
        bu = 0.5*(nu + transpose(nu))     # small strain operator
        K1 = qform(self.cijkl, bu, bu)
        # Contribution of epsz on sigmax and sigmay and symmetrically
        # contribution of epsx and epsy on sigmaz
        r = self.radius
        ou = operator(u)[..., 0]  # radial displacement operator (u_0)
        ou = BaseOperator(u, ou)  # TODO: rethink general operator creation
        c0011 = self.cijkl[..., 0, 0, 1, 1]/r     # lambda/r
        dij = gTensor(self.domain)
        dij[..., 0, 0] = c0011
        dij[..., 1, 1] = c0011
        K2 = qform(dij, bu, ou)
        K3 = qform(dij, ou, bu)
        # Contribution of eps22 on sigma22
        c1111 = self.cijkl[..., 1, 1, 1, 1]/r**2  # (lambda + 2*mu)/r**2
        h = gScalar(self.domain, c1111)
        K4 = qform(h, ou, ou)
        # Sum and return
        # Note: resulting jacobian is not symmetric anymore...
        return K1 + K2 + K3 + K4


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
