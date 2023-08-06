# This file serves to test the operator.py module
from Dotua.operator import Operator as op
from Dotua.autodiff import AutoDiff as ad
import numpy as np

x, z, n = tuple(ad.create_scalar([0, 1, 2048]))
v = ad.create_vector([[.6,.25,.5,.75]])[0]
v2 = op.sin(v)
orig_vals = np.copy(v._val)
y = 0


def test_sin():
    # Scalar
    sx = op.sin(x)
    assert np.sin(x._val) == sx._val
    for k in x._jacobian.keys():
        assert sx.partial(k) == x.partial(k) * np.cos(x._val)

    # Simple Vector Values
    sv = op.sin(v)
    assert ~(np.sin(orig_vals) - sv._val).any()

    # Simple Vector Jacobian
    for key in sv._dict.keys():
        assert ~(sv._dict[key] - v.getDerivative(key) * np.cos(v._val) * np.eye(len(v._val))).any()

    # Complex Vector Values
    scv = op.sin(sv)

    assert ~(np.sin(np.sin(orig_vals)) - scv._val).any()

    # Complex Vector Jacobian
    for key in scv._dict.keys():
        assert ~(scv._dict[key] - sv.getDerivative(key) * np.cos(sv._val) * np.eye(len(sv._val))).any()

    # Constant
    assert op.sin(y) == np.sin(y)


def test_cos():
    # Scalar
    cx = op.cos(x)
    assert np.cos(x._val) == cx._val
    for k in x._jacobian.keys():
        assert(cx.partial(k) == -x.partial(k) * np.sin(x._val))

    # Simple Vector Values
    cv = op.cos(v)
    assert ~(np.cos(orig_vals) - cv._val).any()

    # Simple Vector Jacobian
    for key in cv._dict.keys():
        assert ~(cv._dict[key] - v.getDerivative(key) * -np.sin(v._val) * np.eye(len(v._val))).any()

    # Complex Vector Values
    ccv = op.cos(cv)

    assert ~(np.cos(np.cos(orig_vals)) - ccv._val).any()

    # Complex Vector Jacobian
    for key in ccv._dict.keys():
        assert ~(ccv._dict[key] - cv.getDerivative(key) * -np.sin(cv._val) * np.eye(len(cv._val))).any()

    # Constant
    assert op.cos(y) == np.cos(y)


def test_tan():
    # Scalar
    tx = op.tan(x)
    assert np.tan(x._val) == tx._val
    for k in x._jacobian.keys():
        assert tx.partial(k) == x.partial(k) * np.arccos(x._val)**2

    # Simple Vector Values
    tv = op.tan(v)
    assert ~(np.tan(orig_vals) - tv._val).any()

    # Simple Vector Jacobian
    for key in tv._dict.keys():
        assert ~(tv._dict[key] - v.getDerivative(key) * np.arccos(v._val)**2 * np.eye(len(v._val))).any()

    # Complex Vector Values
    tcv = op.tan(tv)

    assert ~(np.tan(np.tan(orig_vals)) - tcv._val).any()

    # Complex Vector Jacobian
    for key in tcv._dict.keys():
        assert ~(tcv._dict[key] - tv.getDerivative(key) * np.arccos(tv._val)**2 * np.eye(len(tv._val))).any()

    # Constant
    assert op.tan(y) == np.tan(y)


