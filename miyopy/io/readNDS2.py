#
#! coding:utf-8
import numpy as np
from scipy import signal
import platform
import numpy as np
import pickle
from miyopy.types import Timeseries
import traceback
import logging

def fetch_data(start,end,chlst,nds_hostname='k1nds0'):
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
    #if platform.system() == 'Linux':
    try:
        import nds2
        print 'loading data from {0} server'.format(nds_hostname)
        conn = nds2.connection('10.68.10.121', 8088) # nds0
        buffers = conn.fetch(start,end,chlst)
        data_list = []
        print 'Loading is done.'
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
    #else:
    except Exception as e:
        logging.error(traceback.format_exc())
        print '[NDSError] No nds2 library in your PC'
        print '[NDSError] Your computer is {0}.'.format(platform.system())
        print '[NDSError] Please use k1ctr computer under KAGRA CDS network...'
        print '[NDSError] - ssh controls@10.68.10.55'
        print '[NSDError] - cd /users/Miyo/KagraDropboxMiyo/GIF/github/'
        exit()    

        
def dump(fn,data):
    print 'Dumping a pickle file to {0}'.format(fn)
    with open(fn, 'wb') as f:       
        pickle.dump(data, f)
    print 'Dumping is done'

    
def load(fn):
    with open(fn, 'rb') as f:
        data_ = pickle.load(f)
    return data_


if __name__ == '__main__':
    data = fetch_data(1207197172,1207197172+100,['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_NS_SENSINF_OUT16'])
    print data
