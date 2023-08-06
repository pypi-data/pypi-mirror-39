import numpy as np
import scipy.stats as st

def rmse(p, y):
    return np.sqrt(np.sum((p - y)**2)/y.shape[0])

def likelihood(mean, cov, y, log=False, allow_singular=False):
    mean = mean[:, 0]
    if log == False:
        return st.multivariate_normal(mean, cov, allow_singular=allow_singular).pdf(y)
    else:
        return st.multivariate_normal(mean, cov, allow_singular=allow_singular).logpdf(y)

def acc(p, y):
    if y.shape[0] <= 1:
        return y.T[y.T == p].shape[0] / y.shape[0]
    else:
        return y[y == p].shape[0] / y.shape[1]

def brier_score():
    raise NotImplementedError()

def precision():
    raise NotImplementedError()

def recall():
    raise NotImplementedError()

def roc_auc():
    raise NotImplementedError()

def posterior_checks():
    raise NotImplementedError()

def variational_inference():
    raise NotImplementedError()

def MCMC():
    raise NotImplementedError()

def bayes_nets_approximation():
    raise NotImplementedError()
