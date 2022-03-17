import numpy as np
from globalparameters import *

#def calc_tr_new_mp_2(i,j,TrailPotential,z,Weight,subexpdist):
#
#    TrailPotential[:,:]=sg.convolve2d(z[:,:]*Weight[:,:],subexpdist[:,:],mode="same")  # 2D convolution#
#
#    TrailPotential[i][j]=sg.convolve2d(z[:,:]*Weight[:,:],subexpdist[:,:],mode="same")  # 2D convolution
#
#    return TrailPotential

def calc_tr(xi,TrailPotential,expdist,z,Weight,Nx,Ny):
    rowval = np.empty((1,Ny))
    for yi in range(Ny):
        rowval[0,yi]=np.sum(expdist[Nx-1-xi:2*Nx-1-xi,Ny-1-yi:2*Ny-1-yi]*z[:,:]*Weight[:,:])
    
    return xi,rowval