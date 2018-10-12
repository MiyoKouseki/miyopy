#
#! coding:utf-8
from astropy import units as u
import numpy as np
import traceback
import os
from datatype import gifdata



def getsize(path):
    try:
        return os.path.getsize(path)
    except:
        #print(traceback.format_exc())
        print '! {0}'.format(path)
        return 0

    
def check_filesize(fnames,chname):
    ''' check whether GIF files lacks data or not.
    
    Parameter
    ---------
    fnames : list of str
        path to file 
    chname : str
        channel name
    '''    
    g = gifdatatype(chname)
    fsize = [getsize(path) for path in fnames]        
    size_ = [g.byte*g.fs*60 for i in range(len(fnames))]
    ans = np.array(fsize)==np.array(size_)
    if fsize!=size_:
        print '[Warning] detect lack of data'
        idxs = np.where(ans==False)[0]
        lack_of_data = [fnames[idx] for idx in idxs]
        lack = [fsize[idx] for idx in idxs]
        for i,fname in enumerate(lack_of_data):
            print ' - ',fname,lack[i]            
    return fsize


def path_to_file(t0,chname,prefix='/Volumes/HDPF-UT/DATA/'):
    '''T0時刻、ただし分で丸められた時刻、に対応するファイル名を返す関数。

    Parameter
    ---------
    t0time: int
      開始時刻。T0時間で指定。
    tlen: int
      長さ。秒で指定。
    chname:str
      チャンネル名。fname_fmtで指定されている名前を指定。
    prefix: str
      GIFデータが保存されているローカルディレクトリ。
    '''
    g = gifdatatype(chname,t0)
    path_to_file = prefix[:-1] + g.fname
    return path_to_file


def findFiles(t0,tlen,chname,prefix='/Volumes/HDPF-UT/DATA/'):
    '''T0時刻で指定した期間を含むファイルをローカルディレクトリから探す関数。

    GIFのファイルは１ファイル１分のファイルを日時で管理しているため、ファイルに保存されている時系列データはかならず00秒始まり。なのでファイル名を探すときは、指定した開始時刻と終了時刻を60秒で丸める必要がある。簡単な例として、2017-01-15-00:00:00のT0時間は60で割ると18なので、とりあえず、指定した時刻を60で割った余りがそれになるように丸めればよい。ただし注意として、途中、うるう秒が入ってくるとつかえない。
    
    Parameter
    ---------
    t0: int
      開始時刻。T0時間で指定。
    tlen: int
      長さ。秒で指定。
    chname:str
      チャンネル名。fname_fmtで指定されている名前を指定。
    prefix: str
      GIFデータが保存されているローカルディレクトリ。一応デフォルトでは、'/Users/miyo/KAGRA/DATA/'に保存している。

    Return
    ------
    fnames: list of str
      GIFデータまでの絶対PATHを1ファイルごとに格納したリスト。
    '''
    s_ = 60*(t0/60)+18#*u.second
    e_ = 60*((t0+tlen)/60)+18#*u.second
    fnames_t0 = np.arange(s_,e_+60,60)#*u.second
    print 'calc filename'
    fnames = [path_to_file(t0,chname,prefix) for t0 in fnames_t0]
    print 'done.'
    return fnames


def fromfiles(fnames,chname,fs,mintrend=False):
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
    g = gifdatatype(chname)    
    if mintrend==False:
        data = np.array([np.fromfile(fname,dtype=g.dtype) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]*shape[1]))[0]
    else:
        data = np.array([np.average(np.fromfile(fname,dtype=g.dtype)) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]))[0]
    try:
        return data
    except IOError as e:
        print e
        print 'No data. Did you download GIF file?'
        exit()


def check_nan(data,fname,chname):
    if True in np.isnan(data):
        idx = np.where(np.isnan(data)==True)[0]
        print '[Warning] found nan value. did zero padding'
        print '\t Continuing..'
        data[idx] = np.nan
    else:
        pass    
    return data
        
