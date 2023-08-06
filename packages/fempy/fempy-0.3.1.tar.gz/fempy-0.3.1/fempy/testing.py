# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 21:32:10 2014

@author: mwojc
"""
import os
import sys
import pytest

filedir = os.path.dirname(__file__)
if os.path.isdir(os.path.join(filedir, 'tests')):
    testdir = os.path.realpath(filedir + '/tests') + '/'
    testdata = os.path.realpath(filedir + '/tests/data') + '/'
else:
    testdir = os.path.realpath(filedir + '/../tests') + '/'
    testdata = os.path.realpath(filedir + '/../tests/data') + '/'
sys.path.append(testdir)
# imports from testdir
import common
from common import *


def gettestfile(module):
    module = module.replace(filedir, '')
    p, s = os.path.split(module)
    s = s.replace('.pyc', '.py')
    testfile = p + '/test_' + s
    testfile = testdir + testfile
    open(testfile)  # for rising possible IOError
    return testfile


def testmodule(module, opts=''):
    try:
        testfile = gettestfile(module)
        d, f = os.path.split(testfile)
        curdir = os.getcwd()
        os.chdir(d)
        opts = opts if isinstance(opts, list) else opts.split()
        pytest.main([str(f)] + opts)
        os.chdir(curdir)
    except IOError:
        pass  # Skip testing silently if no testing file


if __name__ == '__main__':
    pytest.main([testdir, '-vrs'])  # Run all tests from testdir
