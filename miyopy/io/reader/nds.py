#
#! coding:utf-8

import nds2

class ChannelNameException(Exception):
    pass

def read(start,end,chlst,nds_hostname='k1nds0',**kwargs):
    ''' read data using nds.    
    
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
    >>> read(1205201472,1205205568,channel)
    <list of the numpy array>
    '''
    if not isinstance(chlst,list):
        raise ChannelNameException('Please give chlst as list type.\n'\
                                   'Given chlst is {}, which type is {}'\
                                       .format(chlst,type(chlst)))
    elif isinstance(chlst,str):
        chlst = [chlst]        
    conn = nds2.connection('10.68.10.121', 8088) # nds0
    buffers = conn.fetch(start,end,chlst)
    return buffers



if __name__ == '__main__':
    chlst = ['K1:PEM-EXV_SEIS_WE_SENSINF_INMON']
    buffers = read(1222387218,1222387218+100,chlst)
    print buffers[0].data    
