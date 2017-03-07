import PatchSurfaces
import math
import unittest
import numpy as np


tiny = 1e-12

def testPatchCornerValues():
    success = True
    pat = PatchSurfaces.Patch(0.,0.,1.,1.,1.,1.5,0.5,3.0)
    success = success and math.fabs(pat.getZ(0.0, 0.0) - 1.0) < tiny
    success = success and math.fabs(pat.getZ(0.0, 1.0) - 1.5) < tiny
    success = success and math.fabs(pat.getZ(1.0, 0.0) - 0.5) < tiny
    success = success and math.fabs(pat.getZ(1.0, 1.0) - 3.0) < tiny
    return success
    
def testNormalOnPlanes():
    success = True
    pat = PatchSurfaces.Patch(0.,0.,1.,1.,0.,0.,0.,0.)
    n = pat.getNormal(0.5, 0.5)
    n2 = pat.getNormal(0.7, 0.5) 
    n3 = pat.getNormal(0.1, 0.9)
    success = success and len(n) == 3
    success = success and math.fabs(n[0]) < tiny
    success = success and math.fabs(n[1]) < tiny
    success = success and math.fabs(n[2] + 1.0) < tiny
    success = success and np.linalg.norm(n - n2) < tiny
    success = success and np.linalg.norm(n - n3) < tiny
    
    pat = PatchSurfaces.Patch(0.,0.,1.,1.,0.,0.,1.,1.)
    n = pat.getNormal(0.5, 0.5)
    success = success and len(n) == 3
    success = success and math.fabs(n[0] - (2.**.5 / 2.)) < tiny
    success = success and math.fabs(n[1]) < tiny
    success = success and math.fabs(n[2] + (2.**.5 / 2.)) < tiny
    
    pat = PatchSurfaces.Patch(0.,0.,1.,1.,0.,1.,0.,1.)
    n = pat.getNormal(0.5, 0.5)
    success = success and len(n) == 3
    success = success and math.fabs(n[0]) < tiny
    success = success and math.fabs(n[1] - (2.**.5 / 2.)) < tiny
    success = success and math.fabs(n[2] + (2.**.5 / 2.)) < tiny
    return success
    
def testSphericalSurface():
    success = True
    z0 = 100.
    r = 50.
    max_dist_error = 0.0
    max_normal_error = 0.0
    sphere = PatchSurfaces.Sphere(z0, r, np.arange(-15.0, 15.01, 0.1), np.arange(-15.0, 15.01, 0.1))    
    for x in np.arange(-10.0, 10.01, 0.05):
        for y in np.arange(-10.0, 10.01, 0.05):
            z = sphere.getZ(x, y)
            dist_error = math.fabs(x**2. + y**2. + (z-z0)**2. - r**2.)
            if dist_error > max_dist_error:
                max_dist_error = dist_error
                
            p = np.array([x, y, z])
            pcen = np.array([0.0, 0.0, z0])
            n = sphere.getNormal(x, y)
            n = n / np.linalg.norm(n)
            n_exact = (p - pcen) / np.linalg.norm(p - pcen)
            dot = np.clip(np.dot(n, n_exact), -1.0, 1.0)
            normal_error = math.acos(dot) * 180.0 / math.pi
            if normal_error > max_normal_error:
                max_normal_error = normal_error
    success = success and max_dist_error < 1e-2
    success = success and max_normal_error < 1e-1
    if not success:
        print max_dist_error, max_normal_error
    return success
    
def testGetPatchIJ():
    success = True
    pg = PatchSurfaces.PatchGrid([-2.0, 1.0, 3.0], [-20.0, 0.0, 5.0], np.ones((3,3)))
    success = success and pg.getPatchIJ(-3., -5.) == (-1, 0)
    success = success and pg.getPatchIJ(-1.99, -10.) == (0, 0)
    success = success and pg.getPatchIJ(1.1, 1.0) == (1, 1)
    success = success and pg.getPatchIJ(2.99, 6.0) == (1, 2)
    
    return success
    
def main():
    print "testPatchCornerValues:  ", testPatchCornerValues()
    print "testNormalOnPlanes:  ", testNormalOnPlanes()
    print "testSphericalSurface:  ", testSphericalSurface()
    print "testGetPatchIJ:  ", testGetPatchIJ()
    

main()