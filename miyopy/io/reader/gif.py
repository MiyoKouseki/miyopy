#
#! coding:utf-8
import traceback
import numpy as np
import datetime
from datetime import datetime as dt
#from sys import exit
from astropy.time import Time

from scipy import signal
#from miyopy.signal import butter_bandpass_filter
import miyopy.signal.mpfilter as mpf
from miyopy.types import Timeseries
from gifdatatype import gifdatatype

#from gwpy.timeseries import TimeSeries



def _00sec(gps):
    return gps - (gps%60) + 18


def get_filelist(sgt,tlen,chname,prefix='/Volumes/HDPF-UT/DATA/'):
    ''' Return file path
    
    Parameter
    ---------
    sgt: int
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
    _s = _00sec(sgt)
    _e = _00sec(sgt+tlen)
    gdata = gifdatatype(chname)    
    gpslist = np.arange(_s,_e+60,60)
    flist = [gdata.path_to_file(gps) for gps in gpslist]
    return flist


def _fromfile(fname,fs,dtype=None):
    try:
        data = np.fromfile(fname,dtype=dtype)
    except:
        data = np.zero([60*fs])
        data[:] = np.nan
    return data

def fromfiles(fnames,chname):
    ''' np.fromfileを連続したファイルに対応させたもの。
    
    Parameter
    ---------
    fname : list of str
        GIFのファイル名が書かれたリスト。
    chname : str
        チャンネル名。これをつかってDtypeを調べているけど、どこかに移して綺麗にしたい。それにnp.fromfileの上位互換になるように、*args,**kwargsを拾えるようにしたい。
    Return
    ------
    data : numpy.ndarray
        1次元になったndarray    
    '''
    gdata = gifdatatype(chname)
    data = _fromfile(fnames[0],gdata.fs,dtype=gdata.dtype)
    for fname in fnames[1:]:
        data = np.r_[data,_fromfile(fname,gdata.fs,dtype=gdata.dtype)]
    return data

def _getsize(path):
    import os
    try:
        size = os.path.getsize(path)
    except Exception as e:
        print(e)
        size = 0
    return size 
        
def check_filesize(fnames,chname):
    '''GIFのファイルが欠損していないか確認する関数。
    
    Parameter
    ---------
    fnames : list of str
      GIFデータの絶対パスのリスト
    chname : str
      GIFデータのチャンネル名。これを元にしてチャンネルの情報をしらべる。ゆくゆくはなくして綺麗にしたい。
    '''    
    import os
    gdata = gifdatatype(chname)
    fsize = [_getsize(path) for path in fnames]
    size_ = [gdata.byte*gdata.fs*60 for i in range(len(fnames))]
    ans = np.array(fsize)==np.array(size_)

    if fsize!=size_:
        print '[Warning] detect lack of data'
        idxs = np.where(ans==False)[0]
        lack_of_data = [fnames[idx] for idx in idxs]
        lack = [fsize[idx] for idx in idxs]
        for i,fname in enumerate(lack_of_data):
            print ' - ',fname,lack[i]
        #exit()
    else:
        return True

def check_nan(data,fname,chname):
    if True in np.isnan(data):
        idx = np.where(np.isnan(data)==True)[0]
        print '[Warning] found nan value. did zero padding'
        print '\t Continuing..'
        data[idx] = np.nan
    else:
        pass    
    return data

    
def read(gps,tlen,chname,plot=False,detrend=False,name=None,title='./tmp_',**kwargs):    
    '''指定された期間のGIFデータを取ってくる関数。
    
    GIFのバイナリファイルを読み込むための関数。                
    
    Parameter
    ---------------    
    gps : int
        開始時刻。
    tlen : int
        データ長さ。秒。
    chname : str
        チャンネル名。
    fs : int
        サンプリングを指定。1/4,1/2,1,2,4,8まで対応。
    '''
    fnames = get_filelist(gps,tlen,chname,**kwargs)
    check_filesize(fnames,chname)
    data = fromfiles(fnames,chname)
    data = check_nan(data,fnames,chname)
    gdata = gifdatatype(chname)
    s_ = 60*(gps/60)+18 
    e_ = 60*((gps+tlen)/60)+18
    idx = [(gps-s_)*gdata.fs,(gps+tlen-s_)*gdata.fs]
    data = data[idx[0]:idx[1]]*gdata.c2V
    #
    #data = mpf.decimate(data,fs_befor=fs_,fs_after=fs)
    #data = Timeseries(data,fs=fs,plot=True,detrend=detrend,name=name,title=title,unit='Voltage')
    return data
    
    
if __name__=="__main__":
    t0 = 1208908938+93400 # 2018-04-29T10:58:40
    print '[JST] 2018-04-29T10:58:40'
    tlen = 10
    data = readGIFdata(t0,tlen,'X500_BARO')
