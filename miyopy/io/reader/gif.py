#
#! coding:utf-8
import traceback
import numpy as np
import datetime
from datetime import datetime as dt
#from sys import exit
from astropy.time import Time
from datetime import datetime as dt
from scipy import signal
#from miyopy.signal import butter_bandpass_filter
import miyopy.signal.mpfilter as mpf
from miyopy.types import Timeseries

Hz = 1
byte = 1
#from gwpy.timeseries import TimeSeries
from astropy.time import Time
        
datatype = {
    # Data Loction   : [ Sampling Frequncy, Data Size, c2V or Strain]
    '/NAS/cRIO01_data/':[(200*Hz,4*byte), np.int32, 1.25e-6],
    '/NAS/cRIO02_data/':[(200*Hz,4*byte), np.int32, 1.25e-6],
    '/NAS/cRIO03_data/':[(200*Hz,4*byte), np.int32, 1.25e-6],
    '/NAS/PXI1_data/5000Hz/':[(5000*Hz,4*byte), np.int32, 5.525e-9],
    '/NAS/PXI1_data/50000Hz/':[(50000*Hz,4*byte), np.int32, 5.525e-9],
    '/data1/PHASE/50000Hz/':[(200*Hz,8*byte),np.float64,1],
    '/data2/CLIO/LIN/':[(200*Hz,8*byte), np.float64, 1],
    '/data2/CLIO/SHR/':[(200*Hz,8*byte), np.float64, 1],
}
    
