# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 00:17:22 2015

@author: jazz
"""

from .modules import *

####################

#######################
csv1D = lambda fl, sep=' ': pd.read_csv(fl,sep=sep).T.values[0]
csv2D = lambda fl, sep=' ': pd.read_csv(fl, sep=sep).values


def open_finder(file):
    subprocess.call(["open", "-R", file])


def SimpleCSVread(fl, separator, header=0):
    a = open(fl, 'rb')
    lines = a.readlines()
    datlist = list()
    for j in range(header, len(lines)):
        ln = lines[j].decode()
        # if re.match('^\#(\s\w+.\w+)\:', ln ):
        #    chanlist.append(re.findall('^\#(\s\w+.\w+)\:', ln.strip()))
        #print(ln.strip().split(','))
        datlist.append([float(x) for x in
                            ln.strip().split(separator)])  # [float(x) for x in re.findall('[-+]?\d*\.\d+E[-+]?\d+', lines[j].decode())])

    datlist = np.asarray(datlist[::-1])
    a.close()
    return datlist


def SearchFile(patt=None, base=None, generic=False):
    ''' Yield files that match a given pattern '''
    if base is None:
        base = os.getcwd()
    if generic:
        for root, dirs, files in os.walk(base):
            try:
                for _ in [os.path.join(root, _) for _ in files if fnmatch.fnmatch(_, patt)]:
                    yield _
            except IOError as error:
                print(error)
    else:
        for root, dirs, files in os.walk(base):
            try:
                for a in [_ for _ in files if fnmatch.fnmatch(_, patt)]:
                    return os.path.join(root, a)
            except IOError as error:
                print(error)

def CrawlDir(topdir=[], ext='sxm'):
    # directory crawler: return all files of a given extension
    # in the current and all the nested directories
    import tkinter as tk
    from tkinter import filedialog

    if not (len(topdir)):
        root = tk.Tk()
        root.withdraw()
        topdir = filedialog.askdirectory()

    fn = dict()
    for root, dirs, files in os.walk(topdir):
        for name in files:
            if len(re.findall('\.' + ext, name)):
                addname = os.path.join(root, name)
                if root in fn.keys():
                    fn[root].append(addname)

                else:
                    fn[root] = [addname]
    return fn

def SelectFolder():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def FindGrids(topdir=[], ext='3ds'):
    # directory crawler: return all files of a given extension
    # in the current and all the nested directories
    from data_xray import nanonisio as nio
    import tkinter as tk
    from tkinter import filedialog

    if not (len(topdir)):
        root = tk.Tk()
        root.withdraw()
        topdir = filedialog.askdirectory()

    fn = dict()
    grids = dict()
    # scans = list()

    for root, dirs, files in tqdm(os.walk(topdir)):
        for name in (files):
            if len(re.findall('\.' + ext, name)):
                addname = os.path.join(root, name)
                skey = os.path.relpath(root, topdir).replace('/', '::')
                try:
                    g2 = nio.Grid(fname=addname)
                    if np.size(g2.ds.zf) > 0:

                        if skey in grids.keys():
                            grids[skey].append(g2)
                        else:
                            grids[skey] = [g2]
                except:
                   print('skipping ' + addname)
    return grids

def FindScans(topdir=[], ext='sxm'):
    print('help')
    from data_xray import nanonisio as nio

    scans = list()
    for root, dirs, files in (os.walk(topdir)):
        for name in tqdm(files):
            if len(re.findall('\.' + ext, name)):
                addname = os.path.join(root, name)
                scans.append(nio.Scan(fname=addname))
    return scans




def GetFile(ext='mat'):

    #import easygui as eg
    #return eg.fileopenbox(default='*.'+ext, multiple=True)

    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames()
    return file_path

###############################################################
############# read Gwyddion exported txt files ################
###############################################################

def readGwyTxt(fl):
    a=open(fl,'rb')
    lines = a.readlines()
    datlist = list()
    chanlist =list()
    for j in range(len(lines))[::-1]:
        ln = lines[j].decode()
        #if re.match('^\#(\s\w+.\w+)\:', ln ):
        #    chanlist.append(re.findall('^\#(\s\w+.\w+)\:', ln.strip()))
        if re.findall(r"annel",ln):
            chan = re.findall('\:\W(.*)', '# Channel: Input 8 (Forward)' )[0].strip()
        if re.match('^\#(\s\w+.\w+)\:', ln ):
            if re.findall('Width', ln):
                chanlist.append(float(re.findall('\d+\.\d+|\d+', ln.strip())[0]))
        else:
            datlist.append([float(x) for x in ln.strip().split()])#[float(x) for x in re.findall('[-+]?\d*\.\d+E[-+]?\d+', lines[j].decode())])

    datlist = np.asarray(datlist[::-1])
    a.close()
    return datlist, chan

def walk_depth(top, topdown=True, onerror=None, followlinks=False, maxdepth=None):
    import os
    import os.path as path

    islink, join, isdir = path.islink, path.join, path.isdir

    try:
        names = os.listdir(top)
    except:
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
    if topdown:
        yield top, dirs, nondirs

    if maxdepth is None or maxdepth > 1:
        for name in dirs:
            new_path = join(top, name)
            if followlinks or not islink(new_path):
                for x in walk_depth(new_path, topdown, onerror, followlinks, None if maxdepth is None else maxdepth-1):
                    yield x
    if not topdown:
        yield top, dirs, nondirs