#
#! coding:utf-8
import numpy as np
from .datatype import gifdata

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

    
def fromfiles(fnames,chname,fs=8):
    '''Read from files continuously
    
    Parameters
    ----------
    fnames : list of str
        list of file name 
    chname : str    
        channel name
    fs : int
        aaa    
        
    Returns
    -------
    data : numpy.ndarray
        data         

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
