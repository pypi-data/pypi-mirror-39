"""pydif.py
This file implements the autodiff class. The autodiff class is initialized with a function that accepts single variables of the form f(x,y,z,...).
The autodiff object then allows for the evaluation of the value, and derivatives of a function at a specified position.

Args:
    param1 (function object): The function whose value and derivatives are to be evaluated.

Returns:
    autodiff Object: Returns a new autodiff object for evaluation of the specified function.

"""

from inspect import signature
from pydif.dual.dual import Dual
import numpy as np
import collections

class autodiff():

    #initialize autodiff class with a function
    def __init__(self, func):
        self.func = func
        self.num_params = len(signature(func).parameters)

    #make function parameters dual numbers and evaluate function at a position
    def _eval(self, pos, wrt_variables = False):
        if isinstance(pos, collections.Iterable):
            if wrt_variables:
                params = []
                for cursor, pos_i in enumerate(pos):
                    der_partials = np.zeros(self.num_params)
                    der_partials[cursor] = 1
                    params.append(Dual(pos_i, der_partials, np.zeros(self.num_params)))
            else:
                params = [Dual(pos_i,1,0) for pos_i in pos]
            return self.func(*params)
        else:
            if wrt_variables:
                params = Dual(pos,[1],[0])
            else:
                params = Dual(pos,1,0)
            return self.func(params)

    #check that the specified iterable is the same shape as the function (specified at object creation) input
    def _check_dim(self, item):
        badDimentionsMsg = 'poorly formatted position or direction. should be of length {}.'.format(self.num_params)
        if isinstance(item, collections.Iterable):
            if len(item) != self.num_params:
                raise ValueError(badDimentionsMsg)
        else:
            if self.num_params != 1:
                raise ValueError(badDimentionsMsg)

    def _enforce_unitvector(self, direction):
        tmp_direction = np.array(direction)
        magnitude = np.sqrt(tmp_direction.dot(tmp_direction))
        if magnitude == 0:
            raise ValueError('poorly formatted direction. should be a vector of non-zero magnitude.')
        if magnitude != 1:
            tmp_direction = tmp_direction / magnitude
        return tmp_direction

    #evaluate the value of the function at a specified position
    def get_val(self, pos, direction=None):
        if direction is None:
            self._check_dim(pos)
            res = self._eval(pos)
            if isinstance(res, collections.Iterable):
                return [i.val for i in res]
            else:
                return res.val
        else:
            self._check_dim(pos)
            self._check_dim(direction)
            self._enforce_unitvector(direction)
            res = self._eval(pos)
            if isinstance(res, collections.Iterable):
                return np.sum(np.array([i.val for i in res]) * direction)
            else:
                return res.val

    #evaluate the derivatives of the function at a specified position in a specified direction
    def get_der(self, pos, wrt_variables = False, direction=None, order=1):
        if order == 1:
            der_attr = 'der'
        elif order == 2:
            der_attr = 'der2'
        else:
            raise NotImplementedError('only first and second order derivatives are implemented.')

        if direction is None:
            self._check_dim(pos)
            res = self._eval(pos, wrt_variables)

            if isinstance(res, collections.Iterable):
                return [getattr(i, der_attr) for i in res]
            else:
                return getattr(res, der_attr)
        else:
            self._check_dim(pos)
            self._check_dim(direction)
            self._enforce_unitvector(direction)
            res = self._eval(pos, wrt_variables)

            if isinstance(res, collections.Iterable):
                return np.sum(np.array([getattr(i, der_attr) for i in res]) * direction)
            else:
                return getattr(res, der_attr)

class autodiff_vector():

    #initialize autodiff vector with autodiff objects
    def __init__(self, funcs):
        funcs = np.array(funcs)
        self.func_vector = np.empty(funcs.shape, dtype=object)
        for cursor, func in np.ndenumerate(funcs):
            self.func_vector[cursor] = autodiff(func)

    def _clean_dim(self, param, req_dim):
        if isinstance(param, collections.Iterable):
            return param[:req_dim]
        else:
            return param

    #evaluate the value of the vector function at a specified position
    def get_val(self, pos, direction=None):
        res = np.empty(self.func_vector.shape, dtype=object)
        for cursor, autodiff_obj in np.ndenumerate(self.func_vector):
            clean_pos = self._clean_dim(pos, self.func_vector[cursor].num_params)
            clean_direction = self._clean_dim(direction, self.func_vector[cursor].num_params)
            res[cursor] = autodiff_obj.get_val(clean_pos, clean_direction)
        return res

    #evaluate the derivative of the vector function at a specified position in a specified direction
    def get_der(self, pos, wrt_variables = False, direction=None, order=1):
        res = np.empty(self.func_vector.shape, dtype=object)
        for cursor, autodiff_obj in np.ndenumerate(self.func_vector):
            clean_pos = self._clean_dim(pos, self.func_vector[cursor].num_params)
            clean_direction = self._clean_dim(direction, self.func_vector[cursor].num_params)
            res[cursor] = autodiff_obj.get_der(clean_pos, wrt_variables, clean_direction, order)
        return res

def _eval_func(func, args, der_attr):
    if isinstance(args, collections.Iterable):
        params = []
        for cursor, arg in enumerate(args):
            der_partials = np.zeros(len(args))
            der_partials[cursor] = 1
            params.append(Dual(arg, der_partials, np.zeros(len(args))))
        res = func(*params)
        if isinstance(res, collections.Iterable):
            return [getattr(i, der_attr) for i in res]
        else:
            return getattr(res, der_attr)
    else:
        args = Dual(args,[1],[0])
        res = func(args)
        if isinstance(res, collections.Iterable):
            return [getattr(i, der_attr) for i in res]
        else:
            return getattr(res, der_attr)

def diff(func):
    def func_wrapper(args):
        return _eval_func(func, args, 'der')
    return func_wrapper

def diffdiff(func):
    def func_wrapper(args):
        return _eval_func(func, args, 'der2')
    return func_wrapper

if __name__ == '__main__':
    pass
