#
#! coding:utf-8
import numpy as np
from scipy import signal
import miyopy.plot as mpplot
from control import matlab

def tf_240():
    z = np.array([0.0, 0.0, -108.0, -161.0]) # rad/sec
    p = np.array([-0.01815+0.01799j,
                  -0.01815-0.01799j,
                  -173,
                  -196+231j,
                  -196-231j,
                  -732+1415j,
                  -732-1415j])# rad/sec
    k = 2.316e9
    #S = 1/(9.98243029518/749.1) # to have a Gain is 749.1 at f0. Please check!
    S = 1196.5
    #S = 1
    num,den  = signal.zpk2tf(z,p,S*k)
    H  = matlab.tf(num,den)    
    return H

def tf_nazo():
    z = np.array([0, 0, -434.1]) # rad/sec
    p = np.array([-0.03691+0.03712j,
                -0.03691-0.03712j,
                -371.2,
                -373.9+475.5j,
                -373.9-475.5j,
                -588.4+1508j,
                -588.4-1508j])# rad/sec
    k = 8.184*10e11
    #S = 1/(9.98243029518/749.1) # to have a Gain is 749.1 at f0. Please check!
    S = 749.1 # to have a Gain is 749.1 at f0. Please check!
    num,den  = signal.zpk2tf(z,p,S*k)
    H  = matlab.tf(num,den)
    return H

def tf_120():
    z = np.array([0, 0, -31.63,-160,-350,-3177]) # rad/sec
    p = np.array([-0.03614+0.037059j,
                  -0.03614-0.037059j,
                  -32.55,
                  -142,
                  -364+404j,
                  -364-404j,
                  -1260,
                  -4900+5200j,
                  -4900-5200j,
                  -7100+1700j,
                  -7100-1700j])# rad/sec
    k = 8.31871*10e17
    #S = 1202.5 # to have a Gain is 749.1 at f0. Please check!
    S=1.0/10.0
    num,den  = signal.zpk2tf(z,p,S*k)
    H  = matlab.tf(num,den)
    #print H
    return H


