#
#! coding:utf-8

import os

data_prefix = '/Users/miyo/Dropbox/KagraMiyo/GIF/data/'
import numpy as np
import pickle

def load(fn):
    with open(fn, 'rb') as f:
        data_ = pickle.load(f)
    return data_

def _loadchlst(chlst_fname):
    '''
    使用するデータのチャンネルを".chlst"ファイルから取得する           
    '''
    with open(chlst_fname,'r') as f:
        chlst = f.read().splitlines()    
        chdic = {str(ch):i for i,ch in enumerate(chlst)}
    return chlst,chdic
           
def getpicklefname(start,duration,chlst_num):
    strList2intList = lambda List: map(lambda x:int(x),List)    
    files = os.listdir(data_prefix)
    info = map(lambda x:x.replace('.pickle',''),files)
    info = map(lambda x:x.split('_'),info)
    info = map(lambda x:strList2intList(x),info)
    info_ = map(lambda x:[x[0],x[0]+x[1],x[2]],info)
    end = start+duration
    for i,info__ in enumerate(info_):
        if (info__[0]<start) and (end<info__[1]):
            break
    pickle_fname = data_prefix + '{0}_{1}_{2}.pickle'.format(
        info[i][0],
        info[i][1],
        info[i][2]
        )
    return pickle_fname,[start-info[i][0],end-info[i][0]]

def readKAGRAdata(start,duration,channel):
    print start,duration
    chlst_fname = '1.chlst'
    chlst_num = chlst_fname.split('.chlst')[0]
    pickle_fname,idx = getpicklefname(start,duration,chlst_num)
    _,chdic = _loadchlst(chlst_fname)    
    data = load(pickle_fname)
    data = data[chdic[channel]]
    data = data[16*idx[0]:16*idx[1]]
    return data