fname_fmt={
    # ChannelName:Format,Mustreplace<filename>.
    'X500_TEMP':'/NAS/cRIO01_data/<filename>.AD00',
    'X500_HUMD':'/NAS/cRIO01_data/<filename>.AD01',
    'X500_BARO':'/NAS/cRIO01_data/<filename>.AD02',
    'X500_VACU':'/NAS/cRIO01_data/<filename>.AD03',
    'X500_04':'/NAS/cRIO01_data/<filename>.AD04',
    'X500_05':'/NAS/cRIO01_data/<filename>.AD05',
    'X500_06':'/NAS/cRIO01_data/<filename>.AD06',
    'X500_07':'/NAS/cRIO01_data/<filename>.AD07',
    'X2000_TEMP':'/NAS/cRIO02_data/<filename>.AD00',
    'X2000_HUMD':'/NAS/cRIO02_data/<filename>.AD01',
    'X2000_BARO':'/NAS/cRIO02_data/<filename>.AD02',
    'X2000_VACU':'/NAS/cRIO02_data/<filename>.AD03',
    'X2000_04':'/NAS/cRIO02_data/<filename>.AD04',
    'X2000_05':'/NAS/cRIO02_data/<filename>.AD05',
    'X2000_06':'/NAS/cRIO02_data/<filename>.AD06',
    'X2000_07':'/NAS/cRIO02_data/<filename>.AD07',
    #
    'X1500_TR240velEW'	:'/NAS/cRIO03_data/<filename>.AD00',
    'X1500_01'	:'/NAS/cRIO03_data/<filename>.AD01',
    'X1500_TR240velNS':'/NAS/cRIO03_data/<filename>.AD02',
    'X1500_TR240velUD':'/NAS/cRIO03_data/<filename>.AD03',
    'X1500_TR240posEW':'/NAS/cRIO03_data/<filename>.AD04',
    'X1500_TR240posNS':'/NAS/cRIO03_data/<filename>.AD05',
    'X1500_TR240posUD':'/NAS/cRIO03_data/<filename>.AD06',
    'X1500_07':'/NAS/cRIO03_data/<filename>.AD07',
    'X1500_CMG3TvelEW':'/NAS/cRIO03_data/<filename>.AD08',
    'X1500_CMG3TvelNS':'/NAS/cRIO03_data/<filename>.AD09',
    'X1500_CMG3TvelUD':'/NAS/cRIO03_data/<filename>.AD10',
    'X1500_11':'/NAS/cRIO03_data/<filename>.AD11',
    'X1500_CMG3TposEW':'/NAS/cRIO03_data/<filename>.AD12',
    'X1500_CMG3TposNS':'/NAS/cRIO03_data/<filename>.AD13',
    'X1500_CMG3TposUD':'/NAS/cRIO03_data/<filename>.AD14',
    'X1500_15':'/NAS/cRIO03_data/<filename>.AD15',
    #
    'PD_PWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<filename>.AD00',
    'PD_SWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<filename>.AD01',
    'PD_INPUTWAVE_PXI01_50k':'/NAS/PXI1_data/50000Hz/<filename>.AD02',
    'PD_ABSORP_PXI01_50k':'/NAS/PXI1_data/50000Hz/<filename>.AD03',
    'PD_PWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<filename>.AD00',
    'PD_SWAVE_PXI01_5k':'/NAS/PXI1_data/5000Hz/<filename>.AD01',
    'PD_INPUTWAVE_PXI0_5k':'/NAS/PXI1_data/5000Hz/<filename>.AD02',
    'PD_ABSORP_PXI0_5k':'/NAS/PXI1_data/5000Hz/<filename>.AD03',
    'CALC_PHASE':'/data1/PHASE/50000Hz/<filename>.PHASE',
    'CALC_STRAIN':'/data1/PHASE/50000Hz/<filename>.STRAIN',
    'CALC_ZOBUN':'/data1/PHASE/50000Hz/<filename>.ZOBUN',
    'CALC_SQRT':'/data1/PHASE/50000Hz/<filename>.SQRT',
    'CLIO_CALC_STRAIN_LIN':'/data2/CLIO/LIN/<filename>.LIN',
    'CLIO_CALC_STRAIN_SHR':'/data2/CLIO/SHR/<filename>.SHR',
}

    
class gifdatatype(object):
    def __init__(self,chname,t0):
        self.chname = chname
        self.t0 = t0
        DataLocation = fname_fmt[chname].split('<filename>')[0]
        info = datatype[DataLocation]        
        self.dtype = info[1]
        self.byte = info[0][1]
        self.fs = info[0][0]
        self.c2V = info[2]
        self.get_path_to_file(t0)

        
    def get_path_to_file(self):
        '''ファイルがある場所を調べる関数

        Parameter
        ---------
        gpstime: int
            開始時刻。GPS時間で指定。
        tlen: int
            長さ。秒で指定。
        chname:str
            チャンネル名。fname_fmtで指定されている名前を指定。
        prefix: str
            GIFデータが保存されているローカルディレクトリ。
        '''        
        assert (gps%60)==18,'{0}%60={1}'.format(gps,gps%60)
        date = to_JSTdatetime(gps)
        date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
        try:
            self.fname = fname_fmt[chname].replace('<filename>',date_str)
            self.path_to_file = prefix[:-1] + self.fname    
            return self.path_to_file            
        except KeyError as e:
            print type(e),e
            for key in fname_fmt.keys():
                print key
                exit()

                
    def readfile(self):
        pass



        
        
def to_JSTdatetime(jst):
    if isinstance(jst,str):
        jst = Time(gps).to_datetime()
    elif isinstance(jst,int):
        gps = Time(jst+3600*9, format='gps')
        jst = gps.to_datetime()
    elif isinstance(jst,dt):
        jst = Time(jst+3600*9, format='gps')
        pass
    else:
        print 
        raise NameError('Unknown data type!{0},{1}'.format(jst,type(jst)))    
    assert isinstance(jst,dt),'Please {0}, not {1}!'.format(dt,type(jst))   
    return jst


def to_GPStime(gps):
    gps = Time(gps).gps
    return int(gps)


def path_to_file(gps,chname,prefix):
    '''GPS時刻、ただし分で丸められた時刻、に対応するファイル名を返す関数。

    Parameter
    ---------
    gpstime: int
      開始時刻。GPS時間で指定。
    tlen: int
      長さ。秒で指定。
    chname:str
      チャンネル名。fname_fmtで指定されている名前を指定。
    prefix: str
      GIFデータが保存されているローカルディレクトリ。
    '''
    assert (gps%60)==18,'{0}%60={1}'.format(gps,gps%60)
    date = to_JSTdatetime(gps)
    date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
    try:
        fname = fname_fmt[chname].replace('<filename>',date_str)
    except KeyError as e:
        print type(e),e
        for key in fname_fmt.keys():
            print key
        exit()
    path_to_file = prefix[:-1] + fname
    
    return path_to_file


