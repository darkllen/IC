from term import Term


class Substitution:
    def __init__(self, term_a: Term, term_b: Term):
        self.__term_a = term_a
        self.__term_b = term_b

    @staticmethod
    def apply(sub_list, term) -> Term:
        tail = term.subterms
        for sub in sub_list:
            tail = [Term(str(subterm).replace(str(sub.__term_a), str(sub.__term_b))) for subterm in tail]
        term.subterms = tail
        return term

    @property
    def is_none(self):
        return self.__term_a is None and self.__term_b is None

    def __str__(self):
        return f'{str(self.__term_a)}/{str(self.__term_b)}'

    def __repr__(self):
        return  self.__str__()