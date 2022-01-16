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
        elif term.isalnum() and term.count('(') == 0:
            self.type = TermType.VARIABLE
            self.term = term
        else:
            self.type = TermType.FUNCTION
            self.term = term[0:term.find('(')]
            subterms = []

            start_i = term.find('(')+1
            end_i = start_i
            count = 0
            while end_i<len(term):
                if term[end_i] == '(':
                    count += 1
                if term[end_i] == ')':
                    count -=1
                    if end_i == len(term)-1:
                        subterms.append(Term(term[start_i:end_i]))
                        start_i = end_i + 1
                if term[end_i] == ',' and count == 0:
                    subterms.append(Term(term[start_i:end_i]))
                    start_i = end_i+1
                end_i+=1

            self.subterms = subterms

    def __str__(self):
        string = f'{self.term}'
        if self.type == TermType.FUNCTION:
            string += f'({",".join([str(subterm) for subterm in self.subterms])})'
        return string

    # @property
    def head(self):
        return Term('') if self.subterms == [] else self.subterms[0]

    def tail(self):
        return Term('') if len(self.subterms)<2 else Term(f'{self.term}({",".join([str(subterm) for subterm in self.subterms[1:]])})')

    def occurs_in(self, term_b) -> bool:
        return any(self.term in str(term) for term in term_b.subterms)

    def __repr__(self):
        return  self.__str__()