def findFiles(gpstime,tlen,chname,prefix='/Volumes/HDPF-UT/DATA/'):
    '''GPS時刻で指定した期間を含むファイルをローカルディレクトリから探す関数。

    GIFのファイルは１ファイル１分のファイルを日時で管理しているため、ファイルに保存されている時系列データはかならず00秒始まり。なのでファイル名を探すときは、指定した開始時刻と終了時刻を60秒で丸める必要がある。簡単な例として、2017-01-15-00:00:00のGPS時間は60で割ると18なので、とりあえず、指定した時刻を60で割った余りがそれになるように丸めればよい。ただし注意として、途中、うるう秒が入ってくるとつかえない。
    
    Parameter
    ---------
    gpstime: int
      開始時刻。GPS時間で指定。
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
    s_ = 60*(gpstime/60)+18
    e_ = 60*((gpstime+tlen)/60)+18
    fnames_gps = np.arange(s_,e_+60,60)
    fnames = [path_to_file(gps,chname,prefix) for gps in fnames_gps]
    return fnames


def fromfiles(fnames,chname,mintrend=False):
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
    DataLocation = fname_fmt[chname].split('<filename>')[0]
    info = datatype[DataLocation]
    dtype = info[1]
    byte = info[0][1]
    fs = info[0][0]
    c2V = info[2]
    #gifdata = gifdatatype(chname,)
    if mintrend==False:
        data = np.array([np.fromfile(fname,dtype=dtype) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]*shape[1]))[0]
    else:
        data = np.array([np.average(np.fromfile(fname,dtype=dtype)) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]))[0]
    try:
        return data
    except IOError as e:
        print e
        print 'No data. Did you download GIF file?'
        exit()
        
        
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
    # ------------------綺麗にしたい
    DataLocation = fname_fmt[chname].split('<filename>')[0]
    info = datatype[DataLocation]
    dtype = info[1]
    byte = info[0][1]
    fs = info[0][0]
    c2V = info[2]
    try:
        fsize = [os.path.getsize(path) for path in fnames]
        size_ = [byte*fs*60 for i in range(len(fnames))]
        ans = np.array(fsize)==np.array(size_)
    except OSError as e:
        print e
        exit()
    else:
        pass        
    # ------------------    
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

    
def read(gps,tlen,chname,fs,
         plot=False,detrend=False,
             name=None,title='./tmp_'):    
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
    fnames = findFiles(gps,tlen,chname)
    check_filesize(fnames,chname)
    if fs==(1.0/60.0):
        mintrend = True
    data = fromfiles(fnames,chname,mintrend)
    data = check_nan(data,fnames,chname)
    # ------------------綺麗にしたい
    DataLocation = fname_fmt[chname].split('<filename>')[0]
    info = datatype[DataLocation]
    dtype = info[1]
    byte = info[0][1]
    fs_ = info[0][0]
    c2V = info[2]
    s_ = 60*(gps/60)+18 
    e_ = 60*((gps+tlen)/60)+18
    # ------------------
    idx = [(gps-s_)*fs_,(gps+tlen-s_)*fs_]
    data = data[idx[0]:idx[1]]*c2V
    #print True in np.isnan(data)
    if mintrend==False and (len(data)/fs_!=tlen):
        #print len(data)
        print 'Error: tlen do not match'
        print len(data)/fs_,'!=',tlen
        exit()
    try:
        if mintrend==False:
            data = mpf.decimate(data,fs_befor=fs_,fs_after=fs)
            data = Timeseries(data,fs=fs,plot=True,detrend=detrend,name=name,title=title,unit='Voltage')
            return data
        else:
            data = Timeseries(data,fs=fs,plot=True,detrend=detrend,name=name,title=title,unit='Voltage')
            return data            
    except KeyError as e:
        traceback.print_exc()
        return None
    except Exception as e:
        traceback.print_exc()
        exit()
        return None
    
    
if __name__=="__main__":
    t0 = 1208908938+93400 # 2018-04-29T10:58:40
    print '[JST] 2018-04-29T10:58:40'
    tlen = 10
    data = readGIFdata(t0,tlen,'X500_BARO')
