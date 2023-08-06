# -*- coding: utf-8 -*-
#
'''
I/O for Gmsh's msh format, cf.
<http://geuz.org/gmsh/doc/texinfo/gmsh.html#File-formats>.

.. moduleauthor:: Nico Schlömer <nico.schloemer@gmail.com>


This module is copied form meshio project and adapted for fempy needs
Added: dumpig $NodeData, examples

'''
import logging
import struct
import collections
import numpy

num_nodes_per_cell = {
    'vertex': 1,
    'line': 2,
    'triangle': 3,
    'quad': 4,
    'tetra': 4,
    'hexahedron': 8,
    'wedge': 6,
    'pyramid': 5,
    #
    'line3': 3,
    'triangle6': 6,
    'quad9': 9,
    'tetra10': 10,
    'hexahedron27': 27,
    'prism18': 18,
    'pyramid14': 14,
    'line4': 4,
    'quad16': 16,
    }

# Translate meshio types to gmsh codes
# http://geuz.org/gmsh/doc/texinfo/gmsh.html#MSH-ASCII-file-format
_gmsh_to_meshio_type = {
        15: 'vertex',
        1: 'line',
        2: 'triangle',
        3: 'quad',
        4: 'tetra',
        5: 'hexahedron',
        6: 'wedge',
        7: 'pyramid',
        8: 'line3',
        9: 'triangle6',
        10: 'quad9',
        11: 'tetra10',
        12: 'hexahedron27',
        13: 'prism18',
        14: 'pyramid14',
        26: 'line4',
        36: 'quad16',
        }
_meshio_to_gmsh_type = {v: k for k, v in _gmsh_to_meshio_type.items()}

_fempy_to_meshio_type = {
        'point': 'vertex',
        'line2': 'line',
        'line3': 'line3',
        'tria3': 'triangle',
        'tria6': 'triangle6',
        'tetr4': 'tetra',
        'tetr10': 'tetra10'
        }
_meshio_to_fempy_type = {v: k for k, v in _fempy_to_meshio_type.items()}


def read(filename):
    '''Reads a Gmsh msh file.
    '''
    with open(filename, 'rb') as f:
        out = read_buffer(f)
    return out


def read_buffer(f):
    # The format is specified at
    # <http://geuz.org/gmsh/doc/texinfo/gmsh.html#MSH-ASCII-file-format>.

    # Initialize the data optional data fields
    points = []
    cells = {}
    field_data = {}
    cell_data = {}
    point_data = {}

    has_additional_tag_data = False
    is_ascii = None
    int_size = 4
    data_size = None
    while True:
        line = f.readline().decode('utf-8')
        if not line:
            # EOF
            break
        assert line[0] == '$'
        environ = line[1:].strip()
        if environ == 'MeshFormat':
            line = f.readline().decode('utf-8')
            # Split the line
            # 2.2 0 8
            # into its components.
            str_list = list(filter(None, line.split()))
            assert str_list[0][0] == '2', 'Need mesh format 2'
            assert str_list[1] in ['0', '1']
            is_ascii = str_list[1] == '0'
            data_size = int(str_list[2])
            if not is_ascii:
                # The next line is the integer 1 in bytes. Useful to check
                # endianness. Just assert that we get 1 here.
                one = f.read(int_size)
                assert struct.unpack('i', one)[0] == 1
                line = f.readline().decode('utf-8')
                assert line == '\n'
            line = f.readline().decode('utf-8')
            assert line.strip() == '$EndMeshFormat'
        # TODO PhysicalNames code does not work properly
        elif environ == 'PhysicalNames':
            line = f.readline().decode('utf-8')
            num_phys_names = int(line)
            for _ in range(num_phys_names):
                line = f.readline().decode('utf-8')
