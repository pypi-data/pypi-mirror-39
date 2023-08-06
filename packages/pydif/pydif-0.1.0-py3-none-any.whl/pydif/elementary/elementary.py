"""elementary.py
This file overloads elementary functions which do no have dunder methods
including exponential and trig functions. The functions first try to work 
with x as a dual number and falls back to treating x as a normal numerical type"""

from pydif.dual.dual import Dual 
import numpy as np 

def cos(x):
    try: 
        return Dual(np.cos(x.val), -1 * x.der * np.sin(x.val), x.der**2 * -1 * np.cos(x.val)- x.der2 * np.sin(x.val))
    except:
        return np.cos(x)

def sin(x):
    try: 
        return Dual(np.sin(x.val),  x.der * np.cos(x.val), x.der2 * np.cos(x.val) - x.der **2 * np.sin(x.val))
    except:
        return np.sin(x)

def tan(x):
    try:
        return Dual(np.tan(x.val), x.der * (1/np.cos(x.val))**2, (1/np.cos(x.val)**2) * (x.der2 + 2*x.der**2 * np.tan(x.val)))
    except:
        return np.tan(x)

def arccos(x):
    try:
        return Dual(np.arccos(x.val), -1 * x.der * 1/(np.sqrt(1- x.val**2)), -1 * (x.val**2*-1*(x.der2) + x.der2 + x.val * x.der**2)/(1- x.val**2)**(3/2))
    except:
        return np.arccos(x)


def arcsin(x):
    try:
        return Dual(np.arcsin(x.val), x.der * 1/(np.sqrt(1- x.val**2)), (x.val*x.der**2 - (x.val**2 -1 )*x.der2)/(1-x.val**2)**(3/2))
    except:
        return np.arcsin(x)


def arctan(x):
    try:
        return Dual(np.arctan(x.val), x.der * 1/(x.val**2 +1), ((x.val**2+1)*x.der2 - 2 * x.val * x.der**2)/(x.val**2 +1)**2)
    except:
        return np.arctan(x)

def sinh(x):
    try:
        return Dual(np.sinh(x.val), x.der * np.cosh(x.val), x.der2 * np.cosh(x.val) + x.der **2 * np.sinh(x.val))
    except:
        return np.sinh(x)

def cosh(x):
    try:
        return Dual(np.cosh(x.val), x.der * np.sinh(x.val), x.der2 * np.sinh(x.val) + x.der **2 *np.cosh(x.val))
    except:
        return np.cosh(x)

def tanh(x):
    try:
        return Dual(np.tanh(x.val), x.der * 1/(np.cosh(x.val)**2), (1/np.cosh(x.val))**2 * (x.der2 - 2*x.der**2 * np.tanh(x.val)))
    except:
        return np.tanh(x)

def arcsinh(x):
    try:
        return Dual(np.arcsinh(x.val), x.der * 1/np.sqrt(x.val**2 +1), (x.val**2 * x.der2 + x.der2 - x.val*x.der**2)/(x.val**2 + 1)**(3/2))
    except:
        return np.arcsinh(x)

def arccosh(x):
    try:
        return Dual(np.arccosh(x.val), x.der * (1/np.sqrt(x.val -1) * 1/(np.sqrt(x.val +1))), (x.val**2*x.der2 - x.der2 - x.val*x.der**2)/((x.val-1)**(3/2) *(x.val+1)**(3/2)))
    except:
        return np.arccosh(x)

def arctanh(x):
    try:
        return Dual(np.arctanh(x.val), -1 * x.der * 1/(x.val**2 -1), (-1*x.val**2*x.der2 + x.der2+ 2 * x.val * x.der**2)/(1-x.val**2)**2)
    except:
        return np.arctanh(x)

def exp(x):
    try:
        return Dual(np.exp(x.val), x.der * np.exp(x.val), np.exp(x.val) * (x.der2 + x.der**2))
    except:
        return np.exp(x)

def exp2(x):
    try:
        return Dual(np.exp2(x.val), np.exp2(x.val) * (x.der * np.log(2)), np.log(2)*np.exp2(x.val)*(x.der2 + np.log(2) * x.der**2))
    except:
        return np.exp2(x)

# natural log 
def log(x):
    try: 
        return Dual(np.log(x.val), (1 / float(x.val)) * x.der, (x.val * x.der2 - x.der**2)/(x.val**2)  )
    except:
        return np.log(x)    

# log base 2
def log2(x):
    try:
        return Dual(np.log2(x.val), 1/(x.val * np.log(2)) * x.der, (x.val * x.der2- x.der**2)/(np.log(2)* x.val**2))
    except:
        return np.log2(x)

# log base 10
def log10(x):
    try:
        return Dual(np.log10(x.val), 1/(x.val * np.log(10)) * x.der, (x.val * x.der2 - x.der**2)/(np.log(10)*x.val**2))
    except:
        return np.log10(x)


def sqrt(x):
    try:
        return Dual(np.sqrt(x.val), x.der * 1/(2*np.sqrt(x.val)), (2 * x.val * x.der2 - x.der**2)/(4 * x.val **(3/2)))
    except:
        return np.sqrt(x)

def sigmoid(x):
    try:
        a = x.val
        return 1/(1 + exp(-1*x))
    except:
        return 1/(1+ np.exp(-1 * x))

def relu(x):
    try:
        u = np.maximum(0, x.val)
        v = np.where(u > 0, 1, 0)
        return Dual(u, x.der * v, 0)
    except:
        return np.maximum(0, x)

