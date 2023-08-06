from Dotua.nodes.scalar import Scalar
from Dotua.nodes.vector import Vector


class AutoDiff():
    """
    Provide user interface for creating Scalar and Vector objects.

    The AutoDiff class allows users to define Scalar and Vector objects
    through staticmethods and thus does not need to be instantiated.  In both
    methods, AutoDiff requires that the user create all variables that will be
    used within the same scope with a single call to either create_scalar or
    create_vector.  This requirement allows AutoDiff to create an implicit
    variable 'universe' which facilitates the tracking of function
    derivatives in Scalar and Vector objects.
    """

    @staticmethod
    def create_scalar(vals):
        """
        Return Scalar object(s) with user defined value(s).

        INPUTS
        =======
        vals: a list of numeric types or a single numeric type value

        RETURNS
        =======
        scalar: if vals is a single numeric type, scalar, a Scalar instance
                with user defined value, is returned as a single object
        scalars: if vals is a list of numeric types, scalars, a list of Scalar
                 objects with values corresponding to vals, is returned as a
                 list

        NOTES
        ======
        This method initializes all Scalar objects desired by the user with
        user defined value.  Before returning these Scalar objects, this method
        solidifies the variable 'universe' by seeding the jacobians of each
        of the Scalar objects with appropriate values with respect to all
        Scalars requested by the user.
        """
        try:
            scalars = [None] * len(vals)
            for i in range(len(vals)):
                scalars[i] = Scalar(vals[i])

            # Initialize the jacobians
            for var in scalars:
                var.init_jacobian(scalars)
            return scalars
        except TypeError:
            scalar = Scalar(vals)
            scalar.init_jacobian([scalar])
            return scalar

    @staticmethod
    def create_vector(vals):
        '''
        Return a list of vector variables with values as defined in vals

        INPUTS
        ======
        vals: list of lists of floats, compulsory
            Value of the list of Vector variables

        RETURNS
        ========
        A list of Vector variables

        '''
        vectors = [None] * len(vals)
        for i in range(len(vals)):
            vectors[i] = Vector(vals[i])
        return vectors
