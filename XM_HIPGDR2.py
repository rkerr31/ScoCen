#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:06:20 2019

@author: rmk2432
"""
import numpy as np
import matplotlib.pyplot as plt

dl,rao,ra,dc,par,pae,pmra,pmrae,pmdc,pmdce,g,bmr  = np.loadtxt('HIP+GDR2XM.csv', delimiter=',', usecols=[0,3,14,16,18,19,20,21,22,23,27,34],skiprows=1, dtype=str).T
name,spt,mem,rv,rve = np.loadtxt('HIP+GDR2XM.csv', delimiter=',', dtype=str, usecols=[1,6,7,35,36], skiprows=1).T
###REMOVE OBJECTS WITH INCOMPLETE DATA#############################################################################################
par[par=='']=0
pmdc[pmdc=='']=0
pmra[pmra=='']=0
par = np.asarray(map(float, par))
pmra = np.asarray(map(float, pmra))
pmdc = np.asarray(map(float, pmdc))
fltr = np.logical_and(bmr!='', par>4)
#fltr = np.logical_and(bmr!='', par!='')
###REMOVE STARS WITH DUPLICATES IN XMATCH##########################################################################################
def purgeduplicates(name, dl):
    dl = map(float, dl)
    nl = np.full(len(dl),3)
    for i in xrange(len(name)):
        if nl[i]==3:
            ls    = rao[rao==rao[i]]
            rmtch = np.argmin(ls)
            for j in xrange(len(ls)):
                if j==rmtch:
                    nl[i+j]=True
                else:
                    nl[i+j]=False 
    return nl

pdf = purgeduplicates(name, dl)
fltr = np.logical_and(fltr, pdf==1)
fltr = np.logical_and(fltr, mem!='N')
flpr = np.logical_and(pmra<-2, pmra>-50)
flpd = np.logical_and(pmdc<-2, pmdc>-50)
flpm = np.logical_and(flpd,flpr)
#fltr = np.logical_and(fltr, flpm)
###APPLY NEWLY UPDATED FILTERS#####################################################################################################
dl,ra,dc,par,pae,pmra,pmrae,pmdc,pmdce,g,bmr  = np.loadtxt('HIP+GDR2XM.csv', delimiter=',', usecols=[0,14,16,18,19,20,21,22,23,27,34],skiprows=1, dtype=str)[fltr].astype(np.float).T
name,spt,mem,rv,rve = np.loadtxt('HIP+GDR2XM.csv', delimiter=',', dtype=str, usecols=[1,6,7,35,36], skiprows=1)[fltr].T
###LOAD ISOCHRONE#################################################################################################################
Gi,Bi,Ri = np.loadtxt('40Myr_iso.dat',usecols=[25,26,27], skiprows=1).T
bmri = Bi-Ri
###DO STUFF#######################################################################################################################
G = g + 5.0*(np.log10(par/1000.)+1)
#plt.plot(ra, dc, 'r.')
#plt.gca().invert_xaxis()
plt.plot(bmr, G,'g.')
plt.gca().invert_yaxis()
plt.xlabel('BP-RP')
plt.ylabel('G')

da = np.concatenate((np.loadtxt('HIP+GDR2XM.csv', delimiter=',', usecols=[14,16,18,19,20,21,22,23,27,34],skiprows=1, dtype=str)[fltr],np.loadtxt('HIP+GDR2XM.csv', delimiter=',', dtype=str, usecols=[1,6,7,35,36], skiprows=1)[fltr] ), axis=1)
np.savetxt('XM_SCOCEN_CANDIDATES.csv', da, fmt='%s', delimiter=',', header='RA,DEC,PAR,PAR_ERR,PM_RA,PM_RA_ERR,PM_DEC,PM_DEC_ERR,G,BP_RP,NAME,SPT,MEM?,RV,RV_ERR')
