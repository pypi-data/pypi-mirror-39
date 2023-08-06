from Dotua.nodes.rscalar import rScalar
from Dotua.nodes.rvector import rVector


class rAutoDiff():
    def __init__(self):
        self._func = None
        self._universe = []

    def create_rscalar(self, vals):
        '''
        Return rScalar object(s) with user defined value(s).

        INPUTS
        ======
        vals: list of lists of floats, compulsory
            Value of the list of Vector variables

        RETURNS
        ========
        A list of Vector variables

        NOTES
        =====

        POST:
            returns a list of vector variables with value defined in vals
        '''
        try:
            rscalars = [None] * len(vals)
            for i in range(len(vals)):
                rscalars[i] = rScalar(vals[i])
            self._universe += rscalars
            return rscalars
        except TypeError:
            rscalar = rScalar(vals)
            self._universe += [rscalar]
            return rscalar

    def create_rvector(self, vals):
        '''
        Return rScalar object(s) with user defined value(s).

        INPUTS
        ======
        vals: list of lists of floats, compulsory
            Value of the list of Vector variables

        RETURNS
        ========
        A list of Vector variables

        NOTES
        =====

        POST:
            returns a list of vector variables with value defined in vals
        '''
        rvectors = [None] * len(vals)
        for i in range(len(vals)):
            rvectors[i] = rVector(vals[i])
            self._universe += [rvectors[i]]
            for j in range(len(vals[i])):
                self._universe += [rvectors[i][j]]
        return rvectors


    def partial(self, func, var):
        '''
        Returns derivative of the function with regard to the given variable

        INPUTS
        =====
        func: a function of rScalar variables
        var: an rScalar variable

        RETURNS
        =======
        A constant, which is the gradient of func with regarding to var
        '''
        if (self._func != func):
            for item in self._universe:
                self._reset_universe(item)
            func.grad_val = 1
            self._func = func
        return var.gradient()

    def _reset_universe(self, var):
        '''
        Reset gradients of nodes in computational graph before next computation

        INPUTS
        =====
        var: user defined input variable (rScalar)
        '''
        var.grad_val = None
        for parent, _ in var.parents:
            self._reset_universe(parent)
