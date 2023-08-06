# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 18:45:49 2018

@author: awitek
"""
import numpy as np
from fempy.models.heatandmoisture import HeatAndMoisture


class Test_HAM(object):
    def test_EN_15026(self):
        from fempy.geometry import Point, Line
        A = Point([0, 0, 0], groups='left', elsize_factor=0.001)
        B = Point([15, 0, 0], groups='right', elsize_factor=0.15)
        AB = Line(A, B, groups='construction')
        d = AB.gmsh.domain(2)

        c = construction()
        c.useT(False)
        mat = [c]
        fsn = ['construction']
        env = [outside()]
        sds = ['left']

        m = HAMvalidation(d, mat, fsn, env, sds)
        # setting adiabatic surfaces
        m.T[:] = 293.15
        m.fi[:] = 0.5
        m.alpha[:] = 1.0e4
        m.beta[:] = 1.0e-3
        m.alpha['~left'] = 0.0
        m.beta['~left'] = 0.0
        m.time0 = 0.              # start time
        m.time1 = 7. * 24 * 3600  # finish time, 7 days
        m.solve(verbose=False, rtol=1e-4, atol=1e-4)  # solve
        ###
        scs = m.domain.ngroups.nums(sortby='x')
        x = m.domain.coors[scs, 0]
        # Test after 7 days
        m.sol(7. * 24 * 3600)
        psuc = -c.R/c.Mw * 293.15 * 1.0e3 * np.log(m.fi)
        n_w = 146./(1. + (8.0e-8 * psuc)**1.6)**0.375
        y = n_w[scs]
        # data from standard EN 15026 - test n_w
        xx = [0.01, 0.02, 0.03, 0.04]
        miny7 = [50.2, 41.3, 40.8, 40.8]
        maxy7 = [54.5, 45.6, 45.1, 45.1]
#        miny30=[[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08],
#                [81.0, 51.1, 43.6, 41.5, 40.9, 40.8, 40.8]]
#        maxy30=[[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08],
#                [85.3, 55.3, 47.9, 45.7, 45.2, 45.1, 45.1]]
#        miny365=[[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1],
#                 [117.5, 104.4, 88.7, 75.6, 62.8, 55.7, 47.9, 44.1]]
#        maxy365=[[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1],
#                 [121.8, 108.7, 93.0, 77.9, 67.1, 60.0, 52.2, 48.4]]
        resfi = np.interp(xx, x, y)
        assert np.all(resfi > miny7)
        assert np.all(resfi < maxy7)
        # data from standard EN 15026  - test temperature
        xx = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
        miny7 = [26.4, 23.6, 21.7, 20.6, 20.0, 19.8, 19.8, 19.8]
        maxy7 = [26.9, 24.1, 22.2, 21.1, 20.5, 20.4, 20.3, 20.3]
#        miny30=[x, [28.1, 26.5, 25.0, 23.7, 22.7, 21.8, 20.7, 20.1]]
#        maxy30=[x, [28.6, 27.0, 25.5, 24.3, 23.2, 22.3, 21.2, 20.6]]
#        miny365=[x, [29.2, 28.8, 28.3, 27.8, 27.4, 26.9, 26.0, 25.2]]
#        maxy365=[x, [29.8, 29.3, 28.8, 28.4, 27.9, 27.4, 26.6, 25.7]]
        y = m.T[scs] - 273.15
        resT = np.interp(xx, x, y)
        assert np.all(resT > miny7)
        assert np.all(resT < maxy7)
        # Test specific temperature at some point
        num = 800
        np.testing.assert_almost_equal(m.T[num], 294.370064598995)


class outside():
    t2 = 1*1*3600

    def temp(self, time):
        return 293.15 + 10. * time/max(time, self.t2)

    def fi(self, time):
        return 0.5 + 0.45 * time/max(time, self.t2)


class HAMvalidation(HeatAndMoisture):
    def setup(self, materials, field_names, environment, sides):
        self.materials = materials
        self.field_names = field_names
        self.environment = environment
        self.sides = sides
        # Set constants
        self.rho_w[:] = 1000.
        self.cp_w[:] = 4190.
        # Initialize variables
        self.update()

    def coefficients_update(self):
        from fempy.fields.operators import ongauss
        T = ongauss(self.T)
        fi = ongauss(self.fi)
        for i, m in enumerate(self.materials):
            n = self.field_names[i]
            #
            f = fi[n]
            m.setfi(f)
            temp = T[n]
            m.setT(temp)
            m.useT(True)
            #
            self.rho_s[n] = m.rho
            self.cp_s[n] = m.cp
            self.w[n] = m.w
            self.ksi[n] = m.ksi
            #
            k = m.k
            d = m.vdp
            D = m.dfi
            #
            self.kij[n, ..., 0, 0] = k
            self.dp[n, ..., 0, 0] = d
            self.Dfi[n, ..., 0, 0] = D
            s = self.kij.shape[-1]
            if s > 1:
                self.kij[n, ..., 1, 1] = k
                self.dp[n, ..., 1, 1] = d
                self.Dfi[n, ..., 1, 1] = D
            if s > 2:
                self.kij[n, ..., 2, 2] = k
                self.dp[n, ..., 2, 2] = d
                self.Dfi[n, ..., 2, 2] = D

    def environments_update(self):
        t = self.time
        for i, s in enumerate(self.sides):
            envir = self.environment[i]
            self.Text[s] = envir.temp(t)
            if 'fi' in dir(envir):
                fi = envir.fi(t)
            elif 'press' in dir(envir):
                fi = envir.press(t)/self.pextsat
            self.fiext[s] = fi


class materials():
    Mw = 0.01801528            # molar weight of water [kg/mol]
    R = 8.3144598              # universal gas constant [J/(mol*K)]

    def setfi(self, fi):
        self.fi = fi

    def setT(self, T):
        self.T = T

    def useT(self, yn):
        if yn:
            self.temp = self.T
        else:
            self.temp = 293.15

    @property
    def hpsuc(self):
        return self.psuc / (1.0e3 * 9.81)

    @property
    def psuc(self):
        """
        Moisture storage function
        Standard simplification: constatnt temperature
        """
        f = self.fi
        return - self.R / self.Mw * self.temp * 1.0e3 * np.log(f)

    @property
    def dw(self):
        """ Liquid transport coefficient [m2/s] """
        return - self.KK * self.dpsucdw

    @property
    def dfi(self):
        """ Liquid conduction coefficient [kg/(m*s)] """
        return self.dw * self.ksi


class construction(materials):
    rho = 2280.  # [kg/m3]
    cp = 800.    # [J/(kg*K)]

    @property
    def w(self):
        """ Moisture storage function [kg/m3] """
        return 146. / (1. + (8.0e-8 * self.psuc)**1.6)**0.375

    @property
    def vdp(self):
        """ Vapour permeability of the solid, [kg/(m*s*Pa)],
        accordingly to standard, Wufi splits it to nu and delta"""
        w = self.w
        v = self.Mw / self.R / self.temp
        v *= 26.1e-6 / 200. * (1. - w/146.)
        v /= 0.503 * (1. - w/146.)**2 + 0.497
        return v

    @property
    def k(self):
        """ Thermal conductivity [W/(m*K)]"""
        return 1.5 + 15.8e-3 * self.w  # w - water content

    @property
    def dpsucdw(self):
        """ Suction pressure derivative """
        w = self.w
        return -self.psuc * 0.625 / (1. - (146./w)**(-1./0.375)) / (0.375 * w)

    @property
    def KK(self):
        """ Liquid water conductivity """
        w = self.w
        k = -39.2619 + 0.0704 * (w-73.) - 1.7420e-4 * (w-73.)**2
        k -= 2.7953e-6 * (w-73.)**3 + 1.1566e-7 * (w-73.)**4
        k += 2.5969e-9 * (w-73.)**5
        from numpy import exp
        return exp(k)

    @property
    def ksi(self):
        """ Moisture storage capacity [kg/m3] """
        f = self.fi
        k = 3.867658187008071e-10 * self.R / self.Mw
        k *= self.temp * 1.0e3 * self.psuc**0.6
        k /= f * (4.41513491667588e-12 * self.psuc**1.6 + 1.)**1.375
        return k


if __name__ == '__main__':
    import pytest
    pytest.main([str(__file__), '-v'])
