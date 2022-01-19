import re
from enum import  Enum
from copy import copy, deepcopy

class TermType(Enum):
    EMPTY = 0
    CONSTANT = 1
    VARIABLE = 2
    FUNCTION = 3

class Term:
    INNER_VARS = {}

    def __init__(self, term):
        # if term_object:
        #     self.term = term_object.term
        #     self.subterms = [Term(inner_vars=inner_vars, term_object=sub) for sub in term_object.subterms]
        #     self.type = term_object.type
        #     return

        self.term = ''
        self.subterms = []
        self.inner = {}

        if term == '':
            self.type = TermType.EMPTY
        elif term in ['0', '1']:
            self.type = TermType.CONSTANT
            self.term = term[0]
        elif term.isalnum() and term.count('(') == 0:
            self.type = TermType.VARIABLE
            self.term = term
            if self.term not in self.INNER_VARS:
                self.INNER_VARS[self.term] = self
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
                        if term[start_i:end_i] in self.INNER_VARS:
                            var = self.INNER_VARS[term[start_i:end_i]]
                            subterms.append(var)
                            self.inner.update(var.inner) if var.type == TermType.FUNCTION else self.inner.update({var.term})
                        else:
                            var = Term(term[start_i:end_i])
                            subterms.append(var)
                            self.inner.update(var.inner) if var.type == TermType.FUNCTION else self.inner.update({var.term})
                        start_i = end_i + 1
                if term[end_i] == ',' and count == 0:
                    if term[start_i:end_i] in self.INNER_VARS:
                        var = self.INNER_VARS[term[start_i:end_i]]
                        subterms.append(var)
                        self.inner.update(var.inner) if var.type == TermType.FUNCTION else self.inner.update({var.term})
                    else:
                        var = Term(term[start_i:end_i])
                        subterms.append(var)
                        self.inner.update(var.inner) if var.type == TermType.FUNCTION else self.inner.update({var.term})
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
        if len(self.subterms) < 2:

            return Term('')
        else:
            self.subterms.pop(0)
            return self

    def apply(self, sub_l):
        for sub in sub_l:
            if not sub.is_none and sub.term_a.term in self.INNER_VARS:
                self.INNER_VARS[sub.term_a.term].subterms = sub.term_b.subterms
                self.INNER_VARS[sub.term_a.term].type = sub.term_b.type
                self.INNER_VARS[sub.term_a.term].term = sub.term_b.term
        return self

    def __apply(self, sub):
        if self.type == TermType.FUNCTION:
            for subterm in self.subterms:
                subterm.__apply(sub)
        elif self == sub.term_a:
            self.term = sub.term_b.term
            self.subterms = sub.term_b.subterms
            self.type = sub.term_b.type

    def __repr__(self):
        return  self.__str__()

    def __eq__(self, other):
        return self.term == other.term and self.subterms == other.subterms if isinstance(other, Term) else False

    def __contains__(self, item):
        for i in self.subterms:
            if i.type == TermType.VARIABLE and i == item:
                return True
            else:
                is_in = item in i
                if is_in:
                    return True
        return False