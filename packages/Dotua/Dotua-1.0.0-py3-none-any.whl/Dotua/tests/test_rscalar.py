from Dotua.nodes.rscalar import rScalar
import numpy as np


'''
Initialize local variables for testing. Since these tests need to be
independent of rAutoDiff, we will simulate calling partial from rAutoDiff by
manually setting the @grad_val of the function we want to compute a partial
for and then redefining the input variables before calling partial for a
different function
'''


# Define rScalar objects
def generate():
    vars = rScalar(10), rScalar(20), rScalar(30)
    for var in vars:
        var._init_roots()
    return tuple(vars)


# Define constants
c_1, c2, c5 = -1, 2, 5


def test_eval():
    x, y, z = generate()
    assert x.eval() == x._val
    assert y.eval() == y._val
    assert z.eval() == z._val


def test_add():
    x, y, z = generate()
    f = x + y + z
    assert f.eval() == x._val + y._val + z._val

    f._grad_val = 1
    f.gradient(x)
    assert x._grad_val == 1
    f.gradient(y)
    assert y._grad_val == 1
    f.gradient(z)
    assert z._grad_val == 1

    x, y, z = generate()
    g = z + x + y
    assert g.eval() == x._val + y._val + z._val

    g._grad_val = 1
    g.gradient(x)
    assert x._grad_val == 1
    g.gradient(y)
    assert y._grad_val == 1
    g.gradient(z)
    assert z._grad_val == 1

    x, y, z = generate()
    h = c_1 + x + y + z + c2
    assert h.eval() == c_1 + x._val + y._val + z._val + c2

    h._grad_val = 1
    h.gradient(x)
    assert x._grad_val == 1
    h.gradient(y)
    assert y._grad_val == 1
    h.gradient(z)
    assert z._grad_val == 1


def test_subtract():
    x, y, z = generate()
    f = x - y - z
    assert f.eval() == x._val - y._val - z._val

    f._grad_val = 1
    f.gradient(x)
    assert x._grad_val == 1
    f.gradient(y)
    assert y._grad_val == -1
    f.gradient(z)
    assert z._grad_val == -1

    x, y, z = generate()
    g = z - x - y
    assert g.eval() == z._val - x._val - y._val

    g._grad_val = 1
    g.gradient(x)
    assert x._grad_val == -1
    g.gradient(y)
    assert y._grad_val == -1
    g.gradient(z)
    assert z._grad_val == 1

    x, y, z = generate()
    h = c_1 - x - y - z - c2
    assert h.eval() == c_1 - x._val - y._val - z._val - c2

    h._grad_val = 1
    h.gradient(x)
    assert x._grad_val == -1
    h.gradient(y)
    assert y._grad_val == -1
    h.gradient(z)
    assert z._grad_val == -1


def test_multiply():
    x, y, z = generate()
    f = x * y * z
    assert f.eval() == x._val * y._val * z._val

    f._grad_val = 1
    f.gradient(x)
    assert x._grad_val == y._val * z._val
    f.gradient(y)
    assert y._grad_val == x._val * z._val
    f.gradient(z)
    assert z._grad_val == x._val * y._val

    x, y, z = generate()
    g = z * x * y
    assert g.eval() == x._val * y._val * z._val

    g._grad_val = 1
    g.gradient(x)
    assert x._grad_val == y._val * z._val
    g.gradient(y)
    assert y._grad_val == x._val * z._val
    g.gradient(z)
    assert z._grad_val == x._val * y._val

    x, y, z = generate()
    h = c_1 * x * y * z * c2
    assert h.eval() == c_1 * x._val * y._val * z._val * c2

    h._grad_val = 1
    h.gradient(x)
    assert x._grad_val == c_1 * y._val * z._val * c2
    h.gradient(y)
    assert y._grad_val == c_1 * x._val * z._val * c2
    h.gradient(z)
    assert z._grad_val == c_1 * x._val * y._val * c2


