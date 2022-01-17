import json
from typing import Union
from copy import  deepcopy

from substitution import Substitution
from term import Term,TermType

input_file = 'input.txt'


def unify(term_a: Term, term_b: Term) -> Union[None, bool, Substitution]:
    if ((term_a.type == TermType.CONSTANT and term_b.type == TermType.CONSTANT)
            or (term_a.type == TermType.EMPTY and term_b.type == TermType.EMPTY)):
        if term_a == term_b:
            return [Substitution(None, None)]
        else:
            return False
    elif term_a.type == TermType.VARIABLE:
        if term_a.occurs_in(term_b):
            return False
        if term_a.term == term_b.term:
            return [Substitution(None, None)]
        else:
            return [Substitution(term_a, term_b)]
    elif term_b.type == TermType.VARIABLE:
        if term_b.occurs_in(term_a):
            return False
        else:
            return [Substitution(term_b, term_a)]
    elif term_a.type == TermType.EMPTY or term_b.type == TermType.EMPTY:
        return False
    elif term_a.type == TermType.FUNCTION and term_b.type == TermType.FUNCTION and term_a.term != term_b.term:
        return False

    head_a, head_b = term_a.head(), term_b.head()
    substitution1 = unify(head_a, head_b)
    if substitution1 is False:
        return False
    te1 = Substitution.apply(substitution1, term_a.tail())
    te2 = Substitution.apply(substitution1, term_b.tail())

    substitution2 = unify(te1,te2)
    if substitution2 is False:
        return False
    return [sub for sub in substitution1 + substitution2 if not sub.is_none]


with open(input_file, 'r') as f:
    terms = json.loads(f.read())
    terms = terms[terms[0]["term_index"]]
    e1, e2 = Term(terms['term_a']), Term(terms['term_b'])
    res = unify(e1, e2)

    print('term a: ', e1)
    print('term b: ', e2)
    print('res: ', res)
    if res:
        for ind, sub in enumerate(res):
            print()
            print(f'step {ind+1}:')
            e1_i, e2_i = deepcopy(e1), deepcopy(e2)
            e1, e2 = Substitution.apply([sub],e1), Substitution.apply([sub],e2)
            print('sub:         ', sub)
            print('term a prev: ', e1_i)
            print('term a new:  ', e1)
            print('term b prev: ', e2_i)
            print('term b new:  ', e2)

        print()
        print('term a res: ', e1)
        print('term b res: ', e2)