#                key = line.split(' ')[2].replace('"', '').replace('\n', '')
#                phys_group = int(line.split(' ')[1])
#                field_data[key] = phys_group
            line = f.readline().decode('utf-8')
            assert line.strip() == '$EndPhysicalNames'
        # ####
        elif environ == 'Nodes':
            # The first line is the number of nodes
            line = f.readline().decode('utf-8')
            num_nodes = int(line)
            if is_ascii:
                points = numpy.fromfile(
                    f, count=num_nodes*4, sep=' '
                    ).reshape((num_nodes, 4))
                # The first number is the index
                points = points[:, 1:]
            else:
                # binary
                num_bytes = num_nodes * (int_size + 3 * data_size)
                assert numpy.int32(0).nbytes == int_size
                assert numpy.float64(0.0).nbytes == data_size
                dtype = [('index', numpy.int32), ('x', numpy.float64, (3,))]
                data = numpy.fromstring(f.read(num_bytes), dtype=dtype)
                assert (data['index'] == range(1, num_nodes+1)).all()
                # vtk numpy support requires contiguous data
                points = numpy.ascontiguousarray(data['x'])
                line = f.readline().decode('utf-8')
                assert line == '\n'

            line = f.readline().decode('utf-8')
            assert line.strip() == '$EndNodes'
        elif environ == 'Elements':
#            assert environ == 'Elements', \
#                'Unknown environment \'{}\'.'.format(environ)
            # The first line is the number of elements
            line = f.readline().decode('utf-8')
            total_num_cells = int(line)
            if is_ascii:
                for _ in range(total_num_cells):
                    line = f.readline().decode('utf-8')
                    data = [int(k) for k in filter(None, line.split())]
                    t = _gmsh_to_meshio_type[data[1]]
                    num_nodes_per_elem = num_nodes_per_cell[t]

                    if t not in cells:
                        cells[t] = []
                    cells[t].append(data[-num_nodes_per_elem:])

                    # data[2] gives the number of tags. The gmsh manual
                    # <http://gmsh.info/doc/texinfo/gmsh.html#MSH-ASCII-file-format>
                    # says:
                    # >>>
                    # By default, the first tag is the number of the physical
                    # entity to which the element belongs; the second is the
                    # number of the elementary geometrical entity to which the
                    # element belongs; the third is the number of mesh
                    # partitions to which the element belongs, followed by the
                    # partition ids (negative partition ids indicate ghost
                    # cells). A zero tag is equivalent to no tag. Gmsh and most
                    # codes using the MSH 2 format require at least the first
                    # two tags (physical and elementary tags).
                    # <<<
                    num_tags = data[2]
                    if t not in cell_data:
                        cell_data[t] = []
                    cell_data[t].append(data[3:3+num_tags])

                # convert to numpy arrays
                for key in cells:
                    cells[key] = numpy.array(cells[key], dtype=int)
                for key in cell_data:
                    cell_data[key] = numpy.array(cell_data[key], dtype=int)
            else:
                # binary
                num_elems = 0
                while num_elems < total_num_cells:
                    # read element header
                    elem_type = struct.unpack('i', f.read(int_size))[0]
                    t = _gmsh_to_meshio_type[elem_type]
                    num_nodes_per_elem = num_nodes_per_cell[t]
                    num_elems0 = struct.unpack('i', f.read(int_size))[0]
                    num_tags = struct.unpack('i', f.read(int_size))[0]
                    # assert num_tags >= 2

                    # read element data
                    num_bytes = 4 * (
                        num_elems0 * (1 + num_tags + num_nodes_per_elem)
                        )
                    shape = \
                        (num_elems0, 1 + num_tags + num_nodes_per_elem)
                    b = f.read(num_bytes)
                    data = numpy.fromstring(
                        b, dtype=numpy.int32
                        ).reshape(shape)

                    if t not in cells:
                        cells[t] = []
                    cells[t].append(data[:, -num_nodes_per_elem:])

                    if t not in cell_data:
                        cell_data[t] = []
                    cell_data[t].append(data[:, 1:num_tags+1])

                    num_elems += num_elems0

                # collect cells
                for key in cells:
                    cells[key] = numpy.vstack(cells[key])

                # collect cell data
                for key in cell_data:
                    cell_data[key] = numpy.vstack(cell_data[key])

                line = f.readline().decode('utf-8')
                assert line == '\n'

            line = f.readline().decode('utf-8')
            assert line.strip() == '$EndElements'

            # Subtract one to account for the fact that python indices are
            # 0-based.
            for key in cells:
                cells[key] -= 1

            # restrict to the standard two data items
            output_cell_data = {}
            for key in cell_data:
                if cell_data[key].shape[1] > 2:
                    has_additional_tag_data = True
                output_cell_data[key] = {}
                if cell_data[key].shape[1] > 0:
                    output_cell_data[key]['physical'] = cell_data[key][:, 0]
                if cell_data[key].shape[1] > 1:
                    output_cell_data[key]['geometrical'] = cell_data[key][:, 1]
            cell_data = output_cell_data
        else:
            logging.warning(
                'Environment \'{}\' is not supported.'.format(environ)
                )
            while not line.startswith('$End'):  # might be slow but is safe
                line = f.readline().decode('utf-8')
