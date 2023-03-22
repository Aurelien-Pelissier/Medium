from math import log
from Quantum import quantum_period


"""
This code is a simplified implementation of the Shor's Algorithm for N=15
The code is  written to run on a 5Qbit IBMQ quantum processor
"""


def main():

    
    print ("\n")
    print ("===========================================")
    print ("             SHOR'S  ALGPRITHM")
    print ("===========================================")
    print ("\n")
    
    
    #N is the prime factor to be factorized, 
    #    (Currently, the IBMQ processor has 5qbits, 
    #     So the number to be factorized should be less 2^5 = 32)
    
    N = 15
          
    if Check(N):
        p1, p2 = Shor(N)
	
    
        

def Check(N):

    if N % 2 == 0:
        print ("2 is a trivial factor")
        return False
        
    for k in range(2,int(log(N,2))): #log2(N)
        if pow(N,(1/k)).is_integer():
            print ("N =", pow(N,(1/k)), '^', k)
            return False
    
    return True


def gcd(a, b):   #Compute the GCD with Euclide algorithm
    while b:
        a, b = b, a%b
    return a	
	
	
	
def Shor(N):

    while True:
    
      #1) pick a random number a<N
        #a = randint(1, N-1) 
        a = 7   
    
      #2) check for the GCD(a,N)
        p = gcd(a,N)
        if p != 1:  # We found a nontrivial factor
            p1 = p
            p2 = N/p
            break
        
      #3) Compute the periode r      
        r = quantum_period(a,N)  #Quantum part of the algorithm
        if r % 2 == 0 :
            if a**(r/2) % N != -1:  #If r is a goof period, we found prime factors   
                p1 = gcd(a**(r/2)-1,N)
                p2 = gcd(a**(r/2)+1,N)
                break
                
    print ("\n  N =", int(p1), "*", int(p2))
    return p1, p2
        
        
if __name__ == '__main__':
    main()
        