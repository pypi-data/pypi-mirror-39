# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 21:30:46 2014

@author: mwojc
"""

from fempy.geometry import Rectangle
from fempy.models.elastic import ev2cijkl
from fempy.fields.nfields import nVector
from fempy.fields.gfields import gScalar, gVector, gTensor, gTensor4
from fempy.fields.operators import dot, grad, nabla
from fempy.fields.operators import qform, lform, dirichlet
from fempy.fields.algebra import transpose, tensordot
from fempy.solvers.linear import dsolve  # direct solver
from fempy.geometry.gmsh_io import preview_fields

d = Rectangle(elsize=0.05).gmsh.domain(2)

# Assemble stiffness matrix
u = nVector(d)
nu = nabla(u)
bu = 0.5*(nu + transpose(nu))  # small strain operator
cijkl = gTensor4(d, ev2cijkl(20000., 0.3, ndime=2))  # material tensor
K = qform(cijkl, bu)  # the same trial and test

# Assemble body forces - weight
F = nVector(d)
rho = gScalar(d, 2.)
gravity = gVector(d, [0., -9.81])
weight = dot(rho, gravity)
F += lform(weight)

# Assemble boundary pressures (given vector)
q = gVector(d.boundary)
q['left'] = [10, 0.]
F += lform(q)  # operator(onboundary(u)))

# Assemble boundary pressures (given scalar normal pressure)
p = gScalar(d.boundary)
p['right'] = -10.
n = d.boundary.normal
f = dot(p, n)
F += lform(f)  # operator(onboundary(u)))

# Assemble thermal load
alpha = 1e-4 * gTensor(d, [[1., 0], [0, 1]])
dT = 3.
eps_dT = alpha * dT
sigma_dT = (1 + 0.3)*tensordot(cijkl, eps_dT)  # 0.3 is Poisson coefficient
F += lform(sigma_dT, bu)

# Dirichlet BC's
r = dirichlet(u)
u['top', 1] = -0.0005
r['top', 1] = True
r['bottom'] = True

# Solve (linear)
u = dsolve(K, F, r, u)

# Strains and stresses
du = grad(u)
eps = 0.5*(du + transpose(du))
sigma = tensordot(cijkl, eps - eps_dT)

# View
preview_fields([u, sigma], ['u [m]', 'stress [kPa]'])

# FempyView is currently depreciated
#from fempy.view import FempyView
#view = FempyView(d, u*500, mesh_visible=True)
#view.cell_scalars(sigma[..., 0, 1, 1], name='Syy', legend=True)

#view.point_scalars(onnodes(sigma)[:, 1, 1], name='Syy')
#view.point_scalars(onboundary(onnodes(sigma))[:, 1, 1], name='Syy')
#view.add_lines(d.boundary.coors, d.boundary.conec)
#view.cell_scalars(sigma[:, 0, 1, 1], name='Syy', legend=True)
