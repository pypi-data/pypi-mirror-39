# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:54:09 2016

@author: mwojc
"""
from __future__ import print_function
from fempy.compat import reload
import pytest
import inspect
import numpy as np
import fempy.solvers.methods as methods
import fempy.solvers.precon as precon
import fempy.solvers.nonlin as nonlin
from fempy.testing import testdata
from solvers import test_linear


def get_solvers():
    reload(methods)
    reload(precon)
    reload(nonlin)
    mc = [ls for ls in methods.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, methods.linear)]

    pc = [ls for ls in precon.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, precon.preconditioner)]

#    lsc = [ls for ls in linear.__dict__.values()
#           if inspect.isclass(ls) and issubclass(ls, linear.LinearSolver)]

    nsc = [ls for ls in nonlin.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, nonlin.NonLinearSolver)]
    return mc, pc, nsc


# TEST NONLIN
# howto INITIALIZE MODEL, OPTIONS, PRECONDITIOENR, ETc.


class Mscipy(object):
    info = "MODEL 1 - integro-differential equation from scipy docs"
    blacklist = ['SimpleIterationSolver']
    pblacklist = {}

    def __init__(self):
        n = 25
        self.n = n
        self.rhs = np.zeros((n, n))
        self.lhs = np.zeros((n, n))
        self.lhs0 = np.loadtxt(testdata + '/mscipy.sol').ravel()

    @property
    def lop(self):
        # parameters
        nx, ny = self.n, self.n
        hx, hy = 1./(nx-1), 1./(ny-1)

        P_left, P_right = 0, 0
        P_top, P_bottom = 1, 0

        P = self.lhs
        d2x = np.zeros_like(P)
        d2y = np.zeros_like(P)

        d2x[1:-1] = (P[2:]   - 2*P[1:-1] + P[:-2]) / hx/hx
        d2x[0]    = (P[1]    - 2*P[0]    + P_left)/hx/hx
        d2x[-1]   = (P_right - 2*P[-1]   + P[-2])/hx/hx
    
        d2y[:,1:-1] = (P[:,2:] - 2*P[:,1:-1] + P[:,:-2])/hy/hy
        d2y[:,0]    = (P[:,1]  - 2*P[:,0]    + P_bottom)/hy/hy
        d2y[:,-1]   = (P_top   - 2*P[:,-1]   + P[:,-2])/hy/hy

        return d2x + d2y - 10*np.cosh(P).mean()**2


class Test_NonLinear_Solvers(test_linear.Solver_Test):
    def test_nonlinear_solvers(self, capsys):
        N = 1  # NUMBER OF SOLVER PASSAGES FOR EVERY MODEL
#        test_linear.Mlm.pblacklist={'bicgstab': ['amg_sas', 'diag', 'lu',
#                                                 'inexact', 'exact', 'ilu',
#                                                 'preconditioner', 'umfpack',
#                                                 'none']}
        models = [test_linear.M, test_linear.Mbcs, test_linear.Mbcseq,
                  test_linear.Mlm, Mscipy]
        with capsys.disabled():
            print("\n")

            # First test NonLinearSolver against all available methods
            # and precons
            mc, pc, nsc = get_solvers()
            solvers = [nonlin.NonLinearSolver]
            methods = mc
            preconditioners = pc + [None]
            self.iterate_solvers(models, solvers, methods, preconditioners, N,
                                 f_tol=1e-8)

            # And then test the rest with default methods and preconditioners
            mc, pc, nsc = get_solvers()
            solvers = nsc
            methods = []
            preconditioners = []
            self.iterate_solvers(models, solvers, methods, preconditioners, N,
                                 f_tol=1e-8)


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
