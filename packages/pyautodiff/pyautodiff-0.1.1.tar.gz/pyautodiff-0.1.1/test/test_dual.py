import pytest
from autodiff.dual import dual
import numpy as np

## Unary operation test
def test__neg__():
    x = dual.Dual(3)
    f = -x
    assert f.val == -3
    assert f.der == -1
    
def test__pos__():
    x = dual.Dual(-3)
    f = +x
    assert f.val == -3
    assert f.der == 1


## Addition operation test

def test1__add__():
    x = dual.Dual(3)
    f = 6*x + 9
    assert f.val == 27
    assert f.der == 6
    
def test2__add__():
    x = dual.Dual(2)
    f = 6*x + 4*x
    assert f.val == 20
    assert f.der == 10
    
def test__radd__():
    x = dual.Dual(2)
    f = 4 + 4*x
    assert f.val == 12
    assert f.der == 4
    
    
    
## Substraction operation test
    
def test1__sub__():
    x = dual.Dual(2)
    f = 6*x - 9
    assert f.val == 3
    assert f.der == 6
    
def test2__sub__():
    x = dual.Dual(3)
    f = 6*x - 4*x
    assert f.val == 6
    assert f.der == 2
    
def test__rsub__():
    x = dual.Dual(1)
    f = 4 - 4*x
    assert f.val == 0
    assert f.der == -4
    
    
    
## Multiplication operation test

def test1__mul__():
    x = dual.Dual(2)
    f = x * 9
    assert f.val == 18
    assert f.der == 9
    
def test2__mul__():
    x = dual.Dual(1)
    f = x * x
    assert f.val == 1
    assert f.der == 2
    
def test__rmul__():
    x = dual.Dual(3)
    f = 4 * x
    assert f.val == 12
    assert f.der == 4
    
    
    
## Division operation test 

def test1__truediv__():
    x = dual.Dual(2)
    f = x / 10
    assert f.val == 0.2
    assert f.der == 0.1
    
def test2__truediv__():
    x = dual.Dual(1)
    f = (2*x ** 2) / (4*x)
    assert f.val == 0.5
    assert f.der == 0.5
    
def test__rtruediv__():
    x = dual.Dual(2)
    f =  1 / x
    assert f.val == 0.5
    assert f.der == -0.25
    
    

# Power operation test

def test1__pow__():
    x = dual.Dual(2)
    f = x ** x
    assert f.val == 4.0
    assert f.der == 2*(2+2*np.log(2))
    
def test2__pow__():
    x = dual.Dual(2)
    f = x ** 2
    assert f.val == 4
    assert f.der == 4

def test__rpow__():
    x = dual.Dual(2)
    f = 2 ** x
    assert f.val == 4.0
    assert f.der == np.log(2) * 2 ** 2 

    