import pytest
import numpy as np
from pydif.optimize.optimize import Optimize

# global minimum at (1, 1)
def rosenbrock(x, y):
    return ((100)*((y - (x**2))**2)) + ((1-x)**2)

# global minimum at (3, 2)
def f1(x, y):
    return x**2 - 6 * x + y**2 - 4 * y + 2

# global minimum at (0, 0)
def f2(x, y):
    return  x**2 + 4 * (y**2) - 2 * (x**2) * y + 4

# global minimum at (0, 0)
def f3(x, y):
    return  x**2 + x * y + y**2

# roots at (0, 1) amd (0, -1)
def f4(x, y):
    return np.array(
        [((x**4 + y**4)**(1/4)) - 1,
         ((((3*x) - (y))**4 + (x)**4)**(1/4)) - 1])

def test_gradient_descent():

    min_pos = Optimize(f1).gradient_descent((1, 1))
    assert(min_pos[0] == pytest.approx(3, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(2, rel = 1e-2, abs = 1e-2))

    min_pos = Optimize(f2).gradient_descent((1, 1))
    assert(min_pos[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(0, rel = 1e-2, abs = 1e-2))

    min_pos = Optimize(f3).gradient_descent((1, 1))
    assert(min_pos[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(0, rel = 1e-2, abs = 1e-2))

def test_BFGS():

    min_pos = Optimize(f1).BFGS((1, -1))
    assert(min_pos[0] == pytest.approx(3, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(2, rel = 1e-2, abs = 1e-2))

    min_pos = Optimize(f2).BFGS((1, -1))
    assert(min_pos[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(0, rel = 1e-2, abs = 1e-2))

    min_pos = Optimize(f3).BFGS((1, -1))
    assert(min_pos[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(min_pos[1] == pytest.approx(0, rel = 1e-2, abs = 1e-2))

def test_newton():

    root = Optimize(f4).newton(np.array([-0.5, 1.5]), max_iters = 10000)
    assert(root[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(root[1] == pytest.approx(1, rel = 1e-2, abs = 1e-2))

    root = Optimize(f4).newton(np.array([0.5, -1.5]), max_iters = 10000)
    assert(root[0] == pytest.approx(0, rel = 1e-2, abs = 1e-2))
    assert(root[1] == pytest.approx(-1, rel = 1e-2, abs = 1e-2))
