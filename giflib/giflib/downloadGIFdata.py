#!/usr/bin/env python
#! coding:utf-8

import numpy as np
import paramiko,scp
import os
'''
GIFの1分データファイルのなかから特定のチャンネルのファイルをダウンロードするクリプト。1つしかファイルをダウンロードしないので1分以上の時系列をみたい場合は複数回実行しないといけない。

1つのファイルの中には1つの信号が記録されていて拡張子で区別しているが、DAQが違えばファイル名がかぶるので、複数のDAQで取ったファイルを扱う場合は注意が必要。一応ファイル名が同じだったとしても、サンプリングレートが異なるのでファイル容量を比べれば区別することはできる。なのでcRIO同士だと区別はできない。(拡張子を全体で固有なものにしたほうがいい気がする...。)ただしこのスクリプトでは、ファイル名が重複すると上書きするようになっているので注意。
'''

Hz = 1
byte = 1
DataSizeInfo = {
    # Data Loction            : [ Sampling Frequncy, Data Size]
    '/NAS/cRIO01_data'        : [(   200*Hz, 4*byte), np.int32  ],  # for X500 PEM
    '/NAS/cRIO02_data'        : [(   200*Hz, 4*byte), np.int32  ],  # for X2000 PEM
    '/NAS/PXI1_data/5000Hz'   : [(  5000*Hz, 4*byte), np.int32  ],  # for PD with 5kHz sample
    '/NAS/PXI1_data/50000Hz'  : [( 50000*Hz, 4*byte), np.int32  ],  # for PD with 50kHz sample
    '/data1'                  : [(   200*Hz, 8*byte), np.float64],  # for Strain data of GIF
    '/data2'                  : [(   211*Hz, 8*byte), np.float64],  # for Strain data of CLIO
}

FileLocationFormat = {
    #ChannelName                   : Format , Must replace <filename>.
    'GIF_X500_TEMP'                : '/NAS/cRIO01_data/<filename>.AD00',
    'GIF_X500_HUMD'                : '/NAS/cRIO01_data/<filename>.AD01',
    'GIF_X500_BARO'                : '/NAS/cRIO01_data/<filename>.AD02',
    'GIF_X500_VACU'                : '/NAS/cRIO01_data/<filename>.AD03',
    'GIF_X500_04'                  : '/NAS/cRIO01_data/<filename>.AD04',
    'GIF_X500_05'                  : '/NAS/cRIO01_data/<filename>.AD05',
    'GIF_X500_06'                  : '/NAS/cRIO01_data/<filename>.AD06',
    'GIF_X500_07'                  : '/NAS/cRIO01_data/<filename>.AD07',        
    'GIF_X2000_TEMP'               : '/NAS/cRIO02_data/<filename>.AD00',
    'GIF_X2000_HUMD'               : '/NAS/cRIO02_data/<filename>.AD01',
    'GIF_X2000_BARO'               : '/NAS/cRIO02_data/<filename>.AD02',
    'GIF_X2000_VACU'               : '/NAS/cRIO02_data/<filename>.AD03',
    'GIF_X2000_04'                 : '/NAS/cRIO02_data/<filename>.AD04',
    'GIF_X2000_05'                 : '/NAS/cRIO02_data/<filename>.AD05',
    'GIF_X2000_06'                 : '/NAS/cRIO02_data/<filename>.AD06',
    'GIF_X2000_07'                 : '/NAS/cRIO02_data/<filename>.AD07',
    'GIF_PD_PWAVE_PXI01_50k'       : '/NAS/PXI1_data/50000Hz/<filename>.AD00',
    'GIF_PD_SWAVE_PXI01_50k'       : '/NAS/PXI1_data/50000Hz/<filename>.AD01', 
    'GIF_PD_INPUTWAVE_PXI01_50k'   : '/NAS/PXI1_data/50000Hz/<filename>.AD02', 
    'GIF_PD_ABSORP_PXI01_50k'      : '/NAS/PXI1_data/50000Hz/<filename>.AD03',  
    'GIF_PD_PWAVE_PXI01_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD00',  
    'GIF_PD_SWAVE_PXI01_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD01',  
    'GIF_PD_INPUTWAVE_PXI0_5k'     : '/NAS/PXI1_data/5000Hz/<filename>.AD02',  
    'GIF_PD_ABSORP_PXI0_5k'        : '/NAS/PXI1_data/5000Hz/<filename>.AD03',    
    'GIF_CALC_PHASE'               : '/data1/PHASE/50000Hz/<filename>.PHASE',
    'GIF_CALC_ZOBUN'               : '/data1/PHASE/50000Hz/<filename>.ZOBUN',
    'GIF_CALC_SQRT'                : '/data1/PHASE/50000Hz/<filename>.SQRT',    
    'CLO_CALC_STRAIN_LIN'          : '/data2/CLIO/LIN/<filename>.LIN',
    'CLO_CALC_STRAIN_SHR'          : '/data2/CLIO/SHR/<filename>.SHR',
    }

def scpDownload(fname):
    HOST = "172.16.32.201"
    PORT = "22"
    USER = "GIF"
    PSWD = "kami00"    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, port=PORT, username=USER, password=PSWD)
        with scp.SCPClient(ssh.get_transport()) as scpClient:
            try:
                print 'Please Wait. Downloading..'
                scpClient.get(fname)
                print 'Done : ',fname
                return True
            except scp.SCPException as e:
                print e.message
                return False
            
def getGIFFile(dtime='2018/01/15 00:00',chname='GIF_X500_TEMP'):
    from datetime import datetime as dt
    try: 
        dtime     = dt.strptime(dtime, '%Y/%m/%d-%H:%M')
        dtime_str = dtime.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
        fname = FileLocationFormat[chname].replace('<filename>',dtime_str)
        if fname.split('/')[-1] in os.listdir('./'): print 'Duplicate.'
        scpDownload(fname)        
    except ValueError as e:
        print e
        print 'example) 2018/01/15-00:00'
        print 'exit..'
        exit()
    except KeyError as e:
        print e
        print 'example) Available Channel Name'
        for key in FileLocationFormat.keys():
            print ' - ',key
        print 'exit..'
        exit()
        
def test_getAlldata(dtime='2018/01/15-00:00'):
    # make directory
    # download
    for chname in FileLocationFormat.keys():
        print chname
        getGIFFile(dtime,chname=chname)        
        
if __name__ == '__main__':
    #test_getAlldata(dtime='2018/01/15-00:00')
    #exit()
    import sys
    argvs = sys.argv
    if len(argvs) != 3:        
        print 'example) ./downloadGIFdata.py 2018/01/15-00:00 GIF_X500_TEMP'
        exit()
    getGIFFile(dtime=argvs[1],chname=argvs[2])       