#            break  # immediate bu not safe


    if has_additional_tag_data:
        logging.warning(
            'The file contains tag data that couldn\'t be processed.'
            )

    return points, cells, point_data, cell_data, field_data


def write(
        filename,
        points,
        cells,
        is_ascii=False,
        point_data=None,
        cell_data=None,
        field_data=None
        ):
    '''Writes msh files, cf.
    http://geuz.org/gmsh/doc/texinfo/gmsh.html#MSH-ASCII-file-format
    '''
    point_data = {} if point_data is None else point_data
    cell_data = {} if cell_data is None else cell_data
    field_data = {} if field_data is None else field_data

    if not is_ascii:
        for key in cells:
            if cells[key].dtype != numpy.int32:
#                logging.warning(
#                    'Binary Gmsh needs 32-bit integers. Converting.'
#                    )
                cells[key] = numpy.array(cells[key], dtype=numpy.int32)
    mode = 'wb'    
    if is_ascii:
        mode = 'w'

    with open(filename, mode) as fh:
        mode_idx = 0 if is_ascii else 1
        size_of_double = 8
        fh.write((
            '$MeshFormat\n2.2 {} {}\n'.format(mode_idx, size_of_double)
            ).encode('utf-8'))
        if not is_ascii:  # binary
            fh.write(struct.pack('i', 1))
            fh.write('\n'.encode('utf-8'))
        fh.write('$EndMeshFormat\n'.encode('utf-8'))

        # Write nodes
        fh.write('$Nodes\n'.encode('utf-8'))
        fh.write('{}\n'.format(len(points)).encode('utf-8'))
        if is_ascii:
            for k, x in enumerate(points):
                fh.write(
                    '{} {!r} {!r} {!r}\n'.format(k+1, x[0], x[1], x[2])
                    .encode('utf-8')
                    )
        else:
            dtype = [('index', numpy.int32), ('x', numpy.float64, (3,))]
            tmp = numpy.empty(len(points), dtype=dtype)
            tmp['index'] = 1 + numpy.arange(len(points))
            tmp['x'] = points
            fh.write(tmp.tostring())
            fh.write('\n'.encode('utf-8'))
        fh.write('$EndNodes\n'.encode('utf-8'))

        fh.write('$Elements\n'.encode('utf-8'))
        # count all cells
        total_num_cells = sum([data.shape[0] for _, data in cells.items()])
        fh.write('{}\n'.format(total_num_cells).encode('utf-8'))

        consecutive_index = 0
        cell_numbers = {}
        for cell_type, node_idcs in cells.items():
            cell_numbers[cell_type] = \
                numpy.arange(consecutive_index,
                             consecutive_index + len(node_idcs))
            # handle cell data
            if cell_type in cell_data and cell_data[cell_type]:
                datas = []
                for key in sorted(cell_data[cell_type].keys()):
                    if key == 'physical':
                        ph = cell_data[cell_type]['physical']
                        assert len(ph) == len(node_idcs)
                    else:
                        ph = numpy.ones(len(node_idcs), dtype=numpy.int32)
                    if key == 'geometrical':
                        geo = cell_data[cell_type]['geometrical']
                        assert len(geo) == len(node_idcs)
                    else:
                        geo = numpy.ones(len(node_idcs), dtype=numpy.int32)
                    if key not in ('physical', 'geometrical'):
                        dat = cell_data[cell_type][key]
                        if len(dat) == len(node_idcs):  # not sufficient?
                            datas += [dat]
                    # TODO assert that the data type is int
                fcd = numpy.column_stack([ph, geo] + datas)
            else:
                # no cell data
                fcd = numpy.empty([len(node_idcs), 0], dtype=numpy.int32)

            if is_ascii:
                form = '{} ' + str(_meshio_to_gmsh_type[cell_type]) \
                    + ' ' + str(fcd.shape[1]) \
                    + ' {} {}\n'
                for k, c in enumerate(node_idcs):
                    fh.write(
                        form.format(
                            consecutive_index + k + 1,
                            ' '.join([str(val) for val in fcd[k]]),
                            ' '.join([str(cc + 1) for cc in c])
                            ).encode('utf-8')
                        )
            else:
                # header
                fh.write(struct.pack('i', _meshio_to_gmsh_type[cell_type]))
                fh.write(struct.pack('i', node_idcs.shape[0]))
                fh.write(struct.pack('i', fcd.shape[1]))
                # actual data
                a = numpy.arange(
                    len(node_idcs), dtype=numpy.int32
                    )[:, numpy.newaxis]
                a += 1 + consecutive_index
                array = numpy.hstack([a, fcd, node_idcs + 1])
                fh.write(array.tostring())

            consecutive_index += len(node_idcs)
        if not is_ascii:
            fh.write('\n'.encode('utf-8'))
        fh.write('$EndElements\n'.encode('utf-8'))

        # Write point data
        num_nodes = len(points)
        for data_name, data in point_data.items():
            for i, di in enumerate(data):
                time, arr = di
                n = arr.shape[0]
                arr = arr.reshape(n, -1)
                f = arr.shape[1]
                assert n == num_nodes
                assert f in (1, 3, 9)
                fh.write('$NodeData\n'.encode('utf-8'))
                fh.write('{}\n'.format('1').encode('utf-8'))
                fh.write(('"'+data_name+'"\n').encode('utf-8'))
                fh.write('{}\n'.format('1').encode('utf-8'))
                fh.write('{}\n'.format(str(float(time))).encode('utf-8'))
                fh.write('{}\n'.format('3').encode('utf-8'))
                fh.write('{}\n'.format(str(i)).encode('utf-8'))
                fh.write('{}\n'.format(str(f)).encode('utf-8'))
                fh.write('{}\n'.format(str(n)).encode('utf-8'))
                if not is_ascii:
                    dtype = [('index', numpy.int32),
                             ('field', numpy.float64, (f,))]
                    tmp = numpy.empty(n, dtype=dtype)
                    tmp['index'] = 1 + numpy.arange(n)
                    tmp['field'] = arr
                    fh.write(tmp.tostring())
                    fh.write('\n'.encode('utf-8'))
                else:
                    form = '{} '+'{}\n'*f
                    for nidx in range(n):
                        nf = [nidx+1] + arr[nidx].tolist()
                        fh.write(form.format(*nf).encode('utf-8'))
                fh.write('$EndNodeData\n'.encode('utf-8'))

        # Write element data
        for cell_type_i, cell_data_i in cell_data.items():
            cell_numbers_i = cell_numbers[cell_type_i]
            num_cells = len(cell_numbers_i)
            for data_name, data in cell_data_i.items():
                for i, di in enumerate(data):
                    time, arr = di
                    n = arr.shape[0]
                    arr = arr.reshape(n, -1)
                    f = arr.shape[1]
                    assert n == num_cells
                    assert f in (1, 3, 9)
                    fh.write('$ElementData\n'.encode('utf-8'))
                    fh.write('{}\n'.format('1').encode('utf-8'))
                    fh.write(('"'+data_name+'"\n').encode('utf-8'))
                    fh.write('{}\n'.format('1').encode('utf-8'))
                    fh.write('{}\n'.format(str(float(time))).encode('utf-8'))
                    fh.write('{}\n'.format('3').encode('utf-8'))
                    fh.write('{}\n'.format(str(i)).encode('utf-8'))
                    fh.write('{}\n'.format(str(f)).encode('utf-8'))
                    fh.write('{}\n'.format(str(n)).encode('utf-8'))
                    if not is_ascii:
                        dtype = [('index', numpy.int32),
                                 ('field', numpy.float64, (f,))]
                        tmp = numpy.empty(n, dtype=dtype)
                        tmp['index'] = 1 + cell_numbers_i
                        tmp['field'] = arr
                        fh.write(tmp.tostring())
                        fh.write('\n'.encode('utf-8'))
                    else:
                        form = '{} '+'{}\n'*f
                        for ni, nidx in enumerate(cell_numbers_i):
                            nf = [nidx+1] + arr[ni].tolist()
                            fh.write(form.format(*nf).encode('utf-8'))
                    fh.write('$EndElementData\n'.encode('utf-8'))
    return


