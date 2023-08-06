import pytest
import numpy as np
from pydif import pydif 
from pydif.pydif import diff, diffdiff
from pydif.elementary import elementary as el


def test_init():
    def f1(x):
        return x
    def f2(x, y):
        return x+y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    assert(ad1.func == f1)
    assert(ad2.func == f2)
    assert(ad1.num_params == 1)
    assert(ad2.num_params == 2)

def test_check_dim():
    def f1(x):
        return x
    def f2(x, y):
        return x+y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    with pytest.raises(ValueError):
        ad1._check_dim([0,0])
    ad1._check_dim([0])
    ad1._check_dim(0)

    with pytest.raises(ValueError):
        ad2._check_dim([0])
    with pytest.raises(ValueError):
        ad2._check_dim(0)
    ad2._check_dim([0,0])

def test_enforce_unitvector():
    def f1(x):
        return x

    dir1 = np.array([1])
    dir2 = np.array([0.5])
    dir3 = np.array([0,1])
    dir4 = np.array([1,-1])
    dir5 = np.array([0,0])

    ad1 = pydif.autodiff(f1)

    assert(np.isclose(ad1._enforce_unitvector(dir1),np.array([1])))
    assert(np.isclose(ad1._enforce_unitvector(dir2),np.array([1])))
    assert(all(np.isclose(ad1._enforce_unitvector(dir3),np.array([0,1]))))
    assert(all(np.isclose(ad1._enforce_unitvector(dir4),np.array([np.sqrt(1/2),-np.sqrt(1/2)]))))

    with pytest.raises(ValueError):
        ad1._enforce_unitvector(dir5)


def test_eval():
    def f1(x):
        return x
    def f2(x, y):
        return x+y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    pos1 = 3
    pos2 = [3,4]

    assert(ad1._eval(pos1, wrt_variables=False).val == pos1)
    assert(ad1._eval(pos1, wrt_variables=False).der == 1)
    assert(ad1._eval(pos1, wrt_variables=False).der2 == 0)
    assert(ad1._eval(pos1, wrt_variables=True).val == pos1)
    assert(ad1._eval(pos1, wrt_variables=True).der == 1)
    assert(ad1._eval(pos1, wrt_variables=True).der2 == 0)

    assert(ad2._eval(pos2, wrt_variables=False).val == pos2[0] + pos2[1])
    assert(ad2._eval(pos2, wrt_variables=False).der == 2)
    assert(ad2._eval(pos2, wrt_variables=False).der2 == 0)
    assert(ad2._eval(pos2, wrt_variables=True).val == pos2[0] + pos2[1])
    assert(all(ad2._eval(pos2, wrt_variables=True).der == [1,1]))
    assert(all(ad2._eval(pos2, wrt_variables=True).der2 == [0,0]))

def test_get_val():
    def f1(x):
        return x
    def f2(x, y):
        return x, y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    pos1 = 3
    pos2 = [3,4]
    dir1 = [1]
    dir2 = [0,1]

    assert(ad1.get_val(pos1, direction=None) == pos1)
    assert(ad1.get_val(pos1, direction=dir1) == pos1)

    assert(ad2.get_val(pos2, direction=None) == pos2)
    assert(ad2.get_val(pos2, direction=dir2) == pos2[1])

def test_get_val_vector():
    def f1(x):
        return x
    def f2(x, y):
        return x, y

    ad1 = pydif.autodiff_vector([[f1, f2], [f2, f1]])
    ad2 = pydif.autodiff_vector([f2, f2, f2, f2])

    pos1 = 3
    pos2 = [3,4]
    dir1 = [1]
    dir2 = [0,1]
    dir3 = [1,0]

    res = ad1.get_val(pos2, direction=None)
    assert(res[0][0] == res[1][1] == pos1)
    assert(res[0][1] == res[1][0] == pos2)

    res = ad1.get_val(pos2, direction=dir3)
    assert(res[0][0] == res[1][1] == pos1)
    assert(res[0][1] == res[1][0] == pos2[0])

    res = ad2.get_val(pos2, direction=None)
    assert(res[0] == res[1] == res[2] == res[3] == pos2)

    res = ad2.get_val(pos2, direction=dir2)
    assert(res[0] == res[1] == res[2] == res[3] == pos2[1])

def test_get_der():
    def f1(x):
        return x
    def f2(x, y):
        return x, y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    pos1 = 3
    pos2 = [3,4]
    dir1 = [1]
    dir2 = [0,1]

    assert(ad1.get_der(pos1, direction=None) == 1)
    assert(ad1.get_der(pos1, direction=dir1) == 1)

    assert(ad2.get_der(pos2, direction=None) == [1,1])
    assert(ad2.get_der(pos2, direction=dir2) == 1)

def test_get_der_vector():
    def f1(x):
        return x
    def f2(x, y):
        return x, y

    ad1 = pydif.autodiff_vector([[f1, f2], [f2, f1]])
    ad2 = pydif.autodiff_vector([f2, f2, f2, f2])

    pos1 = 3
    pos2 = [3,4]
    dir1 = [1]
    dir2 = [0,1]
    dir3 = [1,0]

    res = ad1.get_der(pos2, direction=None)
    assert(res[0][0] == res[1][1] == 1)
    assert(res[0][1] == res[1][0] == [1,1])

    res = ad1.get_der(pos2, direction=dir3)
    assert(res[0][0] == res[1][1] == 1)
    assert(res[0][1] == res[1][0] == 1)

    res = ad2.get_der(pos2, direction=None)
    assert(res[0] == res[1] == res[2] == res[3] == [1,1])

    res = ad2.get_der(pos2, direction=dir2)
    assert(res[0] == res[1] == res[2] == res[3] == 1)

