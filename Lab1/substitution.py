from term import Term


class Substitution:
    def __init__(self, term_a: Term, term_b: Term):
        self.__term_a = term_a
        self.__term_b = term_b

    def apply(self) -> Term:
        pass