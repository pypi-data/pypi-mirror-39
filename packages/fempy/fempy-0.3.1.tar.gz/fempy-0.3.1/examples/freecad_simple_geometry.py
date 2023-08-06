# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:15:43 2017

@author: mwojc
"""
from fempy.geometry.gmsh import Gmsh
from fempy.geometry.tools import tmpfname
import sys
sys.path.append('/usr/lib64')
import FreeCAD, Part, Draft


def Circles(R=1., r=0.85, shift=(0, 0, 0), hole=True):
    d = FreeCAD.newDocument()
    cout = Draft.makeCircle(R)
    p = FreeCAD.Placement()
    p.Base = shift
    cin = Draft.makeCircle(r, p)
    geometry = cout.Shape.cut(cin.Shape)
    if not hole:
        geometry = Part.Compound([geometry, cin.Shape])
    fname = tmpfname() + '.brep'
    geometry.exportBrep(fname)
    g = Gmsh(fname)
    g.options.Mesh.CharacteristicLengthFactor = 0.25
    g.options.Mesh.ElementOrder = 2
    return g


def Balls(R=1., r=0.85, shift=(0, 0, 0), hole=True):
    d = FreeCAD.newDocument()
    b1 = Part.makeSphere(R)
    b2 = Part.makeSphere(r, FreeCAD.Vector(*shift))
    geometry = b1.cut(b2)
    if not hole:
        geometry = Part.Compound([geometry, b2])
    fname = tmpfname() + '.brep'
    geometry.exportBrep(fname)
    g = Gmsh(fname)
    g.options.Mesh.CharacteristicLengthFactor = 0.25
    g.options.Mesh.ElementOrder = 2
    return g


Circles(shift=(1, 0, 0)).preview()
Balls(shift=(0, 0, 1)).preview()
