import numpy as np
import matplotlib.pyplot as plt
import sys
import random as rd


N = 50
boxsize = 128
Tend = 15
coarsegraining = 2 #we split the box into coarsegraining**2 because we are in 2D

def main():
    
    Nsimul = 5000
    positions = np.random.randint(low=1, high=boxsize, size=(Nsimul,N,2))
    entropy_list = []
    for ni in range(Nsimul):
        entropy_list.append(comppute_entropy(positions[ni,:,:], coarsegraining))
        
    Smax = np.log(coarsegraining**2)
    plt.hist(entropy_list, density = True, color = 'blue', alpha=0.5, bins = 20, edgecolor = 'black')
    plt.axvline(x=Smax, color = 'black', alpha = 0.5, linestyle = '--')
    plt.show()
    
    
def comppute_entropy(positions, coarsegraining):
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
    entropy = -np.sum(pis_*np.log(pis_))
        
    return entropy

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
        

if __name__ == '__main__':
    plt.rcParams.update({'font.size': 16})
    main()