
from pyqpanda import *
from copy import deepcopy
from math import pi

class VariationalCircuit:

    def __init__(self, circuit_callable):
        self._circuit_callable = circuit_callable
        self._qubit = None
        self._n_qubit = 0
        self._placeholder = None
        self._n_placeholder = 0
        self._parameter = None
        self._n_parameter = 0

    def set_qubit(self, q):
        self._qubit = q
        self._n_qubit = len(q)

    def set_placeholer(self, placeholder):
        self._placeholder = placeholder
        self._n_placeholder = len(placeholder)

    def feed_parameter(self, parameter):
        self._parameter = parameter
        self._n_parameter = len(parameter)
        return self._circuit_callable(
            qubit = self._qubit, 
            placeholder = self._placeholder, 
            parameter = self._parameter
            )

    def feed_parameter_once(self, parameter):
        return self._circuit_callable(
            qubit = self._qubit, 
            placeholder = self._placeholder, 
            parameter = parameter
            )
    
    def get_parameter_delta_circuit(self, parameter_number, delta_value):
        if parameter_number>=self._n_parameter:
            assert False
        parameter = deepcopy(self._n_parameter)
        parameter[parameter_number] += (delta_value)
        circuit = self.feed_parameter_once(parameter)
        return circuit

    def get_grad_circuit_plus(self, parameter_number):   
        return self.get_parameter_delta_circuit(parameter_number, pi/2)

    def get_grad_circuit_minus(self, parameter_number):        
        return self.get_parameter_delta_circuit(parameter_number, -pi/2)

    def get_grad_circuit(self, parameter_number):        
        return (self.get_grad_circuit_plus(parameter_number),
                self.get_grad_circuit_minus(parameter_number))
    