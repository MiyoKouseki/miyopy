import numpy as np
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
start = tconvert('Sep 24 2019 21:55:00 JST')
end = tconvert('Sep 24 2019 22:05:00 JST')
#start = tconvert('Sep 25 2019 15:28:30 JST')
#end = tconvert('Sep 25 2019 15:28:31 JST')

def on_filt(swstat):
    is_on = lambda num,n:n+1 if int(num,0)>>n&1 else False
    on_filter =  [is_on(swstat,i) for i in range(0,10)]
    return filter(lambda x:x is not False,on_filter)

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
#                0b 1001110000000000
#                0b 1001000000000000
#                0b 1011110000000110
    if bin((swstat&mask_out)^default) == '0b0':
        return 'DEFAULT_OUT',on_filt(bin((swstat&mask_filt)))
    elif bin((swstat&mask_out)^limit) == '0b0':
        return 'LIMIT_OUT',on_filt(bin((swstat&mask_filt)))
    elif bin((swstat&mask_out)^offset) == '0b0':
        return 'OFFSET_OUT',on_filt(bin((swstat&mask_filt)))    
    elif (~(swstat>>12)&1):
        return 'NO_OUT',on_filt(bin((swstat&mask_filt)))
    elif (~(swstat>>10)&1):
        return 'NO_INPUT',on_filt(bin((swstat&mask_filt)))    
    else:
        pass
    return bin(swstat)


if __name__=='__main__':
    with open('./k1visetmxtepics/swstat.txt','r') as f:
        channels = map(lambda x:x.replace('\n',''),f.readlines())
    
    from Kozapy.utils import filelist
    #source = filelist(start,end,trend='full',place='kamioka')
    source = 'K-K1_C-1253435392-32.gwf'
    data = TimeSeriesDict.read(source,channels=channels,nproc=2)    
    for d in data.values():
        _min = int(d.min().value)
        _max = int(d.max().value)
        if _min == _max:
            print '{0:50s}: {1}'.format(d.name,filt_status(_min))
        else:
            raise ValueError('Detect filter change!')
   
    
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
