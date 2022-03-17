import multiprocessing
from scipy import signal as sg

def calc_tr_new_mp_2(xi,yi,TrailPotential,z,Weight,subexpdist):
    #total_cores = multiprocessing.cpu_count()
    #jstart = int(((core-1)/total_cores)*len(z))
    #jend = int((core/total_cores)*len(z)-1)

    # Section = []
    # Section = sg.convolve2d(z[jstart:jend+1,:]*Weight[jstart:jend+1,:],subexpdist[:,:],mode="same")  # 2D convolution

    #TrailPotential[jstart:jend,:] = sg.convolve2d(z[jstart:jend,:]*Weight[jstart:jend,:],subexpdist[:,:],mode="same")  # 2D convolution
    
    TrailPotential = sg.convolve2d(z*Weight,subexpdist[:,:],mode="same")  # 2D convolution

    #TrailPotential[:,:]=sg.convolve2d(z[:,:]*Weight[:,:],subexpdist[:,:],mode="same")  # 2D convolution

    return xi,yi,TrailPotential