#%%

#misc modules supporting data_xray
from data_xray.modules import *

#sub-module to read nanonis files

#sub-module to plot data
from data_xray import viz

#routines to work with files
from data_xray.file_io import FindScans

#module that handles powerpoint interface

#this is convenient for development purpose
%load_ext autoreload
%autoreload 2

#DarkPlot()



#%%
'''typically in a folder we find a mix of sxm files (images)
.dat files (single ASCII spectra)
.3ds files (hyperspectral data)
our first task is to look at this data and convert it to xarray
'''
#%%
#Top level folder
topdir = os.getcwd()
topdir = '/media/petro/Seagate Backup Plus Drive/Complete vacuum data set - Peter/'

#%%


#clean function to find all the sxm image files in the folder, read them and convert them to a Scan object within dataxray
fdict = FindScans(topdir,'sxm')
#fdict = fdict['.']

#%%
print(fdict)

#%%
#intialize presentation
pres = InitPPT(new=True, pname='allims.pptx')

#%%
#dump all images into a presentation
chanselect = 'Z'

for folder in (fdict.keys()):
    TextToSlide(folder,pres=pres)
    for fj in tqdm(fdict[folder]):
        #TextToSlide(fj.fname,pres=pres)
        #print(fj.fname)
        f3,a3 = plt.subplots(1,1)
        d2 = viz.PlotImage(fj, chan=chanselect, ax=a3, high_pass=None)
        FigToPPT([f3],pres=pres,leftop=[3,2], txt=fj.fname)
        #f3.clf()

#%%
#don't forget to save the summary
pres.save('summary2.pptx')