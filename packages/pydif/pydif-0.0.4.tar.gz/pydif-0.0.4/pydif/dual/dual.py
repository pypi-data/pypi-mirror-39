"""dual.py
This file overloads operators dunder methods to allow for dual numbers to be used. The functions first try to work
with x as a dual number and falls back to treating x as a normal numerical type
Args:
    param1 (float): The value of a function at a point.
    param2 (array or array-like): An array of partial first derivatives at a point
    param2 (array or array-like): An array of partial second derivatives at a point

Returns:
    Dual Number Object: Returns a new Dual number object with the above parameters.

"""

import numpy as np
class Dual():

    #initialize derivative as a numpy array to handle partial derivatives
    def __init__(self, val , der, der2):
        self.val = val
        self.der = np.array(der)
        self.der2 = np.array(der2)

    #overload the addition method
    def __add__(self, x):
        try:
            return Dual(self.val +  x.val, self.der +  x.der, self.der2 +  x.der2)
        except AttributeError:
            return Dual(self.val +  x, self.der, self.der2)

    #overload radd by calling addition on the Dual number
    def __radd__(self, x):
        return self.__add__(x)

    #overload the subtraction method
    def __sub__(self, x):
        try:
            return Dual(self.val -  x.val, self.der -  x.der, self.der2 -  x.der2)
        except AttributeError:
            return Dual(self.val -  x, self.der, self.der2)

    #overload rsub
    def __rsub__(self, x):
        try:
            return Dual(self.val -  x.val, self.der -  x.der, self.der2 -  x.der2)
        except AttributeError:
            return Dual(x - self.val, self.der, self.der2)

    #overload multiplication
    def __mul__(self, x):
        try:
            return Dual(self.val * x.val, self.der * x.val + self.val * x.der, x.val * self.der2 + 2 * self.der * x.der + self.der * x.der2)
        except AttributeError:
            return Dual(self.val *  x, self.der *  x, self.der2 *  x)

    #overload rmul by calling multiplication on the Dual number
    def __rmul__(self, x):
        return self.__mul__(x)

    #overload division
    def __truediv__(self, x):
        try:
            return Dual(self.val/ x.val, (self.der * x.val - self.val * x.der)/(x.val)**2, (x.val ** 2 * self.der2 - x.val * (2 * self.der * x.der + self.val * x.der2) + 2 * self.val * x.der **2)/x.val**3)
        except AttributeError:
            return Dual(self.val /x, self.der / x, self.der2 / x)

    #overload rdivision by multiplying by the value to the negative first power
    def __rtruediv__(self, x):
        return Dual(x/self.val, -(x * self.der)/self.val ** 2, (2 * x * self.der ** 2 - x * self.val * self.der2 )/self.val**3)

    #overload power operator using formula for derivative of a function raised to a function if both are dual numbers
    def __pow__(self, x):
        try:
            return Dual(self.val**x.val, self.val**x.val*(self.der*(x.val/self.val)+x.der * np.log(self.val)), self.val ** x.val * ((x.val * self.der)/self.val + np.log(self.val) * x.der) ** 2 + self.val ** x.val * ((x.val * self.der2)/self.val + (2 * self.der * x.der)/self.val - (x.val * self.der**2)/self.val**2 + np.log(self.val) * x.der2))
        except AttributeError:
            return Dual(x**self.val, np.log(x) * x ** self.val  * self.der, np.log(x) * x  ** self.val * (self.der2 + np.log(x) * self.der  ** 2))

    #overload rpow similarly to above
    def __rpow__(self, x):
        return Dual(x**self.val, np.log(x) * x ** self.val  * self.der, np.log(x) * x  ** self.val * (self.der2 + np.log(x) * self.der  ** 2))

    #overload negation
    def __neg__(self):
        return Dual(-self.val, -self.der, -self.der2)

    #overload equality
    def __eq__(self, x):
        try:
            return (self.val == x.val and np.array_equal(self.der, x.der) and np.array_equal(self.der2, x.der2))
        except: #if not Dual, compare to value
            return self.val == x

    #overload inequality
    def __neq__(self, x):
        try:
            return (self.val != x.val or (np.array_equal(self.der, x.der) == False) or (np.array_equal(self.der2, x.der2) == False))
        except: #if not Dual, compare to value
            return (self.val != x)

    #overload repr by displaying as a list where the first value is the value and the second is a derivative
    def __repr__(self):
        return '[{0}, {1}, {2}]'.format(self.val, self.der, self.der2)
