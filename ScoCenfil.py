# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt

datarr = np.loadtxt('ScoCen_F2.csv', delimiter=',', skiprows=1, usecols=[1,2,3,4,5,6,7,8,9,10,13,14]).T
rva, rve = np.loadtxt('ScoCen_F2.csv', delimiter=',', skiprows=1, dtype=str, usecols=[11,12]).T
ra, dec, par, pae, pmra, pmrae, pmdc, pmdce, g, bmr, l, b = datarr
G = g + 5.0*(np.log10(par/1000.)+1)

#plt.plot(bmr[G<13], G[G<13], 'k,')
plt.hexbin(bmr[G<13], G[G<13])
plt.gca().invert_yaxis()
