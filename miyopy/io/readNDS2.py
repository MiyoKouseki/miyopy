#
#! coding:utf-8
import numpy as np
from scipy import signal
import platform
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
    if platform.system() == 'Linux':
        import nds2
        conn = nds2.connection('10.68.10.121', 8088) # nds0
        buffers = conn.fetch(start,end,chlst)
        data = [b.data for b in buffers]
        return data        
    else:
        print """Your computer is {0}.
 Please use k1ctr computer under KAGRA CDS network...
""".format(platform.system())
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
