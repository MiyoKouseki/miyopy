import numpy as np
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from Kozapy.utils import filelist

def on_fm(swstat):
    ''' return number of turned on filter.
    '''
    is_on = lambda num,n:n+1 if int(num,0)>>n&1 else False
    _on =  [is_on(swstat,i) for i in range(0,10)]
    _on = filter(lambda x:x is not False,_on)
    _on = map(str,_on)
    return '['+','.join(_on)+']'

def filt_status(swstat):
    '''
    mask_out : check except FMs
    default : IN,OUT,DEC is turned on
    limit : IN,OUT,DEC,LIMIT is turned on
    '''
    #               D LOO
    #               E IUFI
    #               C MTFN
    mask_noout = 0b00001000000000000    
    mask_out   = 0b11111110000000000
    mask_filt  = 0b00000001111111111
    default    = 0b01001010000000000
    limit      = 0b01011010000000000
    offset     = 0b01001110000000000    
    if bin((swstat&mask_out)^default) == '0b0':
        return 'DEFAULT_OUT,'+on_fm(bin((swstat&mask_filt)))
    elif bin((swstat&mask_out)^limit) == '0b0':
        return 'LIMIT_OUT,'+on_fm(bin((swstat&mask_filt)))
    elif bin((swstat&mask_out)^offset) == '0b0':
        return 'OFFSET_OUT,'+on_fm(bin((swstat&mask_filt)))
    elif (~(swstat>>12)&1):
        return 'NO_OUT,'+on_fm(bin((swstat&mask_filt)))
    elif (~(swstat>>10)&1):
        return 'NO_INPUT,'+on_fm(bin((swstat&mask_filt)))
    else:
        pass
    return ','.join(bin(swstat))


if __name__=='__main__':
    import argparse   
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('hoge', help='hoge')    
    args = parser.parse_args() 
    hoge = args.hoge
    # ----------------------------------------------
    if hoge == 'sc1_0':
        start = tconvert('Sep 06 2019 00:30:00 JST')
    if hoge == 'sc1_1':
        start = tconvert('Sep 06 2019 01:40:00 JST')
    if hoge == 'sc1_2':
        start = tconvert('Sep 06 2019 02:52:00 JST')
    if hoge == 'sc1_3':
        start = tconvert('Sep 06 2019 03:10:00 JST')
    if hoge == 'sc1_4':
        start = tconvert('Sep 06 2019 03:22:00 JST')
    if hoge == 'sc1_5':
        start = tconvert('Sep 06 2019 03:42:00 JST')
    # ----------------------------------------------
    if hoge == 'sc2_0':
        start = tconvert('Sep 17 2019 05:26:00 JST')
    if hoge == 'sc2_1':
        start = tconvert('Sep 17 2019 05:39:00 JST')
    # ----------------------------------------------
    if hoge == 'sc3_0':
        start = tconvert('Sep 23 2019 20:43:00 JST')
    if hoge == 'sc3_1':
        start = tconvert('Sep 23 2019 21:09:00 JST')
    if hoge == 'sc3_2':
        start = tconvert('Sep 23 2019 21:22:00 JST')
    if hoge == 'sc3_3':
        start = tconvert('Sep 23 2019 21:34:00 JST')
    if hoge == 'sc3_4':
        start = tconvert('Sep 23 2019 21:46:00 JST')
    if hoge == 'sc3_5':
        start = tconvert('Sep 23 2019 22:35:00 JST')
    if hoge == 'sc3_6':
        start = tconvert('Sep 23 2019 22:46:00 JST')
    if hoge == 'sc3_7':
        start = tconvert('Sep 23 2019 23:25:00 JST')
    if hoge == 'sc3_8':
        start = tconvert('Sep 23 2019 20:57:00 JST')
    # ----------------------------------------------
    if hoge == 'sc4_0':
        start = tconvert('Sep 24 2019 21:55:00 JST')
    if hoge == 'sc4_1':
        start = tconvert('Sep 24 2019 23:20:00 JST')
    if hoge == 'sc4_2':
        start = tconvert('Sep 25 2019 00:11:00 JST')
    if hoge == 'sc4_3':
        start = tconvert('Sep 25 2019 00:53:00 JST')
    if hoge == 'sc4_4':
        start = tconvert('Sep 25 2019 01:25:00 JST')
    if hoge == 'sc4_5':
        start = tconvert('Sep 24 2019 22:08:00 JST')
    if hoge == 'sc4_6':
        start = tconvert('Sep 24 2019 22:42:00 JST')
    # 
    end = start + 1

    # Read filter names
    with open('./filtername.txt','r') as f:
        channels = map(lambda x:x.replace('\n',''),f.readlines())

    # 
    source = filelist(start,end,trend='full',place='kashiwa')
    f = open('./results/{0}.txt'.format(hoge), mode='w')
    f.write('# NAME,STATUS,[FILTER_NUMBER],GAIN,OFFSET,LIMIT'+'\n')
    for name in channels:
        names = [name+_suffix for _suffix in ['_SWSTAT','_GAIN','_OFFSET','_LIMIT']]
        data = TimeSeriesDict.read(source,names,start=start,end=end,nproc=1,
                                   format='gwf.lalframe')
        swstat = int(data[name+'_SWSTAT'].mean())
        gain = data[name+'_GAIN'].mean()
        offset = data[name+'_OFFSET'].mean()
        limit = data[name+'_LIMIT'].mean()
        txt = '{0},{1},{2:3.5e},{3:3.5e},{4:3.5e}'.format(name,filt_status(swstat),
                                                          gain,offset,limit)
        print(txt)
        f.write(txt+'\n')
    f.close()
   
    
# MEMO
# dont remove
# -> FM1  :  0
# -> FM2  :  1
# -> FM3  :  2
# -> FM4  :  3
# -> FM5  :  4
# -> FM6  :  5
# -> FM7  :  6
# -> FM8  :  7
# -> FM9  :  8
# -> FM10 :  9
# -> IN1  : 10
# -> OSET : 11
# -> OUT  : 12
# -> LIM  : 13
# -> DEC  : 15
# -> HOLD : 16
