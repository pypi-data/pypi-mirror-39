import random
from pythum.qubit import Qubit
from pythum.qublock import Qublock, List, Union

class QuantumEngine:
    def measure(self, qubit: Qubit):
        alpha = qubit.alpha
        spin = random.random()
        return 1 if spin > alpha else 0

    def measure_byte(self, qublock: Union[Qublock, List[Qubit]]):
        value = 0
        pos = 0
        for qubit in qublock:
            value += self.measure(qubit) * pow(2, pos)
            pos += 1
        return value
