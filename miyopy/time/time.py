
from astropy.time import Time
from datetime import datetime as dt


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
    print gps
    gps = Time(gps).gps
    return int(gps)
