#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:53:50 2019

@author: rmk2432
"""
import numpy as np
for i in xrange(40):
    dat = np.loadtxt('Isochrones/iso'+str(i+1)+".txt", usecols=[1,2,5,25,26,28])
    if i+1==1:
        ca = dat
    else:
        ca = np.concatenate((ca, dat))
    print i+1

np.save('Isochrones/ISO_ALL_bright.npy', ca)

for i in xrange(40):
    dat = np.loadtxt('Isochrones/iso'+str(i+1)+".txt", usecols=[1,2,5,25,27,28])
    if i+1==1:
        ca = dat
    else:
        ca = np.concatenate((ca, dat))
    print i+1

np.save('Isochrones/ISO_ALL_faint.npy', ca)