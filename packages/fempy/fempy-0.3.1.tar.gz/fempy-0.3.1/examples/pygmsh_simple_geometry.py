# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""
import pygmsh
from fempy.geometry import Gmsh

# Geometry and domain
pg = pygmsh.built_in.Geometry()
c1 = pg.add_circle([0., 0., 0.], 1., 0.25)
c2 = pg.add_circle([0., 0., 0.], 5., 1, holes=[c1])
t1, v1, l1 = pg.extrude(c1.plane_surface, [0, 0, 3.])
t2, v2, l2 = pg.extrude(c2.plane_surface, [0, 0, 3.])
g = Gmsh(pg, entities={3: {1: 'c1',
                           2: 'c2'},
                       2: {5:  'c1_bottom',
                           10: 'c2_bottom',
                           27: 'c1_top',
                           59: 'c2_top',
                           18: 'c1_side',
                           22: 'c1_side',
                           26: 'c1_side',
                           38: 'c2_side',
                           42: 'c2_side',
                           46: 'c2_side'
                           }
                       }
         )
g.preview()
