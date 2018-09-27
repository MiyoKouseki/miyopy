#
#! coding:utf-8
import numpy as np 
    

def readdump(start,end,chname,**kwargs):
    pc_system = _check_system()
    prefix,prefix_gif,prefix_kagra = _get_prefix(pc_system)
    
    try:
        fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
        with open(fname,'rb') as f:
            value = np.load(f)
    except Exception as e:
        print(e)
        if 'K1' not in chname:
            value = _download_gifdata(start,end,chname=chname,
                                      prefix=prefix,prefix_gif=prefix_gif,**kwargs)
        else:
            value = _download_kagradata(start,end,chname=chname,prefix=prefix_kagra)
    return value


def _download_gifdata(start,end,chname='CALC_STRAIN',
                     prefix=None,prefix_gif=None,**kwargs):
    from miyopy.timeseries import TimeSeries as ts    
    print('taking data from gif')
    data = ts.read(start,end-start,chname,prefix=prefix_gif,**kwargs)
    value = data.value
    print('done')
    print('saving data')
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print(fname)
    _savedump(fname,value)
    return value

    
def _download_kagradata(start,end,chname=None,prefix=None,**kwargs):
    '''
    '''
    from gwpy.timeseries import TimeSeries    
    if chname==None:
        raise ValueError('Invalid chname name; {}'.format(chname))

    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print('data taking {}'.format(chname))
    data = TimeSeries.fetch(chname,
                            start, end,
                            host='10.68.10.121', port=8088)
    data =  data.value 
    print('done')
    print('save')

    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    _savedump(fname,data)
    return data


def _savedump(fname,value):
    with open(fname,'w') as f:
        np.save(f,value)
    print('done')
    return value

def _check_system():
    import platform
    import socket    
    system = platform.system()
    hostname = socket.gethostname()        
    return system

def _get_prefix(pc_system):
    if pc_system=='Darwin':
        prefix ='/Users/miyo/Dropbox/KagraData/dump/'
        prefix_gif='/Users/miyo/Dropbox/KagraData/gif/'
        prefix_kagra='./'
    elif pc_system=='Linux':
        if hostname=='z400-001':
            prefix='/home/miyo/Dropbox/KagraData/dump/'
            prefix_gif='/home/miyo/Dropbox/KagraData/gif/'
        else:
            prefix = './'
            prefix_gif = './'
            prefix_kagra='./'                    
    else:
        raise UserWarning('Invalid computer pc_system; {}'.format(pc_system))
    
    return prefix,prefix_gif,prefix_kagra
