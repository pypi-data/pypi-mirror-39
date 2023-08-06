def NewtonsMethod(func, x0, tol=1e-15, maxiters=1000):
    '''
    Computes the roots of func through iterative guesses until change is below tolerance.

    Takes in a function (func), a point at which to estimate (x0),
        an error tolerance (tol), and a maximum number of iterations (maxiters).

    func must be composed of 'AutoDiff.Operator' operations and AutoDiff.Scalar structures.

    Example usage:
    '''

    xn = x0
    steps = []

    for i in range(maxiters):

        # Calculate y at this step.
        y = func(xn)._val

        # Calculate derivative at this step
        dy_dx = list(func(xn)._jacobian.values())[0]

        # If y reaches tolerance, stop
        if abs(y) < tol:
            return xn._val, steps
            break

        else:
            steps.append((xn._val, y))
            # Compute Newton Step
            x_next = y / dy_dx

            # Update X
            xn = xn - x_next


    return xn._val, steps
