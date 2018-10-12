#
#! coding:utf-8
Hz = 1
byte = 1
import numpy as np

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
    def __init__(self,chname):
        self.chname = chname
        DataLocation = fname_fmt[chname].split('<filename>')[0]
        info = datatype[DataLocation]
        #date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')        
        #self.fname = fname_fmt[chname].replace('<filename>',date_str)
        self.dtype = info[1]
        self.byte = info[0][1]
        self.fs = info[0][0]
        self.c2V = info[2]
        #self.path_to_file(gps)

    #@staticmethod
    def path_to_file(self,gps,prefix='/Users/miyo/Dropbox/KagraData/gif/'):
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
            self.fname = fname_fmt[self.chname].replace('<filename>',date_str)
            path_to_file = prefix[:-1] + self.fname    
        except KeyError as e:
            print type(e),e
            for key in fname_fmt.keys():
                print key
                exit()
        return path_to_file            

                
    def readfile(self):
        pass



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
    gdata = gifdatatype(chname)
    try:
        fname = fname_fmt[chname].replace('<filename>',date_str)
    except KeyError as e:
        print type(e),e
        for key in fname_fmt.keys():
            print key
        exit()
    path_to_file = prefix[:-1] + fname
    
    return path_to_file
    
def to_JSTdatetime(jst):
    from astropy.time import Time
    from datetime import datetime as dt    
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
