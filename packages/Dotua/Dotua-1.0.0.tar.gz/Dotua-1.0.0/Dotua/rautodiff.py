import numpy as np
from Dotua.nodes.rscalar import rScalar
from Dotua.nodes.rvector import rVector


class rAutoDiff():
    def __init__(self):
        self._func = None

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
                rscalars[i]._init_roots()
            return rscalars
        except TypeError:
            rscalar = rScalar(vals)
            rscalar._init_roots()
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
        try:
            rvectors = [None] * len(vals)
            for i in range(len(vals)):
                rvectors[i] = rVector(vals[i])
                rvectors[i]._init_roots()
            return rvectors
        except TypeError:
            rvector = rVector(vals)
            rvector._init_roots()
            return rvector

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
            if self._func is not None:
                self._reset_universe(func)
            self._func = func
        try:
            func._grad_val = np.zeros(len(var._grad_val)) + 1
        except TypeError:
            func._grad_val = 1
        func.gradient(var)
        return var._grad_val

    def _reset_universe(self, func):
        '''
        Reset gradients of nodes in computational graph before next computation

        INPUTS
        =====
        var: user defined input variable (rScalar)
        '''
        try:
            func._grad_val = np.zeros(len(func._grad_val))
        except TypeError:
            func._grad_val = 0
        for val in func._roots.values():
            for child, _ in val:
                if child is not None:
                    self._reset_universe(child)
