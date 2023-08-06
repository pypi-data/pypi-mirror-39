# -*- coding: utf-8 -*-
import pytest
from fempy.geometry import gmsh_io


# if __name__ == "__main__":
class Test_Dump_and_Preview(object):
    def test_2D_model_preview(self):
        from fempy.geometry import Rectangle
        from fempy.models.elastic import PlaneStrain

        # 2D
        d = Rectangle(elsize=0.025).gmsh.domain(order=1)
        m = PlaneStrain(d)
        m.ev(20000, 0.3)
        # gravity
        m.rho[:] = 2.
        m.gravity[:] = [0., -9.81]
        # pressures
        m.qi['right'] = [-10, 0.]
        m.p['left'] = -10.
        # dirichlet bcs
        m.u['top', 1] = -0.0005
        m.bcs['top', 1] = True
        m.bcs['bottom'] = True

        m.solve()
        # m.preview()
        data, nfields = gmsh_io.prepare_model_data(m, 'all')
        gmsh_io._preview(*data + ('-parse_and_exit',))  # no display

    def test_3D_model_preview(self):
        pytest.importorskip("pygmsh")
        from fempy.models.elastic import LinearElastic
        # 3D
        from fempy.geometry import Gmsh
        from pygmsh.built_in import Geometry
        pg = Geometry()
        pg.add_box(0, 0.3, 0, 0.1, 0, 0.1, 0.0125)
        g = Gmsh(pg, entities={2: {19: 'right',
                                   20: 'top',
                                   21: 'front',
                                   22: 'back',
                                   23: 'bottom',
                                   24: 'left'}})
        d = g.domain(order=1)
        m = LinearElastic(d)
        m.ev(20000, 0.3)
        # gravity
        m.rho[:] = 2.
        m.gravity[:] = [0., 0., -9.81]
        # pressures
        m.qi['right'] = [-10, 0., 0.]
        m.p['left'] = -10.
        # dirichlet bcs
        m.u['top', 1] = -0.0005
        m.bcs['top', 1] = True
        m.bcs['bottom'] = True

        m.solve()
        data, nfields = gmsh_io.prepare_model_data(m, 'all')
        gmsh_io._preview(*data + ('-parse_and_exit',))  # no display
        # m.preview_dump('test.msh', 'all', ascii=True)


if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file