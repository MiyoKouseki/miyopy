#
#! coding:utf-8
import numpy as np
import traceback

from gifutils import checkParams

Hz = 1
byte = 1
#from gwpy.timeseries import TimeSeries

        
datatype = {
    # Data Loction in GIF PC  : [ Sampling Frequncy, Data Size, Integer2Voltage]
    '/NAS/cRIO01_data/'        : [(   200*Hz, 4*byte), np.int32  ,1.25e-6],  # for X500 PEM
    '/NAS/cRIO02_data/'        : [(   200*Hz, 4*byte), np.int32  ,1.25e-6],  # for X2000 PEM
    '/NAS/cRIO03_data/'        : [(   200*Hz, 4*byte), np.int32  ,1.25e-6],  # for X1500 PEM
    '/NAS/PXI1_data/5000Hz/'   : [(  5000*Hz, 4*byte), np.int32  ,5.525e-9], # for PD 
    '/NAS/PXI1_data/50000Hz/'  : [( 50000*Hz, 4*byte), np.int32  ,5.525e-9], # for PD
    '/data1/PHASE/50000Hz/'    : [(   200*Hz, 8*byte), np.float64,1],  # for Strain data of GIF
    '/data2/CLIO/LIN/'         : [(   211*Hz, 8*byte), np.float64,1],  # for Strain data of CLIO
    '/data2/CLIO/SHR/'         : [(   211*Hz, 8*byte), np.float64,1],  # for Strain data of CLIO
}

filename_format = {
    #ChannelName                   : Format , Must replace <filename>.
    'X500_TEMP'                : '/NAS/cRIO01_data/<filename>.AD00',
    'X500_HUMD'                : '/NAS/cRIO01_data/<filename>.AD01',
    'X500_BARO'                : '/NAS/cRIO01_data/<filename>.AD02',
    'X500_VACU'                : '/NAS/cRIO01_data/<filename>.AD03',
    'X500_04'                  : '/NAS/cRIO01_data/<filename>.AD04',
    'X500_05'                  : '/NAS/cRIO01_data/<filename>.AD05',
    'X500_06'                  : '/NAS/cRIO01_data/<filename>.AD06',
    'X500_07'                  : '/NAS/cRIO01_data/<filename>.AD07',        
    'X2000_TEMP'               : '/NAS/cRIO02_data/<filename>.AD00',
    'X2000_HUMD'               : '/NAS/cRIO02_data/<filename>.AD01',
    'X2000_BARO'               : '/NAS/cRIO02_data/<filename>.AD02',
    'X2000_VACU'               : '/NAS/cRIO02_data/<filename>.AD03',
    'X2000_04'                 : '/NAS/cRIO02_data/<filename>.AD04',
    'X2000_05'                 : '/NAS/cRIO02_data/<filename>.AD05',
    'X2000_06'                 : '/NAS/cRIO02_data/<filename>.AD06',
    'X2000_07'                 : '/NAS/cRIO02_data/<filename>.AD07',
    #
    'X1500_TR240velEW'	   : '/NAS/cRIO03_data/<filename>.AD00',
    'X1500_01'         	   : '/NAS/cRIO03_data/<filename>.AD01',
    'X1500_TR240velNS'     : '/NAS/cRIO03_data/<filename>.AD02',
    'X1500_TR240velUD'     : '/NAS/cRIO03_data/<filename>.AD03',
    'X1500_TR240posEW'     : '/NAS/cRIO03_data/<filename>.AD04',
    'X1500_TR240posNS'     : '/NAS/cRIO03_data/<filename>.AD05',
    'X1500_TR240posUD'     : '/NAS/cRIO03_data/<filename>.AD06',
    'X1500_07'             : '/NAS/cRIO03_data/<filename>.AD07',
    'X1500_CMG3TvelEW'     : '/NAS/cRIO03_data/<filename>.AD08',
    'X1500_CMG3TvelNS'     : '/NAS/cRIO03_data/<filename>.AD09',
    'X1500_CMG3TvelUD'     : '/NAS/cRIO03_data/<filename>.AD10',
    'X1500_11'             : '/NAS/cRIO03_data/<filename>.AD11',
    'X1500_CMG3TposEW'     : '/NAS/cRIO03_data/<filename>.AD12',
    'X1500_CMG3TposNS'     : '/NAS/cRIO03_data/<filename>.AD13',
    'X1500_CMG3TposUD'     : '/NAS/cRIO03_data/<filename>.AD14',
    'X1500_15'             : '/NAS/cRIO03_data/<filename>.AD15',    
    #    
    'PD_PWAVE_PXI01_50k'       : '/NAS/PXI1_data/50000Hz/<filename>.AD00',
    'PD_SWAVE_PXI01_50k'       : '/NAS/PXI1_data/50000Hz/<filename>.AD01', 
    'PD_INPUTWAVE_PXI01_50k'   : '/NAS/PXI1_data/50000Hz/<filename>.AD02', 
    'PD_ABSORP_PXI01_50k'      : '/NAS/PXI1_data/50000Hz/<filename>.AD03',  
    'PD_PWAVE_PXI01_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD00',  
    'PD_SWAVE_PXI01_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD01',  
    'PD_INPUTWAVE_PXI0_5k'     : '/NAS/PXI1_data/5000Hz/<filename>.AD02',  
    'PD_ABSORP_PXI0_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD03',    
    'CALC_PHASE'               : '/data1/PHASE/50000Hz/<filename>.PHASE',
    'CALC_STRAIN'               : '/data1/PHASE/50000Hz/<filename>.STRAIN',
    'CALC_ZOBUN'               : '/data1/PHASE/50000Hz/<filename>.ZOBUN',
    'CALC_SQRT'                : '/data1/PHASE/50000Hz/<filename>.SQRT',    
    'CLO_CALC_STRAIN_LIN'          : '/data2/CLIO/LIN/<filename>.LIN',
    'CLO_CALC_STRAIN_SHR'          : '/data2/CLIO/SHR/<filename>.SHR',
    }

