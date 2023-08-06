import sys
import os
import numpy as np
from inspect import signature
import scipy.optimize
from collections import Iterable
sys.path.append(os.path.join(os.getcwd(),'pydif'))
np.warnings.filterwarnings('ignore')
from pydif.pydif import autodiff

class Optimize():
    def __init__(self, func):
        self.func = func
        self.num_params = len(signature(func).parameters)

    def wrapper_func_(x):
        return self.func(*x)


    def gradient_descent(self, init_pos, step_size=0.1, max_iters=100, precision=0.001, return_hist=False):
        num_params = len(signature(self.func).parameters)
        badDimentionsMsg = 'poorly formatted initial position. should be of length {}.'.format(num_params)
        if num_params != len(init_pos):
            raise ValueError(badDimentionsMsg)

        cur_pos = init_pos
        iters = 0
        dfdx = autodiff(self.func)
        val = dfdx.get_val(init_pos)

        if isinstance(val, Iterable):
            raise ValueError("The optimize class only optimizes scalar valued functions")

        # pre allocate history array
        hist = [cur_pos]
        prev_step_size = 100 + precision
        while (prev_step_size > precision and iters < max_iters):
            jac = dfdx.get_der(cur_pos, wrt_variables=True)
            prev_pos = cur_pos
            cur_pos = cur_pos - step_size * jac
            prev_step_size = np.linalg.norm(abs(cur_pos - prev_pos))
            iters += 1
            hist.append(cur_pos) #store history
        np.array(hist)

        if return_hist:
            return cur_pos, hist
        else:
            return cur_pos

    def delta_B(self, y, s, B):
        y = y.reshape((self.num_params, 1))
        s = s.reshape((self.num_params, 1))
        return np.matmul(y, y.T)/np.matmul(y.T, s)-np.matmul(np.matmul(np.matmul(B, s), s.T), B)/(np.matmul(np.matmul(s.T, B),s))

    def BFGS(self, init_pos, max_iters=100, precision=10**-8, return_hist=False):
        #set original values
        coord = init_pos

        hist = [coord] #preallocate array

        #set inital conditions
        s = 0
        iterations = 0
        step = 10000
        B = np.identity(self.num_params)
        dfdx = autodiff(self.func)

        #set conditions for while loop
        while ((iterations <= max_iters) and (step >= precision)):
            s = np.linalg.solve(B, -dfdx.get_der(coord, wrt_variables = True)) #step
            step = np.linalg.norm(s) #step size
            y = dfdx.get_der(coord+s, wrt_variables = True) - dfdx.get_der(coord, wrt_variables = True) #new y
            coord = coord + s #new coord
            B = B + self.delta_B(y, s, B) #get new B
            iterations += 1
            hist.append(coord)
        hist = np.array(hist)

        if return_hist:
            return coord, hist
        else:
            return coord

    #define steepest descent
    def steepest(self, init_pos, step_size=0.1, max_iters=100, precision=0.001, return_hist=False):

        num_params = len(signature(self.func).parameters)
        badDimentionsMsg = 'poorly formatted initial position. should be of length {}.'.format(num_params)

        if num_params != len(init_pos):
            raise ValueError(badDimentionsMsg)

        cur_pos = init_pos
        iters = 0
        dfdx = autodiff(self.func)
        val = dfdx.get_val(init_pos)

        if isinstance(val, Iterable):
            raise ValueError("The optimize class only optimizes scalar valued functions")

        #preallocate arrays
        hist = [cur_pos]

        #set inital conditions
        iters = 0
        s = 0
        step = 100000

        #define conditions to break loop
        while ((iters <= max_iters) and (step >= precision)):
            s = -dfdx.get_der(cur_pos, wrt_variables = True) #step
            def line_to_search(step):
                return self.func(*(np.array(cur_pos)+step*s))
            n = scipy.optimize.minimize(line_to_search, 1).x[0]
            # n = line_search(self.wrapper_func_, dfdx.get_der, cur_pos, s)[0]
            print(n)
            step = np.linalg.norm(n*s) #set step size
            cur_pos = cur_pos + n * s #append value after step
            iters += 1 #count step
            hist.append(cur_pos) #store history
        np.array(hist)
        print(hist)

        if return_hist:
            return cur_pos, hist
        else:
            return cur_pos
