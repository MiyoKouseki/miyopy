#
#! coding:utf-8
import numpy as np
from scipy import signal
import mpplot as mpp

from gwpy.timeseries import TimeSeries
from glue.lal import Cache


class data(object):
    def __init__(self,attrdic,gwpy_is_work=True):
        [setattr(self, '_'+key, attrdic[key]) for key in attrdic.keys()]
        self._getTimeSeriese(gwpy_is_work)
        
    @property
    def timeseriese(self):
        return self._timeseriese
    
    @property
    def psd(self):
        return self._psd
          
    @property
    def csd(self):
        return self._csd
                
    @timeseriese.setter
    def timeseriese(self,value):
        self._timeseriese = value
        self._nlen = len(self._timeseriese)
        self._duration = self._nlen/self._fs
        self._time = np.arange(self._duration*self._fs)/float(self._fs)
        
    @psd.setter
    def psd(self,value):
        self._psd = value
        
    @psd.setter
    def csd(self,value):
        self._csd = value
        self._ksd,self._qsd = self._csd.real,self._csd.imag
    
    def _getTimeSeriese(self,data_from='txt'):
        if data_from='txt':
            self.timeseriese = np.loadtxt(self._filepath)
        elif data_from='gwf':
            gwf_cache = '/Users/miyo/Documents/KAGRA/data/frames/K-K1_C.iKAGRA.cache'
            with open(gwf_cache, 'r') as fobj:
                cache = Cache.fromfile(fobj)
            data = TimeSeries.read(cache,self._channelname,self._gps,self._gps+self._duration)       
            self.timeseriese = data.value
        elif data_from = 'gif':
            dtime = mptime.gps2JST(self._gps)
            data  = gif.read(dtime ,self._duration,self._channelname)
            
    def downsample(self,fs):        
        fs0 = self._fs
        self._fs   = fs
        self.timeseriese = signal.decimate(self.timeseriese,int(fs0/fs))
        
    def cliptime(self,start,end):
        self.timeseriese = self.timeseriese[int(start*self._fs):int(end*self._fs)]
        self._gps  = self._gps + start

    def get_psd(self,ave,plot=True):
        self._f,self._psd = signal.welch(
            self.timeseriese,
            fs=self._fs,
            nperseg=self._nlen/ave,
            scaling='spectrum'
        )
        
    def get_spectrogram(self,ave,plot=True):
        self._nFFT = self._nlen/ave
        self._ovlp = 0.5
        self._f, self._t, self._Sxx = signal.spectrogram(
            x        = self.timeseriese,
            fs       = self._fs,
            window   = np.hanning(self._nFFT),
            nperseg  = self._nFFT,
            noverlap = self._nFFT*self._ovlp,
            mode     = 'magnitude',
            scaling  = 'density'
        )
       
    def get_coherence(self,data2,ave,plot=True):
        self._f,self.csd = signal.csd(
            x = self.timeseriese,
            y = data2.timeseriese,
            fs = self._fs,
            nperseg=self._nlen/ave,
            #scaling='density'
            scaling='spectrum'
        )
        data2.csd = self.csd
        self._coh   = ( np.abs(self._ksd)**2 + np.abs(self._qsd)**2 )/(self.psd*data2.psd )
        self._cohphase = np.arctan2(self._qsd,self._ksd)
        # !!! なぜかCSDとPSDから求めた結果がCoherence関数の値よりも微妙に少しだけ大きい(1e-20程度)
        #f,coh_ = signal.coherence(self.timeseriese,data2.timeseriese, fs=self._fs, nperseg=self._nlen/ave)
        if plot==True:
            mpp.CoherencePlot(self,'coherence_micns',ave=ave,cl=99.99)


if __name__            
