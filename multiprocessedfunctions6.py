import numpy as np
from globalparameters import *
from scipy.interpolate import RectBivariateSpline as ReBiSpline
from datetime import datetime
import time
import copy


    #inputs route_id, route, wlkr_range, intens, xmin, xmax, ymin, ymax, Nx, Ny, stalledpos, x, y
    #outputs start, dest, pos, track, intens, stalledpos, grad

def set_up_walker_mp(route_id, route, intens, xmin, xmax, ymin, ymax, Nx, Ny, x, y, TrailPotential): 
    #start
    stalledpos = []
    t1 = time.perf_counter()
    dispersion = 0 # length away from start point walkers are allowed to spawn, measured in m

    start=np.array(route[route_id,0,:]) # commented for simplicity
    start[0]+=np.random.randint(-dispersion,dispersion+1) # adds dispersion to x
    start[1]+=np.random.randint(-dispersion,dispersion+1) # adds dispersion to y
    dest=np.array(route[route_id,1,:]) # commented for simplicity
    dest[0]+=np.random.randint(-dispersion,dispersion+1)
    dest[1]+=np.random.randint(-dispersion,dispersion+1)
    #vel=np.array([0.,0.])
    pos=np.array(start)
    track=np.zeros((wlkr_range,2))

    trailpotweight = 0.004 # weighting of trail potential over destination potential, started as 0.003, increasing this increases number of stalls
    storedtrailpotweight = trailpotweight
    #storedtrailpotweight = copy.deepcopy(trailpotweight)

#def setup_potentials_mp():

    DestinationPotential=np.zeros((Nx,Ny))
    grad=np.zeros((2,Nx,Ny))
    grad=trailpotweight*np.array(np.gradient(TrailPotential))
    DestinationPotential=-np.sqrt((dest[0]-x[:,None])**2+(dest[1]-y[None,:])**2)
    #Combine gradients
    grad+=np.array(np.gradient(DestinationPotential)[:])
    #Normalise
    #grad[:,:,:]/=(np.sqrt(grad[0,:,:]**2+grad[1,:,:]**2))
    desdirx=ReBiSpline(x,y,grad[0,:,:],s=2) # gradeint plus magnitude, Spline approximation over a rectangular mesh
    desdiry=ReBiSpline(x,y,grad[1,:,:],s=2)


#def calc_path_mp():
    
    i=0
    hist=5
    samp=5
    avpos=np.zeros((2,hist))
    success = 'Reached Goal' # qualitative info on what happened, e.g. 'Stalled'

    #Setup While loop to run until either the walker reaches the destination or the walker has passed 'wlkr_range' number of movement cycles to 
    #attempt to get there
    while (np.dot(pos-dest,pos-dest)>precision and i<wlkr_range):
    #set the postiion of the walker on its first then subsequent cycles
        
        #conditional logic saying to update the average position of the walker every 10 iterations
        if (i%samp==0): avpos[:,(i%(hist*samp))//samp]=pos[:]
        
        gradmagnitude=max(0.0001,np.sqrt(desdirx(pos[0],pos[1])**2+desdiry(pos[0],pos[1])**2))
        xi=np.array(np.random.normal(0,1,2))
        # Equation 6 in Helbing, differential in position, eliminised velocity decay components
        # gradmagnitude makes sure it is normalised, desdir not normalised
        pos[0]+= dt *(dvel * desdirx(pos[0],pos[1])/gradmagnitude +np.sqrt(2.*eps/tau)*xi[0])  # x-position vector component 
        pos[1]+= dt *(dvel * desdiry(pos[0],pos[1])/gradmagnitude +np.sqrt(2.*eps/tau)*xi[1])  # y-position vector component

        #curDir = math.atan(desdiry(pos[0],pos[1])/desdirx(pos[0],pos[1]))

        #Set the current position of the walker into the trakc array for the current iteration
        track[i,:]=pos[:]

#        if math.isnan(pos[1])==1: 
#                print ("NaN error ",pos,vel, dest)
#                break

        intens[int((pos[0]-xmin)*(Nx-1)/(xmax-xmin)),int((pos[1]-ymin)*(Ny-1)/(ymax-ymin))]+=1.
        i+=1
        if (i%(hist*samp)==0):
            meanpos=np.mean(avpos,axis=1)

            if (np.dot(pos-meanpos,pos-meanpos)<precision): #this detects 'stalls'

                stalledpos = meanpos # store position where walker is stalled
                success = 'Stalled     '
                break

    if (i==wlkr_range): #print ("Missed goal ",dest,pos)
        success = 'Missed     '
 
    #stopping condition
    now = datetime.now() # referenced elsewhere
    current_time = now.strftime("%H:%M:%S")
    t2 = time.perf_counter()
    duration = t2-t1
    duration = str("{:.2f}".format(duration))
    return start, dest, pos, track, intens, stalledpos, grad, success, current_time, duration, TrailPotential