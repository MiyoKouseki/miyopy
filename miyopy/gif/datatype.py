#
#! coding:utf-8
import logging
import numpy as np

from astropy import units as u
from .fromfiles import fromfiles,fromfile,cliptime
from .files import findfiles,fname_fmt
#from ..time import to_JSTdatetime
#from gwpy.time import tconvert
from datetime import datetime

Hz = 1
byte = 1   

datatype = {
    # Data Loction   : [ Sampling Frequncy, Data Size, c2V or Strain]
    '/NAS/cRIO01_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO02_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO03_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/PXI1_data/5000Hz/':[(5000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/NAS/PXI1_data/50000Hz/':[(50000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/data1/PHASE/50000Hz/':[(200*Hz,8*byte),np.float64,1*u.dimensionless_unscaled],
    '/data2/CLIO/LIN/':[(200*Hz,8*byte), np.float64, 1*u.dimensionless_unscaled],
    '/data2/CLIO/SHR/':[(200*Hz,8*byte), np.float64, 1*u.dimensionless_unscaled],
    '/PXI_DATA2/PXI1_data/5Hz/':[(5*Hz,4*byte), np.int32, 5.525e-9*u.Volt],        
    }
    
def second_is_00(date):
    '''
    Parameters
    ----------
    date : datetime

        
    if second is 0, return True, not if return False.
    '''
    if date.second == 0 :
        return True
    else:
        return False
    

class GifData(object):
    def __init__(self,chname):
        self.chname = chname
        DataLocation = fname_fmt[self.chname].split('<fname>')[0]
        info = datatype[DataLocation]
        self.dtype = info[1]
        self.byte = info[0][1]
        self.fs = info[0][0]
        self.c2V = info[2]
        self._check_chname()
        
        
    @classmethod
    def read(cls,start,end,chname,**kwargs):
        ''' Read gif dataa
        
        Parameter
        ---------
        start : `int`
            start start time.
        end : int
            end.
        chname : `str`
            channel name.            

        Returns
        -------
        data : `numpy.array`
        '''
        fnames = findfiles(cls,start,end,chname,**kwargs)
        fnames = fnames[0] # ignore segment
        data = fromfiles(cls,fnames,chname)        
        data = cliptime(data,start,end,cls(chname).fs)
        data = data*cls(chname).c2V
        return data
    
    @classmethod
    def fromfiles(cls,fname,chname,**kwargs):
        '''
        '''        
        return fromfiles(cls,fname,chname)

    @classmethod
    def fromfile(cls,fname,chname,**kwargs):
        '''
        '''        
        return fromfile(cls,fname,chname)
    
    
    @classmethod
    def findfiles(cls,start,end,chname,**kwargs):
        return findfiles(cls,start,end,chname,**kwargs)
    
    @classmethod
    def path_to_file(cls,chname,date,prefix='/Users/miyo/Dropbox/KagraData/gif/'):
        ''' Return path to file
        
        Parameter
        ---------
        date: datetime
            datetime. JST
        prefix: str
            location where gif binary data is saved.

        Return
        ------
        path : str
            path to file
        '''
        if not isinstance(date,datetime):
            raise ValueError('not datetime. {0}'.format(type(date)))
                
        if not second_is_00(date):
            raise ValueError('Second is not 0!')

        # date is datetime    
        date_str = date.strftime(date_fmt)
        path_to_file = prefix + fname_fmt[chname].replace('<fname>',date_str)
        return path_to_file

    
    def _check_chname(self):
        ''' check wheter channel name exit or not.        
        
        '''
        from .error import NoChannelNameError
        if not self.chname in fname_fmt.keys():
            raise NoChannelNameError(self.chname)
       
        
    def _get_fname(self):
        date = to_JSTdatetime(int(self.t0))
        date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
        self.fname = fname_fmt[self.chname].replace('<fname>',date_str)        


        




      
