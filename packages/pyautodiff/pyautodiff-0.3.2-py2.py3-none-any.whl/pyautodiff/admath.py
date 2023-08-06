from pyautodiff.dual import Dual as Dual
import numpy as np

def sin(x):
    """Calculate sine of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the sine value
    """
    if (isinstance(x,Dual)):
        x.der = np.cos(x.val)*x.der
        x.val = np.sin(x.val)
        return x
    else:
        return np.sin(x)

def cos(x):
    """Calculate cosine of the input

        Keyword arguments:numpy.tan
        x -- a real number or a dual number

        Return:
        the cosine value
    """
    if (isinstance(x,Dual)):
        x.der = -1 * np.sin(x.val)*x.der
        x.val = np.cos(x.val)
        return x
    else:
        return np.cos(x)

def tan(x):
    """Calculate tangent of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the tanget value
    """
    if (isinstance(x,Dual)):
        x.der = 1/np.cos(x.val)**2*x.der
        x.val = np.tan(x.val)
        return x
    else:
        return np.tan(x)


def log(x):
    """Calculate the natural log of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the natural log value
    """
    if (isinstance(x,Dual)):
        x.der = (1/x.val)*x.der
        x.val = np.log(x.val)
        return x
    else:
        return np.log(x)

def log2(x):
    """Calculate the log2 of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the log2 value
    """
    if (isinstance(x,Dual)):
        x.der = (1/(x.val*np.log(2)))*x.der
        x.val = np.log2(x.val)
        return x
    else:
        return np.log2(x)

def log10(x):
    """Calculate the log10 of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the log10 value
    """
    if (isinstance(x,Dual)):
        x.der = (1/(x.val*np.log(10)))*x.der
        x.val = np.log10(x.val)
        return x
    else:
        return np.log10(x)

def logb(x, base):
    """Calculate the log of the input with bases b

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the log value with base b
    """
    if (isinstance(x,Dual)):
        x.der = (1/x.val/np.log(base)) * x.der
        x.val = np.log(x.val) / np.log(base)
        return x
    else:
        return np.log(x) / np.log(base)

def exp(x):
    """Calculate the exponential of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the exponential value
    """
    if (isinstance(x,Dual)):
        x.der = np.exp(x.val) * x.der
        x.val = np.exp(x.val)
        return x
    else:
        return np.exp(x)

def power(x1, x2):
    """Calculate the exponential of the input x1 with base x2

        Keyword arguments:
        x1 -- a real number or a dual number
        x2 -- a real number or a dual number

        Return:
        the exponential value x1 with base x2
    """
    if (isinstance(x1,Dual)) and (isinstance(x2,Dual)):
        # da^u/dx = ln(a) a^u du/dx
        factor = x1.val ** (x2.val -1)
        sum_1 = x2.val * x1.der
        sum_2 = x1.val * np.log(x1.val) * x2.der
        temp = factor * (sum_1 + sum_2)
        return Dual(x1.val ** x2.val, temp)
    elif (isinstance(x1,Dual)):
        # du^n/dx = n * u^(n-1) * du/dx
        temp = x2 * x1.val ** (x2-1) * x1.der
        return Dual(x1.val ** x2, temp)
    elif (isinstance(x2,Dual)):
        # da^u/dx = ln(a) a^u du/dx
        temp = np.log(x2.val) * x2.val ** x1 * x2.der
        return Dual(x1 ** x2.val, temp)
    else:
        return np.power(x1,x2)


def sqrt(x):
    """Calculate the square root of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the square root value
    """
    if (isinstance(x,Dual)):
        x.der = 0.5/np.sqrt(x.val) * x.der
        x.val = np.sqrt(x.val)
        return x
    else:
        return np.sqrt(x)

def arcsin(x):
    """Calculate the arcsin of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the arcsin value
    """
    if (isinstance(x,Dual)):
        x.der = 1 / np.sqrt(1 - x.val **2) * x.der
        x.val = np.arcsin(x.val)
        return x
    else:
        return np.arcsin(x)

def arccos(x):
    """Calculate the arccos of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the arccos value
    """
    if (isinstance(x,Dual)):
        x.der = -1 / np.sqrt(1 - x.val**2) * x.der
        x.val = np.arccos(x.val)
        return x
    else:
        return np.arccos(x)

def arctan(x):
    """Calculate the arccos of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the arctan value
    """
    if (isinstance(x,Dual)):
        x.der = 1 / (1 + x.val**2) * x.der
        x.val = np.arctan(x.val)
        return x
    else:
        return np.arctan(x)

def sinh(x):
    """Calculate the sinh of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the sinh value
    """
    if (isinstance(x,Dual)):
        x.der = np.cosh(x.val) * x.der
        x.val = np.sinh(x.val)
        return x
    else:
        return np.sinh(x)

def cosh(x):
    """Calculate the cosh of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the cosh value
    """
    if (isinstance(x,Dual)):
        x.der = np.sinh(x.val) * x.der
        x.val = np.cosh(x.val)
        return x
    else:
        return np.cosh(x)

def tanh(x):
    """Calculate the tanh of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the tanh value
    """
    if (isinstance(x,Dual)):
        x.der = x.der / np.cosh(x.val)
        x.val = np.tanh(x.val)
        return x
    else:
        return np.tanh(x)

def help_logistic(x, L=1, k=1, x0=1):
    return L/(1 + np.exp(-k*(x-x0)))

def logistic(x, L=1, k=1, x0=1):
    """Calculate the logistic of the input

        Keyword arguments:
        x -- a real number or a dual number

        Return:
        the logistic value
    """
    if (isinstance(x,Dual)):
        temp = help_logistic(x.val,L,k,x0)
        x.der = temp * (1 - temp ) * x.der
        x.val = temp
        return x
    else:
        return help_logistic(x, L, k, x0)


# (5*x+3+4)
# der = 5*x.der, val = 5*x.val+3+4
def sum(xs):
    """Calculate the sum of the input

        Keyword arguments:
        xs -- a real value list

        Return:
        the sum of the array
    """
    cur_val = 0
    cur_der = 0
    is_dual = False
    # print('xs')
    for x in xs:
        # print('val: ',x.val)
        if (isinstance(x,Dual)):
            is_dual = True
            cur_der += x.der
            cur_val += x.val
        else:
            cur_val += x
    if is_dual:
        return Dual(cur_val,cur_der)
    else:
        return cur_val

def abs(x):
    """Calculate the sum of the input

        Keyword arguments:
        x -- a real value

        Return:
        the absolute value of x
    """
    if (isinstance(x,Dual)):
        x.der = x.val/np.abs(x.val)
        x.val = np.abs(x.val)
        return x
    else:
        return np.abs(x)
