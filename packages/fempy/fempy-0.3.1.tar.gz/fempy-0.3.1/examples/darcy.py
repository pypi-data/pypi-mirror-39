# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""

from fempy.geometry import Rectangle
from fempy.fields.gfields import gScalar, gTensor
from fempy.fields.nfields import nScalar
from fempy.fields.operators import dot, grad, nabla, qform, lform, dirichlet
from fempy.solvers.linear import dsolve
from fempy.geometry.gmsh_io import preview_fields


d = Rectangle(elsize_factor=0.5).gmsh.domain(order=2)

# Assemble stiffness matrix
p = nScalar(d)
kij = gTensor(d, [[1., 0], [0, 1.]])
K = qform(kij, nabla(p))

# Assemble flux
q = gScalar(d.boundary)
q['left + bottom'] = 1.
q = -lform(q)

# Dirichlet BC's - prescribed pressures
r = dirichlet(p)
r['top + right'] = True
p['top + right'] = 1.

# Solve
p = dsolve(K, q, r, p)

# Retrieve velocities
v = -dot(kij, grad(p))

# Preview fields
preview_fields([p, v], ['p [kPa]', 'v [m/s]'])

# FempyView is depreciated
#### View
#from fempy.view import FempyView
#view = FempyView(d, mesh_visible=False)
#view.point_scalars(P, name='p')
#view.point_vectors(onnodes(V), name='v',
#                   scale_factor=0.05,
#                   color_mode='no_color')
