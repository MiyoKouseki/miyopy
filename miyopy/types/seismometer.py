#
#! coding:utf-8

import miyopy.io.reader as reader
import numpy as np


def clockwise_Zaxis(theta):
    theta = np.deg2rad(-1.0*float(theta)) # minus is clockwise
    mat = np.array([
        [np.cos(theta),-1*np.sin(theta),0.],
        [np.sin(theta),np.cos(theta),0.],
        [0.,0.,1.]
    ])
    return mat


class Seismometer(object):
    def __init__(self,t0,tlen,name='EX1',theta=0.0,plot=True,detrend=True,title='./tmp_'):        
        self.name = name
        self.start = t0
        self.tlen = tlen
        self._getEWNSZ(title)
        if 'X1500_TR240' == self.name:
            theta = -30+theta
            self._rotate(theta)
        else:
            theta = 180+30+theta
            self._rotate(theta)
        
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
        
    def _rotate(self,theta=0.0):
        '''
        ex1_ns(theta=0) = y 
        '''
        self._theta = theta
        data = np.array([self.x.timeseries, self.y.timeseries, self.z.timeseries]).T
        data = np.dot(data,clockwise_Zaxis(theta))
        self.x.timeseries = data[:,0]
        self.x._name = self.name+'_'+'EW'
        self.y.timeseries = data[:,1]
        self.y._name = self.name+'_'+'NS'        
        self.z.timeseries = data[:,2]
        self.z._name = self.name+'_'+'Z'
        
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
        
