import numpy as np
from Dotua.nodes.rscalar import rScalar


class rVector():
    """
    Allow user defined variables capable of reverse automatic differentiation.

    rVector objects have a single user defined value and 'private' class
    variables parents and grad_val corresponding to functions defined using
    the given rVector and the current gradient value of the rVector
    respectively.  The parents of rVector are defined via operator
    overloading.  Each time the user creates functions using rVector
    variables, at least one new rVector object is created and assigned as the
    parent of the rVector objects used to create it.
    """

    def __init__(self, vals):
        """
        Return an rVector object with user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        rVector class instance

        NOTES
        ======
        The val class variable is user defined during initialization.  It can
        be accessed directly but it should never be modified.  The parents and
        grad_val class variables are meant to be 'private' and should never be
        accessed or modified directly by users.  Additionally, note that
        parents is a list of tuples (par, val) where par is an rVector
        instance and val is the derivative of the rVector par with respect
        to the rVector self.
        """
        self._val = np.array(vals)
        self._roots = {}
        self._grad_val = np.zeros(len(vals))
        self._rscalars = [rScalar(val) for val in vals]

    def __getitem__(self, idx):
        return self._rscalars[idx]

    def _init_roots(self):
        self._roots[self] = [(None, 1)]

    def eval(self):
        """
        Return the value self rVector object.

        INPUTS
        =======
        self: rVector class instance

        RETURNS
        =======
        self._val: value of the user defined variable, user defined function,
                   or intermediate rVector in the computational grpah
                   represented by the self rVector object

        NOTES
        ======
        rVector does not overload comparison operators so if users desire to
        compare the values of different rVector objects they should do so
        by calling eval on each object to obtain the value.
        """
        return self._val

    def gradient(self, input_var):
        """
        Return the derivative of some function with respect to this rVector.

        INPUTS
        =======
        self: rVector class instance

        RETURNS
        =======
        self._grad_val: numeric type value repesenting the derivative of a
                       function with respect to this rVector variable

        NOTES
        ======
        This function is called by rAutoDiff.partial which dictates which
        function's derivative is being calculated with respect to the
        variable represented by the rVector self.  This method calculates the
        necessary derivative using reverse automatic differentiation by
        recursively finding the derivative of the specified function with
        respect to the given rVector by defining this derivative in terms of
        the rVector objects that represent 'intermediary functions' in the
        implicit computational graph that are defined using the rVector self.
        """
        try:
            for child, val in self._roots[input_var]:
                if child is not None:
                    if child._grad_val.any() == 0:
                        child._grad_val += self._grad_val * val
                    child.gradient(input_var)
        except KeyError:
            raise ValueError("User attempted to differentiate a function " +
                             "respect to a variable on which it is not " +
                             "defined.")

    def __add__(self, other):
        """
        Return an rVector object whose value is the sum of self and other.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_node: a new rVector object whose value is the sum of the value of
                  the rVector self and the value of other

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_child = rVector(self._val)
        try:
            new_child._val = self._val + other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, 1)]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += [(other, 1)]
                except KeyError:
                    new_child._roots[input_var] = [(other, 1)]
        except AttributeError:
            new_child._val = self._val + other
            new_child._roots = {input_var: [(self, 1)]
                                for input_var in self._roots.keys()}
        return new_child

    def __radd__(self, other):
        """Return an rVector object with value self + other."""
        return self + other

    def __sub__(self, other):
        """Return an rVector object with value self - other."""
        return self + (-other)

    def __rsub__(self, other):
        """Return an rVector object with value other - self."""
        return -self + other

    def __mul__(self, other):
        """
        Return an rVector object whose value is the product of self and other.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_rVector: a new rVector object whose value is the product of the value
                  of the rVector self and the value of other

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_child = rVector(self._val)
        try:
            new_child._val = self._val * other._val
            # For each input variable on which self is defined
            new_child._roots = {input_var: [(self, other._val)]
                                for input_var in self._roots.keys()}

            for input_var in other._roots.keys():
                try:
                    new_child._roots[input_var] += [(other, self._val)]
                except KeyError:
                    new_child._roots[input_var] = [(other, self._val)]
        except AttributeError:
            new_child._val = self._val * other
            new_child._roots = {input_var: [(self, other)]
                                for input_var in self._roots.keys()}
        return new_child

    def __rmul__(self, other):
        """Return an rVector object with value self * other."""
        return self * other

    def __truediv__(self, other):
        """
        Return an rVector object whose value is the quotient of self and other.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_rVector: a new rVector object whose value is the quotient of the value
                  of the rVector self and the value of other

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_child = rVector(self._val)
        try:
            new_child._val = self._val / other._val
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
            new_child._val = self._val / other
            new_child._roots = {input_var: [(self, 1 / other)]
                                for input_var in self._roots.keys()}
        return new_child

    def __rtruediv__(self, other):
        """
        Return an rVector object whose value is the quotient of other and self.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_rVector: a new rVector object whose value is the quotient of the value
                  of other nad the value of the rVector self

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.   Additionally,
        this method can assume that other is not an instance of rVector because
        otherwise the division of other and self would be handled by the
        overloading of __truediv__ for the other object.
        """
        new_child = rVector(other / self._val)
        new_child._roots = {input_var: [(self, -other / (self._val ** 2))]
                            for input_var in self._roots.keys()}
        return new_child

    def __pow__(self, other):
        """
        Return an rVector object with value self to the power of other.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_rVector: a new rVector object whose value is the value of the rVector
                  self raised to the power of the value of other

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.
        """
        new_child = rVector(self._val)
        try:
            new_child._val = self._val ** other._val
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
            new_child._val = self._val ** other
            new_child._roots = {input_var: [(self, other *
                                self._val ** (other - 1))]
                                for input_var in self._roots.keys()}
        return new_child

    def __rpow__(self, other):
        """
        Return an rVector object with value other to the power of self.

        INPUTS
        =======
        self: rVector class instance
        other: either a rVector object or numeric type constant

        RETURNS
        =======
        new_rVector: a new rVector object whose value is the value of other raised
                  to the power of the value of the rVector self

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self (and of other if other is an rVector
        instance).  Specifically, this relationship is stored as a tuple
        (par, val) where par is the new_parent rVector instance and val is
        the derivative of new_parent with respect to its child rVector object.
        Storing relationships in this way facilitates the computation of
        gradients through reverse automatic differentiation.  Additionally,
        this method can assume that other is not an instance of rVector because
        otherwise the exponentiation of other and self would be handled by the
        overloading of __pow__ for the other object.
        """
        new_child = rVector(other ** self._val)
        new_child._roots = {input_var:
                            [(self, other ** self._val * np.log(other))]
                            for input_var in self._roots.keys()}
        return new_child

    def __neg__(self):
        """
        Return an rVector object with the negated value of self.

        INPUTS
        =======
        self: rVector class instance

        RETURNS
        =======
        A new rVector object whose value is the negated value of the rVector
        self

        NOTES
        ======
        The rVector object that is returned by this method is assigned as the
        parent of the rVector self.  Specifically, this relationship is stored
        as a tuple (par, val) where par is the new_parent rVector instance and
        val is the derivative of new_parent with respect to its child rVector
        object.  Storing relationships in this way facilitates the computation
        of gradients through reverse automatic differentiation.
        """
        new_child = rVector(-self._val)
        new_child._roots = {input_var: [(self, -1)]
                            for input_var in self._roots.keys()}
        return new_child
