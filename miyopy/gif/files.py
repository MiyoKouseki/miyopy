#
#! coding:utf-8
import os 
from astropy.time import Time
from datetime import datetime as dt

from numpy import arange

from datetime import datetime as dt
from datetime import datetime,timedelta

from gwpy.time import tconvert


def findfiles(cls,chname,start,end,prefix='/Users/miyo/Dropbox/KagraData/gif/'):
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
    
    if isinstance(start,str):
        start_utc = tconvert(start) 
        end_utc = tconvert(end)
    else:
        pass

    start = start + 9*3600
    end = end + 9*3600
    
    _00sec = lambda gps: gps - (gps%60) + 18    
    _s = _00sec(start)
    _e = _00sec(end)
    gps_filenames = arange(_s,_e+60,60)

    segments = [[]]
    for gps in gps_filenames:
        path = cls.path_to_file(chname, gps, prefix)
        if os.path.exists(path):
            segments[-1].append(path)
        else:
            segments.append([])
    if not segments[-1]:
        segments.pop(-1)
        
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
    
