import sys
import numpy as np
from random import randint

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction
plt.rcParams.update({'font.size': 18})

#%matplotlib inline

from IPython import get_ipython

"""
  Qiski notes:
    qc.u1(lambda) is now qc.p(lambda)
    qc.u2(phi, lambda) is now qc.u(pi/2, phi, lambda)
    qc.u3(theta, phi, lambda) is now qc.u(theta, phi, lambda)
    
    -> Same for controlled versions cu1, cu2, cu3
"""


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
    
    
    n0 = int(np.log2(N) + 1) #number of qbits in the input register (n0 ~ log2(N) )
    n = 2*n0  #number of qbits in the output register (n = 2*n0 )
    qc = QuantumCircuit(n0+n, n) #QuantumCircuit(n_QuantumRegister, n_ClassicalRegister)
    #q[------n------][---n0---] -> c[------n------]
    #output register is [0,n], input is [n+1,n+n0]

    
    #Apply Hadamard Gate to all of the qubit in the output register
    for q in range(n):
        qc.h(q)  
        
    #Initialize the input register with the last qubit at state |1⟩ 
    qc.x(n+n0-1)
    
    #Apply the controled modular exponentiation gates Ua, Ua², Ua⁴, Ua⁸, .., Ua^(2^(2n-1)) to the input register.
    for q in range(n): 
        #cmul_amodN_apply(qc, [q] + [i+n for i in range(n0)],a, 2**q,N)
        qc.append(cmul_amodN(a, 2**q,N), [q] + [i+n for i in range(n0)])
        #q is the control qubit, and the other n0 qubit are the qubits in the input register
        
        """ Note that the implemented method of creating the U^2^j gates by repeating U 
        grows exponentially with j and will not result in a polynomial time algorithm.
        despite scaling polynomially with j, modular exponentiation circuits are not 
        straightforward and are the bottleneck in Shor’s algorithm. """
        
    #Apply inverse-QFT    
    #qft_dagger_apply(qc, range(n), n)
    qc.append(qft_dagger(n), range(n)) 
    
    #Measure the quantum state
    qc.measure(range(n), range(n))
    
    #Count number of gates (TODO ITS WRONG)
    Nops_dict = qc.count_ops()
    Nops = np.sum(list(Nops_dict.values())) - Nops_dict['measure']
    print("  %s gate operations" % Nops)
    
    #Draw the circuit
    #get_ipython().run_line_magic('matplotlib', 'inline')
    qc.draw(output='mpl', filename='Shor_circuit.png', fold=300) #requires pip install pylatexenc
    #plt.show()
    
    
    # Simulate Quantum circuit in AER simulator (locally)
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc, shots=1)
    result = aer_sim.run(qobj, memory=True).result()
    readings = result.get_memory()
    print("      Register Reading: " + readings[0])
    phase = int(readings[0],2)/(2**n)
    print("      Corresponding Phase: %f" % phase)
    
    frac = Fraction(phase).limit_denominator(N) # Denominator should (hopefully!) tell us r
    r = frac.denominator
  
    print("\n      Found period r =", r)
    return r



def cmul_amodN_apply(qc, q_, a, power, N):
    """Controlled multiplication by a mod N"""
    
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13 but is %s" % a)

    for iteration in range(power):
        if a in [2,13]:
            qc.swap(q_[2],q_[3])
            qc.swap(q_[1],q_[2])
            qc.swap(q_[0],q_[1])
        if a in [7,8]:
            qc.swap(q_[0],q_[1])
            qc.swap(q_[1],q_[2])
            qc.swap(q_[2],q_[3])
        if a in [4, 11]:
            qc.swap(q_[1],q_[3])
            qc.swap(q_[2],q_[2])
        if a in [7,11,13]:
            for q in range(4):
                qc.x(q_[q])
    return
    

def cmul_amodN(a, power, N):
    """Controlled multiplication by a mod N"""
    
    n0 = int(np.log2(N) + 1) #number of qbits in the input register (n0 ~ log2(N) )
    
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13 but is %s" % a)
    U = QuantumCircuit(n0)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7,8]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U.name = "Ua^%i mod N" % (power)
    U.draw(output='mpl', filename='%s.png' % U.name, fold=300)
    U = U.to_gate()
    c_U = U.control()
    return c_U



def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    qc.draw(output='mpl', filename='%s.png' % qc.name, fold=300)
    return qc

def qft_dagger_apply(qc, q_,n):
    """n-qubit QFTdagger the first n qubits in circ"""
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(q_[j]-q_[m])), q_[m], q_[j])
        qc.h(q_[j])

    return
    


def a2jmodN(a, j, N):
    """Compute a^{2^j} (mod N) by repeated squaring"""
    for i in range(j):
        a = np.mod(a**2, N)
    return a
    
    
    
    
    
if __name__ == '__main__':
    
    a = 4
    N = 15
    r = quantum_period(a,N)