from .node import Node
import numpy as np


class Scalar(Node):
    """
    Implements the Node interface for single valued, user defined variables.

    Scalar objects have a single user defined value (either defined by user
    initialization or function composition) and a jacobian.  For
    each @Scalar object, the jacobian is a dictionary representation of the
    derivative of the function represented by the @Scalar object with respect
    to all user initialized Scalar objects defined by the same call to
    AutoDiff.create_scalar() that created the Scalar obect(s) used to define
    the function represented by this Scalar object.
    """

    def __init__(self, val, der=None):
        """
        Return a Scalar object with user specified value and derivative.

        INPUTS
        =======
        val: real valued numeric type
        der: dictionary representation of a jacobian

        RETURNS
        =======
        Scalar class instance

        NOTES
        ======
        The _val and _jacobian class variables are defined with leading
        underscores because they should be accessed or modified directly by
        the user.  The user should only access these variables via the
        Scalar object's eval method.
        """
        self._val = val
        self._jacobian = der

    def init_jacobian(self, nodes):
        """
        Initialize the jacobian class variable with appropriate seed values.

        INPUTS
        =======
        self: Scalar class instance
        nodes: list of Scalar objects, created by the same call to
               AutoDiff.create_scalar as the self Scalar object

        RETURNS
        =======
        Nothing is returned by this method.

        NOTES
        ======
        This function is called by AutoDiff.create_scalar after initializing
        all Scalar objects requested by the user.  This ensures that each
        Scalar object that the user might compose to create new Scalar
        functions has a derivative that is well defined with respect to all
        variables in the 'universe'.
        """
        self._jacobian = {node: int(id(self) == id(node)) for node in nodes}
        print(self._jacobian)

    def eval(self):
        """
        Return the value and derivative of the self Scalar object.

        INPUTS
        =======
        self: Scalar class instance

        RETURNS
        =======
        self._val: value of the user defined variable or function represented
                   by the self Scalar object
        self._jacobian: dictionary representation of the derivative of the self
                        Scalar object (which could be a user defined variable
                        or function) with respect to all variables in the
                        'universe'

        NOTES
        ======
        Scalar does not overload comparison operators so if users desire to
        compare the values of different Scalar objects they should do so
        by calling eval on each object to obtain the value.
        """
        return self._val, self._jacobian

    def partial(self, var):
        """Return the derivative of self with respect to var."""
        return self._jacobian[var]

    def __add__(self, other):
        """
        Return a Scalar object whose value is the sum of self and other.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the sum of the value of
                  the Scalar self and the value of other

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.
        """
        new_node = Scalar(self._val, self._jacobian)
        try:
            new_node._val += other._val
            new_node._jacobian = {k: (v + other.partial(k))
                                  for k, v in self._jacobian.items()}
        except AttributeError:
            new_node._val += other
        return new_node

    def __radd__(self, other):
        """Return a Scalar object whose value is the sum of self and other."""
        return self + other

    def __sub__(self, other):
        """Return a Scalar object with value self - other."""
        return self + (-other)

    def __rsub__(self, other):
        """Return a Scalar object with value other - self."""
        return -self + other

    def __mul__(self, other):
        """
        Return a Scalar object whose value is the product of self and other.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the product of the value
                  of the Scalar self and the value of other

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.
        """
        new_node = Scalar(self._val, self._jacobian)
        try:
            new_node._val *= other._val
            new_node._jacobian = {k: self._val * other.partial(k)
                                  + v * other._val
                                  for k, v in self._jacobian.items()}
        except:
            new_node._val *= other
            new_node._jacobian = \
                {k: v * other for k, v in self._jacobian.items()}
        return new_node

    def __rmul__(self, other):
        """Return a Scalar object with value self * other."""
        return self * other

    def __truediv__(self, other):
        """
        Return a Scalar object whose value is the quotient of self and other.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the quotient of the value
                  of the Scalar self and the value of other

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.
        """
        new_node = Scalar(self._val, self._jacobian)
        try:
            new_node._val /= other._val
            new_node._jacobian = \
                {k: (v * other._val - self._val * other.partial(k))
                 / (other._val ** 2) for k, v in self._jacobian.items()}
        except AttributeError:
            new_node._val /= other
            new_node._jacobian = \
                {k: v / other for k, v in self._jacobian.items()}
        return new_node

    def __rtruediv__(self, other):
        """
        Return a Scalar object whose value is quotient of other and self.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the quotient of the value
                  of other nad the value of the Scalar self

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.  Additionally, this
        method can assume that other is not an instance of Scalar because
        otherwise the division of other and self would be handled by the
        overloading of __truediv__ for the other object.
        """
        new_node = Scalar(self._val, self._jacobian)
        new_node._val = other / self._val
        new_node._jacobian = \
            {k: other * (-v) / (self._val ** 2)
             for k, v in self._jacobian.items()}
        return new_node

    def __pow__(self, other):
        """
        Return a Scalar object with value self to the power of other.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the value of the Scalar
                  self raised to the power of the value of other

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.
        """
        new_node = Scalar(self._val, self._jacobian)
        try:
            new_node._val **= other._val
            new_node._jacobian = \
                {k: (other._val * v / self._val
                 + np.log(self._val) * other.partial(k))
                 * (self._val ** other._val)
                 for k, v in self._jacobian.items()}
        except AttributeError:
            new_node._val **= other
            new_node._jacobian = \
                {k: other * (self._val ** (other - 1)) * v
                 for k, v in self._jacobian.items()}
        return new_node

    def __rpow__(self, other):
        """
        Return a Scalar object with value other to the power of self.

        INPUTS
        =======
        self: Scalar class instance
        other: either a Scalar object or numeric type constant

        RETURNS
        =======
        new_node: a new Scalar object whose value is the value of other raised
                  to the power of the value of the Scalar self

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object(s) that were used to create this function.  Additionally, this
        method can assume that other is not an instance of Scalar because
        otherwise the exponentiation of other and self would be handled by the
        overloading of __pow__ for the other object.
        """
        new_node = Scalar(self._val, self._jacobian)
        new_node._val = other ** self._val
        new_node._jacobian = \
            {k: (other ** self._val) * np.log(other) * v
             for k, v in self._jacobian.items()}
        return new_node

    def __neg__(self):
        """
        Return a Scalar object with the negated value of self.

        INPUTS
        =======
        self: Scalar class instance

        RETURNS
        =======
        A new Scalar object whose value is the negated value of the Scalar self

        NOTES
        ======
        The Scalar object that is returned by this method has a well defined
        jacobian with respect to all variables in the 'universe' of the Scalar
        object that was used to create this function.
        """
        jacobian = {k: -1 * v for k, v in self._jacobian.items()}
        return Scalar(-1 * self._val, jacobian)
