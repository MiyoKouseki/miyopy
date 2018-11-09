#
#! coding:utf-8
import numpy as np


def fromfiles(cls,fnames,chname):
    ''' Read from files continuously.
    
    Parameters
    ----------
    fnames : list of str
        file names
    chname : str
        channel name

    Returns
    -------
    data : numpy.ndarray
        value
    '''
    _check_filesize(cls,fnames,chname)
    gdata = cls(chname)
    data = fromfile(fnames[0],gdata.fs,dtype=gdata.dtype)
    for fname in fnames[1:]:
        data = np.r_[data,fromfile(fname,gdata.fs,dtype=gdata.dtype)]
    data = _check_nan(data)        
    return data


def _check_filesize(cls,fnames,chname):
    ''' Check lack of data in files
    
    Parameters
    ----------
    fnames : list of str
        list of file names
    chname : str
        channel name
        
    Returns
    -------
    Bool
    '''    
    import os
    fsize = [_getsize(path) for path in fnames]
    gdata = cls(chname)
    size_ = [gdata.byte*gdata.fs*60 for i in range(len(fnames))]
    ans = np.array(fsize)==np.array(size_)
    #
    if fsize!=size_:
        print('[Warning] detect lack of data')
        idxs = np.where(ans==False)[0]
        lack_of_data = [fnames[idx] for idx in idxs]
        lack = [fsize[idx] for idx in idxs]
        for i,fname in enumerate(lack_of_data):
            print(' - ',fname,lack[i])
    else:
        return True



def fromfile(fname,fs,dtype=None):
    ''' Read from one file
    
    Parameters
    ----------
    fname : str
        file name
    fs : int
        sampling frequency

    Returns
    -------
    data : numpy.array
        1 minutes timeseries
    '''
    try:
        data = np.fromfile(fname,dtype=dtype)
    except:
        data = np.zero([60*fs])
        data[:] = np.nan
    return data


def _check_nan(data):
    ''' Check nan-data in the file
    
    Parameters
    ----------
    data : numpy.array
        un-checked data

    Returns
    -------
    data : numpy.array
        checked data    
    '''
    if True in np.isnan(data):
        idx = np.where(np.isnan(data)==True)[0]
        print('[Warning] found nan value. zero padding')
        print('\t Continuing..')
        data[idx] = np.nan
    else:
        pass    
    return data




def cliptime(data,start,tlen,fs):
    ''' Clip data 
    
    Parameters
    ----------
    data : numpy.array
        time series data.
    start : int
        start gps time.second
    tlen : int
        time length. second
    fs : int
        sampling frequency.

    Returns
    -------
    data : numpy.array
        cliped data
    '''
    _s = 60*(start/60)+18 
    _e = 60*((start+tlen)/60)+18
    idx = [(start-_s)*fs,(start+tlen-_s)*fs]
    data = data[idx[0]:idx[1]]
    return data




def _getsize(path):
    ''' Get size of file
    
    Parameter
    ---------
    path : str
        path to files

    Returns
    -------
    size : int
        size of file
    '''
    import os
    try:
        size = os.path.getsize(path)
    except Exception as e:
        print(e)
        size = 0
    return size
