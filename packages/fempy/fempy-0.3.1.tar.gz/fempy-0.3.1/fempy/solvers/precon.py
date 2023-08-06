# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:51:44 2016

@author: mwojc
"""
import scipy.sparse as sparse
import scipy.sparse.linalg
from fempy.solvers._solver import Solver

LOP = sparse.linalg.LinearOperator


class preconditioner(Solver):
    exact = False
    method = staticmethod(sparse.linalg.spilu)  # use this by default

    def inverse(self, A, **options):
        options = self.getopts(options)
        iA = self.method(A, **options)
        if hasattr(iA, 'solve'):
            iA = LOP(A.shape, dtype=A.dtype, matvec=iA.solve)
        else:
            iA = sparse.linalg.aslinearoperator(iA)
        return iA
    __call__ = inverse

    def solve(self, A, b, **options):
        x = self.inverse(A, **options).dot(b)
        self.info = 0
        return x


# INEXACT PRECONDITIONERS
class inexact(preconditioner):
    pass


class ilu(inexact):
    pass


class diag(inexact):
    def method(self, A, **options):
        iA = sparse.csr_matrix(A.shape, dtype=A.dtype)
        iA.setdiag(1./A.diagonal())
        return iA


# if pyamg is present
try:
    from pyamg import smoothed_aggregation_solver as sas

    class amg_sas(inexact):
        def method(self, A, **options):
            return sas(A, **options).aspreconditioner()
except ImportError:
    pass


# EXACT PRECONDITIONERS
class exact(preconditioner):
    exact = True
    method = staticmethod(sparse.linalg.splu)


class lu(exact):
    pass


# if umfpack is present
try:
    from scikits import umfpack as umf

    class umfpack(exact):
        exact = True

        def method(self, A, **options):
            if hasattr(A, 'has_sorted_indices'):
                umf.assumeSortedIndices = A.has_sorted_indices
            return umf.splu(A, **options)
except ImportError:
    pass


# if pyamgcl is present
try:
    import pyamgcl

    class amgcl_cg(exact):  # We create pyamg solver actually here
        def method(self, A, **options):
            options = self.getopts(options)
            options['type'] = 'cg'
            options['maxiter'] = 1000
            if not sparse.issparse(A):
                A = sparse.csr_matrix(A)
            S = pyamgcl.solver(pyamgcl.amg(A), prm=options)

            def matvec(b):
                x = S(b.ravel())
                return x.reshape(b.shape)  # necesacry for matmat
            #return LOP(A.shape, dtype=A.dtype, matvec=matvec)
            return pyamgcl.amg(A)
except ImportError:
    pass


# lu_default_opts = {'perm_spec': None,
#                    'diag_pivot_tresh': None,
#                    'drop_tol': None,
#                    'relax': None,
#                    'panel_size': None,
#                    'options': {}}
# ilu_default_opts = {'drop_tol': None,
#                    'fill_factor': None,
#                    'drop_rule': None,
#                    'perm_spec': None,
#                    'diag_pivot_tresh': None,
#                    'drop_tol': None,
#                    'relax': None,
#                    'panel_size': None,
#                    'options': {}}


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
