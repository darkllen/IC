import re
from enum import  Enum

class TermType(Enum):
    EMPTY = 0
    CONSTANT = 1
    VARIABLE = 2
    FUNCTION = 3

class Term:
    def __init__(self, term: str):
        self.term = ''
        self.subterms = []

        if term == '':
            self.type = TermType.EMPTY
        elif term in ['0', '1']:
            self.type = TermType.CONSTANT
            self.term = term[0]
        elif len(term) == 1 and term.isalpha():
            self.type = TermType.VARIABLE
            self.term = term[0]
        else:
            self.type = TermType.FUNCTION
            self.term = term[0]
            self.subterms = re.findall('\w\(.*\)|\w', term[1:-1])

    def __str__(self):
        string = f'{self.term}'
        if self.type == TermType.FUNCTION:
            string += f'({",".join(self.subterms)})'
        return string

    def __eq__(self, other):
        return self.term == other.term and self.subterms == other.subterms

    @property
    def head(self):
        return Term(self.subterms[0])

    def occurs_in(self, term_b) -> bool:
        return any(self.term in term for term in term_b.subterms)