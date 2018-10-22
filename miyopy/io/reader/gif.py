#
#! coding:utf-8

import numpy as np

from ...gif import GifData


def read(start,tlen,chname,**kwargs):
    ''' Read gif data

    Parameters
    ----------
    start : int
        start gps time
    tlen : int
        time length
    chname : str
        channel name

    Returns 
    -------
    timeseries of the gif data    
    '''
    return GifData.read(start,tlen,chname,**kwargs)
    

