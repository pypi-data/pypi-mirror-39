import numpy as np
from .node import Node


class Vector(Node):
    def __init__(self, val, der = 1):
        """
        Returns a Vector variable with user defined value and derivative

        INPUTS
        =======
        val: list of floats, compulsory
            Value of the Vector variable
        der: float, optional, default value is 1
            Derivative of the Vector variable/function of a variable

        RETURNS
        ========
        Vector class instance

        NOTES
        =====
        PRE:
            - val and der have numeric type and val must be a list
            - two or fewer inputs
        POST:
            returns a Vector class instance with value = val and derivative = der
        """
        self._val = np.array(val)
        self._jacobian = der * np.eye(len(val))

    def __getitem__(self, idx):
        return Element(self._val[idx], self._jacobian[idx], self)

    def __add__(self, other):
        """
        Returns the sum of self and other

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        try:
            value = self._val + other._val # If other is a constant, then there will be an attribute error
        except AttributeError:
            value = self._val + other
            try:
                dict_self = self._dict # If self is a user defined variable, then there will be an attribute error
                new = Vector(value, self._jacobian)
                new._dict = dict_self # When self is a complex function and other is a constant, the derivatives of the sum is just the derivatives of self
                return new
            except AttributeError:
                derivative = Counter() # If self is a user defined variable, then we add a dictionary of derivatives of user defined variables to the result Vector variable
                derivative[self] = self._jacobian
                new = Vector(value, self._jacobian)
                new._dict = derivative
                return new
        else:
            try:
                dict_self = self._dict
            except AttributeError:
                dict_self = Counter()
                dict_self[self] = self._jacobian
                try:
                    dict_other = other._dict # If other is a user defined variable, then there will be an attribute error
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian  # If other is a user defined variable, then we initiate a Counter dictionary for it
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] + dict_other[key] # Then the derivatives of result Vector variable are sums of derivatives of self and derivatives of other
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] + dict_other[key] # If self and other are both complex functions, then the derivatives of result Vector variable are sums of derivatives of self and derivatives of other
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
            else:
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] + dict_other[key]
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] + dict_other[key]
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new


    def __radd__(self, other):
        """
        Returns the sum of self and other

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        return self + other

    def __sub__(self, other):
        """
        Returns the difference of self and other

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        try:
            value = self._val - other._val # If other is a constant, then there will be an attribute error
        except AttributeError:
            value = self._val - other
            try:
                dict_self = self._dict # If self is a user defined variable, then there will be an attribute
                new = Vector(value, self._jacobian)
                new._dict = dict_self
                return new
            except AttributeError:
                derivative = Counter()
                derivative[self] = self._jacobian
                new = Vector(value, self._jacobian)
                new._dict = derivative # When self is a complex function and other is a constant, the derivatives of the result variable is just the derivatives of self
                return new
        else:
            try:
                dict_self = self._dict
            except AttributeError:
                dict_self = Counter() # If self is a user defined variable, then we add a dictionary of derivatives of user defined variables to the result Vector variable
                dict_self[self] = self._jacobian
                try:
                    dict_other = other._dict # If other is a user defined variable, then there will be an attribute error
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian # If other is a user defined variable, then we initiate a Counter dictionary for it
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] - dict_other[key] # Then the derivatives of result Vector variable are differences of derivatives of self and derivatives of other
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] - dict_other[key] # If self and other are both complex functions, then the derivatives of result Vector variable are differences of derivatives of self and derivatives of other
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
            else:
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] - dict_other[key]
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] - dict_other[key]
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new

    def __rsub__(self, other):
        """
        Returns the difference of other and self

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        return self.__neg__() + other

    def __mul__(self, other):
        """
        Returns the product of other and self

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        try:
            val_other = other._val # If other is a constant, then there will be an attribute error
            value = self._val * other._val
        except AttributeError:
            val_other = other
            value = self._val * other
            try:
                dict_self = self._dict # If self is a user defined variable, then there will be an attribute
                for key in dict_self.keys():
                    dict_self[key] = dict_self[key] * val_other
                new = Vector(value, self._jacobian)
                new._dict = dict_self # When self is a complex function and other is a constant, the derivatives of the result variable is just the derivatives of self
                return new
            except AttributeError:
                derivative = Counter() # If self is a user defined variable, then we add a dictionary of derivatives of user defined variables to the result Vector variable
                derivative[self] = self._jacobian * val_other
                new = Vector(value, self._jacobian)
                new._dict = derivative
                return new
        else:
            try:
                dict_self = self._dict
            except AttributeError:
                dict_self = Counter()
                dict_self[self] = self._jacobian
                try:
                    dict_other = other._dict # If other is a user defined variable, then there will be an attribute error
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian # If other is a user defined variable, then we initiate a Counter dictionary for it
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] * val_other + dict_other[key] * self._val # Then the derivatives of result Vector variable are sum of products of derivatives and values
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] * val_other + dict_other[key] * self._val # If self and other are both complex functions,then the derivatives of result Vector variable are sum of products of derivatives and values
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
            else:
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] * val_other + dict_other[key] * self._val
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] * val_other + dict_other[key] * self._val
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new

    def __rmul__(self, other):
        """
        Returns the product of other and self

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        return self * other

    def __truediv__(self, other):
        """
        Returns the quotient of self and other

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        try:
            val_other = other._val
            value = self._val / val_other
        except AttributeError:
            val_other = other
            value = self._val / val_other
            try:
                dict_self = self._dict
                for key in dict_self.keys():
                    dict_self[key] = dict_self[key] / val_other
                new = Vector(value, self._jacobian)
                new._dict = dict_self
                return new
            except AttributeError:
                derivative = Counter()
                derivative[self] = self._jacobian / val_other
                new = Vector(value, self._jacobian)
                new._dict = derivative
                return new
        else:
            value = self._val / other._val
            try:
                dict_self = self._dict
            except AttributeError:
                dict_self = Counter()
                dict_self[self] = self._jacobian
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] / val_other - dict_other[key] * self._val / (val_other * val_other)
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] / val_other - dict_other[key] * self._val / (val_other * val_other)
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
            else:
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] / val_other - dict_other[key] * self._val / (val_other * val_other)
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = dict_self[key] / val_other - dict_other[key] * self._val / (val_other * val_other)
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new

    def __rtruediv__(self, other):
        """
        Returns the quotient of other and self

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance

        NOTES
        ======
        This method can assume that other is not an instance of Vector because
        otherwise the division of other and self would be handled by the
        overloading of __truediv__ for the other object.
        """
        val_other = other
        value = val_other / self._val
        try:
            dict_self = self._dict
            for key in dict_self.keys():
                dict_self[key] = - val_other * dict_self[key] / (self._val * self._val)
            new = Vector(value, self._jacobian)
            new._dict = dict_self
            return new
        except AttributeError:
            derivative = Counter()
            derivative[self] = - val_other * self._jacobian / (self._val * self._val)
            new = Vector(value, self._jacobian)
            new._dict = derivative
            return new

    def __pow__(self, other):
        """
        Returns the other'th power of self

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        try:
            val_other = other._val
            value = np.power(self._val, val_other)
        except AttributeError:
            val_other  = other
            value = np.power(self._val, val_other)
            try:
                dict_self = self._dict
                for key in dict_self.keys():
                    dict_self[key] = dict_self[key] * val_other * self._val ** (val_other - 1)
                new = Vector(value, self._jacobian)
                new._dict = dict_self
                return new
            except AttributeError:
                derivative = Counter()
                derivative[self] = self._jacobian * val_other * self._val ** (val_other - 1)
                new = Vector(value, self._jacobian)
                new._dict = derivative
                return new
        else:
            try:
                dict_self = self._dict
            except AttributeError:
                dict_self = Counter()
                dict_self[self] = self._jacobian
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = self._val ** val_other * (val_other / self._val * dict_self[key] + np.log(self._val) * dict_other[key])
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = self._val ** val_other * (val_other / self._val * dict_self[key] + np.log(self._val) * dict_other[key])
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
            else:
                try:
                    dict_other = other._dict
                except AttributeError:
                    dict_other = Counter()
                    dict_other[other] = other._jacobian
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = self._val ** val_other * (val_other / self._val * dict_self[key] + np.log(self._val) * dict_other[key])
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new
                else:
                    derivative = Counter()
                    lst = list(dict_self.keys()) + list(dict_other.keys())
                    for key in lst:
                        derivative[key] = self._val ** val_other * (val_other / self._val * dict_self[key] + np.log(self._val) * dict_other[key])
                    new = Vector(value, self._jacobian)
                    new._dict = derivative
                    return new

    def __rpow__(self, other):
        """
        Returns the self'th power of other

        INPUTS
        =======
        self: this Vector class instance, compulsory
        other: constant or Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance

        NOTES
        ======
        This method can assume that other is not an instance of Vector because
        otherwise the exponentiation of other and self would be handled by the
        overloading of __pow__ for the other object.
        """
        val_other  = other
        value = np.power(val_other, self._val)
        try:
            dict_self = self._dict
            for key in dict_self.keys():
                dict_self[key] = val_other ** self._val * np.log(val_other) * dict_self[key]
            new = Vector(value, self._jacobian)
            new._dict = dict_self
            return new
        except AttributeError:
            derivative = Counter()
            derivative[self] = val_other ** self._val * np.log(val_other) * self._jacobian
            new = Vector(value, self._jacobian)
            new._dict = derivative
            return new

    def __neg__(self):
        """
        Returns the product of -1 and self

        INPUTS
        =======
        self: this Vector class instance, compulsory

        RETURNS
        ========
        Vector class instance
        """
        value = - self._val
        derivative = - self._jacobian
        new = Vector(value, derivative)
        try:
            dict_self = self._dict
        except AttributeError:
            dict_self = Counter()
            dict_self[self] = derivative
            new._dict = dict_self
            return new
        else:
            for key in dict_self.keys():
                dict_self[key] = - dict_self[key]
            new._dict = dict_self
            return new

    def __repr__(self):
        """
        Returns a description about the Vector variable class instance

        INPUTS
        =======
        self: this Vector class instance, compulsory

        RETURNS
        ========
        description about the Scalar variable class instance: string
        """
        representation = 'Vector variable with value {}'.format(self._val)
        return representation

    def getDerivative(self, x):
        """ Returns the derivative of function self of variable x

        INPUTS
        =======
        self: this Vector class instance, compulsory
        x: user defined variable, compulsory

        RETURNS
        ========
        derivative of function self of user defined variable x: float

        NOTES
        =====
        PRE:
            - x must be user defined variable
        POST:
            - returns a float derivative
        """
        try:
            d = sum(self._dict[x])
        except Exception:
            if self == x:
                return sum(self._jacobian)
            else:
                return 0
        else:
            return d

    def eval(self):
        return list(self._val)

