from Dotua.roperator import rOperator as op
from Dotua.rautodiff import rAutoDiff
import numpy as np


def test_create_rscalar():
    rad = rAutoDiff()
    rscalars = rad.create_rscalar([1, 3, 6])
    assert rscalars[0].val == 1
    assert rscalars[1].val == 3
    assert rscalars[2].val == 6

    x = rad.create_rscalar(10)
    assert x.val == 10


def test__reset_universe():
    rad = rAutoDiff()
    x, y, z = rad.create_rscalar([1, 3, 6])
    f = x + y - z
    rad.partial(f,z)

    rad._reset_universe(x)
    g = op.exp(x)
    assert rad.partial(g, x) == np.exp(1)


def test_multiple_partials():
    rad = rAutoDiff()

    a, b, c = 4, 9, 13
    x, y, z = rad.create_rscalar([a, b, c])
    f = x + y - z
    assert rad.partial(f, x) == 1
    assert rad.partial(f, y) == 1
    assert rad.partial(f, z) == -1

    g = x * y + z
    assert rad.partial(g, y) == a
    assert rad.partial(g, x) == b

    assert rad.partial(g, z) == 1


def test_partial():
    rad = rAutoDiff()

    x, y, z = rad.create_rscalar([1, 3, 6])
    f = x + y - z
    assert rad.partial(f, x) == 1
    assert rad.partial(f, y) == 1
    assert rad.partial(f, z) == -1

    # rad._reset_universe([x,y])
    g = x * y
    assert rad.partial(g, x) == 3
    assert rad.partial(g, y) == 1

    # rad._reset_universe([x,y,z])
    h = op.sin(x * y * z) - op.cos(y)
    assert rad.partial(h, x) == 3 * 6 * np.cos(1 * 3 * 6)
    assert rad.partial(h, y) == 1 * 6 * np.cos(1 * 3 * 6) + np.sin(3)
    assert rad.partial(h, z) == 1 * 3 * np.cos(1 * 3 * 6)
