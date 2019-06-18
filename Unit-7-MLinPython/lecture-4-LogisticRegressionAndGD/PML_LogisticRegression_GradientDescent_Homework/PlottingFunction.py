import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


def multivariate_normal(mu, sigma, width = 3):
    ## generate data for 3D surface plot
    X = np.linspace(mu[0] - width*sigma[0, 0], mu[0] + width*sigma[0, 0], 300)
    Y = np.linspace(mu[1] - width*sigma[1, 1], mu[1] + width*sigma[1, 1], 300)
    X, Y = np.meshgrid(X, Y)
    s_inv = sigma.I
    Z = np.exp(-(s_inv[0,0]*(X-mu[0])**2 + s_inv[1,1]*(Y-mu[1])**2 + \
                (s_inv[0,1]+s_inv[1,0])*(X-mu[0])*(Y-mu[1]))/2)
    return X, Y, Z/(2*np.pi)/(np.linalg.det(sigma))**.5

def multivariate_normal_plot(mu, sigma, n, step, color, ax, width=3, alpha=0.3, cmap=cm.copper, label=None):
    ## plot
    X, Y, Z = multivariate_normal(mu, sigma, width=width)
    ax.plot_surface(X, Y, Z, rstride=6, cstride=6, alpha=alpha, color=color, linewidth=0.5, label=label)
    cset = ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cmap, levels=np.arange(n)*step)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
def show_sample():
    np.random.seed(1)
    class_1 = stats.multivariate_normal(np.zeros([2]), np.eye(2)).rvs(50)
    class_2 = stats.multivariate_normal(np.ones([2])*3, np.array([[1, 0.5],[0.5, 1]])).rvs(53)
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(class_1[:, 0], class_1[:, 1], alpha=0.7, label='class blue')
    plt.scatter(class_2[:, 0], class_2[:, 1], color='green', alpha=0.7, label='class green')
    plt.legend(loc=2)

def data_1Dplot(x, y, xlabel=None, ylabel=None, labels=None, title=None):
    ## scatter plot the data
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.scatter(x, y, c=y, s=50, alpha=0.6)
    ## set labels
    if not xlabel is None:
        plt.xlabel(xlabel, size=12)
    if not ylabel is None:
        plt.ylabel(ylabel, size=12)
    ## set ticks for y
    y_ticks = np.unique(y)
    if not labels is None:
        plt.yticks(y_ticks, labels, rotation='vertical', size=12)
    ## set title
    if not title is None:
        plt.title(title, size=16)

def logistic_model_1Dplot(x, model, c="b"):
    x = np.array(x)
    num = 10000
    x = np.linspace(min(x), max(x), num=num).reshape(num,1)
    ## only plot the probability of prediction to be 1
    plt.plot(x, model.predict_proba(x)[:,1],
             ls='--', lw=2, c=c, label="Probability estimates")
    plt.plot(x, model.predict(x), lw=2, c=c, label="predictions")
    
        
def lda_1Dplot(x, model):
    x = np.array(x)
    num = 10000
    x = np.linspace(start=min(x), stop=max(x), num=num).reshape(num,1)
    plt.plot(x, model.predict(x), lw=2)
    for i in range(len(model.predict_proba(x)[0])):
        plt.plot(x, model.predict_proba(x)[:,i], ls='--', lw=2)  

def plotModel(model, x, y, label):
    '''
    model: a fitted model
    x, y: two variables, should arrays
    label: true label
    '''
    x_min = x.min() - 1
    x_max = x.max() + 1
    y_min = y.min() - 1
    y_max = y.max() + 1
    import matplotlib.pyplot as pl
    from matplotlib import colors
    colDict = {
        'red': [(0, 1, 1), (1, 0.7, 0.7)],
        'green': [(0, 1, 0.5), (1, 0.7, 0.7)],
        'blue': [(0, 1, 0.5), (1, 1, 1)]
    }
    cmap = colors.LinearSegmentedColormap('red_blue_classes', colDict)
    plt.cm.register_cmap(cmap=cmap)
    nx, ny = 200, 200
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, nx),
        np.linspace(y_min, y_max, ny)
    )
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ## plot colormap
    plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes')
    loc_half = np.argmin(np.abs(Z-0.5))
    loc_1    = np.argmin(np.abs(Z-1.0))
    ## plot boundaries
    if len(set(label))>2:
              plt.contour(xx, yy, Z, [Z[loc_half]], linewidths=1., colors='k')
    plt.contour(xx, yy, Z, [Z[loc_1]], linewidths=1., colors='k')
    ## plot scatters ans true labels
    plt.scatter(x, y, c = label)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

