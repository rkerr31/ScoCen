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
from numpy import random as rand

feh, prob = np.load('fehdist.npy').T
dfeh = feh[1]-feh[0]

def rndmFeH():
    return (rand.choice(feh, size=1, p=prob)+(dfeh*rand.rand(1)-(dfeh/2)))[0]

l = []
for i in xrange(1000000):
    l.append(rndmFeH())

rndm = l

plt.hist(rndm, bins=np.linspace(min(feh), max(feh), 1000))
hst, bn = np.histogram(rndm, bins=np.linspace(min(feh), max(feh), 1000))
plt.plot(feh, prob*100000000)