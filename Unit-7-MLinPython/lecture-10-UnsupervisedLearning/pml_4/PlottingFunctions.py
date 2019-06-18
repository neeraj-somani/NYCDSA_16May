from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from sklearn.metrics import silhouette_samples
import numpy as np

def rotate(array):
    data = [
        [1, 0, 0],
        [0, np.sqrt(3) / 2, -np.sqrt(1) / 2],
        [0, np.sqrt(1) / 2, np.sqrt(3) / 2]]
    rot = np.matrix(data=data).T
    return np.array(np.matrix(array) * rot)


def plot_vec(ax, array, length, color='blue', alpha=1):
    kwargs = dict(
        color=color,  # color of the curve
        linewidth=1.4,  # thickness of the line
        # linestyle='--',  # available styles - -- -. :
        alpha=alpha,
    )
    ax.plot(*zip(-array[0] * length, array[0] * length), **kwargs)


def plot_plane(ax, normal, color='blue', alpha=0.2, x_min=-1.5, x_max=2.5, y_min=-2.5, y_max=1.5):
    x_min_rng = list(range(int(np.floor(x_min) + 1), 0))
    x_max_rng = list(range(int(np.floor(x_max))))
    y_min_rng = list(range(int(np.floor(y_min) + 1), 0))
    y_max_rng = list(range(int(np.floor(y_max))))
    surf_x, surf_y = np.meshgrid(
        [x_min] + x_min_rng + x_max_rng + [x_max],
        [y_min]+ y_min_rng + y_max_rng + [y_max])
    surf_z = (-normal[0, 0]*surf_x - normal[0, 1]*surf_y - 0.5)* 1. / normal[0, 2]
    ax.plot_surface(surf_x, surf_y, surf_z, color=color, alpha=0.1)
    
    
def project2vec(ax, data, vec, id_=0, color='green', along=False):
    pp = data[[id_]]
    proj = (np.sum(vec*pp)*vec)
    ax.scatter( *( proj.ravel() ), color=color, s=16)
    kwargs = dict(
        color=color,  # colour of the curve
        linewidth=1.4,  # thickness of the line
        # linestyle='--',  # available styles - -- -. :
        alpha=0.5,
    )
    ax.plot(*(zip(pp[0], proj[0])), **kwargs)
    if along:
        along_kwargs = dict(
            color='Dark' + color,  # colour of the curve
            linewidth=1.4,  # thickness of the line
            # linestyle='--',  # available styles - -- -. :
            alpha=1,
        )
        ax.plot(*(zip(np.array([0,0,0]), proj[0])), **along_kwargs)
    return np.sum(vec*pp)

def project2plane(ax, data, normal, id_=0, color='green', shoot=False):
    pp = data[[id_]]
    proj = pp - np.sum((pp * normal)) * normal
    ax.scatter(*proj.ravel(), color=color, s=16)
    if shoot:
        kwargs = dict(
            color=color,  # colour of the curve
            linewidth=1.4,  # thickness of the line
            # linestyle = '--',  # available styles - -- -. :
            alpha=0.5,
        )
        ax.plot(*(zip(pp[0], proj[0])), **kwargs)
    return pp - np.sum(normal * pp) * normal    
    
def plot_origin(ax):
    ax.scatter(0, 0, 0, marker='o', s=26, color='black', alpha=1)
    
def plotModel(model, x, y, label):
    '''
    model: a fitted model
    x, y: two variables, should arrays
    label: true label
    '''
    margin = 0.5
    x_min = x.min() - margin
    x_max = x.max() + margin
    y_min = y.min() - margin
    y_max = y.max() + margin
    import  matplotlib.pyplot as plt
    from matplotlib import colors
    col_dict = {
        'red': [(0, 1, 1), (1, 0.7, 0.7)],
        'green': [(0, 1, 0.5), (1, 0.7, 0.7)],
        'blue': [(0, 1, 0.5), (1, 1, 1)]
    }
    cmap = colors.LinearSegmentedColormap('red_blue_classes', col_dict)
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
    #plt.contour(xx, yy, Z, [1], linewidths=1., colors='k')
    ## plot scatters ans true labels
    plt.scatter(x, y, c=label, edgecolors='k')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    ## if it's a SVM model
    if hasattr(model, 'support_'):
        # if it's a SVC, plot the support vectors
        index = model.support_
        plt.scatter(x[index], y[index], c=label[index], s=150, alpha=0.5, edgecolors='k')

def visualize(data, n_sample=25):
    fig = plt.figure(figsize=(10, 10))
    num = int(n_sample**0.5)
    gs = gridspec.GridSpec(num, num)
    fig.subplots_adjust(wspace=0.01, hspace=0.02)
    l = len(data.iloc[1, :])
    ll = int(l**0.5)
    for i in range(num):
        for j in range(num):
            temp = np.array(data.loc[(num*i + j), :]).reshape(ll, ll)
            ax = plt.subplot(gs[i, j])
            ax.imshow(temp, cmap=plt.cm.gray, interpolation='nearest')
            ax.axis('off')
    plt.show()


def plot_silhouette(kmeans, x):
    y_km = kmeans.fit_predict(x)
    cluster_labels = np.unique(y_km)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = silhouette_samples(x, y_km, metric='euclidean')
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    for i, c in enumerate(cluster_labels):
        # Aggregate the silhouette scores for samples belonging to
        # cluster c, and sort them
        c_silhouette_vals = silhouette_vals[y_km == c]
        c_silhouette_vals.sort()

        size_cluster_c = len(c_silhouette_vals)
        y_ax_upper += size_cluster_c
        color = cm.jet(i*1.0/n_clusters)
        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0, color=color)

        # Compute the new y_ax_lower for next plot
        yticks.append((y_ax_lower + y_ax_upper) / 2)
        y_ax_lower += size_cluster_c

    # The vertical line for average silhouette score of all the values
    silhouette_avg = np.mean(silhouette_vals)
    plt.axvline(silhouette_avg, color='red', linestyle='--')

    plt.yticks(yticks, cluster_labels + 1)
    plt.title('Silhouette Analysis')
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')
    plt.show()

def plot_inertia(km, X, n_cluster_range):
    inertias = []
    for i in n_cluster_range:
        km.set_params(n_clusters=i)
        km.fit(X)
        inertias.append(km.inertia_)
    plt.plot(n_cluster_range, inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()
