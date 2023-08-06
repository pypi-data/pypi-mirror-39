# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 10:45:27 2014

@author: mwojc
"""

##########################################################
import numpy as np
from fempy.fields.fields import Field
from fempy.fields.algebra import transpose


class Test_Field:
    r0 = np.random.rand(10)
    r1 = np.random.rand(10, 3)
    r2 = np.random.rand(10, 2, 2)
    r3 = np.random.rand(10, 3, 3, 3)
    r4 = np.random.rand(10, 4, 4, 4, 6)

    def test_getitem(self):
        f = Field(self.r4, groups={'a': [1, 2, 3], 'b': [5, 4]})
        assert np.allclose(f['a'], self.r4[[1, 2, 3]])
        assert np.allclose(f['a', 0], self.r4[[1, 2, 3], 0])
        assert np.allclose(f['b'][0], self.r4[5])

        # Groups work only on first axis
        f = Field(self.r4, prefix=2, groups={'a': [1, 2, 3], 'b': [5, 4]})
        assert np.allclose(f['a'], self.r4[[1, 2, 3]])
        assert np.allclose(f['a', 0], self.r4[[1, 2, 3], 0])
        assert np.allclose(f['b'][0], self.r4[5])

    def test_setitem(self):
        f = Field(self.r2, groups={'a': [1, 2, 3], 'b': [5, 4]})
        f['a'] = 3.
        assert np.allclose(f['a'], 3.)
        f['b'] = [[1, 2], [3, 4]]
        assert np.allclose(f['b', 1, 1], 4.)
        assert np.allclose(f['b'][0], [[1, 2], [3, 4]])
        f['b'] = [4, 5]
        assert np.allclose(f['b'][0], [[4, 5], [4, 5]])
        f['b', 0] = 7.
        assert np.allclose(f['b'][0], [[7, 7], [4, 5]])
        f['b', 1, 0] = 17.
        assert np.allclose(f['b'][0], [[7, 7], [17, 5]])

        # Groups work only on first axis
        f = Field(self.r2, prefix=2, groups={'a': [1, 2, 3], 'b': [5, 4]})
        f['b'] = [[1, 2], [3, 4]]
        assert np.allclose(f['b', 1, 1], 4.)
        assert np.allclose(f['b'][0], [[1, 2], [3, 4]])
        f['b'] = [4, 5]
        assert np.allclose(f['b'][0], [[4, 5], [4, 5]])

    def test_scalar_field_creation(self):
        f = Field(self.r0)
        assert f.base is self.r0
        assert f.pshape == (10,)
        assert f.paxes == (0,)
        assert f.sshape == ()
        assert f.saxes == ()
        assert (f == transpose(f)).all()
        f = Field(self.r1, 2)
        assert f.base is self.r1
        assert f.pshape == (10, 3)
        assert f.paxes == (0, 1)
        assert f.sshape == ()
        assert f.saxes == ()
        assert (f == transpose(f)).all()

    def test_vector_field_creation(self):
        f = Field(self.r1)
        assert f.base is self.r1
        assert f.pshape == (10,)
        assert f.paxes == (0,)
        assert f.sshape == (3,)
        assert f.saxes == (1,)
        assert (f == transpose(f)).all()
        f = Field(self.r2, 2)
        assert f.base is self.r2
        assert f.pshape == (10, 2)
        assert f.paxes == (0, 1)
        assert f.sshape == (2,)
        assert f.saxes == (2,)
        assert (f == transpose(f)).all()

    def test_tensor_field_creation(self):
        f = Field(self.r2)
        assert f.base is self.r2
        assert f.pshape == (10,)
        assert f.paxes == (0,)
        assert f.sshape == (2, 2)
        assert f.saxes == (1, 2)
        fT = np.transpose(self.r2, (0, 2, 1))
        assert (fT == transpose(f)).all()
        f = Field(self.r3, 2)
        assert f.base is self.r3
        assert f.pshape == (10, 3)
        assert f.paxes == (0, 1)
        assert f.sshape == (3, 3)
        assert f.saxes == (2, 3)
        fT = np.transpose(self.r3, (0, 1, 3, 2))
        assert (fT == transpose(f)).all()

    def test_any_field_creation(self):
        f = Field(self.r4, 2)
        assert f.base is self.r4
        assert f.pshape == (10, 4)
        assert f.paxes == (0, 1)
        assert f.sshape == (4, 4, 6)
        assert f.saxes == (2, 3, 4)
        fT = np.transpose(self.r4, (0, 1, 4, 3, 2))
        assert (fT == transpose(f)).all()

    def test_ufuncs(self):
        # ufuncs should return field only if pshape of the result is the same
        f = Field(self.r0)  # scalar
        assert isinstance(np.sum(f), float)
        f = Field(self.r2)  # tensor
        assert isinstance(np.sum(f, 2), Field)
        assert isinstance(np.sum(f, 0), np.ndarray)


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
