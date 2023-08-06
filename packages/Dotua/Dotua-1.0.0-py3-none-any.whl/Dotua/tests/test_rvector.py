import numpy as np
from Dotua.nodes.rvector import rVector

# Define rVector objects
def generate():
    vars = rVector([10, 10, 15]), rVector([20, 20, 25]), rVector([30, 30, 1])
    for var in vars:
        var._init_roots()
    return tuple(vars)


# Define constants
c_1, c2, c5 = -1, 2, 5


def test_get_item():
    x = rVector([10, 20])
    assert x[0].eval() == 10
    assert x[1].eval() == 20


def test_eval():
    x, y, z = generate()
    assert (x.eval() == x._val).all()
    assert (y.eval() == y._val).all()
    assert (z.eval() == z._val).all()


def test_add():
    x, y, z = generate()
    f = x + y + z
    assert (f.eval() == x._val + y._val + z._val).all()

    f._grad_val = 1
    f.gradient(x)
    assert (x._grad_val == 1).all()
    f.gradient(y)
    assert (y._grad_val == 1).all()
    f.gradient(z)
    assert (z._grad_val == 1).all()

    x, y, z = generate()
    g = z + x + y
    assert (g.eval() == x._val + y._val + z._val).all()

    g._grad_val = 1
    g.gradient(x)
    assert (x._grad_val == 1).all()
    g.gradient(y)
    assert (y._grad_val == 1).all()
    g.gradient(z)
    assert (z._grad_val == 1).all()

    x, y, z = generate()
    h = c_1 + x + y + z + c2
    assert (h.eval() == c_1 + x._val + y._val + z._val + c2).all()

    h._grad_val = 1
    h.gradient(x)
    assert (x._grad_val == 1).all()
    h.gradient(y)
    assert (y._grad_val == 1).all()
    h.gradient(z)
    assert (z._grad_val == 1).all()


def test_subtract():
    x, y, z = generate()
    f = x - y - z
    assert (f.eval() == x._val - y._val - z._val).all()

    f._grad_val = 1
    f.gradient(x)
    assert (x._grad_val == 1).all()
    f.gradient(y)
    assert (y._grad_val == -1).all()
    f.gradient(z)
    assert (z._grad_val == -1).all()

    x, y, z = generate()
    g = z - x - y
    assert (g.eval() == z._val - x._val - y._val).all()

    g._grad_val = 1
    g.gradient(x)
    assert (x._grad_val == -1).all()
    g.gradient(y)
    assert (y._grad_val == -1).all()
    g.gradient(z)
    assert (z._grad_val == 1).all()

    x, y, z = generate()
    h = c_1 - x - y - z - c2
    assert (h.eval() == c_1 - x._val - y._val - z._val - c2).all()

    h._grad_val = 1
    h.gradient(x)
    assert (x._grad_val == -1).all()
    h.gradient(y)
    assert (y._grad_val == -1).all()
    h.gradient(z)
    assert (z._grad_val == -1).all()


def test_multiply():
    x, y, z = generate()
    f = x * y * z
    assert (f.eval() == x._val * y._val * z._val).all()

    f._grad_val = 1
    f.gradient(x)
    assert (x._grad_val == y._val * z._val).all()
    f.gradient(y)
    assert (y._grad_val == x._val * z._val).all()
    f.gradient(z)
    assert (z._grad_val == x._val * y._val).all()

    x, y, z = generate()
    g = z * x * y
    assert (g.eval() == x._val * y._val * z._val).all()

    g._grad_val = 1
    g.gradient(x)
    assert (x._grad_val == y._val * z._val).all()
    g.gradient(y)
    assert (y._grad_val == x._val * z._val).all()
    g.gradient(z)
    assert (z._grad_val == x._val * y._val).all()

    x, y, z = generate()
    h = c_1 * x * y * z * c2
    assert (h.eval() == c_1 * x._val * y._val * z._val * c2).all()

    h._grad_val = 1
    h.gradient(x)
    assert (x._grad_val == c_1 * y._val * z._val * c2).all()
    h.gradient(y)
    assert (y._grad_val == c_1 * x._val * z._val * c2).all()
    h.gradient(z)
    assert (z._grad_val == c_1 * x._val * y._val * c2).all()


