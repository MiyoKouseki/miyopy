#
#! coding:utf-8

from astropy.units import Quantity
from miyopy.io._reader import get_reader

class TimeSeriesBase(Quantity):
    def __new__(cls, value, unit=None,  # Quantity attrs
                name=None, epoch=None, channel=None,  # new attrs
                dtype=None, copy=True, subok=True,  # ndarray attrs
                order=None, ndmin=0, **kwargs):
        
        new = super(TimeSeriesBase, cls).__new__(cls, value,
                                                 unit=unit)
        if channel is not None:
            print Channel
        return new

    
    
    
    @classmethod
    def read(cls, channel,*args, **kwargs):
        if 'K1' in channel:
            fmt = 'kagra'
        else:
            fmt = 'gif'
        reader = get_reader(fmt, cls)
        data = reader(kwargs['t0'],kwargs['tlen'],channel)
        return cls(data,*args,**kwargs)

class TimeSeries(TimeSeriesBase):    
    pass

if __name__ == '__main__':
    ts = TimeSeries.read('K1:PEM-IY0_SEIS_NS_SENSINF_OUT16',t0=1207240372,tlen=2**12)
    print type(ts)
    print ts.unit
