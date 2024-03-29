<img src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/qiskit-heading.gif" width=300>

### This repository supports the Medium article

### [The Ultimate Hack: Crack your Credit Card with Quantum Programming](https://medium.com/p/17ddd045eba6/edit)

The code in this repository is inspired from the Qiskit implementation of [Tiago Leão](https://github.com/ttlion/ShorAlgQiskit).

&nbsp;


# Shor's Algorithm

The [Shor's algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm), proposed by Peter Shor in 1995 [2], is today one of the most famous quantum algorithm; it is considerably significant because, while the security of our online transactions rests on the assumption that factoring integers with a thousand or more digits is practically impossible, the algorithm enables to find 2 factors of a number in polynomial time with its number of digits. Shor's algorithm was first experimentally demonstrated in 2001 by a group at IBM, which factored 15 into 3 and 5, using a quantum computer of 7 qubits [3].  


&nbsp;

### Complexity of factoring

<img align="right" src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/complexity.png" width=510>
Let N be the number to be factorized, and d~log2(N) its number of digit. The most efficient classical factoring algorithm currently known is the [General number field sieve](https://en.wikipedia.org/wiki/General_number_field_sieve), which has an exponential asymptotic runtime to the number of digits : O(exp(d^1/3)). On the other hand, Shor’s factoring algorithm has an asymptotic runtime polynomial in d : O(d^3). 

This remarquable difference between polynomial and exponential runtime scaling currently places the Factoring problem into the [BQP\P](https://en.wikipedia.org/wiki/BQP) decision class (cf. figure in introduction).


&nbsp;

## General implementation

We want to find two factors *p1* and *p2* that divide *N*. Before diving into the algorithm, we have to make sure that:  
* N is odd (if it's even, then 2 is a trivial factor)
* N is not the power of a prime

```python
from math import log

def Check(N):

    if N % 2 == 0:
        print ("2 is a trivial factor")
        return False
        
    for k in range(2,int(log(N,2))): #log2(N)
        if (pow(N,(1/k)).is_integer():
            print ("N =", pow(N,(1/k)), "^", k)
            return False
    
    return True
```


&nbsp;

### Classical part

With some Arithmetic, Group theory, Euler's Theorem and Bézout's identity, it is possible to reduce the factorization problem into a period finding problem of the modular exponential function (see [this page](https://en.wikipedia.org/wiki/Shor%27s_algorithm) for more details). The classical part of the algorithm is implemented as follow:

```python
from random import randint

def Shor(N):

    while True:
    
        #1) pick a random number a<N
        a = randint(1, N-1)    
    
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
                
    print ("N =", p1, "*", p2)
    return p1, p2
```


&nbsp;

### Period finding quantum subroutine
We want to find *r* the period of the modular exponentiation function <img src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/modular.png" width=128>, which is the smallest positive integer for which <img src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/period.png" width=123>. Given the numbers *N* and *a*, the period finding subroutine of the modular exponentiation function proposed by Shor proceed as follow:

* Initialize *n0* qubit and store *N* in the input register (*n0* ~ log2(*N*) )
* Initialize *n* qubit for the output register (where 2^*n* ~ *N*^2 => *n* ~ 2*n0*)
* Apply Hadamard Gate to all of the qubit in the output register
* Apply the controled modular exponentiation gates *Ua*, *Ua*^2, *Ua*^4, *Ua*^8, .., *Ua*^(2^(2*n*-1)) to the input register
* Apply the inverse QFT (Quantum Fourier Transform) to the output register
* Measure the output *y*
* Calculate the irreducible form of *y*/*N* and extract the denominator *r*
* Check if *r* is a period, if not, check multiples of *r*
* If period not found, try again from the beginning

<img src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/Shor.png" width=800>

The quantum gate *Ua* refers to the unitary operator that perform the modular exponentiation function *x → a^x (modN)*.
The implementation of controlled *Ua* are relatively complex [4], and the "right" gate set to use is currently still an open question (plus it also depends the architecture used for the quantum computer). While not optimal, Beauregard [5] gave a practical implementation for a general *Ua* that is entirely general.


&nbsp;

### Factoring *N*=35

As a concrete example, we run the Shor's algorithm *N* = 35 and *a* = 2, measure the output of the quantum circuit and try to infer *r* from the denominator of the fraction 1000 times (the source code is in `src/Shor_factoring`). When *r* is found to not be the period, we also check for multiple of 2 and 3 of *r*. Then, we recover non-trivail factors of *N* with the relationship *p* = gcd(*a*^(*r*/2)-1, *N*) and *q* = gcd(*a*^(*r*/2)+1, *N*).
In our case, as seen on the figure below, we find the correct period 60% of the time (*r* = 12). from which we recover *p* = gcd(63,35) = 7 and *q* = gcd(65,35) = 5.

<img src="https://raw.githubusercontent.com/Aurelien-Pelissier/Medium/master/Quantum%20Programming/img/Shor35.png" width=900>



&nbsp;

## References

[2]: Shor, P. W. (1999). Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer. SIAM review, 41(2), 303-332. [https://arxiv.org/abs/quant-ph/9508027]


[3]: Vandersypen, L. M., Steffen, M., Breyta, G., Yannoni, C. S., Sherwood, M. H., & Chuang, I. L. (2001). Experimental realization of Shor's quantum factoring algorithm using nuclear magnetic resonance. Nature, 414(6866), 883. [https://www.nature.com/articles/414883a]


[4]: Markov, I. L., & Saeedi, M. (2012). Constant-optimized quantum circuits for modular multiplication and exponentiation. arXiv preprint arXiv:1202.6614. [https://arxiv.org/abs/1202.6614]


[5]: Beauregard, Stephane. "Circuit for Shor's algorithm using 2n+ 3 qubits." arXiv preprint quant-ph/0205095 (2002). [https://arxiv.org/abs/quant-ph/0205095]
