import sys
import numpy as np
from qiskit import QuantumProgram
from random import randint


def to_binary(N,n_bit):
    
    Nbin = np.zeros(n_bit, dtype=bool)
    for i in range(1,n_bit+1):
        bit_state = (N % (2**i) != 0)
        if bit_state:
            N -= 2**(i-1)
        
        Nbin[n_bit-i] = bit_state
        
    return Nbin




def quantum_period(a,N):
    
    n_bit = 5 #number of availables bits in the IBMQ processor
    if N >= 2**n_bit:
        print ("    Error: the number N =", N, "is too big, should be smaller than 2^" + str(n_bit),"=", 2**n_bit)
        print("\n\n")
        sys.exit(0)
        

    
    
  #---------------------------------------------------------------------------#
  #------------------------------ Quantum part -------------------------------#
  #---------------------------------------------------------------------------#
    
    print("  Searching the period for N =", N, "and a =", a)
    
    qp = QuantumProgram()
    qr = qp.create_quantum_register('qr',n_bit)   #working register
    cr = qp.create_classical_register('cr',n_bit) #register to store our measurement
    qc = qp.create_circuit('Period',[qr],[cr])
    
    
        
  
    s0 = randint(1, N-1) 
    sbin = to_binary(s0,n_bit)     # Decompose s0 in binary unit for our quantum algorithm
    print("\n      Statrting at \n      s =", s0, "=", sbin)
    
    #initialize the input with s
    for i in range(0,n_bit):
        if sbin[n_bit-i-1]:
            qc.x(qr[i])
            
    s = s0
    r=-1   
    
    # Apply the modular multiplication transformation until we come back to the same initial number s
    while np.logical_or(s != s0, r <= 0):
        
        r+=1
        qc.measure(qr, cr) 
        modular_multiplication(qc,qr,cr,a,N)
        result = qp.execute('Period', shots=10)
        P = result.get_counts('Period')
        
        results = [[],[]]
        for k,v in P.items(): #the result should be deterministic but there might be some quantum calculation error so we take the most reccurent output
            results[0].append(k)
            results[1].append(int(v))
        
        index = np.argmax(np.array(results[1]))
        s_str = str(results[0][index])
        
        s = int(s_str, 2)
        print("       ",s_str[::-1])
        
        #sbin = 
        
        
        
            
    print("\n      Found period r =", r)
    return r
       
    


def modular_multiplication(qc,qr,cr,a,N):
    """
    apply the unitary operator that implements the modular multiplication function x -> a*x(modN)
    Only work for the particular case x -> 7*x(mod15)
    """
    
    for i in range(0,3): 
        qc.x(qr[i])
        
    qc.cx(qr[2],qr[1]);
    qc.cx(qr[1],qr[2]);
    qc.cx(qr[2],qr[1]);
    
    qc.cx(qr[1],qr[0]);
    qc.cx(qr[0],qr[1]);
    qc.cx(qr[1],qr[0]);
    
    qc.cx(qr[3],qr[0]);
    qc.cx(qr[0],qr[1]);
    qc.cx(qr[1],qr[0]);
    
    
    
    
    
    
if __name__ == '__main__':
    
    a = 7
    N = 15
    r = quantum_period(a,N)