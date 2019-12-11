'''
from math import sqrt, sin, cos


class Vector:
    """A Python implementation of a vector class and some of its operations."""

    values = None

    def __init__(self, *args):
        self.values = list(args)

    def __str__(self):
        """String representation of a vector is its components surrounded by < and >."""
        return f"<{str(self.values)[1:-1]}>"

    __repr__ = __str__

    def __len__(self):
        """Defines the length of the vector as the number of its components."""
        return len(self.values)

    def __hash__(self):
        """Defines the hash of the vector as a hash of a tuple with its components."""
        return hash(tuple(self))

    def __eq__(self, other):
        """Defines vector equality as the equality of all of its components."""
        return self.values == other.values

    def __setitem__(self, i, value):
        """Sets the i-th vector component to the specified value."""
        self.values[i] = value

    def __getitem__(self, i):
        """Either returns a new vector when sliced, or the i-th vector component."""
        if type(i) == slice:
            return Vector(*self.values[i])
        else:
            return self.values[i]

    def __delitem__(self, i):
        """Deletes the i-th component of the vector."""
        del self.values[i]

    def __neg__(self):
        """Defines vector negation as the negation of all of its components."""
        return Vector(*iter(-component for component in self))

    def __add__(self, other):
        """Defines vector addition as the addition of each of their components."""
        return Vector(*iter(u + v for u, v in zip(self, other)))

    __iadd__ = __add__

    def __sub__(self, other):
        """Defines vector subtraction as the subtraction of each of its components."""
        return Vector(*iter(u - v for u, v in zip(self, other)))

    __isub__ = __sub__

    def __mul__(self, other):
        """Defines scalar and dot multiplication of a vector."""
        if type(other) == int or type(other) == float:
            # scalar multiplication
            return Vector(*iter(component * other for component in self))
        else:
            # dot multiplication
            return sum(u * v for u, v in zip(self, other))

    __rmul__ = __imul__ = __mul__

    def __truediv__(self, other):
        """Defines vector division by a scalar."""
        return Vector(*iter(component / other for component in self))

    def __floordiv__(self, other):
        """Defines floor vector division by a scalar."""
        return Vector(*iter(component // other for component in self))

    def __matmul__(self, other):
        """Defines cross multiplication of a vector."""
        return Vector(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0],
        )

    __imatmul__ = __matmul__

    def __mod__(self, other):
        """Defines vector mod as the mod of its components."""
        return Vector(*iter(component % other for component in self))

    def magnitude(self):
        """Returns the magnitude of the vector."""
        return sqrt(sum(component ** 2 for component in self))

    def rotated(self, angle):
        """Returns the vector rotated by an angle (in radians)."""
        return Vector(
            self[0] * cos(angle) - self[1] * sin(angle),
            self[0] * sin(angle) + self[1] * cos(angle),
        )

    def rotated_new(self, angle: float, point: Vector = None):
        """Returns this vector rotated by an angle (in radians) around a certain point."""
        if point is None:
            point = Vector(0, 0)

        return self.__rotated(self - point, angle) + point

    def __rotated(self, vector: Vector, angle: float):
        """Returns a vector rotated by an angle (in radians)."""
        return Vector(
            vector[0] * cos(angle) - vector[1] * sin(angle),
            vector[0] * sin(angle) + vector[1] * cos(angle),
        )

    def unit(self):
        """Returns a unit vector with the same direction as this vector."""
        return self / self.magnitude()

    def abs(self):
        """Returns a vector with absolute values of the components of this vector."""
        return Vector(*iter(abs(component) for component in self))

    def repeat(self, n):
        """Performs sequence repetition on the vector (n times)."""
        return Vector(*self.values * n)


def distance(p1: Vector, p2: Vector):
    """Returns the distance of two points in space (represented as Vectors)."""
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


'''
from __future__ import annotations
from math import sqrt, sin, cos


