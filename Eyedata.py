import matplotlib.pyplot as plt
from scipy import misc
import numpy as np
import PatchSurfaces


class ColorBar(object):
    def __init__(self, imgname, num_colors, vhi):
        img = misc.imread(imgname)       
        R = img[:,1,0]
        G = img[:,1,1]
        B = img[:,1,2]
        
        scaleh = float(len(R))
        cenx = [scaleh / float(num_colors*2) + float(i)*scaleh / float(num_colors) for i in range(num_colors)]
        cenR = [R[int(cenx[i])] for i in range(num_colors)]
        cenG = [G[int(cenx[i])] for i in range(num_colors)]
        cenB = [B[int(cenx[i])] for i in range(num_colors)]
        val = [vhi - (cenx[i] / scaleh)*vhi for i in range(num_colors)]
        
        self.R = cenR
        self.G = cenG
        self.B = cenB
        self.value = val
    
    def get_color_value(self,r, g, b):
        min_dist = 1e40
        min_i = -1
        for i in range(len(self.R)):
            dist = ((self.R[i] - r)**2.0 + (self.G[i] - g)**2.0 + (self.B[i] - b)**2.0)**0.5
            if (dist < min_dist):
                min_dist = dist
                min_i = i
        return self.value[min_i]
        
    def get_image_values(self,imgname,num_samples):
        img = misc.imread(imgname)
        R = img[:,:,0]
        G = img[:,:,1]
        B = img[:,:,2]
        dims = R.shape
        sample_r = int(0.5*float(np.min(dims)) / float(num_samples-1))
        val = np.zeros([num_samples,num_samples])
        for isam in range(num_samples):
            for jsam in range(num_samples):
                i = int(float(dims[0] - 1) * float(isam) / float(num_samples - 1))
                j = int(float(dims[1] - 1) * float(jsam) / float(num_samples - 1))
                ilo = max([0,i-sample_r])
                ihi = min([dims[0]-1,i+sample_r])
                jlo = max([0,j-sample_r])
                jhi = min([dims[1]-1,j+sample_r])
                val[isam,jsam] = 0.0
                count = 0.0
                for i in range(ilo,ihi+1):
                    for j in range(jlo,jhi+1):
                        cv = self.get_color_value(R[i,j],G[i,j],B[i,j])
                        if True:
                            val[isam,jsam] += cv
                            count += 1.0
                val[isam,jsam] /= count
        return val

def load():
    color_bar_max = 0.4
    color_bar_quant = 24
    left_contact_r = 8.65   #mm
    right_contact_r = 9.0   #mm
    eyebox_len = 6.0 / 2.0**0.5     #mm (6mm diameter scan?)
    eye_x = np.array([eyebox_len*float(i)/50.0 - eyebox_len/2.0 for i in range(51)])
    eye_y = eye_x
    
    cb = ColorBar("eyedata/colorbar.png", color_bar_quant, color_bar_max)
    left_contact_dist = cb.get_image_values("eyedata/left.png", 51)
    right_contact_dist = cb.get_image_values("eyedata/right.png", 51)

    left_eye_r = left_contact_r - left_contact_dist
    right_eye_r = right_contact_r - right_contact_dist
    left_eye_z = np.zeros([51,51])
    right_eye_z = left_eye_z
    for i in range(51):
        for j in range(51):
            #r^2 = z^2 + xy^2
            eye_xy = (eye_x[i]**2.0 + eye_y[j]**2.0)**0.5
            left_eye_z[i,j] = (left_eye_r[i,j]**2.0 - eye_xy**2.0)**0.5
            right_eye_z[i,j] = (right_eye_r[i,j]**2.0 - eye_xy**2.0)**0.5
    
    left_eye_z = left_eye_z[25,25] - left_eye_z
    right_eye_z = right_eye_z[25,25] - right_eye_z  
    
    left_pg = PatchSurfaces.PatchGrid(eye_x, eye_y, left_eye_r)
    right_pg = PatchSurfaces.PatchGrid(eye_x, eye_y, right_eye_z)
    
    return (left_pg, right_pg)
