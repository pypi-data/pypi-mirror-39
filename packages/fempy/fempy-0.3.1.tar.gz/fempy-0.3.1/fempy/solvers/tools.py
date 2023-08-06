# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 09:20:09 2017

@author: mwojc
"""
from __future__ import print_function
from fempy.compat import reload
import inspect
import numpy as np
from fempy.solvers import linear
from fempy.solvers import nonlin
from fempy.solvers import precon
from fempy.solvers import methods


def _get_solvers():
    reload(methods)
    reload(precon)
    reload(linear)
    reload(nonlin)
    mc = [ls for ls in methods.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, methods.linear)]

    pc = [ls for ls in precon.__dict__.values()
          if inspect.isclass(ls) and issubclass(ls, precon.preconditioner)]

    lsc = [ls for ls in linear.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, linear.LinearSolver)]

    nsc = [ls for ls in nonlin.__dict__.values()
           if inspect.isclass(ls) and issubclass(ls, nonlin.NonLinearSolver)]
    return mc, pc, lsc, nsc


def _solver_test(solver, model, n=1, x0=None, **opts):
    import time
    T = 0.
    err = 0
    lhs_init = model.lhs.copy()
    if hasattr(model, 'lhslm'):
        lhslm_init = model.lhslm.copy()
    for i in range(n):
        m = model
        m.lhs[:] = lhs_init
        if hasattr(model, 'jaclm'):
            m.lhslm[:] = lhslm_init
        ls = solver(m)  # new solver is created

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
            print("Testing %s model against %s with %s method and"
                  " %s preconditioner" % (mname, nname, lname, pname))
            import sys
            sys.stdout.flush()

        t0 = time.time()
        ls.solve(**opts)
        T += time.time() - t0

        # Test solution
        x = ls.x
        # x0 = m.x0 if hasattr(m, 'x0') else x0
        if x0 is not None:
            if not np.allclose(x, x0.ravel()):
                print("    Solver did not reach the reference solution...")
                print("    Average x error: %s" % np.mean(abs(x - x0.ravel())))
                err = 1
    m.lhs[:] = lhs_init
    if hasattr(model, 'lhslm'):
        m.lhslm[:] = lhslm_init
    T = T/float(n)
    print("    Time spent in solver: %s\n" % T)
    return T, err


def model_test(model, solver=None, method=None, preconditioner=None,
               n=1, x0=None, strict=False, **options):
    mc, pc, lsc, nsc = _get_solvers()
    # Choose solvers
    if solver is None or len(solver) == 0:
        solver = [model.default_solver]
    if solver == 'all':
        solver = lsc + nsc
    if solver == 'linear':
        solver = lsc
    if solver == 'nonlin':
        solver = nsc
    # Choose methods
    if method is None or len(method) == 0:
        method = [model.solver.default_method]
    if method == 'all':
        method = mc
    if method == 'direct':
        method = [m for m in mc if m.direct]
    if method == 'iterative':
        method = [m for m in mc if not m.direct]
    # Choose preconditioners
    if preconditioner is None or len(preconditioner) == 0:
        preconditioner = [model.solver.default_preconditioner]
    if preconditioner == 'all':
        preconditioner = pc + [None]
    if preconditioner == 'exact':
        preconditioner = [p for p in pc if p.exact]
    if preconditioner == 'inexact':
        preconditioner = [p for p in pc if not p.exact]

    name = model.__class__.__name__
    if hasattr(model, 'info'):
        print(model.info)
    Tl = 100000000.
    bs = ''
    bm = ''
    bp = ''
    for sol in solver:
        sname = sol.__name__
        if hasattr(model, 'blacklist') and sname in model.blacklist:
            continue
        for mth in method:
            mname = mth.__name__
            sol.default_method = mth
            for p in preconditioner:
                pname = p.__name__ if p is not None else 'none'
                # skip direct methods when preconditioner is inexact
                if sol.default_method.direct:
                    if p is None or not p.exact:
                        continue
                if hasattr(model, 'pblacklist') and \
                        mname in model.pblacklist and \
                        (len(model.pblacklist[mname]) == 0 or
                         pname in model.pblacklist[mname]):
                    continue
                sol.default_preconditioner = p
                # print(name, sname, mname, pname)
                tl, err = _solver_test(sol, model, n=n, x0=x0, **options)
                if tl < Tl and not err:
                    Tl = tl
                    bs = sname
                    bm = mname
                    bp = pname
                if err and strict:
                    raise Exception('Solutions do not match')
    print('Best time for model %s: %s s' % (name, Tl))
    print('Best solver: %s with %s method and %s preconditioner'
          % (bs, bm, bp))


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
