# -*- coding: utf-8 -*-
import pytest
from fempy.geometry import *
import numpy as np


class TestPrimitivies:
    # Points
    A = Point([0, 0, 0], elsize=0.2, groups='A, corners')
    B = Point([1, 0, 0], elsize=0.1, groups=['B', 'corners'])
    C = Point([0, 1, 0], elsize=0.1, groups=['C', 'corners'])
    D = Point([0, -1e-8, 0], elsize=0.5, groups=['D', 'corners'])
    E = Point([2, 0, 0], elsize=0.5, groups=['E'])
    F = Point([1+np.sqrt(2), 0, 0], elsize=0.5, groups=['F'])
    G = Point([0.5, 0.5, 0], elsize=0.2, groups=['G', 'corners'])
    H = Point([0.25, 0.25, 0], elsize=0.2, groups=['H', 'corners'])
    I = Point([0, 0, 1e-6], groups=['I', 'corners'])  # out of plane
    J = Point([0, 0, 1], groups=['J', 'corners'])  # out of plane
    K = Point([0.0001, 0.9999, 0], groups=['K', 'corners'])
    L = Point([-2., 0, 0], groups=['L'])
    M = Point([0., -2., 0], groups=['M'])
    N = Point([0.5, 0.3, 0], groups=['N'])
    O = Point([0.5, 0.1, 0], groups=['O'])
    P = Point([0.5, -0.1, 0], groups=['P'])

#               C, ~K
#              o
#              |\
#              | \
#              |  \
#              |   o G
#              | H  \
#              |  o  \
#    o_________o______o______o___o
#    L         |A,D   B      E   F
#              |
#              |
#              o M

    # Lines
    AB = Line(A, B, groups=['AB', 'boundary'])
    BC = Line(B, C, groups=['BC', 'boundary'])
    CA = Line(C, A, groups=['CA', 'boundary'])

    BD = Line(B, D, groups=['BD', 'boundary'])
    DC = Line(D, C, groups=['DC', 'boundary'])
    CD = Line(C, D, groups=['CD', 'boundary'])
    AC = Line(A, C, groups=['AC', 'boundary'])
    CB = Line(C, B, groups=['CB', 'boundary'])
    AE = Line(A, E, groups=['AE', 'boundary'])
    BE = Line(B, E, groups=['BE', 'boundary'])
    CE = Line(C, E, groups=['CE', 'boundary'])
    CF = Line(C, F, groups=['CF', 'boundary'])
    CJ = Line(C, J, groups=['CJ'])
    JB = Line(J, B, groups=['JB'])
    AJ = Line(A, J, groups=['AJ'])
    AH = Line(A, H, groups=['AH'])
    HB = Line(H, B, groups=['HB'])
    AK = Line(A, K, groups=['AK'])
    KB = Line(K, B, groups=['KB'])
    IH = Line(I, H, groups=['IH'])
    IC = Line(I, C, groups=['IC'])
    AL = Line(A, L, groups=['AL'])
    LC = Line(L, C, groups=['LC'])

    # Splines
    ABCA = Spline([A, B, C, A], groups='closed, spline')
    ABCD = Spline([A, B, C, D], groups='closed, spline')
    ACBA = Spline([A, C, B, A], groups='closed, spline')
    ABC = Spline([A, B, C], groups='open, spline')
    ABEF = Spline([A, B, E, F], groups='open, spline')
    MFCLM = Spline([M, F, C, L, M], groups='boundary')
    ABGA = Spline([A, B, G, A], groups='hole')

    # Circular Arcs
    BAC = CircularArc(B, A, C, groups=['BAC'])
    BDC = CircularArc(B, D, C, groups=['BDC'])
    CAB = CircularArc(C, A, B, groups=['CAB'])
    CDB = CircularArc(C, D, B, groups=['CDB'])
    FBC = CircularArc(F, B, C, groups=['FBC'])
    BCJ = CircularArc(B, C, J, groups=['BCJ'])

    # Elliptical Arcs
    EAEC = EllipticalArc(E, A, E, C)
    EALC = EllipticalArc(E, A, L, C)
    CALE = EllipticalArc(C, A, L, E)
    CACE = EllipticalArc(C, A, C, E)
    ECEJ = EllipticalArc(E, C, E, J)
    EAFC = EllipticalArc(E, A, F, C)
    BALM = EllipticalArc(B, A, L, M)
    BAEM = EllipticalArc(B, A, E, M)
    BAEC = EllipticalArc(B, A, E, C)
    OAEM = EllipticalArc(O, A, E, M)
    OALM = EllipticalArc(O, A, E, M)
    OACL = EllipticalArc(O, A, C, L)
    MAMO = EllipticalArc(M, A, M, O)
    MALO = EllipticalArc(M, A, L, O)
    MAEO = EllipticalArc(M, A, E, O)

    # Plane surfaces
    ABCAs = PlaneSurface([ABCA], groups=['domain'])


