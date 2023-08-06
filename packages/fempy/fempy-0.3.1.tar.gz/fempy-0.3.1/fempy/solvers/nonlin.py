# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 19:09:58 2016

@author: mwojc
"""
from __future__ import print_function
import numpy as np
from scipy.optimize import newton_krylov
from scipy.interpolate import interp1d
from fempy.solvers import linear
from fempy.solvers import ivp


class NonLinearSolver(linear.IterativeSolver):
    def callback(self, x, f=None):
        if hasattr(self.model, 'callback'):
            self.model.callback(x, f)
        self.update(x)

    def nsolve(self, **options):
        self.lsolve(maxiter=1)
        # self.update()

        options = self.getopts(options)
        F = self.residual
        x0 = self.x
        method = self.method
        M = self.M

        x = newton_krylov(F, x0, method=method.method, inner_M=M,
                          callback=self.callback, **options)
        self.x = x

    def solve(self, steps=None, **options):
        m = self.model
        if steps is None or steps == 1:
            m.time = m.time1
            return self.nsolve(**options)
        elif isinstance(steps, int):
            steps = np.linspace(m.time0, m.time1, steps)
        else:
            assert steps[0] >= m.time0
            assert steps[-1] <= m.time1
            assert np.all(np.diff(steps) >= 0)
        x = []
        for step in steps:
            print("Step: {}".format(step))
            m.time = step
            self.nsolve(**options)
            x.append(self.x)
        # Interpolate solution for dense output
        # TODO: should we always solve for intermediate time step
        x = np.array(x).T
        sol = interp1d(steps, x, kind='linear', fill_value='extrapolate')
        sol.t = sol.x
        sol.sol = sol
        m._sol = sol
        m.__class__.sol = ivp._set_solution_at_time
        m.sol()  # This sets sotution at last time step


class NewtonKrylovSolver(NonLinearSolver):
    pass


class SimpleIterationSolver(NonLinearSolver):
    def nsolve(self, xtol=1e-5, maxiter=10, verbose=False, raise_error=False,
               **options):
        options = self.getopts(options)
        opts = {}
        for k, v in options.items():
            if 'inner_' in k:
                opts[k[6:]] = v
        self.lsolve(**opts)
        x0 = self.x
        for i in range(maxiter):
            self.update()
            self.lsolve(**opts)
            x = self.x.copy()
            dxnorm = np.linalg.norm(np.abs(x - x0))
            if verbose:
                print('{}:   xtol: {}'.format(i, dxnorm))
            if np.allclose(x, x0, rtol=xtol):
                return
            x0 = x.copy()
        if raise_error:
            raise ValueError("No convergence in %s iterations" % maxiter)
        else:
            import warnings
            warnings.warn(("No convergence in %s iterations" % maxiter))


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
