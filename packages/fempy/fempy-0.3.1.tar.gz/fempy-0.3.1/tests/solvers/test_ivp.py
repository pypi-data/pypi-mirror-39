# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:54:09 2016

@author: mwojc
"""
from __future__ import print_function
from fempy.compat import reload
import pytest
import inspect
import fempy.solvers.methods as methods
import fempy.solvers.precon as precon
import fempy.solvers.ivp as ivp
from solvers import test_linear


def get_solvers():
    reload(methods)
    reload(precon)
    reload(ivp)
    mc = [ls for ls in methods.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, methods.linear)]

    pc = [ls for ls in precon.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, precon.preconditioner)]

    isc = [ls for ls in ivp.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, ivp.ODESolver)]
    return mc, pc, isc


class M(test_linear.M):
    pblacklist = {'gmres': 'diag'}

    def __init__(self, kind=''):
        test_linear.M.__init__(self, kind)
        del self.rhs0
        self.rhs_tot = self.rhs.copy()
        self.rhs[:] = 0.
        self.time0 = 0.
        self.time1 = 10000000000000.

    def update(self):
        self.rhs[:] = self.time*self.rhs_tot/10000000000000.


class Mbcs(test_linear.Mbcs):
    pblacklist = {'gmres': 'diag'}

    def __init__(self, kind=''):
        test_linear.Mbcs.__init__(self, kind)
        del self.rhs0
        self.rhs_tot = self.rhs.copy()
        self.lhs_bcs_tot = self.lhs[self.bcs].copy()
        self.rhs[:] = 0.
        self.time0 = 0.
        self.time1 = 10000000000000.

    def update(self):
        self.rhs[:] = self.time*self.rhs_tot/10000000000000.
        self.lhs[self.bcs] = self.time*self.lhs_bcs_tot/10000000000000.


class Mbcseq(test_linear.Mbcseq):
    pblacklist = {'gmres': 'diag'}

    def __init__(self, kind=''):
        test_linear.Mbcseq.__init__(self, kind)
        del self.rhs0
        self.rhs_tot = self.rhs.copy()
        self.delta_bcseq_tot = self.bcseq[0][2][-1]
        self.rhs[:] = 0.
        self.time0 = 0.
        self.time1 = 10000000000000.

    def update(self):
        self.rhs[:] = self.time*self.rhs_tot/10000000000000.
        self.bcseq[0][2][-1] = self.time*self.delta_bcseq_tot/10000000000000.


class Mlm(test_linear.Mlm):
    pblacklist = {'gmres': 'diag'}

    def __init__(self, kind=''):
        test_linear.Mlm.__init__(self, kind)
        del self.rhs0
        self.rhs_tot = self.rhs.copy()
        self.lhs_bcs_tot = self.lhs[self.bcs].copy()
        self.rhslm_tot = self.rhslm.copy()
        self.rhs[:] = 0.
        self.time0 = 0.
        self.time1 = 10000000000000.

    def update(self):
        self.rhs[:] = self.time*self.rhs_tot/10000000000000.
        self.lhs[self.bcs] = self.time*self.lhs_bcs_tot/10000000000000.
        self.rhslm[:] = self.time*self.rhslm_tot/10000000000000.


class Test_Ivp_Solvers(test_linear.Solver_Test):
    def test_ivp_solvers(self, capsys):
        N = 1  # NUMBER OF SOLVER PASSAGES FOR EVERY MODEL
        models = [M, Mbcs, Mlm, Mbcseq]  # , [Mscipy]

        with capsys.disabled():
            print("\n")

            # First test solvers capable to use fempy linear methods
            # against all available methods and precons
            mc, pc, _ = get_solvers()
            solvers = [ivp.BDFSolver]
            methods = mc
            preconditioners = pc + [None]
            self.iterate_solvers(models, solvers, methods, preconditioners, N,)
                                 # verbose=True)

            # And then test the rest with default methods and preconditioners
            _, _, solvers = get_solvers()
            methods = []
            preconditioners = []
            self.iterate_solvers(models, solvers, methods, preconditioners, N)
                                 # verbose=True)

    def test_compare_BDF_bcseq(self):
        import numpy as np
        m = Mbcseq()
        s1 = ivp.BDFSolverDS(m)
        s1.update()
        s2 = ivp.BDFSolver(m)
        s2._verbose = False
        s2.update()
        s2.update_c(0.1)

        Js1 = s1.Jsparse
        I = np.eye(10)
        Js1 = I - 0.1 * s1.Jsparse
        Js2 = s2.Jsparse.toarray()

        assert np.allclose(Js1, Js2)

        x = np.random.rand(10)
        assert np.allclose(s2.J*x, s2.Jsparse*x)

    def test_compare_BDF_bcs(self):
        import numpy as np
        m = Mbcs()
        s1 = ivp.BDFSolverDS(m)
        s1.update()
        s2 = ivp.BDFSolver(m)
        s2._verbose = False
        s2.update()
        s2.update_c(0.1)

        Js1 = s1.Jsparse
        I = np.eye(10)
        Js1 = I - 0.1 * s1.Jsparse
        Js2 = s2.Jsparse.toarray()

        assert np.allclose(Js1, Js2)

        x = np.random.rand(10)
        assert np.allclose(s2.J*x, s2.Jsparse*x)

    def test_compare_BDF_lm(self):
        import numpy as np
        m = Mlm()
        s1 = ivp.BDFSolverDS(m)
        s1.update()
        s2 = ivp.BDFSolver(m)
        s2._verbose = False
        s2.update()
        s2.update_c(0.1)
        
        Js1 = s1.Jsparse
        I = np.eye(13)
        Js1 = I - 0.1 * s1.Jsparse
        Js2 = s2.Jsparse.toarray()
        
        # print(Js1 - Js2)
        assert np.allclose(Js1, Js2)
        
        x = np.random.rand(13)
        # print(s2.J*x)
        # print(s2.Jsparse*x)
        assert np.allclose(s2.J*x, s2.Jsparse*x)

    def test_compare_BDF(self):
        import numpy as np
        m = M()
        s1 = ivp.BDFSolverDS(m)
        s1.update()
        s2 = ivp.BDFSolver(m)
        s2._verbose=False
        s2.update()
        s2.update_c(0.1)
        
        Js1 = s1.Jsparse
        I = np.eye(10)
        Js1 = I - 0.1 * s1.Jsparse
        Js2 = s2.Jsparse.toarray()
        
        # print(Js1 - Js2)
        assert np.allclose(Js1, Js2)
        
        x = np.random.rand(10)
        # print(s2.J*x)
        # print(s2.Jsparse*x)
        assert np.allclose(s2.J*x, s2.Jsparse*x)

    def test_M_J_bcseq(self):
        import numpy as np
        m = ivp.BDFSolver(Mbcseq)
        m._verbose = True
        m.update()
        m.update_c(0.1)
        b = np.random.rand(10)
        # print(m.J*(m.M*b) - b)
        # print(m.Jsparse*(m.M*b))
        # print(b)
        # print(m.M*b)
        Js = m.Jsparse
        from scipy.sparse import linalg
        splu = linalg.splu(Js)
        # print(splu.solve(b))
        # print(m.M*b - splu.solve(b))
        # print Js[0]
        assert np.allclose(m.J*(m.M*b), b)
        assert np.allclose(m.Jsparse*(m.M*b), b)

    def test_M_J_bcs(self):
        import numpy as np
        m = ivp.BDFSolver(Mbcs)
        m._verbose = True
        m.update()
        m.update_c(0.1)
        b = np.random.rand(10)
        # print(m.J*(m.M*b) - b)
        # print(m.Jsparse*(m.M*b))
        # print(b)
        # print(m.M*b)
        #
        # Js = m.Jsparse
        # from scipy.sparse import linalg
        # splu = linalg.splu(Js)
        # print(splu.solve(b))
        # print(Js.toarray() - (m.I - m.c*m.K))
        assert np.allclose(m.J*(m.M*b), b)
        assert np.allclose(m.Jsparse*(m.M*b), b)

    def test_M_J_lm(self):
        import numpy as np
        m = ivp.BDFSolver(Mlm)
        m._verbose = True
        m.update()
        m.update_c(0.1)
        b = np.random.rand(13)
        # print(m.J*(m.M*b) - b)
        assert np.allclose(m.J*(m.M*b), b)
        assert np.allclose(m.Jsparse*(m.M*b), b)

    def test_M_J(self):
        import numpy as np
        m = ivp.BDFSolver(M)
        m._verbose = True
        m.update()
        m.update_c(0.1)
        b = np.random.rand(10)
        assert np.allclose(m.J*(m.M*b), b)
        assert np.allclose(m.Jsparse*(m.M*b), b)


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
