import PatchSurfaces

class Interface(object):
    def __init__(self, n_before, patch_grid, n_after):
        self.nBefore = n_before
        self.patchGrid = patch_grid
        self.nAfter = n_after
        
    def plot(self):
        self.patchGrid.plot()

class OpticalSystem(object):
    def __init__(self, rbound, zbound):
        self.rbound = rbound
        self.zbound = zbound
        self.interfaces = []
        
    def addInterface(self, n_before, patch_grid, n_after):
        self.interfaces.append(Interface(n_before, patch_grid, n_after))
        