import numpy as np
import scipy.optimize
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Ray(object):
    def __init__(self, start, v):
        self.start = start
        self.v = v / np.linalg.norm(v)

    def getIntersection(self, patch_grid, zbound):
        startz = self.start[2]
        vz = self.v[2]

        #We will solve for t st start+t*v intesects the surface utilizing a binary search
        tlo = 0.0
        thi = (zbound - startz) / vz
        for i in range(128):
            tmid = 0.5*(tlo + thi)
            tpoint = self.start + tmid*self.v
            if patch_grid.isPointInRange(tpoint[0], tpoint[1]):
                if patch_grid.isPointBefore(tpoint):
                    tlo = tmid
                elif patch_grid.isPointAfter(tpoint):
                    thi = tmid
                else:
                    break
            else:
                return []
        
        tmid = 0.5*(tlo + thi)
        return self.start + tmid*self.v

class Path(object):
    def __init__(self, start, v):
        self.rays = [Ray(start, v)]
        self.isOutOfBounds = False
        
    def propagateThroughSystem(self, optical_system):
        for zone in range(len(optical_system.interfaces)):
            if not self.isOutOfBounds:
                interface = optical_system.interfaces[zone]
                n_before = interface.nBefore
                patch_grid = interface.patchGrid
                n_after = interface.nAfter
                p = self.rays[-1].getIntersection(patch_grid, optical_system.zbound)
                if (len(p) == 3):
                    v_in = self.rays[-1].v
                    v_normal = -patch_grid.getNormal(p[0],p[1])
                    c = -np.dot(v_normal, v_in)
                    nfrac = n_before / n_after
                    arg = 1. - nfrac**2. * (1. - c**2.)
                    if arg >= 0.0:
                        v_out = nfrac*v_in + (nfrac*c + math.sqrt(arg))*v_normal
                        self.rays.append(Ray(p, v_out))
                    else:
                        print "Lost ray"
                        self.isOutOfBounds = True
                else:
                    print "Ray out of bounds"
                    self.isOutOfBounds = True
                    
class PathCollection(object):
    def __init__(self, starter_paths):
        self.paths = starter_paths
        
    def propagateThroughSystem(self, optical_system):
        for path in self.paths:
            path.propagateThroughSystem(optical_system)
            
    def getSpotRMSAtZ(self, spotz):
        n = float(len(self.paths))
        norm_squares_sum = 0.0
        for path in self.paths:
            if not path.isOutOfBounds:
                rayz = [r.start[2] for r in path.rays]
                i = np.searchsorted(rayz,spotz) - 1
                if i >= len(rayz) - 1:
                    print "z out of bounds for RMS calculatipm"
                    return 1e20
                p0 = path.rays[i].start
                p1 = path.rays[i+1].start
                v = p1 - p0
                spotz_frac = (spotz - p0[2]) / (p1[2] - p0[2])
                p_at_z = p0 + spotz_frac*v
                norm_squares_sum += (p_at_z[0]**2 + p_at_z[1]**2) / n
        return math.sqrt(norm_squares_sum)

    def findBestFocusZ(self):
        zlo = np.max([path.rays[-2].start[2] for path in self.paths if not path.isOutOfBounds])
        zhi = np.min([path.rays[-1].start[2] for path in self.paths if not path.isOutOfBounds])                   
        result = scipy.optimize.minimize_scalar(self.getSpotRMSAtZ, method='Bounded', bounds=(zlo, zhi))
        return result.x
        
    def plot(self):
        fig = plt.figure()
        fig.add_subplot(111, projection='3d')
        for path in self.paths:
            x = [ray.start[0] for ray in path.rays]
            y = [ray.start[1] for ray in path.rays]
            z = [ray.start[2] for ray in path.rays]
            plt.plot(x, y, z, "r+-")
        plt.show()