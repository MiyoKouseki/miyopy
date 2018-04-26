#
#! coding:utf-8
import numpy as np
from scipy import signal
import miyopy.plot.mpplot as mpplot


class Timeseries(object):
    def __init__(self,value,name='None',fs=8,t0=None,plot=False,unit=None):
        self._fs = fs
        self._unit = unit
        self._name = name
        self._t0 = t0
        self._dt = 1.0/self._fs
        self.timeseries = value
        if plot:
            import matplotlib.pyplot as plt
            print 'plotting.. as ./tmp_{0}.png'.format(self._name)
            plt.plot(self._time,self._timeseries_nodetrend)
            plt.savefig('./tmp_{0}.png'.format(self._name))
            plt.close()
        pass
        
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
        
        
    @psd.setter
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
        
        
    def get_psd(self,ave=4,plot=False,asd=True,integ=False,savefile=True,**kwargs):
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
            if integ == True:
                print self._name
                self._psd = self._psd/(2.0*np.pi*self._f)

        if plot==True:
            mpplot.LogLogPlot(self,
                              lim=(None,[1e-11,1e-7]),                              
                                  )
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

        
    def get_coherence(self,data2,ave,plot=True):
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
        self._coh   = ( np.abs(self._ksd)**2 + np.abs(self._qsd)**2 )/(self.psd*data2.psd )
        self._cohphase = np.arctan2(self._qsd,self._ksd)
        # !!! なぜかCSDとPSDから求めた結果がCoherence関数の値よりも微妙に少しだけ大きい(1e-20程度)
        f,self._coh = signal.coherence(self.timeseries,data2.timeseries, fs=self._fs, nperseg=self._nlen/ave)
        if plot==True:
            mpplot.CoherencePlot(self,'test',ave=ave,cl=95)

       
