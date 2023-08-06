import numpy as np


class rScalar():
    """
    Allow user defined variables capable of reverse audotmatic differentiation.

    rScalar objects have a single user defined value and 'private' class
    variables parents and grad_val corresponding to functions defined using
    the given rScalar and the current gradient value of the rScalar
    respectively.  The parents of rScalar are defined via operator
    overloading.  Each time the user crreates functions using rScalar
    variables, at least one new rScalar object is created and assigned as the
    parent of the rScalar objects used to create it.
    """

    def __init__(self, val):
        """
        Return an rScalar object with user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        rScalar class instance

        NOTES
        ======
        The val class variable is user defined during initialization.  It can
        be accessed directly but it should never be modified.  The parents and
        grad_val class variables are meant to be 'private' and should never be
        accessed or modified directly by users.  Additionally, note that
        parents is a list of tuples (par, val) where par is an rScalar
        instance and val is the derivative of the rScalar par with respect
        to the rScalar self.
        """
        self.val = val
        self.parents = []
        self.grad_val = None

    def eval(self):
        """
        Return the value self rScalar object.

        INPUTS
        =======
        self: rScalar class instance

        RETURNS
        =======
        self._val: value of the user defined variable, user defined function,
                   or intermediate node in the computational grpah represented
                   by the self rScalar object

        NOTES
        ======
        rScalar does not overload comparison operators so if users desire to
        compare the values of different rScalar objects they should do so
        by calling eval on each object to obtain the value.
        """
        return self.val

    def gradient(self):
        """
        Return the derivative of some function with respect to this rScalar.

        INPUTS
        =======
        self: rScalar class instance

        RETURNS
        =======
        self.grad_val: numeric type value repesenting the derivative of a
                       function with respect to this rScalar variable

        NOTES
        ======
        This function is called by rAutoDiff.partial which dictates which
        function's derivative is being calculated with respect to the
        variable represented by the rScalar self.  This method calculates the
        necessary derivative using reverse automatic differentiation by
        recursively finding the derivative of the specified function with
        respect to the given rScalar by defining this derivative in terms of
        the rScalar objects that represent 'intermediary functions' in the
        implicit computational graph that are defined using the rScalar self.
        """
        if self.grad_val is None:
            self.grad_val = 0
            for parent, val in self.parents:
                self.grad_val += parent.gradient() * val
        return self.grad_val
        
    def __add__(self, other):
        """
        Return an rScalar object whose value is the sum of self and other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the sum of the value of
                  the rScalar self and the value of other

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_parent = rScalar(self.val)
        try:
            new_parent.val += other.val
            self.parents.append((new_parent, 1))
            other.parents.append((new_parent, 1))
        except AttributeError:
            new_parent.val += other
            self.parents.append((new_parent, 1))
        return new_parent

    def __radd__(self, other):
        """Return an rScalar object with value self + other."""
        return self + other

    def __sub__(self, other):
        """Return an rScalar object with value self - other."""
        return self + (-other)

    def __rsub__(self, other):
        """Return an rScalar object with value other - self."""
        return -self + other

    def __mul__(self, other):
        """
        Return an rScalar object whose value is the product of self and other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the product of the value
                  of the rScalar self and the value of other

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_parent = rScalar(self.val)
        try:
            new_parent.val *= other.val
            self.parents.append((new_parent, other.val))
            other.parents.append((new_parent, self.val))
        except AttributeError:
            new_parent.val *= other
            self.parents.append((new_parent, other))
        return new_parent

    def __rmul__(self, other):
        """Return an rScalar object with value self * other."""
        return self * other

    def __truediv__(self, other):
        """
        Return an rScalar object whose value is the quotient of self and other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the quotient of the value
                  of the rScalar self and the value of other

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_parent = rScalar(self.val)
        try:
            new_parent.val /= other.val
            self.parents.append((new_parent, 1 / other.val))
            other.parents.append((new_parent, -self.val / (other.val ** 2)))
        except AttributeError:
            new_parent.val /= other
            self.parents.append((new_parent, 1 / other))
        return new_parent

    def __rtruediv__(self, other):
        """
        Return an rScalar object whose value is the quotient of other and self.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the quotient of the value
                  of other nad the value of the rScalar self

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.   Additionally,
        this method can assume that other is not an instance of rScalar because
        otherwise the division of other and self would be handled by the
        overloading of __truediv__ for the other object.
        """
        new_parent = rScalar(self.val)
        new_parent.val = other / new_parent.val
        self.parents.append((new_parent, -other / (self.val ** 2)))
        return new_parent

    def __pow__(self, other):
        """
        Return an rScalar object with value self to the power of other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the value of the rScalar
                  self raised to the power of the value of other

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_parent = rScalar(self.val)
        try:
            new_parent.val **= other.val
            self.parents.append((new_parent,
                                other.val * self.val ** (other.val - 1)))
            other.parents.append((new_parent,
                                 self.val ** other.val * np.log(self.val)))
        except AttributeError:
            new_parent.val **= other
            self.parents.append((new_parent, other * self.val ** (other - 1)))
        return new_parent

    def __rpow__(self, other):
        """
        Return an rScalar object with value other to the power of self.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_node: a new rScalar object whose value is the value of other raised
                  to the power of the value of the rScalar self

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self (and of other if other is an rScalar
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rScalar instance and val is
        the derivative of new_parent with respect to its child rScalar object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.  Additionally,
        this method can assume that other is not an instance of rScalar because
        otherwise the exponentiation of other and self would be handled by the
        overloading of __pow__ for the other object.
        """
        new_parent = rScalar(self.val)
        new_parent.val = other ** self.val
        self.parents.append((new_parent, other ** self.val * np.log(other)))
        return new_parent

    def __neg__(self):
        """
        Return an rScalar object with the negated value of self.

        INPUTS
        =======
        self: rScalar class instance

        RETURNS
        =======
        A new rScalar object whose value is the negated value of the rScalar
        self

        NOTES
        ======
        The rScalar object that is returned by this method is assigned as the
        parent of the rScalar self.  Specifically, this relationship is stored
        as a tuple (par, val) where par is the new_parent rScalar instance and
        val is the derivative of new_parent with respect to its child rScalar
        object.  Storing relationships in this way facilitates the computation
        of gradients through reverse automatic differentiation.
        """
        new_parent = rScalar(-self.val)
        self.parents.append((new_parent, -1))
        return new_parent
