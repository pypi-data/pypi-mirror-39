import pytest
import numpy as np
from pydif.dual.dual import Dual

def test_add():
    x = Dual(2, [1, 0], [1, 0])
    y = Dual(3, [0, 1], [0, 1])
    z = x + y

    assert(z.val == 5)
    assert(all(z.der == [1, 1]))
    assert(all(z.der2 == [1, 1]))

def test_radd():
    x = 2
    y = Dual(3, [0, 1], [0, 1])
    z = x + y

    assert(z.val == 5)
    assert(all(z.der == [0, 1]))
    assert(all(z.der2 == [0, 1]))

def test_sub():
    x = Dual(2, [1, 0], [1, 0])
    y = Dual(3, [0, 1], [0, 1])
    a = 2
    z = x - y
    z1 = x - 2

    assert(z1.val == 0)
    assert(z.val == -1)
    assert(all(z.der == [1, -1]))
    assert(all(z.der2 == [1, -1]))

def test_rsub():
    x = 2
    y = Dual(3, [0, 1], [0, 1])
    z = x - y

    assert(z == -1)
    assert(all(z.der == [0, 1]))
    assert(all(z.der2 == [0, 1]))

def test_mul():
    x = Dual(2, [1, 0], [1, 0])
    y = Dual(3, [0, 1], [0, 1])
    z = x * y

    assert(z.val == 6)
    assert(all(z.der == [3, 2]))
    assert(all(z.der2 == [3, 0]))

def test_rmul():
    x = 2
    y = Dual(3, [0, 1], [0, 1])
    z = x * y

    assert(z.val == 6)
    assert(all(z.der == [0, 2]))
    assert(all(z.der2 == [0, 2]))

def test_truediv():
    x = Dual(6, [1, 0], [1, 0])
    y = Dual(2, [0, 1], [0, 1])
    z = x / y

    assert(z.val == 3)
    assert(all(z.der == [0.5, -1.5]))
    assert(all(z.der2 == [0.5, 0]))

def test_rtruediv():
    x = 6
    y = Dual(3, [0, 1], [0, 1])
    z = x / y

    assert(z.val == 2)
    assert(z.der[0] == 0)
    assert(z.der[1] == pytest.approx(-0.66666667))
    assert(z.der2[0] == 0)
    assert(z.der2[1] == pytest.approx(-0.2222222))

def test_pow():
    x = Dual(2, [1, 0], [1, 0])
    y = Dual(3, [0, 1], [0, 1])

    z1 = x**y

    assert(z1.val == 8)
    assert(z1.der[0] == 12)
    assert(z1.der[1] == pytest.approx(5.54517744))
    assert(z1.der2[0] == 24)
    assert(z1.der2[1] == pytest.approx(9.38880156))

    z2 = x**x

    assert(z2.val == 4)
    assert(z2.der[0] == pytest.approx(6.77258872))
    assert(z2.der[1] == 0)
    assert(z2.der2[0] == pytest.approx(20.23957822))
    assert(z2.der2[1] == 0)

def test_rpow():
    x = 2
    y = Dual(3, [0, 1], [0, 1])
    z = x**y

    assert(z.val == 8)
    assert(z.der[0] == 0)
    assert(z.der[1] == pytest.approx(5.54517744))
    assert(z.der2[0] == 0)
    assert(z.der2[1] == pytest.approx(9.38880156))

def test_neg():
    x = Dual(10, [1, 0], [1, 0])
    z = -x

    assert(z.val == -10)
    assert(all(z.der == [-1, 0]))
    assert(all(z.der2 == [-1, 0]))

def test_repr():
    x = Dual(10, [1, 0], [1, 0])

    assert(repr(x) == '[10, [1 0], [1 0]]')

def test_eq():
    x = Dual(10, [1, 0], [1,0])
    y = Dual(10, [1, 0], [1,0])
    result = (x == y)

    assert(result == True)

def test_neq():
    x = Dual(10, [1, 0], [1,0])
    y = Dual(10, [0, 1], [1,0])
    result = (x != y)

    assert(result == True)
