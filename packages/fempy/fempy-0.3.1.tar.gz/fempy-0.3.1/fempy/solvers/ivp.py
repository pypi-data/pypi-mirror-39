# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 19:09:58 2016

@author: mwojc
"""
from __future__ import print_function
import warnings
import scipy.sparse
from scipy.integrate import solve_ivp
from scipy.optimize.nonlin import KrylovJacobian
import numpy as np
from fempy.solvers import linear
from fempy.solvers import _bdf

hasattr = linear.hasattr


def _identity_like(A, n=None):
    if A is None:
        return
    if n is None:
        n = A.shape[0]
    if scipy.sparse.issparse(A):
        I = scipy.sparse.eye(n, dtype=A.dtype, format=A.format)
    else:  # is dense
        I = np.eye(n, dtype=A.dtype)
    return I


def _set_solution_at_time(m, t=None):
    if t is None:
        t = m._sol.t[-1]
    tmin = m._sol.t[0]
    tmax = m._sol.t[-1]
    if t < tmin or t > tmax:
        warnings.warn("Time {} lays outside the solution range: (t0, t1) = "
                      "({}, {})".format(float(t), m.time0, m.time1))
    # assign time
    m.time = t
    # get solution from dense output
    x = m._sol.sol(t)
    # set solution and update
    linear._set_solution(m, x)
    m.update()
    return m.lhs.copy()


class ODESolver(linear.LinearSolver):
    ode_solver = 'BDF'
    default_options = {'verbose': False}

    def _divide_by_jact(self, v):
        if hasattr(self.model, 'jact'):
            v[:self.nlhs] /= self.model.jact
        if hasattr(self.model, 'jaclmt'):
            v[self.nlhs:] /= self.model.jaclmt
        return v

    def _divide_matrix_by_jact(self, A, jact):
        if scipy.sparse.issparse(A):
            A = A.multiply(1./jact[:, None]).tocsr()
        else:
            A = A/jact[:, None]
        return A

    def _update_K(self):
        super(ODESolver, self)._update_K()
        if self.K is not None and hasattr(self.model, 'jact'):
            self.K = self._divide_matrix_by_jact(self.K, self.model.jact)

    def _update_B(self):
        super(ODESolver, self)._update_B()
        if self.B is not None and hasattr(self.model, 'jaclmt'):
            self.B = self._divide_matrix_by_jact(self.B, self.model.jaclmt)
            self.BT = self.B.T

    @property
    def b(self):
        b = super(ODESolver, self).b
        return self._divide_by_jact(b)

    @property
    def l(self):
        l = super(ODESolver, self).l
        return self._divide_by_jact(l)

    @property
    def r(self):
        # This is faster then simply self.l - self.b
        # because division is made once
        r = super(ODESolver, self).l - super(ODESolver, self).b
        return self._divide_by_jact(r)

    def residual(self, t, x, verbose=True):
        self.update_model(t, x)
        self.x
        r = -self.r
        if self._verbose and verbose:
            print('{:10f}: residual called'.format(t))
        return r

    def jacobian(self, t, x):
        self._update_K()
        self._update_B()
        jac = self.Jsparse
        if jac is None:
            raise ValueError("'%s' solver needs jacobian" % (self.ode_solver))
        if self._verbose:
            print('{:10f}: jacobian updated'.format(t))
        return -jac

    def getopts(self, options):
        options = super(ODESolver, self).getopts(options)
        self._verbose = options['verbose']
        del options['verbose']  # solve_ivp does not accept verbose
        return options

    def solve(self, **options):
        options = self.getopts(options)
        t_span = (self.model.time0, self.model.time1)
        ode_solver = self.ode_solver
        jacobian = self.jacobian
        sol = solve_ivp(self.residual, t_span, self.x,
                        method=ode_solver, jac=jacobian,
                        dense_output=True, **options)
        # Make sure last solution is applied to the model
        self.model._sol = sol
        self.model.__class__.sol = _set_solution_at_time
        self.model.sol()  # This sets sotution at last time step

    def update_model(self, t=None, x=None):
        if t is not None:
            self.model.time = t
        super(ODESolver, self).update_model(x)

    def update(self, t=None, x=None, f=None):
        # assign x to model and call its update if it exists
        self.update_model(t, x)
        # clear current data grab new data from model
        self.clear()
        self.x0 = self.x  # here we set also all shaping data
        self._update_K()
        self._update_B()
        self._update_P()
        self._update_Klm()
        self._update_Mlm()


class BDFSolverDS(ODESolver):
    # ode_solver = 'BDF'
    pass


class RadauSolverDS(ODESolver):
    ode_solver = 'Radau'


# class LSODASolverDS(ODESolver):  # NOT WORKING CURRENTLY...
#    ode_solver = 'LSODA'
#
#    def jacobian(self, t, x):
#        jac = super(LSODASolverDS, self).jacobian(t, x)
#        return jac.toarray()


class BDFSolver(ODESolver):
    ode_solver = _bdf.FempyBDF

    def update(self, t=None, x=None):
        self.update_model(t, x)
        self.clear()
        self.x0 = self.x  # here we set also all shaping data
        self._update_K()
        self._update_B()
        # self._update_P()
        # self._update_Klm()
        # self._update_Mlm()
        self.K0 = self.K
        self.B0 = self.B
        self.BT0 = self.BT
        self.I = _identity_like(self.K0)
        if self.nlm:
            self.Ilm = _identity_like(self.B, n=len(self.B)) 
        if self.K is None:
            self.t0 = self.model.time
            self.y0 = self.x0
            self.f0 = self.residual(self.t0, self.y0)
        if self._verbose:
            print('{:10f}: jacobian updated'.format(self.model.time))

    def update_c(self, c):
        self.c = c
        if self.K is not None:
            self.K = self.I - c * self.K0
            if self.nlm:
                self.B = -c * self.B0
                self.BT = -c * self.BT0
            self._update_P()
            self._update_Klm()
            if self.Klm is not None:
                self.Klm -= self.Ilm  # take Ilm into account
            self._update_Mlm()

    # Unfortunately ne need to hack update_P.
    # This is because our jacobian is now not K, but I - c*K and changes are
    # needed to properly handle bcs and bcseq. Possibly this could be
    # better done (but not here i think, in linear solver rather).
    def _update_P(self):
        K = self.K
        nbcs = self.nbcs
        nbcseq = self.nbcseq
        pre = self.preconditioner if hasattr(self, 'preconditioner') else None
        if K is None or pre is None:
            self.P = None
            return
        if not nbcs and not nbcseq:
            P = pre(K)  # LOP or sp matrix
        else:
            bcsr = self.bcsr.copy()
            c = self.c
            if nbcseq:
                K = K.copy()  # this is safe but this is a copy...
                # TODO: K should not be copied here at all
                c0, c1, c2 = self.bcseqc
                bcseq0 = self.bcseq0
                bcseq1 = self.bcseq1
                c01 = c0/c1 * (-c / (1. - c))  # WE HACK HERE ...
                K[bcseq0] += K[bcseq1]
                K[bcseq0, bcseq1] -= 1.  # ... AND HERE ...
                K[:, bcseq0] -= linear._multiply(K[:, bcseq1], c01)
                bcsr[bcseq1] = True
            K0 = K[~bcsr]
            K0 = K0[:, ~bcsr]
            Kbcs = K[:, bcsr]
            P0 = pre(K0)  # LOP or sp matrix

            def matvec(b):
                b = b.copy()  # need a copy, to not alter original b
                b[bcsr] /= (1. - self.c)  # ... AND HERE
                bbcs = (Kbcs.dot(b[bcsr]))[~bcsr]  # b carries x at bcsr
                b0 = b[~bcsr] - bbcs
                x0 = P0.dot(b0)
                x = b.copy()                     # copies also x at bcsr
                x[~bcsr] = x0
                if nbcseq:
                    x[bcseq1] -= c01 * x[bcseq0]
                return x
            P = linear.LOP(K.shape, dtype=K.dtype, matvec=matvec)  # LOP
        self.P = P

    # Get also consistent J (for I - c*K)
    def _matvecJ(self, x):
        ll = super(self.__class__, self)._matvecJ(x)
        if self.nlm:
            ll[-self.nlm:] += x[-self.nlm:]  # add Ilm*lmbd
        if self.nbcs:
            ll[:self.nlhs][self.bcsr] += -self.c * x[:self.nlhs][self.bcsr]
        if self.nbcseq:
            ll[:self.nlhs][self.bcseq1] *= -self.c
            ll[:self.nlhs][self.bcseq1] += x[self.bcseq1]
            ll[:self.nlhs][self.bcseq0] -= x[self.bcseq1]
        return ll

    # and Jsparse ...
    @property
    def Jsparse(self):
        Js = super(self.__class__, self).Jsparse.tocsc()
        if self.nlm:
            idx = np.arange(self.nlhs, self.nlhs + self.nlm)
            Js[idx, idx] = 1.  # assign Ilm in place of D in Schur
        if self.nbcs:
            Js[self.bcsr, self.bcsr] += -self.c  # bcsr size!
        if self.nbcseq:
            Js[self.bcseq1] *= -self.c
            Js[self.bcseq1, self.bcseq1] += 1.
            Js[self.bcseq0, self.bcseq1] -= 1.
        return Js

    def step_solve(self, db):
        if self.K is None:  # use KrylovJacobian
            def res(dy):
                c = -self.c
                t0 = self.t0
                y0 = self.y0
                f0 = self.f0
                r = self.residual(t0, y0 + dy, verbose=False)
                return dy - c * (r - f0)
            KJ = KrylovJacobian()  # KJ uses lgmres by default
            KJ.setup(np.zeros_like(db), np.zeros_like(db), res)
            dx = KJ.solve(db)
            self.info = 0
            return dx
        J = self.J
        M = self.M
        # opts = self.getopts()  # TODO: proper options handling
        dx, info = self.method.method(J, db, M=M)  # , **opts)
        self.info = info
        return dx

    @property
    def jacobian(self):
        return self


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