def test_divide():
    x, y, z = generate()
    f = x / y / (1 / z)
    assert (f.eval() == x._val / y._val / (1 / z._val)).all()

    f._grad_val = 1
    f.gradient(x)
    assert (x._grad_val == z._val / y._val).all()
    f.gradient(y)
    assert (y._grad_val == -x._val * z._val / y._val ** 2).all()
    f.gradient(z)
    assert (z._grad_val == x._val / y._val).all()

    x, y, z = generate()
    g = z / (x * y)
    assert (g.eval() == z._val / (x._val * y._val)).all()

    g._grad_val = 1
    g.gradient(x)
    assert (x._grad_val == -z._val / (x._val ** 2 * y._val)).all()
    g.gradient(y)
    assert (y._grad_val == -z._val / (x._val * y._val ** 2)).all()
    g.gradient(z)
    assert (z._grad_val == 1 / (x._val * y._val)).all()

    x, y, z = generate()
    h = c_1 * x / (y * z * c2)
    assert (h.eval() == c_1 * x._val / (y._val * z._val * c2)).all()

    h._grad_val = 1
    h.gradient(x)
    assert (x._grad_val == c_1 / (y._val * z._val * c2)).all()
    h.gradient(y)
    assert (y._grad_val ==
            -c_1 * x._val / (y._val * y._val * z._val * c2)).all()
    h.gradient(z)
    assert (z._grad_val == -c_1 * x._val / (y._val * z._val ** 2 * c2)).all()

    x, y, z = generate()
    w = x / c5
    assert (w.eval() == x._val / c5).all()

    w._grad_val = 1
    w.gradient(x)
    assert (x._grad_val == 1 / c5).all()

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
    x._val, y._val, z._val = \
        np.array([2, 2, 2]), np.array([3, 3, 3]), np.array([4, 4, 4])
    f = x ** y * z
    assert (f.eval() == x._val ** y._val * z._val).all()

    f._grad_val = 1
    f.gradient(x)
    assert (x._grad_val == y._val * x._val ** (y._val - 1) * z._val).all()
    f.gradient(y)
    assert (y._grad_val == x._val ** y._val * z._val * np.log(x._val)).all()
    f.gradient(z)
    assert (z._grad_val == x._val ** y._val).all()

    x, y, z = generate()
    g = z ** (x * y)
    assert (g.eval() == z._val ** (x._val * y._val)).all()

    g._grad_val = 1
    g.gradient(x)
    assert (x._grad_val == y._val * np.log(z._val) *
            z._val ** (x._val * y._val)).all()
    g.gradient(y)
    assert (y._grad_val == x._val * np.log(z._val) *
            z._val ** (x._val * y._val)).all()
    g.gradient(z)
    assert (z._grad_val == x._val * y._val *
            z._val ** (x._val * y._val - 1)).all()

    x, y, z = generate()
    x._val, y._val, z._val = \
        np.array([2, 2, 2]), np.array([3, 3, 3]), np.array([4, 4, 4])
    h = c_1 * x ** (y ** z * c2)
    assert (h.eval() == c_1 * x._val ** (y._val ** z._val * c2)).all()

    h._grad_val = 1
    h.gradient(x)
    assert (x._grad_val ==
            -c2 * y._val ** z._val * x._val **
            (c2 * y._val ** z._val - 1)).all()
    h.gradient(y)
    assert (y._grad_val == (-c2 * z._val * np.log(x._val) * y._val **
                            (z._val - 1) * x._val ** (c2 *
                            y._val ** z._val))).all()
    h.gradient(z)
    assert (z._grad_val == (-c2 * np.log(x._val) * y._val ** z._val *
                            np.log(y._val) * x._val ** (c2 *
                            y._val ** z._val))).all()

    x, y, z = generate()
    q = 2 ** x
    assert (q.eval() == 2 ** x._val).all()

    q._grad_val = 1
    q.gradient(x)
    assert (x._grad_val == 2 ** x._val * np.log(2)).all()

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
    assert (w.eval() == x._val ** 2).all()

    w._grad_val = 1
    w.gradient(x)
    assert (x._grad_val == 2 * x._val).all()

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