class TestPoint(TestPrimitivies):
    def test_eq_ne(self):
        assert self.A != self.D
        assert self.A.eq(self.D)
        assert self.A.ne(self.B)

        class Pseudo:
            coors = np.array([0, 0, 0])
        P = Pseudo()
        assert not self.A.eq(P)

    def test_groups(self):
        assert self.A.groups == ['A', 'corners']
        self.A.remove_from_groups('corners')
        assert self.A.groups == ['A']
        self.A.add_to_groups('boundary')
        assert self.A.groups == ['A', 'boundary']


class TestLine(TestPrimitivies):
    def test_degenerated_line(self):
        with pytest.raises(AssertionError):
            Line(self.D, self.A)
        with pytest.raises(AssertionError):
            Line(self.A, self.D)

    def test_eq_ne(self):
        assert self.DC.eq(self.AC)
        assert self.DC.ne(self.AB)

    def test_is_reversed(self):
        assert self.DC.is_reversed(self.CD)
        assert self.DC.is_reversed(self.CA)

    def test_length(self):
        np.testing.assert_almost_equal(self.BC.length, np.sqrt(2))

    def test_poly(self):
        np.testing.assert_almost_equal(self.AB.poly(), self.AB.coors)
        #assert self.ABCD.poly(resolution=12).shape[0] == 12


class TestSpline(TestPrimitivies):
    def test_degenerated_line(self):
        with pytest.raises(AssertionError):
            Spline([self.D, self.A])

    def test_eq_ne(self):
        assert self.ABCA.eq(self.ABCD)

    def test_is_reversed(self):
        assert self.ABCD.is_reversed(self.ACBA)

    def test_is_closed(self):
        assert self.ABCD.is_closed is True
        assert self.ABCA.is_closed is True
        assert self.ABC.is_closed is False

    def test_poly(self):
        np.testing.assert_almost_equal(self.ABC.poly(), self.ABC.coors)
        assert self.ABCD.poly(res=12).shape[0] == 12
        x = [1, 0, -1, 0, 1]
        y = [0, 1, 0, -1, 0]
        pts = [Point(p) for p in zip(x, y)]
        S = Spline(pts)
        xy = S.poly(50)
        np.testing.assert_almost_equal(xy[0], xy[-1])
#        import pylab
#        pylab.plot(xy.T[0], xy.T[1])


class TestCircularArc(TestPrimitivies):
    def test_degenerated_arc(self):
        with pytest.raises(AssertionError):
            CircularArc(self.D, self.B, self.E)  # 180 degree
        with pytest.raises(AssertionError):
            CircularArc(self.A, self.C, self.B)  # not co-circular
        with pytest.raises(AssertionError):
            CircularArc(self.A, self.D, self.B)  # start eq center
        with pytest.raises(AssertionError):
            CircularArc(self.A, self.B, self.D)  # start eq end
        with pytest.raises(AssertionError):
            CircularArc(self.B, self.A, self.D)  # center eq end

    def test_eq_ne(self):
        assert self.BAC.eq(self.BDC)
        assert self.BAC.ne(self.FBC)

    def test_is_reversed(self):
        assert self.BAC.is_reversed(self.CDB)

    def test_radius(self):
        assert round(self.BAC.radius - 1., 7) == 0
        assert round(self.FBC.radius - np.sqrt(2), 7) == 0

    def test_angle(self):
        assert round(self.BAC.angle - np.pi/2., 7) == 0

    def test_chord(self):
        assert round(self.BAC.chord - np.sqrt(2), 7) == 0

    def test_length(self):
        assert round(self.BAC.length - 1*np.pi/2., 7) == 0

    def test_midpoint(self):
        target = np.array([0.57735027, -0.15470054,  0.57735027])
        check = abs(self.BCJ.midpoint.coors - target) < 1e-7
        assert check.all()

    def test_poly(self):
        np.testing.assert_almost_equal(self.BCJ.poly(), [self.BCJ.start.coors,
                                       self.BCJ.midpoint.coors,
                                       self.BCJ.end.coors])
        np.testing.assert_almost_equal(self.BCJ.poly(3)[1],
                                       self.BCJ.midpoint.coors)
        np.testing.assert_almost_equal(self.BCJ.poly(11)[[0, 5, 10]],
                                       [self.BCJ.start.coors,
                                        self.BCJ.midpoint.coors,
                                        self.BCJ.end.coors])


