import math
import numpy as np
from Dotua.nodes.rscalar import rScalar


class rOperator:
    """Returns a new rScalar object subject to the operator and propagates the
    value and derivative according to reverse mode autodifferentiation.

    The example below pertains to an action on an autodiff rScalar object: x

    Example Usage
    -------------

        $ import rautodiff.rautodiff as rad
        $ x = rad.create_scalar(0)
        $ from rautodiff.roperator import rOperator as rop
        $ y = rop.sin(x)

    """
    @staticmethod
    def sin(x):
        """
        Returns a constant or rScalar object that is the sine of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the sine function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.sin(x.val))
            x.parents.append((new_parent, np.cos(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.sin(x)

    @staticmethod
    def cos(x):
        """
        Returns a constant or rScalar object that is the cosine of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the cosine function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.cos(x.val))
            x.parents.append((new_parent, -np.sin(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.cos(x)

    @staticmethod
    def tan(x):
        """
        Returns a constant or rScalar object that is the tangent of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the tangent function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.tan(x.val))
            x.parents.append((new_parent, np.arccos(x.val)**2))
            return new_parent

        except AttributeError: # if constant
            return np.tan(x)

    @staticmethod
    def arcsin(x):
        """
        Returns a constant or rScalar object that is the arcsine of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arcsine function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arcsin(x.val))
            x.parents.append((new_parent, -np.arcsin(x.val)*np.arctan(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.arcsin(x)

    @staticmethod
    def arccos(x):
        """
        Returns a constant or rScalar object that is the arccosine of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arccosine function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arccos(x.val))
            x.parents.append((new_parent, np.arccos(x.val)*np.tan(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.arccos(x)

    @staticmethod
    def arctan(x):
        """
        Returns a constant or rScalar object that is the arctan of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arctan function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arctan(x.val))
            x.parents.append((new_parent, -np.arcsin(x.val)**2))
            return new_parent

        except AttributeError: # if constant
            return np.arctan(x)

    @staticmethod
    def sinh(x):
        """
        Returns a constant or rScalar object that is the sinh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the sinh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.sinh(x.val))
            x.parents.append((new_parent, np.cosh(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.sinh(x)

    @staticmethod
    def cosh(x):
        """
        Returns a constant or rScalar object that is the cosh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the cosh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.cosh(x.val))
            x.parents.append((new_parent, np.sinh(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.cosh(x)

    @staticmethod
    def tanh(x):
        """
        Returns a constant or rScalar object that is the tanh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the tanh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.tanh(x.val))
            x.parents.append((new_parent, 1-np.tanh(x.val)**2))
            return new_parent

        except AttributeError: # if constant
            return np.tanh(x)

    @staticmethod
    def arcsinh(x):
        """
        Returns a constant or rScalar object that is the arcsinh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arcsinh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arcsinh(x.val))
            x.parents.append((new_parent, -np.arcsinh(x.val)*np.arctanh(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.arcsinh(x)

    @staticmethod
    def arccosh(x):
        """
        Returns a constant or rScalar object that is the arccosh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arccosh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arccosh(x.val))
            x.parents.append((new_parent, -np.arccosh(x.val)*np.tanh(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.arccosh(x)

    @staticmethod
    def arctanh(x):
        """
        Returns a constant or rScalar object that is the arctanh of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the arctanh function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.arctanh(x.val))
            x.parents.append((new_parent, 1-np.arctanh(x.val)**2))
            return new_parent

        except AttributeError: # if constant
            return np.arctanh(x)

    @staticmethod
    def exp(x):
        """
        Returns a constant or rScalar object that is the exponential of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the exponential function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(np.exp(x.val))
            x.parents.append((new_parent, np.exp(x.val)))
            return new_parent

        except AttributeError: # if constant
            return np.exp(x)

    @staticmethod
    def log(x, base=np.exp(1)):
        """
        Returns a constant or rScalar object that is the log of the user specified value.

        INPUTS
        =======
        val: real valued numeric type

        RETURNS
        =======
        constant or rScalar class instance

        NOTES
        ======
        If the input is a constant, a constant is returned with the operation applied. If the input
        is an rScalar object, this method creates a parent node by wrapping the input value in the
        operator function, in this case the log function. The parent is then linked to the child
        for later backpropagation and the parent is returned as a new rScalar object.
        """
        try:
            new_parent = rScalar(math.log(x.val, base))
            x.parents.append((new_parent, (x.val * math.log(base))**(-1)))
            return new_parent

        except AttributeError: # if constant
            return math.log(x, base)
