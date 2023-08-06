from VariationalCircuit import VariationalCircuit
from pyqpanda import *

def base_vqc_evaluation(VariationalCircuit, 
                        qvm,
                        qubits,
                        placeholders, 
                        parameters,
                        backend_type = CPU_SINGLE_THREAD):
    pass


class VariationalCircuitSimulator:

    def __init__(self, variational_circuit,
                 n_qubit = None,
                 n_placeholder = None,
                 n_parameter = None,
                 placeholder = None,
                 backend_type = CPU_SINGLE_THREAD
    ):
        self._variational_circuit = variational_circuit
        self._n_qubit = n_qubit
        self._n_placeholder = n_placeholder
        self._n_parameter = n_parameter
        self._variational_circuit.set_placeholder = placeholder
        self._backend_type = backend_type
        self._qvm = None
        self._qubits = None
        self._cbits = None

    def set_n_qubit(self, n_qubit):
        self._n_qubit = n_qubit

    def set_n_placeholder(self, n_placeholder):
        self._n_placeholder = n_placeholder
    
    def set_n_parameter(self, n_parameter):
        self._n_parameter = n_parameter

    def set_placeholder(self, placeholder):
        self._variational_circuit.set_placeholder = placeholder

    def base_evaluation(self, parameter):
        if self._qvm is None:
            self._qvm = QuantumMachine(backend_type=self._backend_type)

        if self._qubits is None:
            self._qubits = self._qvm.qAlloc_many(self._n_qubit)

        prog = self._variational_circuit.feed_parameter(parameter)





    
    

    
    