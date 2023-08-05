from typing import Union, List
from pythum.qubit import Qubit

class Qublock:
    """An list-like block of n qubits"""
    def __init__(self, value: Union[int, 'Qublock', List[Qubit]]):
        _type = type(value)
        if _type is int:
            # Just instanciate the block with n qubits
            n = value
            value = [
                Qubit()
                for i in range(n)
            ]
        elif issubclass(_type, Qublock):
            # Copy each qubit
            qublock = value
            value = [Qubit.from_qubit(qubit) for qubit in qublock.__qubits]
        elif _type is not list:
            raise ValueError("Expected an int or list of Qubits")
        self.__qubits = value
    
    @classmethod
    def from_notation(cls, value: str) -> 'Qublock':
        block = value.split(">")
        value = [
            Qubit.from_notation("{0}>".format(q))
            for q in block
        ]
        return cls(value)
    
    def __str__(self):
        return "".join((
            str(qbit)
            for qbit in self.__qubits
        ))
    
    def __repr__(self):
        return str(self)
    
    def __in__(self, value) -> bool:
        return value in self.__qubits
    
    def __iter__(self):
        return iter(self.__qubits)
    
    def __len__(self):
        return len(self.__qubits)
    
    def __getitem__(self, pos: int):
        return self.__qubits[pos]
    
    def __setitem__(self, pos: int, qubit: Qubit):
        self.__qubits[pos] = qubit


class Qubyte(Qublock):
    def __init__(self, value: Union[Qublock, List[Qubit]]=None):
        if value is None:
            value = 8
        if type(value) is int and value > 8:
            value = 8
        super().__init__(value)

    @classmethod
    def from_notation(cls, value: str) -> 'Qubyte':
        block = value.split(">")[:-1]
        value = [
            Qubit.from_notation("{0}>".format(q))
            for q in block
        ]
        _len = len(value)
        if _len < 8:
            value = (
                Qubit()
                for i in range(_len, 8)
            ) + value
        elif _len > 8:
            value = value[-8:]
        return cls(value)
