from numpy import (loadtxt,isclose,pi)
from datetime import datetime as dt
from astropy.time import Time

import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Kagra/Git/gwpy/')
#from gwpy.timeseries import TimeSeries # dont use to avoid import duplication.
from astropy import units as u
from miyopy.gif import rotate2d,gps2datestr
from gwpy.time import tconvert
    
class GoticStrain(object):
    t0 = None
    time = None
    ns = None
    ew = None
    shear = None
    areal = None
    azimuth = None
    cubic = None
    
    def __init__(self):
        pass
        
    @classmethod
    def read(cls,source,**kwargs):
        '''
        
        Parameters
        ----------

        start : 

        
        end : 


        Returns
        -------
        cls
        
        '''
        fname = source
        time, ns, ew, shear, azimuth, areal, cubic = loadtxt(fname,unpack=True)
        start = fname.split('_')[0]
        start_datetime = dt.strptime(start, '%Y%m%d%H%M')        
        t0 = Time(start_datetime).gps
        start = tconvert(kwargs.pop('start',0))
        end = tconvert(kwargs.pop('end',0))
        #print start
        cls.t0 = t0 
        cls.time = time + t0
        cls.ns = TimeSeries(ns,t0=cls.t0, dt=60*u.min,unit='strain')
        cls.ew = TimeSeries(ew,t0=cls.t0, dt=60*u.min,unit='strain')
        cls.shear = TimeSeries(shear,t0=cls.t0, dt=60*u.min,unit='strain')
        cls.areal = TimeSeries(areal,t0=cls.t0, dt=60*u.min,unit='strain')
        cls.azimuth = TimeSeries(azimuth,t0=cls.t0, dt=60*u.min,unit='strain')
        cls.cubic = TimeSeries(cubic,t0=cls.t0, dt=60*u.min,unit='strain')
        # crop
        cls.ns = cls.ns.crop(start,end)
        cls.ew = cls.ew.crop(start,end)
        cls.shear = cls.shear.crop(start,end)
        cls.areal = cls.areal.crop(start,end)
        cls.azimuth = cls.azimuth.crop(start,end)
        cls.cubic = cls.cubic.crop(start,end)        
        return cls

    
    
class KagraGoticStrain(GoticStrain):
    def __init__(self,start,end):
        super(KagraGoticStrain,self).__init__(start,end)

    @classmethod
    def read(cls,source,**kwargs):
        cls = super(KagraGoticStrain, cls).read(source,**kwargs)
        
        theta = pi/6.0
        x,y,shear = rotate2d(cls.ew,cls.ns,cls.shear,theta)
        
        if not all(isclose(x.value+y.value,cls.areal.value)):
            raise ValueError('Gotic result is wrong')
        
        cls.x = x
        cls.y = y
        cls.shear = shear        
        return cls
