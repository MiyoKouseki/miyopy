#
#! coding:utf-8

from .series import Series


class TimeSeries(Series):
    ''' Timseries class 
    This class based on Series class which have simple attribute and method for 
    handling series data.         
    
    Parameter
    ---------
    value: 'array-like'
        value of the seriese data.
    vunit: 'str','astropy.unit'
        unit od value parameter. 
    t0: int
        gps time.
    dt: float
        differential time.
    tunit:
        unit of differential time.
    name: 'str'
        name of this timeseries.
    
    '''    
    def __new__(cls, value, vunit=None, dt=None, t0=None, tunit=None,
                name=None, dtype=None, copy=True, order=None, subok=True, ndmin=0): 
        
        new = super(TimeSeries, cls).__new__(cls, value, vunit=vunit, dx=dt,
                                             x0=t0,dtype=dtype,
                                             copy=copy, order=order, subok=subok,
                                             ndmin=ndmin)
        if copy:
            new = new.copy()

        new.nlen = len(value)        
        return new

    t0 = Series.x0
    dt = Series.dx

    
if __name__=='__main__':
    value=[0,1,2,3,4,5]#*u.m/u.s
    dt = 0.1
    t0 = 1212143472
    q = TimeSeries(value,dt=dt,t0=t0,vunit='um/s',tunit='us',name='hoge')
    #print q
    #print q.time