def test_arcsin():
    # Scalar
    asx = op.arcsin(x)
    assert np.arcsin(x._val) == asx._val
    for k in x._jacobian.keys():
        assert asx.partial(k) == -x.partial(k) * np.arcsin(x._val) \
               * np.arctan(x._val)

    # Simple Vector Values
    asv = op.arcsin(v)
    assert ~(np.arcsin(orig_vals) - asv._val).any()

    # Simple Vector Jacobian
    for key in asv._dict.keys():
        assert ~(asv._dict[key] - v.getDerivative(key) *-np.arcsin(v._val)*np.arctan(v._val) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    ascv = op.arcsin(asv)

    assert ~(np.arcsin(np.arcsin(orig_vals)) - ascv._val).any()

    # Complex Vector Jacobian
    for key in ascv._dict.keys():
        assert ~(ascv._dict[key] - asv.getDerivative(key) *-np.arcsin(asv._val)*np.arctan(asv._val) *
                 np.eye(len(asv._val))).any()

    # Constant
    assert op.arcsin(y) == np.arcsin(y)


def test_arccos():
    # Scalar
    acx = op.arccos(x)
    assert np.arccos(x._val) == acx._val
    for k in x._jacobian.keys():
        assert acx.partial(k) == x.partial(k) * np.arccos(x._val) \
               * np.tan(x._val)

    # Simple Vector Values
    acv = op.arccos(v)
    assert ~(np.arccos(orig_vals) - acv._val).any()

    # Simple Vector Jacobian
    for key in acv._dict.keys():
        assert ~(acv._dict[key] - v.getDerivative(key) * np.arccos(v._val)*np.tan(v._val)*
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    accv = op.arccos(v2)

    assert ~(np.arccos(np.sin(orig_vals)) - accv._val).any()

    # Complex Vector Jacobian
    for key in accv._dict.keys():
        assert ~(accv._dict[key] - v2.getDerivative(key) * np.arccos(v2._val)*np.tan(v2._val) *
                 np.eye(len(v2._val))).any()

    # Constant
    assert op.arccos(y) == np.arccos(y)


def test_arctan():
    # Scalar
    atx = op.arctan(x)
    assert np.arctan(x._val) == atx._val
    for k in x._jacobian.keys():
        assert atx.partial(k) == -x.partial(k) * np.arcsin(x._val)**2

    # Simple Vector Values
    atv = op.arctan(v)
    assert ~(np.arctan(orig_vals) - atv._val).any()

    # Simple Vector Jacobian
    for key in atv._dict.keys():
        assert ~(atv._dict[key] - v.getDerivative(key) * -np.arcsin(v._val)**2 *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    atcv = op.arctan(v2)

    assert ~(np.arctan(np.sin(orig_vals)) - atcv._val).any()

    # Complex Vector Jacobian
    for key in atcv._dict.keys():
        assert ~(atcv._dict[key] - v2.getDerivative(key) * -np.arcsin(v2._val)**2 * np.eye(len(v2._val))).any()

    # Constant
    assert op.arctan(y) == np.arctan(y)


def test_sinh():
    # Scalar
    shx = op.sinh(x)
    assert np.sinh(x._val) == shx._val
    for k in x._jacobian.keys():
        assert shx.partial(k) == x.partial(k) * np.cosh(x._val)

    # Simple Vector Values
    shv = op.sinh(v)
    assert ~(np.sinh(orig_vals) - shv._val).any()

    # Simple Vector Jacobian
    for key in shv._dict.keys():
        assert ~(shv._dict[key] - v.getDerivative(key) * np.cosh(v._val) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    shcv = op.sinh(v2)

    assert ~(np.sinh(np.sin(orig_vals)) - shcv._val).any()

    # Complex Vector Jacobian
    for key in shcv._dict.keys():
        assert ~(shcv._dict[key] - v2.getDerivative(key) * np.cosh(v2._val) * np.eye(len(v2._val))).any()

    # Constant
    assert op.sinh(y) == np.sinh(y)


def test_cosh():
    # Scalar
    chx = op.cosh(x)
    assert np.cosh(x._val) == chx._val
    for k in x._jacobian.keys():
        assert chx.partial(k) == x.partial(k) * np.sinh(x._val)

    # Simple Vector Values
    chv = op.cosh(v)
    assert ~(np.cosh(orig_vals) - chv._val).any()

    # Simple Vector Jacobian
    for key in chv._dict.keys():
        assert ~(chv._dict[key] - v.getDerivative(key) * np.sinh(v._val) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    chcv = op.cosh(v2)

    assert ~(np.cosh(np.sin(orig_vals)) - chcv._val).any()

    # Complex Vector Jacobian
    for key in chcv._dict.keys():
        assert ~(chcv._dict[key] - v2.getDerivative(key) * np.sinh(v2._val) * np.eye(len(v2._val))).any()

    # Constant
    assert op.cosh(y) == np.cosh(y)


def test_tanh():
    # Scalar
    thx = op.tanh(x)
    assert np.tanh(x._val) == thx._val
    for k in x._jacobian.keys():
        assert thx.partial(k) == x.partial(k) * (1 - np.tanh(x._val)**2)

    # Simple Vector Values
    thv = op.tanh(v)
    assert ~(np.tanh(orig_vals) - thv._val).any()

    # Simple Vector Jacobian
    for key in thv._dict.keys():
        assert ~(thv._dict[key] - v.getDerivative(key) * (1-np.tanh(v._val)**2) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    thcv = op.tanh(v2)

    assert ~(np.tanh(np.sin(orig_vals)) - thcv._val).any()

    # Complex Vector Jacobian
    for key in thcv._dict.keys():
        assert ~(thcv._dict[key] - v2.getDerivative(key) * (1-np.tanh(v2._val)**2) * np.eye(len(v2._val))).any()

    # Constant
    assert op.tanh(y) == np.tanh(y)


def test_arcsinh():
    # Scalar
    ashx = op.arcsinh(x)
    assert np.arcsinh(x._val) == ashx._val
    for k in x._jacobian.keys():
        assert ashx.partial(k) == -x.partial(k) * np.arcsinh(x._val) \
               * np.arctanh(x._val)

    # Simple Vector Values
    ashv = op.arcsinh(v)
    assert ~(np.arcsinh(orig_vals) - ashv._val).any()

    # Simple Vector Jacobian
    for key in ashv._dict.keys():
        assert ~(ashv._dict[key] - v.getDerivative(key) * -np.arcsinh(v._val)*np.arctanh(v._val) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    ashcv = op.arcsinh(v2)

    assert ~(np.arcsinh(np.sin(orig_vals)) - ashcv._val).any()

    # Complex Vector Jacobian
    for key in ashcv._dict.keys():
        assert ~(ashcv._dict[key] - v2.getDerivative(key) * -np.arcsinh(v2._val)*np.arctanh(v2._val)
                 * np.eye(len(v2._val))).any()

    # Constant
    assert op.arcsinh(y) == np.arcsinh(y)


def test_arccosh():
    x = ad.create_scalar(1)
    y = 2
    # Scalar
    achx = op.arccosh(x)
    assert np.arccosh(x._val) == achx._val
    for k in x._jacobian.keys():
        assert achx.partial(k) == -x.partial(k) * np.arccosh(x._val) \
               * np.tanh(x._val)

    # Simple Vector Values
    v_temp = ad.create_vector([[2, 3, 4, 5]])[0]
    orig_temp = np.copy(v_temp._val)
    achv = op.arccosh(v_temp)
    assert ~(np.arccosh(orig_temp) - achv._val).any()

    # Simple Vector Jacobian
    for key in achv._dict.keys():
        assert ~(achv._dict[key] - v_temp.getDerivative(key) * -np.arccosh(v_temp._val)*np.tanh(v_temp._val) *
                 np.eye(len(v_temp._val))).any()

    # Complex Vector Values
    achcv = op.arccosh(achv)

    assert ~(np.arccosh(np.arccosh(orig_temp)) - achcv._val).any()

    # Complex Vector Jacobian
    for key in achcv._dict.keys():
        assert ~(achcv._dict[key] - achv.getDerivative(key) * -np.arccosh(achv._val)*np.tanh(achv._val)
                 * np.eye(len(achv._val))).any()

    # Constant
    assert(op.arccosh(y) == np.arccosh(y))


def test_arctanh():
    # Scalar
    athx = op.arctanh(x)
    assert np.arctanh(x._val) == athx._val
    for k in x._jacobian.keys():
        assert athx.partial(k) == x.partial(k) * (1 - np.arctanh(x._val)**2)

    # Simple Vector Values
    athv = op.arctanh(v)
    assert ~(np.arctanh(orig_vals) - athv._val).any()

    # Simple Vector Jacobian
    for key in athv._dict.keys():
        assert ~(athv._dict[key] - v.getDerivative(key) * (1-np.arctanh(v._val)**2) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    athcv = op.arctanh(v2)

    assert ~(np.arctanh(np.sin(orig_vals)) - athcv._val).any()

    # Complex Vector Jacobian
    for key in athcv._dict.keys():
        assert ~(athcv._dict[key] - v2.getDerivative(key) * (1-np.arctanh(v2._val)**2)
                 * np.eye(len(v2._val))).any()

    # Constant
    assert op.arctanh(y) == np.arctanh(y)


def test_exp():
    # Scalar
    ex = op.exp(x)
    assert np.exp(x._val) == ex._val
    for k in x._jacobian.keys():
        assert ex.partial(k) == x.partial(k) * np.exp(x._val)

    # Simple Vector Values
    ev = op.exp(v)
    assert ~(np.exp(orig_vals) - ev._val).any()

    # Simple Vector Jacobian
    for key in ev._dict.keys():
        assert ~(ev._dict[key] - v.getDerivative(key) * np.exp(v._val) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    ecv = op.exp(v2)

    assert ~(np.exp(np.sin(orig_vals)) - ecv._val).any()

    # Complex Vector Jacobian
    for key in ecv._dict.keys():
        assert ~(ecv._dict[key] - v2.getDerivative(key) * np.exp(v2._val)
                 * np.eye(len(v2._val))).any()

    # Constant
    assert op.exp(y) == np.exp(y)


def test_log():
    # Scalar
    base = 10
    lgn = op.log(n, base)
    assert np.log(n._val) / np.log(base) == lgn._val
    for k in x._jacobian.keys():
        assert lgn.partial(k) == n.partial(k) / (n._val * np.log(base))

    # Simple Vector Values
    lgv = op.log(v, base)
    assert ~(np.log(orig_vals) / np.log(base) - lgv._val).any()

    # Simple Vector Jacobian
    for key in lgv._dict.keys():
        print(lgv._dict[key])
        print(v.getDerivative(key) / (v._val * np.log(base)) *
                 np.eye(len(v._val)))
        assert ~(lgv._dict[key] - v.getDerivative(key) / (v._val * np.log(base)) *
                 np.eye(len(v._val))).any()

    # Complex Vector Values
    lgcv = op.log(v2, base)

    assert ~(np.log(np.sin(orig_vals)) / np.log(base) - lgcv._val).any()

    # Complex Vector Jacobian
    for key in lgcv._dict.keys():
        assert ~(lgcv._dict[key] - v2.getDerivative(key) / (v2._val * np.log(base))
                 * np.eye(len(v2._val))).any()

    # Constant
    z = 24
    assert op.log(z, base) == np.log(z) / np.log(base)


def test_add():
    # Scalar
    res = op.sin(x) + op.sin(z)
    assert np.sin(x._val) + np.sin(z._val) == res._val
    for k in x._jacobian.keys():
        assert res.partial(k) == op.sin(x).partial(k) + op.sin(z).partial(k)

    # Constant
    assert op.sin(y) + op.sin(2 * y) == np.sin(y) + np.sin(2 * y)
