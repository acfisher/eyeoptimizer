import numpy as np

class Ray:
    def __init__(self, start, v):
	self.start = start
	self.v = v / np.linalg.norm(v)
	self.end = np.array([])
	
    def setEndAtIntersection(self, patch_grid, zbound):
	startz = self.start[2]
	vz = self.v[2]
	
	#We will solve for t st start+t*v intesects the surface utilizing a binary search
	tlo = 0.0
	thi = (startz - zbound) / vz
	for i in range(128):
	    tmid = 0.5*(tlo + thi)
	    tpoint = self.start + tmid*self.v
	    if patch_grid.isPointBefore(tpoint):
		tlo = tmid
	    elif patch_grid.isPointAfter(tpoint):
		thi = tmid
	    else:
		break
	
	tmid = 0.5*(tlo + thi)
	self.end = self.start + tmid*self.v
	
