import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from control import matlab


def decimate(data,fs_befor,fs_after):
    from scipy.signal import decimate
    data_ = decimate(data,int(fs_befor/fs_after))
    return data_

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut/nyq
    high = highcut/nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def filt_iirpeak(dic,fs,f0,Q,plot=False):
    w0 = f0/(fs/2)
    num, den = signal.iirpeak(w0, Q)
    data = { key:signal.lfilter(num,den,dic[key]) for key in dic.keys()}
    if plot == True:
        w, h = signal.freqz(num, den,worN=10000)
        freq = w*fs/(2*np.pi)
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        ax[0].semilogx(freq, 20*np.log10(abs(h)), color='blue')
        ax[0].set_title("Frequency Response")
        ax[0].set_ylabel("Amplitude (dB)", color='blue')
        #ax[0].set_xlim([0, 100])
        #ax[0].set_ylim([-50, 10])
        ax[0].grid()
        ax[1].semilogx(freq, np.unwrap(np.angle(h))*180/np.pi, color='green')
        ax[1].set_ylabel("Angle (degrees)", color='green')
        ax[1].set_xlabel("Frequency (Hz)")
        #ax[1].set_xlim([0, 100])
        #ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
        #ax[1].set_ylim([-90, 90])
        ax[1].grid()
        plt.savefig('hoge.png')
        plt.close()
    return data

def filt_butterBandPass(dic,fs,lowcut,highcut,order,plot=False):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    num, den = butter(order, [low, high], btype='band')
    data = { key:signal.lfilter(num,den,dic[key]) for key in dic.keys()}
    if plot == True:
        w, h = signal.freqz(num, den,worN=1000)
        freq = w*fs/(2*np.pi)
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        ax[0].semilogx(freq, 20*np.log10(abs(h)), color='blue')
        ax[0].set_title("Frequency Response")
        ax[0].set_ylabel("Amplitude (dB)", color='blue')
        #ax[0].set_xlim([0, 100])
        #ax[0].set_ylim([-50, 10])
        ax[0].grid()
        ax[1].semilogx(freq, np.unwrap(np.angle(h))*180/np.pi, color='green')
        ax[1].set_ylabel("Angle (degrees)", color='green')
        ax[1].set_xlabel("Frequency (Hz)")
        #ax[1].set_xlim([0, 100])
        #ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
        #ax[1].set_ylim([-90, 90])
        ax[1].grid()
        plt.savefig('hoge.png')
        plt.close()
    return data