# Fempy previewing and dumping functions
from fempy.geometry import tools
import subprocess, os, inspect


def prepare_domain_data(d, add_normals=True):
    coors = tools.add_dimensions(d.coors)
    conec = d.conec
    etype = _fempy_to_meshio_type[d.etype.name]

    # Meshio data
    points = coors
    cells = {etype: conec}  # , betype: bconec}
    point_data = {}
    cell_data = {}
    data = (points, cells, point_data, cell_data)
    if hasattr(d, 'normal') and add_normals:
        data = prepare_field_data(d.normal, 'domain_normals',
                                  d, data)
    # Handle boundary  (use recurency here?)
    if d.boundary is not None:
        if d.boundary.nelem > 0:
            # PLEASE DO SOMETHING WITH THIS MESS
            lst = d.boundary.eidx.nidx.lst
            pos = d.eidx.nidx.pos[lst]
            bconec = pos[d.boundary.conec]
            # PLEASE
            betype = _fempy_to_meshio_type[d.boundary.etype.name]
            cells[betype] = bconec
            if hasattr(d.boundary, 'normal') and add_normals:
                data = prepare_field_data(d.boundary.normal,
                                          'boundary_normals',
                                          d.boundary, data)
    return data


def prepare_field_data(f, name, d=None, data=None, time=0.):
    assert hasattr(f, 'domain') or d is not None
    d = f.domain if d is None else d  # preferes d

    if not hasattr(f, 'domain'):
        if len(f) == d.nnode:  # nField is assumed
            from fempy.fields.nfields import nField
            f = nField(d, f)
        elif len(f) == d.nelem:  # gField is assumed
            from fempy.fields.gfields import gField
            f = gField(d, f)
        else:
            raise ValueError("Given array cannot be converted to proper field")

    if data is None:
        data = prepare_domain_data(d, add_normals=False)
    else:
        pass  # consistency should be checked?

    # Shape tests
    if f.pshape == (d.nnode,):              # nField
        if f.sshape == ():                  # nScalar
            pass
        elif f.sshape == (d.ndime,):        # nVector
            f = tools.add_dimensions(f)
        elif f.sshape == (d.ndime,)*2:      # nTensor
            if d.ndime < 3:
                fz = numpy.zeros(f.pshape + (3, 3))
                fz[..., :d.ndime, :d.ndime] = f
                f = fz
        else:
            raise "Field shape '%s' not supported" % str(f.sshape)
        if name not in data[2]:
            data[2][name] = [(time, f)]  # Create point data
        else:
            data[2][name] += [(time, f)]  # Append next time step
    elif f.pshape == (d.nelem, d.etype.ngauss):  # gField
        f1 = f.mean(1)  # Average from Gauss points, better ideas?
        if f.sshape == ():                       # gScalar
            pass
        elif f.sshape == (d.ndime,):             # gVector
            f1 = tools.add_dimensions(f1)
        elif f.sshape == (d.ndime,)*2:           # gTensor
            if d.ndime < 3:
                fz = numpy.zeros((d.nelem, 3, 3))
                fz[..., :d.ndime, :d.ndime] = f1
                f1 = fz
        else:
            raise TypeError("Field shape '%s' not supported" % str(f.sshape))
        etype = _fempy_to_meshio_type[d.etype.name]
        if etype not in data[3]:
            data[3][etype] = {name: [(time, f1)]}
        else:
            if name not in data[3][etype]:
                data[3][etype][name] = [(time, f1)]  # Update cell data
            else:
                data[3][etype][name] += [(time, f1)]  # Append next time step
    return data


