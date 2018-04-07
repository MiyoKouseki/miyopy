#
#! coding:utf-8
import numpy as np
from scipy import signal
import mpplot as mpp
import platform
if platform.system() == 'Linux':
    #from gwpy.timeseries import TimeSeries
    #from glue.lal import Cache
    import nds2 # if you use mac , please comment out
import numpy as np
import pickle

def fetch_data(start,end,chlst):
    '''
    NDS2を利用してデータを取得する。
    
    Parameters
    ----------
    start : int
        Start GPS time.
    end : int
        End GPS time.
    chlst : list
        List of the CDS channel.
    
    Returns
    -------
    data : list 
        

    Example
    -------
    >>> channel = ['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']
    >>> fetch_data(1205201472,1205205568,channel)
    <list of the numpy array>
    '''
    conn = nds2.connection('10.68.10.122', 8088) # nds1
    buffers = conn.fetch(start,end,chlst)
    data = [b.data for b in buffers]
    return data

def dump(fn,data):
    with open(fn, 'wb') as f:       
        pickle.dump(data, f)

def load(fn):
    with open(fn, 'rb') as f:
        data_ = pickle.load(f)
    return data_


