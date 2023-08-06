'''
This file tests that the AutoDiff initializer functions defined in autodiff.py
are correct.
'''
from Dotua.autodiff import AutoDiff


# Test creating a single variable
def test_single_variable():
    x = AutoDiff.create_scalar(5)
    assert x.eval() == 5
    assert x.partial(x) == 1


# Test initializing multiple variables at once
def test_multiple_variables():
    x, y, z = tuple(AutoDiff.create_scalar([1, 2, 3]))
    assert x.eval() == 1
    assert x.partial(x) == 1
    assert x.partial(y) == 0
    assert x.partial(z) == 0

    assert y.eval() == 2
    assert y.partial(x) == 0
    assert y.partial(y) == 1
    assert y.partial(z) == 0

    assert z.eval() == 3
    assert z.partial(x) == 0
    assert z.partial(y) == 0
    assert z.partial(z) == 1
