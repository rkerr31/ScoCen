#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 14:34:58 2019

@author: rmk2432
"""
import numpy as np 
from XMf import XM
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.pyplot as plt
from astropy.io import fits
###IMPORT COMPLETE CANDIDATES LIST#############################################################
ral, dcl = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1]).T
arr1 = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14], dtype=str)
###INTRODUCE RADIAL VELOCITIES DATA FROM CHIRON AND WIFES######################################
rax, dcx = np.loadtxt('joint_rvtab.csv', delimiter=',', usecols=[1,2], skiprows=1).T
arr2 = np.loadtxt('joint_rvtab.csv', delimiter=',', usecols=[13,14], skiprows=1, dtype=str)
###INTRODUCE RAVE RADIAL VELOCITIES (DR4 FOR NOW, UPDATE TO DR5 POSSIBLY NECESSARY)############
rave = np.load('BigCatalogs/RAVE_DR5_TRUNCATED.npy')
rar, dcr = rave.T[0:2]
rave = rave.T[2:].T
###INTRODUCE GALAH RADIAL VELOCITY OBSERVATIONS################################################
galah = np.load('BigCatalogs/GALAH_DR2_catalog.npy')[:,[5, 6, 20, 21]]
galah = galah[np.invert(np.isnan(map(float, galah[:,2])))]
rag, dcg = galah.T[0:2].astype(np.float)
galah = galah.T[2:].T
###BEGIN THE CROSSMATCHING#####################################################################
daxm = XM(ral, dcl, rax, dcx, arr1, arr2, 2.5)
ra, dc, par, pae, pmra, pmrae, pmdc, pmdce, g, bmr, name, spt, mem, rvm, rvme, rvx, rvxe = daxm.T
daxmxm = XM(ra.astype(np.float), dc.astype(np.float), rag, dcg, daxm, galah, 2.5)
ra, dc, par, pae, pmra, pmrae, pmdc, pmdce, g, bmr, name, spt, mem, rvm, rvme, rvx, rvxe, rvg, rvge = daxmxm.T
daxmxmxm = XM(ra.astype(np.float), dc.astype(np.float), rar, dcr, daxmxm, rave, 2.5)
ra, dc, par, pae, pmra, pmrae, pmdc, pmdce, g, bmr, name, spt, mem, rvm, rvme, rvx, rvxe, rvg, rvge, rvr, rvre = daxmxmxm.T
rvm[rvm=='']=None
rvme[rvme=='']=None

rvca = []
rveca = []
for i in xrange(len(rvm)):
    if rvm[i]!='' or rvx[i] is not None or rvg[i] is not None or rvr[i] is not None:
        rvs = np.asarray([rvm[i], rvx[i], rvg[i], rvr[i]]).astype(float)
        rves = np.asarray([rvme[i], rvxe[i], rvge[i], rvre[i]]).astype(float)
        cnd = np.invert(np.isnan(rvs))
        rvs = rvs[cnd]
        rves = rves[cnd]
        wt = 1./rves**2 
        if len(rvs)==1:
            rvca.append(rvs[0])
            rveca.append(rves[0])
        elif len(rvs)>1:
            rvca.append(np.average(rvs, weights=wt))
            rveca.append(1./np.sqrt(np.sum(wt)))
        else:
            rvca.append(None)
            rveca.append(None)
rvd = np.asarray(zip(rvca, rveca))
dat = np.concatenate((daxm.T[:13].T, rvd), axis=1)
dat = dat[np.logical_and(np.invert(np.isnan(rvd.T[0].astype(float))), rvd.T[1]>0)]
np.save('SCOCEN_ALL_WITH_RVS.npy', dat)

