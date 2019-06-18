import numpy as np
import pandas as pd

class BaseRegressor(object):
    
    def __init__(self):
        self.alpha = 1.0
        self.max_iter = 2000
        self.intercept_ = 0.0
        self.coef_ = None
        self.tol  = None
        self.args = None
        self.verbose = True
        self.loss_ = -np.inf 
        self.init_ = None
        
    def set_params(self, **kwargs): # throw an exception if the input C is not a float
        if 'alpha' in kwargs and not isinstance(kwargs['alpha'], float):
            raise TypeError('alpha must be of float type')
        for key in kwargs:
               self.__dict__[key] = kwargs[key] 
                
    def get_params(self, keyString): 
        return self.__dict__[keyString]
    
    def fit(self, X,y, init=None):
        options = {'maxiter':self.max_iter, 'disp':self.verbose}
        init = 0*np.ones(X.shape[1]+1) if init is None else init
        if init.shape[0] != X.shape[1] + 1:
                raise ValueError('init must be a 1D numpy array of shape %d' %(X.shape[1]+1))
        sol = minimize(self.loss, init, args=(self.augment(X),y), tol=self.tol, options=options, method='Nelder-Mead')
        x   = sol['x']
        self.n_iter     = sol['nit']
        self.loss_      = sol['fun']
        self.intercept_ = x[0]
        self.coef_      = x[1:]
        self.init_      = init
        
    def predict(self, X):    # X is a 2D array-like object
        if isinstance(X, list): X0 = np.array(X)
        elif isinstance(X, pd.DataFrame): X0 = X.values
        elif isinstance(X, np.ndarray): X0 = X
        else:
            raise TypeError('The input needs to be nested list/numpy array/data frame of a 2D object')
        if len(X.shape)!=2:
            raise ValueError('X needs to be of 2D')
            
        X0 = self.augment(X0)
        beta = self.intercept_ * np.ones(1+self.coef_.shape[0])
        beta[1:] = self.coef_
        return np.sum(X0 * beta.reshape((1,-1)), axis=1)
        
    
    def augment(self, X):
        return np.hstack((np.ones((X.shape[0], 1)),X))
    
    def rss(self, X0, y, beta):
        return np.sum((np.sum(X0 * beta.reshape(1,-1), axis=1) - y)**2)
    
    def _parseArgs(self, *args):
        X0, y = args[0], args[1]
        if X0.shape[0] != y.shape[0]:
               raise ValueError('X0 and y need to have equal sample size')
        return X0, y        
    
    def loss(self, beta, *args):
        pass
        
