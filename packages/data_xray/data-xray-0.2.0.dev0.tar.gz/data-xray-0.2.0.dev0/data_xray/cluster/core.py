"""
Created on Wed Jan 11 10:50:02 2017

@author: 5nm
"""

from ..modules import *
from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def KmeansIterative(X=None, keach=3, iters=2):
    from sklearn import metrics
    from sklearn.metrics import pairwise_distances
    #iters = 3
    #keach = 3
    for j in range(iters):
        km = KMeans(n_clusters=keach, random_state=1).fit(X)
        labels = km.labels_
        pops = np.asarray([[m,len(np.where(km.labels_==m)[0])] for m in range(keach)])
        subind = np.where(km.labels_ == pops[pops[:,1].argsort()][-1][0])[0]
        X = X[subind]
    print(len(X))
    return X


def HirearchicClustering(dat=None, k=None, plotit=0):

    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.cluster.hierarchy import fcluster

    xy,z = np.product(dat.shape[:-1]),dat.shape[-1]
    dat2 = dat.reshape((xy,z))
    Z = linkage(dat2, 'ward')
    cmask = fcluster(Z, k, criterion='maxclust')

    #xsel,ysel= np.where(cmask.reshape(20,20)==1)
    cmask_square = cmask.reshape(dat.shape[:-1])-1

    if plotit:
        return dendrogram(Z, leaf_rotation=90, leaf_font_size=8, truncate_mode='lastp', p=k), cmask_square
    else:
        return cmask_square

def ScpDendrogram(X=None, lastp=10):
    #adopted from Joern Hees blog

    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist

    def fancy_dendrogram(*args, **kwargs):
        max_d = kwargs.pop('max_d', None)
        if max_d and 'color_threshold' not in kwargs:
            kwargs['color_threshold'] = max_d
        annotate_above = kwargs.pop('annotate_above', 0)

        ddata = dendrogram(*args, **kwargs)

        if not kwargs.get('no_plot', False):
            plt.title('Hierarchical Clustering Dendrogram (truncated)')
            plt.xlabel('sample index or (cluster size)')
            plt.ylabel('distance')
            for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
                x = 0.5 * sum(i[1:3])
                y = d[1]
                if y > annotate_above:
                    plt.plot(x, y, 'o', c=c)
                    plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                                 textcoords='offset points',
                                 va='top', ha='center')
            if max_d:
                plt.axhline(y=max_d, c='k')
        return ddata


    Z = linkage(X, 'ward')
    c, coph_dists = cophenet(Z, pdist(X))

    # calculate full dendrogram
    fancy_dendrogram(
        Z,
        truncate_mode='lastp',
        p=12,
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
        annotate_above=10,  # useful in small plots so annotations don't overlap
    )
    plt.show()

def PcaCore(pca_dat=None, display=0, dim=2):

    pca = RandomizedPCA(whiten=False).fit(pca_dat)
    if display:
        fig2 = plt.figure()
        #fig2.suptitle('PCA components', size=11)
        G = gridspec.GridSpec(3, 3)
        for j in range(9):
            ax = fig2.add_subplot(G[j])
            ax.plot(pca.components_[j])
            ax.set_title('comp #' + str(j), size=10)
        _f3, _a3 = plt.subplots(1,1)
        _a3.semilogy(pca.explained_variance_ratio_)
        _a3.set_title('scree plot')
        #fig2.tight_layout()
    load_maps = pca.transform(pca_dat)

    if display and dim > 1:
        fig3 = plt.figure()
        #fig3.suptitle('loading maps', size=11)
        G = gridspec.GridSpec(3, 3)
        for j in range(9):
            ax = fig3.add_subplot(G[j])

            side = int(np.sqrt(load_maps.shape[0]))
            ax.imshow(load_maps[:,j].reshape(side,side), cmap=plt.cm.RdBu)
            ax.set_title('map #' + str(j), size=10)
        #fig3.tight_layout()
    plt.show()

    return {'load_maps':load_maps, 'eigenims':pca.components_, 'weight':pca.explained_variance_ratio_}

def KmeansCore(dat=None, nclust=None):

    km = KMeans(nclust)
    km.fit(dat)
    # clustind = km.predict(dat)
    return km  # clustind

