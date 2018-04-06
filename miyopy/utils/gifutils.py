#
# coding:utf-8
from datetime import datetime as dt
import giftime
#from sys import exit

def convert_datetime(dtime):
    strformat = '%Y-%m-%d %H:%M:%S'
    if  isinstance(dtime,dt):
        pass
    elif isinstance(dtime,str):
        try:
            dtime     = dt.strptime(dtime,strformat)
        except ValueError as e:
            print 'DatetimeStringFormatError:',e
            dtime = None                            
    elif isinstance(dtime,int):
        dtime = giftime.gps2JSTdatetime(dtime)
    elif isinstance(dtime,Time):
        giftime.astroTime2JSTdatetime(dtime)
    else:
        dtime = None
    return dtime


def checkParams(*params) :
    import inspect
    import functools
    import itertools
    def deco(func):
        @functools.wraps(func)
        def wrapper(*funcargs,**funckwars) :
            for i,par in enumerate(zip(funcargs,params)):
                if not isinstance(par[0],par[1]):
                    #print 'Warning',func.__name__,':',par[0],'!=',par[1]
                    if params[i] == dt:
                        funcargs = list(funcargs)
                        funcargs[i] = convert_datetime(funcargs[i])
            return func(*funcargs,**funckwars)
        return wrapper
    return deco


