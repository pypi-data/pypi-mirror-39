# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:51:44 2016

@author: mwojc
"""


class Solver(object):
    default_options = None

    def __init__(self, **options):
        self.options = options

    def getopts(self, options=None):
        if self.default_options is not None:
            opts = self.default_options.copy()
        else:
            opts = {}
        if hasattr(self, 'options'):
            opts.update(self.options)
        if options is not None:
            opts.update(options)
        return opts

    def solve(self, *args, **options):
        raise NotImplementedError


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
