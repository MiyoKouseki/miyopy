#
#! coding:utf-8

import os
from scipy import signal
import miyopy.signal.mpfilter as mpf
#import miyopy
from  miyopy.io import readNDS2
import platform
#
if platform.system() == 'Linux':
    DATAdir = '/users/Miyo/KagraDropboxMiyo/GIF/data/'
    #DATAdir = '/users/Miyo/KagraDropboxMiyo/AOS/data/'
else:
    DATAdir = '/Users/miyo/Dropbox/KagraMiyo/GIF/data/'
    #DATAdir = '/Users/miyo/Dropbox/KagraMiyo/AOS/data/'
    
import numpy as np
import pickle


def dumpPickle(fn,channels,chlst='4.chlst'):
    with open(DATAdir+chlst,'r') as f:
        chlst = f.read().splitlines()
        chdic = {str(ch):i for i,ch in enumerate(chlst)}
    #print fn
    with open(fn, 'rb') as f:
        pdata = pickle.load(f)
    #ch = channel[0]
    #print ch,chdic[ch]
    #exit()
    #exit()
    data = [ pdata[chdic[ch]] for ch in channels]
    fs = 16.0
    return data,fs


def getpicklefname(t0,tlen,chlst_num=4):
    strList2intList = lambda List: map(lambda x:int(x),List)
    files = os.listdir(DATAdir)
    files = filter(lambda x:'chlst' not in x, files)
    files = filter(lambda x:'pickle' in x, files)
    #print files
    info = map(lambda x:x.replace('.pickle',''),files)
    info = map(lambda x:x.split('_'),info)
    info = map(lambda x:strList2intList(x),info)
    for i,inf in enumerate(info):
        if ((t0+tlen)-inf[0]<=inf[1])and(inf[0]<=t0):
            pickle_fname = DATAdir + '{0}_{1}_{2}.pickle'.format(info[i][0],info[i][1],info[i][2])
            return pickle_fname,[t0-info[i][0],(t0+tlen)-info[i][0]]
        
        
def DumpedFile_is_exist(t0,tlen,channel):
    return True


def loaddata_nds(t0,tlen,chlst='4.chlst'):
    try:
        with open(DATAdir+chlst,'r') as f:
            channels = f.read().splitlines()
            #for i in channels:
            #    print i
        data = readNDS2.fetch_data(t0,t0+tlen,channels)
        fs = 16
        fname = DATAdir+'{0}_{1}_{2}.pickle'.format(t0,tlen,chlst.split('.')[0])
        #print fname
        #print data
        #exit()
        readNDS2.dump(fname,data)        
    except TypeError as e:
        print e
        print 'huge'
        exit()
    return data


def readKAGRAdata(t0,tlen,channels,fs_resample=8,plot=False,detrend=False,title='./tmp_'):
    '''
    KAGRAデータを読み込む
    '''   
    try:
        fname,_ = getpicklefname(t0,tlen)
        print fname
        data_lst,_ = dumpPickle(fname,channels)
        [data.cliptime(t0,t0+tlen) for data in data_lst]
        return data_lst
    except TypeError as e:
        print type(e),e
        print 'There is no pickle data'
        print ' please save pickle data from nds or gwf'
        data_lst = loaddata_nds(t0,tlen)
        print 'bye'
        exit()
