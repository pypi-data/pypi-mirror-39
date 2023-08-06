# -*- coding: utf-8 -*-

import pytest
from fempy.geometry.shapes import *

class TestShapes:
    def test_rectangle(self):
        R = Rectangle()
        R.gmsh.msh
        R.gmsh.options.Mesh.CharacteristicLengthFactor = 1
#        R.gmsh.preview()

    def test_rectangle_periodic(self):
        R = Rectangle(periodic=True)
        R.points[0].elsize_factor=0.25
        R.gmsh.msh
#        R.gmsh.options.Mesh.CharacteristicLengthFactor = 0.5
#        R.gmsh.preview()

    def test_rectangles(self):
        Rectangles().gmsh.msh
        #Rectangles().gmsh.preview()

    def test_polygon(self):
        p = Polygon([[0, 0], [1, 0],[0, 1]])
        p.gmsh.msh
        #p.gmsh.preview()

    def test_circle(self):
        Circle().gmsh.msh
        #Circle().gmsh.preview()

    def test_circles(self):
        Circles().gmsh.msh
        #Circles().gmsh.preview()

    def test_ellipse(self):
        Ellipse().gmsh.msh
        #Ellipse().gmsh.preview()

    def test_ellipses(self):
        E = Ellipses([(1, 0.5), (0.75, 0.4), (0.5, 0.25)])
        E.gmsh.msh
        #E.gmsh.options.Mesh.CharacteristicLengthFromCurvature = 1
        #E.gmsh.preview()

    def test_random_hull(self):
        pytest.importorskip('shapely')
        RandomHull().gmsh.msh
        #RandomHull().gmsh.preview()

    def test_flow_rve(self):
        FlowRVE().gmsh.msh
        #FlowRVE().gmsh.preview()

    def test_box(self):
        Box().gmsh.msh
        # Box().gmsh.preview()
        
    def test_cylinder(self):
        pytest.importorskip("pygmsh")
        g = Cylinder()
        g.gmsh.msh
        g.gmsh.domain()
#        g.preview()

    def test_multipy(self):
        R1 = Rectangle()
        R2 = R1.copy()
        R2.move([1, 0])
        R = R1 + R2
#        R.gmsh.preview()

    def test_save_load(self):
        import tempfile
        tempdir = tempfile.gettempdir()
        R = Rectangle()
        R.save(tempdir + '/aaabbbccc')
        R2 = g.Geometry.load(tempdir + '/aaabbbccc')
        R2.coors
        R2.gmsh.msh


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file
