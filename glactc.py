##a python version of the astrolib glactc.pro for IDL
##written as a function and assuming everything is in J2000 coords
##only goes radec-->l,b at the moment, assumes ra and dec are numpy arrays
##assumes inputs (other than year) are np.arrays

import numpy as np
from ACRastro.bprecess import bprecess
from ACRastro.precess  import precess
from ACRastro.jprecess import jprecess
###import pdb
def glactc(ra,dec,year=2000,degree=True,fk4=False,reverse=False):
	##reverse = False ##for now always false
	##db.set_trace()
	rapol  = 12.0 + 49.0/60.0 
	decpol = 27.4	
	dlon   = 123.0
	sdp    = np.sin(decpol*np.pi/180.0)
	cdp    = np.sqrt(1.0-sdp**2)
	radeg  = 180.0/np.pi
	radhrs = radeg/15.0
	if reverse == False:
	## if not in degrees convert to degrees
		if degree == False:
			ra  = ra*15.0
	##first bprecess to 1950
		if fk4 == False:
			if year != 2000:
				ra,dec = precess(ra,dec,year,2000)
			ras,decs = bprecess(ra,dec)
		if fk4 == True:
			if  year != 1950:
				ras,decs=precess(ra,dec,year,1950,fk4=True)
		ras  = ras/radeg - rapol/radhrs 
		sdec = np.sin(decs/radeg)
		cdec = np.sqrt(1.0-sdec*sdec)
		sgb  = sdec*sdp + cdec*cdp*np.cos(ras)
		gb   = radeg * np.arcsin(sgb)
		cgb  = np.sqrt(1.0-sgb*sgb)
		sine = cdec * np.sin(ras)/cgb
		cose = (sdec-sdp*sgb)/(cdp*cgb)
		gl   = dlon - radeg*np.arctan2(sine,cose)
      ## pdb.set_trace()
		ltzero=(gl<0.0).nonzero()		
		nltzero = len(ltzero)
		##pdb.set_trace()
		if nltzero > 0:
			if hasattr(gl, "__len__") == False:
				gl=gl+360
			if hasattr(gl, "__len__") == True:
				gl[ltzero]=gl[ltzero]+360.0
		##pdb.set_trace()
		return gl,gb
    
	if reverse == True:
		#pdb.set_trace()
		gb = dec
		gl = ra
		sgb = np.sin(gb/radeg)
		cgb = np.sqrt(1.0-sgb*sgb)
		sdec = sgb*sdp + cgb*cdp*np.cos((dlon-gl)/radeg)
		dec1 = radeg * np.arcsin(sdec)
		cdec = np.sqrt(1.0-sdec*sdec)
		sinf = cgb*np.sin((dlon-gl)/radeg)/cdec
		cosf = (sgb-sdp*sdec)/(cdp*cdec)
		ra1 = rapol + radhrs*np.arctan2(sinf,cosf)
		ra1 = ra1*15.0
		if fk4 == False:
			ras = ra1
			decs = dec1
			rr,dd = jprecess(ras,decs,1950)
			if year != 2000:
				rr,dd=precess(rr,dd,2000,year)
		if fk4 == True:
			if year != 1950:
				rr,dd = precess(ra1,dec1,1950,year,fk4=True)
		gt36 = np.where(rr > 360.0)
		if len(gt36) > 1:
			rr[gt36] == rr[gt36] - 360.0
		if degree == False:
			rr = rr/15.0
		##pdb.set_trace()
		return rr,dd
        