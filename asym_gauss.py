#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:38:05 2019

@author: rmk2432
"""
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import lmfit

feh = np.load('BigCatalogs/FEH.npy')

fehd, bne = np.histogram(feh, bins=300)
bnc = (bne[:-1]+bne[1:])/2.

cnl = bnc<0.02
cnh = bnc>0.02

bnl = bnc[cnl]
bnh = bnc[cnh]
fehl = fehd[cnl]
fehh = fehd[cnh]

plt.hist(feh, bins=300)

def modelfit(y, bn):
    def model(parameters, x):
        a = parameters['a'].value
        b = parameters['b'].value
        c = parameters['c'].value
        return a*np.exp(-((x-b)**2/(2*c**2)))

    x = bn
     
# Residuals to be Minimized
    def residuals(fit_parameters, x_data, y_data):
        return (y_data - model(fit_parameters, x_data))**2

# Load Data
    p = lmfit.Parameters()
#           (Name,   Value,   Vary,   Min,   Max,   Expr)
    p.add_many(('a', 1796.,     True,   None,  None,  None),
               ('b', 0,     True,   None,  None,  None),
               ('c', 0.3,     True,   None,  None,  None))
# the earlier values are parameter guesses. they should work, but if the fits are poor, try adjusting 'b'.
# Perform least-squares optimization
    fit_results = lmfit.minimize(residuals, p, args=(x, y))
    ys = model(fit_results.params, x)
    plt.plot(x, ys)
    #plt.imshow(y_fit, extent=[np.min(xa), np.max(xa), np.max(za), np.min(za)])
    return fit_results.params['b'].value, fit_results.params['a'].value, fit_results.params['c'].value

modelfit(fehl, bnl)
modelfit(fehh, bnh)