class Vector:
    """A Python implementation of a vector class and some of its operations."""

    values = None

    def __init__(self, *args):
        self.values = list(args)

    def __str__(self):
        """String representation of a vector is its components surrounded by < and >."""
        return f"<{str(self.values)[1:-1]}>"

    __repr__ = __str__

    def __len__(self):
        """Defines the length of the vector as the number of its components."""
        return len(self.values)

    def __hash__(self):
        """Defines the hash of the vector as a hash of a tuple with its components."""
        return hash(tuple(self))

    def __eq__(self, other):
        """Defines vector equality as the equality of all of its components."""
        return self.values == other.values

    def __setitem__(self, i, value):
        """Sets the i-th vector component to the specified value."""
        self.values[i] = value

    def __getitem__(self, i):
        """Either returns a new vector when sliced, or the i-th vector component."""
        if type(i) == slice:
            return Vector(*self.values[i])
        else:
            return self.values[i]

    def __delitem__(self, i):
        """Deletes the i-th component of the vector."""
        del self.values[i]

    def __neg__(self):
        """Defines vector negation as the negation of all of its components."""
        return Vector(*iter(-component for component in self))

    def __add__(self, other):
        """Defines vector addition as the addition of each of their components."""
        return Vector(*iter(u + v for u, v in zip(self, other)))

    __iadd__ = __add__

    def __sub__(self, other):
        """Defines vector subtraction as the subtraction of each of its components."""
        return Vector(*iter(u - v for u, v in zip(self, other)))

    __isub__ = __sub__

    def __mul__(self, other):
        """Defines scalar and dot multiplication of a vector."""
        if type(other) == int or type(other) == float:
            # scalar multiplication
            return Vector(*iter(component * other for component in self))
        else:
            # dot multiplication
            return sum(u * v for u, v in zip(self, other))

    __rmul__ = __imul__ = __mul__

    def __truediv__(self, other):
        """Defines vector division by a scalar."""
        return Vector(*iter(component / other for component in self))

    def __floordiv__(self, other):
        """Defines floor vector division by a scalar."""
        return Vector(*iter(component // other for component in self))

    def __matmul__(self, other):
        """Defines cross multiplication of a vector."""
        return Vector(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0],
        )

    __imatmul__ = __matmul__

    def __mod__(self, other):
        """Defines vector mod as the mod of its components."""
        return Vector(*iter(component % other for component in self))

    def magnitude(self):
        """Returns the magnitude of the vector."""
        return sqrt(sum(component ** 2 for component in self))

    def rotated(self, angle: float, point: Vector = None):
        """Returns this vector rotated by an angle (in radians) around a certain point."""
        if point is None:
            point = Vector(0, 0)

        return self.__rotated(self - point, angle) + point

    def rotated_new(self, angle: float, point: Vector = None):
        """Returns this vector rotated by an angle (in radians) around a certain point."""
        if point is None:
            point = Vector(0, 0)

        return self.__rotated(self - point, angle) + point

    def __rotated(self, vector: Vector, angle: float):
        """Returns a vector rotated by an angle (in radians)."""
        return Vector(
            vector[0] * cos(angle) - vector[1] * sin(angle),
            vector[0] * sin(angle) + vector[1] * cos(angle),
        )

    def unit(self):
        """Returns a unit vector with the same direction as this vector."""
        return self / self.magnitude()

    def abs(self):
        """Returns a vector with absolute values of the components of this vector."""
        return Vector(*iter(abs(component) for component in self))

    def repeat(self, n):
        """Performs sequence repetition on the vector (n times)."""
        return Vector(*self.values * n)


def distance(p1: Vector, p2: Vector):
    """Returns the distance of two points in space (represented as Vectors)."""
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generate_link_number(lnetd_links):
    i = 0
    while i < len(lnetd_links):
        if i==0:
            lnetd_links[1]['linknum'] = 1
        if lnetd_links[i]['source'] == lnetd_links[i-1]['source'] and lnetd_links[i]['target'] == lnetd_links[i-1]['target']:
            lnetd_links[i]['linknum'] = lnetd_links[i-1]['linknum'] + 1;
        else:
            lnetd_links[i]['linknum'] = 1;
        i = i+1
    return lnetd_links
