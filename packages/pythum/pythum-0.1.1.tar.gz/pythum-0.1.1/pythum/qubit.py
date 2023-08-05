import math

class Qubit:
    """Class for qubit manipulation and instanciation by notation"""
    def __init__(self):
        self.__alpha = 1
        self.__beta = 0
    
    @classmethod
    def from_notation(cls, value: str) -> 'Qubit':
        """Instanciate a qubit by the formal notation. 
        The following are possible values:
            "|0>": 0
            "|1>": 1
            "|10>", "|01>": super position
        """
        qubit = cls()
        if not value.startswith('|') or not value.endswith('>'):
            raise ValueError("Unexpected notation {0}".format(value))
        value = value[1:-1]
        alpha_beta = {
            '0': (1, 0), 
            '1': (0, 1), 
            '10': (0.5, 0.5), 
            '01': (0.5, 0.5)
        }.get(value)
        if alpha_beta is None:
            raise ValueError("Unexpected notation {0}".format(value))
        qubit.__alpha, qubit.__beta = alpha_beta
        return qubit

    @classmethod
    def from_qubit(cls, qubit: 'Qubit') -> 'Qubit':
        """Instanciate a copy of another qubit"""
        self = cls()
        self.__alpha = qubit.__alpha
        self.__beta = qubit.__beta
        return self

    def __str__(self):
        """String represantation for the qubit using the formal notation"""
        if self.__alpha == 0 and self.__beta == 1:
            return "|1>"
        elif self.__alpha == 1 and self.__beta == 0:
            return "|0>"
        # return "|01>" if self.__alpha >= self.__beta else "|10>"
        return "|01>"
    
    def __repr__(self):
        """String represantation for the qubit using the formal notation"""
        return str(self)

    def up(self) -> 'self':
        """Points up the eletron. The outcome of any measure will always be 1"""
        self.__alpha = 0
        self.__beta = 1
        return self
    
    def down(self) -> 'self':
        """Points down the eletron. The outcome of any measure will always be 0"""
        self.__alpha = 1
        self.__beta = 0
        return self

    def left(self) -> 'self':
        """Points the eletron to the left. The outcome of a measure may be 0 or 1"""
        self.__alpha = 0.5
        self.__beta = 0.5
        return self
    
    def right(self) -> 'self':
        """Points the eletronto the right. The outcome of a measure may be 0 or 1"""
        self.__alpha = 0.5
        self.__beta = 0.5 
        return self

    @property
    def alpha(self):
        """Alpha probability for mesuring 0"""
        beta2 = self.__beta * self.__beta
        return math.sqrt(1 - beta2)
    
    @property
    def beta(self):
        """Beta probability for mesuring 1"""
        alpha2 = self.__alpha * self.__alpha
        return math.sqrt(1 - alpha2)