def test_get_der2():
    def f1(x):
        return x
    def f2(x, y):
        return x, y

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    pos1 = 3
    pos2 = [3,4]
    dir1 = [1]
    dir2 = [0,1]

    assert(ad1.get_der(pos1, direction=None, order=2) == 0)
    assert(ad1.get_der(pos1, direction=dir1, order=2) == 0)

    assert(ad2.get_der(pos2, direction=None, order=2) == [0,0])
    assert(ad2.get_der(pos2, direction=dir2, order=2) == 0)

def test_multiply_add_simple():
    alpha = 2
    pos = 2

    def f1(x):
        return alpha*x+3
    def f2(x):
        return x*alpha+3
    def f3(x):
        return 3+x*alpha
    def f4(x):
        return 3+alpha*x

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)
    ad3 = pydif.autodiff(f3)
    ad4 = pydif.autodiff(f4)

    assert(ad1.get_val(pos) == 7)
    assert(ad2.get_val(pos) == 7)
    assert(ad3.get_val(pos) == 7)
    assert(ad4.get_val(pos) == 7)

    assert(ad1.get_der(pos) == 2)
    assert(ad2.get_der(pos) == 2)
    assert(ad3.get_der(pos) == 2)
    assert(ad4.get_der(pos) == 2)

    assert(ad1.get_der(pos, order=2) == 0)
    assert(ad1.get_der(pos, order=2) == 0)
    assert(ad1.get_der(pos, order=2) == 0)
    assert(ad1.get_der(pos, order=2) == 0)

def test_divide_add_simple():
    alpha = 2
    pos = 2

    def f1(x):
        return alpha/x+3
    def f2(x):
        return 3+alpha/x
    def f3(x):
        return x/alpha+3
    def f4(x):
        return 3+x/alpha

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)
    ad3 = pydif.autodiff(f3)
    ad4 = pydif.autodiff(f4)

    assert(ad1.get_val(pos) == 4)
    assert(ad2.get_val(pos) == 4)
    assert(ad3.get_val(pos) == 4)
    assert(ad4.get_val(pos) == 4)

    assert(ad1.get_der(pos) == -0.5)
    assert(ad2.get_der(pos) == -0.5)
    assert(ad3.get_der(pos) == 0.5)
    assert(ad4.get_der(pos) == 0.5)

    assert(ad1.get_der(pos, order=2) == 0.5)
    assert(ad2.get_der(pos, order=2) == 0.5)
    assert(ad3.get_der(pos, order=2) == 0)
    assert(ad4.get_der(pos, order=2) == 0)

def test_composite():
    pos = (1,2,3)

    def f1(x,y,z):
        return (1/(x*y*z)) + el.sin((1/x) + (1/y) + (1/z))
    def f2(x,y,z):
        return (1/(x*y*z))

    ad1 = pydif.autodiff(f1)
    ad2 = pydif.autodiff(f2)

    expected_val = (1/6) + np.sin(11/6)

    assert(ad1.get_val(pos) == expected_val)

    der1 = -(1/6) - np.cos(11/6) #d/dx
    der2 = -(1/12) - (np.cos(11/6)/4) #d/dy
    der3 = -(1/18) - (np.cos(11/6)/9) #d/dz

    assert(np.allclose(ad1.get_der(pos,wrt_variables=True),[der1,der2,der3]))

    assert(ad2.get_val(pos) == 1/(1*2*3))
    #http://www.wolframalpha.com/input/?i=d%2Fda+(1%2F(x(a)*y(a)*z(a))
    expected_der = -((2*3 + 1*3 + 1*2)/((1**2) * (2**2) * (3**2)))
    assert(np.isclose(float(ad2.get_der(pos)), expected_der))

    der2_1 = 2/(1*2*3) #d/dx^2
    der2_2 = 2/(1*((2)**3)*3) #d/dy^2
    der2_3 = 2/(1*2*((3)**3)) #d/dz^2
    assert(np.allclose(ad2.get_der(pos,wrt_variables=True,order=2),[der2_1, der2_2, der2_3]))

def test_derorder():
    def f1(x):
        return x

    ad1 = pydif.autodiff(f1)

    assert(ad1.get_der(2, order=1) == 1)
    assert(ad1.get_der(2, order=2) == 0)
    with pytest.raises(NotImplementedError):
        ad1.get_der(2, order=3)

def test_decorator():
    @diff
    def f1d(x):
        return x
    @diffdiff
    def f1dd(x):
        return x

    alpha=2

    @diff
    def f2d(x):
        return alpha*x+3
    @diffdiff
    def f2dd(x):
        return alpha*x+3

    pos = (1,2,3)

    @diff
    def f3d(x,y,z):
        return (1/(x*y*z)) + el.sin((1/x) + (1/y) + (1/z))

    assert(f1d(3) == 1)
    assert(f1dd(3) == 0)

    assert(f2d(2) == 2)
    assert(f2dd(2) == 0)

    der1 = -(1/6) - np.cos(11/6) #d/dx
    der2 = -(1/12) - (np.cos(11/6)/4) #d/dy
    der3 = -(1/18) - (np.cos(11/6)/9) #d/dz

    assert(np.allclose(f3d(pos),[der1,der2,der3]))
