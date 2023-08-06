"""
Created on Wed Jan 11 10:50:02 2017

@author: 5nm
"""
from ..general_utilities import *
from ..file_io import *
from ..cluster import *
from ..modules import *


"""these are experimental methods that should not be used for now"""

def ClusterCenter(xr=None, chan='cr'):
    cent_dict = {}
    if chan + '_km' in xr.ds:
        cls = np.arange(np.max(xr.ds[chan + '_km']) + 1)
        for j in cls:
            f, a = plt.subplots(1, 1)
            xs, ys = np.where(xr.ds.cr_km == j)
            dat = xr.ds.cr.isel_points(x=xs, y=ys)
            xm = np.abs(xr.ds.bias)
            ym = dat.mean(axis=0)
            yerr = dat.std(axis=0)
            cent_dict[j] = [ym, yerr]
            a.errorbar(np.abs(xm), ym, yerr)
            a.set_xscale("log", nonposx='clip')
            a.set_yscale("log", nonposy='clip')
            # a.set_xlim([6e-1, np.max(xm)])
            a.set_xlabel('bias, V')
            a.set_ylabel('current, nA')
            a.set_title('cluster #' + str(j))
    plt.show()
    return cent_dict

#just some 


def GroupBySimilarity(xr=None, xrdat=None, nclust=3, plotit=1, clusterorder=None):
    # let's revise this that data can be shaped externally

    def get_dimensions(xrobj):

        dim_names = []
        for k in list(xrobj.dims):
            if k not in list(xrobj.coords.keys()):
                dim_names.append(k)

        dim_sizes = [xrobj[i].shape[0] for i in dim_names]
        size_arr = [np.size(xrobj) / xrobj.bias.shape[0], xrobj.bias.shape[0]]
        return dim_names, dim_sizes, size_arr

    chan = xrdat.name
    clust_dim_names, clust_dim_sizes, clust_size_arr = get_dimensions(xrdat)
    src_dim_names, src_dim_sizes, src_size_arr = get_dimensions(xr.ds[chan])

    # clust_dim_sizes = [xrdat[i].shape[0] for i in dim_names]
    # clust_size_arr = [np.size(xrdat)/xrdat.bias.shape[0],xrdat.bias.shape[0]]
    #
    # src_dim_sizes = [xr.ds[chan].shape[0] for i in dim_names]
    # src_size_arr = [xr.ds[chan].shape[0] for i in dim_names]
    #

    yclust = xrdat.values.reshape(tuple(int(s) for s in clust_size_arr))
    ysrc = xr.ds[chan].values.reshape(tuple(int(s) for s in src_size_arr))

    km = pca_kmeans(ysrc, nclust=nclust, plotit=0)

    kmarr = xr.DataArray(np.reshape(km.labels_, tuple(clust_dim_sizes)), dims=clust_dim_names)

    """"""

    mean_dict = []
    err_dict = []

    for j in np.arange(nclust):
        dat = ysrc[np.where(km.labels_ == j)]

        # print(np.where(kmarr==j))
        # play with np.flatten
        # xs, ys = np.where(kmarr == j)
        # dat = xr.ds[chan].isel_points(x=xs, y=ys)
        mean_dict.append(np.abs(dat.mean(axis=0)))
        err_dict.append(dat.std(axis=0))

    if clusterorder is None:
        cluster_order = np.flipud(np.argsort(np.asarray(mean_dict).mean(axis=1)))
    else:
        cluster_order = clusterorder
    # print(cluster_order)
    # print(km.labels_)
    kmsort = copy.copy(km.labels_)
    for j in np.arange(np.max(km.labels_) + 1):
        kmsort[np.where(km.labels_ == j)] = cluster_order[j]

    # kmarr = xr.DataArray(np.reshape(kmsort, (x, y)), dims=['x', 'y'])
    kmarr = xr.DataArray(np.reshape(kmsort, tuple(clust_dim_sizes)), dims=clust_dim_names)

    xr.ds.__setitem__(chan + '_km', kmarr)

    mean_dict = np.asarray(mean_dict)[np.argsort(np.asarray(mean_dict).mean(axis=1))]
    err_dict = np.asarray(err_dict)[np.argsort(np.asarray(mean_dict).mean(axis=1))]

    cm = xr.DataArray(data=mean_dict.T, coords={'bias': xr.ds.bias.values, chan + '_clust': np.arange(nclust)},
                      dims=['bias', chan + '_clust'],
                      name=chan + '_clust_mean')
    cmerr = xr.DataArray(data=err_dict.T, coords={'bias': xr.ds.bias.values, chan + '_clust': np.arange(nclust)},
                         dims=['bias', chan + '_clust'], name=chan + '_clust_err')

    xr.ds.__setitem__(chan + '_km' + '_mean', cm)
    xr.ds.__setitem__(chan + '_km' + '_err', cmerr)

    if plotit:
        # scree plot
        for i in range(nclust):
            k_ind = np.where(km.labels_ == i)[0]
            np_glance_random(data=xr.ds[xrdat.name], xvec=xr.ds.bias.values, labels=['V', 'z', str(i)])









