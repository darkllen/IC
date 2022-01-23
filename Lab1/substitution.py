from term import Term
from copy import deepcopy

class Substitution:
    def __init__(self, term_a: Term, term_b: Term):
        self.term_a = term_a
        self.term_b = term_b

        if not self.is_none:
            self.copied_a = deepcopy(term_a)
            self.copied_b = deepcopy(term_b)

    @property
    def is_none(self):
        return self.term_a is None and self.term_b is None

    def __str__(self):
        return f'{str(self.copied_a)}/{str(self.copied_b)}'

    def __repr__(self):
        return  self.__str__()