def data_1Dplot(x, y, xlabel=None, ylabel=None, labels=None, title=None):
    ## scatter plot the data
    plt.scatter(x, y, c=y, s=50, alpha=0.6)
    ## set labels
    if not xlabel is None:
        plt.xlabel(xlabel, size=12)
    if not ylabel is None:
        plt.ylabel(ylabel, size=12)
    ## set ticks for y
    y_ticks = np.unique(y)
    if not labels is None:
        plt.yticks(y_ticks, labels, rotation='vertical', size=12)
    ## set title
    if not title is None:
        plt.title(title, size=16)
        
def lda_1Dplot(x, model):
    x = np.array(x)
    num = 10000
    x = np.linspace(start=min(x), stop=max(x), num=num).reshape(num,1)
    plt.plot(x, model.predict(x), lw=2)
    for i in range(len(model.predict_proba(x)[0])):
        plt.plot(x, model.predict_proba(x)[:,i], ls='--', lw=2)

def plotModel(model, x, y, label):
    '''
    model: a fitted model
    x, y: two variables, should arrays
    label: true label
    '''
    x_min = x.min() - 1
    x_max = x.max() + 1
    y_min = y.min() - 1
    y_max = y.max() + 1
    import matplotlib.pyplot as pl
    from matplotlib import colors
    colDict = {
        'red': [(0, 1, 1), (1, 0.7, 0.7)],
        'green': [(0, 1, 0.5), (1, 0.7, 0.7)],
        'blue': [(0, 1, 0.5), (1, 1, 1)]
    }
    cmap = colors.LinearSegmentedColormap('red_blue_classes', colDict)
    plt.cm.register_cmap(cmap=cmap)
    nx, ny = 200, 200
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, nx),
        np.linspace(y_min, y_max, ny)
    )
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ## plot colormap
    plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes')
    ## plot boundaries
    plt.contour(xx, yy, Z, [0.5], linewidths=1., colors='k')
    plt.contour(xx, yy, Z, [1], linewidths=1., colors='k')
    ## plot scatters ans true labels
    plt.scatter(x, y, c = label)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)


def data_2Dplot(x, y, legends=None, xlabel=None, ylabel=None):
    x, y = np.array(x), np.array(y)
    if legends is None:
        legends = np.unique(y)
    col = ["r", "g", "b", "m", "c", "k"]
    ## plot the data points
    for i in np.unique(y):
        plt.scatter(x[y==i,0], x[y==i,1], c=col[i%6], s=25, label=legends[i])
    
    if xlabel:
        plt.xlabel(xlabel,size=12)
    if ylabel:
        plt.ylabel(ylabel,size=12)
    plt.legend(loc=2)
    del_0, del_1 = (max(x[:,0]) - min(x[:,0]))*.1, (max(x[:,1]) - min(x[:,1]))*.1
    plt.axis([
        min(x[:,0]) - del_0, max(x[:,0]) + del_0,
        min(x[:,1]) - del_1, max(x[:,1]) + del_1]
    )

def logistic_model_2Dplot(x, model):
    # import warnings
    # warnings.warn('Does not work for all problems. (Works only for binary label?)')
    
    def plot_y(x_1, model=model):
        ## np.column_stack() combines intercept with coefficents
        for coef in np.column_stack((model.intercept_, model.coef_)):
            ## take b0, b1, b2 for one boundary at a time 
            b_0, b_1, b_2 = coef[:3]
            # given 1, calculate corresponding x2
            # http://python-future.org/compatible_idioms.html
            # Idiomatic Py3, but inefficient on Py2
            yield list(map(lambda x: -(b_0 + b_1*x) / b_2, x_1))
    
    x = np.array(x)
    x_a = [min(x[:,0]), max(x[:,0])]
    col = ["r", "g", "b", "m", "c", "k"]
    for i, x_b in enumerate(plot_y(x_a, model)):
        plt.plot(x_a, x_b, c=col[i])

