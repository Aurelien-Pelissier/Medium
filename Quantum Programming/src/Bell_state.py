"""
this code create a Bell's state (|00> + |11>)
and measure it 1000 times
"""

from qiskit import QuantumProgram
qp = QuantumProgram()
qr = qp.create_quantum_register('qr',2)      #Initialize 2 qubits to perform operations
cr = qp.create_classical_register('qc',2)    #Initialize 2 classical bits to store the measurements
qc = qp.create_circuit('Bell',[qr],[cr])
qc.h(qr[0])                                  #Apply Hadamar gate
qc.cx(qr[0], qr[1])                          #Apply CNOT gate
qc.measure(qr[0], cr[0])                     #Measure qubit 0 and store the result in bit 0
qc.measure(qr[1], cr[1])                     #Measure qubit 1 and store the result in bit 1

result = qp.execute('Bell', shots=1000)      #Compile and run the Quantum Program 1000 times
print(result.get_counts('Bell'))


#https://www.softynews.com/optional-tutorial-qiskit-quantum-computing-platform/