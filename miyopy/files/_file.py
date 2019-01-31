import os 
import re
import warnings
import numpy as np

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

def get_csd_specgram(chname1,chname2,remake=True,fftlength=2**6,overlap=0.0,**kwargs):
    hdf5fname = to_hdf5fname(chname1,chname2)
    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)
        timeseries1 = get_timeseries(chname1,**kwargs)
        timeseries2 = get_timeseries(chname2,**kwargs)
        specgram = timeseries1.csd_spectrogram(timeseries2,
                                               stride=fftlength*2,
                                               fftlength=fftlength,
                                               overlap=overlap,
                                               window='hanning',
                                               nproc=2)
        specgram.write(hdf5fname)
        return specgram
    else:
        #warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram


def get_asd(chname,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries = get_timeseries(chname,**kwargs)    
    asd = timeseries.asd(fftlength=fftlength,
                         overlap=overlap,
                         window='hanning')
    return asd

def get_csd(chname1,chname2,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries1 = get_timeseries(chname1,**kwargs)
    timeseries2 = get_timeseries(chname2,**kwargs)    
    csd = timeseries1.csd(timeseries2,
                          fftlength=fftlength,
                          overlap=overlap,
                          window='hanning')
    return csd


def get_coherence(chname1,chname2,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries1 = get_timeseries(chname1,**kwargs)
    timeseries2 = get_timeseries(chname2,**kwargs)    
    coherence = timeseries1.coherence(timeseries2,
                                      fftlength=fftlength,
                                      overlap=overlap,
                                      window='hanning')
    return coherence

    
def get_specgram(*chname,**kwargs):
    n = len(chname)
    if n==2:
        chname1,chname2 = chname
        specgram = get_csd_specgram(chname1,chname2,**kwargs)
        return specgram
    elif n==1:
        chname = chname[0]
    else:
        raise ValueError('Wrong chname arguments')
    

    fftlength = kwargs.pop('fftlength',None)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)
    hdf5fname = to_hdf5fname(chname,**kwargs)
    #print hdf5fname
    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)
        timeseries = get_timeseries(chname,**kwargs)
        specgram = timeseries.spectrogram(stride=fftlength*2,
                                          fftlength=fftlength,
                                          overlap=overlap,
                                          window='hanning')
        #exit()        
        specgram.write(hdf5fname)
        return specgram
    else:
        #warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram




def get_timeseries(chname,**kwargs):
    start = kwargs.pop('start',None)
    end = kwargs.pop('end',None)
    nds = kwargs.pop('nds',None)
    fname = to_gwffname(chname,**kwargs)

    if os.path.exists(fname):
        print '{0} exist.',format(fname)
        print('Skip fetch from nds {0}'.format(fname))
        data = TimeSeries.read(fname,chname,start,end,
                                format='gwf.lalframe',
                                verbose=True,
                                pad=np.nan)
        return data
    elif nds and not os.path.exists(fname):
        print('{0} dose not exist.',format(fname))
        data = TimeSeries.fetch(chname, start, end,
                                verbose=True,
                                host='10.68.10.121', port=8088,
                                pad=np.nan,
                                verify=True,type=1,dtype=np.float32)
        data.write(fname,format='gwf.lalframe')
        print('wrote data in '+fname)
        return data
    else:
        print nds
        print os.path.exists(fname)
        print fname
        raise ValueError('! Must use nds or load files')
        exit()




def to_gwffname(chname,**kwargs):
    prefix = kwargs.pop('prefix',None)
    m = re.search(r'K1:PEM-(.*)_(.*)_DQ',chname)
    try:
        fname = prefix + m.group(1).lower() + '.gwf'
    except Exception as e:
        print e
        exit()
    return fname


def to_hdf5fname(*args,**kwargs):
    prefix = kwargs.pop('prefix','./data/')
    N = len(args)
    if N==2:
        chname1,chname2 = args
        #m1 = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname1)
        #m2 = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname2)
        m1 = re.search(r'K1:PEM-(.*)_(.*)_DQ',chname1)
        m2 = re.search(r'K1:PEM-(.*)_(.*)_DQ',chname2)
        fname = prefix + m1.group(1).lower() + '-' + m2.group(1).lower() + '.hdf5'
    elif N==1:
        chname = args[0]
        #m = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname)
        m = re.search(r'K1:PEM-(.*)_(.*)_DQ',chname)        
        try:
            fname = prefix + m.group(1).lower() + '.hdf5'
        except Exception as e:
            print e
    return fname
    


def to_pngfname(chname,ftype,prefix='./',**kwargs):
    if not chname:
        return  'None.png'
    
    #m = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname) old
    m = re.search(r'K1:PEM-(.*)_(.*)_DQ',chname)
    try:
        fname = prefix + ftype + '_' + m.group(1).lower() + '.png'
    except Exception as e:
        print e
        exit()
    return fname
