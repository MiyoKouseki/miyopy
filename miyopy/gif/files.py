#
#! coding:utf-8
from astropy import units as u
import numpy as np
import traceback
import os


def findfiles(cls,start,tlen,chname,prefix='/Volumes/HDPF-UT/DATA/'):
    ''' Return file path
    
    Parameter
    ---------
    start: int
        start gps time. second.
    tlen: int
        time length. second.
    chname:str
        Channel name. Must be choosen from fname_fmt.
    prefix: str
        Location where GIF data are saved in. Default is '/Users/miyo/KAGRA/DATA/'

    Return
    ------
    flist: list of str
        file path.
    '''
    _00sec = lambda gps: gps - (gps%60) + 18    
    _s = _00sec(start)
    _e = _00sec(start+tlen)
    gpslist = np.arange(_s,_e+60,60)    
    flist = [cls.path_to_file(chname,gps,prefix) for gps in gpslist]
    return flist