def PcaKmeans(dat=None, comps=None, nclust=3, pf=lambda x, i: x, ax=0):
    # dat is 2D numpy array

    if comps is None:
        pca = PCA(n_components=comps)
    else:

        pca = PCA()

    pca.fit(dat)
    Y = pca.fit_transform(dat)
    km = KMeans(n_clusters=nclust, random_state=0).fit(Y[:, 0:nclust])

    if type(ax) == np.ndarray :
        clrs = ['b.-', 'g.-', 'r.-']

        ax[0].plot(np.arange(20), 100*np.cumsum(pca.explained_variance_ratio_[:20]), 'b.-')
        ax[0].set_title('PCA variance')
        ax[0].set_ylabel('%')
        ax[0].set_xlabel('PCA component')

        ax[1].plot(Y[km.labels_ == 0, 0], Y[km.labels_ == 0, 1], 'r.')
        ax[1].plot(Y[km.labels_ == 1, 0], Y[km.labels_ == 1, 1], 'b.')
        ax[1].plot(Y[km.labels_ == 2, 0], Y[km.labels_ == 2, 1], 'g.')
        ax[1].set_xlabel('PCA1 score')
        ax[1].set_ylabel('PCA2 score')

        plt.legend()
        #plt.tight_layout()

        #plt.show()
    return km, Y

def PcaDbscan(dat=None, comps=None, nclust=3, plotit=0, pf=lambda x, i: x):
    # dat is 2D numpy array

    if comps is None:
        pca = PCA(n_components=comps)
    else:
        pca = PCA()

    pca.fit(dat)
    Y = pca.fit_transform(dat)
    km = KMeans(n_clusters=nclust, random_state=0).fit(Y[:, 0:nclust])

    if plotit:
        fig_3, ax_3 = plt.subplots(1, 2)
        clrs = ['b.-', 'g.-', 'r.-']

        ax_3[0].semilogy(np.arange(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_, 'b.-')
        ax_3[1].plot(Y[km.labels_ == 0, 0], Y[km.labels_ == 0, 1], 'r.')
        ax_3[1].plot(Y[km.labels_ == 1, 0], Y[km.labels_ == 1, 1], 'b.')
        ax_3[1].plot(Y[km.labels_ == 2, 0], Y[km.labels_ == 2, 1], 'g.')

        fig_4, ax_4 = plt.subplots(1, 1)
        for i in range(nclust):
            for pl_i in np.random.choice(np.where(km.labels_ == i)[0],5):
                ax_4.plot(pf(dat[pl_i], i))

        plt.show()
    return km

def PcaAffinity(dat=None, comps=None, nclust=3, plotit=0, pf=lambda x, i: x):
    # dat is 2D numpy array
    from sklearn.cluster import AffinityPropagation

    if comps is None:
        pca = PCA(n_components=comps)
    else:
        pca = PCA()

    pca.fit(dat)
    Y = pca.fit_transform(dat)
    # km = KMeans(n_clusters=nclust, random_state=0).fit(Y[:,0:nclust])

    af = AffinityPropagation(preference=-50).fit(Y[:, 0:nclust])
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)

    if plotit:
        fig_3, ax_3 = plt.subplots(1, 2)
        clrs = ['b.-', 'g.-', 'r.-']

        ax_3[0].semilogy(np.arange(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_, 'b.-')
        ax_3[1].plot(Y[af.labels_ == 0, 0], Y[km.labels_ == 0, 1], 'r.')
        ax_3[1].plot(Y[af.labels_ == 1, 0], Y[km.labels_ == 1, 1], 'b.')
        ax_3[1].plot(Y[af.labels_ == 2, 0], Y[km.labels_ == 2, 1], 'g.')

        plt.show()
    return af


def PcaDenoise(pca_dat=None, display=0, keep_components=3, savgolparms=None):
    import scipy.signal as scp
    pca = RandomizedPCA()
    load_maps = pca.fit_transform(pca_dat)
    if savgolparms is not None:
        for j in range(pca.components_.shape[0]):
              pca.components_[j] = scp.savgol_filter(pca.components_[j], window_length=savgolparms[0], polyorder=savgolparms[1])
    #load_maps = pca.transform(pca_dat)
    load_maps[:,keep_components:] = 0
    return pca.inverse_transform(load_maps)
