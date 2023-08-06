import numpy as np

np.seterr(over='raise')

# future optimization
# https://stackoverflow.com/questions/47271662/what-is-the-fastest-way-to-compute-an-rbf-kernel-in-python

class rbf(object):
    def __init__(self,var_k,l):
        self.var_k = var_k
        self.l = l

    def _k(self,a,b):
        a = a.reshape(-1,1)
        b = b.reshape(-1,1)
        z = np.sum(a**2,1).reshape(-1,1) + np.sum(b**2,1) -2.0*a.dot(b.T)
        alpha = (1.0/(self.l**2))
        return self.var_k * np.exp(-0.5*alpha*z)

    def k(self,a,b):
        if len(a.shape) == 1:
            return self._k(a,b)
        output = 1
        for i in range(a.shape[1]):
            output *= self._k(a[:,i],b[:,i])
        return output
