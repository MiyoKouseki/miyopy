#
#! coding:utf-8

#import miyopy.io.reader as reader
import numpy as np
from gwpy.timeseries import TimeSeries


def clockwise_Zaxis(theta):
    theta = np.deg2rad(-1.0*float(theta)) # minus is clockwise
    mat = np.array([
        [np.cos(theta),-1*np.sin(theta),0.],
        [np.sin(theta),np.cos(theta),0.],
        [0.,0.,1.]
    ])
    return mat


class SeismoMeter(object):
    def __init__(self,ew,ns,ud):
        self.ew = ew
        self.ns = ns
        self.ud = ud
        self.theta = 0.0
        self.dt = ns.dt
        self.unit = ns.unit
        self.t0 = ns.t0

    def rotate(self,theta):
        '''
        '''
        data = np.array([self.ew, self.ns, self.ud]).T
        data = np.dot(data,clockwise_Zaxis(theta))
        self.x = TimeSeries(data[:,0],unit=self.unit,dt=self.dt,
                            t0=self.t0,name=self.ew.name)#,channel=self.ew.channel)
        self.y = TimeSeries(data[:,1],unit=self.unit,dt=self.dt,
                            t0=self.t0,name=self.ns.name)#,channel=self.ns.channel)
        self.z = TimeSeries(data[:,2],unit=self.unit,dt=self.dt,
                            t0=self.t0,name=self.ud.name)#,channel=self.ud.channel)
        
    def __add__(self,value):
        self.x.timeseries += value
        self.y.timeseries += value
        self.z.timeseries += value
        return self

    
    def __sub__(self,value):
        if isinstance(value,float):
            self.x.timeseries -= value
            self.y.timeseries -= value
            self.z.timeseries -= value
        if isinstance(value,Seismometer):
            print type(value)
            self.x.timeseries -= value.x.timeseries
            self.y.timeseries -= value.y.timeseries
            self.z.timeseries -= value.z.timeseries
        return self

    
    def __div__(self,value):
        self.x.timeseries /= value
        self.y.timeseries /= value
        self.z.timeseries /= value
        return self

    
    def __mul__(self,value):
        self.x.timeseries *= value
        self.y.timeseries *= value
        self.z.timeseries *= value
        return self

    def bandpass(self,lowcut=1e-3,highcut=1e0,order=1):
        self.x.bandpass(lowcut,highcut,order)
        self.y.bandpass(lowcut,highcut,order)
        self.z.bandpass(lowcut,highcut,order)
        


        
def _getEWNSZ(self,title):
    if 'X1500_TR240' == self.name:
        self.x = reader.gif.readGIFdata(self.start,
                                        self.tlen,
                                        'X1500_TR240velEW',
                                        plot=False,detrend=True,
                                        name='X1500_TR_X',
                                        title=title,
                                            )    
        self.y = reader.gif.readGIFdata(self.start,
                                        self.tlen,
                                        'X1500_TR240velNS',
                                        plot=False,detrend=True,
                                        name='X1500_TR_Y',   
                                        title=title,
                                            )    
        self.z = reader.gif.readGIFdata(self.start,
                                        self.tlen,
                                        'X1500_TR240velUD',
                                        plot=False,detrend=True,
                                        name='X1500_TR_Z',   
                                        title=title,
                                            )    
    else:
        channels = ['K1:PEM-{0}_SEIS_WE_SENSINF_OUT16'.format(self.name),
                        'K1:PEM-{0}_SEIS_NS_SENSINF_OUT16'.format(self.name),
                        'K1:PEM-{0}_SEIS_Z_SENSINF_OUT16'.format(self.name)]
        self.x,self.y,self.z = reader.kagra.readKAGRAdata(self.start,
                                                          self.tlen,
                                                          channels,
                                                          title=title,
                                                              )        
        
