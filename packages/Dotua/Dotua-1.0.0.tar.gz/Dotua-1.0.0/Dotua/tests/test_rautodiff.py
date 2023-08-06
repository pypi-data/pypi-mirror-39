import numpy as np
from Dotua.rautodiff import rAutoDiff
from Dotua.roperator import rOperator as op


def test_create_rscalar():
    rad = rAutoDiff()

    # Create a single rScalar
    x = rad.create_rscalar(10)
    assert x.eval() == 10

    # Ensure that roots have been initialized
    assert x in x._roots.keys()

    # Create multiple rScalars
    x, y, z = rad.create_rscalar([1, 3, 6])
    assert x.eval() == 1
    assert y.eval() == 3
    assert z.eval() == 6

    # Ensure that roots have been initialized
    assert x in x._roots.keys()
    assert y in y._roots.keys()
    assert z in z._roots.keys()


def test_create_rvector():
    rad = rAutoDiff()

    # Create a single rScalar
    x = rad.create_rvector([10, 20, 30])
    assert (x.eval() == np.array([10, 20, 30])).all()

    # Ensure that roots have been initialized
    assert x in x._roots.keys()

    # Create multiple rScalars
    x, y, z = rad.create_rvector([[1, 3, 6], [2, 4, 8], [5, 10, 15]])
    assert (x.eval() == np.array([1, 3, 6])).all()
    assert (y.eval() == np.array([2, 4, 8])).all()
    assert (z.eval() == np.array([5, 10, 15])).all()

    # Ensure that roots have been initialized
    assert x in x._roots.keys()
    assert y in y._roots.keys()
    assert z in z._roots.keys()


def test__reset_universe():
    # Test rScalars
    rad = rAutoDiff()
    x, y, z = rad.create_rscalar([1, 3, 6])
    f = x + y - z
    x._grad_val = 1

    rad._reset_universe(f)
    assert x._grad_val == 0

    # Test rVectors
    x, y, z = rad.create_rvector([[1, 3, 6], [2, 4, 8], [5, 10, 15]])
    f = x + y - z
    x._grad_val = 1

    rad._reset_universe(f)
    assert x._grad_val == 0


def test_partial():
    rad = rAutoDiff()

    a, b, c = 0, np.pi / 2, np.pi / 4
    x, y, z = rad.create_rscalar([a, b, c])
    f = x + y - z
    assert rad.partial(f, x) == 1
    assert rad.partial(f, y) == 1
    assert rad.partial(f, z) == -1

    g = x * y
    assert rad.partial(g, x) == b
    assert rad.partial(g, y) == a

    h = op.sin(x * y * z) - op.cos(y)
    assert rad.partial(h, x) == b * c * np.cos(a * b * c)
    assert rad.partial(h, y) == a * c * np.cos(a * b * c) + np.sin(b)
    assert rad.partial(h, z) == a * b * np.cos(a * b * c)

    x, y = rad.create_rvector([[1, 2, 3], [1, 3, 6]])
    h = x + 1
    assert (rad.partial(h, x) == np.array([1, 1, 1])).all()

    f = op.sin(x)
    assert (rad.partial(f, x) == np.cos(np.array([1, 2, 3]))).all()


def test_multiple_partials():
    rad = rAutoDiff()

    a, b, c = 4, 9, 13
    x, y, z = rad.create_rscalar([a, b, c])
    f = x + y - z
    assert rad.partial(f, x) == 1
    assert rad.partial(f, y) == 1
    assert rad.partial(f, z) == -1

    g = x * y + z
    assert rad.partial(g, x) == b
    assert rad.partial(g, y) == a
    assert rad.partial(g, z) == 1

    x, y, z = rad.create_rvector([[1, 3, 6], [2, 4, 8], [5, 10, 15]])
    f = x + y - z
    assert (rad.partial(f, x) == np.array([1, 1, 1])).all()
    assert (rad.partial(f, y) == np.array([1, 1, 1])).all()
    assert (rad.partial(f, z) == np.array([-1, -1, -1])).all()

    g = x * y + z
    assert (rad.partial(g, x) == np.array([2, 4, 8])).all()
    assert (rad.partial(g, y) == np.array([1, 3, 6])).all()
    assert (rad.partial(g, z) == np.array([1, 1, 1])).all()
