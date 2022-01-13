from enum import  Enum

class TermType(Enum):
    EMPTY = 0
    CONSTANT = 1
    VARIABLE = 2
    FUNCTION = 3

class Term:
    def __init__(self, term: str):
        if term == '':
            self.type = TermType.EMPTY
            return

        self.__term = term

    def __str__(self):
        return self.__term

    def __eq__(self, other):
        return self.__term == other.__term

    @property
    def head(self):
        k = self.__term.find(',')
        b = self.__term.find('(')
        print(k, b)
        return Term('')

    @property
    def is_constant(self) -> bool:
        return self.__term in ['0', '1']

    @property
    def is_variable(self) -> bool:
        return self.__term.isalpha()

    @property
    def is_empty(self) -> bool:
        return self.__term == ''

    def occurs_in(self, term_b) -> bool:
        return term_b.__term in self.__term
