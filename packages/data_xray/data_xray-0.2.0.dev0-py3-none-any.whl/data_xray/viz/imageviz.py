from ..modules import *

#####SXM IMAGE FILES


import mpld3
##this is the new version working with xarray dataset
from plotly import tools
from tqdm import tqdm

#list of functions for image analysis
def AxesColorLimits(arr2d):
    return [np.mean(arr2d) - 3*np.std(arr2d/np.max(arr2d)),np.mean(arr2d) + 3*np.std(arr2d/np.max(arr2d))]


#high pass
def HighLowPass2d(im, type='low', pxwidth=3):
    #this works on numpy arrays and should also work on xarrayed images
    from scipy import ndimage
    lowpass = ndimage.gaussian_filter(im, pxwidth)

    if type == 'high':
        return im - lowpass
    else:
        highp = im-lowpass
        return im - highp


def SubtractLine(im2, deg=2):

    im2, _ = spiepy.flatten_poly_xy(im2/1e-9, deg=deg)
    return im2

    # bglist = list()
    # x = np.arange(im2.shape[0])
    # for j in range(im2.shape[0]):
    #     plf = np.polyfit(x, im2[j], 2)
    #     bglist.append(list(np.polyval(plf, x)))
    # im2 = im2 - np.asarray(bglist)
    # return im2

def PlotImage(_Scan, chan, ax, backw=0, cm='magma',zoom=1, high_pass=None):
    #clean up missing vavlues
    from matplotlib.colors import LogNorm
    fb = 'backward' if backw else 'forward'
    im2 = _Scan.signals[chan][fb]
    if np.any(np.isnan(im2)):
        cleanrange = np.setxor1d(np.arange(np.size(im2, 0)), np.unique(np.where(np.isnan(im2))[0]))
        im2 = im2[cleanrange]

    original_size = im2.shape

    if chan.lower()=='z':
        try:
            if high_pass is not None:
                im2 = HighLowPass2d(im2, type='high', pxwidth=high_pass)
                crop = 2*high_pass
                im2 = im2[crop:-crop,crop:-crop] #crop the edges
            else:
                im2 = SubtractLine(im2)
        except:
            print('problems subtracting background in ' + _Scan.fname)
            im2 = im2
    scale = _Scan.header['scan_range']/_Scan.header['scan_pixels']
    stat = [np.mean(im2), np.mean([np.std(im2 / np.max(im2)), np.std(im2 / np.min(im2))])]
    color_range = [stat[0] - 3 * stat[1], stat[0] + 3 * stat[1]]
    #im2 = (im2 - np.min(im2))/(np.max(im2)-np.min(im2))
    im2 = (im2 - np.min(im2))# / (np.max(im2) - np.min(im2))
    im2 = im2/np.max(im2)

    if zoom != 1:
         im2 = ndimage.zoom(im2,zoom=zoom,order=3)

    if backw:
        ax.imshow(np.fliplr(im2), cmap=cm, norm=LogNorm(vmin=0.05, vmax=1.1))
    else:
        ax.imshow(im2, cmap=cm, norm=LogNorm(vmin=0.05, vmax=1.1))


    scale_unit = np.min([i / j for i, j in zip(_Scan.header['scan_range'], original_size)])

    sbar = ScaleBar(scale_unit, location='upper right', font_properties={'size': 8})

    fp = sbar.get_font_properties()
    fp.set_size(8)
    #ax.axes([0.08, 0.08, 0.94 - 0.08, 0.94 - 0.08])  # [left, bottom, width, height]
    #ax.axis('scaled')
    ax.add_artist(sbar)
    ax.set_title(chan+' '+ fb, fontsize=8)
    # ax.set_title(phdf+j)
    # ax.set_title('$'+j+'$')
    ax.set_axis_off()
    return im2


def PlotScan(_Scan, chans='all', scanid=0, scandir=2, zoom=1, high_pass=None):
    #scandir 2 for forward-backward, 1 for forward only
   # import plotly.tools as tls
