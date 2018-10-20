#
#! coding:utf-8
import logging
import numpy as np

from astropy import units as u

from .fromfiles import fromfiles,cliptime
from .files import findfiles
from ..time import to_JSTdatetime

Hz = 1
byte = 1   

datatype = {
    # Data Loction   : [ Sampling Frequncy, Data Size, c2V or Strain]
    '/NAS/cRIO01_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO02_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO03_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/PXI1_data/5000Hz/':[(5000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/NAS/PXI1_data/50000Hz/':[(50000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/data1/PHASE/50000Hz/':[(200*Hz,8*byte),np.float64,1],
    '/data2/CLIO/LIN/':[(200*Hz,8*byte), np.float64, 1],
    '/data2/CLIO/SHR/':[(200*Hz,8*byte), np.float64, 1],
    }
    
fname_fmt={
    # ChannelName:Format,Mustreplace<fname>.
    'X500_TEMP':'/NAS/cRIO01_data/<fname>.AD00',
    'X500_HUMD':'/NAS/cRIO01_data/<fname>.AD01',
    'X500_BARO':'/NAS/cRIO01_data/<fname>.AD02',
    'X500_VACU':'/NAS/cRIO01_data/<fname>.AD03',
    'X500_04':'/NAS/cRIO01_data/<fname>.AD04',
    'X500_05':'/NAS/cRIO01_data/<fname>.AD05',
    'X500_06':'/NAS/cRIO01_data/<fname>.AD06',
    'X500_07':'/NAS/cRIO01_data/<fname>.AD07',
    'X2000_TEMP':'/NAS/cRIO02_data/<fname>.AD00',
    'X2000_HUMD':'/NAS/cRIO02_data/<fname>.AD01',
    'X2000_BARO':'/NAS/cRIO02_data/<fname>.AD02',
    'X2000_VACU':'/NAS/cRIO02_data/<fname>.AD03',
    'X2000_04':'/NAS/cRIO02_data/<fname>.AD04',
    'X2000_05':'/NAS/cRIO02_data/<fname>.AD05',
    'X2000_06':'/NAS/cRIO02_data/<fname>.AD06',
    'X2000_07':'/NAS/cRIO02_data/<fname>.AD07',
    #
    'X1500_TR240velEW'	:'/NAS/cRIO03_data/<fname>.AD00',
    'X1500_01'	:'/NAS/cRIO03_data/<fname>.AD01',
    'X1500_TR240velNS':'/NAS/cRIO03_data/<fname>.AD02',
    'X1500_TR240velUD':'/NAS/cRIO03_data/<fname>.AD03',
    'X1500_TR240posEW':'/NAS/cRIO03_data/<fname>.AD04',
    'X1500_TR240posNS':'/NAS/cRIO03_data/<fname>.AD05',
    'X1500_TR240posUD':'/NAS/cRIO03_data/<fname>.AD06',
    'X1500_07':'/NAS/cRIO03_data/<fname>.AD07',
    'X1500_CMG3TvelEW':'/NAS/cRIO03_data/<fname>.AD08',
    'X1500_CMG3TvelNS':'/NAS/cRIO03_data/<fname>.AD09',
    'X1500_CMG3TvelUD':'/NAS/cRIO03_data/<fname>.AD10',
    'X1500_11':'/NAS/cRIO03_data/<fname>.AD11',
    'X1500_CMG3TposEW':'/NAS/cRIO03_data/<fname>.AD12',
    'X1500_CMG3TposNS':'/NAS/cRIO03_data/<fname>.AD13',
    'X1500_CMG3TposUD':'/NAS/cRIO03_data/<fname>.AD14',
    'X1500_15':'/NAS/cRIO03_data/<fname>.AD15',
    #
    'PD_PWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD00',
    'PD_SWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD01',
    'PD_INPUTWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD02',
    'PD_ABSORP_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD03',
    'PD_PWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD00',
    'PD_SWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD01',
    'PD_INPUTWAVE_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD02',
    'PD_ABSORP_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD03',
    'CALC_PHASE':'/data1/PHASE/50000Hz/<fname>.PHASE',
    'CALC_STRAIN':'/data1/PHASE/50000Hz/<fname>.STRAIN',
    'CALC_ZOBUN':'/data1/PHASE/50000Hz/<fname>.ZOBUN',
    'CALC_SQRT':'/data1/PHASE/50000Hz/<fname>.SQRT',
    'CLIO_CALC_STRAIN_LIN':'/data2/CLIO/LIN/<fname>.LIN',
    'CLIO_CALC_STRAIN_SHR':'/data2/CLIO/SHR/<fname>.SHR',
    }

date_fmt = '%Y/%m/%d/%H/%y%m%d%H%M'    


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
    def read(cls,start,tlen,chname,**kwargs):
        ''' Read gif dataa
        
        Parameter
        ---------
        start : `int`
            start start time.
        tlen : int
            time length.
        chname : `str`
            channel name.            

        Returns
        -------
        data : `numpy.array`
        '''
        fnames = findfiles(cls,start,tlen,chname,**kwargs)
        data = fromfiles(cls,fnames,chname)
        data = cliptime(data,start,tlen,cls(chname).fs)
        data = data*cls(chname).c2V
        return data

    
    @classmethod
    def path_to_file(cls,chname,date,prefix='/Users/miyo/Dropbox/KagraData/gif/'):    
        ''' Return path to file
        
        Parameter
        ---------
        gpstime: int
            start gps time.
        tlen: int
            time length.
        prefix: str
            location where gif binary data is saved.

        Return
        ------
        path : str
            path to file
        '''
        date=int(date)
        if isinstance(date,int):            
            assert (date%60)==18,'{0}%60={1}'.format(date,date%60)
            date = to_JSTdatetime(date)
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
        


    




      
