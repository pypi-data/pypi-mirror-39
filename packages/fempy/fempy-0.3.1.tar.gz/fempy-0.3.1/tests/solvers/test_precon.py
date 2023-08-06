# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:54:09 2016

@author: mwojc
"""

import pytest
import numpy as np
import scipy.sparse as sparse
import fempy.solvers.precon as precon

pn = [p for p in dir(precon) if 'Preconditioner' in p]
pc = [getattr(precon, p) for p in pn]
# po = [p() for p in pc]


class Test_Preconditioners:
    def get_dense_sparse_matrix(self, n, symmetric=False):
        Ad = np.random.rand(n, n)
        if symmetric:
            Ad = (Ad + Ad.T)/2.
        As = sparse.csr_matrix(Ad)
        return Ad, As

    def get_rhs(self, n):
        return np.random.rand(n)

    def setup(self):
        n = 10
        Ad, As = self.get_dense_sparse_matrix(n)
        b = self.get_rhs(n)
        x = np.linalg.solve(Ad, b)
        self.Ad = Ad
        self.As = As
        self.b = b
        self.x = x

    def test_superlu_preconditioner(self):
        p = precon.lu()
        x = p(self.Ad)*self.b
        assert np.allclose(x, self.x)
        x = p(self.As)*self.b
        assert np.allclose(x, self.x)

    # @pytest.mark.skipif('UmfpackPreconditioner' not in pn)
    def test_umfpack_preconditioner(self):
        pytest.importorskip('scikits.umfpack')
        p = precon.umfpack()
        x = p(self.Ad)*self.b
        assert np.allclose(x, self.x)
        x = p(self.As)*self.b
        assert np.allclose(x, self.x)

    # @pytest.mark.skipif('AmgPrecondtioner' not in pn, reason='no pyamg')
    def test_amg_preconditioner(self):
        pytest.importorskip('pyamg')
        p = precon.amg_sas()
        x1 = p(self.Ad)*self.b
        x2 = p(self.As)*self.b
        assert np.allclose(x1, x2)

    # @pytest.mark.skipif('AmgPrecondtioner' not in pn, reason='no pyamg')
    def test_amgcl_preconditioner(self):
        pytest.importorskip('pyamgcl')
        p = precon.amgcl_cg()
        x1 = p(self.Ad)*self.b
        x2 = p(self.As)*self.b
        assert np.allclose(x1, x2)

    def test_superilu_preconditioner(self):
        p = precon.ilu()
        x1 = p(self.Ad)*self.b
        x2 = p(self.As)*self.b
        assert np.allclose(x1, x2)

    def test_diag_preconditioner(self):
        p = precon.diag()
        x1 = p(self.Ad)*self.b
        x2 = p(self.As)*self.b
        assert np.allclose(x1, x2)


if __name__ == '__main__':
    # import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
