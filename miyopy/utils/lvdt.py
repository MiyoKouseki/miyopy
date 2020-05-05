from warnings import warn
import matplotlib.pyplot as plt
import numpy as np
from gwpy.frequencyseries import FrequencySeries
from gwpy.types import Index

prefix = '/Users/miyo/Git/miyopy/miyopy/utils'
_freq, f0gas, h1, h2, h3 = np.loadtxt(prefix+'/noise/LVDTnoiseETMX_disp.dat').T
noise = np.sqrt(h1**2 + h2**2 + h3**2)
df = 1./1024.0
_freq = np.arange(0.0,100.0+df,df)
noise = FrequencySeries(noise,frequencies=_freq,name='ETMX_LVDT_L',unit='um') # m/rtHz

plot = False
if plot:
    fig = plt.figure(figsize=(10,7))
    plt.loglog(_freq,h1,label='ETMX IP H1')
    plt.loglog(_freq,h2,label='ETMX IP H2')
    plt.loglog(_freq,h3,label='ETMX IP H3 ')
    #plt.loglog(_freq,noise,label='ETMX IP Length')
    plt.loglog(noise,label='ETMX IP Length')
    plt.loglog(_noise,label='ETMX IP Length')
    plt.legend(fontsize=15)
    plt.ylabel('Displacement [um/rtHz]')
    plt.ylim(1e-4,1e0)
    plt.xlabel('Frequency [Hz]')
    plt.savefig('img_noise_etmx_noise.png')
    plt.close()

