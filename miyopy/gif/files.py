#
#! coding:utf-8
import os 
from astropy.time import Time
from datetime import datetime as dt

from numpy import arange

from datetime import datetime as dt
from datetime import datetime,timedelta

from lal import LIGOTimeGPS
from gwpy.time import tconvert

from numba import jit
    
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
    'PD_PPOL_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD00',
    'PD_SPOL_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD01',
    'PD_INPUT_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD02',
    'PD_ABSORP_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD03',
    'PD_PPOL_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD00',
    'PD_SPOL_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD01',
    'PD_INPUT_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD02',
    'PD_ABSORP_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD03',
    'CALC_STRAIN':'/data1/PHASE/50000Hz/<fname>.STRAIN',
    'CLIO_CALC_STRAIN_LIN':'/data2/CLIO/LIN/<fname>.LIN',
    'CLIO_CALC_STRAIN_SHR':'/data2/CLIO/SHR/<fname>.SHR',
    #
    'PD_PPOL_PXI01_5':'/PXI_DATA2/PXI1_data/5Hz/<fname>.AD00',
    'PD_SPOL_PXI01_5':'/PXI_DATA2/PXI1_data/5Hz/<fname>.AD01',
    'PD_INPUT_PXI01_5':'/PXI_DATA2/PXI1_data/5Hz/<fname>.AD02',
    'PD_ABSORP_PXI01_5':'/PXI_DATA2/PXI1_data/5Hz/<fname>.AD03',    
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


def path_to_file(chname,date,prefix='/Users/miyo/KagraData/gif/'):        
    ''' Return path to file
    
    Parameter
    ---------
    date: 
        gpstime(JST)

    prefix: str
    location where gif binary data is saved.
    
    Return
    ------
    path : str
    path to file
    '''
    date = tconvert(date) # GPS(JST) -> JST
    date = date + timedelta(hours=9) #UTC -> JST
    date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
    path_to_file = prefix + fname_fmt[chname].replace('<fname>',date_str)
    return path_to_file



def findfiles(cls,start,end,chname,**kwargs):
    ''' Return file path
    
    Parameter
    ---------
    start: int
        start gps time. 

    end: int
        end gps time. 

    chname:str
        Channel name. Must be choosen from fname_fmt.

    prefix: str
        Location where GIF data are saved in. Default is '/Users/miyo/KAGRA/DATA/'


    Return
    ------
    segment: list of list
        Segment contains only list of file path, which files are exist. 
    '''

    prefix = kwargs.pop('prefix','/Users/miyo/KagraData/gif/')

    if isinstance(start,str) or isinstance(end,str):
        raise ValueError('Please not give `str` type',start)
    elif isinstance(start,LIGOTimeGPS) and isinstance(end,LIGOTimeGPS):
        start, end = int(start), int(end) 
    else:
        pass

    start = start #+ 9*3600
    end = end #+ 9*3600
    
    _00sec = lambda gps: gps - (gps%60) + 18    
    _s = _00sec(start)
    _e = _00sec(end)
    #gps_filenames = arange(_s,_e+60,60)
    gps_filenames = arange(_s,_e,60)    
    segments = [path_to_file(chname,gps,prefix) for gps in gps_filenames]
    return segments


def fname2gps(fname):
    datetime_str = fname.split('.')[0].split('/')[-1]
    time = dt.strptime(datetime_str, '%y%m%d%H%M')
    gps = Time(time).gps - 3600*9
    return gps

def gps2datestr(gps):
    utc = Time(gps, format='gps').to_datetime()
    date_str = utc.strftime('%Y%m%d%H%M')
    return date_str


def _read():
    segments = findfiles()
    data = []
    times = []
    for files in segments:
        new = TimeSeries.read(files,)
        data.append(new.value)
        times.append(new.times.value)
    alldata = numpy.concatenate(data)
    alltimes = numpy.concatenate(times)
    # interporate
    

def _read_with_nan():
    allfiles = [path for files in segments for path in files]
    data = TimeSeries.read(allfiles, pad=numpy.nan)
    spectrogram = data.spectrogram()
    badtimes = numpy.isnan(spectrogram[0,:])
    gooddata = spectrogram.where(badtimes)
    asd = gooddata.percentile(50)
    
