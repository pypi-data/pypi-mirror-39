from Dotua.nodes.scalar import Scalar
import numpy as np

'''
Initialize local variables for testing. Since these tests need to be
independent of AutoDiff, we will simulate the initalization process by calling
init_jacobian once the entire 'universe' of variables has been defined
'''
# Define scalar objects
vars = x, y = Scalar(1), Scalar(2)
a, b = x.eval(), y.eval()
for var in vars:
    var.init_jacobian(vars)

# Define functions of the scalar objects
f_1 = x + y
f_2 = y + x
f_3 = x - y
f_4 = y - x
f_5 = x * y
f_6 = y * x
f_7 = x / y
f_8 = y / x

# Slightly more complicated functions
g_1 = 10 * x + y / 2 + 1000
g_2 = -2 * x * x - 1 / y

# Exponential functions
h_1 = x ** 2
h_2 = 2 ** x
h_3 = x ** y


def test_jacobian():
    # Test jacobians of scalar primitives
    assert x.partial(x) == 1
    assert x.partial(y) == 0
    assert y.partial(y) == 1
    assert y.partial(x) == 0

    # Test jacobians of functions with addition
    assert f_1.partial(x) == 1
    assert f_1.partial(y) == 1
    assert f_2.partial(x) == 1
    assert f_2.partial(y) == 1

    # Test jacobians of functions with subtraction
    assert f_3.partial(x) == 1
    assert f_3.partial(y) == -1
    assert f_4.partial(x) == -1
    assert f_4.partial(y) == 1

    # Test jacobians of functions with multiplication
    assert f_5.partial(x) == 2
    assert f_5.partial(y) == 1
    assert f_6.partial(x) == 2
    assert f_6.partial(y) == 1

    # Test jacobians of functions with division
    assert f_7.partial(x) == 1/2
    assert f_7.partial(y) == -1/4
    assert f_8.partial(x) == -2
    assert f_8.partial(y) == 1

    # Test jacobians of more complicated functions
    assert g_1.partial(x) == 10
    assert g_1.partial(y) == 1/2
    assert g_2.partial(x) == -4
    assert g_2.partial(y) == 1/4

    # Test jacobians for exponentials and deg > 1 polynomials
    assert h_1.partial(x) == 2*a
    assert h_1.partial(y) == 0
    assert h_2.partial(x) == (2 ** a) * np.log(2)
    assert h_2.partial(y) == 0

def test_add():
    assert f_1.eval() == a + b
    assert f_2.eval() == a + b

    # Directly check commutativity
    assert f_1.eval() == f_2.eval()

    # Check addition with a constant
    radd = 5 + x
    assert radd.eval() == 5 + a


def test_subtract():
    assert f_3.eval() == a - b
    assert f_4.eval() == b - a

    # Check subtraction from a constant
    radd = 5 - x
    assert radd.eval() == 5 - a


def test_multiply():
    assert f_5.eval() == a * b
    assert f_6.eval() == a * b

    # Directly check commutativity
    assert f_5.eval() == f_6.eval()


def test_divide():
    assert f_7.eval() == a / b
    assert f_8.eval() == b / a


def test_power():
    assert h_1.eval() == a ** 2
    assert h_2.eval() == 2 ** a
    assert h_3.eval() == a ** b


def test_other():
    assert g_1.eval() == 10 * a + b / 2 + 1000
    assert g_2.eval() == -2 * (a ** 2) - 1 / b
