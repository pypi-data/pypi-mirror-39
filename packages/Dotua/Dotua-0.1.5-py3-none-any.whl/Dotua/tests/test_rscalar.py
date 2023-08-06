from Dotua.nodes.rscalar import rScalar
import numpy as np

'''
Initialize local variables for testing. Since these tests need to be
independent of rAutoDiff, we will simulate calling partial from rAutoDiff by
manually setting the @grad_val of the function we want to compute a partial
for and then redefining the input variables before calling partial for a
different function
'''


# Define rscalar objects and constants
def generate():
    return rScalar(10), rScalar(20), rScalar(30)


c_1, c2, c5 = -1, 2, 5


def test_eval():
    x, y, z = generate()
    assert x.eval() == x.val
    assert y.eval() == y.val
    assert z.eval() == z.val


def test_add():
    x, y, z = generate()
    f = x + y + z

    f.grad_val = 1
    assert x.gradient() == 1
    assert y.gradient() == 1
    assert z.gradient() == 1

    x, y, z = generate()
    g = z + x + y
    g.grad_val = 1
    assert x.gradient() == 1
    assert y.gradient() == 1
    assert z.gradient() == 1

    x, y, z = generate()
    h = c_1 + x + y + z + c2
    h.grad_val = 1
    assert x.gradient() == 1
    assert y.gradient() == 1
    assert z.gradient() == 1


def test_subtract():
    x, y, z = generate()
    f = x - y - z

    f.grad_val = 1
    assert x.gradient() == 1
    assert y.gradient() == -1
    assert z.gradient() == -1

    x, y, z = generate()
    g = z - x - y
    g.grad_val = 1
    assert x.gradient() == -1
    assert y.gradient() == -1
    assert z.gradient() == 1

    x, y, z = generate()
    h = c_1 - x - y - z - c2
    h.grad_val = 1
    assert x.gradient() == -1
    assert y.gradient() == -1
    assert z.gradient() == -1


def test_multiply():
    x, y, z = generate()
    f = x * y * z

    f.grad_val = 1
    assert x.gradient() == y.val * z.val
    assert y.gradient() == x.val * z.val
    assert z.gradient() == x.val * y.val

    x, y, z = generate()
    g = z * x * y
    g.grad_val = 1
    assert x.gradient() == y.val * z.val
    assert y.gradient() == x.val * z.val
    assert z.gradient() == x.val * y.val

    x, y, z = generate()
    h = c_1 * x * y * z * c2
    h.grad_val = 1
    assert x.gradient() == c_1 * y.val * z.val * c2
    assert y.gradient() == c_1 * x.val * z.val * c2
    assert z.gradient() == c_1 * x.val * y.val * c2


def test_divide():
    x, y, z = generate()
    f = x / y / (1 / z)

    f.grad_val = 1
    assert x.gradient() == z.val / y.val
    assert y.gradient() == -x.val * z.val / y.val ** 2
    assert z.gradient() == x.val / y.val

    x, y, z = generate()
    g = z / (x * y)
    g.grad_val = 1
    assert x.gradient() == -z.val / (x.val ** 2 * y.val)
    assert y.gradient() == -z.val / (x.val * y.val ** 2)
    assert z.gradient() == 1 / (x.val * y.val)

    x, y, z = generate()
    h = c_1 * x / (y * z * c2)
    h.grad_val = 1
    assert x.gradient() == c_1 / (y.val * z.val * c2)
    assert y.gradient() == -c_1 * x.val / (y.val * y.val * z.val * c2)
    assert z.gradient() == -c_1 * x.val / (y.val * z.val ** 2 * c2)

    x, y, z = generate()
    w = x / c5
    w.grad_val = 1
    assert x.gradient() == 1 / c5
    assert y.gradient() == 0
    assert z.gradient() == 0


def test_power():
    x, y, z = generate()
    f = x ** y * z

    f.grad_val = 1
    assert x.gradient() == y.val * x.val ** (y.val - 1) * z.val
    assert y.gradient() == x.val ** y.val * z.val * np.log(x.val)
    assert z.gradient() == x.val ** y.val

    x, y, z = generate()
    g = z ** (x * y)
    g.grad_val = 1
    assert x.gradient() == y.val * np.log(z.val) * z.val ** (x.val * y.val)
    assert y.gradient() == x.val * np.log(z.val) * z.val ** (x.val * y.val)
    assert z.gradient() == x.val * y.val * z.val ** (x.val * y.val - 1)

    x, y, z = generate()
    x.val, y.val, z.val = 2, 3, 4
    h = c_1 * x ** (y ** z * c2)
    h.grad_val = 1
    assert x.gradient() == -c2 * y.val ** z.val * x.val ** (c2 * y.val ** z.val - 1)
    assert y.gradient() == (-c2 * z.val * np.log(x.val) * y.val ** (z.val - 1) *
                            x.val ** (c2 * y.val ** z.val))
    assert z.gradient() == (-c2 * np.log(x.val) * y.val ** z.val *
                            np.log(y.val) * x.val ** (c2 * y.val ** z.val))

    x, y, z = generate()
    q = 2 ** x
    q.grad_val = 1
    assert x.gradient() == 2 ** x.val * np.log(2)
    assert y.gradient() == 0
    assert z.gradient() == 0

    x, y, z = generate()
    w = x ** 2
    w.grad_val = 1
    assert x.gradient() == 2 * x.val
    assert y.gradient() == 0
    assert z.gradient() == 0
