import numpy as np
import OpticalSystem
import PatchSurfaces
import Optimizer
import time
import Eyedata


rbound = 6.0
zbound = 250.0
opticx = np.arange(-6., 6.01, 0.1)
opticy = np.arange(-6., 6.01, 0.1)
pathx = np.arange(-3., 3.01, 0.1)
pathy = np.arange(-3., 3.01, 0.1)

optical_system = OpticalSystem.OpticalSystem(rbound, zbound)
optical_system.addInterface(1.0, PatchSurfaces.Sphere(22.0, 17.0, opticx, opticy), 1.5)
optical_system.addInterface(1.5, PatchSurfaces.Sphere(25.0, 20.0, opticx, opticy), 1.0)
optical_system.addInterface(1.0, PatchSurfaces.ZPlane(500.0, 250.0), 1.0)

(left_eye, right_eye) = Eyedata.load()
left_eye.plot()
print "Optimizing"

#opt = Optimizer.Optimizer(optical_system, pathx, pathy, 1.5)
#rms = opt.optFocusAtZ(215.)

#start = time.clock()
#opt.getPathCollection()
#print time.clock() - start

#print "RMS = ", rms
print "Done"
