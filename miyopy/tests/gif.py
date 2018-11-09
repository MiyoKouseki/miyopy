#
#! coding-utf8

from miyopy.io.reader import gif
from miyopy.signal import asd

prefix = '/Users/miyo/Dropbox/KagraData/gif/'


def baro():    
    start = 1223251218
    tlen = 3600*2
    x500 = gif.read(start,tlen,'X500_BARO',prefix=prefix)
    x2000 = gif.read(start,tlen,'X2000_BARO',prefix=prefix)

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    print(len(x500))
    ax1.plot(-x500)
    ax2 = ax1.twinx()
    ax2.plot(x2000,alpha=0.4,color='k')
    plt.savefig('hoge.png')
    plt.close()
    #
    # check
    '''
    f,asd_x500 = asd(x500,200,ave=32,integ=False,gif=False,psd='asd',scaling='density',window='hanning')
    f,asd_x2000 = asd(x2000,200,ave=32,integ=False,gif=False,psd='asd',scaling='density',window='hanning')
    plt.loglog(f,asd_x500)
    plt.loglog(f,asd_x2000)
    #plt.ylim(1e-6,1e-4)
    plt.savefig('hoge_asd.png')
    plt.close()
'''

def strain():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import ScalarFormatter    
    start = 1223510418 # 2018/10/14 00:00:00 UTC
    start = 1223478018 # 2018/10/14 00:00:00 JST
    tlen = 60
    fs= 200.0
    strain = gif.read(start,tlen,'CALC_STRAIN',prefix=prefix)
    time = np.arange(len(strain))/fs#/3600.0
    #
    fig = plt.figure(figsize=(18,5))
    ax1 = fig.add_subplot(111)
    ax1.plot(time,strain)
    ax1.set_xlabel('Time[sec]',fontsize=10)
    ax1.set_ylabel('Strain',fontsize=10)
    ax1.set_xlim(0,60)
    ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    #ax2 = ax1.twinx()
    #ax2.plot(x2000,alpha=0.4,color='k')
    print(strain)
    plt.savefig('strain.png')
    plt.close()
    #
    #
    f,asd_strain = asd(strain,200,ave=6,integ=False,gif=False,psd='asd',scaling='density',window='hanning')
    plt.loglog(f,asd_strain)
    #plt.ylim(1e-6,1e-4)
    plt.savefig('hoge_asd.png')
    plt.close()

    
    
if __name__=='__main__':
    #baro()
    strain()
