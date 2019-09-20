#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:59:50 2019

@author: rmk2432
"""

from astropy import units as u
from astroquery.xmatch import XMatch
table = XMatch.query(cat1=open('BigCatalogs/GALAH_DR2_FEH.csv'),
                      cat2='vizier:I/347/gaia2dis',
                      max_distance=1 * u.arcsec, colRA1='ra',
                      colDec1='dec')

#table = XMatch.query(cat1=open('BigCatalogs/GALAH_DR2_FEH_TR.csv'),
#                     cat2='vizier:I/347/gaia2dis',max_distance=1 * u.arcsec,colRA1='ra',colDec1='dec')