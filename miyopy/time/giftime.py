#
#! coding:utf-8

from astropy.time import Time
from datetime import datetime as dt


def astroTime2JSTdatetime(Time):
    return dt.strptime(str(Time), '%Y-%m-%d %H:%M:%S')
    
def gps2JSTdatetime(gps):
    gps = gps + 60*60*9    
    t = Time(gps,format='gps')
    t.format = 'datetime'
    dtime = dt.strptime(str(t), '%Y-%m-%d %H:%M:%S')
    return dtime
