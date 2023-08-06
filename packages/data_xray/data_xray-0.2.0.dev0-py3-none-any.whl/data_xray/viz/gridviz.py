from ..modules import *
from .core import Kaleidoscope
from matplotlib.colors import LogNorm

 # this is going to be for one axis only. Tired of figuring out the whole stack.
# # then the figure is going to be built of individual ax_aggregate
def ViewGridSpectra(ds=None, chan=['zf', 'zr'], ax=None, labels={'x':'', 'y':'', 't':''}, scale=['linear', 'linear'],
               pickrandom=False, plotindex=False, alpha=1, color=None, mod=lambda x: x, lim=[None, None],
               name=None, sf=None):
    # attempt to simplify multiaxis plots
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
            ax.plot(ds.bias, mod(dat), c, linewidth=0.3, alpha=alpha, label=nonecheck(name))

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

# # this is going to be for one axis only. Tired of figuring out the whole stack.
# # then the figure is going to be built of individual ax_aggregate
# def ViewGridChannel(xr=None, chan=[['zf', 'zr']], pickrandom=False, plotindex=False,
#            labels=Container(x=None, y=None, title=None), \
#            mod=lambda x: x, saveit=0, ax=None, plotit=1, fig=None, color=None):
#     # pickrandom needs to be a number
#     # clusters needs to be a truth table, say km.labels_==0 for the first cluster
#     import pandas as pd
#
#     plts = []
#     clrs = []
#     xlabel_group = []
#     ylabel_group = []
#     title_group = []
#     save_chan_label = []
#     for cj, cg in enumerate(chan):
#         if pickrandom:
#             xsel = np.random.randint(xr.ds[cg[0]].shape[0], size=pickrandom)
#             ysel = np.random.randint(xr.ds[cg[0]].shape[1], size=pickrandom)
#             _spec = len(xsel)
#         elif plotindex != False:
#             # example would be np.where(xr.ds.cr_km==2)
#             xsel, ysel = plotindex
#             _spec = len(xsel)
#         else:
#             xsel, ysel = [np.ravel(i) for i in np.meshgrid(range(xr.ds.dims['x']), range(xr.ds.dims['y']))]
#
#             # xsel = np.arange(xr.ds.dims['x'])
#             # ysel = np.arange(xr.ds.dims['y'])
#             _spec = xr.ds.dims['x'] * xr.ds.dims['y']
#
#         framedim = (_spec, xr.ds[cg[0]].shape[-1])
#         plot_group = []
#
#         color_group = []
#         if color is None:
#             color = ['blue', 'red']
#         else:
#             color = color
#
#         for im, m in enumerate(cg):
#             if m in xr.ds.keys():
#                 plot_group.append(xr.ds[m].isel_points(x=xsel, y=ysel))
#                 color_group.append(color[im])
#
#         xlabel_group.append('' if labels.x is None else labels.x[cj])
#         ylabel_group.append('' if labels.y is None else labels.y[cj])
#
#         plts.append(plot_group)
#         clrs.append(color_group)
#         # plts.append(pd.DataFrame(dat, index=xr.ds.bias.values,columns=[m for i in range(dat.shape[1])]))
#         # plts[-1].name=m
#
#     if plotit:
#         if ax is None:
#             fig, ax = plt.subplots(1, len(chan), figsize=(4 * len(chan), 4), dpi=150)
#             ax = np.ravel(ax)
#         else:
#             ax = ax
#             fig = fig
#         for cj, cg in enumerate(chan):
#             # (p, c, l) in enumerate(zip(plts, clrs, lbls)):
#             for p, c in zip(plts[cj], clrs[cj]):
#                 dat = np.reshape(p.values, framedim).T
#                 ax[cj].plot(xr.ds.bias, mod(dat), c, linewidth=0.3, alpha=0.6)
#             ax[cj].set_xlabel(xlabel_group[cj], size=18)
#             ax[cj].set_ylabel(ylabel_group[cj], size=18)
#
#         fig.suptitle('' if labels.title is None else labels.title, fontsize=16)
#         plt.legend('')
#         plt.xticks(fontsize=14)
#         plt.yticks(fontsize=14)
#
#         # plt.tight_layout()
#         plt.legend('')
#         if saveit:
#             chans_label = ''
#             for c in chan:
#                 for m in c:
#                     chans_label += '_' + m
#             savename = os.path.dirname(xr.ds.cdf) + '/' + os.path.basename(xr.ds.cdf)[
#                                                             :-3] + chans_label + '.png'
#             fig.savefig(savename, type='png', dpi=200)
#
#     if plotit:
#         return plts, fig
#     else:
#         return plts

def PlotSlices(ds=None, ind=[0], chan='cf', cfig=None, mod=lambda x: x, v=[0,3],
               ticks={'x': None, 'y': None}, labels={'x': '', 'y': '', 'ttl': ''}, sf=None):


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


def ViewHeatmap(ds=None, chan='cr', mod=lambda x: x, v=[0, 3], \
                ticks={'x':None,'y':None}, labels={'x':'', 'y':'', 'ttl':''},
                sf=None, cfig=None):
    from matplotlib.ticker import NullFormatter
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    nmft = NullFormatter()

    def forceAspect(ax, aspect=1):
        im = ax.get_images()
        extent = im[0].get_extent()
        ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)

    if chan in ds.keys():

        # ax1.imshow(mod(ysrc), cmap=plt.cm.RdBu, vmin=vmin, vmax=vmax)

        bd = ds.dims['bias']
        xd = ds.dims['x']
        yd = ds.dims['y']

        _xt = ds.bias.values
        _yt = np.arange(xd * yd)

        _xt = [_xt[0], _xt[2]]
        _yt = [_yt[0], _yt[2]]

        if ticks['x'] is not None:
            _xt = [ticks['x'][0], ticks['x'][-1]]
        if ticks['y'] is not None:
            _yt = [ticks['y'][0], ticks['y'][-1]]

        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        bottom_h = left_h = left + width + 0.02

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom_h, width, 0.2]

        # start with a rectangular Figure
        f2 = plt.figure(1, figsize=(8, 6)) if cfig is None else cfig

        rect_map = [left, bottom, width, height]
        rect_x = [bottom, bottom - 0.22, width * 0.8, 0.2]

        axX = plt.axes(rect_x)
        axMap = plt.axes(rect_map)

        axMap.xaxis.set_major_formatter(nmft)

        ysrc = ds[chan].values.reshape((xd * yd, bd))
        # _map = a2.pcolorfast(_xt, _yt, mod(ysrc[:,:-1]), cmap=plt.cm.RdBu)

        _map = axMap.pcolorfast(mod(ysrc), cmap=plt.cm.RdBu, vmin=min(v), vmax=max(v))

        # divider = make_axes_locatable(axMap)
        # cax = divider.append_axes('right', size='100%', pad=0.05)

        f2.colorbar(_map, orientation='vertical')

        axX.plot(ds.bias, 'b-')
        axX.set_ylabel('bias' if labels['x'] == '' else labels['x'])

        axMap.set_ylabel(labels['y'], size=11)

        axMap.set_title(chan if labels['ttl'] == '' else labels['ttl'])
        forceAspect(axMap, aspect=1)
        if sf is not None:
            f2.savefig(sf + '.png', savedpi=200)
        plt.autoscale(enable=True, axis=axX, tight=True)
        plt.axis('tight')
        #plt.tight_layout()
        #plt.show()


def HistogramDS(x, y, ax=None, label=['', '', ''], cbar=True):

        from matplotlib.colors import LogNorm

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


