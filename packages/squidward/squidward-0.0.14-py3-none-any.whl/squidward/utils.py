import numpy as np
import scipy as sp
import scipy.linalg as la
import sys

def is_invertible(a, strict=False):
    if strict == True:
        if np.linalg.cond(a) < 1.0/sys.float_info.epsilon:
            return False
    return a.shape[0] == a.shape[1] and np.linalg.matrix_rank(a) == a.shape[0]

def check_valid_cov(cov):
    var = np.diag(cov)
    if var[var<0].shape[0] != 0:
        raise ValueError('Negative values in diagonal of covariance matrix.\nLikely cause is kernel inversion instability.\nCheck kernel variance.')
    return None

def atleast_2d(x):
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    return x

def atmost_1d(x):
    if len(x.shape) != 1:
        return x[:, 0]
    return x

def make_grid(coordinates=(-10, 10, 1)):
    min, max, grain = coordinates
    x = np.mgrid[min:max:grain, min:max:grain].reshape(2, -1).T
    if np.sqrt(x.shape[0]) % 2 == 0:
        s = int(np.sqrt(x.shape[0]))
    else:
        raise ValueError('Plot topology not square!')
    return x, s

def invert(A, method='inv'):
    if is_invertible(cov) == False:
        warnings.warn('Matrix is of low rank. Matrix might not be invertible. Recommend using LU decomposition for inversion.')
    if method == 'inv':
        return np.linalg.inv(A)
    elif method == 'pinv':
        return np.linalg.pinv(A)
    elif method == 'solve':
        I = np.identity(A.shape[-1], dtype=A.dtype)
        return np.linalg.solve(A, I)
    elif method == 'cholesky':
        c = np.linalg.inv(np.linalg.cholesky(A))
        return np.dot(c.T, c)
    elif method == 'svd':
        u, s, v = np.linalg.svd(A)
        return np.dot(v.transpose(), np.dot(np.diag(s**-1), u.transpose()))
    elif method == 'lu':
        P, L, U = la.lu(A)
        invU = np.linalg.inv(U)
        invL = np.linalg.inv(L)
        invP = np.linalg.inv(P)
        return invU.dot(invL).dot(invP)
    else:
        raise ValueError('Invalid inversion method argument.')
