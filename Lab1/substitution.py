from term import Term


class Substitution:
    def __init__(self, term_a: Term, term_b: Term):
        self.__term_a = term_a
        self.__term_b = term_b

    def apply(self, term) -> Term:
        return Term(str(term).replace(str(self.__term_a), str(self.__term_b)))