# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:17:33 2016

@author: mwojc
"""
from fempy.compat import pickle
from fempy.models.heat import Heat
from fempy.solvers.tools import model_test
from fempy.testing import testdata
import numpy as np


class Test_Heat(object):
    def test_heat_2D_p2(self):
        d = pickle.load(open(testdata + '/heat/2D_p2.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1., 0], [0, 1.]]

        m.alpha['left + bottom'] = 8.
        m.epsilon['left + bottom'] = 0.85
        m.Text['left + bottom'] = 293.15

        m.alpha['right + top'] = 25.
        m.epsilon['right + top'] = 0.85
        m.Text['right + top'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/2D_p2.sol'), strict=True)

    def test_heat_2D_s1(self):
        d = pickle.load(open(testdata + '/heat/2D_s1.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1., 0], [0, 1.]]

        m.alpha['left'] = 8.
        m.epsilon['left'] = 0.85
        m.Text['left'] = 293.15

        m.alpha['right'] = 25.
        m.epsilon['right'] = 0.85
        m.Text['right'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/2D_s1.sol'), strict=True)

    def test_heat_3D_p2(self):
        d = pickle.load(open(testdata + '/heat/3D_p2.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

        m.alpha['left+bottom'] = 8.
        m.epsilon['left+bottom'] = 0.85
        m.Text['left+bottom'] = 293.15

        m.alpha['right+top'] = 25.
        m.epsilon['right+top'] = 0.85
        m.Text['right+top'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/3D_p2.sol'), strict=True)

    def test_heat_3D_s1(self):
        d = pickle.load(open(testdata + '/heat/3D_s1.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

        m.alpha['left'] = 8.
        m.epsilon['left'] = 0.85
        m.Text['left'] = 293.15

        m.alpha['right'] = 25.
        m.epsilon['right'] = 0.85
        m.Text['right'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/3D_s1.sol'), strict=True)

    def test_heat_3D(self):
        d = pickle.load(open(testdata + '/heat/3D.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1., 0, 0], [0, 1., 0], [0, 0, 1.]]

        m.alpha['left+bottom+front'] = 8.
        m.epsilon['left+bottom+front'] = 0.85
        m.Text['left+bottom+front'] = 293.15

        m.alpha['right+top+back'] = 25.
        m.epsilon['right+top+back'] = 0.85
        m.Text['right+top+back'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/3D.sol'), strict=True)

    def test_heat_1D(self):
        d = pickle.load(open(testdata + '/heat/1D.dom', 'rb'))
        m = Heat(d)

        m.kij[:] = [[1.]]

        m.alpha['left'] = 8.
        m.epsilon['left'] = 0.85
        m.Text['left'] = 293.15

        m.alpha['right'] = 25.
        m.epsilon['right'] = 0.85
        m.Text['right'] = 1273.15

        model_test(m, x0=np.loadtxt(testdata + '/heat/1D.sol'), strict=True)


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
