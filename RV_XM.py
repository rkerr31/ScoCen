#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:00:21 2019

@author: rmk2432
"""
import numpy as np 
import matplotlib.pyplot as plt

#dat = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1,2,3,4,5,6,7,8,9]).T
ral, dcl = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1]).T
rax, dcx, rvx, rvex = np.loadtxt('joint_rvtab.csv', delimiter=',', usecols=[1,2,13,14], skiprows=1).T
#name = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[10],dtype=str)
###FILTER SOURCES THAT HAVE NO RVS WHATSOEVER###########################################################
rvxml = []
rvexml = []
for i in xrange(len(ral)):
    dil = np.sqrt((ral[i]-rax)**2+(dcl[i]-dcx)**2)*3600
    if np.min(dil)<3.0:
        rvxml.append(rvx[np.argmin(dil)])
        rvexml.append(rvex[np.argmin(dil)])
    else:
        rvxml.append('x')
        rvexml.append('x')
rvxml = np.asarray(rvxml)
rvexml = np.asarray(rvexml)
rv, rve = np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', dtype=str, usecols=[13,14]).T

filcond = np.logical_or(rv!='', rvxml!='x')
###ASSEMBLE RVS FROM BOTH SOURCES AND COMBINE THEM VIA WEIGHTED AVERAGE##################################
rvg = rv[filcond]
rvge = rve[filcond]
rvm = rvxml[filcond] 
rvme = rvexml[filcond]      

rvc = []
rvce = []
for i in xrange(len(rvg)):
    if rvg[i]!='' and rvm[i]!='x':
        wt = np.asarray([1./(float(rvge[i]))**2,1./(float(rvme[i]))**2]) 
        rv = np.asarray([float(rvg[i]), float(rvm[i])])
        rvc.append(np.average(rv, weights=wt))
        rvce.append(np.sqrt(float(rvge[i])**2+float(rvme[i])**2)/2.)
#        print wt, rv, np.average(rv, weights=wt), np.sqrt(float(rvge[i])**2+float(rvme[i])**2)/2.
    elif rvg[i]!='':
        rvc.append(rvg[i])
        rvce.append(rvge[i])
    else:
        rvc.append(rvm[i])
        rvce.append(rvme[i])

rvc = np.asarray(rvc).astype(np.float)
rvce = np.asarray(rvce).astype(np.float)

da = np.concatenate((np.loadtxt('XM_SCOCEN_CANDIDATES.csv', delimiter=',', usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12], dtype=str)[filcond], zip(rvc, rvce)), axis=1)
np.savetxt('SCO_CEN_RV.csv', da, fmt='%s', delimiter=',', header='RA,DEC,PAR,PAR_ERR,PM_RA,PM_RA_ERR,PM_DEC,PM_DEC_ERR,G,BP_RP,NAME,SPT,MEM?,RV,RV_ERR')
