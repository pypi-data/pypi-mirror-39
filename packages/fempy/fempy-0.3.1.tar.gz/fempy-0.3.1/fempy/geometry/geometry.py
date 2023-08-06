# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:31:10 2013

@author: mwojc
"""

import numpy as np
import networkx as nx
from fempy.geometry.gmsh import Gmsh
from fempy.geometry import tools
import copy


class Geometry(object):
    """
    Class representing 3D geometry.

    Attributes
    ----------
    points : list
        Points representing geometry
    curves : list
        Curves representing geometry
    surfaces: list
        Surfaces representing geometry
    volumes: list
        Volumes representing geometry
    coors: numpy array
        Coordinates of points
    gmsh : fempy.geometry.Gmsh instance
        Generator of finite element meshes
    elsize : float or None
        Parameter determinig element size at all points of geometry
    elsize_factor: float or None
        Number by which elsize at each point is multiplied

    Methods
    -------

    """
    tol = 1e-7

    def __init__(self, entities=[], **kwargs):
        self._entities = set(entities)
        if 'elsize' not in kwargs:
            self.__dict__['elsize'] = None
        if 'elsize_factor' not in kwargs:
            self.__dict__['elsize_factor'] = None
        for (k, v) in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '%s' % (self.__class__.__name__,)  # self.groups)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.remove(other)

    def __setattr__(self, name, value):
        if name == 'elsize':
            # set via __dict__ to avoid recurrency
            for e in self.points + self.curves + self.surfaces + self.volumes:
                e.__dict__['elsize'] = value
                if not hasattr(e, 'elsize_factor'):
                    e.__dict__['elsize_factor'] = 1.0
                if e.elsize_factor is None:
                    e.__dict__['elsize_factor'] = 1.0
        elif name == 'elsize_factor':
            for e in self.points + self.curves + self.surfaces + self.volumes:
                e.__dict__['elsize_factor'] = value
                if e.elsize is None:
                    e.__dict__['elsize'] = 1.0
        else:
            object.__setattr__(self, name, value)

    def __get_groups(self, entities):
        groups = {}
        for ent in entities:
            for group in ent.groups:
                if group not in groups:
                    groups[group] = [ent]
                else:
                    groups[group] += [ent]
        return groups

    @property
    def points(self):
        pts = []
        for entity in self._entities:
            if isinstance(entity, Point):  # infinite reccurency otherwise
                pts += [entity]
            else:
                pts += entity.points
        #return list(set(pts))   # TODO: order is lost!
        return tools.uniquify(pts)

    @property
    def curves(self):
        crv = []
        for entity in self._entities:
            if isinstance(entity, Point):
                pass
            elif isinstance(entity, Curve):
                crv += [entity]
            else:
                crv += entity.curves
        #return list(set(crv))
        return tools.uniquify(crv)

    @property
    def surfaces(self):
        srf = []
        for entity in self._entities:
            if isinstance(entity, (Point, Curve)):
                pass
            elif isinstance(entity, Surface):
                srf += [entity]
            else:
                srf += entity.surfaces
        #return list(set(srf))
        return tools.uniquify(srf)

    @property
    def volumes(self):
        return []

    @property
    def point_groups(self):
        return self.__get_groups(self.points)

    @property
    def curve_groups(self):
        return self.__get_groups(self.curves)

    @property
    def surface_groups(self):
        return self.__get_groups(self.surfaces)

    @property
    def volume_groups(self):
        return self.__get_groups(self.volumes)

    @property
    def coors(self):
        coors = []
        for p in self.points:
            coors.append(p.coors)
        return np.array(coors)

    @property
    def gmsh(self):
        if not hasattr(self, '__gmsh'):
            self.__gmsh = Gmsh(self)
        return self.__gmsh

    def eq(self, other):
        return self == other

    def ne(self, other):
        return not self.eq(other)

    def add(self, others):
        """
        This method always returns new Geometry object
        """
        if not isinstance(others, (list, tuple)):
            others = [others]
        entities = self._entities
        sname = self.__class__.__name__
        for other in others:
            if not isinstance(other, Geometry):
                oname = other.__class__.__name__
                raise TypeError('Cannot add %s to %s' % (oname, sname))
            entities = entities.union(other._entities)
        return Geometry(entities)

    def remove(self, others):
        """
        This method always returns new Geometry object
        """
        if not isinstance(others, (list, tuple)):
            others = [others]
        entities = self._entities
        sname = self.__class__.__name__
        for other in others:
            if not isinstance(other, Geometry):
                oname = other.__class__.__name__
                raise TypeError('Cannot remove %s from %s' % (oname, sname))
            entities = entities.difference(other._entities)
        return Geometry(entities)

    def copy(self):
        return copy.deepcopy(self)

    def save(self, fname):
        tools.saveobj(self, fname, ext='.Geometry')

    @classmethod
    def load(cls, fname):
        return tools.loadobj(fname, ext='.Geometry')

    def move(self, vec):
        for p in self.points:
            p.move(vec)

    def rotate(self, angle, axis=[0., 0., 1.]):
        # angle in radians
        R = tools.rotation_matrix(axis, angle)
        for p in self.points:
            p._rotate(R)

    def resize(self, m=1., center=None, resize_elsize_factor=True):
        coors = self.coors
        if center is None:
            center = coors.mean(axis=0)
        vectors = coors - center
        updates = vectors * (m - 1.)
        for p, vec in zip(self.points, updates):
            p.move(vec)
        if resize_elsize_factor:
            if self.elsize_factor is not None:
                self.elsize_factor = self.elsize_factor * m


class Primitive(object):
    @property
    def groups(self):
        try:
            return sorted(list(self.__groups))
        except AttributeError:
            return []

    def add_to_groups(self, groups):
        if isinstance(groups, str):
            groups = groups.split(',')
            groups = [g.strip() for g in groups]
        groups = [str(g) for g in groups]
        try:
            self.__groups.update(groups)
        except:
            self.__groups = set(groups)

    def remove_from_groups(self, groups):
        if isinstance(groups, str):
            groups = groups.split(',')
            groups = [g.strip() for g in groups]
        self.__groups.difference_update(groups)

    def clear_groups(self):
        self.__groups.clear()


class Point(Geometry, Primitive):
    def __init__(self, coors, groups=[], **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        self.__coors = tools.coors3D(coors)
        self.add_to_groups(groups)
        Geometry.__init__(self, [self], **kwargs)

    @property
    def coors(self):
        return self.__coors

    def _rotate(self, R):
        self.__coors = R.dot(self.__coors)

    def move(self, vec):
        vec = tools.coors3D(vec)
        self.__coors += vec

    def eq(self, other):
        if type(self) == type(other):
            tol = min(self.tol, other.tol)
            return (abs(self.coors - other.coors) < tol).all()
        return False

    def distance(self, other):
        return np.linalg.norm(self.coors-other.coors)


class Curve(Geometry, Primitive):
    orientation = 1  # physical orientation - manipulated in PlaneSurface
    slaves = None

    def eq(self, other):
        if type(self) == type(other):
            sp = self.points
            op = other.points
            if len(sp) == len(op):  # not necesserily true for splines
                check = [p1.eq(p2) for p1, p2 in zip(sp, op)]
                if False not in check:
                    return True
        return False

    def is_reversed(self, other):
        if type(self) == type(other):
            sp = self.points
            op = other.points[::-1]
            check = [p1.eq(p2) for p1, p2 in zip(sp, op)]
            if False not in check:
                return True
        return False

    def periodic(self, curve, sign=-1):
        if self.slaves is None:
            self.slaves = {curve: sign}
        else:
            self.slaves[curve] = sign


class Line(Curve):
    def __init__(self, start, end, groups=[], **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        assert start.ne(end)
        self.__start = start
        self.__end = end
        self.add_to_groups(groups)
        Geometry.__init__(self, [self], **kwargs)

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def points(self):
        return [self.start, self.end]

    @property
    def coors(self):
        return np.array([self.start.coors, self.end.coors])

    @property
    def length(self):
        return np.linalg.norm(self.start.coors-self.end.coors)

    @property
    def _lines(self):
        return [self]

    def poly(self, res=None):
        if res is None:
            res = 2
        return tools.multi_linspace(self.start.coors, self.end.coors, num=res)


class Spline(Curve):
    def __init__(self, points, groups=[], **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        if len(points) == 2:
            assert points[0].ne(points[1])
        self.__points = points  # List of points
        self.add_to_groups(groups)
        Geometry.__init__(self, [self], **kwargs)

    @property
    def start(self):
        return self.__points[0]

    @property
    def end(self):
        return self.__points[-1]

    @property
    def points(self):
        return self.__points

    @property
    def coors(self):
        coors = []
        for p in self.points:
            coors.append(p.coors)
        return np.array(coors)

    @property
    def is_closed(self):
        c = False
        if self.start.eq(self.end):
            c = True
        return c

    @property
    def _lines(self):
        p = self.points
        return [Line(p[i], p[i+1]) for i in range(len(p)-1)]

    def poly(self, res=None):
        if res is None:
            res = len(self.points)
        N = np.linspace(0, 1, res)
        x, y, z = self.coors.T
        ic = self.is_closed
        # interpolate
        x = tools.GmshSpline(x, closed=ic).eval(N)
        y = tools.GmshSpline(y, closed=ic).eval(N)
        z = tools.GmshSpline(z, closed=ic).eval(N)
        return np.array([x, y, z]).T

    # def length(self):  #AND SO ON...


class CircularArc(Curve):
    def __init__(self, start, center, end, groups=[], **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        assert start.ne(center)
        assert start.ne(end)
        assert center.ne(end)
        radius1 = center.distance(start)
        radius2 = center.distance(end)
        chord = start.distance(end)
        assert abs(radius1 - radius2) <= self.tol  # cocircular?
        assert radius1 - chord/2. >= self.tol  # half circle?
        self.__start = start
        self.__center = center
        self.__end = end
#        self.__midpoint = self.__get_midpoint()
        self.add_to_groups(groups)
        Geometry.__init__(self, [self], **kwargs)

    @property
    def start(self):
        return self.__start

    @property
    def center(self):
        return self.__center

    @property
    def end(self):
        return self.__end

    @property
    def midpoint(self):
        return self.__get_midpoint()

    @property
    def plane(self):
        return self.__get_plane()

    @property
    def points(self):
        return [self.start, self.center, self.end]

    @property
    def radius(self):
        return self.center.distance(self.start)

    @property
    def chord(self):
        return self.start.distance(self.end)

    @property
    def angle(self):
        return 2 * np.arcsin((self.chord/2.)/self.radius)

    @property
    def length(self):
        return self.angle*self.radius

    @property
    def _lines(self):
        midpoint = self.midpoint
        return [Line(self.start, midpoint), Line(midpoint, self.end)]

    def poly(self, res=None):
        if res is None:
            return np.array([self.start.coors, self.midpoint.coors,
                             self.end.coors])
        c = self.center.coors
        r = self.radius
        a = self.angle
        u, v = self.plane[:-1]
        ai = np.linspace(0, a, res)
        pcoors = r*np.einsum('n, i -> ni', np.cos(ai), u) +\
            r*np.einsum('n, i -> ni', np.sin(ai), v) + c
        return pcoors

    def __get_plane(self):
        c = self.center.coors
        sc = self.start.coors - c
        ec = self.end.coors - c
        u = sc/np.linalg.norm(sc)
        n = np.cross(sc, ec)
        n = n/np.linalg.norm(n)
        v = np.cross(n, u)
        return u, v, n

    def __get_midpoint(self):
        c = self.center.coors
        r = self.radius
        a = self.angle
        u, v = self.plane[:-1]
        mcoors = r*np.cos(a/2.)*u + r*np.sin(a/2.)*v + c
        return Point(mcoors)


class EllipticalArc(Curve):
    def __init__(self, start, center, major, end, groups=[], **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        self.__start = start
        self.__center = center
        self.__major = major
        self.__end = end
        assert center.ne(major)
        assert tools.coplanar(self.coors, self.tol)
        assert not tools.colinear([start.coors, center.coors, end.coors],
                                  self.tol)
        self.radiuses  # raises ValueError is radiuses cannot be calcukated
        self.add_to_groups(groups)
        Geometry.__init__(self, [self], **kwargs)

    @property
    def start(self):
        return self.__start

    @property
    def center(self):
        return self.__center

    @property
    def major(self):
        return self.__major

    @property
    def end(self):
        return self.__end

    @property
    def midpoint(self):
        return self.__get_midpoint()

    @property
    def points(self):
        return [self.start, self.center, self.major, self.end]

    @property
    def start_radius(self):
        return self.center.distance(self.start)

    @property
    def end_radius(self):
        return self.center.distance(self.end)

    @property
    def chord(self):
        return self.start.distance(self.end)

    @property
    def plane(self):
        return self.__get_plane()

    @property
    def start_polar_angle(self):
        v1 = self.major.coors - self.center.coors  # self.__get_plane()[0]
        v2 = self.start.coors - self.center.coors
        return tools.signed_angle(v1, v2)

    @property
    def end_polar_angle(self):
#        v1 = self.major.coors - self.center.coors  # self.__get_plane()[0]
#        v2 = self.end.coors - self.center.coors
#        return tools.signed_angle(v1, v2)
        return self.start_polar_angle + self.polar_angle

    @property
    def polar_angle(self):
        v1 = self.start.coors - self.center.coors
        v2 = self.end.coors - self.center.coors
        return tools.signed_angle(v1, v2)

    @property
    def start_parametric_angle(self):
        return self.__get_parametric_angle(self.start_polar_angle)

    @property
    def end_parametric_angle(self):
        return self.__get_parametric_angle(self.end_polar_angle)

    @property
    def parametric_angle(self):
        return self.end_parametric_angle - self.start_parametric_angle

    @property
    def eccentricity(self):
        A, B = self.radiuses
        a = max(A, B)
        b = min(A, B)
        return np.sqrt(a**2 - b**2)/a

    @property
    def length(self):
        a = max(self.radiuses)
        t1 = self.start_parametric_angle
        t2 = self.end_parametric_angle
        m = self.eccentricity**2
        from scipy.special import ellipeinc  # second kind
        l1 = a*ellipeinc(t1, m)
        l2 = a*ellipeinc(t2, m)
        return l2 - l1

    @property
    def radiuses(self):
        r_1 = self.start_radius
        r_2 = self.end_radius
        t_1 = self.start_polar_angle
        t_2 = self.end_polar_angle
        sqrt = np.sqrt
        sin = np.sin
        cos = np.cos
        # M = np.array([[np.cos(sa), np.sin(sa)], [np.cos(ea), np.sin(ea)]])
        # A, B = np.einsum('ij, j -> i', np.linalg.inv(M), [sr, er])
        usa = r_1**2*r_2**2*(-cos(2*t_1) + cos(2*t_2)) / \
            (r_1**2*sin(t_1)**2 - r_2**2*sin(t_2)**2)
        usb = r_1**2*r_2**2*(cos(2*t_1) - cos(2*t_2)) / \
            (r_1**2*cos(t_1)**2 - r_2**2*cos(t_2)**2)
        if usa < self.tol or usb < self.tol:
            raise ValueError(
                "Wrong ellipse definition. Radiuses cannot be calculated."
                )
        A = sqrt(2)*sqrt(usa)/2.
        B = sqrt(2)*sqrt(usb)/2.
        return A, B

    @property
    def _lines(self):
        midpoint = self.midpoint
        return [Line(self.start, midpoint), Line(midpoint, self.end)]

    def __get_plane(self):
        c = self.center.coors
        mc = self.major.coors - c
        ec = self.end.coors - c
        u = mc/np.linalg.norm(mc)
        n = np.cross(u, ec)
        if np.linalg.norm(n) == 0.:
            ec = self.start.coors - c
            n = np.cross(u, ec)
        if tools.signed_angle(u, ec) < 0.:  # make xy ccw
            n = -n
        n = n/np.linalg.norm(n)
        v = np.cross(n, u)
        return u, v, n  # u - major axis, v - minor axis

    def __get_parametric_angle(self, theta):
        A, B = self.radiuses
        n = int(theta // (np.pi/2.))
        if n % 2 == 0:
            frac = A/B  # we are in first or third quarter
        else:
            frac = B/A  # we are in second or fourth quarter
        base = n * np.pi/2.
        return base + np.arctan(frac * np.tan(theta-base))

    def __get_midpoint(self):
        c = self.center.coors
        A, B = self.radiuses
        # is this really midpoint ??
        a = (self.start_parametric_angle + self.end_parametric_angle)/2.
        u, v = self.plane[:-1]
        mcoors = A*np.cos(a)*u + B*np.sin(a)*v + c
        return Point(mcoors)

    def poly(self, res=None):
        if res is None:
            return np.array([self.start.coors, self.midpoint.coors,
                             self.end.coors])
        c = self.center.coors
        A, B = self.radiuses
        t1 = self.start_parametric_angle
        t2 = self.end_parametric_angle
        u, v = self.plane[:-1]
        ai = np.linspace(t1, t2, res)
        pcoors = A*np.einsum('n, i -> ni', np.cos(ai), u) +\
            B*np.einsum('n, i -> ni', np.sin(ai), v) + c
        return pcoors

    def eq(self, other):
        if type(self) == type(other):
            sp = self.start, self.midpoint, self.end
            op = other.start, other.midpoint, other.end
            if False not in [p1.eq(p2) for p1, p2 in zip(sp, op)]:
                return True
        return False

    def is_reversed(self, other):
        if type(self) == type(other):
            sp = self.start, self.midpoint, self.end
            op = other.end, other.midpoint, other.start
            if False not in [p1.eq(p2) for p1, p2 in zip(sp, op)]:
                return True
        return False


class Surface(Geometry, Primitive):
    pass


class PlaneSurface(Surface):
    def __init__(self, curves, groups=[], holes=[], orientation=1, **kwargs):
        if 'tol' in kwargs:
            self.tol = kwargs['tol']
        self.__graph, self.__curves, self.__corient = self.__arrange(curves)
        self.__holes = []
        self.add_holes(holes)
        if not tools.coplanar(self.coors, tol=self.tol):
            raise ValueError("Coordinates of points are not coplanar")
        self.add_to_groups(groups)
        self.orientation = orientation  # see __setattr__
        Geometry.__init__(self, [self], **kwargs)
        # TODO: what about covering lines?

    @property
    def curves(self):
        curves = [c for c in self.__curves]  # new list
        for h in self.holes:
            curves += h.curves  # recursive
        return curves

    @property
    def corient(self):
        corient = [o for o in self.__corient]  # new list
        for h in self.holes:
            corient += h.corient  # recursive, negative orients not work
        return corient

    @property
    def loops(self):
        loops = [(self.__curves, self.__corient)]
        loops += sum([h.loops for h in self.holes], [])  # recursive
        return loops

    @property
    def graph(self):
        return self.__graph

    @property
    def holes(self):
        return self.__holes

    @property
    def points(self):  # in current orientation order, no repetitions
        points = []
        for c, o in zip(self.curves, self.corient):
            if o == 1:
                pts = c.points
            else:
                pts = c.points[::-1]
            for p in pts:
                if p not in points:
                    points += [p]
        return points

#    @property
#    def coors(self):
#        coors = []
#        for p in self.points:
#            coors.append(p.coors)
#        return np.array(coors)
#
#    @property
#    def center(self):
#        return self.coors.mean(axis=0)

    def __arrange(self, curves):
        # Create graph
        g = nx.Graph()
        uvd = []
        for c in curves:
            for p in c._lines:
                uvd += [(p.start, p.end, {'curve': c})]
        g.add_edges_from(uvd)
        # Recreate graph with cycles only
        cycles = nx.cycle_basis(g)
        g = g.subgraph(sum(cycles, []))
        # Check if proper graph
        if len(cycles) == 0:
            raise ValueError('No line loops found')
        if len(cycles) > 1:
            degree = g.degree()
            if hasattr(degree, 'items'):  # in networkx-2.0 degree is not
                degree = degree.items()   # a dict any more ...
            for n, deg in degree:
                if deg > 2:
                    raise ValueError("To many lines in point: %s" % n)
        # Make some efforts to get predictible order of curves
        for u, v, d in uvd:
            if u in g:
                root = u
                after_root = v
                break
        cycle = nx.cycle_basis(g, root=root)[0][::-1]  # only one cycle exists
        #if cycle[-1] == after_root:
        if cycle[1] != after_root:
            cycle = [cycle[0]] + cycle[1:][::-1]  #
        # The above can be replaces by simple:
        #   cycle = nx.cycle_basis(g)[0][::-1]
        # but then we will get curves starting from random curve  (SO WHAT?)
        # Now get list of curves and orientations
        circuit = cycle + [cycle[0]]
        curves = []
        corient = []
        for i in range(len(cycle)):
            u = circuit[i]
            v = circuit[i+1]
            c = g[u][v]['curve']
            if c not in curves:  # This 'if' is for circle hack
                curves += [c]
                if c.start == u:  # This is always true for closed spline!
                    corient += [1]
                else:
                    corient += [-1]
        return g, curves, corient

    def __coplanar_curves(self):
        # coors computed twice here
        rank = np.linalg.matrix_rank(self.coors - self.center, tol=self.tol)
        if rank == 2:
            return True
        return False

    def __get_orientation(self):
        poly = self.poly()
        pcenter = poly[:-1].mean(axis=0) + 10*self.tol  # shift a bit to
                                                        # avoid perfect symm.
        vectors = poly - pcenter
        lengths = np.sqrt((vectors**2).sum(1))
        slengths = lengths[0:-1] * lengths[1:]
        dots = (vectors[0:-1] * vectors[1:]).sum(1)
        cross = np.cross(vectors[0:-1], vectors[1:])
        angles = np.arccos((dots/slengths).round(15))
        signs = np.sign(cross.sum(1))  # cross.sum(1): dot product with [1,1,1]
        if (angles*signs).sum() < 0:  # is possible = 0 here? no, if no symm.
            return -1  # clockwise
        return 1  # counter-clockwise

    def __setattr__(self, name, value):
        if name == 'orientation':
            if not hasattr(self, 'orientation'):
                current_orientation = self.__get_orientation()
            else:
                current_orientation = self.orientation

            if value not in [1, 'ccw', 'counterclockwise',
                             -1, 'cw', 'clockwise']:
                raise AttributeError('Wrong orientation name')

            curves = self.__curves
            corient = self.__corient
            c1 = value in [1, 'ccw', 'counterclockwise'] and \
                current_orientation in [-1, 'cw', 'clockwise']
            c2 = value in [-1, 'cw', 'clockwise'] and \
                current_orientation in [1, 'ccw', 'counterclockwise']
            if c1 or c2:
                self.__curves = [curves[0]] + curves[1:][::-1]
                self.__corient = [corient[0]] + corient[1:][::-1]
                self.__corient = [-o for o in self.__corient]
            for c, o in zip(self.__curves, self.__corient):
                c.orientation = o   # This can make also
                                    # unwanted changes!
        Geometry.__setattr__(self, name, value)

    def poly(self, res=None):  # repeated point at start and end
        pcoors = []
        #only exterior boundary
        for c, o in zip(self.__curves, self.__corient):
            poly = c.poly(res)
            if o == -1:
                poly = poly[::-1]
            pcoors += poly[:-1].tolist()
        if Point(pcoors[0]).ne(Point(pcoors[-1])):
            pcoors = np.asarray(pcoors + [pcoors[0]])  # close polygon
        return pcoors

    def poly_center(self, res=None):
        poly = self.poly(res=res)
        return poly.mean(0)

    def poly_bbox(self, res=None):
        poly = self.poly(res=res)
        mini = poly[poly.argmin(axis=0)]
        maxi = poly[poly.argmax(axis=0)]
        return mini, maxi

    def add_hole(self, hole, validate=False, m=1.0, res=50):
        ss = self
        os = hole
        add_hole = True
        if validate:
            ost = os.copy()
            ost.resize(m)
            if ss.contains(ost):
                for ssh in ss.holes:
                    if not ost.disjoint(ssh, res) or \
                       not ssh.disjoint(ost, res):
                        add_hole = False
                        break
            else:
                add_hole = False
        if add_hole:
            ss.__holes = ss.__holes + [os]
            return True
        return False

    def add_holes(self, holes, **kwargs):
        for i, h in enumerate(holes):
            success = self.add_hole(h, **kwargs)
            if not success:
                raise ValueError('Hole %i cannot be added' % i)

    def remove_holes(self, holes):
        for h in holes:
            idx = self.__holes.index(h)
            del self.__holes[idx]

    def contains(self, other, res=50):
        polygon = self.poly(res)
        points = other.poly(res)
        test = tools.contains(polygon, points)
        return test

    def disjoint(self, other, res=50):
        polygon = self.poly(res)
        points = other.poly(res)
        test = tools.disjoint(polygon, points)
        return test


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