class TestEllipticalArc(TestPrimitivies):
    def test_degenerated_arc(self):
        with pytest.raises(AssertionError):
            EllipticalArc(self.D, self.B, self.D, self.E)  # colinear
        with pytest.raises(AssertionError):
            EllipticalArc(self.E, self.A, self.C, self.L)  # 180 degree
        with pytest.raises(ValueError):
            EllipticalArc(self.E, self.A, self.N, self.C)  # wrong radiuses

    def test_eq_ne(self):
        assert self.EAEC.eq(self.EAFC)
        assert self.EAEC.eq(self.EALC)
        assert self.MAMO.eq(self.MAEO)
        assert self.MAMO.eq(self.MALO)
        assert self.OAEM.eq(self.OALM)
        assert self.CALE.eq(self.CACE)
        assert self.OAEM.ne(self.MAMO)

    def test_is_reversed(self):
        assert self.OAEM.is_reversed(self.MAMO)
        assert self.EALC.is_reversed(self.CALE)

    def test_parametric_angle(self):
        spcangle = round(self.EALC.start_parametric_angle, 7)
        sprangle = round(self.EALC.start_polar_angle, 7)
        epcangle = round(self.EALC.end_parametric_angle, 7)
        eprangle = round(self.EALC.end_polar_angle, 7)
        assert spcangle == sprangle
        assert epcangle == eprangle

    def test_radiuses(self):
        aae = np.testing.assert_almost_equal
        aae(self.CALE.radiuses, (2, 1))
        aae(self.CACE.radiuses, (1, 2))

    def test_length(self):
        assert abs(self.EAEC.length - self.EALC.length) < 1e-7
        assert self.BAEC.length - np.pi/2. < 1e-7
        assert abs(self.EAEC.length - np.sqrt(93 + np.sqrt(3)/2)/4.) < 1e-7

    def test_midpoint(self):
        target = np.array([np.sqrt(2), np.sqrt(2)/2,  0.])
        check = abs(self.EAEC.midpoint.coors - target) < 1e-7
        assert check.all()

    def test_poly(self):
        aae = np.testing.assert_almost_equal
        aae(self.EAEC.poly(), [self.EAEC.start.coors,
                               self.EAEC.midpoint.coors,
                               self.EAEC.end.coors])
        aae(self.EAEC.poly(3)[1], self.EAEC.midpoint.coors)
        aae(self.EAEC.poly(11)[[0, 5, 10]], [self.EAEC.start.coors,
                                             self.EAEC.midpoint.coors,
                                             self.EAEC.end.coors])
        np.testing.assert_almost_equal(self.EAEC.poly(50), self.EALC.poly(50))
        x, y, z = self.EAEC.poly(50).T
        #import pylab
        #pylab.plot(x, y)
        #pylab.show()


