import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys

def main():
    
    N = 50000
    uniform = np.random.randint(0,2**30,size=N)
    
    
    #Uniform
    a = 0;
    b = 1000;
    uniform_translated = uniform/2**30*b + a
    plt.hist(uniform_translated, bins=30, color = 'green', density=True, edgecolor='black', alpha = 0.4)
    plt.xlabel('Value')
    plt.ylabel('PDF')
    plt.show()
    print(" Mean is %.2f = (b-a)/2" % np.mean(uniform_translated))
    print()
    
    
    #Normal
    mu = 100000
    sigma = 100
    normal_distribution = np.zeros(N)
    for i in range(N):
        nones = bin(uniform[i]).count("1")
        std_ones = np.sqrt(30/4)
        mean_ones = 15
        normal_distribution[i] = nones*sigma/std_ones - mean_ones*sigma/std_ones + mu
   
    plt.hist(normal_distribution, bins=21, color = 'orange', density=True, edgecolor='black', alpha = 0.4)
    plt.xlabel('Value')
    plt.ylabel('PDF')    
    plt.show()
    print(" Mean is %.2f (mu)" % np.mean(normal_distribution))
    print(" std is %.2f (sigma)" % np.std(normal_distribution))
    print()
    
    
    #Exponential
    rate = 1e-4
    exp_distribution = (-np.log2(uniform)+30)/rate*np.log(2)
    plt.hist(exp_distribution, bins=30, color = 'red', density=True, edgecolor='black', alpha = 0.4)
    plt.xlabel('Value')
    plt.ylabel('PDF')    
    plt.show()
    print(" Mean is %.2f (1/lambda)" % np.mean(exp_distribution))
    print()
    
    
    #Gamma
    k = 10
    gamma_distribution = np.zeros(N)
    for i in range(N):
        value = 0
        for ki in range(k):
            value += exp_distribution[np.random.randint(0,N)]
        gamma_distribution[i] = value
    plt.hist(gamma_distribution, bins=30, color = 'blue', density=True, edgecolor='black', alpha = 0.4)
    plt.xlabel('Value')
    plt.ylabel('PDF')    
    plt.show()
    print(" Mean is %.2f (k/lambda)" % np.mean(gamma_distribution))
    print()
    
    
    #arbitrary(quantile), beta distribution as example
    """
    We can apply the the quantile function (inverse CDF) of a probability
    distribution to the uniformly distributed value in order to get a 
    variable with the specified distribution.
    """
    
    Nprecision = 100
    prob = np.arange(1,Nprecision)/Nprecision
    quantiles = (stats.beta.ppf(prob,0.5,0.5)*1e5).astype(int) #generating quantile function for Beta distribution
    print(list(quantiles))
    
    uniform = np.random.randint(0,Nprecision-1,size=N)
    beta_distribution = np.zeros(N)
    for i in range(N):
        beta_distribution[i] = quantiles[uniform[i]]
    
    
    plt.hist(beta_distribution, bins=20, color = 'purple', density=True, edgecolor='black', alpha = 0.4)
    plt.xlabel('Value')
    plt.ylabel('PDF')    
    plt.show()
    


if __name__ == '__main__':
    plt.rcParams.update({'font.size': 16})
    main()