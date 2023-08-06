from functools import total_ordering


@total_ordering
class Point:
    def __init__(self, *args):
        ints = list(map(lambda v: isinstance(v, int), args))
        if not all(ints):
            raise TypeError('{} is not an integer'.format(args[ints.index(False)]))
        self.values = args
        self.order = len(args)

    def distance_to(self, other):
        return sum([abs(a - b) for a, b in zip(self.values, other.values)])

    def zero_distance(self):
        return self.distance_to(self.zero_point())

    def __repr__(self):
        return "Point{}".format(str(self))

    def __str__(self):
        return "({})".format(','.join(map(str, self.values)))

    def __add__(self, other):
        return Point(*[a + b for a, b in zip(self.values, other.values)])

    def __sub__(self, other):
        return Point(*[a - b for a, b in zip(self.values, other.values)])

    def __eq__(self, other):
        return all(a == b for a, b in zip(self.values, other.values))

    def __hash__(self):
        return hash(repr(self))

    def __iter__(self):
        yield from self.values

    def __bool__(self):
        return True

    def __lt__(self, other):
        # return self < other
        return all(a < b for a, b in zip(self.values, other.values))

    def zero_point(self):
        return zero_point(self.order)

    @property
    def adjacent(self):
        return [self + p for p in [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]]


def zero_point(order):
    return Point(*([0] * order))


directions = {
    'left': Point(-1, 0),
    'right': Point(1, 0),
    'up': Point(0, 1),
    'down': Point(0, -1)
}
file_directions = {
    'left': Point(0, -1),
    'right': Point(0, 1),
    'up': Point(-1, 0),
    'down': Point(1, 0)
}
