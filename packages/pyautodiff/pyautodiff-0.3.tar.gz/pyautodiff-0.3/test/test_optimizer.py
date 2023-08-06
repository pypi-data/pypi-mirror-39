import pytest
from pyautodiff.optimizer import Optimizer

import numpy as np

def test_get_loss2():
    opt1 = Optimizer(loss='mse',optimizer='gd',regularizer='lasso',lam=0.01)
    with pytest.raises(Exception):
        opt1._get_loss_fn('yo')

def test_get_loss3():
    with pytest.raises(Exception):
        opt2=Optimizer(loss='mse',optimizer='homie',regularizer='lasso',lam=0.01)
        opt2._get_loss_fn('homie')

def test_cost():
    opt1 = Optimizer(loss='mse',optimizer='gd',regularizer='lasso',lam=0.01)
    assert type(opt1._get_cost_fn('mse', optimizer='gd')).__name__ == "method"

X2 = np.array([[1,0,1],[1,1,2],[1,2,-2]])
y2 = [-2,-3,21]

def test_opty1():
    opt=Optimizer(loss='mse',optimizer='gd',regularizer='lasso',lam=0.01)
    opt.fit(X2,y2,iters=1000)
    assert opt.coefs[0] <= 3

def user_mse(y,y_preds):
    return (y-y_preds)**2

def test_opty2():
    opt=Optimizer(loss=user_mse,optimizer='sgd',regularizer='ridge',lam=0.01)
    opt.fit(X2,y2,iters=1000)
    assert opt.coefs[0] <= 3

def test_opty3():
    opt=Optimizer(loss=user_mse,optimizer='sgd',lam=0.01)
    opt.fit(X2,y2,iters=1000)
    assert opt.coefs[0] <= 3

def test_opty4():
    opt=Optimizer(loss=user_mse,optimizer='gd',lam=0.01)
    opt.fit(X2,y2,iters=1000)
    assert opt.coefs[0] <= 3

def test_opty_verbose_gd():
    opt=Optimizer(loss=user_mse,optimizer='gd',lam=0.01)
    opt.fit(X2,y2,iters=1000, verbose=True)
    assert opt.coefs[0] <= 3

def test_opty_verbose_sgd():
    opt=Optimizer(loss=user_mse,optimizer='sgd',lam=0.01)
    opt.fit(X2,y2,iters=1000, verbose=True)
    assert opt.coefs[0] <= 3

def test_opty_verbose_steepestgd():
    opt=Optimizer(loss='mse',optimizer='steepestgd',lam=0.01)
    opt.fit(X2,y2,iters=1000, verbose=True)
    assert opt.coefs[0] <= 3

def test_opty_verbose_bfgs():
    opt=Optimizer(loss='mse',optimizer='bfgs',regularizer='ridge',lam=0.01)
    opt.fit(X2,y2,iters=1000, verbose=True)
    assert opt.coefs[0] <= 3

def test_opty_classification():
    opt=Optimizer(loss='mse',optimizer='bfgs',regularizer='ridge',lam=0.01,
                  problem_type='classification')
    opt.fit(X2,y2,iters=1000, verbose=True)
    assert opt.coefs[0] <= 3
    
# def test_opty_regression():
#     opt=Optimizer(loss='mse',optimizer='bfgs',regularizer='ridge',lam=0.01,
#                   problem_type='regression')
#     opt.fit(X2,y2,iters=1000, verbose=True)
#     assert opt.coefs[0] <= 3
    
def test_score():
    opt=Optimizer(loss='mse',optimizer='bfgs',regularizer='ridge',lam=0.01,
                  problem_type='classification')
    opt.fit(X2,y2,iters=1000, verbose=True)
    a = opt.score(X2,y2) 
    assert a>=0 
    
def test_score1():
    opt=Optimizer(loss='mse',optimizer='sgd',regularizer='ridge',lam=0.01,
                  problem_type='classification')
    opt.fit(X2,y2,iters=1000, verbose=True)
    a = opt.score(X2,y2) 
    assert a>=0

def test_score2():
    opt=Optimizer(loss='mse',optimizer='sgd',regularizer='ridge',lam=0.01,
                  problem_type='regression')
    opt.fit(X2,y2,iters=1000, verbose=True)
    a = opt.score(X2,y2) 
    assert a>=0
    
def test_score():
    opt=Optimizer(loss='mse',optimizer='bfgs',regularizer='ridge',lam=0.01,
                  problem_type='classification')
    opt.fit(X2,y2,iters=1000, verbose=True)
    a = opt.predict_proba(X2)[0] 
    assert a>=0 
    