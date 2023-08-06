# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:51:44 2016

@author: mwojc
"""
import scipy.sparse as sparse
import scipy.sparse.linalg
from fempy.solvers._solver import Solver


class linear(Solver):
    direct = False
    method = staticmethod(sparse.linalg.lgmres)

    def solve(self, A, b, x0=None, M=None, **options):
        options = self.getopts(options)
        x, info = self.method(A, b, x0=x0, M=M, **options)
        self.info = info
        return x, info
    __call__ = solve


# ITERATIVE SOLVERS
class iterative(linear):
    pass


class lgmres(iterative):
    pass


class gmres(iterative):
    method = staticmethod(sparse.linalg.gmres)

# Seems to not work without preconditioner
#class cg(iterative):
#    method = staticmethod(sparse.linalg.cg)


class cgs(iterative):
    method = staticmethod(sparse.linalg.cgs)


class bicgstab(iterative):
    method = staticmethod(sparse.linalg.bicgstab)


# This is solver only for symmetric systems - need to be tested
# class Minres(IterativeSolver):
#     method = staticmethod(sparse.linalg.minres)


# if pyamg is present
try:
    from pyamg import krylov
# Seems to not work if the system is not positively defined
#    class AmgCg(IterativeSolver):
#        method = staticmethod(krylov.cg)

# Seems to not work at all
#    class AmgSteepestDescent(IterativeSolver):
#        method = staticmethod(krylov.steepest_descent)

# This is solver only for symmetric systems - need to be tested
#    class AmgMinimalResidual(IterativeSolver):
#        method = staticmethod(krylov.minimal_residual)

# There are some exactness troubles in this solver it finishes before
# tol is reached
#    class amg_bicgstab(iterative):
#        method = staticmethod(krylov.bicgstab)

# Prints annoying warnings in testing
#    class amg_fgmres(iterative):
#        method = staticmethod(krylov.fgmres)

#    class amg_gmres(iterative):
#        method = staticmethod(krylov.gmres)
except ImportError:
    pass


## if pyamgcl is present
#try:
#    from pyamgcl import solver
#
#    class cg_amgcl(iterative):        
#        def method(self, A, b, x0=None, M=None, **options):
#            options = self.getopts(options)
#            options['type'] = 'cg'
#            S = solver(M, options)   # Would be inefficient to create solver
#            x = S(b)
#            return x, S.error
#except ImportError:
#    pass


# DIRECT SOLVER
class direct(linear):
    direct = True

    def method(self, A, b, x0=None, M=None, **options):
        if M is None:
            raise ValueError("No jacobian? Direct solver cannot handle this.")
        x = M*b
        return x, 0


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
#    import numpy as np
#    A = np.random.rand(5,5)
#    b = np.random.rand(5)
#    s = iterative()
#    print s.solve(A, b)
