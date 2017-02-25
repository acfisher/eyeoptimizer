import numpy as np
import math

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
	

class RayChain:
    def __init__(self, start, v, zbound):
        self.rays = [Ray(start, v)]
        self.zbound = zbound
        
    def propagateThroughSurface(self, patch_grid, n_before, n_after):
        self.rays[-1].setEndAtIntersection(patch_grid, self.zbound)
        p = self.rays[-1].end
        v_in = self.rays[-1].v
        v_normal = patch_grid.getNormal(p[0],p[1])
        
        c = -np.linalg.dot(v_normal, v_in)
        r = n_before / n_after
        v_out = r*v_in + (r*c + math.sqrt(1. - r**2. * (1. - c**2.)))
        self.rays.append(Ray(p, v_out))
        