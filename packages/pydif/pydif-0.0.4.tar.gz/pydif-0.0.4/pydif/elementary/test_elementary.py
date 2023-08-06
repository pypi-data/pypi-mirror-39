from pydif.elementary import elementary as el
import pytest
# from ..dual.dual import Dual
from pydif.dual.dual import Dual

def test_cos():
    assert(el.cos(5) == pytest.approx(0.2836, 0.001))
    x = Dual(5, 8, 1)
    cosx = el.cos(x)
    assert(cosx.val == pytest.approx(0.2836, 0.001))
    assert(cosx.der == pytest.approx(7.671, 0.001))
    assert(cosx.der2 == pytest.approx(-17.1954, 0.001))

def test_sin():
    assert(el.sin(3) == pytest.approx(0.1411, 0.001))
    x = Dual(3, 3, 1)
    sinx = el.sin(x)
    assert(sinx.val == pytest.approx(0.1411, 0.001))
    assert(sinx.der == pytest.approx(-2.9699, 0.001))
    assert(sinx.der2 == pytest.approx(-2.260, 0.001))

def test_tan():
    assert(el.tan(2) == pytest.approx(-2.185, 0.001))
    x = Dual(2, 3, 4)
    tanx = el.tan(x)
    assert(tanx.val == pytest.approx(-2.185, 0.001))
    assert(tanx.der == pytest.approx(17.32319, 0.001))
    assert(tanx.der2 == pytest.approx(-204.0136, 0.001))

def test_exp():
    assert(el.exp(0) == pytest.approx(1))
    assert(el.exp(5)) == pytest.approx(148.413159, 0.0001)
    x = Dual(3, 4, 5)
    ex = el.exp(x)
    assert(ex.val == pytest.approx(20.0855369, 0.0001))
    assert(ex.der == pytest.approx(80.3421476, 0.0001))
    assert(ex.der2 == pytest.approx(421.7962, 0.001))

def test_arcsin():
    assert(el.arcsin(1) == pytest.approx(1.570, 0.001))
    x = Dual(0.5, 2, 2)
    arcsinx = el.arcsin(x)
    assert(arcsinx.val == pytest.approx(0.5235, 0.01))
    assert(arcsinx.der == pytest.approx(1.154*2, 0.01))
    assert(arcsinx.der2 == pytest.approx(5.3886, 0.01))

def test_arccos():
    assert(el.arccos(0.9) == pytest.approx(0.451, 0.001))
    x = Dual(0.5, 2, 4)
    arccosx = el.arccos(x)
    assert(arccosx.val == pytest.approx(1.047, 0.01))
    assert(arccosx.der == pytest.approx( -2 *1.1547, 0.01))
    assert(arccosx.der2 == pytest.approx(-7.698, 0.01))

def test_arctan():
    assert(el.arctan(0.75) == pytest.approx(0.6435, 0.001))
    x = Dual(0.5, 2, 5)
    arctanx = el.arctan(x)
    assert(arctanx.val == pytest.approx(0.4636, 0.001))
    assert(arctanx.der == pytest.approx(2 *0.8, 0.001))
    assert(arctanx.der2 == pytest.approx(1.44, 0.01))

def test_sinh():
    assert(el.sinh(0.7) == pytest.approx(0.7585, 0.001))
    x = Dual(0.5, 2, 3)
    sinhx = el.sinh(x)
    assert(sinhx.val == pytest.approx(0.5210, 0.01))
    assert(sinhx.der == pytest.approx(2 * 1.127, 0.01))
    assert(sinhx.der2 == pytest.approx(5.467, 0.01))

def test_cosh():
    assert(el.cosh(0.6) == pytest.approx(1.185, 0.001))
    x = Dual(0.5, 2, 3)
    coshx = el.cosh(x)
    assert(coshx.val == pytest.approx(1.127, 0.001))
    assert(coshx.der == pytest.approx(2 * 0.52109, 0.001))
    assert(coshx.der2 == pytest.approx(6.073789, 0.0001))

