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
        self.is_unified = False

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
            self.subterms = [Term(subterm) for subterm in re.findall('\w\(.*\)|\w', term[1:-1])]

    def __str__(self):
        string = f'{self.term}'
        if self.type == TermType.FUNCTION:
            string += f'({",".join([str(subterm) for subterm in self.subterms])})'
        return string

    def __eq__(self, other):
        return self.term == other.term and self.subterms == other.subterms

    # @property
    def head(self):
        for i in self.subterms:
            if not i.is_unified:
                i.is_unified = True
                return Term(str(i))
        return Term('')

    def occurs_in(self, term_b) -> bool:
        return any(self.term in str(term) for term in term_b.subterms)