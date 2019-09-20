#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 13:46:54 2019

@author: rmk2432
"""
import numpy as np 
import matplotlib.pyplot as plt
from gcirc import gcirc

###SCRIPT FOR CROSS-MATCHING TWO ARRAYS AND JOINING THEIR DATA SETS
#ral, dcl = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1]).T
#arr1 = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12], dtype=str)
#rax, dcx = np.loadtxt('joint_rvtab.csv', delimiter=',', usecols=[1,2], skiprows=1).T
#arr2 = np.loadtxt('joint_rvtab.csv', delimiter=',', usecols=[1,2,13,14], skiprows=1, dtype=str)

def XM(ral1, dcl1, ral2, dcl2, a1, a2, sr):
    #sr: search radius
    #ral1, dcl1: RA and Dec on list you wish to find matches for
    #ral2, dcl2: RA and Dec containing data you would like to associate with main list
    #a1, a2: data arrays containing information corresponding to objects in ral1, dcl1, ral2, dcl2 
    xmd = []
    for i in xrange(len(ral1)):
        dlm = gcirc(ral1[i], dcl1[i], ral2, dcl2)
        if np.min(dlm)<sr:
            tda = np.concatenate((a1[i], a2[np.argmin(gcirc(ral1[i], dcl1[i], ral2, dcl2))]))
            xmd.append(tda)
        else:
            tda = np.concatenate((a1[i], [None]*len(a2[0])))
            xmd.append(tda)
    return np.asarray(xmd)


    