def test_tanh():
    assert(el.tanh(0.5) == pytest.approx(0.462, 0.001))
    x = Dual(0.5, 2, 3)
    tanhx = el.tanh(x)
    assert(tanhx.val == pytest.approx(0.462, 0.001))
    assert(tanhx.der == pytest.approx(2*0.7864, 0.001))
    assert(tanhx.der2 == pytest.approx(-0.5481, 0.001))

def test_arcsinh():
    assert(el.arcsinh(0.6) == pytest.approx(0.5688, 0.001))
    x = Dual(0.5, 2, 3)
    arcsinhx = el.arcsinh(x)
    assert(arcsinhx.val == pytest.approx(0.48121, 0.001))
    assert(arcsinhx.der == pytest.approx(1.7888, 0.001))
    assert(arcsinhx.der2 == pytest.approx(1.2521, 0.001))

def test_arccosh():
    assert(el.arccosh(2) == pytest.approx(1.3169, 0.001))
    x = Dual(3, 2, 1)
    arccoshx = el.arccosh(x)
    assert(arccoshx.val == pytest.approx(1.7627, 0.001))
    assert(arccoshx.der == pytest.approx(0.3535 *2, 0.001))
    assert(arccoshx.der2 == pytest.approx(-0.17677, 0.001))

def test_arctanh():
    assert(el.arctanh(0.6) == pytest.approx(0.6931, 0.001))
    x = Dual(0.5, 2, 3)
    arctanhx = el.arctanh(x)
    assert(arctanhx.val == pytest.approx(0.5493, 0.001))
    assert(arctanhx.der == pytest.approx(1.333 *2, 0.001))
    assert(arctanhx.der2 == pytest.approx(11.11111, 0.001))

def test_exp2():
    assert(el.exp2(0) == pytest.approx(1))
    assert(el.exp2(4) == pytest.approx(16))
    x = Dual(4, 4, 1)
    x2 = el.exp2(x)
    assert(x2.val == pytest.approx(16))
    assert(x2.der == pytest.approx(44.361, 0.001))

def test_log():
    assert(el.log(27) == pytest.approx(3.2958, 0.001))
    x = Dual(3, 5, 2)
    lnx = el.log(x)
    assert(lnx.val == pytest.approx(1.098, 0.001))
    assert(lnx.der == pytest.approx(1.6666, 0.001))
    assert(lnx.der2 == pytest.approx(-2.11111, 0.001))

def test_log2():
    assert(el.log2(8) == pytest.approx(3))
    x = Dual(4, 8, 3)
    log2x = el.log2(x)
    assert(log2x.val == pytest.approx(2))
    assert(log2x.der == pytest.approx(2.8853, 0.001))
    assert(log2x.der2 == pytest.approx(-4.68875, 0.001))

def test_log10():
    assert(el.log10(100) == pytest.approx(2))
    x = Dual(10, 30, 3)
    log10x = el.log10(x)
    assert(log10x.val == pytest.approx(1))
    assert(log10x.der == pytest.approx(1.30288, 0.001))
    assert(log10x.der2 == pytest.approx(-3.778, 0.001))

def test_sqrt():
    assert(el.sqrt(5) == pytest.approx(2.236, 0.001))
    x = Dual(7, 3, 4)
    sqrtx = el.sqrt(x)
    assert(sqrtx.val == pytest.approx(2.6457, 0.001))
    assert(sqrtx.der == pytest.approx(0.5669, 0.001))
    assert(sqrtx.der2 == pytest.approx(0.63444, 0.001))

def test_sigmoid():
    assert(el.sigmoid(5) == pytest.approx(0.9933, 0.001))
    x = Dual(2, 3, 1)
    sigmoidx = el.sigmoid(x)
    assert(sigmoidx.val == pytest.approx(0.8807, 0.001))
    assert(sigmoidx.der == pytest.approx(0.10499*3, 0.001 ))

def test_relu():
    assert(el.relu(5) == 5)
    assert(el.relu(-5) == 0)
    x = Dual(2, 3, 7)
    y = Dual(-2, 3, 8)
    relux = el.relu(x)
    reluy = el.relu(y)
    assert(relux.val == 2)
    assert(relux.der == 3)
    assert(relux.der2 == 0)
    assert(reluy.val == 0)
    assert(reluy.der == 0)
    assert(reluy.der2 == 0)
