#
#! coding:utf-8

import numpy as np
from scipy import signal

def cf(alpha=0.05,k=32):
    from scipy.stats import chi2   
    cfmax = k/chi2.ppf(alpha/2.0, k)
    cfmin = k/chi2.ppf(1.0-alpha/2.0, k)
    return cfmin, cfmax


def asd(data1,fs,ave=None,integ=False,gif=False,
        psd='asd',scaling='density',window='hanning',**kwargs):
    
    if ave==None:
        raise ValueError('Average is not defined. ave; {}'.format(ave))

    f, Pxx_den = signal.welch(data1,
                              fs,
                              nperseg=len(data1)/ave,
                              window=window,
                              scaling=scaling
                              )
    #f = f[1:]
    #Pxx_den = Pxx_den[1:]
    if psd=='asd':        
        Asd_den = np.sqrt(Pxx_den)
    elif psd=='psd':
        Asd_den = Pxx_den
        pass
    else:
        raise ValueError('invalid type psd; {}'.format(psd))    
            
    return f, Asd_den



def coherence(data1,data2,fs,tlen,ave=32,**kwargs):
    print(tlen)
    f, P1_den = signal.welch(data1,
                             fs,
                             nperseg=len(data1)/ave,
                             window='hanning',
                             scaling='density',
    )
    f, P2_den = signal.welch(data1,
                             fs,
                             nperseg=len(data2)/ave,
                             window='hanning',
                             scaling='density',
    )
    f, csd = signal.csd(data1,
                        data2,
                        fs,
                        nperseg=len(data1)/ave,
                        window='hanning',
                        scaling='density',
                        )
    f, coh2 = signal.coherence(data1, data2, fs=len(data1)/tlen, nperseg=len(data1)/ave)        
    A1_den = np.sqrt(P1_den)
    A2_den = np.sqrt(P2_den)
    #csd = np.sqrt(csd)
    deg = np.rad2deg(np.angle(csd))
    #coh2 = np.sqrt((np.abs(csd)**2/np.sqrt(P1_den*P2_den)))
    #coh = np.sqrt(coh2)
    return f, coh2, deg    

