#
#! coding:utf-8
from miyopy import get_module_logger
logger = get_module_logger(__name__)

#from __future__ import print_function
#import os
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#mpl.rcParams['agg.path.chunksize'] = 1000000
#print(mpl.rcParams['agg.path.chunksize'])
import numpy as np
#from scipy.signal import butter, lfilter
#from scipy import signal, interpolate
#from control import matlab
#from trillium import selfnoise

#from miyopy.timeseries import TimeSeries as ts
from gwpy.timeseries import TimeSeries

class DumpFileException(Exception):
    pass


try:
    import nds2
    import gwpy    
except:
    pass


pfx = {'Darwin':'/Users/miyo/Dropbox/KagraData/dump/', 'Linux':'./'}
pfx_gif = {'Darwin':'/Users/miyo/Dropbox/KagraData/gif/', 'Linux':'./'}
pfx_kagra = {'Darwin':'./', 'Linux':'./'}


def read_fromsource(start,end,chname,**kwargs):
    if 'K1' not in chname:
        from miyopy.io import gif
        value = gif.read(start,end,chname,**kwargs)
    else:
        from miyopy.io import kagra
        value = kagra.read(start,end,chname,**kwargs)
        
        
def read_from_dumpfile(start,end,chname,**kwargs):
    ''' 
    '''
    import platform
    system = platform.system()
    fname = pfx[system]+'{0}_{1}_{2}'.format(start,end,chname[3:])
    try:
        with open(fname,'rb') as f:
            value = np.load(f)
        logger.info('Data was loaded from "{0}" successfully'.format(fname))
        return value
    except IOError as e:
        logger.error(e)
        raise DumpFileException('There is no such dump file "{}"'.format(fname))
    

def save_to_dump():    
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])        
    with open(fname,'w') as f:
        np.save(f,data)
    logger.info('Taken data was dumped in the {0}'.format(fname))
    
    

def read(start,end,chname,fmt='dump',**kwargs):
    '''Read 
   
    Parameters
    ----------
    start : int 
        start GPS time
    end : int 
        end GPS time
    chname : str
        channel name    

    Return
    ------
    values : 
        aaa
        
    '''
    if fmt=='dump':
        value = read_from_dumpfile(start,end,chname,**kwargs)
    elif fmt=='gif':
        value = gif.read(start,end,chname,**kwargs)
    elif fmt=='nds':
        value = kagra.read(start,end,chname,**kwargs)
    else:
        raise ValueError('invalid format. "{}"'.format(fmt))            
    return value


def fetch(chname,start,end,ndsserver='10.68.10.121'):
    try:
        print('Loading data from nds server... It may take few minutes..')
        print('ChannelName : {}'.format(chname))        
        data = TimeSeries.fetch(chname,start, end, host=ndsserver, port=8088)
        print('Done.')
        return data        
    except RuntimeError as e:
        print('[Error]',e)
        print('[Error] Faild to establish a connection to NDSserver({})'.format(ndsserver))
        print('[Error] Please check the connection with "ping {}"'.format(ndsserver))
        print('[Error] Exit..')
        exit()
    except ImportError as e:
        print('[Error] {}. Please execute "source ~/.bash_profile"'.format(e))
        exit()
