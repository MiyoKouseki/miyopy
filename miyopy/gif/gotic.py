from numpy import (loadtxt,isclose,pi)
from datetime import datetime as dt
from astropy.time import Time

import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Kagra/Git/gwpy/')
from gwpy.timeseries import TimeSeries
from astropy import units as u
from miyopy.gif import rotate2d,gps2datestr

class GoticStrain(object):
    def __init__(self,start,end):
        start_str = gps2datestr(start)
        end_str = gps2datestr(end)
        fname = '{0}_{1}.gotic'.format(start_str,end_str)
        time, ns, ew, shear, azimuth, areal, cubic = loadtxt(fname,unpack=True)
        print fname
        start = fname.split('_')[0]
        start_datetime = dt.strptime(start, '%Y%m%d%H%M')
        t0 = Time(start_datetime).gps
        self.t0 = t0
        self.time = time + t0
        self.ns = TimeSeries(ns,t0=self.t0, dt=60*u.min,unit='strain')
        self.ew = TimeSeries(ew,t0=self.t0, dt=60*u.min,unit='strain')
        self.shear = TimeSeries(shear,t0=self.t0, dt=60*u.min,unit='strain')
        self.areal = TimeSeries(areal,t0=self.t0, dt=60*u.min,unit='strain')
        self.azimuth = TimeSeries(azimuth,t0=self.t0, dt=60*u.min,unit='strain')
        self.cubic = TimeSeries(cubic,t0=self.t0, dt=60*u.min,unit='strain')

    
class KagraStrain(GoticStrain):
    def __init__(self,start,end):
        super(KagraStrain,self).__init__(start,end)
        theta = pi/6.0
        x,y,shear = rotate2d(self.ew,self.ns,self.shear,theta)
        if not all(isclose(x.value+y.value,self.areal.value)):
            raise ValueError('Gotic result is wrong')
        self.x = x
        self.y = y
        self.shear = shear        
