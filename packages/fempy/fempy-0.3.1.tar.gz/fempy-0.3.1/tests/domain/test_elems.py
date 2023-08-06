# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 22:47:46 2014

@author: mwojc
"""

import numpy as np
import fempy.domain.elems as elems
from fempy.domain.domain import Domain


class TestElements(object):
    def test_attributes(self):
        for k, v in elems.__dict__.items():
            if isinstance(v, type) and issubclass(v, elems.Element) and \
                    v is not elems.Element:
                e = v()
                e.ncoors
                e.gcoors
                e.gweights
                e.shp
                e.shpd
                e.shpd2
                e.gshp
                e.gshpd
                e.gshpd2
                e.ngauss
                e.nnode
                e.ndime

                e.faces
                e.btype
                e.bncoors
                e.bgcoors
                e.bgshp
                e.bgshpd
                e.bgshpd2
                e.nfaces

    def test_line21(self):
        allc = np.allclose
        e = elems.Line21()
        assert allc(e.nshp, np.eye(e.nnode))

        d = Domain(e.ncoors, np.arange(e.nnode)[None, :])  # single element d
        b = d.boundary
        assert allc(d.vol, 2.0)
        assert allc(b.vol, 2.0)

    def test_tetr41_and_tetr104(self):
        allc = np.allclose
        for e in elems.Tetr41(), elems.Tetr104():
            assert allc(e.nshp, np.eye(e.nnode))

            # single element domain
            d = Domain(e.ncoors, np.arange(e.nnode)[None, :])
            assert allc(d.vol, 0.1666666666667)

            # Faces
            faces = d.boundary
            assert allc(faces.evol, [0.5, 0.8660254, 0.5, 0.5])
            assert allc(faces.vol, 2.36602540378)
            n = faces.normal
            assert allc(n[0], [0, -1, 0])
            assert allc(n[1], [0.57735027, 0.57735027, 0.57735027])
            assert allc(n[2], [-1, 0, 0])
            assert allc(n[3], [0, 0, -1])

            # Edges
            n = faces[0].boundary.normal
            assert allc(n[0], [0, 0, -1])
            assert allc(n[1], [0.70710678, 0., 0.70710678])
            assert allc(n[2], [-1, 0., 0.])
            assert allc(faces[0].boundary.evol, [1., 1.41421356, 1.])

            n = faces[1].boundary.normal
            assert allc(n[0], [0.40824829, 0.40824829, -0.81649658])
            assert allc(n[1], [-0.81649658, 0.40824829, 0.40824829])
            assert allc(n[2], [0.40824829, -0.81649658, 0.40824829])
            assert allc(faces[1].boundary.evol,
                        [1.41421356, 1.41421356, 1.41421356])

            n = faces[2].boundary.normal
            assert allc(n[0], [0, 0, -1])
            assert allc(n[1], [0,  -1,  0.])
            assert allc(n[2], [0., 0.70710678, 0.70710678])
            assert allc(faces[2].boundary.evol, [1., 1., 1.41421356])

            n = faces[3].boundary.normal
            assert allc(n[0], [-1, 0, 0])
            assert allc(n[1], [0.70710678, 0.70710678, 0.])
            assert allc(n[2], [0, -1, 0.])
            assert allc(faces[3].boundary.evol, [1., 1.41421356, 1.])


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])  # Run tests from current file
