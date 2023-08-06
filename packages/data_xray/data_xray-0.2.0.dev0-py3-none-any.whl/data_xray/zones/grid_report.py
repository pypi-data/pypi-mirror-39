#%%

#nanonis import sub-module

#viz sub-module
from data_xray import viz

#clustering sub-module

#grid-specific functions
from data_xray import grid

#all the nice modules

#helfpful functions

from data_xray.file_io import *

%load_ext autoreload
%autoreload 2

#from data_xray.file_io import FindGrids

#%%
topdir = '/Volumes/Seagate Backup Plus Drive/Complete vacuum data set - Peter'
topdir = '/media/petro/Seagate Backup Plus Drive/Complete vacuum data set - Peter/'
#locate grid files

#%%
print(topdir)

#%%
grids = FindGrids(topdir=topdir, ext='3ds')

#%%
grids
#%%


#%%
pres = InitPPT(new=True, pname='allgrids2.pptx')


for gf in grids:
    for g in tqdm(grids[gf]):
        ds1 = g.ds
        grid.SubtractZOffsetDS(ds1,chan=['zf'])
        grid.ChanModDS(ds1,['zf'], mod=lambda x: x/1e-9)

        #look at 25 random spectra
        #use mod parameter to pass lambda functions to modify the channels if needed
        f1,a1=plt.subplots(1,1,figsize=(6,4))
        d2 = viz.ViewGridSpectra(ds1, chan=['zf'],ax=a1, pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Z, nm','t':'a few Z-V curves'})
        #fig.savefig('random_log(I).png',type='png', dpi=200)
        FigToPPT([f1],pres=pres,leftop=[2,2], txt=ds1.attrs['filename'] + '  Random Z-spectra')

        #histogram
        f2,a2 = plt.subplots(1,1, figsize=(6,4))
        grid.ChanHistogramDS(ds1,xy=['bias','zf'],xymod=[lambda x:x,lambda y:y],
               ax=a2,label=[r'$bias, V$',r'$strain$', r'all points'])
        FigToPPT([f2],pres=pres,leftop=[2,2], txt='Z Histogram ')

        #Amplitude, Phase
        f3,a3=plt.subplots(1,2,figsize=(10,4))
        d2 = viz.ViewGridSpectra(ds1, chan=['ampf'],ax=a3[0], pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Amplitude','t':'a few Z-V curves'})
        d3 = viz.ViewGridSpectra(ds1, chan=['phif'],ax=a3[1], pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Phase','t':'a few Z-V curves'})
        FigToPPT([f3],pres=pres,leftop=[0,2], txt='Amplitude/Phase')

        #Histogram of amplitude and phase
        f4,a4 = plt.subplots(1,2, figsize=(10,4))
        grid.ChanHistogramDS(ds1,xy=['bias','ampf'],xymod=[lambda x:x,lambda y:y],
               ax=a4[0],label=[r'$bias, V$',r'$amplitude$', r'all points'])
        grid.ChanHistogramDS(ds1,xy=['bias','ampf'],xymod=[lambda x:x,lambda y:y],
               ax=a4[1],label=[r'$bias, V$',r'$phase$', r'all points'])
               
        FigToPPT([f4],pres=pres,leftop=[0,2], txt='Amplitude/Phase Histograms ')

        #pca followed by Kmeans clustering on first two PCA components

        f5,a5 = plt.subplots(1, 3, figsize=(12,3))
        grid.ChanPcaKmeansDS(ds1,chan='zf',comps=6,nclust=3, ax=a5[:2])
        a5[-1].imshow(ds1.zf_kmeans)
        FigToPPT([f5],pres=pres,leftop=[0,2], txt='PCA-KMeans')

        pres.save(topdir + 'allgrids2.pptx')
#%%
#%%
grid.SubtractZOffsetDS(ds1,chan=['zf'])
grid.ChanModDS(ds1,['zf'], mod=lambda x: x/1e-9)
#%%
ds1.attrs['filename']

#%%
import sys
import io

old_stdout = sys.stdout # Memorize the default stdout stream
sys.stdout = buffer = io.StringIO()

print(ds1)

sys.stdout = old_stdout # Put the old stream back in place

whatWasPrinted = buffer.getvalue() # Return a str containing the entire contents of the buffer.
whatWasPrinted

#%%
TextToSlide(ds1.attrs['filename'], pres=pres)
pres.save(topdir + 'allgrids2.pptx')
#%%
#look at 25 random spectra
#use mod parameter to pass lambda functions to modify the channels if needed
fig,ax=plt.subplots(1,1,figsize=(6,4))
d2 = viz.ViewGridSpectra(ds1, chan=['zf'],ax=ax, pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Z, nm','t':'a few Z-V curves'})
#fig.savefig('random_log(I).png',type='png', dpi=200)
FigToPPT([fig],pres=pres,leftop=[2,2], txt=ds1.attrs['filename'])

#%%

f3,a3 = plt.subplots(1,1, figsize=(6,4))
grid.ChanHistogramDS(ds1,xy=['bias','zf'],xymod=[lambda x:x,lambda y:y],
               ax=a3,label=[r'$bias, V$',r'$strain$', r'all points'])
FigToPPT([fig],pres=pres,leftop=[2,2], txt='Z Histogram ')


#%%
fig,ax=plt.subplots(1,2,figsize=(10,4))
d2 = viz.ViewGridSpectra(ds1, chan=['ampf'],ax=ax[0], pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Amplitude','t':'a few Z-V curves'})
d3 = viz.ViewGridSpectra(ds1, chan=['phif'],ax=ax[1], pickrandom=25, mod=lambda x: x,labels={'x':'bias, V','y':'Phase','t':'a few Z-V curves'})
FigToPPT([fig],pres=pres,leftop=[0,2], txt=ds1.attrs['filename'])


#%%
#pca followed by Kmeans clustering on first two PCA components

f6,a6 = plt.subplots(1, 3, figsize=(12,3))
grid.ChanPcaKmeansDS(ds1,chan='zf',comps=6,nclust=3, ax=a6[:2])
a6[-1].imshow(ds1.zf_kmeans)
FigToPPT([f6],pres=pres,leftop=[0,2], txt=ds1.attrs['filename'])

# #%%
# px = np.ravel((ds1.zf_kmeans.values.reshape((ds1.dims['x']*ds1.dims['y'],1))==2))
# print(px)

# #%%
# f3,a3 = plt.subplots(1,1, figsize=(6,4))
# grid.ChanHistogramDS(ds1,xy=['bias','zf'],xymod=[lambda x:x,lambda y:y],
#                ax=a3,label=[r'$bias, V$',r'$strain$', r'all points'])
# #FigToPPT([fig],pres=pres,leftop=[2,2], txt='Z Histogram ')

#%%
plt.imshow(ds1.zf_kmeans)
#%%
ds1

#%%
pres.save(topdir + 'allgrids2.pptx')
#%%
np.size(ds1.zf)

#%%
list(grids.keys())

#%%
ds1

#%%
os.getcwd()