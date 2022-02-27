import numpy as np
import matplotlib.pyplot as plt
import sys
import random as rd

"""
    We take N = 100 particles of identical mass m = 1, and we
    initialize them in the lower left corner of size 8 × 8, within the
    full box of size 16 × 16 with periodic boundary conditions.
    The initial velocity of each particle is randomly drawn from
    the normal distribution. Particles interact via a Lennard-Jones
    potential
    
    u(r) = ε * ( (rm/r)^12 - 2*(rm/r)^6 )
    
    
    where we took ε = 1/120 and rm = 1 as parameters of the
    model, and r denotes the distance between each particle.
    Particles are then evolved via a velocity Verlet algorithm with
    time step 10−4. 
    
    1. Calculate the force (and therefore acceleration) on the particle
    2. Find the position of the particle after some timestep
    3. Calculate the new forces and accelerations
    4. Determine a new velocity for the particle, based on the average acceleration at the current and new positions
    5. Overwrite the old acceleration values with the new ones,  
    6. Repeat

    Entropy is calculated at each time step as:
        
        S = 0
    
    As particles and heat spread from one region to the other,
    entropy S grows from the thermodynamic entropy of the
    first bin to the thermodynamic entropy of the full system.
    
    [ref] Šafránek, Dominik, Anthony Aguirre, and J. M. Deutsch. 
         "Classical dynamical coarse-grained entropy and comparison with
          the quantum version." Physical Review E 102.3 (2020): 032106.
    
"""

Deltat = 1e-2
mass = 1
N = 100
boxsize = 128
Tend = 15
coarsegraining = 2 #we split the box into coarsegraining**2 because we are in 2D
rd.seed(15)


def main():
    
    positions = np.random.randint(low=1, high=boxsize/2, size=(N,2))
    velocities = np.random.randint(low=1, high=10, size=(N,2))

    
    #print(positions)
    #print(velocities)
    
    entropy = []
    t = 0
    ti = 0
    while t<Tend:
        
        #count number of particles in each boxes
        pis = np.zeros(coarsegraining**2)
        for bix in range(coarsegraining):
            for biy in range(coarsegraining):
                ci = bix*coarsegraining + biy
                x1 = boxsize*bix/coarsegraining
                x2 = boxsize*(bix+1)/coarsegraining
                y1 = boxsize*biy/coarsegraining
                y2 = boxsize*(biy+1)/coarsegraining
                nwherex = np.where(np.logical_and(positions[:,0]>x1, positions[:,0]<x2))[0]
                nwherey = np.where(np.logical_and(positions[:,1]>y1, positions[:,1]<y2))[0]
                nbi = len(intersection(list(nwherex), list(nwherey)))
                pis[ci] = nbi/N
        
        pis_ = pis[pis>0]
        S = -np.sum(pis_*np.log(pis_))
        entropy.append(S)
        
        if ti%100 == 0:
            plt.figure(figsize = (6,6))
            plt.scatter(positions[:,0],positions[:,1], color = 'red', edgecolor = 'black', s=150)
            plt.axvline(x=boxsize/2, color = 'black', linestyle = '--', linewidth = 2, alpha = 0.5)
            plt.axhline(y=boxsize/2, color = 'black', linestyle = '--', linewidth = 2, alpha = 0.5)
            plt.xlim(0,boxsize)
            plt.ylim(0,boxsize)
            plt.xticks([],[])
            plt.yticks([],[])
            plt.title("t = %.0f s" % (t))
            plt.show()
            
        accelerations = get_accelerations(positions)
        newpositions = np.zeros((N,2))
        newvelocities = np.zeros((N,2))
        for ni in range(N):
            x = positions[ni,0]
            y = positions[ni,1]
            vx = velocities[ni,0]
            vy = velocities[ni,1]
            ax = accelerations[ni,0]
            ay = accelerations[ni,1]
            newpositions[ni,:] = update_pos(x, y, vx, vy, ax, ay, Deltat)
            newvelocities[ni,:] = update_velo(vx, vy, ax, ay, Deltat)
        positions = newpositions
        velocities = newvelocities
        
        t  += Deltat
        ti += 1
     
    Smin = np.min(entropy)
    Smax1 = np.max(entropy)
    Smax2 = np.log(coarsegraining**2)
    
    print(Smax1,Smax2)
    Smax = Smax2
    
    time_axis = np.arange(len(entropy))*Deltat
    plt.plot(running_mean(time_axis, 20), running_mean(entropy, 20), color = 'blue', linewidth = 3)
    plt.axhline(y=Smin, color = 'gray', linestyle = '--', linewidth = 3)
    plt.axhline(y=Smax, color = 'gray', linestyle = '--', linewidth = 3)
    plt.xlim(0,Tend)
    plt.yticks([Smin,Smax],['$S_0$','$S_{eq}$'])
    plt.ylabel('Entropy S')
    plt.xlabel('Time [s]')
    plt.show()
    
    
def lj_force(r, epsilon, rm):
    
    """
    u(r) = ε * ( (rm/r)^12 - 2*(rm/r)^6 )
    
    
    where we took ε = 1/120 and rm = 1 as parameters of the
    model, and r denotes the distance between each particle.
    Particles are then evolved via a velocity Verlet algorithm with
    time step 10−4.
    """    
    
    
    lj_force = epsilon * ( np.power(rm/r, 12) - 2*np.power(rm/r, 6))
    return lj_force

def get_accelerations(positions):
    accel_x = np.zeros((N, N))
    accel_y = np.zeros((N, N))
    for i in range(0, N - 1):
        for j in range(i+1, N):
            rx = positions[j,0] - positions[i,0]
            ry = positions[j,1] - positions[i,1]
            rmag = max(np.sqrt(rx*rx + ry*ry),0.01)
            force_scalar = lj_force(rmag, 1/120, 1)
            force_x = force_scalar * rx / rmag
            force_y = force_scalar * ry / rmag
            accel_x[i, j] = force_x / mass #eV Å-1 amu-1
            accel_y[i, j] = force_y / mass #eV Å-1 amu-1
            # appling Newton's third law
            accel_x[j, i] = - force_x / mass
            accel_y[j, i] = - force_y / mass
            
    accelerations = np.concatenate((np.sum(accel_x, axis=0).reshape(-1,1), np.sum(accel_y, axis=0).reshape(-1,1)), axis = 1)
    return accelerations

def update_pos(x, y, vx, vy, ax, ay, dt):
    newpos_x = x + vx * dt + 0.5 * ax * dt * dt
    newpos_y = y + vy * dt + 0.5 * ay * dt * dt
    newpos = [newpos_x % boxsize, newpos_y % boxsize]
    return np.array(newpos)

def update_velo(vx, vy, ax, ay, dt):
    newvelo_x = vx + ax * dt
    newvelo_y = vy + ay * dt
    newvelo = [newvelo_x,newvelo_y]
    return np.array(newvelo)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def running_mean(x, N):
    running_mean = np.zeros(len(x))
    for i in range(len(x)):
        if i<N:
            running_mean[i] = np.mean(x[:i+1])
        else:
            running_mean[i] = np.mean(x[i-N:i+1])
            
    return running_mean
        

if __name__ == '__main__':
    plt.rcParams.update({'font.size': 19})
    main()