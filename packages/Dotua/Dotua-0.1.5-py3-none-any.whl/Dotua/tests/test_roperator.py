# This file serves to test the operator.py module
from Dotua.roperator import rOperator as op
from Dotua.nodes.rscalar import rScalar
import numpy as np
import math

# initializations
def generate(v=.75):
    return rScalar(v)

c1, c2 = .5, 1
def test_sin():
    x = generate()
    f = op.sin(x)
    f.grad_val = 1
    assert x.gradient() == np.cos(x.val)
    assert op.sin(c1) == np.sin(c1)



def test_cos():
    x = generate()
    f = op.cos(x)
    f.grad_val = 1
    assert x.gradient() == -np.sin(x.val)
    assert op.cos(c1) == np.cos(c1)


def test_tan():
    x = generate()
    f = op.tan(x)
    f.grad_val = 1
    assert x.gradient() == np.arccos(x.val)**2
    assert op.tan(c1) == np.tan(c1)


def test_arcsin():
    x = generate()
    f = op.arcsin(x)
    f.grad_val = 1
    assert x.gradient() == -np.arcsin(x.val)*np.arctan(x.val)
    assert op.arcsin(c1) == np.arcsin(c1)


def test_arccos():
    x = generate(1)
    f = op.arccos(x)
    f.grad_val = 1
    assert x.gradient() == np.arccos(x.val)*np.tan(x.val)
    assert op.arccos(c2) == np.arccos(c2)


def test_arctan():
    x = generate()
    f = op.arctan(x)
    f.grad_val = 1
    assert x.gradient() == -np.arcsin(x.val)**2
    assert op.arctan(c1) == np.arctan(c1)


def test_sinh():
    x = generate()
    f = op.sinh(x)
    f.grad_val = 1
    assert x.gradient() == np.cosh(x.val)
    assert op.sinh(c1) == np.sinh(c1)


def test_cosh():
    x = generate()
    f = op.cosh(x)
    f.grad_val = 1
    assert x.gradient() == np.sinh(x.val)
    assert op.cosh(c1) == np.cosh(c1)


def test_tanh():
    x = generate()
    f = op.tanh(x)
    f.grad_val = 1
    assert x.gradient() == 1-np.tanh(x.val)**2
    assert op.tanh(c1) == np.tanh(c1)


def test_arcsinh():
    x = generate()
    f = op.arcsinh(x)
    f.grad_val = 1
    assert x.gradient() == -np.arcsinh(x.val)*np.arctanh(x.val)
    assert op.arcsinh(c1) == np.arcsinh(c1)


def test_arccosh():
    x = generate(1)
    f = op.arccosh(x)
    f.grad_val = 1
    assert x.gradient() == -np.arccosh(x.val)*np.tanh(x.val)
    assert op.arccosh(c2) == np.arccosh(c2)


def test_arctanh():
    x = generate()
    f = op.arctanh(x)
    f.grad_val = 1
    assert x.gradient() == 1-np.arctanh(x.val)**2
    assert op.arctanh(c1) == np.arctanh(c1)


def test_exp():
    x = generate()
    f = op.exp(x)
    f.grad_val = 1
    assert x.gradient() == np.exp(x.val)
    assert op.exp(c1) == np.exp(c1)


def test_log():
    base = 10
    x = generate()
    f = op.log(x, base)
    f.grad_val = 1
    assert x.gradient() == (x.val * math.log(base))**(-1)
    assert op.log(c1, base) == math.log(c1, base)
