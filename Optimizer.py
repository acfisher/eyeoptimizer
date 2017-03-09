import numpy as np
import scipy
import RayTools

class Optimizer(object):
    def __init__(self, optical_system, pathx, pathy, zoff_bound):
        self.opticalSystem = optical_system
        self.pathx = np.array(pathx)
        self.pathy = np.array(pathy)
        self.zoffBound = zoff_bound
        
    def optFocusAtZ(self, zfocus):
        self.zfocus = zfocus
        phi = np.zeros(np.size(self.opticalSystem.interfaces[0].patchGrid.z))
        bnds = [(-self.zoffBound, self.zoffBound) for i in range(len(phi))]
        opts = {}
        opts["disp"] = True
        result = scipy.optimize.minimize(self.eval, phi, method="L-BFGS-B", bounds=bnds,
                                         options=opts)
        return self.eval(result.x)
        
        
    def getPathCollection(self):
        #initilize the path collection
        paths = []
        for x in self.pathx:
            for y in self.pathy:
                paths.append(RayTools.Path([x, y, 0.0], [0.0, 0.0, 1.0]))
        path_collection = RayTools.PathCollection(paths)
        path_collection.propagateThroughSystem(self.opticalSystem)  
        return path_collection          
        
    def eval(self, phi):
        zoff = np.reshape(phi, np.shape(self.opticalSystem.interfaces[0].patchGrid.z))
        self.opticalSystem.interfaces[0].patchGrid.setZOff(zoff)
        path_collection = self.getPathCollection()
        return path_collection.getSpotRMSAtZ(self.zfocus)