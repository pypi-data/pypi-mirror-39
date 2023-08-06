# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 10:49:39 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.fields import Field
from fempy.fields.algebra import transpose, tensordot, dot, TensorCalc
import pytest


class Test_Algebra:
    s = np.random.rand(1)[0]
    v = np.random.rand(3)
    t = np.random.rand(3, 3)
    t3 = np.random.rand(3, 3, 3)
    t4 = np.random.rand(3, 3, 3, 3)
    a = np.random.rand(3, 2)

    fs = Field(np.random.rand(20, 10), 2)
    fv = Field(np.random.rand(20, 10, 3), 2)
    ft = Field(np.random.rand(20, 10, 3, 3), 2)
    ft3 = Field(np.random.rand(20, 10, 3, 3, 3), 2)
    ft4 = Field(np.random.rand(20, 10, 3, 3, 3, 3), 2)
    fa = Field(np.random.rand(20, 2, 3), 1)

    def test_transpose(self):
        tr = transpose
        nptr = np.transpose
        assert np.allclose(tr(self.t4), nptr(self.t4))
        assert np.allclose(tr(self.t3, (0, 2, 1)), nptr(self.t3, (0, 2, 1)))
        assert np.allclose(tr(self.ft4)[0, 0], nptr(self.ft4[0, 0]))
        assert np.allclose(tr(self.fa)[5], nptr(self.fa[5]))

    def test_tensordot(self):
        f = tensordot
        npf = np.tensordot
        assert np.allclose(f(self.t4, self.t), npf(self.t4, self.t))
        assert np.allclose(f(self.ft4, self.ft)[0, 0],
                           npf(self.ft4[0, 0], self.ft[0, 0]))
        assert np.allclose(f(self.fa, self.a, [-1, 0])[0],
                           npf(self.fa[0], self.a, [-1, 0]))
        assert np.allclose(f(self.fa, self.a, [[-1, -2], [0, 1]])[0],
                           npf(self.fa[0], self.a, [[-1, -2], [0, 1]]))
        assert np.allclose(f(self.fa, transpose(self.fa), [-1, -2])[0],
                           np.dot(self.fa[0], transpose(self.fa[0])))

        assert type(f(self.ft4, self.ft)) == Field
        assert type(f(self.t4, self.t)) == np.ndarray

        with pytest.raises(IndexError):
            f(self.fs, self.fv)
        assert np.allclose(f(self.fs, self.fv, 0), f(self.fv, self.fs, 0))
        assert np.allclose(f(self.fv, self.v, 1), f(self.v, self.fv, 1))

    def test_dot(self):
        f = dot
        npf = np.dot
        assert np.allclose(f(self.t4, self.t), npf(self.t4, self.t))
        assert np.allclose(f(self.ft4, self.ft)[0, 0],
                           npf(self.ft4[0, 0], self.ft[0, 0]))
        assert np.allclose(f(self.fa, self.a)[0],
                           npf(self.fa[0], self.a))
        assert np.allclose(f(self.ft, self.fv)[0, 0],
                           npf(self.ft[0, 0], self.fv[0, 0]))
        assert np.allclose(f(self.ft, self.v)[0, 0],
                           npf(self.ft[0, 0], self.v))
        assert np.allclose(f(self.v, self.ft)[0, 0],
                           npf(self.v, self.ft[0, 0]))
        assert np.allclose(f(self.v, self.fv)[0, 0],
                           npf(self.v, self.fv[0, 0]))

        assert np.allclose(f(self.fs, self.fv), f(self.fv, self.fs))
        assert np.allclose(f(self.fv, self.v), f(self.v, self.fv))
        assert np.allclose(f(self.fs, self.v)[0, 0],
                           npf(self.v, self.fs[0, 0]))


class TestTensorCalc:
    t3 = Field(np.random.rand(20, 10, 3, 3), 2)
    t2 = Field(np.random.rand(20, 10, 2, 2), 2)

    def call_calc(self, calc):
        calc.tensor
        calc.shape
        calc.T
        calc.sym
        calc.skew
        calc.diag
        calc.trace
        calc.mean
        calc.dev
        calc.pvals
        calc.pvecs
        calc.ptensor
        calc.polar
        calc.svd
        calc.eig
        calc.inv
        calc.det
        calc.I1
        calc.I2
        calc.I3
        calc.J2
        calc.J3
        calc.sqrtJ2
        calc.p
        calc.q
        calc.a
        calc.b
        calc.theta

    def test_call_t2(self):
        calc = TensorCalc(self.t2)
        self.call_calc(calc)

    def test_call_t3(self):
        calc = TensorCalc(self.t3)
        self.call_calc(calc)

    def test_call_t2sym(self):
        t2 = self.t2 + transpose(self.t2)
        calc = TensorCalc(t2)
        self.call_calc(calc)

    def test_call_t3sym(self):
        t3 = self.t3 + transpose(self.t3)
        calc = TensorCalc(t3)
        self.call_calc(calc)


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
