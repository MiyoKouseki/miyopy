#
#! coding:utf-8

import nds2

def fetch(start,end,chlst,nds_hostname='k1nds0'):
    ''' fetch data using nds.    
    
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
    >>> channel = 'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16'
    >>> fetch(1205201472,1205205568,channel)
    <list of the numpy array>
    '''
    conn = nds2.connection('10.68.10.121', 8088) # nds0
    buffers = conn.fetch(start,end,chlst)
    return buffers.data



if __name__ == '__main__':
    chname = 'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16'
    data = fetch(1207197172,1207197172+100,chname)
    print data