from datetime import datetime as dt
import datetime
from datetime import date

@checkParams(dt,int,str)    
def findFiles(dtime,duration,chname,prefix='/Users/miyo/KAGRA/DATA/'):
    def getfname(dtime):        
        pass
    try:
        duration = datetime.timedelta(seconds=duration)
        end = dtime + duration
        dtime_ = []
        while True:
            dtime_ += [dtime]
            dtime += datetime.timedelta(seconds=60)
            print dtime,end
            if dtime>end:
                break
        #
        minutes = len(dtime_)
        dtime = dtime_
        #
        strftime = lambda date:date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
        getfname = lambda dtime_str:filename_format[chname].replace('<filename>',dtime_str)
        hoge = lambda fname: prefix[:-1] + fname        
        dtime_str = map(strftime,dtime)
        fname = map(getfname,dtime_str)
        fname = map(hoge,fname)
        #print fname
        #
        return fname
    except KeyError as e:
        print 'KeyError',e
        print 'example) Available Channel Name'
        for key in filename_format.keys():
            print ' - ',key
        print 'exit..'
        exit()
        return None
    except Exception as e:
        print traceback.format_exc()
        exit()
        return None
    
def fromfiles(fnames,dtype):
    ''' get numpy array from files
        
    fnameに格納されているファイルパスを順番に読み込んで、1次元のnumpy.arrayにする関数。
    Parameter
    --------------

    fname : ファイルパス。絶対パス。

    dtype : データタイプ。numpy.dtype
    '''    
    try:
        data = np.array([np.fromfile(fname,dtype=dtype) for fname in fnames])
        shape = data.shape
        data = np.resize(data, (1,shape[0]*shape[1]))[0]
        return data
    except IOError as e:
        print e
        print 'No data'
        exit()
    
def read(dtime,duration,chname):    
    '''Read binay data
    
    GIFのバイナリファイルを読み込むための関数。                
    
    Parameter
    ---------------
    
    dtime : 開始時刻。datetime,str,gpsに対応している。

    duration : データ長さ。秒。

    chname : チャンネル名。
    '''
    fname = findFiles(dtime,duration,chname)
    print fname
    print len(fname)
    #exit()
    try:
        DataLocation = filename_format[chname].split('<filename>')[0]
        info  = datatype[DataLocation]
        dtype = info[1]
        c2V   = info[2]
        data = fromfiles(fname,dtype=dtype)*c2V
        return data
    except KeyError as e:
        traceback.print_exc()
        return None
    except Exception as e:
        traceback.print_exc()
        exit()
        return None
    
def test_main():
    #data = read(dtime=1199977218,duration=121,chname='X500_HUMD')
    data = read('2018-03-26 18:00:00',1024,'X1500_00')
    print data
    #data = read(1199977218,320,'CALC_STRAIN')
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.savefig('hgoe.png')
    plt.close()
    #plt.show()
    
if __name__ == '__main__':
    #'/Users/miyo/KAGRA/GIF/data1/PHASE/50000Hz/2018/01/15/00/1801150014.STRAIN'
    #gwf_cache = '/Users/miyo/KAGRA/GIF/DATA/gwpy.cache'
    #with open(gwf_cache, 'r') as fobj:
    #    cache = Cache.fromfile(fobj)
    #
    test_main()
    exit()
    # Gwpyで読み込もうとしたらしいけど、もうこの方法は使わないことにする。
    #strain = TimeSeries.read('/Users/miyo/KAGRA/GIF/data1/PHASE/50000Hz/2018/01/15/00/1801150014.STRAIN', 'CALC_STRAIN',1198306368,1198306400,format='gif')
    print 'value[-1]',strain.value[-1]
    print 'unit',strain.unit
    print 'sample_rate',strain.sample_rate
    print 'times[-1]',strain.times[-1]
    print 't0',strain.t0
    print 'dt',strain.dt
    print 'name',strain.name
    print 'channel',strain.channel
    print 'dtype',strain.dtype
    #print 'copy',strain.copy    
    
