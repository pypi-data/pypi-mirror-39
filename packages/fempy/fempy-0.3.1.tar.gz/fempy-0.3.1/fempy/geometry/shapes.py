# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 07:14:03 2014

@author: mwojc
"""
import numpy as np
from fempy.geometry import geometry as g


def _group_prefix(group):
    if group == '':
        prefix = ''
        group = 'domain'
    else:
        prefix = str(group) + '_'
        group = group
    return group, prefix


def Rectangle(a=1., b=1., lb=None, group='', periodic=False, **kwargs):
    if lb is None:
        lb = -a/2., -b/2.
    group, prefix = _group_prefix(group)
    x0, y0 = lb
    A = g.Point([x0, y0],
                groups=[prefix + 'bottom_left', prefix + 'corners'])
    B = g.Point([x0+a, y0],
                groups=[prefix + 'bottom_right', prefix + 'corners'])
    C = g.Point([x0+a, y0+b],
                groups=[prefix + 'top_right', prefix + 'corners'])
    D = g.Point([x0, y0+b],
                groups=[prefix + 'top_left', prefix + 'corners'])

    AB = g.Line(A, B, [prefix + 'bottom', prefix + 'boundary'])
    BC = g.Line(B, C, [prefix + 'right', prefix + 'boundary'])
    CD = g.Line(C, D, [prefix + 'top', prefix + 'boundary'])
    DA = g.Line(D, A, [prefix + 'left', prefix + 'boundary'])

    if periodic:
        AB.periodic(CD)
        DA.periodic(BC)

    ABCD = g.PlaneSurface([AB, BC, CD, DA], group, **kwargs)
    if 'elsize' not in kwargs:
        ABCD.elsize = min([a, b])/8.
    return ABCD


class Shape(object):
    pass


class Rectangle2(Shape):
    """
    D               C
    +---------------+
    |               |
    |               |
    |       +       |
    |     (0,0)     |
    |               |
    +---------------+
    A               B
    """
    def __init__(self, a=1., b=1., lb=None, elsize=None, periodic=False):
        if lb is None:
            lb = -a/2., -b/2.
        x0, y0 = lb
        A = g.Point([x0, y0], groups=['A', 'bottom_left', 'corners'])
        B = g.Point([x0+a, y0], groups=['B', 'bottom_right', 'corners'])
        C = g.Point([x0+a, y0+b], groups=['C', 'top_right', 'corners'])
        D = g.Point([x0, y0+b], groups=['D', 'top_left', 'corners'])

        AB = g.Line(A, B, ['AB', 'bottom'])
        BC = g.Line(B, C, ['BC', 'right'])
        CD = g.Line(C, D, ['CD', 'top'])
        DA = g.Line(D, A, ['DA', 'left'])

        if elsize is None:
            elsize = min([a, b])/8.

        if periodic:
            AB.periodic(CD)
            DA.periodic(BC)

        ABCD = g.PlaneSurface([AB, BC, CD, DA], elsize=elsize)

        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.AB = AB
        self.BC = BC
        self.CD = CD
        self.DA = DA
        self.ABCD = ABCD

    def domain(self, order=1, verbose=False):
        d = self.ABCD.gmsh.domain(order, verbose)
        d.geometry = self
        return d

    def preview(self, default='geomsh'):
        self.ABCD.gmsh.preview(default)


def Rectangles(a=[1., 0.5], b=[1., 0.5], lb=None, hole=False, **kwargs):
    assert len(a) == len(b)     # a and b have to be of the same length
    assert a == sorted(a, reverse=True)  # a have to be in descending order
    assert b == sorted(b, reverse=True)  # b have to be in descending order
    rectangles = [Rectangle(a[0], b[0], group='D0', **kwargs)]
    for i in range(1, len(a)):
        rec = Rectangle(a[i], b[i], group='D'+str(i), **kwargs)
        rectangles[-1].add_hole(rec)
        rectangles.append(rec)
    if hole is True:
        rectangles = rectangles[:-1]
    G = g.Geometry(rectangles)
    if lb is not None:
        vec = (lb[0]+a[0]/2., lb[1]+b[0]/2.)
        G.move(vec)

    if len(rectangles) == 1:
        return rectangles[0]  # if single circle with hole
    else:
        return G


def Polygon(coors, group='', close=True, surface=True, **kwargs):
    coors = g.tools.coors3D(coors)
    group, prefix = _group_prefix(group)
    pts = [g.Point(c) for c in coors]
    is_closed = False
    if pts[0].eq(pts[-1]):
        pts[-1] = pts[0]
        is_closed = True
    if close:
        if pts[0].ne(pts[-1]):
            pts += [pts[0]]  # Close polygon if not closed
            is_closed = True
    lines = []
    for i in range(len(pts)-1):
        l = g.Line(pts[i], pts[i+1], [prefix+'line%i' % i,
                                      prefix+'boundary'])
        lines += [l]
    if is_closed and surface:
        srf = g.PlaneSurface(lines, group, **kwargs)
        return srf
    else:
        geo = g.Geometry(lines, group=group, **kwargs)
        return geo


def Layers2D(H=[1.], L=[1.], firstL=True, elsize=None, elsize_factor=1.):
    points = []
    lines = []
    left = []
    right = []
    layers = []
    if elsize is None:
        def elsize(x, y):
            He = np.array(H)
            He = np.abs(He)
            He = He[He > 1e-15]
            return min(min(He)/3., sum(He)/20.)
    if isinstance(elsize, (int, float)):
        def elsize(x, y):
            return float(elsize)
    for i, h in enumerate(H):
        if i > 0 and firstL and len(L) > 2:
            L = [L[0], L[-1]]
        pts = []
        for j, l in enumerate(L):
            els = elsize(l, h) * elsize_factor
            pts.append(g.Point([l, h], groups='p%s%s' % (i, j), elsize=els))
        lin = [g.Line(p0, p1) for p0, p1 in zip(pts[:-1], pts[1:])]
        for k, l in enumerate(lin):
            l.add_to_groups(['line%s%s' % (i, k), 'line%s' % i])
            if i == 0:
                l.add_to_groups('top')
            if i == len(H)-1:
                l.add_to_groups('bottom')
        if i > 0:
            pts0 = points[i-1]
            lin0 = lines[i-1]
            llin = g.Line(pts0[0], pts[0], groups='left')
            rlin = g.Line(pts0[-1], pts[-1], groups='right')
            layer = g.PlaneSurface(lin + [rlin] + lin0 + [llin],
                                   groups='layer%s' % str(i-1))
            left.append(llin)
            right.append(rlin)
            layers.append(layer)
        points.append(pts)
        lines.append(lin)
#    if elsize is None:
#        H = np.array(H)
#        H = np.abs(H)
#        H = H[H > 1e-15]
#        elsize = min(min(H)/3., sum(H)/20.)*elsize_factor
    geo = g.Geometry(layers) #, elsize=elsize)
    geo.layers = layers
    geo.lines = lines
    geo.right = right
    return geo


def Circle(r=1., center=(0., 0.), group='', **kwargs):
    xc, yc = center
    group, prefix = _group_prefix(group)  # default group is 'domain'
    O = g.Point(center)
    A = g.Point((xc+r, yc), groups=[prefix+'A'])
    B = g.Point((xc, yc+r), groups=[prefix+'B'])
    C = g.Point((xc-r, yc), groups=[prefix+'C'])
    D = g.Point((xc, yc-r), groups=[prefix+'D'])
    AOB = g.CircularArc(A, O, B, [prefix+'q1', prefix+'boundary'])
    BOC = g.CircularArc(B, O, C, [prefix+'q2', prefix+'boundary'])
    COD = g.CircularArc(C, O, D, [prefix+'q3', prefix+'boundary'])
    DOA = g.CircularArc(D, O, A, [prefix+'q4', prefix+'boundary'])
    if 'elsize' not in kwargs:
        kwargs['elsize'] = r/5.
    AOA = g.PlaneSurface([AOB, BOC, COD, DOA], group, **kwargs)
    return AOA


def Circles(r=[1.0, 0.5], center=(0, 0), hole=False, **kwargs):
    assert r == sorted(r, reverse=True)  # r have to be in descending order
    circles = [Circle(r[0], center=center, group='D0', **kwargs)]
    for i in range(1, len(r)):
        circ = Circle(r[i], center=center, group='D'+str(i), **kwargs)
        circles[-1].add_hole(circ)
        circles.append(circ)
    if hole is True:
        circles = circles[:-1]

    if len(circles) == 1:
        return circles[0]  # if single circle with hole
    else:
        return g.Geometry(circles)


def Ellipse(r=(1., 0.5), center=(0, 0), group='', **kwargs):
    ra, rb = r
    xc, yc = center
    group, prefix = _group_prefix(group)  # default group is 'domain'
    O = g.Point(center)
    A = g.Point((xc+ra, yc))
    B = g.Point((xc, yc+rb))
    C = g.Point((xc-ra, yc))
    D = g.Point((xc, yc-rb))
    AOAB = g.EllipticalArc(A, O, A, B, [prefix+'q1', prefix+'boundary'])
    BOAC = g.EllipticalArc(B, O, A, C, [prefix+'q2', prefix+'boundary'])
    COAD = g.EllipticalArc(C, O, A, D, [prefix+'q3', prefix+'boundary'])
    DOAA = g.EllipticalArc(D, O, A, A, [prefix+'q4', prefix+'boundary'])
    if 'elsize' not in kwargs:
        kwargs['elsize'] = sum(r)/10.
    AOA = g.PlaneSurface([AOAB, BOAC, COAD, DOAA], group, **kwargs)
    return AOA


def Ellipses(r=[(1.0, 0.5), (0.5, 0.25)], center=(0, 0), hole=False, **kwargs):
    ra, rb = zip(*r)
    assert list(ra) == sorted(ra, reverse=True)  # in descending order?
    assert list(rb) == sorted(rb, reverse=True)  # in descending order?
    elps = [Ellipse(r=(ra[0], rb[0]), center=center, group='D0', **kwargs)]
    for i in range(1, len(r)):
        ei = Ellipse(r=(ra[i], rb[i]), center=center,
                     group='D'+str(i), **kwargs)
        elps[-1].add_hole(ei)
        elps.append(ei)
    if hole is True:
        elps = elps[:-1]

    if len(elps) == 1:
        return elps[0]  # if single circle with hole
    else:
        return g.Geometry(elps)


def RandomHull(r=1., n=10, center=(0, 0), res=200, clcurve=0, group='',
               **kwargs):
    assert n > 2

    from scipy.spatial import ConvexHull
    from shapely.geometry import LinearRing

    group, prefix = _group_prefix(group)  # default group is 'domain'

    def hull():
        R = np.random.uniform(0, r, n)
        theta = np.random.uniform(0, 2*np.pi, n)
        x0, y0 = center
        x = x0 + R * np.cos(theta)
        y = y0 + R * np.sin(theta)
        coors = np.asarray([x, y]).T
        hull = ConvexHull(coors)
        hcoors = coors[hull.vertices]
        nh = 2
        dist = r/4.
        while nh <= 2:
            rhcoors = g.tools.reduce_coors(hcoors, dist)
            nh = len(rhcoors)
            dist = dist/2.
        points = [g.Point(hc) for hc in rhcoors]
        points = points + [points[0]]
        return points

    spline = g.Spline(hull(), groups=prefix+'boundary')
    vertices = spline.poly(res=res)
    while not LinearRing(vertices).is_simple:
        spline = g.Spline(hull(), groups=prefix+'boundary')
        vertices = spline.poly(res=res)
    if 'elsize' not in kwargs:
        radii = np.linalg.norm((vertices - vertices.mean(axis=0)), axis=1)
        elsize = radii.mean()/3.
        kwargs['elsize'] = elsize
    surface = g.PlaneSurface([spline], groups=group, **kwargs)
    surface.gmsh.options.Mesh.CharacteristicLengthFromCurvature = clcurve
    return surface


def FlowRVE(r=1., h=0.1, elsize_factor=1., full=False):
    #ri = -0.585786437626905*h + 0.414213562373095*r
    h = h/2.
    ri = np.sqrt(2)*(r+h)-r-2*h
    mid = (h+r) - r*np.sqrt(2)/2.

    p0 = g.Point([-r-h, -h])
    p1 = g.Point([-h, -r-h])
    p2 = g.Point([h, -r-h])
    p3 = g.Point([r+h, -h])
    p4 = g.Point([r+h, h])
    p5 = g.Point([h, r+h])
    p6 = g.Point([-h, r+h])
    p7 = g.Point([-r-h, h])
    p8 = g.Point([-r-h, -r-h])
    p9 = g.Point([r+h, -r-h])
    p10 = g.Point([r+h, +r+h])
    p11 = g.Point([-r-h, +r+h])

    p6x = g.Point([-mid, mid], elsize=r/10.)
    p0x = g.Point([-mid, -mid], elsize=r/10.)
    p2x = g.Point([mid, -mid], elsize=r/10.)
    p4x = g.Point([mid, mid], elsize=r/10.)

    c0 = g.CircularArc(p6, p11, p6x, 'outer_boundary, fixed, upper_left')
    c0x = g.CircularArc(p6x, p11, p7, 'outer_boundary, fixed, upper_left')
    c1 = g.CircularArc(p0, p8, p0x, 'outer_boundary, fixed, lower_left')
    c1x = g.CircularArc(p0x, p8, p1, 'outer_boundary, fixed, lower_left')
    c2 = g.CircularArc(p2, p9, p2x, 'outer_boundary, fixed, lower_right')
    c2x = g.CircularArc(p2x, p9, p3, 'outer_boundary, fixed, lower_right')
    c3 = g.CircularArc(p4, p10, p4x, 'outer_boundary, fixed, upper_right')
    c3x = g.CircularArc(p4x, p10, p5, 'outer_boundary, fixed, upper_right')
    c4 = g.Line(p5, p6, 'outer_boundary, flow, top', elsize=h/3.)
    c5 = g.Line(p7, p0, 'outer_boundary, flow, left', elsize=h/3.)
    c6 = g.Line(p1, p2, 'outer_boundary, flow, bottom', elsize=h/3.)
    c7 = g.Line(p3, p4, 'outer_boundary, flow, right', elsize=h/3.)

    srf = g.PlaneSurface([c0, c0x, c5, c1, c1x, c6, c2, c2x, c7, c3, c3x, c4],
                         'domain, matrix_domain')

    hole = Circle(ri, group='inner')
    srf.add_hole(hole)
    srf.elsize_factor = elsize_factor

    if not full:
        return srf

    l0 = g.Line(p6, p11, 'outer_boundary, fixed, top')
    l0x = g.Line(p11, p7, 'outer_boundary, fixed, left')
    srf1 = g.PlaneSurface([l0, l0x, c0, c0x], 'outer_void')
    l1 = g.Line(p0, p8, 'outer_boundary, fixed, left')
    l1x = g.Line(p8, p1, 'outer_boundary, fixed, bottom')
    srf2 = g.PlaneSurface([l1, l1x, c1, c1x], 'outer_void')
    l2 = g.Line(p2, p9, 'outer_boundary, fixed, bottom')
    l2x = g.Line(p9, p3, 'outer_boundary, fixed, right')
    srf3 = g.PlaneSurface([l2, l2x, c2, c2x], 'outer_void')
    l3 = g.Line(p4, p10, 'outer_boundary, fixed, right')
    l3x = g.Line(p10, p5, 'outer_boundary, fixed, top')
    srf4 = g.PlaneSurface([l3, l3x, c3, c3x], 'outer_void')
    return srf+srf1+srf2+srf3+srf4


def Box(a=1., b=1., c=1., origin=(0., 0., 0.), elsize=None, elsize_factor=1.,
        group='', periodic=False, **kwargs):
    from fempy.geometry import Gmsh
    elsize = min((a, b, c))/5. if elsize is None else elsize
    elsize *= elsize_factor
    code = \
"""
SetFactory("OpenCASCADE");
v0 = newv;
Box(v0) = {{{}}};
pts_v0[] = PointsOf{{Volume{{v0}};}};
Characteristic Length{{pts_v0[]}} = {};
""".format(str(origin+(a, b, c))[1:-1], elsize)
    geometry = Gmsh(code, entities={3: {1: 'domain'},
                                    2: {1: 'back', 2: 'front',
                                        3: 'left', 4: 'right',
                                        5: 'bottom', 6: 'top'},
                                    0: {2: 'origin', 7: 'abc'}
                                    })
    return geometry


def Cylinder(x0=(0, 0, 0.), axis=(0, 0, 1.), radius=0.5, angle=None,
             elsize=None, elsize_factor=1., **kwargs):
    import pygmsh
    from fempy.geometry import Gmsh
    elsize = 0.2 * radius * elsize_factor if elsize is None else elsize
    g = pygmsh.opencascade.Geometry()
    g.add_cylinder(x0, axis, radius, angle=angle, char_length=elsize)
    geometry = Gmsh(g, entities={3: {1: 'domain'},
                                 2: {1: 'side', 2: 'top', 3: 'bottom'},
                                 1: {1: 'top_egde', 2: 'side_edge',
                                     3: 'bottom_egde'},
                                 0: {1: 'top_point', 2: 'bottom_point'},
                                 })
    return geometry


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')

#    g = FlowRVE(full=True)
#    g.gmsh.preview()

#    def rigid_bcs(d):
#        # Discover points for fixing rigid body movement
#        b = d.boundary
#        bcoors = b.coors
#        tol = abs(bcoors.max()-bcoors.min()) * 1e-14
#        X, Y, Z = bcoors.T
#        # first point - for all dofs fixing
#        idx = np.nonzero(np.abs(X - X.min()) < tol)[0]
#        if len(idx) > 1:
#            idx = idx[np.abs(Y[idx] - Y[idx].min()) < tol]
#        if len(idx) > 1:
#            idx = idx[np.abs(Z[idx] - Z[idx].min()) < tol]
#        b.ngroups['fix0'] = idx
#        # second point for fixing second dof
#        idx = np.nonzero(np.abs(Y - Y.min()) < tol)[0]
#        if len(idx) > 1:
#            idx = idx[np.abs(X[idx] - X[idx].max()) < tol]
#        if len(idx) > 1:
#            idx = idx[np.abs(Z[idx] - Z[idx].min()) < tol]
#        b.ngroups['fix1'] = idx
#        # other points are necessary only for 3D
#        if d.ndime == 3:
#            # third point for fixing third dof
#            idx = np.nonzero(np.abs(Y - Y.max()) < tol)[0]
#            if len(idx) > 1:
#                idx = idx[np.abs(X[idx] - X[idx].min()) < tol]
#            if len(idx) > 1:
#                idx = idx[np.abs(Z[idx] - Z[idx].min()) < tol]
#            b.ngroups['fix2'] = idx
#            # fourth point for fixing first dof
#            idx = np.nonzero(np.abs(Z - Z.max()) < tol)[0]
#            if len(idx) > 1:
#                idx = idx[np.abs(X[idx] - X[idx].max()) < tol]
#            if len(idx) > 1:
#                idx = idx[np.abs(Y[idx] - Y[idx].max()) < tol]
#            b.ngroups['fix3'] = idx
#
#
#    from fempy.models.elastic import LinearElastic3D, Axisymmetry
#    from fempy.geometry.gmsh_io import preview_field
#
#    class Thermal3D(LinearElastic3D):
#        def setup_domain(self):
#            self.geometry = Cylinder(elsize=0.2)
#            self.domain = self.geometry.gmsh.domain()
#
#        def setup_model(self):
#            rigid_bcs(self.domain)
#            self.bcs['fix0'] = [True, True, True]
#            self.bcs['fix1'] = [False, True, False]
#            self.bcs['fix2'] = [False, False, True]
#            self.bcs['fix3'] = [True, False, False]
#            self.ev(20000., 0.3)
#            self.alpha(1e-4)
#            self.T[:] += 3.
#
#    m3D = Thermal3D()
#    m3D.solve()
#    preview_field(m3D.sigma[..., 1, 1], name='sigma33', d=m3D.domain)
#
#
#    class Thermal2DPlaneStrain(PlaneStrain):
#        def setup_domain(self):
#            self.geometry = Rectangle(10, 10, lb=(0, 0), elsize=0.3)
#            self.domain = self.geometry.gmsh.domain()
#
#        def setup_model(self):
#            self.bcs['bottom_left'] = [True, True]
#            self.bcs['bottom_right'] = [False, True]
#            self.ev(20000., 0.3)
#            self.alpha[:] = 1e-4 * np.array([[1, 0], [0, 1]])
#            self.T[:] += 3.
#
#    m2D = Thermal2DPlaneStrain()
#    m2D.solve()
#    preview_field(m2D.sigmaz, name='sigma33',d=m2D.domain)
