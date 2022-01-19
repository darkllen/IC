from term import Term


class Substitution:
    def __init__(self, term_a: Term, term_b: Term):
        self.term_a = term_a
        self.term_b = term_b

        self.copied_a = str(self.term_a)
        self.copied_b = str(self.term_b)

    @property
    def is_none(self):
        return self.term_a is None and self.term_b is None

    def __str__(self):
        return f'{str(self.copied_a)}/{str(self.copied_b)}'

    def __repr__(self):
        return  self.__str__()