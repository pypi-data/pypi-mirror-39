# -*- coding: utf-8 -*-

import pytest
from fempy.geometry.tools import *


class TestTools:
    def test_make3D(self):
        np.testing.assert_almost_equal(coors3D([1.]), [1, 0, 0])
        np.testing.assert_almost_equal(coors3D(1.), [1, 0, 0])
        np.testing.assert_almost_equal(coors3D([[1], [2.]]),
                                       [[1, 0, 0], [2, 0, 0]])
        with pytest.raises(ValueError):
            coors3D([1., 2, 3, 4])
            coors3D([[1., 2, 3, 4], [1., 2, 3, 4]])
            coors3D([[[1]]])

#    def test_contains_points(self):
#        polygon = [[0, 0, 0], [1, 1, 0], [0, 0, 1]]
#        points1 = [[0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]
#        points2 = [[0.2, 0.2, -0.2], [0.3, 0.3, 0.3]]
#        # points3 = [[0.5, 0.5, 0.5]]
#        assert contains_points(polygon, points1).all()
#        assert not contains_points(polygon, points2).all()
#        assert contains_points(polygon, points2).any()

    def test_add_dimensions(self):
        a = np.random.rand(10, 2)
        b = np.zeros((10, 1))
        r = np.append(a, b, axis=1)
        assert np.allclose(add_dimensions(a), r)

        a = np.random.rand(10, 1)
        b = np.zeros((10, 2))
        r = np.append(a, b, axis=1)
        assert np.allclose(add_dimensions(a), r)

        a = np.random.rand(10, 3)
        assert np.allclose(add_dimensions(a), a)

    def test_contains(self):
        pytest.importorskip('shapely')
        polygon = [[0, 0, 0], [1, 1, 0], [0, 0, 1]]
        points1 = [[0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]
        points2 = [[0.2, 0.2, -0.2], [0.3, 0.3, 0.3]]
        # points3 = [[0.5, 0.5, 0.5]]
        assert contains(polygon, points1)
        assert not contains(polygon, points2)
#        assert contains_points(polygon, points2)

    def test_disjoint(self):
        pytest.importorskip('shapely')
        polygon = [[0, 0, 0], [1, 1, 0], [0, 0, 1]]
        points1 = [[0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]
        points2 = [[0.2, 0.2, -0.2], [0.3, 0.3, 0.3]]
        points3 = [[0.2, 0.2, -0.2], [-0.3, -0.3, 0.3]]
        assert not disjoint(polygon, points1)
        assert not disjoint(polygon, points2)
        assert disjoint(polygon, points3)
        # assert not contains_points(polygon, points3) # when on border

    def test_natural_spline(self):
        from fempy.geometry import Point, Line, Spline, PlaneSurface, Polygon
        coors = [[0, 0], [np.pi/2., 1], [np.pi, 0.31], [3*np.pi/2., 1],
                 [2*np.pi, 0], [3*np.pi/2., -1]]
        pts = [Point(c) for c in coors]
        s = Spline(pts, order=2)
        S = PlaneSurface([s, Line(pts[0], pts[-1])], 'srf', elsize=0.1)

        x, y = list(zip(*coors))
        sx = NaturalSpline(x)
        sy = NaturalSpline(y)
        ti = np.linspace(0, 1, 200)
        xi = sx.eval(ti)
        yi = sy.eval(ti)
        poly = list(zip(xi, yi))
        P = Polygon(poly)
#        (P+S).gmsh.preview()

    def test_natural_closed(self):
        from fempy.geometry import Point, Spline, PlaneSurface, Polygon
        coors = [[0, 0], [np.pi/2., 1], [np.pi, 0.31], [3*np.pi/2., 1],
                 [2*np.pi, 0], [3*np.pi/2., -1], [0, 0]]
        pts = [Point(c) for c in coors]
        pts[-1] = pts[0]
        s = Spline(pts, order=2)
        S = PlaneSurface([s], 'srf', elsize=0.1)

        x, y = list(zip(*coors))
        sx = NaturalSpline(x, closed=True)
        sy = NaturalSpline(y, closed=True)
        ti = np.linspace(0, 1, 200)
        xi = sx.eval(ti)
        yi = sy.eval(ti)
        poly = list(zip(xi, yi))
        P = Polygon(poly)
#        (P+S).gmsh.preview()

    def test_gmsh_spline(self):
        from fempy.geometry import Point, Line, Spline, PlaneSurface, Polygon
        coors = [[0, 0], [np.pi/2., 1], [np.pi, 0.31], [3*np.pi/2., 1],
                 [2*np.pi, 0], [3*np.pi/2., -1]]
        pts = [Point(c) for c in coors]
        s = Spline(pts, order=2)
        S = PlaneSurface([s, Line(pts[0], pts[-1])], 'srf', elsize=0.1)

        x, y = list(zip(*coors))
        sx = GmshSpline(x)
        sy = GmshSpline(y)
        ti = np.linspace(0, 1, 200)
        xi = sx.eval(ti)
        yi = sy.eval(ti)
        poly = list(zip(xi, yi))
        P = Polygon(poly)
#        (P+S).gmsh.preview()

    def test_gmsh_spline_closed(self):
        from fempy.geometry import Point, Spline, PlaneSurface, Polygon
        coors = [[0, 0], [np.pi/2., 1], [np.pi, 0.31], [3*np.pi/2., 1],
                 [2*np.pi, 0], [3*np.pi/2., -1], [0, 0]]
        pts = [Point(c) for c in coors]
        pts[-1] = pts[0]
        s = Spline(pts, order=2)
        S = PlaneSurface([s], 'srf', elsize=0.1)

        x, y = list(zip(*coors))
        sx = GmshSpline(x, closed=True)
        sy = GmshSpline(y, closed=True)
        ti = np.linspace(0, 1, 200)
        xi = sx.eval(ti)
        yi = sy.eval(ti)
        poly = list(zip(xi, yi))
        P = Polygon(poly)
#        (P+S).gmsh.preview()


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
