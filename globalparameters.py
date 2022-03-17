#parameters
#t_track=25. # Track decay time - after 50 walkers ignore a trail, it decays by 1/e
wlkr_range = 20000
dt=0.1  # dt per time step, continuous markings every dt metres
dvel=1. # desired walker velocity in m/s
tau=5.
# isigma=0.4 # trail potential moved back to the main code
#trailpotweight = 0.004 # weighting of trail potential over destination potential, started as 0.003, increasing this increases number of stalls
#storedtrailpotweight = trailpotweight
conv_thresh=10.e-4
precision=1.**2 #distance to target.
eps=0.025 #random motion contribution, same for all

# trailpotweight was moved to mpf2