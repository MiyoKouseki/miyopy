#
#! coding:utf-8
import numpy as np
from astropy import units as u
from ..time import to_JSTdatetime,to_GPStime
import logging

Hz = 1
byte = 1

datatype = {
    # Data Loction   : [ Sampling Frequncy, Data Size, c2V or Strain]
    '/NAS/cRIO01_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO02_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/cRIO03_data/':[(200*Hz,4*byte), np.int32, 1.25e-6*u.Volt],
    '/NAS/PXI1_data/5000Hz/':[(5000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/NAS/PXI1_data/50000Hz/':[(50000*Hz,4*byte), np.int32, 5.525e-9*u.Volt],
    '/data1/PHASE/50000Hz/':[(200*Hz,8*byte),np.float64,1],
    '/data2/CLIO/LIN/':[(200*Hz,8*byte), np.float64, 1],
    '/data2/CLIO/SHR/':[(200*Hz,8*byte), np.float64, 1],
    }
    
fname_fmt={
    # ChannelName:Format,Mustreplace<fname>.
    'X500_TEMP':'/NAS/cRIO01_data/<fname>.AD00',
    'X500_HUMD':'/NAS/cRIO01_data/<fname>.AD01',
    'X500_BARO':'/NAS/cRIO01_data/<fname>.AD02',
    'X500_VACU':'/NAS/cRIO01_data/<fname>.AD03',
    'X500_04':'/NAS/cRIO01_data/<fname>.AD04',
    'X500_05':'/NAS/cRIO01_data/<fname>.AD05',
    'X500_06':'/NAS/cRIO01_data/<fname>.AD06',
    'X500_07':'/NAS/cRIO01_data/<fname>.AD07',
    'X2000_TEMP':'/NAS/cRIO02_data/<fname>.AD00',
    'X2000_HUMD':'/NAS/cRIO02_data/<fname>.AD01',
    'X2000_BARO':'/NAS/cRIO02_data/<fname>.AD02',
    'X2000_VACU':'/NAS/cRIO02_data/<fname>.AD03',
    'X2000_04':'/NAS/cRIO02_data/<fname>.AD04',
    'X2000_05':'/NAS/cRIO02_data/<fname>.AD05',
    'X2000_06':'/NAS/cRIO02_data/<fname>.AD06',
    'X2000_07':'/NAS/cRIO02_data/<fname>.AD07',
    #
    'X1500_TR240velEW'	:'/NAS/cRIO03_data/<fname>.AD00',
    'X1500_01'	:'/NAS/cRIO03_data/<fname>.AD01',
    'X1500_TR240velNS':'/NAS/cRIO03_data/<fname>.AD02',
    'X1500_TR240velUD':'/NAS/cRIO03_data/<fname>.AD03',
    'X1500_TR240posEW':'/NAS/cRIO03_data/<fname>.AD04',
    'X1500_TR240posNS':'/NAS/cRIO03_data/<fname>.AD05',
    'X1500_TR240posUD':'/NAS/cRIO03_data/<fname>.AD06',
    'X1500_07':'/NAS/cRIO03_data/<fname>.AD07',
    'X1500_CMG3TvelEW':'/NAS/cRIO03_data/<fname>.AD08',
    'X1500_CMG3TvelNS':'/NAS/cRIO03_data/<fname>.AD09',
    'X1500_CMG3TvelUD':'/NAS/cRIO03_data/<fname>.AD10',
    'X1500_11':'/NAS/cRIO03_data/<fname>.AD11',
    'X1500_CMG3TposEW':'/NAS/cRIO03_data/<fname>.AD12',
    'X1500_CMG3TposNS':'/NAS/cRIO03_data/<fname>.AD13',
    'X1500_CMG3TposUD':'/NAS/cRIO03_data/<fname>.AD14',
    'X1500_15':'/NAS/cRIO03_data/<fname>.AD15',
    #
    'PD_PWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD00',
    'PD_SWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD01',
    'PD_INPUTWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD02',
    'PD_ABSORP_PXI01_50k':'/NAS/PXI1_data/50000Hz/<fname>.AD03',
    'PD_PWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD00',
    'PD_SWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD01',
    'PD_INPUTWAVE_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD02',
    'PD_ABSORP_PXI0_5k':'/NAS/PXI1_data/5000Hz/<fname>.AD03',
    'CALC_PHASE':'/data1/PHASE/50000Hz/<fname>.PHASE',
    'CALC_STRAIN':'/data1/PHASE/50000Hz/<fname>.STRAIN',
    'CALC_ZOBUN':'/data1/PHASE/50000Hz/<fname>.ZOBUN',
    'CALC_SQRT':'/data1/PHASE/50000Hz/<fname>.SQRT',
    'CLIO_CALC_STRAIN_LIN':'/data2/CLIO/LIN/<fname>.LIN',
    'CLIO_CALC_STRAIN_SHR':'/data2/CLIO/SHR/<fname>.SHR',
    }

date_fmt = '%Y/%m/%d/%H/%y%m%d%H%M'    

    
class NoChannelNameError(Exception):
    def __init__(self,chname):
        self.chname = chname
        keys = [key for key in fname_fmt.keys() if self.chname in key]
        if len(keys)==0:
            keys = fname_fmt.keys()
        self.text = '\n Is it in these channel name?'
        keys.sort(reverse=False)
        for key in keys:
            self.text += '\n- '+key
            
    def __str__(self):
        return "Invalid channel name '{0};{1}'".format(self.chname,self.text)


    
class gifdata(object):
    def __init__(self,chname,):
        self.chname = chname
        DataLocation = fname_fmt[self.chname].split('<fname>')[0]
        info = datatype[DataLocation]
        self.dtype = info[1]
        self.byte = info[0][1]
        self.fs = info[0][0]
        self.c2V = info[2]        
            

    def path_to_file(self,date,prefix='/Users/miyo/Dropbox/KagraData/gif/'):    
        ''' Return path to file
        
        Parameter
        ---------
        gpstime: int
            start gps time.
        tlen: int
            time length.
        prefix: str
            location where gif binary data is saved.

        Return
        ------
        path : str
            path to file
        '''
        
        if isinstance(date,int):            
            assert (date%60)==18,'{0}%60={1}'.format(date,date%60)
            date = to_JSTdatetime(date)
        elif isinstance(date,date):
            pass
        
        date_str = date.strftime(date_fmt)
        path = prefix + fname_fmt[self.chname].replace('<fname>',date_str)
        return path
    
    
    @staticmethod
    def read(gps,tlen,chname,**kwargs):
        ''' Read gif data
        
        Parameter
        ---------
        gps : int
            start gps time.
        tlen : int
            time length.
        chname : str
            channel name.
        '''
        gdata = gifdata(chname)
        fnames = get_filelist(gps,tlen,chname,**kwargs)    
        data = fromfiles(fnames,chname)
        data = cliptime(data,gps,tlen,gdata.fs)
        data = data*gdata.c2V
        return data       
    
    
    def _check_chname(self):
        ''' check wheter channel name exit or not.        
        
        '''        
        if not self.chname in fname_fmt.keys():
            raise NoChannelNameError(self.chname)
        
        
    def _get_info(self):
        DataLocation = fname_fmt[self.chname].split('<fname>')[0]
        info = datatype[DataLocation]
        self.dtype = info[1]
        self.byte = info[0][1]
        self.fs = info[0][0]
        self.c2V = info[2]        

        
    def _get_fname(self):
        date = to_JSTdatetime(int(self.t0))
        date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
        self.fname = fname_fmt[self.chname].replace('<fname>',date_str)        
        

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
    gdata = gifdata(chname)    
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
    check_filesize(fnames,chname)    
    gdata = gifdata(chname)
    data = _fromfile(fnames[0],gdata.fs,dtype=gdata.dtype)
    for fname in fnames[1:]:
        data = np.r_[data,_fromfile(fname,gdata.fs,dtype=gdata.dtype)]
    data = check_nan(data,fnames,chname)        
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
    gdata = gifdata(chname)
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

    
def _read(gps,tlen,chname,**kwargs):    
    ''' Read gif data
        
    Parameter
    ---------
    gps : int
        start gps time.
    tlen : int
        time length.
    chname : str
        channel name.
    '''
    gdata = gifdata(chname)        
    fnames = get_filelist(gps,tlen,chname,**kwargs)    
    data = fromfiles(fnames,chname)
    data = cliptime(data,gps,tlen,gdata.fs)
    data = data*gdata.c2V
    return data


def cliptime(data,gps,tlen,fs):
    s_ = 60*(gps/60)+18 
    e_ = 60*((gps+tlen)/60)+18
    idx = [(gps-s_)*fs,(gps+tlen-s_)*fs]
    data = data[idx[0]:idx[1]]
    return data





        