class Element():
    def __init__(self, val, der, vector):
        """
        Returns Element class instance

        INPUTS
        =======
        self: this  class instance, compulsory
        val: values of Element class instnaces
        der: derivatives of Element class instances
        vector: vector to which the Element class instances belong

        RETURNS
        ========
        a list of Element class instance
        """

        self._val = val
        self._der = der
        self._vector = vector

    def __add__(self, other):
        """
        Returns the sum of the two Element class instances

        INPUTS
        =======
        self: this class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        try:
            value = self._val + other._val
            derivative = self._der + other._der
        except AttributeError:
            value = self._val + other
            derivative = self._der
            return Element(value, derivative, self._vector)
        else:
            if self._vector == other._vector:
                return Element(value, derivative, self._vector)
            else:
                print('Elements from different vectors are not allowed to go together')
                raise TypeError

    def __radd__(self, other):
        """
        Returns the sum of the two Element class instances

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        return self + other

    def __neg__(self):
        """
        Returns the product of -1 and this Element class instance

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        return Element(- self._val, - self._der, self._vector)

    def __sub__(self, other):
        """
        Returns the difference of the two Element class instances

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        try:
            value  = self._val - other._val
        except AttributeError:
            return Element(self._val - other, self._der, self._vector)
        else:
            if self._vector == other._vector:
                return self + other.__neg__()
            else:
                print('Elements from different vectors are not allowed to go together')
                raise TypeError


    def __rsub__(self, other):
        """
        Returns the difference of the two Element class instances

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        return self.__neg__() + other

    def __mul__(self, other):
        """
        Returns the product of the two Element class instances

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        try:
            value = self._val * other._val
            derivative = self._der * other._val + self._val * other._der
        except AttributeError:
            value = self._val * other
            derivative = self._der * other
            return Element(value, derivative, self._vector)
        else:
            if self._vector == other._vector:
                return Element(value, derivative, self._vector)
            else:
                print('Elements from different vectors are not allowed to go together')
                raise TypeError

    def __rmul__(self, other):
        """
        Returns the sum of the two Element class instances

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        return self * other

    def __truediv__(self, other):
        """
        Returns the quotient of self devided by other

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        try:
            val_other = other._val
        except AttributeError:
            val_other = other
            value = self._val / val_other
            return Element(value, self._der / val_other, self._vector)
        else:
            if self._vector == other._vector:
                val_other = other._val
                value = self._val / val_other
                return Element(value, self._der / val_other - other._der * self._val / (val_other * val_other), self._vector)
            else:
                print('Elements from different vectors are not allowed to go together')
                raise TypeError

    def __rtruediv__(self, other):
        """
        Returns the quotient of other devided by self

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance

        NOTES
        ======
        This method can assume that other is not an instance of Vector because
        otherwise the division of other and self would be handled by the
        overloading of __truediv__ for the other object.
        """
        val_other = other
        value = val_other / self._val
        return Element(value, - val_other * self._der / (self._val * self._val), self._vector)


    def __repr__(self):
        """
        Returns representation of Element class

        INPUTS
        =======
        self: this  class instance, compulsory

        RETURNS
        ========
        a representation of the Element class
        """
        representation = 'Vector Element with value {} and derivative {}'.format(self._val, self._der)
        return representation

    def __pow__(self, other):
        """
        Returns the other's th power of self

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance
        """
        try:
            val_other = other._val
        except AttributeError:
            val_other  = other
            return Element(self._val ** val_other, val_other * self._val ** (val_other - 1) * self._der, self._vector)
        else:
            if self._vector == other._vector:
                return Element(self._val ** val_other, self._val ** val_other * (val_other / self._val * self._der + np.log(self._val) * other._der), self._vector)
            else:
                print("Elements from different vectors are not allowed to go together")

    def __rpow__(self, other):
        """
        Returns the self's th power of other

        INPUTS
        =======
        self: this  class instance, compulsory
        other: constant or Element class instance, compulsory

        RETURNS
        ========
        Element class instance

        NOTES
        ======
        This method can assume that other is not an instance of Vector because
        otherwise the exponentiation of other and self would be handled by the
        overloading of __pow__ for the other object.
        """
        val_other  = other
        return Element(val_other ** self._val, val_other ** self._val * np.log(val_other) * self._der, self._vector)

    def eval(self):
        """
        Returns value and derivative of Element class instance

        INPUTS
        =======
        self: this  class instance, compulsory

        RETURNS
        ========
        a tuple of value and derivative of this Element class instance
        """
        return (self._val, list(self._der))


class Counter(dict):
    """
    Data structure for storing derivatives of a function, which is a subclass
    of dict
    """
    
    def __getitem__(self, idx):
        """	It will give 0 if the key is not in the key list of the dictionary.
            So it will give 0 if the called variable is not in the function.
        """
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
