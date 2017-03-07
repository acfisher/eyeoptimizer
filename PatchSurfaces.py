import numpy as np
import math

class Patch(object):
    def __init__(self, x0, y0, x1, y1, z00, z01, z10, z11):        
        dx = x1 - x0
        dy = y1 - y0

        #solve fot the parameters of z = ax + by + cxy + d
        self.c = (z00 + z11 - z01 - z10) / (dx*dx)
        self.a = (z10 - z00) / dx - y0 * self.c
        self.b = (z01 - z00) / dy - x0 * self.c
        self.d = z00 - self.a*x0 - self.b*y0 - self.c*x0*y0

    def getZ(self, x, y):
        return self.a*x + self.b*y + self.c*x*y + self.d

    def isPointBefore(self, p):
        return p[2] < self.getZ(p[0], p[1])

    def isPointAfter(self, p):
        return p[2] > self.getZ(p[0], p[1])

    def getNormal(self, x0, y0):
        #The tangent plane satisfies
        # z - z0 = fx(x0,y0)(x-x0) + fy(x0,y0)(y-y0)
        fx = self.a + self.c*y0
        fy = self.b + self.c*x0
        n = np.array([fx, fy, -1.])
        return n / np.linalg.norm(n)


class PatchGrid(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.grid = [[Patch(x[i],y[j],x[i+1],y[j+1],z[i][j],z[i][j+1],z[i+1][j],z[i+1][j+1])
                      for j in range(len(y)-1)]
                     for i in range(len(x)-1)]
        
    def getZ(self,x0,y0):
        (i,j) = self.getPatchIJ(x0, y0)
        return self.grid[i][j].getZ(x0, y0)
        
    def getNormal(self, x0, y0):
        (i,j) = self.getPatchIJ(x0, y0)
        return self.grid[i][j].getNormal(x0, y0)

    def isPointInRange(self, x0, y0):
        return x0 >= self.x[0] and x0 <= self.x[-1] and y0 >= self.y[0] and y0 <= self.y[-1] 
        
    def getPatchIJ(self, x0, y0):
        return (np.searchsorted(self.x,x0) - 1, np.searchsorted(self.y,y0) - 1)
        
    def isPointBefore(self, p):
        (i, j) = self.getPatchIJ(p[0], p[1])
        return self.grid[i][j].isPointBefore(p)
        
    def isPointAfter(self, p):
        (i,j) = self.getPatchIJ(p[0], p[1])
        return self.grid[i][j].isPointAfter(p)
        
class ZPlane(PatchGrid):
    def __init__(self, rbound, z):
        x = [-rbound, rbound]
        y = [-rbound, rbound]
        z = [[z,z], [z,z]]
        super(ZPlane, self).__init__(x, y, z)
        
class Sphere(PatchGrid):
    def __init__(self, z0, r0, x, y):
        #x^2 + y^2 + (z-z0)^2 = r0^2
        z = []
        for i in range(len(x)):
            z.append([])
            for j in range(len(y)):
                z[i].append(z0 - math.sqrt(r0**2. - x[i]**2. - y[j]**2.))
        super(Sphere, self).__init__(x, y, z)
