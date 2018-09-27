#
#! coding:utf-8

from miyopy.signal import bandpass
import numpy as np
from scipy.signal import lfilter,zpk2tf,butter,filtfilt
from scipy.signal import zpk2sos,sosfilt,butter
from scipy.signal import freqs_zpk,freqs,freqz,bilinear
from control import matlab
from miyopy.plot import bodeplot


def TRselfnoise(trillium='120QA',psd='ASD',acc='acc'):
    '''
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    psd : str
        if PSD, return psd. if ASD, return asd. default is psd.
    acc : str
        if "acc", return acc. if "velo", return velocity, if "disp", 
        return displacement.

    Return 
    ------
    f : np.array
        Frequency
    selfnoise : np.array
        selfnoise spectrum. unit is depend what you choose.    
    '''
    if trillium=='compact':
        data = np.array([[1e-3,-145], # Freq [Hz], PSD (m/s^2)^2/Hz [dB]
                        [3e-3,-153],
                        [4e-2,-169],
                        [1e-1,-171],
                        [1e0, -175],
                        [3e0, -173],
                        [1e1, -166],
                        [2e1, -159],
                        [5e1, -145],
                        [5e2, -105]])
        f,selfnoise = data[:,0],data[:,1]  # PSD Acceleration with dB
        selfnoise     = 10**(selfnoise/10) # PSD Acceleration with Magnitude
    elif trillium=='120QA':
        data = np.array([[1e-3,-171.0], # Freq [Hz.0], PSD (m/s^2)^2/Hz [dB.0]
                        [3e-3,-179.0],
                        [1e-2,-184.0],
                        [3e-2,-188.0],
                        [1e-1,-189.0],
                        [2e-1,-188.0],
                        [1e0, -186.0],
                        [3e0, -182.0],
                        [1e1, -169.0],
                        [2e1, -158.0],
                        [2e2, -118.0]]) # fit 
        f,selfnoise = data[:,0],data[:,1] # PSD Acceleration with dB
        selfnoise = 10**(selfnoise/10.0) # PSD Acceleration with Magnitude
        
    if acc=='acc':
        f, selfnoise = f, selfnoise
    elif acc=='velo':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**2
    elif acc=='disp':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**4
    else:
        raise ValueError('!')
        
    if psd=='PSD':
        f, selfnoise = f, selfnoise
    elif psd=='ASD':
        f, selfnoise = f, np.sqrt(selfnoise)
    else:
        raise ValueError('psd {} didnt match PSD or ASD'.format(psd))        
        
    return f, selfnoise




def H_120QA(flat=True):
    ''' Trillium 120QA TransferFunction

    Transfer function from Velocity to Voltage.

    Retrun
    ------
    H : matlab.tf
    
    '''    
    z = np.array([0,
                  0,
                 -31.63,
                 -160,
                 -350,
                 -3177]) # rad/sec
    p = np.array([-0.03661+0.037059j,
                  -0.03661-0.037059j,
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
    S = 1.0*(1202.5/9.99999979) # f=1Hzで1202.5になるように規格化した。
    num,den  = zpk2tf(z,p,S*k)
    return num,den


def _V2Vel(data):
    fs = 2048.0
    #fs = 16
    #time = np.arange(len(data)) / fs
    #noise_power = 1e-22 * fs / 2   
    #data = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
    num,den = H_120QA()
    # 規格化されてる周波数の場合,fs=1
    numd, dend = bilinear(num, den, fs=2048/2)
    w,h = freqz(numd,dend,np.logspace(-6,1,1e5))
    #f = w/2.0/np.pi*fs
    nyquist = fs/2.0
    f = w/(2.0*np.pi)*nyquist
    #f = w*nyquist
    bodeplot(f,h,ylim=[1e-0,1e4])
    data = lfilter(numd,dend,data)
    #exit()
    import matplotlib.pyplot as plt
    plt.plot(data[:10])
    plt.savefig('hoge.png')
    plt.close()
    return data


class trillium120QA(object):
    def __init__(self):
        pass

    @classmethod
    def V2Vel(self,data):
        return _V2Vel(data)        

    @classmethod
    def bandpass(self,data,low,high,fs,order):
        data,_,_ = bandpass(data,low,high,fs,order)            
        return data
