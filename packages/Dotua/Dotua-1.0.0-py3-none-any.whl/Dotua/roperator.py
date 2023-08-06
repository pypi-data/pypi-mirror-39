import math
import numpy as np
from Dotua.nodes.rscalar import rScalar
from Dotua.nodes.rvector import rVector


class rOperator:
    """Returns a new rScalar/rVector object subject to the operator and propagates the
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
        Returns a constant/rScalar/rVector object that is the sine of the user specified value.

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
            x._rscalars
            new_child = rVector(np.sin(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.cos(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.sin(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.cos(x._val))]
                return new_child
            except AttributeError:
                return np.sin(x)

    @staticmethod
    def cos(x):
        """
        Returns a constant/rScalar/rVector object that is the cosine of the user specified value.

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
            x._rscalars
            new_child = rVector(np.cos(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, -np.sin(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.cos(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, -np.sin(x._val))]
                return new_child
            except AttributeError:
                return np.cos(x)

    @staticmethod
    def tan(x):
        """
        Returns a constant/rScalar/rVector object that is the tangent of the user specified value.

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
            x._rscalars
            new_child = rVector(np.tan(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.arccos(x._val)**2)]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.tan(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.arccos(x._val)**2)]
                return new_child

            except AttributeError:
                return np.tan(x)

    @staticmethod
    def arcsin(x):
        """
        Returns a constant/rScalar/rVector object that is the arcsine of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arcsin(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, -np.arcsin(x._val)*np.arctan(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arcsin(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, -np.arcsin(x._val)*np.arctan(x._val))]
                return new_child

            except AttributeError:
                return np.arcsin(x)

    @staticmethod
    def arccos(x):
        """
        Returns a constant/rScalar/rVector object that is the arccosine of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arccos(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.arccos(x._val)*np.tan(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arccos(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.arccos(x._val)*np.tan(x._val))]
                return new_child

            except AttributeError:
                return np.arccos(x)

    @staticmethod
    def arctan(x):
        """
        Returns a constant/rScalar/rVector object that is the arctan of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arctan(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, -np.arcsin(x._val)**2)]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arctan(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, -np.arcsin(x._val)**2)]
                return new_child

            except AttributeError:
                return np.arctan(x)

    @staticmethod
    def sinh(x):
        """
        Returns a constant/rScalar/rVector object that is the sinh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.sinh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.cosh(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.sinh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.cosh(x._val))]
                return new_child

            except AttributeError:
                return np.sinh(x)

    @staticmethod
    def cosh(x):
        """
        Returns a constant/rScalar/rVector object that is the cosh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.cosh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.sinh(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.cosh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.sinh(x._val))]
                return new_child

            except AttributeError:
                return np.cosh(x)

    @staticmethod
    def tanh(x):
        """
        Returns a constant/rScalar/rVector object that is the tanh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.tanh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, (1-np.tanh(x._val)**2))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.tanh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, (1-np.tanh(x._val)**2))]
                return new_child

            except AttributeError:
                return np.tanh(x)

    @staticmethod
    def arcsinh(x):
        """
        Returns a constant/rScalar/rVector object that is the arcsinh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arcsinh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, -np.arcsinh(x._val)*np.arctanh(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arcsinh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, -np.arcsinh(x._val)*np.arctanh(x._val))]
                return new_child

            except AttributeError:
                return np.arcsinh(x)

    @staticmethod
    def arccosh(x):
        """
        Returns a constant/rScalar/rVector object that is the arccosh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arccosh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, -np.arccosh(x._val)*np.tanh(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arccosh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, -np.arccosh(x._val)*np.tanh(x._val))]
                return new_child

            except AttributeError:
                return np.arccosh(x)

    @staticmethod
    def arctanh(x):
        """
        Returns a constant/rScalar/rVector object that is the arctanh of the user specified value.

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
            x._rscalars
            new_child = rVector(np.arctanh(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, (1-np.arctanh(x._val)**2))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.arctanh(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, (1-np.arctanh(x._val)**2))]
                return new_child

            except AttributeError:
                return np.arctanh(x)

    @staticmethod
    def exp(x):
        """
        Returns a constant/rScalar/rVector object that is the exponential of the user specified value.

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
            x._rscalars
            new_child = rVector(np.exp(x._val))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, np.exp(x._val))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(np.exp(x._val))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, np.exp(x._val))]
                return new_child

            except AttributeError:
                return np.exp(x)

    @staticmethod
    def log(x, base=np.exp(1)):
        """
        Returns a constant/rScalar/rVector object that is the log of the user specified value.

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
            x._rscalars
            new_child = rVector(np.log(x._val) / np.log(base))
            for input_var in x._roots.keys():
                new_child._roots[input_var] = [(x, 1 / (x._val * math.log(base)))]
            return new_child
        except AttributeError:
            try:
                new_child = rScalar(math.log(x._val, base))
                for input_var in x._roots.keys():
                    new_child._roots[input_var] = [(x, 1 / (x._val * math.log(base)))]
                return new_child

            except AttributeError:
                return math.log(x, base)
