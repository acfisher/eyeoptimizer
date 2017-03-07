import numpy as np
import OpticalSystem
import PatchSurfaces
import RayTools

rbound = 10.0
zbound = 100.0
samplex = np.arange(-2., 2.01, 0.1)
sampley = np.arange(-2., 2.01, 0.1)

optical_system = OpticalSystem.OpticalSystem(rbound, zbound)
optical_system.addInterface(1.0, PatchSurfaces.Sphere(25.0, 20.0, np.arange(-10.,10.01, 0.05), np.arange(-10.,10.01,0.05)), 1.5)
optical_system.addInterface(1.5, PatchSurfaces.ZPlane(500.0, 90.0), 1.0)

paths = []
for x in np.arange(-5.0, 5.01, 0.5):
    for y in np.arange(-5.0, 5.01, 0.5):
        paths.append(RayTools.Path([x, y, 0.0], [0.0, 0.0, 1.0]))
path_collection = RayTools.PathCollection(paths)
path_collection.propagateThroughSystem(optical_system)
path_collection.plot()

focusz = path_collection.findBestFocusZ()
print "Best Focus:"
print "z = %f" % (focusz)
print "rms = %f" % (path_collection.getSpotRMSAtZ(focusz))
print "Original rms = %f" % (path_collection.getSpotRMSAtZ(0.0))
