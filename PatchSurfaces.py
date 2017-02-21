import numpy as np

class Patch:
    def __init__(self, x0, y0, x1, y1, z00, z01, z10, z11):
        dx = x1 - x0
        dy = y1 - y0

        #solve fot the parameters of z = ax + by + cxy + d
        self.c = (z00 + z11 - z01 - z10) / (dx*dx)
        self.a = (z10 - z00) / dx - y0 * self.c
        self.b = (z01 - z00) / dy - x0 * self.c
        self.d = z00 - self.a*x0 - self.b*y0 - self.c*x0*y0

    def getZ(self, x, y):
        return self.a * self.x + self.b * self.y + self.c*self.x*self.y + self.d

    def getNormal(self, x0, y0):
        #The tangent plane satisfies
        # z - z0 = fx(x0,y0)(x-x0) + fy(x0,y0)(y-y0)
        fx = self.a + self.c*y0
        fy = self.b + self.c*x0
        n = np.array([fx, fy, -1])
        return n / np.linalg.norm(n)

    def isPointBefore(self, p):
        patchZ = self.getZ(p[0], p[1])
        return p[2] < patchZ
        
    def isPointAfter(self, p):
        patchZ = self.getZ(p[0], p[1])
        return p[2] > patchZ


class PatchGrid:
    def __init__(self, x, y, z):
        self.nx = len(x)
        self.ny = len(y)
        self.grid = [[Patch(x[i],y[j],x[i+1],y[j+1],z[i][j],z[i][j+1],z[i+1][j],z[i+1][j+1])
                      for j in range(self.ny-1)]
                     for i in range(self.nx-1)]
        
    def getZ(self,x0,y0)
        i = np.searchsorted(x,x0)
        j = np.searchsorted(y,y0)
        return self.grid[i][j].getZ(x0, y0)
        
    def getNormal(self, x0, y0):
        i = np.searchsorted(x,x0)
        j = np.searchsorted(y,y0)
        return self.grid[i][j].getNormal(x0, y0)
        
    def isPointBefore(self, p):
        i = np.searchsorted(x,p[0])
        j = np.searchsorted(y,p[1])
        return self.grid[i][j].isPointBefore(p)
        
    def isPointAfter(self, p):
        i = np.searchsorted(x,p[0])
        j = np.searchsorted(y,p[1])
        return self.grid[i][j].isPointAfter(p)
        

p = Patch(0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0)
print p.getNormal(0.5, 0.5)
