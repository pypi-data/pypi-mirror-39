from ..modules import *
from ..viz.core import Kaleidoscope


def GridViewSpectra(ds=None, chan=['zf', 'zr'], ax=None, labels={'x':'', 'y':'', 't':''}, scale=['linear', 'linear'],
               pickrandom=False, plotindex=False, alpha=1, color=None, mod=lambda x: x, lim=[None, None],
               name=None, sf=None):
    """
    open spectra in the grid
    :param ds:
    :param chan:
    :param ax:
    :param labels:
    :param scale:
    :param pickrandom:
    :param plotindex:
    :param alpha:
    :param color:
    :param mod:
    :param lim:
    :param name:
    :param sf:
    :return:
    """
    #
    # options for scale:

    if pickrandom:
        if chan[0] in ds.keys():
            xsel = np.random.randint(ds[chan[0]].shape[0], size=pickrandom)
            ysel = np.random.randint(ds[chan[0]].shape[1], size=pickrandom)
            _spec = len(xsel)
        else:
            print('specify correct channel')
            return

    elif plotindex != False:
        # example would be np.where(xr.ds.cr_km==2)
        xsel, ysel = plotindex
        _spec = len(xsel)

    else:
        xsel, ysel = [np.ravel(i) for i in np.meshgrid(range(ds.dims['x']), range(ds.dims['y']))]
        _spec = ds.dims['x'] * ds.dims['y']

    framedim = (_spec, ds[chan[0]].shape[-1])

    for c, m in zip(Kaleidoscope(), chan):
        if m in ds.keys():
            ds_dat = ds[m].isel_points(x=xsel, y=ysel)
            dat = ds_dat.values.reshape(framedim).T
            # dat = np.reshape(p.values, framedim).T
            c = c if color is None else color
            ax.plot(ds.bias, mod(dat), c, linewidth=0.8, alpha=alpha, label=nonecheck(name))

    ax.set_xlabel(labelcheck(labels,'x'))
    ax.set_ylabel(labelcheck(labels,'y'))
    ax.set_title(labelcheck(labels,'t'))

    ax.set_xscale(scale[0])  # options: linear, log, symlog, logit
    ax.set_yscale(scale[1])  # options: linear, log, symlog, logit

    if lim[0] is not None:
        ax.set_xlim(lim[0])
    if lim[1] is not None:
        ax.set_ylim(lim[1])

    return dat



def GridPlotSlices(ds=None, ind=[0], chan='cf', cfig=None, mod=lambda x: x, v=[0,3],
               ticks={'x': None, 'y': None}, labels={'x': '', 'y': '', 'ttl': ''}, sf=None):
    """
    Plot grid slices
    :param ds:
    :param ind:
    :param chan:
    :param cfig:
    :param mod:
    :param v:
    :param ticks:
    :param labels:
    :param sf:
    :return:
    """

        # side = int(np.sqrt(data.shape[0]))
        # if ind is None:
        #     slind = [int(i) for i in np.linspace(0, data.shape[1] - 1, 9)]
        # else:
        #     slind = ind

    _fig3 = plt.figure(figsize=(10,10)) if cfig is None else cfig
    dat = ds[chan]
    # fig3.suptitle('loading maps', size=11)
    G = gridspec.GridSpec(int(np.ceil(len(ind) / 3)), 3)
    for i, j in enumerate(ind):
        ax = _fig3.add_subplot(G[i])
        xname = list(ds.coords)[0]
        xval = int(ds[xname][j].values*10)/10
        ax.imshow(dat[:,:,j], cmap=plt.cm.RdBu)
        ax.set_title(xname + '  ' + str(xval), size=10)
    plt.show()

def GridViewHeatmap(ds=None, chan='cr', mod=lambda x: x, v=[0, 3], ax=None):
    """
    Plot grid heatmap

    :param ds:
    :param chan:
    :param mod:
    :param v:
    :param ax:
    :return:
    """
    def forceAspect(ax, aspect=1):
        im = ax.get_images()
        extent = im[0].get_extent()
        ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)

    if chan in ds.keys():

        # ax1.imshow(mod(ysrc), cmap=plt.cm.RdBu, vmin=vmin, vmax=vmax)

        bd = ds.dims['bias']
        xd = ds.dims['x']
        yd = ds.dims['y']


        data = mod(ds[chan].values.reshape((xd*yd, bd)))
        data = pd.DataFrame(data, columns=[np.round(np.float(j), 1) for j in list(ds.bias.values)])

        sns.heatmap(data=data, ax=ax, vmin=v[0],vmax=v[1], square=False, xticklabels=int(bd/10), yticklabels=int(xd*yd/10))
        plt.tight_layout()


def GridHistogram(x, y, ax=None, label=['', '', ''], cbar=True):

        """
        Histogram of 2D data. Deptracted
        :param x:
        :param y:
        :param ax:
        :param label:
        :param cbar:
        :return:
        """
        # y is the 2D array - can be from ds.cf.values for example
        # x is the 1D bias vector

        xarr = np.ones(y.shape) * x

        a2 = pd.DataFrame(y.reshape((y.shape[0] * y.shape[1])), columns=['y'])
        a2['x'] = xarr.reshape((xarr.shape[0] * xarr.shape[1]))

        if ax is None:
            _fig, ax = plt.subplots(1, 1)

        a = ax.hist2d(a2.x, a2.y, bins=(120, 40), normed=1, cmap=plt.cm.jet) #norm=LogNorm()

        ax.set_xlabel(label[0])
        ax.set_ylabel(label[1])
        ax.set_title(label[2])
        if cbar:
            plt.colorbar(a[3])


