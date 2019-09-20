#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:53:50 2019

@author: rmk2432
"""
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

feh = np.load('BigCatalogs/FEH.npy')

fehd, bne = np.histogram(feh, bins=np.linspace(-2,1.1,300))
bnc = (bne[:-1]+bne[1:])/2.

fds = savgol_filter(fehd, 15, 3)

pc = fds>0
fds = fds[pc]
bnc = bnc[pc]

intf = interp1d(bnc, fds)

bncf = np.linspace(min(bnc), max(bnc), 100000)

plt.hist(feh, bins=np.linspace(-2,1.1,300))
plt.plot(bnc, fds)

prob = intf(bncf)
prob = savgol_filter(prob, 1501, 3)
plt.plot(bncf, prob)

outarr = zip(bncf, prob/sum(prob))
np.save('fehdist.npy', outarr)
#fds = fds/sum(fds)