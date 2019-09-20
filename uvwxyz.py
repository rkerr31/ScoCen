#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:26:20 2019
@author: rmk2432
"""

import sys
sys.path.append('../')

import numpy as np
from gal_uvw import gal_uvw
from gal_xyz import gal_xyz
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS
from astropy.coordinates import Galactic
###IMPORT OUR DATA ARRAY#######################################################
ra, dc, par, pae, pmra, pmrae, pmdc, pmdce, g, bmr, name, spt, mem, rv, rve = np.load('SCOCEN_ALL_WITH_RVS.npy', allow_pickle=True).T

c = SkyCoord(ra=ra.astype(float)*u.degree, dec=dc.astype(float)*u.degree, frame='icrs')
gc = c.transform_to('galactic')

def cnv(arr):
    return np.asarray(map(float, arr))
l,b = gc.l, gc.b
U, V, W = gal_uvw(lsr=2, ra=cnv(ra), dec=cnv(dc), pmra=cnv(pmra), pmdec=cnv(pmdc), vrad=cnv(rv), plx=cnv(par))
X, Y, Z = gal_xyz(cnv(ra),cnv(dc),cnv(par),radec=True)

G = cnv(g) + 5.0*(np.log10(cnv(par)/1000.)+1)
bmr = cnv(bmr)
ra = cnv(ra)
dc = cnv(dc)
###XYZ PLOT####################################################################
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot(X, Y, Z, 'k.')
#ax.set_xlabel('X')
#ax.set_ylabel("Y")
#ax.set_zlabel("Z")
###UVW PLOT####################################################################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(U, V, W, 'k.')
ax.set_xlabel('U')
ax.set_ylabel("V")
ax.set_zlabel("W")