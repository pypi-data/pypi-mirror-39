# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:31:10 2013

@author: mwojc
"""

import numpy as np
import subprocess
import tempfile
import os

gext = ['.brep', '.brp',
        '.iges', '.igs',
        '.step', '.stp']

mext = ['.mesh']  # Medit files


class Gmsh(object):
    __eltypes = {1: (1, 'line2'),
                 2: (2, 'tria3'),
                 3: (2, 'quad4'),
                 4: (3, 'tetr4'),
                 5: (3, 'hexa8'),
                 6: (3, 'pris6'),
                 7: (3, 'pyra5'),
                 8: (1, 'line3'),
                 9: (2, 'tria6'),
                 10: (2, 'quad9'),
                 11: (3, 'tetr10'),
                 12: (3, 'hexa27'),
                 13: (3, 'pris18'),
                 14: (3, 'pyra14'),
                 15: (0, 'point'),
                 16: (2, 'quad8')}
    __meshio_eltypes = {
                'vertex':       15,
                'line':          1,
                'triangle':      2,
                'quad':          3,
                'tetra':         4,
                'hexahedron':    5,
                'wedge':         6,
                'pyramid':       7,
                'line3':         8,
                'triangle6':     9,
                'quad9':        10,
                'tetra10':      11,
                'hexahedron27': 12,
                'prism18':      13,
                'pyramid14':    14,
                'line4':        26,
                'quad16':       36,
                }
    __dims = {0: 'point', 1: 'curve', 2: 'surface', 3: 'volume'}

    def __init__(self, geometry, groups=None, entities=None,
                 custom=os.linesep, verbose=True):
        self.__groups = {}
        self.groups = {} if groups is None else groups
        self.entities = {} if entities is None else entities
        self.custom = custom
#        if geometry is None:  # create temporary geo file
#            geometry = self.__write_tempfile('', suffix='.geo')
        if isinstance(geometry, str):  # filename or .geo code
            try:
                open(os.path.realpath(geometry), 'r')
            except IOError:  # .geo code is assumed
                geometry = self.__write_tempfile(geometry, suffix='.geo')
            geometry = os.path.realpath(geometry)
            name, ext = os.path.splitext(geometry)
            if ext in ['.geo', '.msh']:
                pass
            elif ext in gext:  # create temporary geo file
                txt = 'Merge "%s";' % geometry
                geometry = self.__write_tempfile(txt, suffix='.geo')
            elif ext in mext:  # Convert meshes to msh
                sb = subprocess
                try:
                    output = sb.check_output(['gmsh', '-3', geometry],
                                             stderr=sb.STDOUT)
                except sb.CalledProcessError as err:
                    # if verbose:
                        # print err.output
                    raise Exception("Unknown mesh type: %s" % ext)
                geometry = name + '.msh'
            else:
                raise ValueError("Unknown geometry type: %s" % ext)
#            except IOError:
#                pass
#        elif isinstance(geometry, (tuple, list)):  # .geo and .msh files
#            pass
#        else:  # Geometry or Pygmsh objects
#            from fempy.geometry import Geometry as FempyGeometry
#            geometries = (FempyGeometry,)
#            try:
#                from pygmsh.built_in import Geometry as PygmshGeometry
#                geometries = geometries + (PygmshGeometry, )
#                # geometries.append(PygmshGeometry)
#            except:
#                pass
#            if not isinstance(geometry, geometries):
#                raise ValueError("Unknown geometry type: %s" % geometry)
        self.geometry = geometry
        self.verbose = verbose
        self.options = GmshOptions()
        self.options.factory = None  # or 'built-in' or 'opencascade'
        self.options_append = True
        self.custom_append = True

    @property
    def gmsh(self):
        return self

    def add_custom_line(self, line):
        line = str(line).strip()
        if not line.endswith(';'):
            line = line + ';'
        if not line.endswith(os.linesep):
            line = line + os.linesep
        self.custom += line

    def domain(self, order=None, etype=None, verbose=False):
        # Set options
        if order:
            if order in [1, 2]:
                self.options.Mesh.ElementOrder = order
            else:
                raise ValueError('Not supported order: %s' % order)
        self.verbose = verbose
        # Create fempy domain
        coors, conecs, etypes, egroups = self.__parse_msh()
        from fempy.domain.domain import Domain, tools
        from fempy.domain.index import EIndex
        dim = max(conecs.keys())
        etype_user = etype
        etype = list(set(etypes[dim]))
        if len(etype) > 1:
            raise TypeError("Mixed element types not supported: %s" % etype)
        else:
            etype = etype[0]
        # Enforce user element type if given
        etype = etype_user if etype_user is not None else etype
        #
        conec = np.asarray(conecs[dim], dtype=int)
        conec = conec.reshape(conec.shape[-2:])  # for _parse_msh, _parse_msh_meshio compat
        lst = tools.unique_rows(conec, sort=True, strict=False)
        lst = np.nonzero(lst)[0]
        eidx = EIndex(conec, lst, coors)
#        # RENUMBER NODES - seems to not help...
#        dom = Domain(coors, conec, etype)
#        segments = dom.segments
#        segments = dom.eidx.nidx.g.lst[segments]
#        v = np.ones(len(segments), dtype=int)
#        from scipy import sparse
#        M = sparse.coo_matrix((v, segments.T), dtype=int).tocsr()
#        perm = sparse.csgraph.reverse_cuthill_mckee(M, symmetric_mode=True)
##        import pylab
##        M = M[perm]
##        M = M[:, perm]
##        pylab.spy(M, markersize=2)
#        coors = coors[perm]
#        iperm = np.zeros(len(perm), dtype=int)
#        iperm[perm] = np.arange(len(perm), dtype=int)
#        conec = iperm[conec]
#        for i in range(dim-1, -1, -1):
#            conecs[i] = iperm[np.asarray(conecs[i], dtype=np.int)]
#        # END RENUMBERING NODES
        dom = Domain(coors, eidx, etype)  # , egroups[dim])
        for key, gpos in egroups[dim].items():
            dom.egroups.set_group_by_conec(key, conec[gpos], glob=True)
        faces = dom.faces
        for i in range(dim-1, -1, -1):
            if i in egroups:
                for key, gpos in egroups[i].items():
                    fconec = np.asarray(conecs[i], dtype=np.int)
                    fconec = fconec.reshape(fconec.shape[-2:])[gpos] # compat
                    faces.egroups.set_group_by_conec(key, fconec, glob=True)
            faces = faces.faces
        dom.geometry = self.geometry
        return dom

    @property
    def geo(self):
        self.__groups.clear()
        g = self.geometry
        if isinstance(g, str):  # possibly .geo file
            name, ext = os.path.splitext(g)
            if ext == '.geo':
                string = open(g, 'r').read()
            else:  # msh file
                return ''
        elif isinstance(g, (tuple, list)):  # .geo and .msh file
            string = open(g[0], 'r').read()
        elif hasattr(g, 'get_code'):
            # Pygmsh only currently
            string = g.get_code()
        else:
            # Geometry object is assumed
            string = ''
            string += self.__points(g.points)
            string += self.__curves(g.points, g.curves)
            string += self.__surfaces(g.curves, g.surfaces)
            string += self.__physical_points(g.points)
            string += self.__physical_curves(g.curves)
            string += self.__physical_surfaces(g.surfaces)

        if self.custom_append:
            string += self.custom

        if self.options_append:
            string += self.options.options

        return string

    @property
    def msh(self):
        g = self.geometry
        if isinstance(g, str):  # possibly .msh file
            name, ext = os.path.splitext(g)
            if ext == '.msh':
                return open(g, 'r').read()
            else:
                pass  # assumed the string is a .geo file (read later)
        elif isinstance(g, (tuple, list)):  # .geo and .msh file
            return open(g[1], 'r').read()
        else:
            pass  # Geometry object is assumed

        gfn = self.__write_tempfile(self.geo)
        mfn = gfn+'.msh'
        try:
            output = subprocess.check_output(['gmsh', '-3', gfn],
                                             stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
#            if self.verbose:
#                print err.output
                #print err.returncode
            raise Exception('Mesh cannot be generated because of errors.')
#        if self.verbose:
#            print output
        mfn_file = open(mfn, 'r')
        m = mfn_file.read()
        mfn_file.close()
        os.remove(gfn)
        os.remove(mfn)
        return m

    def save(self, fname):
        import os
        name, ext = os.path.splitext(fname)
        if ext == '.geo':
            f = open(fname, 'w')
            f.write(self.geo)
            f.close()
        elif ext == '.msh':
            f = open(fname, 'w')
            f.write(self.msh)
            f.close()
        else:
            fg = open(fname+'.geo', 'w')
            fm = open(fname+'.msh', 'w')
            fg.write(self.geo)
            fm.write(self.msh)
            fg.close()
            fm.close()

    def preview(self, default='geomsh'):
        if default == 'geomsh':
            mfn = self.__write_tempfile(self.msh)
            gfn = self.__write_tempfile(self.geo)
            out = subprocess.call(['gmsh', gfn, mfn], stderr=subprocess.STDOUT)
            os.remove(mfn)
            os.remove(gfn)
        elif default == 'geo':
            gfn = self.__write_tempfile(self.geo)
            out = subprocess.call(['gmsh', gfn], stderr=subprocess.STDOUT)
            os.remove(gfn)
        elif default == 'msh':
            mfn = self.__write_tempfile(self.msh)
            out = subprocess.call(['gmsh', mfn], stderr=subprocess.STDOUT)
            os.remove(mfn)
        else:
            out = None
        return out

    def __write_tempfile(self, txt, suffix=''):
        f = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
        f.write(txt)
        name = f.name
        f.close()
        return name

    def __parse_msh(self):
        try:
            return self._parse_msh_meshio()
        except ImportError:
            pass
        # Read file
        msh = self.msh.split('\n')
        msh.reverse()
        line = msh.pop()
        while(line != '$Nodes'):        # Read until we find the nodes
            line = msh.pop()
        msh.pop()                       # Skip next line (number of nodes)
        coors = []
        line = msh.pop()
        while(line != '$EndNodes'):     # Read nodes
            coors += [list(map(float, line.split()[1:]))]
            line = msh.pop()
        while(line != '$Elements'):     # Read until we find elements
            line = msh.pop()
        msh.pop()                       # Skip next line (number of elements)
        elinfo = []
        line = msh.pop()
        while(line != '$EndElements'):  # Read elements
            elinfo += [list(map(int, line.split()[1:]))]
            line = msh.pop()
        # End read file
        # Coordinates - remove unnecessary dimensions (3D --> 2D mostly)
        from fempy.geometry import tools
        coors = tools.remove_dimensions(coors)
        # Parse elements

        def parse_line(el):
            dim, etype = self.__eltypes[el.pop(0)]
            ntags = el.pop(0)
            group = el.pop(0)
            entity = el.pop(0)
            for j in range(ntags-2):
                el.pop(0)  # skip other tags
            con = np.asarray(el) - 1
            return dim, etype, ntags, group, entity, con

        conecs = {}
        etypes = {}
        egroups = {}
        for i in range(len(elinfo)):
            el = elinfo.pop(0)
            dim, etype, ntags, group, entity, con = parse_line(el)
            if dim not in conecs:
                conecs[dim] = []
            if dim not in etypes:
                etypes[dim] = []
            if dim not in egroups:
                egroups[dim] = {}
            #####
            pi = len(conecs[dim])
            if pi == 0:
                conecs[dim].append(con)
                etypes[dim].append(etype)
            else:  # pi > 0
                pcon = conecs[dim][-1]
                if not np.array_equiv(pcon, con):  # if repeated elem
                    conecs[dim].append(con)
                    etypes[dim].append(etype)
                else:
                    pi -= 1
            # Get physical group
            try:
                group = self.__groups[dim][group-1]
            except:
                try:
                    group = self.groups[dim][group]
                except:
                    group = 'gmsh_physical_%s_%s' % (self.__dims[dim], group)
            # Add physical group
            try:
                egroups[dim][group].append(pi)
            except:
                egroups[dim][group] = [pi]
            # Get and add gmsh entity group
            try:
                entity = self.entities[dim][entity]
            except:
                entity = 'gmsh_%s_%s' % (self.__dims[dim], entity)
            try:
                if egroups[dim][entity][-1] != pi:
                    egroups[dim][entity].append(pi)
            except:
                egroups[dim][entity] = [pi]

        return coors, conecs, etypes, egroups

    def _parse_msh_meshio(self):
        from fempy.geometry import gmsh_io
        msh = self.msh
        mfn = self.__write_tempfile(msh, suffix='.msh')
        points, cells, point_data, cell_data, field_data = gmsh_io.read(mfn)
        os.remove(mfn)
        # Coordinates - remove unnecessary dimensions (3D --> 2D mostly)
        from fempy.geometry import tools
        coors = tools.remove_dimensions(points)
        conecs = {}
        etypes = {}
        egroups = {}
        for k, v in cells.items():
            n = self.__meshio_eltypes[k]
            dim, etype = self.__eltypes[n]
            if dim not in conecs:
                conecs[dim] = []
            if dim not in etypes:
                etypes[dim] = []
            if dim not in egroups:
                egroups[dim] = {}
            conecs[dim].append(v)
            etypes[dim].append(etype)
            # Now geometrical groups
            gdata = cell_data[k]['geometrical']
            entities = np.unique(gdata)
            for en in entities:
                try:
                    entity = self.entities[dim][en]
                except:
                    entity = 'gmsh_%s_%s' % (self.__dims[dim], en)
                egroups[dim][entity] = np.nonzero(gdata == en)[0]
            # Now physical groups
            pdata = cell_data[k]['physical']
            if np.allclose(pdata, 0):
                continue  # do not add 0 physical group
            groups = np.unique(pdata)
            for gn in groups:
                try:
                    group = self.__groups[dim][gn - 1]  # -1 necessary here!
                except:
                    try:
                        group = self.groups[dim][gn]
                    except:
                        group = 'gmsh_physical_%s_%s' % (self.__dims[dim], gn)
                egroups[dim][group] = np.nonzero(pdata == gn)[0]
        return coors, conecs, etypes, egroups

    def __points(self, points):
        string = ''
        for i, point in enumerate(points):
            coors = point.coors.tolist().__str__()[1:-1]
            # if not hasattr(point, 'elsize'):
            if point.elsize is None:
                string += 'Point(%i) = {%s};\n' % (i+1, coors)
            else:
                elsize = point.elsize * point.elsize_factor
                #if hasattr(point, 'elsize_factor'):
                #    elsize = elsize * point.elsize_factor
                string += 'Point(%i) = {%s, %s};\n' % (i+1, coors, elsize)
        return string

    def __physical_points(self, points):
        groups = []
        towrite = {}
        for i, point in enumerate(points):
            for group in point.groups:
                if group not in groups:
                    groups += [group]
                    ip = len(groups)
                    towrite[ip] = [i+1]
                else:
                    ip = groups.index(group) + 1
                    towrite[ip] += [i+1]
        self.__groups[0] = groups  # Save groups
        string = ''
        for ip in sorted(towrite.keys()):
            pts = str(towrite[ip])[1:-1]
            string += 'Physical Point(%i) = {%s};\n' % (ip, pts)
        return string

    def __curves(self, points, curves):
        string = ''
        periodic = ''
        for i, curve in enumerate(curves):
            cname = curve.__class__.__name__
            if cname == 'Line':
                start = points.index(curve.start) + 1
                end = points.index(curve.end) + 1
                string += 'Line(%i) = {%i, %i};\n' % (i+1, start, end)
            elif cname == 'CircularArc':
                start = points.index(curve.start) + 1
                center = points.index(curve.center) + 1
                end = points.index(curve.end) + 1
                string += 'Circle(%i) = {%i, %i, %i};\n' \
                          % (i+1, start, center, end)
            elif cname == 'EllipticalArc':
                start = points.index(curve.start) + 1
                center = points.index(curve.center) + 1
                major = points.index(curve.major) + 1
                end = points.index(curve.end) + 1
                string += 'Ellipse(%i) = {%i, %i, %i, %i};\n' \
                          % (i+1, start, center, major, end)
            elif cname == 'Spline':
                pts = []
                for p in curve.points:
                    pts += [points.index(p) + 1]
                spts = str(pts)[1:-1]
                string += 'Spline(%i) = {%s};\n' \
                          % (i+1, spts)
            else:
                raise TypeError('Unknown curve type')
            # Handle periodic slaves
            if curve.slaves is not None:
                for slave, sign in curve.slaves.items():
                    n = (curves.index(slave)+1) # * np.sign(sign)
                    ni = (i+1) * np.sign(sign)
                    periodic += 'Periodic Line {%i} = {%i};\n' % (n, ni)
        return string + periodic

    def __physical_curves(self, curves):
        groups = []
        #curves = self.geometry.curves
        towrite = {}
        for i, curve in enumerate(curves):
            for group in curve.groups:
                if group not in groups:
                    groups += [group]
                    ip = len(groups)
                    towrite[ip] = [(i+1) * curve.orientation]
                else:
                    ip = groups.index(group) + 1
                    towrite[ip] += [(i+1) * curve.orientation]
        string = ''
        self.__groups[1] = groups  # Save groups
        for ip in sorted(towrite.keys()):
            crv = str(towrite[ip])[1:-1]
            string += 'Physical Line(%i) = {%s};\n' % (ip, crv)
        return string

    def __surfaces(self, curves, surfaces):
        curve_loops = []
        lstring = ''
        sstring = ''
        for i, surface in enumerate(surfaces):
            # Line loops
            llst = []
            for loop in surface.loops:
                if loop not in curve_loops:
                    curve_loops += [loop]
                    icl = len(curve_loops)
                    clst = [(curves.index(c)+1)*o for c, o in zip(*loop)]
                    cstr = str(clst)[1:-1]
                    lstring += 'Line Loop(%i) = {%s};\n' % (icl, cstr)
                else:
                    icl = curve_loops.index(loop) + 1
                llst += [icl]
            # Surfaces
            lstr = str(llst)[1:-1]
            if surface.__class__.__name__ == 'PlaneSurface':
                sstring += 'Plane Surface(%i) = {%s};\n' % (i+1, lstr)
            else:
                raise TypeError('Unknown surface type')
        return lstring + sstring

    def __physical_surfaces(self, surfaces):
        groups = []
        towrite = {}
        for i, surface in enumerate(surfaces):
            for group in surface.groups:
                if group not in groups:
                    groups += [group]
                    ip = len(groups)
                    towrite[ip] = [i+1]
                else:
                    ip = groups.index(group) + 1
                    towrite[ip] += [i+1]
        string = ''
        self.__groups[2] = groups  # Save groups
        for ip in sorted(towrite.keys()):
            srf = str(towrite[ip])[1:-1]
            string += 'Physical Surface(%i) = {%s};\n' % (ip, srf)
        return string


class GmshOptions(object):
    """
    Container for Gmsh options
    """
    # General options
    class __General(object):
        # write General options here
        pass
    General = __General()

    # Print options
    class __Print(object):
        # write Print options here
        pass
    Print = __Print()

    # Geometry options
    class __Geometry(object):
        # write Geometry options here
        pass

        class __Color(object):
            # write Geometry.Color options here
            pass
        Color = __Color()
    Geometry = __Geometry()

    # Mesh options
    class __Mesh(object):
        # write Mesh options here
        #
        # Mesh coloring (0=by element type, 1=by elementary entity,
        # 2=by physical entity, 3=by partition)
        ColorCarousel = 2
        # Display faces of surface mesh?
        SurfaceFaces = 1
        # Use vesion 2 of msh file format
        MshFileVersion = 2

        class __Color(object):
            # write Mesh.Color options here
            pass
        Color = __Color()
    Mesh = __Mesh()

    # Solver options
    class __Solver(object):
        # write Solver options here
        pass
    Solver = __Solver()

    # PostProcessing options
    class __PostProcessing(object):
        # write PostPtocessing options here
        #
        # Delay (in seconds) between frames in automatic animation mode
        AnimationDelay = 0.25
    PostProcessing = __PostProcessing()

    # View options
    class __View(object):
        pass
    View = __View()

    @property
    def options(self):
        string = '\n// OPTIONS\n'
        for group in ['General', 'Print', 'Geometry', 'Mesh',
                      'Solver', 'PostProcessing', 'View']:
            string += self.__write_options(group)
        # Apply built-in factory
        if self.factory is not None:
            string += 'SetFactory("%s");\n' % self.factory
        return string

    def __get_options(self, obj):
        options = [attr for attr in dir(obj)
                   if not callable(getattr(obj, attr))
                   and not attr.startswith("__")]
        return options

    def __write_options(self, group):
        string = ''
        opts = getattr(self, group)
        for opt in self.__get_options(opts):
            if opt == 'Color':
                colors = getattr(opts, 'Color')
                for cname in self.__get_options(colors):
                    cval = getattr(colors, cname)
                    if cval is not None:
                        cval = '{' + str(cval)[1:-1] + '}'
                        string += '%s.Color.%s = %s;\n' % (group, cname, cval)
            else:
                val = getattr(opts, opt)
                if val is not None:
                    if isinstance(val, str):
                        val = '"' + str(val) + '"'
                    val = str(val)
                    string += '%s.%s = %s;\n' % (group, opt, val)
        return string


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
