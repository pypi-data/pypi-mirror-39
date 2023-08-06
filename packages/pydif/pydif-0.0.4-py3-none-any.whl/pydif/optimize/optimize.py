import sys
import os
import numpy as np
from inspect import signature
from collections import Iterable
sys.path.append(os.path.join(os.getcwd(),'pydif'))
from pydif.pydif import autodiff

class Optimize():
    def __init__(self, func):
        self.func = func

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
            s = -dfdx.get_val(cur_pos) #step
            n = line_search(f, grad_f, cur_pos, s)[0] #TODO replace line_search
            step = np.linalg.norm(n*s) #set step size
            cur_pos = cur_pos + n * s #append value after step
            iters += 1 #count step
            hist.append(cur_pos) #store history
        np.array(hist)

        if return_hist:
            return cur_pos, hist
        else:
            return cur_pos

    def newton(self, init_pos, step_size=0.1, max_iters=100, precision=0.001, return_hist=False):

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
        s_k = 0
        step = 10000

        #TODO make hessian a function or change the call in the line below
        hessian = dfdx.get_der(cur_pos, wrt_variables=True, order = 2)

        #define conditions to break loop
        while ((iters <= max_iters) and (step >= precision)):
            s = np.linalg.solve(hessian(cur_pos), -dfdx.get_val(cur_pos)) #TODO make hessian work
            step = np.linalg.norm(s) # get step size
            cur_pos = cur_pos + s #step
            iters += 1 #increment counter
            hist.append(cur_pos) #store history
        hist = np.array(hist)

        if return_hist:
            return cur_pos, hist
        else:
            return cur_pos

    #function that allows for numerous initial conditions to be specified and plotted
    def plot_optimization(optimizer, initial_cond):

        #define initial conditions and plot results
        for init in initial_cond:
            min_val, total_it, hist = self.optimizer(init[0], init[1]) #call optimization function
            hist = np.array(hist)

            #format plot
            xs = np.linspace(-5,5,1000)
            ys = np.linspace(-5,5,1000)
            X, Y = np.meshgrid(xs, ys)
            Z = f(np.array([X,Y])) # TODO f is the function we  are optimizing
            plt.contour(X, Y, Z, 100)
            plt.plot(hist[:,0], hist[:,1])
            plt.ylim((ys[0],ys[-1]))
            plt.xlim((xs[0],xs[-1]))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.show()
