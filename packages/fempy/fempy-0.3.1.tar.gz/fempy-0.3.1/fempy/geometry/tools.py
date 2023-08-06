# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:08:22 2014

@author: mwojc
"""
import numpy as np


def norm(vec):
    return np.sqrt(np.einsum('...i,...i', vec, vec))


def coors3D(coors):
    if isinstance(coors, (int, float)):
        coors = [coors]
    coors = np.array(coors, dtype=float)
    shape = coors.shape
    if len(shape) == 1:
        s0 = shape[0]
        if s0 == 3:
            coors3D = coors.copy()
        elif s0 < 3:
            coors3D = np.zeros((3,))
            coors3D[:s0] = coors
        else:
            raise ValueError('Wrong coordinates shape %s' % coors.shape)
    elif len(shape) == 2:
        s0 = shape[0]
        s1 = shape[1]
        if s1 == 3:
            coors3D = coors.copy()
        elif s1 < 3:
            coors3D = np.zeros((s0, 3))
            coors3D[:, :s1] = coors
        else:
            raise ValueError('Wrong coordinates shape %s' % coors.shape)
    else:
        raise ValueError('Wrong coordinates shape %s' % coors.shape)
    return coors3D


def remove_dimensions(coors, tol=1e-7):
    coors = np.asarray(coors)
    assert len(coors.shape) == 2
    rows, cols = coors.shape
    assert cols <= 3
    cid = []
    for c in range(cols):
        if not (abs(coors[:, c] - coors[0, c]) < tol).all():
            cid.append(c)
    if cid == []:
        raise ValueError("Single point in coors")
    return coors[:, cid]


def add_dimensions(coors):
    coors = np.asarray(coors)
    rows, cols = coors.shape
    empty = np.zeros((rows, 3-cols))
    return np.append(coors, empty, axis=1)


def reduce_coors(coors, dmin=1e-7):
    from scipy.spatial.distance import pdist, squareform
    dist = squareform(pdist(coors))
    i, j = np.nonzero((dist < dmin))  # too close coors indices
    i = i[i > j]  # indices to remove
    mask = np.ones(len(coors), dtype=bool)
    mask[i] = False
    coors = coors[mask]
    return coors


def rank(coors, tol=1e-7):
    coors = coors3D(coors)
    center = coors.mean(axis=0)
    return np.linalg.matrix_rank(coors - center, tol=tol)


def coplanar(coors, tol=1e-7):
    if rank(coors, tol) == 2:
        return True
    return False


def colinear(coors, tol=1e-7):
    if rank(coors, tol) == 1:
        return True
    return False


#def contains_points(polygon, points, tol=1e-7):
#    ### polygon should be counterclockwise as matplotlib tests works better
#    polygon = coors3D(polygon)
#    points = coors3D(points)
#    if coplanar(np.vstack((polygon, points))):
#        from matplotlib.path import Path
#        for plane in [(0, 1), (0, 2), (1, 2)]:
#            poly = polygon[:, plane]
#            pts = points[:, plane]
#            if not colinear(poly, tol):
#                p = Path(poly).contains_points(pts)
#                return p
#    raise ValueError('Polygon and points are not coplanar')


def contains(polygon, points, tol=1e-7):
    # polygon should be counterclockwise as matplotlib tests works better
    polygon = coors3D(polygon)
    points = coors3D(points)
    if coplanar(np.vstack((polygon, points))):
        from shapely.geometry import Polygon, MultiPoint
        for plane in [(0, 1), (0, 2), (1, 2)]:
            poly = polygon[:, plane]
            pts = points[:, plane]
            if not colinear(poly, tol):
                p = Polygon(poly).contains(MultiPoint(pts))
                return p
    raise ValueError('Polygon and points are not coplanar')


def disjoint(polygon, points, tol=1e-7):
    # polygon should be counterclockwise as matplotlib tests works better
    polygon = coors3D(polygon)
    points = coors3D(points)
    if coplanar(np.vstack((polygon, points))):
        from shapely.geometry import Polygon, MultiPoint
        for plane in [(0, 1), (0, 2), (1, 2)]:
            poly = polygon[:, plane]
            pts = points[:, plane]
            if not colinear(poly, tol):
                p = Polygon(poly).disjoint(MultiPoint(pts))
                return p
    raise ValueError('Polygon and points are not coplanar')


def multi_linspace(starts, stops, **kwargs):
    assert len(starts) == len(stops)  # starts and stops should be equal in len
    space = []
    for st, sp in zip(starts, stops):
        space += [np.linspace(st, sp, **kwargs)]
    return np.asarray(space).T


def signed_angle(v1, v2):
    dot = np.dot(v1, v2)  # (v1 * v2).sum()
    slen = np.linalg.norm(v1) * np.linalg.norm(v2)
    if slen == 0:
        raise ValueError("Zero length vector.")
    angle = np.arccos(round(dot/slen, 15))
    cross = np.cross(v1, v2)
    sign = np.sign(cross.sum())  # cross.sum(1): dot product with [1,1,1]
    if not sign:
        sign = np.sign(dot)
    return angle*sign


def rotation_matrix(axis, angle):
    axis = coors3D(axis)
    ux, uy, uz = axis/np.linalg.norm(axis)
    c = np.cos(angle)  # angle in radians
    s = np.sin(angle)
    R = np.zeros((3, 3))
    R[0, 0] = c + (ux**2)*(1-c)
    R[0, 1] = ux*uy*(1-c) - uz*s
    R[0, 2] = ux*uz*(1-c) + uy*s
    R[1, 0] = uy*ux*(1-c) + uz*s
    R[1, 1] = c + (uy**2)*(1-c)
    R[1, 2] = uy*uz*(1-c) - ux*s
    R[2, 0] = uz*ux*(1-c) - uy*s
    R[2, 1] = uz*uy*(1-c) + ux*s
    R[2, 2] = c + (uz**2)*(1-c)
    return R


def uniquify(seq, idfun=None):
    # uses hash instesd of cmp so user defined __eq__ will not work
    # order preserving
    if idfun is None:
        def idfun(x):
            return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


#def uniquify(seq):
     # uses __eq__ but this is O(n^2), slow on large lists
     # order preserving
#    useq = []
#    for i in seq:
#        if i not in useq:
#            useq.append(i)
#    return useq


def tmpfname(ext=''):
    from tempfile import NamedTemporaryFile
    f = NamedTemporaryFile()
    fname = f.name + ext
    f.close()
    return fname


def saveobj(obj, fname, ext=''):
    from fempy.compat import pickle
    if ext:
        if not ext.startswith('.') and not fname.endswith('.'):
            ext = '.' + ext
        if not fname.endswith(ext):
            fname = fname + ext
    f = open(fname, 'wb')
    pickle.dump(obj, f)
    f.close()
    return


def loadobj(fname, ext=''):
    from fempy.compat import pickle
    if ext:
        if not ext.startswith('.') and not fname.endswith('.'):
            ext = '.' + ext
        if not fname.endswith(ext):
            fname = fname + ext
    f = open(fname, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj


class CubicSpline(object):
    def eval(self, xn, diff=0):
        n = self.n
        x = self.x
        coeff = self.coeff
        ni = len(xn)
        ci = np.zeros(ni, dtype=int)  # np.zeros((ni, 4))
        xi = np.zeros(ni)
        for i in range(n-1):
            cdn = (x[i] <= xn) * (xn <= x[i+1])
            ci = np.where(cdn, i, ci)
            xi = np.where(cdn, 1-(x[i+1]-xn)/(x[i+1]-x[i]), xi)
        cn = coeff[ci]
        a, b, c, d = cn.T
        if diff == 0:
            return a*xi**3 + b*xi**2 + c*xi + d
        elif diff == 1:
            return 3*a*xi**2 + 2*b*xi + c
        elif diff == 2:
            return 6*a*xi + 2*b
        elif diff == 3:
            return 6*a
        else:
            raise ValueError("Wrong derivative order: %i" % (diff, ))


class NaturalSpline(CubicSpline):
    def __init__(self, y, closed=False):
        """
        Cubic spline defined for equidistant points in range (0,1).
        This is natural cubic spline, i.e. the first derivatives are
        calculated from continuous curvature condition. Curvature equal 0
        is assumed at boundaries if spline is not closed.

        See: http://mathworld.wolfram.com/CubicSpline.html
        """
        n = len(y)
        x = np.linspace(0, 1, n)
        y = np.array(y)
        dy = np.diff(y)

        # Derivatives
        Y = np.zeros(len(x))
        if not closed:
            Y[0] = y[1] - y[0]
            Y[1:-1] = y[2:] - y[:-2]
            Y[-1] = y[-1] - y[-2]
            Y = 3*Y
            # tridiagonal matrix
            A = np.diag(4*np.ones(n)) + \
                np.diag(np.ones(n-1), -1) + \
                np.diag(np.ones(n-1), 1)
            A[0, 0] = 2
            A[-1, -1] = 2
            D = np.linalg.solve(A, Y)
        else:
            Y[0] = y[1] - y[-2]
            Y[1:-1] = y[2:] - y[:-2]
            Y[-1] = y[1] - y[-2]
            Y = 3*Y
            # tridiagonal matrix
            A = np.diag(4*np.ones(n)) + \
                np.diag(np.ones(n-1), -1) + \
                np.diag(np.ones(n-1), 1)
            A[0, -2] = 1
            A[-1, 1] = 1
            D = np.linalg.solve(A, Y)

        # Coeficients
        a = -2*dy + D[:-1] + D[1:]
        b = 3*dy - 2*D[:-1] - D[1:]
        c = D[:-1]
        d = y[:-1]

        self.n = n
        self.x = x
        self.y = y
        self.coeff = np.vstack((a, b, c, d)).T


class GmshSpline(CubicSpline):
    def __init__(self, y, closed=False):
        """
        Cubic spline defined for equidistant points in range (0,1).
        This is *not* natural cubic spline, i.e. the first derivatives are
        not calculated from continuous curvature condition. Instead they
        are calculated directly from control points.
        """
        n = len(y)
        x = np.linspace(0, 1, n)
        y = np.array(y)
        dy = np.diff(y)

        # Derivatives
        D = np.zeros(n)
        D[1:-1] = (dy[:-1] + dy[1:])/2.
        if closed:
            D[0] = D[-1] = (dy[0] + dy[-1])/2.
        else:
            D[0] = dy[0]
            D[-1] = dy[-1]

        # Coeficients
        a = -2*dy + D[:-1] + D[1:]
        b = 3*dy - 2*D[:-1] - D[1:]
        c = D[:-1]
        d = y[:-1]

        self.n = n
        self.x = x
        self.y = y
        self.coeff = np.vstack((a, b, c, d)).T


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
