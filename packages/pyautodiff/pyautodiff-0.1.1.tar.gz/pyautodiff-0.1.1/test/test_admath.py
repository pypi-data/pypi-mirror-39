import pytest
from autodiff.dual.dual import Dual
import autodiff.admath.admath as admath
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


def test_log_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log(x)
        assert np.log(test) == admath.log(test)
        assert np.log(test) == f.val
        assert 1/test == f.der

def test_log10_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log10(x)
        assert np.log10(test) == admath.log10(test)
        assert np.log10(test) == f.val
        assert 1/(test*np.log(10)) == f.der

def test_log2_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.log2(x)
        assert np.log2(test) == admath.log2(test)
        assert np.log2(test) == f.val
        assert 1/(test*np.log(2)) == f.der

def test_exp_fn__():
    tests = np.linspace(-100,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.exp(x)
        assert np.exp(test) == admath.exp(test)
        assert np.exp(test) == f.val
        assert np.exp(test) == f.der

def test_sqrt_fn__():
    tests = np.linspace(1,100,15)
    for test in tests:
        x = Dual(test)
        f = admath.sqrt(x)
        assert np.sqrt(test) == admath.sqrt(test)
        assert np.sqrt(test) == f.val
        assert 1/2*1/np.sqrt(test) == f.der
