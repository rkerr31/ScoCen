#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:01:10 2019

@author: rmk2432
"""
import numpy as np
import astropy.coordinates as coord
import astropy.units as u
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ra,dc,par,pae,pmra,pmrae,pmdc,pmdce,g,bmr, rv, rve  = np.loadtxt('SCO_CEN_RV.csv', delimiter=',', usecols=[0,1,2,3,4,5,6,7,8,9,13,14]).T

ds = coord.ICRS(ra=ra*u.degree, dec=dc*u.degree,
                distance=(par*u.mas).to(u.pc, u.parallax()),
                pm_ra_cosdec=pmra*u.mas/u.yr,
                pm_dec=pmdc*u.mas/u.yr,
                radial_velocity=rv*u.km/u.s)

gc = ds.transform_to(coord.Galactocentric)

X, Y, Z = gc.x, gc.y, gc.z
U,V,W = gc.u, gc.v_y, gc.v_z

G = g + 5.0*(np.log10(par/1000.)+1)

#plt.plot(gc.v_x, gc.v_y, 'k.')

#plt.plot(V,W,'k.')
#plt.xlabel('V')
#plt.ylabel('W')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(X, Y, Z, 'k.')
ax.set_xlabel('U')
ax.set_ylabel("V")
ax.set_zlabel("W")