class TestPlaneSurface(TestPrimitivies):
    def test_proper_definition(self):
        ABC = PlaneSurface([self.AB, self.BC, self.CA])
        assert ABC.curves == [self.AB, self.BC, self.CA]
        assert ABC.corient == [1, 1, 1]

    def test_repeating_lines(self):
        ABC = PlaneSurface([self.AB, self.BC, self.CA, self.CD, self.CA])
        assert ABC.curves == [self.AB, self.BC, self.CA]
        assert ABC.corient == [1, 1, 1]

    def test_not_connected_lines(self):
        ABC = PlaneSurface([self.AB, self.BC, self.CA, self.BE])
        assert ABC.curves == [self.AB, self.BC, self.CA]
        assert ABC.corient == [1, 1, 1]

    def test_overconnected_lines(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.AB, self.BC, self.CA, self.BE, self.CE])

    def test_reorient_single_curve(self):
        ABC = PlaneSurface([self.AB, self.CB, self.CA])
        assert ABC.curves == [self.AB, self.CB, self.CA]
        assert ABC.corient == [1, -1, 1]

    def test_reorganize_curves(self):
        ABC = PlaneSurface([self.AB, self.CE, self.BE, self.AC])
        assert ABC.curves == [self.AB, self.BE, self.CE, self.AC]
        assert ABC.corient == [1, 1, -1, -1]

    def test_reorient_curve_loop(self):
        ABC = PlaneSurface([self.AB, self.CE, self.BE, self.AC],
                           orientation=-1)
        assert ABC.curves == [self.AB, self.AC, self.CE, self.BE]
        assert ABC.corient == [-1, 1, 1, -1]

    def test_cw_ccw_xy(self):
        ABC = PlaneSurface([self.DC, self.BD, self.BC], orientation='cw')
        assert ABC._PlaneSurface__get_orientation() == -1
        assert ABC.curves == [self.DC, self.BC, self.BD]
        assert ABC.corient == [1, -1, 1]
        ABC.orientation = 'counterclockwise'
        assert ABC.curves == [self.DC, self.BD, self.BC]
        assert ABC.corient == [-1, -1, 1]

    def test_cw_ccw_xz(self):
        ABC = PlaneSurface([self.JB, self.AB, self.AJ])
        assert ABC._PlaneSurface__get_orientation() == 1
        assert ABC.curves == [self.JB, self.AB, self.AJ]
        assert ABC.corient == [1, -1, 1]
        ABC.orientation = 'counterclockwise'
        assert ABC.curves == [self.JB, self.AB, self.AJ]
        assert ABC.corient == [1, -1, 1]

    def test_cw_ccw_yz(self):
        ABC = PlaneSurface([self.CA, self.CJ, self.AJ], orientation=-1)
        assert ABC._PlaneSurface__get_orientation() == -1
        assert ABC.curves == [self.CA, self.AJ, self.CJ]
        assert ABC.corient == [1, 1, -1]
        ABC.orientation = 'ccw'
        assert ABC.curves == [self.CA, self.CJ, self.AJ]
        assert ABC.corient == [-1, 1, -1]

    def test_cw_ccw_xyz(self):
        ABC = PlaneSurface([self.BC, self.CJ, self.JB])
        assert ABC._PlaneSurface__get_orientation() == 1
        assert ABC.curves == [self.BC, self.CJ, self.JB]
        assert ABC.corient == [1, 1, 1]
        ABC.orientation = 'cw'
        assert ABC.curves == [self.BC, self.JB, self.CJ]
        assert ABC.corient == [-1, -1, -1]

    def test_cw_ccw_negative(self):
        ABC = PlaneSurface([self.AL, self.LC, self.CA], orientation=-1)
        assert ABC._PlaneSurface__get_orientation() == -1
        ABC = PlaneSurface([self.AC, self.AL, self.LC])
        assert ABC._PlaneSurface__get_orientation() == 1

    def test_cw_ccw_concave(self):
        ABC = PlaneSurface([self.AH, self.HB, self.BC, self.CA])
        assert ABC.curves == [self.AH, self.HB, self.BC, self.CA]
        assert ABC.corient == [1, 1, 1, 1]

    def test_cw_ccw_very_concave(self):
        ABC = PlaneSurface([self.AK, self.KB, self.BC, self.CA],
                           orientation=-1)
        assert ABC.curves == [self.AK, self.CA, self.BC, self.KB]
        assert ABC.corient == [-1, -1, -1, -1]

    def test_cw_ccw_cieslik(self):
        A = Point([0, 0], groups=['corners'], elsize=1)
        B = Point([0, 462], groups=['corners'], elsize=1)
        B1 = Point([0, 457], groups=['corners'], elsize=1)
        C = Point([462, 462], groups=['corners'], elsize=1)
        D = Point([462, 0], groups=['corners'], elsize=1)
        D1 = Point([457, 0], groups=['corners'], elsize=1)

        B1B = Line(B1, B, groups=['left'])
        BC = Line(B, C, groups=['top'])
        CD = Line(C, D, groups=['right'])
        DD1 = Line(D, D1, groups=['bottom'])
        B1AD1 = CircularArc(B1, A, D1)

        BDC_Surface = PlaneSurface([B1B, BC, CD, DD1, B1AD1],
                                   groups=['matrix2'],
                                   elsize_factor=20.)

        assert BDC_Surface.curves == [B1B, B1AD1, DD1, CD, BC]
        assert BDC_Surface.corient == [-1, 1, -1, -1, -1]
        BDC_Surface.orientation = -1
        assert BDC_Surface.curves == [B1B, BC, CD, DD1, B1AD1]
        assert BDC_Surface.corient == [1, 1, 1, 1, -1]

    def test_non_coplanar(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.AH, self.HB, self.JB, self.AJ])

    def test_almost_coplanar(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.IH, self.HB, self.BC, self.IC])
        PlaneSurface([self.IH, self.HB, self.BC, self.IC], tol=1e-6)

    def test_non_coplanar_arc(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.BAC, self.CJ, self.JB])

    def test_no_curve_loops(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.BAC, self.CJ, self.AB, self.HB])

    def test_two_curves(self):
        ABC = PlaneSurface([self.BAC, self.BC])
        assert ABC.curves == [self.BAC, self.BC]
        assert ABC.corient == [1, -1]
        ABC = PlaneSurface([self.BC, self.BAC])
        assert ABC.curves == [self.BC, self.BAC]
        assert ABC.corient == [-1, 1]
        ABC = PlaneSurface([self.CAB, self.BC])
        assert ABC.curves == [self.CAB, self.BC]
        assert ABC.corient == [-1, -1]
        ABC = PlaneSurface([self.BC, self.CAB])
        assert ABC.curves == [self.BC, self.CAB]
        assert ABC.corient == [-1, -1]

    def test_two_curves_ellipse(self):
        ABC = PlaneSurface([self.EAEC, self.CE], 'two curves')
        ABC.gmsh.msh
        #ABC.gmsh.preview()

    def test_colinear_lines(self):
        with pytest.raises(ValueError):
            PlaneSurface([self.AB, self.BE, self.AE])

    def test_single_spline(self):
        ABCA = PlaneSurface([self.ABCA])
        ACBA = PlaneSurface([self.ACBA])
        assert ABCA.curves == [self.ABCA]
        assert ABCA.corient == [1]
        assert ACBA.corient == [-1]

    def test_gmsh_msh_with_hole(self):
        h = PlaneSurface([self.ABGA], groups='hole', remove=False)
        s = PlaneSurface([self.MFCLM], holes=[h], groups='domain')
        s.gmsh.msh
        # s.gmsh.preview()

    def test_surface_add(self):
        s1 = PlaneSurface([self.AB, self.BC, self.CA], groups='ABC')
        s2 = PlaneSurface([self.BE, self.CE, self.CB], groups='BEC')
        s = s1 + s2
        s.gmsh.msh
        #s.gmsh.preview()

    def test_surface_sub(self):
        s1 = PlaneSurface([self.AB, self.BC, self.CA], groups='ABC')
        s2 = PlaneSurface([self.BE, self.CE, self.CB], groups='BEC')
        s = s1 + s2
        s = s - s1
        s.gmsh.msh
        #s.gmsh.preview()

    def test_surface_move(self):
        s = PlaneSurface([self.AB, self.BC, self.CA], groups='ABC')
        s.move([2, 0])
        s.gmsh.msh
        #s.gmsh.preview()

    def test_surface_resize(self):
        s1 = PlaneSurface([self.AB, self.BC, self.CA], groups='ABC')
        s2 = s1.copy()
        s2.resize(0.5)
        s1.add_hole(s2)
        s1.gmsh.msh
        # s1.gmsh.preview()

    def test_periodic_lines(self):
        ef = self.A.elsize_factor
        self.A.elsize_factor=0.05
        self.AB.periodic(self.BC, -1)
        s1 = PlaneSurface([self.AB, self.BC, self.CA], groups='ABC')
        s1.gmsh.msh
        # s1.gmsh.preview()
        self.A.elsize_factor = ef
        self.AB.slaves = None  

if __name__ == '__main__':
    pytest.main([str(__file__), '-v'])  # Run tests from current file