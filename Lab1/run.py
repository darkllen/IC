import json
from typing import Union

from substitution import Substitution
from term import Term,TermType

input_file = 'input.txt'


def unify(term_a: Term, term_b: Term) -> Union[None, bool, Substitution]:
    print('term_a', term_a)
    print('term_b', term_b)
    if ((term_a.type == TermType.CONSTANT and term_b.type == TermType.CONSTANT)
            or (term_a.type == TermType.EMPTY and term_b.type == TermType.EMPTY)):
        if term_a == term_b:
            return None
        else:
            return False
    elif term_a.type == TermType.VARIABLE:
        if term_a.occurs_in(term_b):
            return False
        else:
            return Substitution(term_a, term_b)
    elif term_b.type == TermType.VARIABLE:
        if term_b.occurs_in(term_a):
            return False
        else:
            return Substitution(term_b, term_a)
    elif term_a.type == TermType.EMPTY or term_b.type == TermType.EMPTY:
        return False

    head_a, head_b = term_a.head, term_b.head
    substitution1 = unify(head_a, head_b)
    if not substitution1:
        return False
    te1 = substitution1.apply()


with open(input_file, 'r') as f:
    terms = json.loads(f.read())
    e1, e2 = terms['term_a'], terms['term_b']
    unify(Term(e1), Term(e2))
