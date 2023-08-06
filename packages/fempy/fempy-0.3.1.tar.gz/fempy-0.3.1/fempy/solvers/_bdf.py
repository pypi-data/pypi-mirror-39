# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 19:09:58 2016

@author: mwojc
"""
from __future__ import print_function
import numpy as np
import scipy.sparse
from scipy.integrate import BDF
# from scipy.integrate._ivp import bdf as bdf_module
# bdf_module.NEWTON_MAXITER = 10


class FempyBDF(BDF):
    # Here we hack scipy BDF solver to use fempy linear solvers
    # instead of default lu decompositions. We are able now to use
    # iterative solvers within BDF and also we can implement
    # solution method when no jacobian is available
    def __init__(self, fun, t0, y0, t_bound, max_step=np.inf, rtol=1e-3,
                 atol=1e-6, jac=None, jac_sparsity=None, vectorized=False,
                 **extraneous):
        # initialize scipy BDF with dummy jacobian ...
        n = len(y0)
        dummy_jac = scipy.sparse.csc_matrix((n, n))
        super(FempyBDF, self).__init__(fun, t0, y0, t_bound, max_step=max_step,
                                       rtol=rtol, atol=atol, jac=dummy_jac,
                                       jac_sparsity=jac_sparsity,
                                       vectorized=vectorized, **extraneous)

        # ... and then hack lu and lu_solve functions to use fempy jacobian
        self.fempy_jac = jac
        self.njev += 1
        self.fempy_jac.update()  # in case it was not done before

        def jac_wrapped(t, y):
            self.njev += 1
            self.fempy_jac.update(t, y)
            return 1.
        self.jac = jac_wrapped
        self.I = 0.
        self.J = 1.

        def lu(c):  # This will take c as argument if I=0 and J=1
            self.nlu += 1
            self.fempy_jac.update_c(c)
            return self.fempy_jac
        self.lu = lu

        def solve_lu(fempy_jac, db):
            return fempy_jac.step_solve(db)
        self.solve_lu = solve_lu

    def _step_impl(self):
        toreturn = super(FempyBDF, self)._step_impl()
#        nlhs = self.fempy_jac.nlhs
#        bcsr = self.fempy_jac.bcsr
#        ybcsr = self.fempy_jac.x_bcsr
#        self.y[:nlhs][bcsr] = ybcsr
        if self.fempy_jac._verbose:
            print('{:10f}: TIME STEP ACCEPTED'.format(self.t))
        return toreturn
