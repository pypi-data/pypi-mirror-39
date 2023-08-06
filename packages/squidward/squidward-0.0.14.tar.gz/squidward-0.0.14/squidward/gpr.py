import warnings
import numpy as np
import scipy as sp
from squidward.utils import invert, atleast_2d, check_valid_cov

np.seterr(over='raise')

class gaussian_process(object):
    def __init__(self, kernel=None, var_l=1e-15, inv_method='inv'):
        '''
        Description
        ----------
        Model object for single output gaussian process (SOGP) regression.

        Parameters
        ----------
        kernel : kernel object
            An object with an associated function k that takes in 2 arrays and
            returns a valid K matrix. Valid K matricies are positive
            semi-definite and not singular.
        var_l: float
            The liklihood variance of the process. Currently only supports
            scalars for homoskedastic regression.
        inv_method: string
            A string argument choosing an inversion method for matrix K when
            fitting the gaussian process.
        '''
        self.kernel = kernel
        self.var_l = var_l
        self.x = None
        self.y = None
        self.inv_method = inv_method
        self.K = None
        self.fitted = False
        assert(kernel == None, 'Model object must be instantiated with a valid kernel object.')
        assert(var_l >= 0.0, 'Invalid likelihood variance argument.')

    def fit(self, x, y):
        '''
        Description
        ----------
        Fit the model to data. This function takes in training data
        (x: features, y: targets) and fits the K matrix to that data. The
        predict function can then be used to make predictions.

        Parameters
        ----------
        x: array_like
            An array containing the model features.
        y: array_like
            An array containing the model targets (currently only supports
            single outputs).
        '''
        self.x = atleast_2d(x)
        self.y = atleast_2d(y)
        K = self.kernel.k(x, x)

        I = np.zeros(K.shape)
        idx = np.diag_indices(I.shape[0])
        I[idx] = self.var_l
        K += I

        self.K = invert(K, self.inv_method)
        self.fitted = True

    def posterior_predict(self, x_test, return_cov=False):
        '''
        Description
        ----------
        Make predictions based on fitted model. This function takes in a set of
        test points to make predictions on and returns the mean function of the
        gaussian process and a measure of uncertainty (either covariance or
        variance).

        Parameters
        ----------
        x_test: array_like
            Feature input for points to make predictions for.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.
        '''
        if self.fitted = False:
            raise ValueError('Please fit the model before trying to make posterior predictions!')
        # Gaussian Processes for Machine Learning Eq 2.18/2.19
        K_s = self.kernel.k(x_test, self.x)
        mean = K_s.dot(self.K).dot(self.y)
        K_ss = self.kernel.k(x_test, x_test)
        cov = K_ss - np.dot(np.dot(K_s, self.K), K_s.T)
        check_valid_cov(cov)
        if return_cov == True:
            return mean, cov
        var = atleast_2d(np.diag(cov))
        return mean, var

    def prior_predict(self, x_test, return_cov=False):
        '''
        Description
        ----------
        Make predictions. This function takes in a set of test points to make
        predictions on and returns the mean function of the prior of the
        gaussian process and a measure of uncertainty (either covariance or
        variance).

        Parameters
        ----------
        x_test: array_like
            Feature input for points to make predictions for.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.
        '''
        mean = np.zero(x_test.shape[0])
        cov = self.kernel.k(x_test, x_test)
        check_valid_cov(cov)
        if return_cov == True:
            return mean, cov
        var = atleast_2d(np.diag(cov))
        return mean, var

    def posterior_sample(self, x_test):
        '''
        Description
        ----------
        Draw a function from the fitted posterior.

        Parameters
        ----------
        x_test: array_like
            Feature input for points to draw samples for.
        '''
        mean, cov = posterior_predict(x_test, True)
        return np.random.multivariate_normal(mean, cov, 1).T[:, 0]

    def prior_sample(self, x_test):
        '''
        Description
        ----------
        Draw a function from the prior.

        Parameters
        ----------
        x_test: array_like
            Feature input for points to draw samples for.
        '''
        mean, cov = prior_predict(x_test, True)
        return np.random.multivariate_normal(mean, cov, 1).T[:, 0]

class gaussian_process_stable_cholesky(object):
    def cholesky_predict(self, x, y, x_test, kernel, var_l=1e-15, return_cov=False):
        '''
        Description
        ----------
        Model object for single output gaussian process (SOGP) regression. This
        object uses algorithm 2.1 (pg.19) from Gaussian Processes for Machine
        Learning for increased numerical stability and faster performance.

        Parameters
        ----------
        x: array_like
            An array containing the model features.
        y: array_like
            An array containing the model targets (currently only supports
            single outputs - SOGP).
        x_test: array_like
            Feature input for points to make predictions for.
        kernel : kernel object
            An object with an associated function k that takes in 2 arrays and
            returns a valid K matrix. Valid K matricies are positive
            semi-definite and not singular.
        var_l: float
            The liklihood variance of the process. Currently only supports
            scalars for homoskedastic regression.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.
        '''
        assert(kernel == None, 'Model object must be instantiated with a valid kernel object.')
        assert(var_l >= 0.0, 'Invalid likelihood variance argument.')

        x = atleast_2d(x)
        y = atleast_2d(y)

        # Gaussian Processes for Machine Learning Eq 2.18/2.19
        K = kernel.k(x, x)
        K_ = kernel.k(x, x_test)
        K_ss = kernel.k(x_test, x_test)

        I = np.zeros(K.shape)
        idx = np.diag_indices(I.shape[0])
        I[idx] = var_l
        K += I

        # More numerically stable
        # Gaussian Processes for Machine Learning Alg 2.1
        L = np.linalg.cholesky(K)
		alpha = np.linalg.solve(L.transpose(), np.linalg.solve(L, y))
		V = np.linalg.solve(L, K_)
		mean = np.dot(K_.transpose() , alpha)
		cov = K_ss - np.dot(V.transpose(), V)
        check_valid_cov(cov)
        if return_cov == True:
            return mean, cov
        var = atleast_2d(np.diag(cov))
        return mean, var
