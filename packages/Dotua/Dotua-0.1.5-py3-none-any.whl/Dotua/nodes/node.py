class Node():
    """
    Abstract interface for computational nodes in automatic differentiation.

    Specifically, this class will provide the abstract interface for the
    Scalar and Vector subclasses.  This class outlines each of the operators
    that must be overloaded by Scalar and Vector.  Users of this AD library
    should NEVER instantiate @Node objects directly (as mentioned in the
    documentation).
    """

    def eval(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplemented

    def __radd__(self, other):
        raise NotImplemented

    def __sub__(self, other):
        raise NotImplemented

    def __rsub__(self, other):
        raise NotImplemented

    def __mul__(self, other):
        raise NotImplemented

    def __rmul__(self, other):
        raise NotImplemented

    def __truediv__(self, other):
        raise NotImplemented

    def __rtruediv__(self, other):
        raise NotImplemented

    def __pow__(self, other):
        raise NotImplemented

    def __rpow__(self, other):
        raise NotImplemented

    def __neg__(self):
        raise NotImplemented
