#
#! coding:utf-8

from .core import TimeSeriesBase


class TimeSeries(TimeSeriesBase):
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
