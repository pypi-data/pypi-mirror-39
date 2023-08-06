# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""

import inspect
import fempy.solvers.nonlin as nonlin
from fempy.domain.tools import cached_property


class Model(object):
    default_solver = nonlin.NewtonKrylovSolver

    def __init__(self, *args, **kwargs):
        """
        Model initialization sequence:
        1. Look for domain in args (first argument) or kwargs
        2. If domain is not found: try to call domain_setup which should
           set self.domain atribute, It is called *without* arguments
        2. If domain is found just set self.domain
        3. Call init - init is called *without* arguments!
        4. Look for solver in kwargs
        5. If solver not found set self.solver = self.default_solver
        6. If solver is found set it as self.solver
        7. Finally call self.setup method with unmodified *args and **kwargs
        """
        # Try to discover domain
        domain = kwargs.pop('domain', None)
        if len(args) and hasattr(args[0], 'nnode'):
            domain = args[0]
            args = args[1:]
            kwargs.pop('domain', None)  # remove domain from kwargs
        if domain is None:
            self.setup_domain()
        else:
            self.domain = domain
        if hasattr(self, 'init'):
            self.init(**kwargs)
        # now set solver...
        if 'solver' in kwargs:
            solver = kwargs['solver']
            del kwargs['solver']
        else:
            solver = self.default_solver
        self.solver = solver
        # and make setups
        if hasattr(self, 'setup'):
            self.setup(*args, **kwargs)
        self.setup_model(*args, **kwargs)

    def setup_domain(self, *args, **kwargs):
        raise TypeError("Provide a domain or define 'setup_domain' method")

    def setup_model(self, *args, **kwargs):
        pass

    def update(self):
        # get all names in model class and object
        c = self.__class__
        d = self.__dict__
        cdir = dir(c)
        dkeys = d.keys()
        for n in cdir:
            # find properties and invalidate them if they have been 'cached'
            if isinstance(getattr(c, n), cached_property) and n in dkeys:
                # property has been cached so we invalidate it
                del d[n]
            # now find all update functions and call them (without arguments)
            if (n.endswith('_update') or
                    (n.endswith('_') and not n.endswith('__'))):
                attr = getattr(self, n)
                if callable(attr):
                    attr()

    def invalidate_caches(self, cdir=None, dkeys=None):
        # get all names in model class and object
        c = self.__class__
        d = self.__dict__
        cdir = dir(c)
        dkeys = d.keys()
        for n in cdir:
            if isinstance(getattr(c, n), cached_property) and n in dkeys:
                del d[n]

    def solve(self, **opts):
        self.solver.solve(**opts)
        return self.lhs

    def preview(self, what='lhs', time=()):
        from fempy.geometry import gmsh_io
        gmsh_io.preview_model(self, what, time)

    def preview_dump(self, fname, what='lhs', time=(), ascii=False):
        from fempy.geometry import gmsh_io
        gmsh_io.dump_model(fname, self, what, time, ascii)

    @property
    def solver(self):
        return self._solver

    @solver.setter
    def solver(self, s):
        if inspect.isclass(s):
            self._solver = s(self)
        else:
            self._solver = s
            # TODO: check if 's' is proper solver for the model


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
