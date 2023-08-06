# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 12:35:53 2014

@author: mwojc
"""
from fempy.compat import builtins
import numpy as np
from fempy.fields.nfields import nScalar, nVector
from fempy.fields.gfields import gScalar, gVector, gTensor, gMatrix
from fempy.fields.algebra import normalize
from fempy.domain.elems import guess_etype
from fempy.domain.index import EIndex, EGroups, NGroups
import fempy.domain.tools as tools

# We will use cached property throughout domains
property = tools.cached_property


def Domain(coors, conec, etype=None, egroups=None, ngroups=None):
    """
    Factory of finite element method domains

    Arguments:
    coors   -   node coordinates, indices are node numbers, possibly more
                coordinates then needed (by conec) can be given
    conec   -   connectivity array from which nodes being used are determined,
                if this is an EIndex object than it is used directly (coors
                is ignored)
    etype   -   string with element name or element class/module
    egroups -   element groups dictionary (global)
    ngroups -   node groups dictionary (global)

    Returns:
    FEM domain, one of: Volume, Surface, Surface3D, Curve, Curve2D, Curve3D,
    Points
    """
    eidx = conec if isinstance(conec, EIndex) else EIndex(conec, nidx=coors)
    eidx.g.update(egroups)
    eidx.nidx.g.update(ngroups)
    etype = guess_etype(eidx.nidx.g.coors, eidx.g.conec, etype)
    dtype = guess_dtype(eidx.nidx.g.coors.shape[1], etype.ndime)
    return dtype(eidx, etype)


class BaseDomain(object):
    """
    Base FEM domain consisting in elements of the same type.
    """
    def __init__(self, eidx, etype=None):
        """
        Create FEM domain.

        eidx  - element index (EIndex object)
        etype - element type
        """
        if not isinstance(eidx, EIndex):  # assume eidx is coors and conec
            eidx = EIndex(eidx[1], nidx=eidx[0])
        self.eidx = eidx
        self.etype = guess_etype(eidx.nidx.g.coors, eidx.g.conec, etype)
        self.egroups = EGroups(self)
        self.ngroups = NGroups(self)
        self._faces = None
        self._boundary = None
        self.geometry = None

    @property
    def faces(self):
        if self._faces is None:
            self._faces = tools.create_faces(self)
        return self._faces

    @property
    def boundary(self):
        if self._boundary is None:
            f = self.faces
            if f is not None:
                self._boundary = f['boundary']
        return self._boundary

    @property
    def segments(self):
        if self.ndime == 0:
            return None
        elif self.ndime == 1:
            edges = self
        elif self.ndime == 2:
            edges = self.faces
        else:
            edges = self.faces.faces
        return edges.conec[:, edges.etype.segments].reshape(-1, 2)

    def __getitem__(self, key):
        self.faces  # creates boundary if possible and necessary
        subeidx = self.eidx.subindex(key)
        subdomain = self.__class__(subeidx, self.etype)
        # Handle faces
        # This cannot be as simple as tools.create_faces because also
        # for faces we want to have subdomian not the new faces domain
        if self.etype.btype is not None:
            # global conec for domain faces
            fconec0 = self.faces.eidx.conec_g
            # global conec for subdomain faces
            fconec1 = subdomain.eidx.conec_g[:, self.etype.faces]
            fconec1 = fconec1.reshape(-1, fconec1.shape[-1])
            # find which subdomain faces are in domain faces
            mask = tools.in2d(fconec0, fconec1)  # no sort!
            # be sure only one occurence of each face is taken
            mask2 = tools.unique_rows(fconec0[mask], strict=False)
            mask[mask] = mask2
            # create subindex
            subfidx = self.faces.eidx.subindex(mask)
            # now we will identify boundary elements
            bbool = tools.unique_rows(subfidx.conec, sort=True)
            # and we apply local boundary masks
            subfidx.set_local_mask('boundary', bbool)
            subfidx.set_local_mask('CUT', subfidx['boundary^BOUNDARY'])
            # TODO this below hack is needed to recover proper node indices
            subeidx.nidx.set_local_mask('boundary', subfidx.conec[bbool])
            subeidx.nidx.set_local_mask('CUT', subfidx.conec[subfidx['CUT']])
            # create and assign subfaces
            subfaces = self.faces.__class__(subfidx, self.faces.etype)
            subdomain._faces = subfaces
        return subdomain

    @property
    def nlist(self):
        return self.eidx.nidx.g.pos[self.eidx.nidx.lst]

    @property
    def ndime(self):
        return self.eidx.nidx.g.coors.shape[1]

    @property
    def nnode(self):
        return self.eidx.nidx.n

    @property
    def nedim(self):
        return self.etype.ndime

    @property
    def nenod(self):
        return self.etype.nnode

    @property
    def nelem(self):
        return self.eidx.n

    @property
    def ngauss(self):
        return self.etype.ngauss

    @property
    def coors(self):
        coors = self.eidx.nidx.g.coors
        idx = self.eidx.nidx.msk
        return nVector(self, coors[idx])

    @property
    def conec(self):
        return self.eidx.nidx.pos[self.eidx.conec_g]

    @property
    def ndeg(self):
        ndeg = np.bincount(self.conec.ravel())
        return nScalar(self, ndeg)

    @property
    def ecoors(self):
        coors = self.eidx.nidx.g.coors
        conec = self.eidx.conec_g
        return coors[conec]

    @property
    def ecoors_mean(self):
        ecoors = self.ecoors
        return np.mean(ecoors, axis=1)

    @property
    def gcoors(self):
        gcoors = np.einsum('eni, gn -> egi', self.ecoors, self.etype.gshp)
        return gVector(self, gcoors)

    @property
    def gjac(self):
        gjac = np.einsum('eni, gnj -> egij', self.ecoors, self.etype.gshpd)
        return gTensor(self, gjac)

    @property
    def uvw(self):
        return normalize(self.gjac, axis=-2)

    @property
    def gdet(self):
        detj = np.linalg.det(self.gjac)
        if np.any(detj <= 0.):
            raise ValueError("Determinant of jacobian <= 0")
        return gScalar(self, detj)

    @property
    def gvol(self):
        gvol = np.einsum('eg, g -> eg', self.gdet, self.etype.gweights)
        return gScalar(self, gvol)

    @property
    def evol(self):
        evol = self.gvol.sum(1)
        return evol

    @property
    def vol(self):
        return self.gvol.sum()

#    @property
#    def nvol(self):
#        from fempy.fields.operators import lform
#        nvol = nScalar(self)
#        nvol[:] = lform(gScalar(self, 1.))  # lform currently returns array
#        return nvol
#
#    @property
#    def nvolu(self):
#        nvol = np.zeros((self.nelem, self.etype.nnode))
#        nvol[:] = self.evol[:, None]/self.etype.nnode
#        F = nScalar(self)
#        np.add.at(F, self.eidx.conec_a, nvol)
#        return F
#
#    @property
#    def bvol(self):
#        from fempy.fields.operators import onboundary
#        return onboundary(self.nvol)
#
#    @property
#    def bgvol(self):
#        from fempy.fields.operators import ongauss
#        return ongauss(self.bvol)

    @property
    def gijac(self):
        gijac = np.linalg.inv(self.gjac)
        return gTensor(self, gijac)

    @property
    def egn(self):
        e = np.ones(len(self.conec))
        gshp = np.einsum('e, gn -> egn', e, self.etype.gshp)
        return gshp

    @property
    def egnk(self):
        gijac = self.gijac
        if self.etype.ndime < self.ndime:  # for structural elements
            d = self.etype.ndime
            gijac = gijac[..., :d, :]
        gshpd = np.einsum('egik, gni -> egnk', gijac, self.etype.gshpd)
        return gshpd

    def invalidate_caches(self):
        tools.invalidate_caches(self)
        # invalidate reccurently at boundary...
        if self.faces is not None:
            self.faces.invalidate_caches()
        if self.boundary is not None:
            self.boundary.invalidate_caches()

    def update(self, disp=None):
        if disp is not None:
            self.eidx.nidx.g.coors[self.eidx.nidx.lst] += disp
        self.invalidate_caches()

    def preview(self):
        from fempy.geometry import gmsh_io
        gmsh_io.preview_domain(self)

    # ### Axisymmetry specific code
    # TODO: the below attributes should not be visible in 3D
    @builtins.property
    def axis(self):
        if not hasattr(self, '_axis'):
            self._axis = None
        return self._axis

    @axis.setter
    def axis(self, ax):
        if self.ndime > 2 and ax is not None:
            raise AttributeError("Can't set 'axis' attribute for 3D domains")
        # If ax is None (back to plane surface)
        if ax is None:
            self._axis = None
            self.ngroups.pop('axis', None)  # removes 'axis' group if exists
            self.invalidate_caches()
            return
        # Otherwise (if 'auto' set minimum x coordinate).
        x = self.coors[..., 0]
        if ax in ['auto', 'minx']:
            ax = x.min()
        assert isinstance(ax, (np.float, np.int)), "Axis must be a number" \
                                                   " (x coordinate)"
        assert (x >= ax).all(), "All x coordinates must be greater than axis"
        self._axis = float(ax)
        # when axis is changed other things change
        self.invalidate_caches()
        # set the same axis to the faces and boundary
        if self.faces is not None:
            self.faces.axis = ax
        if self.boundary is not None:
            self.boundary.axis = ax
        # Set 'axis' ngroup
        rn = self.radiusn  # always > 0
        self.ngroups['axis'] = rn < np.spacing(rn)*2

    @property
    def radius(self):
        if self.axis is None:
            return None
        radius = self.gcoors[..., 0] - self.axis
        return gScalar(self, radius)
    radiusg = radius

    @property
    def radiusn(self):
        if self.axis is None:
            return None
        radiusn = self.coors[..., 0] - self.axis
        return nScalar(self, radiusn)


class Volume(BaseDomain):
    """
    3D volume
    """


class Surface(BaseDomain):
    """
    2D surface
    """
    def __getitem__(self, key):
        subdomain = BaseDomain.__getitem__(self, key)
        subdomain.thickness[:] = self.thickness[key]
        subdomain.axis = self.axis
        # TODO: how to properly inherit data in subdomain? Question relevant
        # also for Curve and Points
        return subdomain

    @property
    def _gvol(self):
        return super(Surface, self).gvol

    @property
    def thickness(self):
        # TODO: we should keep the boundary thickness always compatibile
        # superdomain concept is necessary here!
        if self.axis is not None:
            return 2*np.pi * self.radius
        if not hasattr(self, '_thickness'):
            self._thickness = gScalar(self, 1.)
        return self._thickness

    @builtins.property
    def gvol(self):
        return self._gvol * self.thickness


class Curve(BaseDomain):
    """
    1D line
    """
    def __getitem__(self, key):
        subdomain = BaseDomain.__getitem__(self, key)
        subdomain.cross[:] = self.cross[key]
        subdomain.axis = self.axis
        return subdomain

    @property
    def _gvol(self):
        return super(Curve, self).gvol

    @property
    def thickness(self):
        if self.axis is not None:
            return 2*np.pi * self.radius
        if not hasattr(self, '_thickness'):
            self._thickness = gScalar(self, 1.)
        return self._thickness

    @property
    def width(self):
        if not hasattr(self, '_width'):
            self._width = gScalar(self, 1.)
        return self._width

    @builtins.property
    def cross(self):
        return self.thickness * self.width

    @builtins.property
    def gvol(self):
        return self._gvol * self.cross


class Points(BaseDomain):
    """
    0D points (dummy elements)
    """
    def __getitem__(self, key):
        subdomain = BaseDomain.__getitem__(self, key)
        subdomain.gvol[:] = self.gvol[key]
        subdomain.axis = self.axis
        return subdomain

    @property
    def gvol(self):
        if self.axis is not None:
            return 2*np.pi * self.radius
        if not hasattr(self, '_gvol'):
            self._gvol = gScalar(self, 1.)
        return self._gvol


class Surface3D(Surface):
    """
    3D surface with tangents and normals
    """
    @property
    def faces(self):
        faces = super(Surface3D, self).faces
        if faces is not None:
            t = np.einsum('eni, bgnj -> ebgij',
                          self.ecoors, self.etype.bgshpd)
            n = normalize(np.cross(t[..., 0], t[..., 1]))
            n = n.reshape(-1, *n.shape[2:])
            # Agree rows, might be necessary if domain is a subdomain
            #
            # TODO This is a mess which should not be here. Currently this
            # agreement is necessary only here so maybe this is not big deal
            # however this might arise also in other places too. The general
            # problem is that domain faces elements can be given in any
            # order when subdomain is created (faces are also subdomains),
            # but here we need a specific order related to domain conec.
            # It seems there's no obvious way to assure globally that
            # domain.faces.eidx.conec_g is always coincident with
            # domain.eidx.conec_g[:, self.etype.faces]
            # Maybe didx, fidx should be computed when subdomain is created?
            fconecd = self.eidx.conec_g[:, self.etype.faces]
            fconecd = fconecd.reshape(-1, fconecd.shape[-1])
            uidx = tools.unique_rows(fconecd, strict=False)
            fconecd = fconecd[uidx]
            n = n[uidx]
            fconecf = faces.eidx.conec_g
            # ## is this really necesary ??
            didx, fidx = tools.agree_rows(fconecd, fconecf)
            # ##
            # Assign orientarion to faces
            # faces.orientation[:] = n.reshape(faces.orientation.shape)
            faces.orientation[fidx] = n.reshape(faces.orientation.shape)[didx]
        return faces

    @property
    def gjac(self):
        t = np.einsum('eni, gnj -> egij', self.ecoors, self.etype.gshpd)
        n = normalize(np.cross(t[..., 0], t[..., 1]))
        gjac = gTensor(self)
        gjac[..., :2] = t
        gjac[..., 2] = n
        return gjac

    @property
    def ttn(self):
        uvw = self.uvw
        t1 = gVector(self, uvw[..., 0])
        t2 = gVector(self, uvw[..., 1])
        n = gVector(self, uvw[..., 2])
        return t1, t2, n

    @property
    def tn(self):
        uvw = self.uvw
        t = gMatrix(self, uvw[..., 0:2])
        n = gVector(self, uvw[..., 2])
        return t, n

    @property
    def tangent(self):
        return gMatrix(self, self.uvw[..., 0:2])

    @property
    def tangent1(self):
        return gVector(self, self.uvw[..., 0])

    @property
    def tangent2(self):
        return gVector(self, self.uvw[..., 1])

    @property
    def normal(self):
        return gVector(self, self.uvw[..., 2])


class Curve2D(Curve):
    """
    2D curve with tangent and normal
    """
    rot90 = np.array([[0., -1.], [1., 0.]])  # counterclockwise (inward normal)
    # rot90 = np.array([[0., 1.], [-1., 0.]])  # clockwise (outward normal)

    @property
    def gjac(self):
        t = np.einsum('eni, gnj -> egi', self.ecoors, self.etype.gshpd)
        n = normalize(np.einsum('egi, ki -> egk', t, self.rot90))
        gjac = gTensor(self)
        gjac[..., 0] = t  # if t will be normalized it will be a rotation m.
        gjac[..., 1] = n
        return gjac

    @property
    def tn(self):
        uvw = self.uvw
        t = gVector(self, uvw[..., 0])
        n = gVector(self, uvw[..., 1])
        return t, -n  # "-" for outward normal

    @property
    def tangent(self):
        return gVector(self, self.uvw[..., 0])

    @property
    def normal(self):
        return -gVector(self, self.uvw[..., 1])  # "-" for outward normal


class Curve3D(Curve):
    """
    3D curve with orientation tangent and normal
    """
    def __getitem__(self, key):
        subdomain = Curve.__getitem__(self, key)
        subdomain.orientation[:] = self.orientation[key]
        # TODO: make a special function to get data only # .getdata(key)
        return subdomain

    @property
    def orientation(self):
        if not hasattr(self, '_orientation'):
            self._orientation = gVector(self, np.random.rand(3))
        return self._orientation
    # orientation = np.random.rand(3)  # OK for circular cross sections

    @property
    def gjac(self):
        t = np.einsum('eni, gnj -> egi', self.ecoors, self.etype.gshpd)
        # Deal with orientation a bit
        o = np.asarray(self.orientation, float)
        if o.shape == (self.nelem, self.etype.ngauss, 3):
            pass
        elif o.shape == (self.etype.ngauss, 3):
            o = np.tile(o, (self.nelem, 1, 1))
        elif o.shape == (3,):
            o = np.tile(o, (self.nelem, self.etype.ngauss, 1))
        else:
            raise ValueError("Wrong 'orientation' shape: %s" % o.shape)
        n = normalize(np.cross(t, o))
        o = normalize(np.cross(t, -n))
        gjac = gTensor(self)
        gjac[..., 0] = t
        gjac[..., 1] = o
        gjac[..., 2] = n
        return gjac

    @property
    def ton(self):
        uvw = self.uvw
        t = gVector(self, uvw[..., 0])
        o = gVector(self, uvw[..., 1])
        n = gVector(self, uvw[..., 2])
        return t, o, n

    @property
    def tangent(self):
        return gVector(self, self.uvw[..., 0])

    @property
    def orient(self):
        return gVector(self, self.uvw[..., 1])

    @property
    def normal(self):
        return gVector(self, self.uvw[..., 2])


# Set faces types
Volume.btype = Surface3D
Surface3D.btype = Curve3D
Curve3D.btype = Points
Surface.btype = Curve2D
Curve2D.btype = Points
Curve.btype = Points
Points.btype = None


# Domain type guessing
def guess_dtype(ndime, edime):
    # Choose proper domain class and class for boundary
    if ndime == 3:
        if edime == 3:
            cls = Volume
        elif edime == 2:
            cls = Surface3D
        elif edime == 1:
            cls = Curve3D
        elif edime == 0:
            cls = Points
        else:
            raise ValueError("Cannot create %iD domain with %iD elements"
                             % (ndime, edime))
    elif ndime == 2:
        if edime == 2:
            cls = Surface
        elif edime == 1:
            cls = Curve2D
        elif edime == 0:
            cls = Points
        else:
            raise ValueError("Cannot create %iD domain with %iD elements"
                             % (ndime, edime))
    elif ndime == 1:
        if edime == 1:
            cls = Curve
        elif edime == 0:
            cls = Points
        else:
            raise ValueError("Cannot create %iD domain with %iD elements"
                             % (ndime, edime))
    else:
        raise ValueError("Sorry, %iD domains are not supported" % ndime)
    return cls


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