class Timeseries(object):
    def __init__(self,value,name='None',
                 fs=8,t0=None,plot=False,
                 unit=None,detrend=True,
                 title='./tmp_'):
        self._fs = fs
        self._unit = unit
        self._name = name
        self._t0 = t0
        self._dt = 1.0/self._fs
        self.timeseries = value
        self._V2Unit()        
        if plot:
            self._plot(title)
        if detrend*plot:
            self._detrend(title)            
        if detrend:
            self.timeseries_detrend = signal.detrend(self.timeseries)

    def _V2Unit(self):
        print self._name
        if self._name==None:
            pass 
        elif 'pressure' in self._name:
            if '500' in self._name:
                V2hPa = lambda y:y/-2.0/5.0*(1100.0-800.0)+800.0
            else:                    
                V2hPa = lambda y:y/2.0/5.0*(1100.0-800.0)+800.0        
            self.timeseries = V2hPa(self.timeseries)
        elif 'TR' in self._name:            
            #b,a = tf_240()
            #print b,a
            #self.timeseries = signal.filtfilt(b, a, self.timeseries)
            #print self.timeseries
            #self.timeseries = self.timeseries/1196.5
            pass
        else:
            pass
        
    def _detrend(self,title):
        import matplotlib.pyplot as plt
        fname = '{0}DetrendTimeseries_{1}.png'.format(title,self._name)
        print fname
        #print self.timeseries[0]
        value = self.timeseries #- self.timeseries[0]
        value_detrend = signal.detrend(value)
        trend = value - value_detrend
        plt.plot(self._time,value,label='value{0:+3f}'.format(self.timeseries[0]))
        plt.plot(self._time,value_detrend,label='detrend')
        plt.plot(self._time,trend,label='trend')
        plt.ylabel('Value [a.u.]')
        plt.xlabel('Time [sec]')
        plt.legend()
        plt.title(fname)            
        plt.savefig(fname)
        plt.close()

    def _plot(self,title):
        import matplotlib.pyplot as plt
        fname = '{0}Timeseries_{1}.png'.format(title,self._name)
        print fname
        value = self.timeseries #- self.timeseries[0]
        plt.plot(self._time,value,label='value')
        plt.ylabel('Value [a.u.]')
        plt.xlabel('Time [sec]')
        plt.legend()
        plt.title(fname)            
        plt.savefig(fname)
        plt.close()
        

        
    @property
    def timeseries(self):
        return self._timeseries

    
    @property
    def psd(self):
        return self._psd

    
    @property
    def csd(self):
        return self._csd

    
    @timeseries.setter
    def timeseries(self,value):
        self._timeseries = value
        self._nlen = len(self._timeseries)
        self._tlen = self._nlen/self._fs
        self._time = np.arange(self._tlen*self._fs)/self._fs

        
    @psd.setter
    def psd(self,value):
        self._psd = value   

        
    @csd.setter
    def csd(self,value):
        self._csd = value
        self._ksd,self._qsd = self._csd.real,self._csd.imag

        
    def _getTimeseries(self,data_from='txt'):
        if data_from == 'txt':
            self.timeseries = np.loadtxt(self._filepath)
        elif data_from == 'gwf':
            gwf_cache = '/Users/miyo/Documents/KAGRA/data/frames/K-K1_C.iKAGRA.cache'
            with open(gwf_cache, 'r') as fobj:
                cache = Cache.fromfile(fobj)
            data = TimeSeries.read(cache,self._channelname,self._t0,self._t0+self._tlen)
            self.timeseries = data.value
        elif data_from == 'gif':
            dtime = mptime.gps2JST(self._t0)
            data  = gif.read(dtime ,self._tlen,self._channelname)

            
    def plot(self,datatype='Timeseries',workplace='./'):
        plotfunc = {'Timeseries':mpplot.plottimeseries,
                    'ASD':mpplot.plotspectrum,
                    }
        fname = '{0}{1}_{2}.png'.format(workplace,datatype,self._name)
        plotfunc[datatype](self,fname)
        
            
    def bandpass(self,lowcut,highcut,order):
        from scipy.signal import butter, lfilter
        nyq = 0.5 * self._fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        self.timeseries = lfilter(b, a, self.timeseries)

        
    def decimate(self,fs):
        fs0 = self._fs
        self._fs = fs
        self.timeseries = signal.decimate(self.timeseries,int(fs0/fs))

        
    def cliptime(self,start,end):
        '''
        端数は切り捨てている。

        start : float
           開始時刻。GPS
        end : float
           終了時刻。GPS

        '''
        from math import modf
        tlen = end-start
        start_idx = (start - self._t0)*self._fs
        start_decimal,_ = modf(start_idx)
        end_idx = (end-self._t0)*self._fs
        end_decimal,_ = modf(end_idx)
        if start_decimal!=0.0:
            raise(ValueError,'start time can not devide by {0}'.format(self._fs))
        if end_decimal!=0.0:
            raise(ValueError,'end time can not devide by {0}'.format(self._fs))   
        self.timeseries = self.timeseries[int(start_idx):int(end_idx)]
        self._t0  = start

        
    def get_fft(self):
        from scipy.fftpack import fft,fftfreq,fftshift
        import numpy as np
        self.fft = fft(self.timeseries)[1:self._nlen/2]        
        #self.fft = np.fft.fft(self.timeseries)
        self._f = fftfreq(self._nlen, d=1./self._fs)[1:self._nlen/2]        
        #self.fft = fftshift(self.fft)
        #print self._f
        
        
    def get_psd(self,ave=4,plot=False,asd=True,integ=False,savefile=False,TF_240=False,TF_120=False,**kwargs):
        self._f,self._psd = signal.welch(
            self.timeseries,
            fs=self._fs,
            nperseg=self._nlen/ave,
            #scaling='spectrum'
            scaling='density',
            detrend='constant'
            )
        if asd==True:
            self._psd = np.sqrt(self._psd)
            if TF_240:
                def TF_V2Vel(f):
                    import matplotlib.pyplot as plt
                    H = tf_240()
                    #f = np.logspace(-3,2,1e5)
                    matlab.bode(H,f*(2.*np.pi),Plot=True,dB=True,Hz=True,deg=True)
                    plt.hold(True)
                    plt.savefig('./hoge_240.png')
                    plt.close()
                    #exit()
                    H_V2vel, phase, omega = matlab.bode(1/H,
                                                        f*(2.*np.pi),
                                                        Plot=False,dB=False)

                    return H_V2vel
                self._psd = self._psd*TF_V2Vel(self._f)
            if TF_120:
                def TF_V2Vel(f):
                    import matplotlib.pyplot as plt
                    H = tf_120()
                    #f = np.logspace(-3,2,1e5)
                    matlab.bode(H,f*(2.*np.pi),Plot=True,dB=True,Hz=True,deg=True)
                    plt.hold(True)
                    plt.savefig('./hoge_120.png')
                    plt.close()
                    #exit()
                    H_V2vel, phase, omega = matlab.bode(1/H,
                                                        f*(2.*np.pi),
                                                        Plot=False,dB=False)

                    return H_V2vel
                self._psd = self._psd*TF_V2Vel(self._f)
            if integ == True:
                print self._name
                self._psd = self._psd/(2.0*np.pi*self._f)
        if savefile==True:
            with open('./tmp_{0}.csv'.format(self._name),'w') as f:
                for i in range(len(self._f)):
                    f.write('{0}, {1}\n'.format(self._f[i],self._psd[i]))
                    
        return self._f,self.psd
    
        
    def get_spectrogram(self,ave,plot=True):
        self._nFFT = self._nlen/ave
        self._ovlp = 0.5
        self._f, self._t, self._Sxx = signal.spectrogram(
            x        = self.timeseries,
            fs       = self._fs,
            window   = np.hanning(self._nFFT),
            nperseg  = self._nFFT,
            noverlap = self._nFFT*self._ovlp,
            mode     = 'magnitude',
            scaling  = 'density'
        )

        
    def get_coherence(self,data2,ave,plot=False,title='./tmp/'):
        self._f,self.csd = signal.csd(
            x = self.timeseries,
            y = data2.timeseries,
            fs = self._fs,
            nperseg=self._nlen/ave,
            #scaling='density'
            scaling='spectrum'
        )
        self._nameB = data2._name
        data2.csd = self.csd
        self.get_psd(ave)
        data2.get_psd(ave)
        self._coh   = ( np.abs(self._ksd)**2 + np.abs(self._qsd)**2 )/(self.psd*data2.psd )
        self._cohphase = np.arctan2(self._qsd,self._ksd)
        # !!! なぜかCSDとPSDから求めた結果がCoherence関数の値よりも微妙に少しだけ大きい(1e-20程度)
        f,self._coh = signal.coherence(self.timeseries,data2.timeseries, fs=self._fs, nperseg=self._nlen/ave)
        if plot==True:
            fname = '{0}Coherence_{1}_{2}'.format(title,self._name,self._nameB)
            mpplot.plotcoherence(self,fname,ave=ave,cl=95)

            
    def __div__(self,value):
        self.timeseries /= value
        return self    

    
    def __mul__(self,value):
        self.timeseries *= value
        return self

    
    def __sub__(self,value):
        self.timeseries += value
        return self

    
    def __add__(self,value):
        self.timeseries *= value
        return self
   