#     matplotlib.rcParams['font.size'] = 8
#     matplotlib.rcParams['font.family'] = ['sans-serif']
#     # chans two values 'fil' or 'all'. All - just plot all channels
#     # ppl - means use pyplot interface
#     # 'fil' - plot ony those with meaningful std (aka data). Std threshdol 1e-2
#     # the plotter! plots all channels contained in the sxm-dict structure
#
#
    plotted = []
    fn = _Scan.fname
    #plotdict = dict()
    # allow plotting of specific channels
    if chans == 'all':
        chans = _Scan.signals.keys()
    elif chans == 'fil':
        chans = []
        for c in _Scan.signals.keys():
            im2 = _Scan.signals[c]['forward']
            im2 = im2/(np.max(im2)-np.min(im2))
            if np.std(im2) > 0.2:
                chans.append(c)

    if len(chans) == 0:
        return #no valid data found

    fig3 = plt.figure(figsize=(3*(1+len(chans)),8))
    gs = gridspec.GridSpec(scandir, len(chans))


        #, sharex='col', sharey=True,
        #                     gridspec_kw={'height_ratios': [2, 1]},
        #                     figsize=(4, 7))
    #if len(chans) == 1:
    #    ax3 = ax3[:,np.newaxis]
    for j, ch in enumerate(chans):

        #ax3[0,0] = f3.add_subplot(gs[0, j])
        #axr = f3.add_subplot(gs[1, j])

        for scand in np.arange(scandir):
            ax3 = plt.subplot(gs[scand,j])
            p2 = PlotImage(_Scan, chan=ch, ax=ax3, backw=scand, zoom=zoom, high_pass=high_pass)
            plotted.append(p2)
        #PlotImage(_Scan, chan=ch, ax=ax3[0, j], backw=1)
    #plt.tight_layout(pad = 0.04, w_pad = 0.05, h_pad = 0.05)
    plt.subplots_adjust(left=0.11, bottom=0.01, right=0.9, top=0.93, wspace=0.54, hspace=0.1)
    plt.tight_layout(pad=0)
    #fig3.set_tight_layout({'rect': [0, 0.0, 1, 0.92], 'pad': 0.05, 'h_pad': 0.05})
    #plt.setp(axes, title='Test')
    fig3.suptitle("Scan #"+ str(scanid) + ':' + fn, size=12, y=1.02)
    #
    # f3, a3 = plt.subplots(2,len(chans))
    # gs = gridspec.GridSpec(2, len(chans))
    # #     else:
    # #         gs = gridspec.GridSpec(1, len(plotdict))
    # for j, ch in enumerate(chans):
    #     axf = f3.add_subplot(gs[0, j])
    #     axr = f3.add_subplot(gs[1, j])
    #
    #     #PlotImage(_Scan, chan=ch, ax=axf, forw=1)
    #     #PlotImage(_Scan, chan=ch, ax=axr, forw=0)
    #     axf.set_axis_off()
    #     axr.set_axis_off()
    #     axf.set_frame_on('off')
    #     plt.axis('off')
    #
    # gs.update(left=0.05, right=0.98, hspace=0.2)
    # plt.axis('off')
    #plt.show()
    def onresize(event):
        plt.tight_layout()

    cid = fig3.canvas.mpl_connect('resize_event', onresize)

    return fig3, plotted


def PlotScanLy(_Scan, chans='all', scanid=0):
    import plotly.tools as tls
