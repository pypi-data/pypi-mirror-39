from ..modules import *
from ..general_utilities import *


def PlotClustered(dat,labels, xvec=None, cfig=None):


    if xvec is None:
        xvec = np.arange(dat.shape[1])

    n_clusters = np.max(labels)+1
    _fig = plt.figure() if cfig is None else cfig


    G = gridspec.GridSpec(int(np.ceil(n_clusters / 3)), 3)
    for i, j in enumerate(range(n_clusters)):
        ax = _fig.add_subplot(G[i])
        plotlabels = np.random.choice(np.where(labels==j)[0],5)
        for p in plotlabels:
            ax.plot(xvec, dat[p])
        ax.set_title('cluster'+str(j+1))
    plt.tight_layout()
    plt.show()


# def PlotClustered(dat,labels, xvec=None, fig_=None):
#
#
#     if xvec is None:
#         xvec = np.arange(dat.shape[1])
#
#     n_clusters = np.max(labels)
#     if fig_ is None:
#         fig_ = plt.figure(figsize=(10, 10))
#
#     fig_ = plt.figure()
#     G = gridspec.GridSpec(int(np.ceil(n_clusters / 3)), 3)
#     for i, j in enumerate(range(n_clusters)):
#         ax = fig_.add_subplot(G[i])
#         plotlabels = np.random.choice(np.where(labels==j)[0],5)
#         for p in plotlabels:
#             ax.plot(xvec, dat[p, 1])
#         ax.set_title('cluster',j)
#
#     plt.show()