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
        if term_a in term_b:
            return False
        if term_a.term == term_b.term:
            return [Substitution(None, None)]
        else:
            return [Substitution(term_a, term_b)]
    elif term_b.type == TermType.VARIABLE:
        if term_b in term_a:
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

    term_a.apply(substitution1)
    te1 = term_a.tail()
    te2 = term_b.tail()

    substitution2 = unify(te1,te2)
    if substitution2 is False:
        return False
    return [sub for sub in substitution1 + substitution2 if not sub.is_none]


def generate_h_n(n:int):
    h1 = 'h('
    x = [f'x{n + 1}' for n in range(n)]
    y = [f'f(y{n},y{n})' for n in range(n)]
    h1 += ','.join(x + y)
    h1 += f',y{n})'

    h2 = 'h('
    x = [f'f(x{n},x{n})' for n in range(n)]
    y = [f'y{n + 1}' for n in range(n)]
    h2 += ','.join(x + y)
    h2 += f',x{n})'

    return Term(h1), Term(h2)

import time
import sys
with open(input_file, 'r') as f:
    sys.setrecursionlimit(10000)
    terms = json.loads(f.read())
    terms = terms[terms[0]["term_index"]]
    n = 1
    # e1, e2 = Term(terms['term_a']), Term(terms['term_b'])
    e1, e2 = generate_h_n(n)

    print('start')
    t = time.time()
    res = unify(e1, e2)
    print('res time: ', time.time() - t)
    Term.INNER_VARS = {}
    e1_i, e2_i = generate_h_n(n)
    print('term a: ', e1_i)
    print('term b: ', e2_i)
    print('res: ', res)
    #
    # if res:
    #     for ind, sub in enumerate(res):
    #         print()
    #         print(f'step {ind+1}:')
    #         e1_i.apply([Substitution(sub.copied_a, sub.copied_b)])
    #         print('sub:         ', sub)
    #         print('term a prev: ', e1_ii)
    #         print('term a new:  ', e1_i)
    #         # print('term b prev: ', e2_ii)
    #         print('term b new:  ', e2_i)
    #
    #     print()
    #     print('term a res: ', e1_i)
    #     print('term b res: ', e2_i)