#     matplotlib.rcParams['font.size'] = 8
#     matplotlib.rcParams['font.family'] = ['sans-serif']
#     # chans two values 'fil' or 'all'. All - just plot all channels
#     # ppl - means use pyplot interface
#     # 'fil' - plot ony those with meaningful std (aka data). Std threshdol 1e-2
#     # the plotter! plots all channels contained in the sxm-dict structure
#
#
    fn = _Scan.fname
    #plotdict = dict()
    # allow plotting of specific channels
    if chans == 'all':
        chans = _Scan.signals.keys()
    elif chans == 'fil':
        chans = []
        for c in _Scan.signals.keys():
            im2 = _Scan.signals[c]['forward']
            im2 = im2/(np.max(im2)-np.min(im2))
            if np.std(im2) > 0.2:
                chans.append(c)

    if len(chans) == 0:
        return #no valid data found

    fig3 = tools.make_subplots(rows=2, cols=len(chans), vertical_spacing=0.5)


    #fig3, ax3 = plt.subplots(nrows=2, ncols=len(chans),figsize=(5,6*(1+len(chans))))
        #, sharex='col', sharey=True,
        #                     gridspec_kw={'height_ratios': [2, 1]},
        #                     figsize=(4, 7))
    # if len(chans) == 1:
    #     ax3 = ax3[:,np.newaxis]

    for j, ch in tqdm(enumerate(chans)):
        traceForw = PlotImageLy(_Scan, chan=ch, ax=None, forw=1)
        traceRev = PlotImageLy(_Scan, chan=ch, ax=None, forw=0)

        fig3.append_trace(traceForw,1,j+1)
        fig3.append_trace(traceRev, 2,j+1)

        #ax3[0,0] = f3.add_subplot(gs[0, j])
        #axr = f3.add_subplot(gs[1, j])
    fig3['layout'].update(height=800, width=400*(len(chans)), title="Scan #"+ str(scanid) + ':' + fn)
    return fig3

    #plt.tight_layout(pad = 0.04, w_pad = 0.05, h_pad = 0.05)
    #plt.subplots_adjust(left=0.0, bottom=0.2, right=0.1, top=0.9, wspace=0.2, hspace=0.2)
    #plt.tight_layout(pad=0)
    #fig3.set_tight_layout({'rect': [0, 0.0, 1, 0.92], 'pad': 0.05, 'h_pad': 0.05})
    #plt.setp(axes, title='Test')
    #fig3.suptitle("Scan #"+ str(scanid) + ':' + fn, size=12)

def PlotImageLy(_Scan, chan, ax, forw=1, cm='magma'):

    #clean up missing vavlues
    from matplotlib.colors import LogNorm
    fb = 'forward' if forw else 'backward'
    im2 = _Scan.signals[chan][fb]
    if np.any(np.isnan(im2)):
        cleanrange = np.setxor1d(np.arange(np.size(im2, 0)), np.unique(np.where(np.isnan(im2))[0]))
        im2 = im2[cleanrange]

    if chan.lower()=='z':
        im2 = SubtractLine(im2)

    scale = _Scan.header['scan_range']/_Scan.header['scan_pixels']
    stat = [np.mean(im2), np.mean([np.std(im2 / np.max(im2)), np.std(im2 / np.min(im2))])]
    color_range = [stat[0] - 3 * stat[1], stat[0] + 3 * stat[1]]
    #im2 = (im2 - np.min(im2))/(np.max(im2)-np.min(im2))
    im2 = (im2 - np.min(im2))+1e-4# / (np.max(im2) - np.min(im2))
    im2 = im2/np.max(im2)
    #im2 = np.log10(im2)
    #trace = go.Heatmap(z=im2.tolist())
    trace = go.Heatmap(z=im2.tolist(), colorscale='YlOrRd')
    return trace
    #fig = go.Figure(data=[trace])
    # ax.imshow(im2, cmap=cm, norm=LogNorm(vmin=0.05, vmax=1.1))
    #
    # scale_unit = np.min([i / j for i, j in zip(_Scan.header['scan_range'], im2.shape)])
    #
    # sbar = ScaleBar(scale_unit, location='upper right', font_properties={'size': 8})
    #
    # fp = sbar.get_font_properties()
    # fp.set_size(8)
    # #ax.axes([0.08, 0.08, 0.94 - 0.08, 0.94 - 0.08])  # [left, bottom, width, height]
    # #ax.axis('scaled')
    # ax.add_artist(sbar)
    # ax.set_title(chan+' '+ fb, fontsize=8)
    # ax.set_title(phdf+j)
    # ax.set_title('$'+j+'$')
    #ax.set_axis_off()