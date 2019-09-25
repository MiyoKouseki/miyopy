import numpy as np
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert

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
    with open('./swstat.txt','r') as f:
        channels = map(lambda x:x.replace('\n',''),f.readlines())
    import ezca
    ezca = ezca.Ezca()
    for chname in channels:
        val = int(ezca.read(chname[3:]))
        print '{0:50s}: {1}'.format(chname,filt_status(val))
    
        
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
                                                                                                                
