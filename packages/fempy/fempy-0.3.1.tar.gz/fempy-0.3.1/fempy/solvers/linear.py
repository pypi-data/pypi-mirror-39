# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 10:44:36 2017

@author: mwojc
"""
from fempy.compat import builtins
import inspect
import numpy as np
import scipy.sparse
import scipy.optimize
from fempy.solvers import precon
from fempy.solvers import methods
from fempy.solvers._solver import Solver

LOP = scipy.sparse.linalg.LinearOperator


def hasprop(obj, name):
    obj = obj.__class__ if not inspect.isclass(obj) else obj
    if builtins.hasattr(obj, name):
        if isinstance(getattr(obj, name), property):
            return True
    return False


def hasattr(obj, name):
#    # first test for class properties...
#    if __builtin__.hasattr(obj.__class__, name):
#        if isinstance(getattr(obj.__class__, name), property):
#            return True
#    # and then test object...
#    return __builtin__.hasattr(obj, name)
    return hasprop(obj, name) or builtins.hasattr(obj, name)


def _append(*args):
    return np.concatenate([a for a in args if a is not None])


def _initialize(obj, msg='obj'):
    if inspect.isclass(obj):
        try:
            obj = obj()
        except Exception:
            raise TypeError("Please, initialize {}...".format(msg))
    return obj


def _set_solution(m, x):
    if hasattr(m, 'lhslm'):
        nlm = m.lhslm.size
        xlm = x[-nlm:]
        if hasprop(m, 'lhslm'):
            m.lhslm = xlm
        else:
            m.lhslm[:] = xlm
        x = x[:-nlm]
    if hasprop(m, 'lhs'):
        m.lhs = x
    else:
        m.lhs[:] = x.reshape(m.lhs.shape)


def _get_jac_times_lhs(model):
    # jac is always 2D?
    lhs = model.lhs
    r = lhs.copy()  # return same type as lhs
    r[:] = model.jac.dot(lhs.ravel()).reshape(lhs.shape)
    return r


def _get_loplm(model):
    # jaclm is always 2D?
    lhs = model.lhs
    lhslm = model.lhslm
    jaclm = model.jaclm
    rx = lhs.copy()  # return same type as lhs
    rx[:] = jaclm.T.dot(lhslm).reshape(lhs.shape)
    rlm = jaclm.dot(lhs.ravel())
    return rx, rlm


def _get_res(model):
    r = model.lop
    rhs = model.rhs
    if not hasattr(model, 'jaclm'):
        return r - rhs
    rx, rlm = model.loplm
    rhslm = model.rhslm
    return r + rx - rhs, rlm - rhslm


def _get_lop(model):
    r = model.lop
    if not hasattr(model, 'jaclm'):
        return r
    rx, rlm = model.loplm
    return r + rx, rlm


def _solvelm(P, B, BT, Mlm, bx, blm):
    blm = (B.dot(P.dot(bx)).T - blm).T
    lm = Mlm.dot(blm)  # get lagrange multipliers
    x = P.dot(bx - BT.dot(lm))
    return x, lm


def _unroll_bcseq(m):
    bcseq = m.bcseq
    bcseqm = []
    bcseqs = []
    bcseqc = []
    for eq in bcseq:
        n = len(eq)
        coeffs = (1., -1., 0.) if n < 3 else eq[2]
        mr = eq[0]  # master
        sv = eq[1]  # slave
        mr = (mr,) if not isinstance(mr, tuple) else mr
        sv = (sv,) if not isinstance(sv, tuple) else sv
        # mr = list(mr) if not isinstance(mr, (int, str)) else [mr]
        # sv = list(sv) if not isinstance(sv, (int, str)) else [sv]
        if hasattr(m, 'domain'):
            sort = None if n < 4 else eq[3]
            # get properly sorted indices
            if isinstance(mr[0], str):
                mr = (m.domain.ngroups.nums(mr[0], sortby=sort),) + mr[1:]
            if isinstance(sv[0], str):
                sv = (m.domain.ngroups.nums(sv[0], sortby=sort),) + sv[1:]
            # get global numbers of dofs
            mr = m.lhs.nipos[mr].ravel()
            sv = m.lhs.nipos[sv].ravel()
            mr = np.asarray([mr]) if isinstance(mr, int) else mr
            sv = np.asarray([sv]) if isinstance(sv, int) else sv
        N = len(mr)
        assert N == len(sv)
        bcseqm += [mr]
        bcseqs += [sv]
#        bcseqc += [np.tile(coeffs, (len(mr), 1))]
        c0, c1, c2 = coeffs
        c0 = np.zeros(N)+c0 if isinstance(c0, (float, int)) else \
            np.asarray(c0).ravel()
        c1 = np.zeros(N)+c1 if isinstance(c1, (float, int)) else \
            np.asarray(c1).ravel()
        c2 = np.zeros(N)+c2 if isinstance(c2, (float, int)) else \
            np.asarray(c2).ravel()
        bcseqc += [np.asarray([c0, c1, c2]).T]
    npc = np.concatenate
    bcseq0, bcseq1, bcseqc = npc(bcseqm), npc(bcseqs), npc(bcseqc).T
#    return npc(bcseqm), npc(bcseqs), npc(bcseqc).T
#    # Perform some tests for duplicated constraints
#    # find duplicates in bcseq - only first occurence is left, master nodes
#    # are considered first, prescribed msters are protected
#    from fempy.domain.tools import unique_rows
#    nb = len(bcseq0)
#    uidx = unique_rows(npc((bcseq0, bcseq1))[:, None], strict=False)
#    uidx = uidx[:nb]*uidx[nb:] #+ ibm  # protect prescribed nodes
#    bcseq0 = bcseq0[uidx]
#    bcseq1 = bcseq1[uidx]
#    bcseqc = bcseqc[:, uidx]
    # find conflicting bcs and bcseq constraints
    if hasattr(m, 'bcs'):
        bcsr = m.bcs.ravel()
        lhsr = m.lhs.ravel()
        # 'slave' unknown is prescribed - reverse order
        b0 = bcsr[bcseq0]
        b1 = bcsr[bcseq1]
        ibs = ~b0 * b1
        bcseq0[ibs], bcseq1[ibs] = bcseq1[ibs], bcseq0[ibs]
        bcseqc[0, ibs], bcseqc[1, ibs] = bcseqc[1, ibs], bcseqc[0, ibs]
        # 'master' unknown is prescribed, TODO: remove from bcseq ???
        b0 = bcsr[bcseq0]
        b1 = bcsr[bcseq1]
        ibm = b0 * ~b1
        bcseqc[2, ibm] = bcseqc[2, ibm] - bcseqc[0, ibm] * lhsr[bcseq0[ibm]]
        bcseqc[0, ibm] = 0.
        # both unknowns are prescribed
        ib = b0 * b1
        bcseq0 = bcseq0[~ib]
        bcseq1 = bcseq1[~ib]
        bcseqc = bcseqc[..., ~ib]
        ibm = ibm[~ib]
    # find duplicates in bcseq - only first occurence is taken if dup
    from fempy.domain.tools import unique_rows
    beq = np.concatenate(([bcseq0], [bcseq1])).T
    idx = unique_rows(beq, sort=True, strict=False)
    idx *= ~(bcseq0 == bcseq1)  # exclude also "self-periodicity"
    bcseq0, bcseq1 = beq[idx].T
    bcseqc = bcseqc[..., idx]
    # Masters cannot be duplicated (unless they are prescribed)
    ibm = ibm[idx]
    midx = unique_rows(bcseq0[:, None], strict=False) + ibm
    bcseq0 = bcseq0[midx]
    bcseq1 = bcseq1[midx]
    bcseqc = bcseqc[:, midx]
    # Slaves cannot be duplicated
    ibm = ibm[midx]
    sidx = unique_rows(bcseq1[:, None], strict=False)
    bcseq0 = bcseq0[sidx]
    bcseq1 = bcseq1[sidx]
    bcseqc = bcseqc[:, sidx]
#    # Slaves cannot be masters (unless corresponding masters are prescribed)
    ibm = ibm[sidx]
    sidx = ~np.isin(bcseq1, bcseq0) + ibm
    bcseq0 = bcseq0[sidx]
    bcseq1 = bcseq1[sidx]
    bcseqc = bcseqc[:, sidx]
    return bcseq0, bcseq1, bcseqc


def _multiply(A, b):
    if not scipy.sparse.issparse(A):
        return A * b
    else:
        return A.multiply(b)


# We derive from Solver only for proper options handling
# Defaut jacobian uses direct linear solver (superlu from scipy)
class LinearSolver(Solver):
    default_preconditioner = precon.exact
    default_method = methods.direct

    def __init__(self, model, **options):
        # Assign and update model
        self.model = _initialize(model, 'model')
#        if hasattr(self.model, 'update'):
#            self.model.update()
        # Query model for all necessary data
        m = self.model
        if m is None:
            return
        # test for lop or jac
        if not hasattr(m, 'lop') and not hasattr(m, 'jac'):
            raise AttributeError("Neither 'jac' nor 'lop' found in model")
        # now we query for lhs
        if not hasattr(m, 'lhs'):
            if hasattr(m, 'rhs'):
                m.lhs = np.zeros_like(m.rhs)
            else:
                if hasattr(m, 'lop'):
                    m.lhs = np.zeros_like(m.lop)
                else:
                    jac = m.jac
                    m.lhs = np.zeros((jac.shape[0],), jac.dtype)
        self.nlhs = m.lhs.size
        # now jac and lop
        if not hasattr(m, 'lop'):   # only jac is given
            m.__class__.lop = property(_get_jac_times_lhs)
        if not hasattr(m, 'jac'):  # only lop is given
            m.jac = None  # solvers have to decide what to do without jac
        # create jac testing utility
        if not hasattr(m, 'jac_times_lhs'):
            m.__class__.jac_times_lhs = property(_get_jac_times_lhs)
        #  we test for rhs also
        if not hasattr(m, 'rhs'):
            m.rhs = np.zeros_like(m.lhs)
        # bcs is optional, we create it here, but we
        # should not rely on its existence in solvers
        if not hasattr(m, 'bcs'):
            m.bcs = np.zeros_like(m.lhs, dtype=bool)
        # now lagrange multipliers part, created only if jaclm exists in model
        if hasattr(m, 'jaclm'):
            if not hasattr(m, 'rhslm'):
                m.rhslm = np.zeros(len(m.jaclm))
            if not hasattr(m, 'lhslm'):
                m.lhslm = np.zeros(len(m.jaclm))
            if not hasattr(m, 'loplm'):
                m.__class__.loplm = property(_get_loplm)
            self.nlm = len(m.lhslm)
        else:
            self.nlm = 0
        # create also residuals, this will be a tuple if Lagrange
        # multipliers are defined
        if not hasattr(m, 'res'):
            m.__class__.res = property(_get_res)
        # and also set time attributes
        if not hasattr(m, 'time'):
            m.time = 0.
        if not hasattr(m, 'time0'):
            m.time0 = 0.
        if not hasattr(m, 'time1'):
            m.time1 = 1.
        # now set preconditioner...
        if 'preconditioner' in options:
            preconditioner = options['preconditioner']
            del options['preconditioner']
        else:
            preconditioner = 'default'
        self.preconditioner = preconditioner
        # ... and linear solver
        if 'method' in options:
            method = options['method']
            del options['method']
        else:
            method = 'default'
        self.method = method
#        # ... and options
#        # ... recognize and set linear solver options
#        for key, value in options.items():
#            if key.startswith('inner_'):
#                self.method.options[key[6:]] = value
        self.options = options
        # update finally
        # self.update()

    @property
    def preconditioner(self):
        return self._preconditioner

    @preconditioner.setter
    def preconditioner(self, p):
        if p == 'default':
            p = _initialize(self.default_preconditioner)
        self._preconditioner = _initialize(p, 'preconditioner')

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, l):
        if l == 'default':
            l = _initialize(self.default_method)
        self._method = _initialize(l, 'linear solver')

    @property
    def x(self):
        m = self.model
        # query for lhs ...
        lhs = m.lhs
        self.nlhs = lhs.size
        self.shape_lhs = lhs.shape
        self.dtype = lhs.dtype
        lhs = lhs.copy().ravel()
        # for lhslm ...
        if not hasattr(m, 'lhslm'):
            self.nlm = 0
            x = lhs
        else:
            lhslm = m.lhslm
            self.nlm = len(lhslm)
            x = _append(lhs, lhslm)
        # for bcs ...
        if hasattr(m, 'bcs'):
            bcs = m.bcs.ravel()
            self.nbcs = bcs.sum()
            self.bcsr = bcs.copy()
            self.x_bcsr = lhs[bcs].copy()
        else:
            self.nbcs = 0
            self.bcsr = np.zeros_like(lhs, bool)  # always have bcsr
        # and bcseq
        if hasattr(m, 'bcseq'):
            self.bcseq0, self.bcseq1, self.bcseqc = _unroll_bcseq(m)
            self.x_bcseq0 = lhs[self.bcseq0].copy()
            self.x_bcseq1 = lhs[self.bcseq1].copy()
            self.nbcseq = len(self.bcseq0)
        else:
            self.nbcseq = 0
        self.n = len(x)
        self.shape = (self.n, )*2
        return x

    @x.setter
    def x(self, x):
        if x is None:
            return
        _set_solution(self.model, x)

    @property
    def b(self):
        # x must be called first!
        m = self.model
        rhs = m.rhs.copy().ravel()
        if self.nbcseq:
            c0, c1, c2 = self.bcseqc
            rhs[self.bcseq0] += rhs[self.bcseq1]
            rhs[self.bcseq1] = c2/c1
        if self.nbcs:
            rhs[self.bcsr] = self.x_bcsr
        b = rhs if not self.nlm else _append(rhs, m.rhslm)
        return b

    @property
    def l(self):
        # x must be called first! !!!
        m = self.model
        lx = m.lop.ravel()
        llm = None
        if self.nlm:
            llmx, llm = m.loplm
            lx += llmx.ravel()
        if self.nbcseq:
            c0, c1, c2 = self.bcseqc
            lx[self.bcseq0] += lx[self.bcseq1]
            lx[self.bcseq1] = (c0/c1)*self.x_bcseq0 + self.x_bcseq1  # proper x
        if self.nbcs:
            lx[self.bcsr] = self.x_bcsr
        return _append(lx, llm)

    @property
    def r(self):
        return self.l - self.b

    def _update_K(self):
        self.K = self.model.jac

    def _update_B(self):
        if self.nlm:
            self.B = self.model.jaclm
            # make sure B is zero at bcsr
            # this is done here because it is necessary in _update_Mlm and
            # _matvecJ
            if self.nbcs:
                self.B[:, self.bcsr] = 0.
            self.BT = self.B.T
        else:
            self.B = None
            self.BT = None

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
            if nbcseq:
                K = K.copy()  # this is safe but this is a copy...
                # TODO: K should not be copied here at all
                c0, c1, c2 = self.bcseqc
                bcseq0 = self.bcseq0
                bcseq1 = self.bcseq1
                c01 = c0/c1
                K[bcseq0] += K[bcseq1]
                K[:, bcseq0] -= _multiply(K[:, bcseq1], c01)  # elementwise
                bcsr[bcseq1] = True
            K0 = K[~bcsr]
            K0 = K0[:, ~bcsr]
            Kbcs = K[:, bcsr]
            P0 = pre(K0)  # LOP or sp matrix

            def matvec(b):
                bbcs = (Kbcs.dot(b[bcsr]))[~bcsr]  # b carries x at bcsr
                b0 = b[~bcsr] - bbcs
                x0 = P0.dot(b0)
                x = b.copy()                     # copies also x at bcsr
                x[~bcsr] = x0
                if nbcseq:
                    x[bcseq1] -= c01 * x[bcseq0]
                return x
            P = LOP(K.shape, dtype=K.dtype, matvec=matvec)  # LOP
        self.P = P

    def _update_Klm(self):
        P = self.P
        if P is None:
            self.Klm = None
            return
        B = self.B
        BT = self.BT
        if B is None:
            self.Klm = None
            return
        self.Klm = B.dot(P.dot(BT))      # Use preconditioner to inverse?

    def _update_Mlm(self):
        Klm = self.Klm
        if Klm is None:
            self.Mlm = None
            return
        if scipy.sparse.issparse(Klm):   # Efficiency for many lms??
            Mlm = scipy.sparse.linalg.inv(Klm)
        else:
            Mlm = np.linalg.inv(Klm)
        self.Mlm = Mlm

    def _matvecJ(self, x):
        K = self.K
        if K is None:
            # then we do not update nothing in solver, just in model
            self.x = x
            self.update_model()  # or simply update :)?
            self.x  # l uses x_bcsr so we need to update...
            return self.l  # self.r + self.b
            # return self.residual(x)
        if not self.nlm:
            lx = K.dot(x)
            llm = None
        else:
            xx, xlm = x[:self.nlhs], x[self.nlhs:]
            B = self.B
            BT = self.BT
            lx = K.dot(xx) + BT.dot(xlm)
            llm = B.dot(xx)
        # TODO: the below is OK for symmetric K only
        # Consider jacobian manipulation here
        if self.nbcseq:
            c0, c1, c2 = self.bcseqc
            lx[self.bcseq0] += lx[self.bcseq1]  # add rows
            x_bcseq1 = x[:self.nlhs][self.bcseq1]
            x_bcseq0 = x[:self.nlhs][self.bcseq0]
            lx[self.bcseq1] = (c0/c1)*x_bcseq0 + x_bcseq1  # proper x
        if self.nbcs:
            x_bcsr = x[:self.nlhs][self.bcsr]
            lx[self.bcsr] = x_bcsr
        return _append(lx, llm)

    def _matvecM(self, b):
        P = self.P
        if not self.nlm:
            x = P.dot(b)
            lm = None
        else:
            bx, blm = b[:self.nlhs], b[self.nlhs:]
            B = self.B
            BT = self.BT
            Mlm = self.Mlm
            x, lm = _solvelm(P, B, BT, Mlm, bx, blm)
#        if self.nbcs:  # This is done in P and Mlm already...
#            x[self.bcsr] = b[self.bcsr]
        return _append(x, lm)

    @property
    def J(self):
        return LOP(self.shape, matvec=self._matvecJ)

    @property
    def M(self):
        if self.P is None:
            return None
        return LOP(self.shape, matvec=self._matvecM)

    @property
    def Jsparse(self):
        if self.K is None:
            return
        J = self.K.copy()  # Should we copy?
        if self.nbcseq:
            c0, c1, c2 = self.bcseqc
            bcseq0 = self.bcseq0
            bcseq1 = self.bcseq1
            # sum up rows at master nodes
            J[bcseq0] += J[bcseq1]
            # add equality constraint at slave nodes
            J[bcseq1] = 0.
            J[bcseq1, bcseq0] = c0/c1
            J[bcseq1, bcseq1] = 1.
        if self.nbcs:
            bcsr = self.bcsr
            J[bcsr] = 0
            J[bcsr, bcsr] = 1.
        if self.nlm:  # bcsr zeroed already in B
            B = self.B
            BT = self.BT
            J = scipy.sparse.bmat([[J, BT], [B, None]])
        return J

    def lop(self, x=None):
        self.update_model(x)  # TODO: is this is wrong becase of x_bcsr?
        return self.l

    def residual(self, x=None):
        self.update_model(x)  # or update rather?
        self.x
        return self.r

    def lsolve(self, **options):
        self.update_model()
        if not hasattr(self, 'K'):  # not initialized yet?
            self.update()
        x0 = self.x
        b = self.b
        J = self.J
        M = self.M
        options = self.getopts(options)
        self.x, info = self.method.method(J, b, x0, M=M, **options)
    solve = lsolve

    def update(self, x=None, f=None):  # f is here for scipy compatibility
        # assign x to model and call its update if it exists
        # self.update_model(x)
        # clear current data grab new data from model
        self.clear()
        self.x0 = self.x  # here we set also all shaping data
        self._update_K()
        self._update_B()
        self._update_P()
        self._update_Klm()
        self._update_Mlm()

    def clear(self):
        attrs = ['nlhs', 'shape_lhs', 'dtype', 'nlm', 'nbcs', 'bcsr', 'x_bcsr',
                 'n', 'shape', 'x0', 'bcseq0', 'bcseq1', 'bcseqc', 'nbcseq',
                 'x_bcseq0', 'x_bcseq1',
                 'K', 'P', 'B', 'BT', 'Klm', 'Mlm',
                 'c', 'K0', 'B0', 'BT0', 'I', 'Ilm', 't0', 'y0', 'f0']
        for a in attrs:
            if hasattr(self, a):
                delattr(self, a)

    def update_model(self, x=None):
        self.x = x    # Should we move x.setter here?
        if hasattr(self.model, 'update'):
            self.model.update()


class DirectSolver(LinearSolver):
    pass


class LUSolver(LinearSolver):
    default_preconditioner = precon.lu


try:
    class UmfpackSolver(DirectSolver):
        default_preconditioner = precon.umfpack
except AttributeError:
    pass


class IterativeSolver(LinearSolver):
    default_preconditioner = precon.inexact
    default_method = methods.iterative


class LgmresSolver(LinearSolver):
    default_preconditioner = precon.inexact
    default_method = methods.lgmres


class GmresSolver(LinearSolver):
    default_preconditioner = precon.inexact
    default_method = methods.gmres


class CgsSolver(LinearSolver):
    default_preconditioner = precon.inexact
    default_method = methods.cgs


class BicgstabSolver(LinearSolver):
    default_preconditioner = precon.inexact
    default_method = methods.bicgstab


try:
    class AmgclCGSolver(IterativeSolver):
        default_preconditioner = precon.amgcl_cg
        # default_method = methods.direct

except AttributeError:
    pass

# if pyamg is present
try:
    #    class AmgBicgstabSolver(LinearSolver):
    #        default_preconditioner = precon.inexact
    #        default_method = methods.amg_bicgstab

    #    class AmgFgmresSolver(LinearSolver):
    #        default_preconditioner = precon.inexact
    #        default_method = methods.amg_fgmres
    #
    #    class AmgGmresSolver(LinearSolver):
    #        default_preconditioner = precon.inexact
    #        default_method = methods.amg_gmres
    pass
except:
    pass


# add utility functions for solving linear systems
def model_from_data(A, b, r=None, x0=None, B=None, c=None):
    class M(object):
        jac = A
        rhs = b
        if r is not None:
            bcs = r
        if x0 is not None:
            lhs = x0.copy()
        if B is not None:
            jaclm = B
        if c is not None:
            lhslm = c
    return M()


def dsolve(A, b, bcs=None, x0=None, B=None, c=None, **options):
    m = model_from_data(A, b, bcs, x0, B, c)
    s = DirectSolver(m, **options)
    s.solve()
    if B is not None:
        return m.lhs, m.lhslm
    return m.lhs


def isolve(A, b, bcs=None, x0=None, B=None, c=None, **options):
    m = model_from_data(A, b, bcs, x0, B, c)
    s = IterativeSolver(m, **options)
    s.solve()
    if B is not None:
        return m.lhs, m.lhslm
    return m.lhs


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
