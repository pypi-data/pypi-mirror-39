# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""
from fempy.geometry.shapes import Rectangle
from fempy.models.elastic import PlaneStrain

d = Rectangle(elsize=0.05).gmsh.domain(order=2)
m = PlaneStrain(d)

# material properties
m.ev(20000, 0.3)
m.alpha(1e-4)
m.rho[:] = 2.

# loads
m.p['right'] = -10.
m.qi['left'] = [10, 0.]

# temperature increase
m.T += 3.

# dirichlet bcs
m.u['top', 1] = -0.0005
m.bcs['top', 1] = True
m.bcs['bottom'] = True

m.solve()
m.preview('u')
# m.preview('all')


# FempyView is depreciated
## View
#from fempy.view import FempyView
##d.coors += m.u*500  # add displacements to mesh
#view = FempyView(d, m.u*500, mesh_visible=True)
#view.cell_scalars(sigma[..., 0, 1, 1], name='Syy', legend=True)
##from fempy.fields.operators import onnodes
##view.point_scalars(onnodes(sigma)[..., 1, 1], name='Syy', legend=True)