def test_divide():
    x, y, z = generate()
    f = x / y / (1 / z)
    assert f.eval() == x._val / y._val / (1 / z._val)

    f._grad_val = 1
    f.gradient(x)
    assert x._grad_val == z._val / y._val
    f.gradient(y)
    assert y._grad_val == -x._val * z._val / y._val ** 2
    f.gradient(z)
    assert z._grad_val == x._val / y._val

    x, y, z = generate()
    g = z / (x * y)
    assert g.eval() == z._val / (x._val * y._val)

    g._grad_val = 1
    g.gradient(x)
    assert x._grad_val == -z._val / (x._val ** 2 * y._val)
    g.gradient(y)
    assert y._grad_val == -z._val / (x._val * y._val ** 2)
    g.gradient(z)
    assert z._grad_val == 1 / (x._val * y._val)

    x, y, z = generate()
    h = c_1 * x / (y * z * c2)
    assert h.eval() == c_1 * x._val / (y._val * z._val * c2)

    h._grad_val = 1
    h.gradient(x)
    assert x._grad_val == c_1 / (y._val * z._val * c2)
    h.gradient(y)
    assert y._grad_val == -c_1 * x._val / (y._val * y._val * z._val * c2)
    h.gradient(z)
    assert z._grad_val == -c_1 * x._val / (y._val * z._val ** 2 * c2)

    x, y, z = generate()
    w = x / c5
    assert w.eval() == x._val / c5

    w._grad_val = 1
    w.gradient(x)
    assert x._grad_val == 1 / c5

    exception_raised = False
    try:
        w.gradient(y)
    except ValueError:
        exception_raised = True
    assert exception_raised

    exception_raised = False
    try:
        w.gradient(z)
    except ValueError:
        exception_raised = True
    assert exception_raised


def test_power():
    x, y, z = generate()
    f = x ** y * z
    assert f.eval() == x._val ** y._val * z._val

    f._grad_val = 1
    f.gradient(x)
    assert x._grad_val == y._val * x._val ** (y._val - 1) * z._val
    f.gradient(y)
    assert y._grad_val == x._val ** y._val * z._val * np.log(x._val)
    f.gradient(z)
    assert z._grad_val == x._val ** y._val

    x, y, z = generate()
    g = z ** (x * y)
    assert g.eval() == z._val ** (x._val * y._val)

    g._grad_val = 1
    g.gradient(x)
    assert x._grad_val == y._val * np.log(z._val) * z._val ** (x._val * y._val)
    g.gradient(y)
    assert y._grad_val == x._val * np.log(z._val) * z._val ** (x._val * y._val)
    g.gradient(z)
    assert z._grad_val == x._val * y._val * z._val ** (x._val * y._val - 1)

    x, y, z = generate()
    x._val, y._val, z._val = 2, 3, 4
    h = c_1 * x ** (y ** z * c2)
    assert h.eval() == c_1 * x._val ** (y._val ** z._val * c2)

    h._grad_val = 1
    h.gradient(x)
    assert x._grad_val == \
        -c2 * y._val ** z._val * x._val ** (c2 * y._val ** z._val - 1)
    h.gradient(y)
    assert y._grad_val == (-c2 * z._val * np.log(x._val) * y._val **
                           (z._val - 1) * x._val ** (c2 * y._val ** z._val))
    h.gradient(z)
    assert z._grad_val == (-c2 * np.log(x._val) * y._val ** z._val *
                           np.log(y._val) * x._val ** (c2 * y._val ** z._val))

    x, y, z = generate()
    q = 2 ** x
    assert q.eval() == 2 ** x._val

    q._grad_val = 1
    q.gradient(x)
    assert x._grad_val == 2 ** x._val * np.log(2)

    exception_raised = False
    try:
        q.gradient(y)
    except ValueError:
        exception_raised = True
    assert exception_raised

    exception_raised = False
    try:
        q.gradient(z)
    except ValueError:
        exception_raised = True
    assert exception_raised

    x, y, z = generate()
    w = x ** 2
    assert w.eval() == x._val ** 2

    w._grad_val = 1
    w.gradient(x)
    assert x._grad_val == 2 * x._val

    exception_raised = False
    try:
        w.gradient(y)
    except ValueError:
        exception_raised = True
    assert exception_raised

    exception_raised = False
    try:
        w.gradient(z)
    except ValueError:
        exception_raised = True
    assert exception_raised
