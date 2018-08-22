#
#! coding:utf-8
import traceback

from .findfiles import findFiles,check_filesize,fromfiles,check_nan
from .datatype import gifdatatype

from ..time import to_JSTdatetime,to_GPStime


def read(t0,tlen,chname,fs=8,trendtype=None,prefix=None,**kwargs):
    '''GIFのデータファイルからデータを読み込むための関数。
    
    GIFのバイナリファイルを読み込むための関数。
    
    Parameter
    ---------
    t0 : int
        開始時刻。
    tlen : int
        データ長さ。秒。
    chname : str
        チャンネル名。
    fs : int
        サンプリングを指定。1/4,1/2,1,2,4,8まで対応。

    Return
    ------
    timeseries

    '''
    from ..timeseries import TimeSeries    
    g = gifdatatype(chname)
    fnames = findFiles(t0,tlen,chname,prefix=prefix)
    check_filesize(fnames,chname) # デコレータにする
    data = fromfiles(fnames,chname,fs)
    data = check_nan(data,fnames,chname) # デコレータにする
    # clip data 関数にまとめる
    s_ = 60*(t0/60)+18
    e_ = 60*((t0+tlen)/60)+18
    idx = [int(((t0-s_)*g.fs)),int(((t0+tlen-s_)*g.fs))]
    data = g.calib(data[idx[0]:idx[1]])
    #
    if not isinstance(fs,str) and (len(data)/g.fs!=tlen):
        print len(data)
        print 'Error: tlen do not match'
        print len(data)/g.fs,'!=',tlen
        exit()
    if trendtype=='min':
        dt=60.0
        data = TimeSeries(data,vunit='V',t0=t0,dt=dt,tunit='second',name=chname)
        return data
    else:
        dt=1.0/fs
        data = TimeSeries(data,vunit='V',t0=t0,dt=dt,tunit='second',name=chname)
        return data        
