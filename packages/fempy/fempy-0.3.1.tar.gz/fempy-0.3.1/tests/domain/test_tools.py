# -*- coding: utf-8 -*-
import pytest
from fempy.domain.tools import *
import fempy.testing as testing
import numpy as np


class TestTools(object):
    def test_unique_rows_lex(self):
        a = np.arange(12).reshape(4, 3)
        b = np.arange(12)[::-1].reshape(4, 3)
        c = np.concatenate((a, b))
        idx, msk = unique_rows_lex(c, sort=True, strict=False)
        assert np.allclose(idx, [0, 7, 1, 6, 2, 5, 3, 4])
        assert np.allclose(msk, [1, 0, 1, 0, 1, 0, 1, 0])

    def test_unique_rows(self):
        a = np.arange(12).reshape(4, 3)
        b = np.arange(12)[::-1].reshape(4, 3)
        c = np.concatenate((a, b))
        c2 = np.concatenate((b, a))
        assert np.allclose(unique_rows(c), True)
        assert np.allclose(unique_rows(c, strict=False), True)
        assert np.allclose(unique_rows(c, sort=True), False)
        assert np.allclose(unique_rows(c, sort=True, strict=False),
                           [True]*4 + [False]*4)
        assert np.allclose(unique_rows(c2, sort=True, strict=False),
                           [True]*4 + [False]*4)
        assert len(unique_rows(np.array([], dtype=np.int))) == 0

    def test_duplicate_rows(self):
        a = np.arange(12).reshape(4, 3)
        b = np.arange(12)[::-1].reshape(4, 3)
        c = np.concatenate((a, b))
        assert np.allclose(np.sort(duplicate_rows(c)),
                           [1, 2, 3, 4, 5, 6, 7, 8])
        assert np.allclose(duplicate_rows(c, sort=True),
                           [1, 2, 3, 4, 4, 3, 2, 1])
        assert len(duplicate_rows(np.array([], dtype=np.int))) == 0

    def test_in2d(self):
        a = np.arange(12).reshape(4, 3)
        b = np.arange(12)[::-1].reshape(4, 3)
        c = np.concatenate((a, b))
        np.allclose(in2d(c, a[:2]), [True]*2 + [False]*6)
        np.allclose(in2d(c, a[:2], sort=True),
                    [True]*2 + [False]*4 + [True]*2)

    def test_sum_rows(self):
        # integer arr
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        mask = np.array([True, False, False, True, True,
                         False, True, False])
        res = np.array([1+2+3, 4, 5+6, 7+8])
        assert np.allclose(res, uneven_sum(arr, mask))
        # with keepshape
        res = np.array([6, 6, 6, 4, 11, 11, 15, 15])
        assert np.allclose(res, uneven_sum(arr, mask, keepshape=True))

        # boolean arr
        arr = np.array([True, False, True, False, False, True, False, True])
        mask = np.array([True, False, False, True, True, False, True, False])
        res = np.array([True, False, True, True])
        assert np.allclose(res, uneven_sum(arr, mask))
        res2 = np.add.reduceat(arr, np.nonzero(mask)[0])
        assert np.allclose(res2 > 0, uneven_sum(arr, mask))
        # with keepshape
        res = np.array([True, True, True, False, True, True, True, True])
        assert np.allclose(res, uneven_sum(arr, mask, keepshape=True))

    def test_agree_rows(self):
        a = np.arange(12).reshape(4, 3)
        b = np.arange(12)[::-1].reshape(4, 3)
        aidx, bidx = agree_rows(a, a[::-1])
        assert np.allclose(a[aidx], a[::-1][bidx])
        with pytest.raises(ValueError):
            aidx, bidx = agree_rows(a, b)

    def test_create_faces(self):
        d = testing.common.SquareWithCircle()
        f = create_faces(d)
        f['BOUNDARY']


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
