# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:54:09 2016

@author: mwojc
"""
from __future__ import print_function
import pytest
import inspect
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg
import fempy.solvers.methods as methods
import fempy.solvers.precon as precon

# List of linear solver methods
methods = [ls for ls in methods.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, methods.linear)]


class Test_Linear_Methods:
    def test_linear_methods(self, capsys):
        n = 20
        tol = 1e-10
        Ad = np.random.rand(n, n)
#        Ad = Ad.dot(Ad.T)       # positively definite
#        Ad /= Ad.max()
#        Ad = (Ad + Ad.T)/2.     # symmetric
        As = sparse.csr_matrix(Ad)
        b = np.random.rand(n)
        x0 = np.linalg.solve(Ad, b)
        with capsys.disabled():
            print("\n")
            for ls in methods:
                print("Testing {} method".format(ls.__name__))
                ls = ls()
                if not ls.direct:  # iterative
                    x, _ = ls.solve(Ad, b, M=precon.ilu()(Ad), tol=tol)
                    assert np.allclose(x, x0)
                    x, _ = ls.solve(As, b, M=precon.lu()(Ad), tol=tol)
                    assert np.allclose(x, x0)
                    x, _ = ls.solve(As, b, tol=tol)
                    assert np.allclose(x, x0)
#                    x, _ = ls.solve(As, b, M=precon.AmgSas()(As), tol=tol)
#                    assert np.allclose(x, self.x)
                else:  # direct
                    with pytest.raises(ValueError):
                        x, _ = ls.solve(Ad, b)
                    x, _ = ls.solve(Ad, b, M=precon.lu()(Ad))
                    assert np.allclose(x, x0)
                    x, _ = ls.solve(As, b, M=precon.lu()(As))
                    assert np.allclose(x, x0)

if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
