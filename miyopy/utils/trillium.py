#
#! coding:utf-8


import numpy as np
from scipy.signal import lfilter,zpk2tf,butter,filtfilt
from scipy.signal import zpk2sos,sosfilt,butter
from scipy.signal import freqs_zpk,freqs,freqz,bilinear
#from control import matlab
#from miyopy.plot import bodeplot
from scipy.interpolate import interp1d    

from gwpy.frequencyseries import FrequencySeries

def tf120QA(f):
    from miyopy.utils.trillium import H_120QA
    from scipy import signal
    from miyopy.plot import bodeplot
    num,den = H_120QA()
    _w = f*(2.0*np.pi)
    #w,h = signal.freqs(num,den,np.logspace(-4,4,1e5))
    w,h = signal.freqs(num,den,_w)    
    #f = w/(2.0*np.pi)    
    #bodeplot(f,h,ylim=[1e-0,1e4],xlim=[1e-4,1e3])
    mag = np.abs(h)
    mag[0] = mag[1]#-1e-20
    return mag


def selfnoise(trillium='120QA',psd='ASD',unit='acc'):
    '''
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    psd : str
        if PSD, return psd. if ASD, return asd. default is psd.
    unit : str
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
        
    if unit=='acc':
        f, selfnoise = f, selfnoise
    elif unit=='velo':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**2
    elif unit=='disp':
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

        
def zpk_120qa(flat=True):
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
    k = 8.31871*10e17  # f=1Hzで1202.5になるように規格化した。だめだけども。
    S = 1202.5/9.99999845
    if False:
        z,p,k = trillium.zpk_120qa()
        num,den = zpk2tf(z,p,k)
        w,h = freqs(num,den,worN=np.logspace(-2,3,1e5))        
        f=w/np.pi/2.0
        df = f[1]-f[0]
        idx = np.where(np.isclose(f,1.0,atol=df)==True)[0]
        print(abs(h[idx]))
        plt.loglog(f,abs(h))
        plt.savefig('hoge.png')                
    return z,p,k*S


def zpk_240(flat=True):
    ''' Trillium 240 TransferFunction

    Transfer function from Velocity to Voltage.

    Retrun
    ------
    H : matlab.tf
    
    '''    
    z = np.array([0,
                  0,
                  -108.0,
                  -161.0]) # rad/sec
    p = np.array([-0.01815+0.01799j,
                  -0.01815-0.01799j,
                  -173.0,
                  -196.0+231.0j,
                  -196.0-231.0j,
                  -732.0+1415.0j,
                  -732.0-1415.0j,
                      ])# rad/sec
    k = 2.316*10e9/10.01198958 # f0=1 で1になるようにした
    S = 1196.5
    
    if False:
        num,den = zpk2tf(z,p,k)
        _w = np.logspace(-3,3,1e4)
        w,h = freqs(num,den,worN=_w)
        f = w/np.pi/2.0
        #f = w
        df = f[1]-f[0]
        idx = np.where(np.isclose(f,1.0,atol=df)==True)[0]
        print(abs(h[idx]))
        print(f)
        import matplotlib.pyplot as plt
        plt.subplot(211)
        plt.semilogx(f,20*np.log10(abs(h)))
        plt.ylim(-30,10)
        plt.yticks(np.arange(-30,11,10))
        plt.xlim(1e-3,200)        
        plt.subplot(212)
        plt.xlim(1e-3,200)
        plt.semilogx(f,np.rad2deg(np.angle(h)))
        plt.ylim(-180,180)
        plt.yticks(np.arange(-180,181,90))
        plt.savefig('hoge.png')
        #exit()
    return z,p,k*S


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



def vel2vel(f,asd):    
    z,p,k = zpk_120qa()
    num,den = zpk2tf(z,p,k)
    w,h = freqs(num,den,worN=np.logspace(-4,5,1e2))
    mag = abs(h)
    _f = w/np.pi/2.0
    func = interp1d(_f,mag)
    if False:
        plt.loglog(_f,abs(mag),'o-')
        #plt.loglog(__f,_mag)
        plt.savefig('hoge.png')
    vel2v = func(f[1:])
    asd = asd[1:]/vel2v*1202.5
    return f[1:],asd


def _v2vel(self, args):
    '''
    args : f, asd

    '''
    n = len(args)
    if n==2:
        f, asd = args
    else:
        try:
            f = args.frequencies.value
            asd = args.value
            name = args.name
        except:
            raise ValueError('!')

    if self.trillium == '120QA':
        z,p,k = zpk_120qa()
    elif self.trillium == 'compact':
        z,p,k = zpk_120compact()        
    elif self.trillium == '240':
        z,p,k = zpk_240()
    else:
        raise ValueError('Invalid trillium name')
    num,den = zpk2tf(z,p,k)
    w,h = freqs(num,den,worN=np.logspace(-4,5,1e2))
    mag = abs(h)
    _f = w/np.pi/2.0
    func = interp1d(_f,mag)
    vel2v = func(f[1:])
    asd = asd[1:]/vel2v#*1202.5
    if n==2:
        return f[1:],asd
    else:
        data = FrequencySeries(asd,frequencies=f[1:],unit='m/s',name=name)
        return data


def _selfnoise(self,psd='ASD',unit='m/s/s'):
    '''
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    psd : str
        if PSD, return psd. if ASD, return asd. default is psd.
    unit : str
        if "acc", return acc. if "velo", return velocity, if "disp", 
        return displacement.

    Return 
    ------
    f : np.array
        Frequency
    selfnoise : np.array
        selfnoise spectrum. unit is depend what you choose.    
    '''
    trillium = self.trillium
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
                        [3e-1,-188.0],
                        [1e0, -186.0],
                        [3e0, -182.0],
                        [1e1, -169.0],
                        [2e1, -158.0],
                        [2e2, -118.0]]) # fit 
        f,selfnoise = data[:,0],data[:,1] # PSD Acceleration with dB
        selfnoise = 10**(selfnoise/10.0) # PSD Acceleration with Magnitude
    elif trillium=='240':
        data = np.array([[1e-3,-172.0], # Freq [Hz.0], PSD (m/s^2)^2/Hz [dB.0]
                        [3e-3,-179.0],
                        [1e-2,-185.0],
                        [3e-2,-189.0],
                        [1e-1,-190.0],
                        [3e-1,-190.0],
                        [1e0, -187.0],
                        [3e0, -180.0],
                        [1e1, -169.0],
                        [2e1, -155.0],
                        [2e2, -110]]) # fit 
        f,selfnoise = data[:,0],data[:,1] # PSD Acceleration with dB
        selfnoise = 10**(selfnoise/10.0) # PSD Acceleration with Magnitude
        
    if unit=='m/s/s':
        f, selfnoise = f, selfnoise
    elif unit=='m/s':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**2
    elif unit=='m':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**4
    else:
        raise ValueError('!')
        
    if psd=='PSD':
        f, selfnoise = f, selfnoise
    elif psd=='ASD':
        f, selfnoise = f, np.sqrt(selfnoise)
    else:
        raise ValueError('psd {} didnt match PSD or ASD'.format(psd))        
    return FrequencySeries(selfnoise,frequencies=f)
    

#from miyopy.signal import bandpass


class Trillium(object):
    def __init__(self,trillium):
        self.trillium = trillium

    def v2vel(self,data):
        return _v2vel(self,data)
    
    def selfnoise(self):
        return _selfnoise(self,psd='ASD',unit='m/s')        
