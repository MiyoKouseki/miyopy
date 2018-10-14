#
#! coding:utf-8
import traceback

from .findfiles import findFiles,check_filesize,fromfiles,check_nan
from .datatype import gifdata

from ..time import to_JSTdatetime,to_GPStime


def read(t0,tlen,chname,fs,plot=False,detrend=False):
    '''Read gif data.
    
    Parameters
    ----------
    t0 : int
        start gps time

    '''    
    from ..timeseries import TimeSeries    
    g = gifdatatype(chname)
    fnames = findFiles(t0,tlen,chname)
    check_filesize(fnames,chname) # デコレータにする
    data = fromfiles(fnames,chname,fs)
    data = check_nan(data,fnames,chname) # デコレータにする
    # clip data 関数にまとめる
    s_ = 60*(t0/60)+18
    e_ = 60*((t0+tlen)/60)+18
    idx = [int(((t0-s_)*g.fs)),int(((t0+tlen-s_)*g.fs))]
    data = data[idx[0]:idx[1]]*g.c2V
    #
    if not isinstance(fs,str) and (len(data)/g.fs!=tlen):
        print len(data)
        print 'Error: tlen do not match'
        print len(data)/g.fs,'!=',tlen
        exit()
    try:
        if fs=='min':
            dt=60.0
            data = TimeSeries(data,vunit='V',t0=t0,dt=dt,tunit='sec',name=chname)
            return data
        else:
            dt=1.0/fs
            data = TimeSeries(data,vunit='V',t0=t0,dt=dt,tunit='sec',name=chname) 
            return data            
    except KeyError as e:
        traceback.print_exc()
        return None
    except Exception as e:
        traceback.print_exc()
        exit()
        return None    

'''    
if __name__=="__main__":
    t0 = 1208908938+93400 # 2018-04-29T10:58:40
    print '[JST] 2018-04-29T10:58:40'
    tlen = 10
    data = readGIFdata(t0,tlen,'X500_BARO')
'''
