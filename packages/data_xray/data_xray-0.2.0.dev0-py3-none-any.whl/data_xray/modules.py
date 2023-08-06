#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 18:31:02 2017

@author: peter
"""

import numpy as np
import deepdish as dd
from copy import copy
import pandas as pd
import seaborn as sns
import inspect
import re
import os
import sys
import copy
import subprocess
#import pyperclip
import base64
import datetime

from matplotlib.colors import LogNorm
from matplotlib import colorbar
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


#
from yattag import Doc
from tqdm import tqdm
from pyearth import Earth
from time import time
from struct import unpack


from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from skimage import exposure
from sklearn.neighbors import NearestNeighbors
from sklearn.gaussian_process.kernels import ConstantKernel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

#
from scipy import ndimage
from scipy.optimize import curve_fit
from scipy import interpolate
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy import misc, optimize
from scipy import constants as C
#
#
from pptx import Presentation
from pptx.util import Inches
from plotly.offline import plot_mpl



import mpld3

import fnmatch
import pywt
import pyperclip

import xarray as xry


def DarkPlot():
    sns.set(style="ticks", context="talk")
    plt.style.use("dark_background")


nonecheck = lambda x: '' if x is None else x
labelcheck = lambda d,x: d[x] if x in d else ''
nearest = lambda d,x: np.argmin(np.abs(d - x))

class Container(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
    def _from_dict(self, d):
        for k in list(d.keys()):
                setattr(self, k, d[k])
    def addxy(self,x,y):
        setattr(self, 'x', x)
        setattr(self, 'y', y)


import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

import spiepy
from matplotlib_scalebar.scalebar import ScaleBar

import warnings
warnings.filterwarnings("ignore")