def gridKmeans(gf, chan, nclust=5):
    from sklearn.cluster import KMeans
    dat = gf.data[chan]
    dat2 = np.reshape(dat, (np.size(dat, 0) * np.size(dat, 1), np.size(dat, 2)))
    km = KMeans(n_clusters=nclust)
    km.fit(dat2)
    clustind = km.predict(dat2)
    meanvec = list()
    for j in range(nclust):
        clustrep = list(np.where(clustind == j)[0])
        meanvec.append(np.mean(dat2[clustrep, :], 0))
    return clustind, meanvec


def _earth_iv(self, curchan='Current', plotall=0, plotfit=1):
    # self should be gridfile() object
    def earth_slope(xvec, yvec, plot=0):
        m = Earth()

        sigind = np.where(np.log10(np.abs(yvec)) > p['thresh'] * self.allnoise)
        vpos = np.intersect1d(sigind, np.where(xvec > 0))
        vneg = np.intersect1d(sigind, np.where(xvec < 0))

        posx, posc, negx, negc = np.abs(xvec[vpos]), np.abs(yvec[vpos]), np.abs(xvec[vneg]), np.abs(yvec[vneg])
        tl = np.zeros(xvec.shape)
        l1, l2 = [], []
        rsq = []

        if len(posc) > 4:  # a meaningful length of iv curve
            m.fit(np.log(posx), np.log(posc))
            l1 = m.predict(np.log(posx))
            tl[vpos] = np.gradient(l1) / np.gradient(np.log(posx))
            rsq.append(m.rsq_)
            if p['plotfit']:
                p['plotax'].plot(np.log(posx), incrj * p['incr'] + l1, linewidth=0.4, color='red')
                p['plotax'].scatter(np.log(posx), incrj * p['incr'] + np.log(posc), s=10, facecolors='none',
                                    edgecolors='blue')

        if len(negc) > 4:
            m.fit(np.log(negx), np.log(negc))
            l2 = m.predict(np.log(negx))
            tl[vneg] = np.gradient(l2) / np.gradient(np.log(negx))
            rsq.append(m.rsq_)
            if p['plotfit']:
                p['plotax'].plot(np.log(negx), incrj * p['incr'] + l2, linewidth=0.4, color='red')
                p['plotax'].scatter(np.log(negx), incrj * p['incr'] + np.log(negc), s=10, facecolors='none',
                                    edgecolors='blue')

        return tl, np.mean(rsq)

        tl = np.zeros(xvec.shape)
        m.fit(xvec, yvec)
        yh = m.predict(xvec)
        dyh = np.abs(np.gradient(yh) / np.gradient(xvec))
        datind = np.where(dyh > np.min(dyh) * 1.1)
        xvec = xvec[dyh]
        yvec = yvec[dyh]

        # np.where(~np.isnan(np.log(yvec)) == True)[0][10:]
        posx, posc, negx, negc = xvec[xvec > 0], yvec[xvec > 0], np.abs(xvec[xvec < 0]), yvec[xvec < 0]
        if plot:
            fig5 = plt.gcf()
            ax5 = fig5.add_subplot(111)

        if len(posx):
            m.fit(np.log(posx), np.log(posc))
            l1 = m.predict(np.log(posx))
            tl[np.where(xvec > 0)] = np.gradient(l1) / np.gradient(np.log(posx))
            if plot:
                ax5.plot(np.log(posx), l1, 'g--')
                ax5.plot(np.log(posx), np.log(posc), 'b.')

        if len(negx):
            m.fit(np.log(negx), np.log(negc))
            l2 = m.predict(np.log(negx))
            tl[np.where(xvec < 0)] = np.gradient(l2) / np.gradient(np.log(negx))
            if plot:
                ax5.plot(np.log(negx), l2, 'g--')
                ax5.plot(np.log(negx), np.log(negc), 'b.')

        return tl


# def _iv_noise_sub(self, noiserange=[]):
#     curclues = ['nput 8', 'urrent']
#     nse = []
#     for si in tqdm(self.data):
#         xv = self.inlist(list(si.keys()), 'ias')[0]
#         yv = self.inlist(list(si.keys()), 'nput 8') or self.inlist(list(si.keys()), 'urrent')
#         for j in yv:
#             si[j], ns = sub_iv_noise(y=si[j], x=si[xv], rng=noiserange)
#             #         self.data[si][c],
#             nse.append(ns)
#     #
#     self.allnoise = np.log10(np.mean(np.asarray(nse))) + 0.6
#
