import pytest
from pyautodiff.dual import Dual
import pyautodiff.admath as admath
import numpy as np
import math


def test1__sin_fn__():
    x = Dual(0)
    f = admath.sin(x)
    assert f.val == 0
    assert f.der == 1


def test2__sin_fn__():
    tests = np.linspace(-10,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.sin(x)
        assert np.sin(test) == admath.sin(test)
        assert np.sin(test) == f.val
        assert np.cos(test) == f.der

def test1__cos_fn__():
    x = Dual(0)
    f = admath.cos(x)
    assert f.val == np.cos(0)
    assert f.der == -1*np.sin(0)


def test2__cos_fn__():
    tests = np.linspace(-10,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.cos(x)
        assert np.cos(test) == admath.cos(test)
        assert np.cos(test) == f.val
        assert -1*np.sin(test) == f.der

def test1__tan_fn__():
    x = Dual(0)
    f = admath.tan(x)
    assert f.val == 0
    assert f.der == 1
    assert admath.tan(0) == 0


def test_log_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log(x)
        assert np.log(test) == admath.log(test)
        assert np.log(test) == f.val
        assert 1/test == f.der

def test_log2_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log2(x)
        assert np.log2(test) == admath.log2(test)
        assert np.log2(test) == f.val
        assert 1/(test*np.log(2)) == f.der

def test_log10_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log10(x)
        assert np.log10(test) == admath.log10(test)
        assert np.log10(test) == f.val
        assert 1/(test*np.log(10)) == f.der

def test_logb__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.logb(x, np.exp(1))
        assert np.log(test) == admath.logb(test, np.exp(1))
        assert np.log(test) == f.val
        assert 1/test == f.der

def test_exp_fn__():
    tests = np.linspace(-100,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.exp(x)
        assert np.exp(test) == admath.exp(test)
        assert np.exp(test) == f.val
        assert np.exp(test) == f.der

def test_power1():
    x = Dual(2)
    f = admath.power(x,x)
    assert f.der == 2*(2+2*np.log(2))
    assert f.val == 4.0
    assert admath.power(2,2) == 4.0
    f = admath.power(x,2)
    assert f.val == 4
    assert f.der == 4
    f = admath.power(2,x)
    assert f.val == 4.0
    assert f.der == np.log(2) * 2 ** 2

def test_sqrt_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.sqrt(x)
        assert np.sqrt(test) == admath.sqrt(test)
        assert np.sqrt(test) == f.val
        assert 1/2*1/np.sqrt(test) == f.der

def test_arcsin():
    x = Dual(0)
    f = admath.arcsin(x)
    assert 1 == f.der
    assert 0 == f.val
    assert 0 == admath.arcsin(0)

def test_arccos():
    x = Dual(0)
    f = admath.arccos(x)
    assert -1 == f.der
    assert np.pi/2 == f.val
    assert np.pi/2 == admath.arccos(0)

def test_arctan():
    x = Dual(0)
    f = admath.arctan(x)
    assert 1 == f.der
    assert 0 == f.val
    assert 0 == admath.arctan(0)

def test_sinh():
    x = Dual(0)
    f = admath.sinh(x)
    assert 1 == f.der
    assert 0 == f.val
    assert 0 == admath.sinh(0)

def test_cosh():
    x = Dual(0)
    f = admath.cosh(x)
    assert 0 == f.der
    assert 1 == f.val
    assert 1 == admath.cosh(0)

def test_tanh():
    x = Dual(0)
    f = admath.tanh(x)
    assert 1 == f.der
    assert 0 == f.val
    assert 0 == admath.tanh(0)

def test_logistic():
    x = Dual(1)
    f = admath.logistic(x)
    assert 0.25 == f.der
    assert 0.50 == f.val
    assert 0.50 == admath.logistic(1)

def test_logistic():
    x = Dual(1)
    f = admath.logistic(x)
    assert 0.25 == f.der
    assert 0.50 == f.val
    assert 0.50 == admath.logistic(1)

def test_sum():
    x = Dual(1)
    f = admath.sum([x**2, x**3])
    assert 5 == f.der
    assert 2 == f.val
    assert 5 == admath.sum([2,3])

def test_abs():
    x = Dual(-1)
    f = admath.abs(x**3)
    assert -1 == f.der
    assert 1 == f.val
    assert 1 == admath.abs(-1)
