import warnings
import numpy as np
import scipy as sp
from squidward.utils import invert, atleast_2d, check_valid_cov, is_invertible

np.seterr(over='raise')

class gaussian_process(object):
    def __init__(self,kernel=None,var_l=1e-15,inv_method='inv'):
        '''
        '''
        self.kernel = kernel
        self.var_l = var_l
        self.x = None
        self.y = None
        self.inv_method = inv_method
        self.K = None
        assert(kernel == None, 'Please specify a valid kernel.')
        assert(var_l >= 0.0, 'Invalid likelihood variance argument.')

    def fit(self,x,y):
        self.x = atleast_2d(x)
        self.y = atleast_2d(y)
        K = self.kernel.k(x,x)

        I = np.zeros(K.shape)
        idx = np.diag_indices(I.shape[0])
        I[idx] = self.var_l
        K += I

        if is_invertible(K) == False:
            warnings.warn('Kernel output of low rank. Matrix might not be invertible. Check kernel parameters. LU inversion suggested.')
        self.K = invert(K,self.inv_method)

    def posterior_predict(self,x_test,return_cov=False):
        K_s = self.kernel.k(x_test,self.x)
        mean = K_s.dot(self.K).dot(self.y)
        K_ss = self.kernel.k(x_test,x_test)
        cov = K_ss - np.dot(np.dot(K_s,self.K),K_s.T)
        check_valid_cov(cov)
        if is_invertible(cov) == False:
            warnings.warn('Covariance of low rank. Matrix might not be invertible.')
        if return_cov == True:
            return mean, cov
        else:
            var = atleast_2d(np.diag(cov))
            return mean, var

    def prior_predict(self,x_test,return_cov=False):
        mean = np.zero(x_test.shape[0])
        cov = self.kernel.k(x_test,x_test)
        check_valid_cov(cov)
        if is_invertible(cov) == False:
            warnings.warn('Covariance of low rank. Matrix might not be invertible.')
        if return_cov == True:
            return mean, cov
        else:
            var = atleast_2d(np.diag(cov))
            return mean

    def posterior_sample(self,x_test):
        mean,cov = posterior_predict(x_test,True)
        return np.random.multivariate_normal(mean,cov,1).T[:,0]

    def prior_sample(self,x_test):
        mean,cov = prior_predict(x_test,True)
        return np.random.multivariate_normal(mean,cov,1).T[:,0]
