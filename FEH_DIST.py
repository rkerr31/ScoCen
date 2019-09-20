#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:53:50 2019

@author: rmk2432
"""
import numpy as np
import numpy.random
import matplotlib.pyplot as plt

dl,feh, dis = np.loadtxt('BigCatalogs/GALAH_FEH_DIS.csv', usecols=[0,3,7], delimiter=',', skiprows=1, dtype=str).T#astype(float)
cnd = dis!=''
feh = feh[cnd].astype(float)
dis = dis[cnd].astype(float)
dl  = dl[cnd].astype(float)
#def randomize_metallicity():

feh = feh[np.logical_and(dis<500., dl<0.75)]

np.save('BigCatalogs/FEH.npy',feh)
    