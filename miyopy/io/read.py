#
#! coding:utf-8
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    filename='example.log',
                    level=logging.DEBUG)

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

try:
    import nds2
    import gwpy    
except:
    pass


pfx = {'Darwin':'/Users/miyo/Dropbox/KagraData/dump/', 'Linux':'./'}
pfx_gif = {'Darwin':'/Users/miyo/Dropbox/KagraData/gif/', 'Linux':'./'}
pfx_kagra = {'Darwin':'./', 'Linux':'./'}


"""
def _download_gifdata(start,end,chname='CALC_STRAIN',
                     prefix=None,prefix_gif=None,**kwargs):
    ''' 
    '''
    
    print('taking data from gif')
    data = ts.read(start,end-start,chname,prefix=prefix_gif,**kwargs)
    value = data.value
    print('done')
    print('saving data')
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print(fname)
    with open(fname,'w') as f:
        np.save(f,value)
    print('done')
    return value

    
def _download_from_nds(start,end,chname=None,prefix=None,**kwargs):
    ''' download from nds.
    
    Parameter
    ---------
    start : int
        start GPS time
    end : int 
        end GPS time
    chname : str
        channel name

    '''
    
    if chname==None:
        raise ValueError('Invalid chname name; {}'.format(chname))

    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    data = TimeSeries.fetch(chname,
                            start, end,
                            host='10.68.10.121', port=8088)
    data = data.value
    logging.info('Data was taken from nds-server({0}) '\
                 'successfully'.format('10.68.10.121'))    
    return data


def _read_from_dump():
    
    return

"""
def read(start,end,chname,**kwargs):
    '''
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
    import platform
    import socket    
    system = platform.system()
    prefix = pfx[system]
    prefix_gif = pfx_gif[system]
    prefix_kagra = pfx_kagra[system]
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    try:
        with open(fname,'rb') as f:
            value = np.load(f)
        logging.info('Data was loaded from "{0}" successfully'.format(fname))
    except IOError as e:
        logging.debug(e)        
        if 'K1' not in chname:
            value = _download_gifdata(start,end,
                                      chname=chname,
                                      prefix=prefix,
                                      prefix_gif=prefix_gif,
                                      **kwargs)
        else:
            value = reader.kagra(start,)
            #value = _download_from_nds(start,end,
            #                            chname=chname,
            #                            prefix=prefix_kagra)        
    else:
        logging.error('hoge')
        exit()
    #
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])        
    with open(fname,'w') as f:
        np.save(f,data)
    logging.info('Taken data was dumped in the {0}'.format(fname))
        
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
