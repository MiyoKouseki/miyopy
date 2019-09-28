from gwpy.frequencyseries import FrequencySeries
from control import matlab
import numpy as np

# Utils
def tf(sys,omega):
    mag, phase, omega = matlab.bode(sys,omega,Plot=False)
    mag = np.squeeze(mag)
    phase = np.squeeze(phase)
    G = mag*np.exp(1j*phase)
    freq = omega/(2.0*np.pi)
    hoge = FrequencySeries(G,frequencies=freq)
    return hoge
