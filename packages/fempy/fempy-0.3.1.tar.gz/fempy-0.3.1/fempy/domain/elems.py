# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:20:15 2014

@author: mwojc
"""
import numpy as np


class Element(object):
    """
    Base finite element from which all elements should derive

    Subclasses have to provide the following attributes:
        ncoors          - local coordinates of nodes
        gcoors          - local coordinates of Gauss points
        gweights        - weights of Gauss points
        faces           - array of nodes defining faces or None
        btype           - type of face element or None

    and methods:
        shp(xloc)
        shpd(xloc)
        shpd2(xloc) [optional]
    """
    name = None
    shpd2 = None
    gshpd2 = None

    faces = None
    btype = None
    bncoors = None
    bgcoors = None
    bgshp = None
    bgshpd = None
    bgshpd2 = None
    nfaces = None

    def __init__(self):
        gc = self.gcoors
        self.nshp = np.array([self.shp(xloc) for xloc in self.ncoors])
        self.gshp = np.array([self.shp(xloc) for xloc in gc])
        self.gshpd = np.array([self.shpd(xloc) for xloc in gc])
        if self.shpd2 is not None:
            self.gshpd2 = np.array([self.shpd2(xloc) for xloc in gc])
        self.ngauss, self.nnode, self.ndime = self.gshpd.shape
        # boundary data...
        if self.faces is not None and self.btype is not None:
            if not isinstance(self.btype, Element):
                self.btype = self.btype()
            self.bncoors = self.ncoors[self.faces]
            self.bgcoors = np.einsum('eni, gn -> egi',
                                     self.bncoors, self.btype.gshp)
            self.bgshp = np.array([[self.shp(xloc) for xloc in bgc]
                                  for bgc in self.bgcoors])
            self.bgshpd = np.array([[self.shpd(xloc) for xloc in bgc]
                                   for bgc in self.bgcoors])
            if self.shpd2 is not None:
                self.bgshpd2 = np.array([[self.shpd2(xloc) for xloc in bgc]
                                        for bgc in self.bgcoors])
            self.nfaces = len(self.faces)


class Point10(Element):
    """
    1-node dummy point element
    """
    # Name used throughout fempy
    name = 'point'
    # Coordinates of nodes
    ncoors = np.array([[0.]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[0.]])
    gweights = np.array([1.])
    # Face ordering
    faces = None
    # Face element type
    btype = None

    # Shape functions...
    def shp(self, xloc):
        shp = np.zeros(1)
        shp[0] = 1.
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        dshp = np.array(()).reshape((1, 0))
        return dshp


class Line21(Element):
    """
    2-noded line with 1 Gauss point
    """
    # Name used throughout fempy
    name = 'line2'
    # Coordinates of nodes
    ncoors = np.array([[-1.], [1.]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[0.]])
    gweights = np.array([2.])
    # Face ordering
    faces = np.array([[0], [1]])
    # Face element type
    btype = Point10
    # Element segments (specific for 1D elements only)
    segments = [[0, 1]]

    # Shape functions...
    def shp(self, xloc):
        xi, = xloc
        shp = np.zeros(2)
        shp[0] = 0.5*(1.0-xi)
        shp[1] = 0.5*(1.0+xi)
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, = xloc
        dshp = np.zeros((2, 1))
        dshp[0, 0] = -0.5
        dshp[1, 0] = 0.5
        return dshp


class Line32(Element):
    """
    3-noded line with 2 Gauss points
    """
    # Name used throughout fempy
    name = 'line3'
    # Coordinates of nodes
    ncoors = np.array([[-1.], [1.], [0.]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[-0.577350269189626], [0.577350269189626]])
    gweights = np.array([1., 1.])
    # Face ordering
    faces = np.array([[0], [1]])
    # Face element type
    btype = Point10
    # Element segments (specific for 1D elements only)
    segments = [[0, 2], [2, 1]]

    # Shape functions...
    def shp(self, xloc):
        xi, = xloc
        shp = np.zeros(3)
        shp[0] = 0.5*xi*(xi-1.0)
        shp[1] = 0.5*xi*(xi+1.0)
        shp[2] = 1.0 - xi*xi
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, = xloc
        dshp = np.zeros((3, 1))
        dshp[0, 0] = xi-0.5
        dshp[1, 0] = xi+0.5
        dshp[2, 0] = -2.0*xi
        return dshp

    # ...and their second derivatives
    def shpd2(self, xloc):
        xi, = xloc
        dshp2 = np.zeros((3, 1, 1))
        dshp2[0, 0, 0] = 1.
        dshp2[1, 0, 0] = 1.
        dshp2[2, 0, 0] = -2.
        return dshp2


class Line32a(Element):
    """
    3-noded line with 2 Gauss points
    """
    # Name used throughout fempy
    name = 'line3a'
    # Coordinates of nodes
    ncoors = np.array([[-1.], [1.], [0.]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[-0.577350269189626], [0.577350269189626]])
    gweights = np.array([1., 1.])
    # Face ordering
    faces = np.array([[0], [1]])
    # Face element type
    btype = Point10
    # Element segments (specific for 1D elements only)
    segments = [[0, 2], [2, 1]]

    # Shape functions...
    def shp(self, xloc):
        xi, = xloc
        shp = np.zeros(3)
        shp[0] = 0.5*(1.0-xi)
        shp[1] = 0.5*(1.0+xi)
        shp[2] = 0.
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, = xloc
        dshp = np.zeros((3, 1))
        dshp[0, 0] = -0.5
        dshp[1, 0] = 0.5
        dshp[2, 0] = 0.
        return dshp


class Tria31(Element):
    """
    3-noded triangle with 1 Gauss point
    """
    # Name used throughout fempy
    name = 'tria3'
    # Coordinates of nodes
    ncoors = np.array([[0., 0.], [1., 0.], [0., 1.]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[0.333333333333333, 0.333333333333333]])
    gweights = np.array([0.5])
    # Face ordering
    faces = np.array([[0, 1], [1, 2], [2, 0]])
    # Face element type
    btype = Line21

    # Shape functions...
    def shp(self, xloc):
        xi, et = xloc
        shp = np.zeros(3)
        shp[0] = 1.-xi-et
        shp[1] = xi
        shp[2] = et
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, et = xloc
        dshp = np.zeros((3, 2))
        dshp[0, 0] = -1.
        dshp[1, 0] = 1.
        dshp[2, 0] = 0.
        dshp[0, 1] = -1.
        dshp[1, 1] = 0.
        dshp[2, 1] = 1.
        return dshp


class Tria63(Element):
    """
    6-noded triangle with 3 Gauss points
    """
    # Name used throughout fempy
    name = 'tria6'
    ncoors = np.array([[0., 0.], [1., 0.], [0., 1.],
                       [.5, 0.], [.5, .5], [0., .5]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[0.166666666666667, 0.166666666666667],
                       [0.666666666666667, 0.166666666666667],
                       [0.166666666666667, 0.666666666666667]])
    gweights = np.array([0.166666666666666, 0.166666666666666,
                         0.166666666666666])
    # Face ordering
    faces = np.array([[0, 1, 3], [1, 2, 4], [2, 0, 5]])
    # Face element type
    btype = Line32

    # Shape functions...
    def shp(self, xloc):
        xi, et = xloc
        shp = np.zeros(6)
        shp[0] = 2.*(0.5-xi-et)*(1.-xi-et)
        shp[1] = xi*(2.*xi-1.)
        shp[2] = et*(2.*et-1.)
        shp[3] = 4.*xi*(1.-xi-et)
        shp[4] = 4.*xi*et
        shp[5] = 4.*et*(1.-xi-et)
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, et = xloc
        dshp = np.zeros((6, 2))
        dshp[0, 0] = 4.*(xi+et)-3.
        dshp[1, 0] = 4.*xi-1.
        dshp[2, 0] = 0.
        dshp[3, 0] = 4.*(1.-2.*xi-et)
        dshp[4, 0] = 4.*et
        dshp[5, 0] = -4.*et
        dshp[0, 1] = 4.*(xi+et)-3.
        dshp[1, 1] = 0.
        dshp[2, 1] = 4.*et-1.
        dshp[3, 1] = -4.*xi
        dshp[4, 1] = 4.*xi
        dshp[5, 1] = 4.*(1.-xi-2.*et)
        return dshp

    # ...and their second derivatives
    def shpd2(self, xloc):
        xi, et = xloc
        dshp2 = np.zeros((6, 2, 2))
        dshp2[0, 0, 0] = 4.
        dshp2[1, 0, 0] = 4.
        dshp2[2, 0, 0] = 0.
        dshp2[3, 0, 0] = -8.
        dshp2[4, 0, 0] = 0.
        dshp2[5, 0, 0] = 0.
        dshp2[0, 1, 0] = 4.
        dshp2[1, 1, 0] = 0.
        dshp2[2, 1, 0] = 0.
        dshp2[3, 1, 0] = -4.
        dshp2[4, 1, 0] = 4.
        dshp2[5, 1, 0] = -4.
        dshp2[0, 0, 1] = 4.
        dshp2[1, 0, 1] = 0.
        dshp2[2, 0, 1] = 0.
        dshp2[3, 0, 1] = -4.
        dshp2[4, 0, 1] = 4.
        dshp2[5, 0, 1] = -4.
        dshp2[0, 1, 1] = 4.
        dshp2[1, 1, 1] = 0.
        dshp2[2, 1, 1] = 4.
        dshp2[3, 1, 1] = 0.
        dshp2[4, 1, 1] = 0.
        dshp2[5, 1, 1] = -8.
        return dshp2


class Tria63a(Element):
    """
    6-noded triangle with 3 Gauss points
    """
    # Name used throughout fempy
    name = 'tria6a'
    ncoors = np.array([[0., 0.], [1., 0.], [0., 1.],
                       [.5, 0.], [.5, .5], [0., .5]])
    # Coordinates and weights of Gauss points
    gcoors = np.array([[0.166666666666667, 0.166666666666667],
                       [0.666666666666667, 0.166666666666667],
                       [0.166666666666667, 0.666666666666667]])
    gweights = np.array([0.166666666666666, 0.166666666666666,
                         0.166666666666666])
    # Face ordering
    faces = np.array([[0, 1, 3], [1, 2, 4], [2, 0, 5]])
    # Face element type
    btype = Line32a

    # Shape functions...
    def shp(self, xloc):
        xi, et = xloc
        shp = np.zeros(6)
        shp[0] = 1.-xi-et
        shp[1] = xi
        shp[2] = et
        shp[3] = 0.
        shp[4] = 0.
        shp[5] = 0.
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, et = xloc
        dshp = np.zeros((6, 2))
        dshp[0, 0] = -1.
        dshp[1, 0] = 1.
        dshp[2, 0] = 0.
        dshp[3, 0] = 0.
        dshp[4, 0] = 0.
        dshp[5, 0] = 0.
        dshp[0, 1] = -1.
        dshp[1, 1] = 0.
        dshp[2, 1] = 1.
        dshp[3, 1] = 0.
        dshp[4, 1] = 0.
        dshp[5, 1] = 0.
        return dshp


class Tetr41(Element):
    """
    4-noded tetrahedra with 1 Gauss points
    """
    # Name used throughout fempy
    name = 'tetr4'
    # Coordinates of nodes
    ncoors = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    # Coordinates and weights of Gauss points
    gcoors = \
        np.array([[0.250000000000000, 0.250000000000000, 0.250000000000000]])
    gweights = np.array([0.166666666666667])
    # Face ordering
    faces = np.array([[0, 1, 3], [1, 2, 3], [2, 0, 3], [0, 2, 1]])
    # Face element type
    btype = Tria31

    # Shape functions...
    def shp(self, xloc):
        xi, et, ze = xloc
        shp = np.zeros(4)
        shp[0] = 1.-xi-et-ze
        shp[1] = xi
        shp[2] = et
        shp[3] = ze
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, et, ze = xloc
        dshp = np.zeros((4, 3))
        dshp[0, 0] = -1.
        dshp[1, 0] = 1.
        dshp[2, 0] = 0.
        dshp[3, 0] = 0.
        dshp[0, 1] = -1.
        dshp[1, 1] = 0.
        dshp[2, 1] = 1.
        dshp[3, 1] = 0.
        dshp[0, 2] = -1.
        dshp[1, 2] = 0.
        dshp[2, 2] = 0.
        dshp[3, 2] = 1.
        return dshp


class Tetr104(Element):
    """
    10-noded tetrahedra with 4 Gauss points
    """
    # Name used throughout fempy
    name = 'tetr10'
    # Coordinates of nodes
    ncoors = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.], [0., 0., 1.],
                       [.5, 0., 0.], [.5, .5, 0.], [0., .5, 0.],
                       [0., 0., .5], [0., .5, .5], [.5, 0., .5]])
    # Coordinates and weights of Gauss points
    gcoors = \
        np.array([[0.138196601125011, 0.138196601125011, 0.138196601125011],
                  [0.585410196624968, 0.138196601125011, 0.138196601125011],
                  [0.138196601125011, 0.585410196624968, 0.138196601125011],
                  [0.138196601125011, 0.138196601125011, 0.585410196624968]])
    gweights = \
        np.array([0.041666666666667, 0.041666666666667, 0.041666666666667,
                  0.041666666666667])
    # Face ordering
    faces = np.array([[0, 1, 3, 4, 9, 7], [1, 2, 3, 5, 8, 9],
                      [2, 0, 3, 6, 7, 8], [0, 2, 1, 6, 5, 4]])
    # Face element type
    btype = Tria63

    # Shape functions...
    def shp(self, xloc):
        xi, et, ze = xloc
        a = 1.-xi-et-ze
        shp = np.zeros(10)
        shp[0] = (2.*a-1.)*a
        shp[1] = xi*(2.*xi-1.)
        shp[2] = et*(2.*et-1.)
        shp[3] = ze*(2.*ze-1.)
        shp[4] = 4.*xi*a
        shp[5] = 4.*xi*et
        shp[6] = 4.*et*a
        shp[7] = 4.*ze*a
        shp[8] = 4.*et*ze
        shp[9] = 4.*xi*ze
        return shp

    # ...and their derivatives
    def shpd(self, xloc):
        xi, et, ze = xloc
        dshp = np.zeros((10, 3))
        dshp[0, 0] = 1.-4.*(1.-xi-et-ze)
        dshp[1, 0] = 4.*xi-1.
        dshp[2, 0] = 0.
        dshp[3, 0] = 0.
        dshp[4, 0] = 4.*(1.-2.*xi-et-ze)
        dshp[5, 0] = 4.*et
        dshp[6, 0] = -4.*et
        dshp[7, 0] = -4.*ze
        dshp[8, 0] = 0.
        dshp[9, 0] = 4.*ze
        dshp[0, 1] = 1.-4.*(1.-xi-et-ze)
        dshp[1, 1] = 0.
        dshp[2, 1] = 4.*et-1.
        dshp[3, 1] = 0.
        dshp[4, 1] = -4.*xi
        dshp[5, 1] = 4.*xi
        dshp[6, 1] = 4.*(1.-xi-2.*et-ze)
        dshp[7, 1] = -4.*ze
        dshp[8, 1] = 4.*ze
        dshp[9, 1] = 0.
        dshp[0, 2] = 1.-4.*(1.-xi-et-ze)
        dshp[1, 2] = 0.
        dshp[2, 2] = 0.
        dshp[3, 2] = 4.*ze-1.
        dshp[4, 2] = -4.*xi
        dshp[5, 2] = 0.
        dshp[6, 2] = -4.*et
        dshp[7, 2] = 4.*(1.-xi-et-2.*ze)
        dshp[8, 2] = 4.*et
        dshp[9, 2] = 4.*xi
        return dshp

    # ...and their second derivatives
    def shpd2(self, xloc):
        xi, et, ze = xloc
        dshp2 = np.zeros((10, 3, 3))
        dshp2[0, 0, 0] = 4.
        dshp2[1, 0, 0] = 4.
        dshp2[2, 0, 0] = 0.
        dshp2[3, 0, 0] = 0.
        dshp2[4, 0, 0] = -8.
        dshp2[5, 0, 0] = 0.
        dshp2[6, 0, 0] = 0.
        dshp2[7, 0, 0] = 0.
        dshp2[8, 0, 0] = 0.
        dshp2[9, 0, 0] = 0.
        dshp2[0, 1, 0] = 4.
        dshp2[1, 1, 0] = 0.
        dshp2[2, 1, 0] = 0.
        dshp2[3, 1, 0] = 0.
        dshp2[4, 1, 0] = -4.
        dshp2[5, 1, 0] = 4.
        dshp2[6, 1, 0] = -4.
        dshp2[7, 1, 0] = 0.
        dshp2[8, 1, 0] = 0.
        dshp2[9, 1, 0] = 0.
        dshp2[0, 2, 0] = 4.
        dshp2[1, 2, 0] = 0.
        dshp2[2, 2, 0] = 0.
        dshp2[3, 2, 0] = 0.
        dshp2[4, 2, 0] = -4.
        dshp2[5, 2, 0] = 0.
        dshp2[6, 2, 0] = 0.
        dshp2[7, 2, 0] = -4.
        dshp2[8, 2, 0] = 0.
        dshp2[9, 2, 0] = 4.
        dshp2[0, 0, 1] = 4.
        dshp2[1, 0, 1] = 0.
        dshp2[2, 0, 1] = 0.
        dshp2[3, 0, 1] = 0.
        dshp2[4, 0, 1] = -4.
        dshp2[5, 0, 1] = 4.
        dshp2[6, 0, 1] = -4.
        dshp2[7, 0, 1] = 0.
        dshp2[8, 0, 1] = 0.
        dshp2[9, 0, 1] = 0.
        dshp2[0, 1, 1] = 4.
        dshp2[1, 1, 1] = 0.
        dshp2[2, 1, 1] = 4.
        dshp2[3, 1, 1] = 0.
        dshp2[4, 1, 1] = 0.
        dshp2[5, 1, 1] = 0.
        dshp2[6, 1, 1] = -8.
        dshp2[7, 1, 1] = 0.
        dshp2[8, 1, 1] = 0.
        dshp2[9, 1, 1] = 0.
        dshp2[0, 2, 1] = 4.
        dshp2[1, 2, 1] = 0.
        dshp2[2, 2, 1] = 0.
        dshp2[3, 2, 1] = 0.
        dshp2[4, 2, 1] = 0.
        dshp2[5, 2, 1] = 0.
        dshp2[6, 2, 1] = -4.
        dshp2[7, 2, 1] = -4.
        dshp2[8, 2, 1] = 4.
        dshp2[9, 2, 1] = 0.
        dshp2[0, 0, 2] = 4.
        dshp2[1, 0, 2] = 0.
        dshp2[2, 0, 2] = 0.
        dshp2[3, 0, 2] = 0.
        dshp2[4, 0, 2] = -4.
        dshp2[5, 0, 2] = 0.
        dshp2[6, 0, 2] = 0.
        dshp2[7, 0, 2] = -4.
        dshp2[8, 0, 2] = 0.
        dshp2[9, 0, 2] = 4.
        dshp2[0, 1, 2] = 4.
        dshp2[1, 1, 2] = 0.
        dshp2[2, 1, 2] = 0.
        dshp2[3, 1, 2] = 0.
        dshp2[4, 1, 2] = 0.
        dshp2[5, 1, 2] = 0.
        dshp2[6, 1, 2] = -4.
        dshp2[7, 1, 2] = -4.
        dshp2[8, 1, 2] = 4.
        dshp2[9, 1, 2] = 0.
        dshp2[0, 2, 2] = 4.
        dshp2[1, 2, 2] = 0.
        dshp2[2, 2, 2] = 0.
        dshp2[3, 2, 2] = 4.
        dshp2[4, 2, 2] = 0.
        dshp2[5, 2, 2] = 0.
        dshp2[6, 2, 2] = 0.
        dshp2[7, 2, 2] = -8.
        dshp2[8, 2, 2] = 0.
        dshp2[9, 2, 2] = 0.


# Convenience definitions
etypes = {'point': Point10,
          'line2': Line21,
          'line3': Line32,
          'tria3': Tria31,
          'tria6': Tria63,
          'tetr4': Tetr41,
          'tetr10': Tetr104}


edims = {(0, 1):  etypes['point'],
         (1, 2):  etypes['line2'],
         (1, 3):  etypes['line3'],
         (2, 3):  etypes['tria3'],
         (2, 6):  etypes['tria6'],
         (3, 4):  etypes['tetr4'],
         (3, 10): etypes['tetr10']
         }


def guess_etype(coors, conec, etype=None):
    enode = conec.shape[1]
    if isinstance(etype, Element):
        assert enode == etype.nnode, \
            "Conec requires %s-node element but %s is defined on %s" \
            " nodes." % (enode, etype.__name__, etype.nnode)
        return etype
    try:
        if isinstance(etype, type) and issubclass(etype, Element):
            etype = etype()
            assert enode == etype.nnode, \
                "Conec requires %s-node element but %s is defined on %s" \
                " nodes." % (enode, etype.__name__, etype.nnode)
            return etype
    except TypeError:
        pass
    if isinstance(etype, str) and etype in etypes:
        return etypes[etype]()
    if isinstance(etype, int):  # etype is treated as edime
        try:
            return edims[(etype, enode)]()
        except KeyError:
            raise ValueError("%iD element with %i nodes not found!"
                             % (etype, enode))
    if etype is None:
        if enode == 1:  # point
            etype = Point10
        elif enode == 2:  # line2
            etype = Line21
        elif enode == 3:
            if len(np.intersect1d(conec[:, :2], conec[:, 2])) == 0:  # line3
                # TODO: doesn't work for single element...
                etype = Line32
            else:
                etype = Tria31
        elif enode == 4:
            etype = Tetr41  # tetr4
        elif enode == 6:  # tria6
            etype = Tria63
        elif enode == 10:  # tetr10
            etype = Tetr104
        else:
            raise ValueError("Element type is not recognized!")
        return etype()
    raise ValueError("Unknown element type: %s" % etype)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')

