import pytest
from autodiff.interface.interface import AutoDiff as AD
import autodiff.admath.admath as admath

import numpy as np


def my_fn_1d(x,y):
	return x**2 + y**2

def test_list():
	fn = AD(my_fn_1d)
	der = fn.get_der([1,2])
	val = fn.get_val([1,2])
	assert der == [2, 4]
	assert val == 5

def test_list_lists():
	fn = AD(my_fn_1d)
	der = fn.get_der([[1,2],[3,4],[5,6]])
	val = fn.get_val([[1,2],[3,4],[5,6]])
	assert der == [[2, 4], [6, 8], [10, 12]], [[1, 1], [1, 1], [1, 1]]
	assert val == [5, 25, 61]

def my_fn_2d(x, y):
	return [x**2 + y**2, x + 2+y]

def test_2d_fn():
	fn = AD(my_fn_2d, ndim=2)
	der = fn.get_der([1,2])
	val = fn.get_val([1,2])
	assert der == [[2, 4], [1, 1]]
	assert val == [5, 5]

def test_func_w_mult_params_single_var():
	fn = lambda x,y: x**2
	ad_fn = AD(fn)
	der = ad_fn.get_der([1,2])
	val = ad_fn.get_val([1,2])
	assert der == [2, 0]
	assert val == 1

def square_fn(x):
        return x ** 2

def test_square_fn():
	ad_square = AD(square_fn)
	der = ad_square.get_der(3)
	val = ad_square.get_val(3)
	assert der == 6
	assert val == 9
	der1 = ad_square.get_der([1,2,3,4])
	val1 = ad_square.get_val([1,2,3,4])
	assert der1 == [2, 4, 6, 8]
	assert val1 == [1, 4, 9, 16]

def test_get_der_types():
	with pytest.raises(TypeError):
        	AD.get_der('string')
	with pytest.raises(TypeError):
        	AD.get_der(dict[1:'a', 2:'b'])

def test_get_val_types():
	with pytest.raises(TypeError):
        	AD.get_val('string')
	with pytest.raises(TypeError):
        	AD.get_val(dict[1:'a', 2:'b'])

def test_get_der_lenlist():
	a = AD(lambda x,y: 3*x**2 + 2*y**3)
	with pytest.raises(Exception):
        	a.get_der(1, 2, 3)
	with pytest.raises(Exception):
			a.get_der([1, 2, 3], [3, 4, 5], [1, 3, 4])

def test_get_val_lenlist():
	a = AD(lambda x,y: 3*x**2 + 2*y**3)
	with pytest.raises(Exception):
        	a.get_val(1, 2, 3)
	with pytest.raises(Exception):
			a.get_val([1, 2, 3], [3, 4, 5], [1, 3, 4])

def test_exception_der():
	fn = AD(my_fn_2d, ndim=2)
	with pytest.raises(Exception):
		fn.get_der([1,2,3])

def test_exception_val():
	fn = AD(my_fn_2d, ndim=2)
	with pytest.raises(Exception):
		fn.get_val([1,2,3])

def my_fn_cos(x):
	return 5*admath.cos(x)

def my_fn_nested_1(x):
	return 5*x**2 * 2*admath.cos(x)

def test_cos():
	cos_fn = AD(my_fn_cos)
	assert cos_fn.get_der(5) == -5*np.sin(5)
	assert cos_fn.get_val(5) == 5*np.cos(5)

def test_nested_1():
	nested_fn = AD(my_fn_nested_1)
	xs = [-10,2,5,10]
	for x in xs:
		assert nested_fn.get_der(x) == pytest.approx(-10*x*(x*np.sin(x)-2*np.cos(x)))
		assert nested_fn.get_val(x) == pytest.approx(5*x**2 * 2*np.cos(x))

def mul_array(x, y):
    return [x**2 * y**2, x + y, 2*x]

def test_mul_array():
	ad_mul_array = AD(mul_array, ndim=3)
	val = ad_mul_array.get_val([[1,2],[1,2],[1,2]])
	der = ad_mul_array.get_der([[1,2],[1,2],[1,2]])
	assert val == [[4, 3, 2], [4, 3, 2], [4, 3, 2]]
	assert der == [[[8, 4], [1, 1], [2, 0]], [[8, 4], [1, 1], [2, 0]], [[8, 4], [1, 1], [2, 0]]]