#def prepare_time_data(m, name=None, data=None):
#    sol = m.sol
#    d = m.domain
#    nlhs = m.lhs.size
#    y = sol.y.T
#    t = sol.t
#    name = 'lhs' if name is None else name
#    for i in range(len(t)):
#        yi = y[i, :nlhs].reshape(m.lhs.shape)
#        data = prepare_field_data(yi, 'lhs', d, data, t[i])
#    return data


def prepare_model_data(m, what, data=None):
    d = m.domain
    b = d.boundary
    n = True if what in [None, 'all'] else False
    data = prepare_domain_data(d, add_normals=n) if data is None else data
    fields = _get_fields(m, what)
    for name, f in fields:
        if f.domain not in (d, b):  # Skip other domains or subdomains
            continue
        try:
            data = prepare_field_data(f, name, data=data)
        except:
            pass  # Skip silently not supported fields
    return data, len(fields)


def _get_times(m, time):
    if isinstance(time, numpy.ndarray):
        return time  # times have been just prepared
    if time is None:
        t = (m.time,)
    elif isinstance(time, float):
        t = (time,)
    elif isinstance(time, int):
        t = numpy.linspace(m.time0, m.time1, time)
    elif isinstance(time, collections.Iterable):
        if len(time) == 0:
            t = m._sol.t.copy()
        elif len(time) == 3:
            t = numpy.linspace(*time)
        else:
            raise ValueError("Provide empty tuple () or (t0, t1, n)")
    else:
        raise ValueError("Time specification not recognized.")
    return t


