from Dotua.rscalar import rScalar

class rAutoDiff():
    def __init__(self):
        self.func = None
        self.universe = []

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
            self.universe += rscalars
            return rscalars
        except TypeError:
            rscalar = rScalar(vals)
            self.universe += [rscalar]
            return rscalar

    def reset_universe(self, var):
        '''
        Reset gradients of nodes in computational graph before next computation

        INPUTS
        =====
        var: user defined input variable (rScalar)
        '''
        var.grad_val = None
        for parent, _ in var.parents:
            self.reset_universe(parent)


    def partial(self, func, var):
        '''
        Returns the gradient of the function with regarding to this variable

        INPUTS
        =====
        func: a function of rscalar variable
        var: a rscalar variable

        RETURNS
        =======
        A constant, which is the gradient of func with regarding to var
        '''
        if (self.func != func):
            for item in self.universe:
                self.reset_universe(item)
            func.grad_val = 1
            self.func = func
        return var.gradient()
