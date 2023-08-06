# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 22:47:46 2014

@author: mwojc
"""
import numpy as np
from fempy.domain.domain import Domain
from fempy.testing import testdata
from fempy.domain import elems


class Simple2D(object):
    """
      6 __7__ 8
       |\ |\ |
      3|_\4_\|5
       |\ |\ |
       |_\|_\|__
      0   1  2  9

    """
    coors = np.array([[0, 0],   # 0
                      [1, 0],   # 1
                      [2, 0],   # 2
                      [0, 1],   # 3
                      [1, 1],   # 4
                      [2, 1],   # 5
                      [0, 2],   # 6
                      [1, 2],   # 7
                      [2, 2],   # 8
                      [3, 0]],  # 9
                     dtype=float)
    conec2D = np.array([[0, 1, 3],   # 0
                        [1, 4, 3],   # 1
                        [1, 2, 4],   # 2
                        [2, 5, 4],   # 3
                        [3, 4, 6],   # 4
                        [4, 7, 6],   # 5
                        [4, 5, 7],   # 6
                        [5, 8, 7]],  # 7
                       dtype=int)
    conec1D = np.array([[0, 1],   # 0
                        [1, 2],   # 1
                        [2, 5],   # 2
                        [5, 8],   # 3
                        [8, 7],   # 4
                        [7, 6],   # 5
                        [6, 3],   # 6
                        [3, 0],   # 7
                        [2, 9]],  # 8
                       dtype=int)
    conec0D = np.array([[0],   # 0
                        [2],   # 1
                        [6],   # 2
                        [8],   # 3
                        [9]],  # 4
                       dtype=int)
    etype2D = elems.Tria31
    etype1D = elems.Line21
    etype0D = elems.Point10
    egroups2D = {'q1': [0, 1], 'q2': [2, 3], 'q3': [4, 5], 'q4': [6, 7]}
    egroups1D = {'b': [0, 1], 'r': [2, 3], 't': [4, 5], 'l': [6, 7], 'o': [8]}
    egroups0D = {'c1': [0], 'c2': [1], 'c3': [2], 'c4': [3], 'c5': [4]}
    ngroups = {'cline': [[3, 4], [4, 5]], 'cpoint': [4], 'opoint': [9],
               'cross': [6, 4, 2]}

    @property
    def domain2D(self):
        d = Domain(self.coors.copy(), self.conec2D, egroups=self.egroups2D,
                   ngroups=self.ngroups)
        f = d.faces
        ff = d.faces.faces
        for k, v in self.egroups1D.items():
            f.egroups.set_group_by_conec(k, self.conec1D[v], glob=True)
            # d.ngroups.update_global([(k, self.conec1D[v])])
        for k, v in self.egroups0D.items():
            ff.egroups.set_group_by_conec(k, self.conec0D[v], glob=True)
            # d.ngroups.update_global([(k, self.conec0D[v])])
        return d

    @property
    def domain1D(self):
        d = Domain(self.coors.copy(), self.conec1D, egroups=self.egroups1D,
                   ngroups=self.ngroups)
        f = d.faces
        for k, v in self.egroups0D.items():
            f.egroups.set_group_by_conec(k, self.conec0D[v], glob=True)
            # d.ngroups.update_global([(k, self.conec0D[v])])
        return d

    @property
    def domain0D(self):
        return Domain(self.coors.copy(), self.conec0D, egroups=self.egroups0D,
                      ngroups=self.ngroups)

    def domain2Dmv(self, v=[0, 0]):
        self.coors[4] += v  # move center point
        d = self.domain2D
        self.coors[4] -= v  # restore center point
        return d


class Simple3D(object):
    """
    Simple 3D domain
    """
    coors = np.loadtxt(testdata + 'simple3D.coors', dtype=float)

    conec3D = np.loadtxt(testdata + 'simple3D.conec3D', dtype=int)
    conec2D = np.loadtxt(testdata + 'simple3D.conec2D', dtype=int)
    conec1D = np.loadtxt(testdata + 'simple3D.conec1D', dtype=int)
    conec0D = np.loadtxt(testdata + 'simple3D.conec0D', dtype=int, ndmin=2)

    etype3D = elems.Tetr41
    etype2D = elems.Tria31
    etype1D = elems.Line21
    etype0D = elems.Point10

    egroups3D = {'center':  [0, 1, 2, 3],      # center elements
                 'bottome': [5, 10, 12, 6],    # elems with bottom faces
                 'lefte':   [5, 11, 9, 13],    # elems with left faces
                 'fronte':  [10, 13, 14, 15],  # elems with front faces
                 'righte':  [15, 12, 7, 8],    # elems with right faces
                 'backe':   [8, 6, 11, 4],     # elems with back faces
                 'tope':    [4, 9, 14, 7]}     # elems with top faces
    egroups2D = {'bottom':  [0, 1, 2, 3],      # z = 0
                 'left':    [4, 5, 6, 7],      # y = 0
                 'front':   [8, 9, 10, 11],    # x = 1
                 'right':   [12, 13, 14, 15],  # y = 1
                 'back':    [16, 17, 18, 19],  # x = 0
                 'top':     [20, 21, 22, 23]}  # z = 1
    egroups1D = {'bottoml': [0, 1, 2, 3],
                 'topl':    [4, 5, 6, 7],
                 'leftl':   [0, 4, 8, 9],
                 'frontl':  [1, 5, 9, 10],
                 'rightl':  [2, 6, 10, 11],
                 'backl':   [3, 7, 11, 8]}
    egroups0D = {'bottomc': [0, 1, 2, 3],
                 'topc':    [4, 5, 6, 7],
                 'leftc':   [0, 1, 4, 5],
                 'frontc':  [1, 2, 5, 6],
                 'rightc':  [2, 3, 6, 7],
                 'backc':   [3, 0, 7, 4]}
    ngroups = {'corners': [0, 1, 2, 3, 4, 5, 6, 7],
               'centers': [8, 9, 10, 11, 12, 13]}

    @property
    def domain3D(self):
        d = Domain(self.coors.copy(), self.conec3D, egroups=self.egroups3D,
                   ngroups=self.ngroups)
        f = d.faces
        ff = f.faces
        fff = ff.faces
        for k, v in self.egroups2D.items():
            f.egroups.set_group_by_conec(k, self.conec2D[v], glob=True)
        for k, v in self.egroups1D.items():
            ff.egroups.set_group_by_conec(k, self.conec1D[v], glob=True)
        for k, v in self.egroups0D.items():
            fff.egroups.set_group_by_conec(k, self.conec0D[v], glob=True)
        return d

    @property
    def domain2D(self):
        return Domain(self.coors, self.conec2D, egroups=self.egroups2D,
                      ngroups=self.ngroups)

    @property
    def domain1D(self):
        return Domain(self.coors, self.conec1D, egroups=self.egroups1D,
                      ngroups=self.ngroups)

    @property
    def domain0D(self):
        return Domain(self.coors, self.conec0D, egroups=self.egroups0D,
                      ngroups=self.ngroups)


def SquareWithCircle():
    """
    Produces square domain (a=1) with circular inclusion (r=0.25) for testing.
    """
    from fempy.geometry import Rectangle, Circle, Gmsh
    R = Rectangle(lb=(-0.5, -0.5))
    R.add_to_groups('r')
    C = Circle(r=0.25, center=(0, 0.))
    C.add_to_groups('c')
    R.add_hole(C)
    G = R + C  # now we have C in 'c, domain', R in 'r, domain'
    gm = Gmsh(G)
    return gm.domain()


if __name__ == "__main__":
    simple2D = Simple2D()
    simple2D.domain0D
    simple2D.domain1D
    simple2D.domain2D

    simple3D = Simple3D()
    simple3D.domain0D
    simple3D.domain1D
    simple3D.domain2D
    simple3D.domain3D

    SquareWithCircle()
