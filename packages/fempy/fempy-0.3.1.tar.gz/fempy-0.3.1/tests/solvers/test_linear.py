# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:54:09 2016

@author: mwojc


MISSING FUNCTIONALITIES AND TESTS

* only 'lop' should be sufficient to define model
* jacobian is a dense matrix?
* bcs in model changed?
* initialize solvers without model, handle model change properly
* possible lop types should be: method(x), property, LinearOperator,
  only property returning result is supported now
* possible jac types should be: method(x), property, LinearOperator, matrix,
  currently jac can be a sparse matrix or property returning it
* possible jaclm types should be as for jac
* it should be possible to define loplm instead of jaclm (be aware that
  loplm must implement B.T*x AND B*lm)
* test for custom 'ilop'
* test for custom 'ijac'


To be verified: maybe the 'method' in linear solvers should be used
inside M (in matvec defining M) on the reduced system instead of the
global use in 'solve' for the whole problem. That should work better
because the reduced problem is first smaller, secondly usually symmetric.
The problem is possibly the longer run whem lm are present...

"""
from __future__ import print_function
from fempy.compat import reload
import pytest
import inspect
import numpy as np
import scipy.sparse as sparse
import fempy.solvers.methods as methods
import fempy.solvers.linear as linear
import fempy.solvers.precon as precon
# import fempy.solvers.nonlin as nonlin


def get_solvers():
    reload(methods)
    reload(precon)
    reload(linear)
    mc = [ls for ls in methods.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, methods.linear)]

    pc = [ls for ls in precon.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, precon.preconditioner)]

    lsc = [ls for ls in linear.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, linear.LinearSolver)]
    return mc, pc, lsc

#    nsc = [ls for ls in nonlin.__dict__.values()
#           if inspect.isclass(ls) and issubclass(ls, nonlin.NonLinearSolver)]

# Preconditioners causing problems
pblacklist = {  # linear.CgsSolver: (None, precon.diag),
                # linear.CgSolver: (None, precon.diag),
                # linear.BicgstabSolver: (None, precon.diag),
                # linear.AmgBicgstabSolver: (None, precon.diag),
                # linear.AmgMinimalResidualSolver: (None, precon.diag),
                # linear.AmgGmresSolver: (None, precon.diag),
                # linear.AmgFgmresSolver: (None, precon.diag),
                # linear.GmresSolver: (precon.diag,),
              }

# Solvers causing problems
blacklist = [  # linear.MinresSolver,
               # linear.AmgSteepestDescentSolver,
               # linear.AmgCgSolver,
             ]


# Dummy model
class M:
    info = "MODEL 1 - no bcs, no lm"

    def __init__(self, kind=''):
        n = 10
        rhs = np.random.rand(n)
        jac = sparse.csr_matrix(np.random.rand(n, n))
        if 'pos' in kind:
            jac = jac.dot(jac.T)       # positively definite
            jac /= jac.max()
        if 'sym' in kind:
            jac = (jac + jac.T)/2.          # symmetric

        jac0 = jac.copy()
        rhs0 = rhs.copy()
        ijac0 = np.linalg.inv(jac.toarray())
        lhs0 = ijac0.dot(rhs0)

        self.jac = jac
        self.rhs = rhs

        # solution
        self.jac0 = jac0
        self.ijac0 = ijac0
        self.lhs0 = lhs0
        self.rhs0 = rhs0


# Dummy model with bcs
class Mbcs:
    info = "MODEL 2 - with bcs, no lm"

    def __init__(self, kind=''):
        n = 10
        rhs = np.random.rand(n)
        jac = sparse.csr_matrix(np.random.rand(n, n))
        if 'pos' in kind:
            jac = jac.dot(jac.T)       # positively definite
            jac /= jac.max()
        if 'sym' in kind:
            jac = (jac + jac.T)/2.          # symmetric

        lhs = np.zeros_like(rhs)
        bcs = np.zeros_like(rhs, dtype=bool)
        bcs[[0, -1]] = True
        lhs[bcs] = [0, 1.]

        # Solve
        jac0 = jac.copy()
        jac0[bcs] = 0.
        jac0[bcs, bcs] = 1.
        rhs0 = rhs.copy()
        rhs0[bcs] = lhs[bcs]

        ijac0 = np.linalg.inv(jac0.toarray())
        lhs0 = ijac0.dot(rhs0)

        self.rhs = rhs
        self.jac = jac
        self.lhs = lhs
        self.bcs = bcs

        # solution
        self.jac0 = jac0
        self.ijac0 = ijac0
        self.lhs0 = lhs0
        self.rhs0 = rhs0


# Dummy model with equality bcs
class Mbcseq:
    info = "MODEL 2a - with bcseq, no lm"

    def __init__(self, kind=''):
        n = 10
        rhs = np.random.rand(n)
        jac = sparse.csr_matrix(np.random.rand(n, n))
        if 'pos' in kind:
            jac = jac.dot(jac.T)       # positively definite
            jac /= jac.max()
        if 'sym' in kind:
            jac = (jac + jac.T)/2.          # symmetric

        lhs = np.zeros_like(rhs)
        bcseq = [[0, -1, [1., -2., 0.2]]]

        # preprocess and solve
        jac0 = jac.copy()
        lhs0 = lhs.copy()
        rhs0 = rhs.copy()
        i0 = bcseq[0][0]
        i1 = bcseq[0][1]
        c0, c1, c2 = bcseq[0][2]
        # modify jacobian
        jac0[i0] += jac0[i1]
        jac0[i1] = 0.
        jac0[i1, i0] = c0/c1
        jac0[i1, i1] = 1.
        # modify rhs
        rhs0[i0] += rhs0[i1]
        rhs0[i1] = c2/c1
        # solve
        ijac0 = np.linalg.inv(jac0.toarray())
        lhs0 = ijac0.dot(rhs0)
        assert np.allclose(c0*lhs0[i0] + c1*lhs0[i1], c2)

        self.rhs = rhs
        self.jac = jac
        self.lhs = lhs
        self.bcseq = bcseq

        # solution
        self.jac0 = jac0
        self.ijac0 = ijac0
        self.lhs0 = lhs0
        self.rhs0 = rhs0


# Dummy model with lm
class Mlm:
    info = "MODEL 3 - with bcs, with lm"

    def __init__(self, kind=''):
        n = 10
        nlm = 3
        rhs = np.random.rand(n)
        jac = sparse.csr_matrix(np.random.rand(n, n))
        if 'pos' in kind:
            jac = jac.dot(jac.T)       # positively definite
            jac /= jac.max()
        if 'sym' in kind:
            jac = (jac + jac.T)/2.          # symmetric

        lhs = np.zeros_like(rhs)
        bcs = np.zeros_like(rhs, dtype=bool)
        bcs[[0, -1]] = True
        lhs[bcs] = [0, 1.]

        jaclm = np.random.rand(nlm, n)
        rhslm = np.random.rand(nlm)

        jac0 = jac.copy()
        jac0[bcs] = 0.
        jac0[bcs, bcs] = 1.
        jaclm0 = jaclm.copy()
        jaclm0T = jaclm0.T
        jaclm0T[bcs] = 0.

        jac0 = sparse.bmat([[jac0, jaclm0T], [jaclm0, None]]).tocsc()

        rhs0 = rhs.copy()
        rhs0[bcs] = lhs[bcs]
        rhs0 = np.append(rhs0, rhslm)

        ijac0 = np.linalg.inv(jac0.toarray())
        lhs0 = ijac0.dot(rhs0)

        self.rhs = rhs
        self.jac = jac
        self.lhs = lhs
        self.bcs = bcs
        self.jaclm = jaclm
        self.rhslm = rhslm

        # solution
        self.jac0 = jac0
        self.ijac0 = ijac0
        self.lhs0 = lhs0
        self.rhs0 = rhs0


class Mempty:
    info = "MODEL 4 - empty"


class Mrhs:
    info = "MODEL 5 - rhs only"

    n = 10
    rhs = np.random.rand(n)


class Mlop(Mlm):
    info = "MODEL 6 - lop only"

    def __init__(self, kind=''):
        Mlm.__init__(self)
        self.jac_for_lop = self.jac
        del self.jac

    @property
    def lop(self):
        return self.jac_for_lop * self.lhs


class Mclass:
    info = "MODEL 7 - class definition"

    n = 10
    rhs = np.random.rand(n)
    lhs = np.zeros(n)
    jac = sparse.csr_matrix(np.random.rand(n, n))
    # lop = property(lambda x: jac1*lhs)


class Mfield:
    info = "MODEL 8 - model with fempy fields"

    def __init__(self, Field, ndime):
        import fempy.testing
        from common import Simple3D
        domain = eval('Simple3D().domain{}D'.format(ndime))
        # domain = Simple2D().domain2D
        rhs = Field(domain, 1.)
        n = rhs.size
        jac = sparse.csr_matrix(np.random.rand(n, n))
        # jac = np.random.rand(n, n)  # TODO: make dense to work

        self.rhs = rhs
        self.jac = jac


class Solver_Test:
    """
    This class will test all linear and nonlinear solvers, except the
    blacklisted, against linear models - non symmetric, non positive definite
    """
    def solver_test(self, solver, model, kind='', n=1, **opts):
        import time, inspect
        T = 0.
        for i in range(n):
            m = model
            if not inspect.isclass(m):  # isinstance(model, (types.TypeType, types.ClassType)):
                m = model.__class__  # Always initialize model
            try:
                m = m(kind)
            except:
                m = m()
            ls = solver(m)

            if ls.method.direct and m.jac is None:
                T = 10000000000.
                break

            if i == 0:
                # Print message
                mname = m.__class__.__name__
                nname = ls.__class__.__name__
                lname = ls.method.__class__.__name__
                pname = ls.preconditioner.__class__.__name__ \
                    if ls.preconditioner is not None else 'none'
                print("    Testing %s model against %s with %s method and"
                      " %s preconditioner" % (mname, nname, lname, pname))
                import sys
                sys.stdout.flush()

            t0 = time.time()
            ls.solve(**opts)
            T += time.time() - t0

            # Test solution
            if hasattr(m, 'lhs0'):
                x = ls.x
                # print(x, m.lhs0)
                # Test if solution is as expected
                assert np.allclose(x, m.lhs0)
            if hasattr(m, 'rhs0'):  # does not work with current ode solvers
                ls._update_P()
                ls._update_Mlm()
                x = ls.x
                b = ls.b
                J = ls.J
                M = ls.M
                # Test if jacobian is OK (jacobian is assumed to be exact)
                assert np.allclose(J.dot(x), m.rhs0)
                # Test if preconditioner is OK (only for exact precs)
                p = ls.preconditioner
                if p is not None and p.exact:
                    assert np.allclose(M.dot(b), m.lhs0)
        return T, 0

    def iterate_solvers(self, models, solvers, methods, preconditioners, N=1,
                        **options):
        methods0 = methods
        preconditioners0 = preconditioners
        for model in models:
            name = model.__name__
            if hasattr(model, 'info'):
                print(model.info)
            Tl = 100000000.
            bs = ''
            bm = ''
            bp = ''
            for solver in solvers:
                sname = solver.__name__
                if solver in blacklist:
                    continue
                if hasattr(model, 'blacklist') and sname in model.blacklist:
                    continue
                if len(methods0) == 0:
                    methods = [solver.default_method]
                for method in methods:
                    mname = method.__name__
                    solver.default_method = method
                    if len(preconditioners0) == 0:
                        preconditioners = [solver.default_preconditioner]
                    for p in preconditioners:
                        pname = p.__name__ if p is not None else 'none'
                        # skip direct methods when preconditioner is inexact
                        # print(name, sname, mname, pname)
                        if solver.default_method.direct:
                            if p is None or not p.exact:
                                continue
                        # skip blacklisted preconditioners
                        if solver in pblacklist and p in pblacklist[solver]:
                            continue
                        if hasattr(model, 'pblacklist') and \
                                mname in model.pblacklist and \
                                (len(model.pblacklist[mname]) == 0 or
                                 pname in model.pblacklist[mname]):
                            continue
                        solver.default_preconditioner = p
                        # print(name, sname, mname, pname)
                        tl, err = self.solver_test(solver, model,
                                                   kind='', n=N,
                                                   **options
                                                   )
                        if tl < Tl and not err:
                            Tl = tl
                            bs = sname
                            bm = mname
                            bp = pname
            print('Best time for model %s: %s s' % (name, Tl))
            print('Best solver: %s with %s method and %s preconditioner'
                  % (bs, bm, bp))


class Test_Linear_Solvers(Solver_Test):
    def test_mbcs(self):
        m = Mbcs()
        s = linear.BicgstabSolver(m)
        s.preconditioner = precon.lu
        s.solve()
        assert np.allclose(s.x, m.lhs0)

    def test_mlm(self):
        m = Mlm()
        s = linear.IterativeSolver(m, preconditioner=None)
        s.solve()
        assert np.allclose(s.x, m.lhs0)

    def test_linear_solvers(self, capsys):
        N = 1  # NUMBER OF SOLVER PASSAGES FOR EVERY MODEL
        models = [M, Mbcs, Mbcseq, Mlm]
        with capsys.disabled():
            print("\n")

            # First test Linear Solver against all available methods
            # and precons
            mc, pc, lsc = get_solvers()
            solvers = [linear.LinearSolver]
            methods = mc
            preconditioners = pc + [None]
            self.iterate_solvers(models, solvers, methods, preconditioners, N,
                                 tol=1e-8)

            # And then test the rest with default mthods and preconditioners
            mc, pc, lsc = get_solvers()
            solvers = lsc
            methods = []
            preconditioners = []
            self.iterate_solvers(models, solvers, methods, preconditioners, N,
                                 tol=1e-8)

    def test_direct_J_M(self):
        for model in [M, Mbcs, Mbcseq, Mlm]:
            m = linear.DirectSolver(model)
            m.update()
            b = np.random.rand(m.nlhs+m.nlm)
            assert np.allclose(m.J*(m.M*b), b)
            assert np.allclose(m.Jsparse*(m.M*b), b)

    def test_direct_J_Jsparse(self):
        for model in [M, Mbcs, Mbcseq, Mlm]:
            m = linear.DirectSolver(model)
            m.update()
            x = np.random.rand(m.nlhs+m.nlm)
            assert np.allclose(m.J*x, m.Jsparse*x)

    def test__bcseq_unroll(self):
        models = [Mbcs()]  # , Mbcseq, Mlm]
        for m in models:
            m.bcseq = [[0, 1], [-2, -1], [2, 3], [1, 0], [4, 4], [0, -1],
                       [2, 1], [1, 4]]
            bcseq0, bcseq1, bcseqc = linear._unroll_bcseq(m)
            assert np.allclose(bcseq0, [0, -1, 2, 1])
            assert np.allclose(bcseq1, [1, -2, 3, 4])
            assert np.allclose(bcseqc.T[0], [0., -1., 0])
            assert np.allclose(bcseqc.T[1], [0., 1., 1.])
            assert np.allclose(bcseqc.T[2], [1., -1., 0.])
            assert np.allclose(bcseqc.T[3], [1., -1., 0.])


class Test_Basic(Solver_Test):
    def test_empty_model(self):
        with pytest.raises(AttributeError):
            linear.LinearSolver(Mempty)

    def test_rhs_only_model(self):
        with pytest.raises(AttributeError):
            linear.LinearSolver(Mrhs).solve()

    def test_lop_only_model(self):
        linear.IterativeSolver(Mlop()).solve()

    def test_class_model(self):
        linear.LinearSolver(Mclass).solve()


class Test_Field_Solve(Solver_Test):
    def test_field_solve(self):
        from fempy.fields import nfields
        self.field_solve(nfields.nScalar, ndime=1)
        self.field_solve(nfields.nScalar, ndime=2)
        self.field_solve(nfields.nScalar, ndime=3)

        self.field_solve(nfields.nVector, ndime=1)
        self.field_solve(nfields.nVector, ndime=2)
        self.field_solve(nfields.nVector, ndime=3)

        self.field_solve(nfields.nTensor, ndime=1)
        self.field_solve(nfields.nTensor, ndime=2)
        self.field_solve(nfields.nTensor, ndime=3)

#        self.field_solve(nfields.nTensor3, ndime=1)
#        self.field_solve(nfields.nTensor3, ndime=2)
#        self.field_solve(nfields.nTensor3, ndime=3)
#
#        self.field_solve(nfields.nTensor4, ndime=1)
#        self.field_solve(nfields.nTensor4, ndime=2)
#        self.field_solve(nfields.nTensor4, ndime=3)

    def field_solve(self, Field, ndime):
        Solver = linear.DirectSolver

        # no bcs
        m = Mfield(Field, ndime)
        ls = Solver(m)
        ls.solve()
        # assert type(xn) is Field

        r = ls.residual()
        A = m.jac
        x = m.lhs.ravel()
        b = m.rhs.ravel()
        assert np.allclose(r, A.dot(x) - b)

        # with bcs
        m = Mfield(Field, ndime)
        m.bcs = np.zeros_like(m.rhs, dtype=bool)
        m.bcs[[0, -1]] = True
        ls = Solver(m)
        ls.solve()
        # assert type(xn) is Field

        r = m.res.ravel()
        A = m.jac
        x = m.lhs.ravel()
        b = m.rhs.ravel()
        # b at fixed nodes should remain???
        assert np.allclose(r, A.dot(x) - b)

#        # with bcs - all True
#        m = Mfield(Field, ndime, nnode)
#        m.bcs = np.zeros_like(m.rhs, dtype=bool)
#        m.bcs[:] = True
#        ls = Solver(m)
#        xn = ls.solve()
#        assert type(xn) is Field
#
#        r = ls.residual()
#        A = m.jac
#        x = m.lhs.ravel()
#        b = m.rhs.ravel()
#        # b at fixed nodes should remain???
#        assert np.allclose(r, A.dot(x) - b)

        # with lm
        m = Mfield(Field, ndime)
        m.bcs = np.zeros_like(m.rhs, dtype=bool)
        m.bcs[[0, -1]] = True
        m.jaclm = np.random.rand(3, m.bcs.size)
        ls = Solver(m)
        ls.solve()
        # assert type(xn) is Field

        r = np.concatenate([ri.ravel() for ri in m.res])
        A = m.jac
        x = m.lhs.ravel()
        b = m.rhs.ravel()
        B = m.jaclm
        lm = m.lhslm
        c = m.rhslm
        rx = A.dot(x) + B.T.dot(lm) - b
        rlm = B.dot(x) - c
        rall = np.concatenate((rx, rlm))
        assert np.allclose(r, rall)


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
