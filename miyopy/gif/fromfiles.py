#
#! coding:utf-8
import numpy as np
from .datatype import gifdatatype

def decimate(data,fs=8):
    fs0 = len(data)/60
    data = signal.decimate(data,int(fs0/fs))
    

def fromfile(fname,chname,**kwargs):
    g = gifdatatype(chname)
    #try:
    data = np.fromfile(fname,dtype=g.dtype)
    data = decimate(data,fs=8)
    #data = 2.0
    #except IOError:        
    #data = 0        
    return data

    
def fromfiles(fnames,chname,fs=8,mintrend=False):
    ''' np.fromfileを連続したファイルに対応させたもの。
    
    Parameter
    ---------
    fname : list of str
        GIFのファイル名が書かれたリスト。
    chname : str
        チャンネル名。これをつかってDtypeを調べているけど、どこかに移して綺麗にしたい。それにnp.fromfileの上位互換になるように、*args,**kwargsを拾えるようにしたい。
    Return
    ------
    data : numpy.ndarray
        1次元になったndarray    
    '''
    g = gifdatatype(chname)    
    if mintrend==False:
        data = np.array([np.fromfile(fname,dtype=g.dtype) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]*shape[1]))[0]
    else:
        data = np.array([np.average(np.fromfile(fname,dtype=g.dtype)) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]))[0]
    try:
        return data
    except IOError as e:
        print e
        print 'No data. Did you download GIF file?'
        exit()