def prepare_time_model_data(m, what, time, data=None):
    if not hasattr(m, '_sol'):  # time solution is not available
        return prepare_model_data(m, what, data)
    d = m.domain
    b = d.boundary
    n = True if what in [None, 'all'] else False
    data = prepare_domain_data(d, add_normals=n) if data is None else data
    t0 = m.time  # record model time
    times = _get_times(m, time)
    for t in times:
        m.sol(t)
        fields = _get_fields(m, what)
        for name, f in fields:
            if f.domain not in (d, b):  # Skip other domains or subdomains
                continue
            try:
                data = prepare_field_data(f.copy(), name, data=data, time=t)
            except:
                pass  # Skip silently not supported fields
    m.sol(t0)  # recover initial model time
    return data, len(fields)


def _dump(fname, points, cells, point_data, cell_data, ascii=False):
    if len(points) == 0:
        raise ValueError("Sorry, no data to be processed. Empty domain?")
    write(fname, points, cells,
          point_data=point_data, cell_data=cell_data,
          is_ascii=ascii)


def _preview(points, cells, point_data, cell_data, *gmsh_opts):
    fname = tools.tmpfname('.msh')
    _dump(fname, points, cells, point_data, cell_data)
    out = subprocess.call(['gmsh', fname] + list(gmsh_opts),
                          stderr=subprocess.STDOUT)
    # subprocess.Popen(['gmsh', fname] + list(gmsh_opts), shell=False)
    os.remove(fname)  # remove to not clutter the system
    return out


def preview_domain(d):
    return _preview(*prepare_domain_data(d))


def dump_domain(fname, d, ascii=False):
    return _dump(fname, *(prepare_domain_data(d)+(ascii,)))


def preview_field(f, name=None, d=None):
    if name is None:
        name = f.__class__.__name__
    return _preview(*prepare_field_data(f, name, d))


def dump_field(fname, f, name=None, d=None, ascii=False):
    if name is None:
        name = f.__class__.__name__
    return _dump(fname, *(prepare_field_data(f, name, d)+(ascii,)))


def preview_fields(fields, names=None, d=None):
    data = None
    for i, f in enumerate(fields):
        if names is None:
            name = f.__class__.__name__
        else:
            name = names[i]
        data = prepare_field_data(f, name, d, data)
    return _preview(*data + ('-n',))


def dump_fields(fname, fields, names=None, d=None, ascii=False):
    data = None
    for i, f in enumerate(fields):
        if names is None:
            name = f.__class__.__name__
        else:
            name = names[i]
        data = prepare_field_data(f, name, d, data)
    return _dump(fname, *(data + (ascii,)))


#def preview_time_data(m, name=None):
#    return _preview(*prepare_time_data(m, name))
#
#
#def dump_time_data(fname, m, name=None, ascii=False):
#    return _dump(fname, *(prepare_time_data(m, name)+(ascii,)))


def _get_fields(model, what, blacklist=()):
    if what in [None, 'all']:
        boring = dir(type('dummy', (object,), {}))
        fields = [item
                  for item in inspect.getmembers(model)
                  if item[0] not in boring and
                  not inspect.ismethod(item[1]) and
                  hasattr(item[1], 'domain') and
                  item not in blacklist]
    elif isinstance(what, str) and what != 'all':
        what = [w.strip() for w in what.split(',')]
        fields = [(w, getattr(model, w)) for w in what]
    elif isinstance(what, collections.Iterable):
        fields = [(w, getattr(model, w)) for w in what]
    else:  # it is assumed that what is a field itself
        fields = [(None, what)]
    return fields


def preview_model(m, what='lhs', time=None):
    data, nfields = prepare_time_model_data(m, what, time)
    if nfields > 1:
        data += ('-n',)
    return _preview(*data)


def dump_model(fname, m, what='lhs', time=None, ascii=False):
    data, nfields = prepare_time_model_data(m, what, time)
    return _dump(fname, *(data + (ascii,)))


# Tests
if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
