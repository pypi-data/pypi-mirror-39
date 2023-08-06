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
        self._val = val
        self._roots = {}  # keys are input rScalars, vals are lists intemediary rScalars
        self._grad_val = 0

    def _init_roots(self):
        self._roots[self] = [(None, 1)]

    def eval(self):
        """
        Return the value self rScalar object.

        INPUTS
        =======
        self: rScalar class instance

        RETURNS
        =======
        self._val: value of the user defined variable, user defined function,
                   or intermediate rScalar in the computational grpah represented
                   by the self rScalar object

        NOTES
        ======
        rScalar does not overload comparison operators so if users desire to
        compare the values of different rScalar objects they should do so
        by calling eval on each object to obtain the value.
        """
        return self._val

    def gradient(self, input_var):
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
        try:
            for child, val in self._roots[input_var]:
                if child is not None:
                    if child._grad_val == 0:
                        child._grad_val += self._grad_val * val
                    child.gradient(input_var)

        except KeyError:
            raise ValueError("User attempted to differentiate a function " +
                             "respect to a variable on which it is not " +
                             "defined.")

    def __add__(self, other):
        """
        Return an rScalar object whose value is the sum of self and other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_rScalar: a new rScalar object whose value is the sum of the value of
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
        new_child = rScalar(self._val)
        try:
            new_child._val += other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, 1)]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += [(other, 1)]
                except KeyError:
                    new_child._roots[input_var] = [(other, 1)]
        except AttributeError:
            new_child._val += other
            new_child._roots = {input_var: [(self, 1)]
                                for input_var in self._roots.keys()}
        return new_child

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
        new_rScalar: a new rScalar object whose value is the product of the value
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
        new_child = rScalar(self._val)
        try:
            new_child._val *= other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, other._val)]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += [(other, self._val)]
                except KeyError:
                    new_child._roots[input_var] = [(other, self._val)]
        except AttributeError:
            new_child._val *= other
            new_child._roots = {input_var: [(self, other)]
                                for input_var in self._roots.keys()}
        return new_child

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
        new_rScalar: a new rScalar object whose value is the quotient of the value
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
        new_child = rScalar(self._val)
        try:
            new_child._val /= other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, 1 / other._val)]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += \
                        [(other, -self._val / (other._val ** 2))]
                except KeyError:
                    new_child._roots[input_var] = \
                        [(other, -self._val / (other._val ** 2))]
        except AttributeError:
            new_child._val /= other
            new_child._roots = {input_var: [(self, 1 / other)]
                                for input_var in self._roots.keys()}
        return new_child

    def __rtruediv__(self, other):
        """
        Return an rScalar object whose value is the quotient of other and self.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_rScalar: a new rScalar object whose value is the quotient of the value
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
        new_child = rScalar(other / self._val)
        new_child._roots = {input_var: [(self, -other / (self._val ** 2))]
                            for input_var in self._roots.keys()}
        return new_child


    def __pow__(self, other):
        """
        Return an rScalar object with value self to the power of other.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_rScalar: a new rScalar object whose value is the value of the rScalar
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
        new_child = rScalar(self._val)
        try:
            new_child._val **= other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, other._val *
                                self._val ** (other._val - 1))]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += \
                        [(other, self._val ** other._val * np.log(self._val))]
                except KeyError:
                    new_child._roots[input_var] = \
                        [(other, self._val ** other._val * np.log(self._val))]
        except AttributeError:
            new_child._val **= other
            new_child._roots = {input_var: [(self, other *
                                self._val ** (other - 1))]
                                for input_var in self._roots.keys()}
        return new_child

    def __rpow__(self, other):
        """
        Return an rScalar object with value other to the power of self.

        INPUTS
        =======
        self: rScalar class instance
        other: either a rScalar object or numeric type constant

        RETURNS
        =======
        new_rScalar: a new rScalar object whose value is the value of other raised
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
        new_child = rScalar(other ** self._val)
        new_child._roots = {input_var:
                            [(self, other ** self._val * np.log(other))]
                            for input_var in self._roots.keys()}
        return new_child

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
        new_child = rScalar(-self._val)
        new_child._roots = {input_var: [(self, -1)]
                            for input_var in self._roots.keys()}
        return new_child
