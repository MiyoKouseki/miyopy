#
#! coding:utf-8
import numpy as np
from scipy import signal
import platform
import numpy as np
import pickle
from miyopy.types import Timeseries

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
    if platform.system() == 'Linux':
        import nds2
        conn = nds2.connection('10.68.10.121', 8088) # nds0
        buffers = conn.fetch(start,end,chlst)
        data_list = []        
        for buf in buffers:
            chname = buf.channel.name
            fs = buf.channel.sample_rate
            unit = buf.channel.signal_units
            nlen = buf.length
            t0 = buf.gps_seconds
            data = buf.data
            mpdata = Timeseries(data,t0=t0,fs=fs,name=chname,unit=unit)
            data_list += [mpdata]
        return data_list
    else:
        print 'Your computer is {0}.'.format(platform.system())
        print 'Please use k1ctr computer under KAGRA CDS network...'
        print ' ssh controls@10.68.10.55'
        print ' cd /users/Miyo/KagraDropboxMiyo/GIF/github/'
        exit()    

        
def dump(fn,data):
    with open(fn, 'wb') as f:       
        pickle.dump(data, f)
    print 'dumped {0}'.format(fn)

    
def load(fn):
    with open(fn, 'rb') as f:
        data_ = pickle.load(f)
    return data_


if __name__ == '__main__':
    data = fetch_data(1207197172,1207197172+100,['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_NS_SENSINF_OUT16'])
    print data
