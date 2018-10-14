#
#! coding:utf-8
import numpy as np

def cliptime(data,gps,tlen,fs):
    s_ = 60*(gps/60)+18 
    e_ = 60*((gps+tlen)/60)+18
    idx = [(gps-s_)*fs,(gps+tlen-s_)*fs]
    data = data[idx[0]:idx[1]]
    return data


#def decimate(data,fs=8):
#    fs0 = len(data)/60
#    data = signal.decimate(data,int(fs0/fs))


def _fromfile(fname,fs,dtype=None):
    try:
        data = np.fromfile(fname,dtype=dtype)
    except:
        data = np.zero([60*fs])
        data[:] = np.nan
    return data


def fromfiles(cls,fnames,chname):
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
    check_filesize(cls,fnames,chname)    
    gdata = cls(chname)
    data = _fromfile(fnames[0],gdata.fs,dtype=gdata.dtype)
    for fname in fnames[1:]:
        data = np.r_[data,_fromfile(fname,gdata.fs,dtype=gdata.dtype)]
    data = check_nan(data,fnames,chname)        
    return data

def check_nan(data,fname,chname):
    if True in np.isnan(data):
        idx = np.where(np.isnan(data)==True)[0]
        print '[Warning] found nan value. did zero padding'
        print '\t Continuing..'
        data[idx] = np.nan
    else:
        pass    
    return data


def _getsize(path):
    import os
    try:
        size = os.path.getsize(path)
    except Exception as e:
        print(e)
        size = 0
    return size 


def check_filesize(cls,fnames,chname):
    '''GIFのファイルが欠損していないか確認する関数。
    
    Parameter
    ---------
    fnames : list of str
      GIFデータの絶対パスのリスト
    chname : str
      GIFデータのチャンネル名。これを元にしてチャンネルの情報をしらべる。ゆくゆくはなくして綺麗にしたい。
    '''    
    import os
    #gdata = gifdata(chname)
    fsize = [_getsize(path) for path in fnames]
    gdata = cls(chname)
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

