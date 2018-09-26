#
#! coding:utf-8

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import spectrum

def peak_index(data):
    return signal.argrelmax(data)

def confidential_peak_index(data,cl):
    pidx = peak_index(data)
    cidx = np.where(data>cl)
    cpidx = np.intersect1d(pidx,cidx)
    return cpidx

def clfunc(ave,alpha=5.0):
    return 1.0-(1.0-alpha/100.0)**(1./(ave-1))

def plotcoherence(data,fn,ave,cl,unwrap=False,xlim=(1e0,1e3)):    
    fig = plt.figure()
    ax1 = fig.add_axes([0.12, 0.43, 0.80, 0.47])  # coherence    
    ax2 = fig.add_axes([0.12, 0.13, 0.80, 0.25])  # phase
    #ax1.set_xlim(xlim[0],xlim[1])
    #ax2.set_xlim(xlim[0],xlim[1])
    # Gain
    #ax1.grid(True, which="major",linestyle=':')
    #ax1.grid(True, which="minor",linestyle=':')
    clfunc = lambda a: 1.0-(1.0-a/100.0)**(1./(ave-1))
    ax1.semilogx(data._f,data._coh,
                 linewidth=0.5,
                 label=data._nameB+' / '+data._name,
                 color='black') #for multi
    #cpidx = confidential_peak_index(data._coh,clfunc(cl))
    #ax1.semilogx(data._f[cpidx],data._coh[cpidx],'ro',markersize=4)
    ax1.set_ylabel("Coherence")
    ax1.legend()
    #ax1.legend(bbox_to_anchor=(0., 1.05, 1, 0.1),mode="expand", borderaxespad=0.,ncol=1)
    ax1.plot(data._f,np.ones(len(data._f))*clfunc(cl),'k--',linewidth=1)
    ax1.text(data._f[1], clfunc(cl)*0.9, '{0:3.2f}%'.format(cl),bbox={'facecolor':'w', 'alpha':0.9, 'pad':0.5})# footter
    # Phase
    #ax2.grid(True, which="major",linestyle=':')
    #ax2.grid(True, which="minor",linestyle=':')
    ax2.set_xlabel("Frequency [Hz]")
    ax2.set_ylabel("Phase")
    if unwrap==True:
        data._cohphase = np.rad2deg(np.unwrap(data._cohphase))
    else:
        data._cohphase = np.rad2deg((data._cohphase))
        ax2.set_yticks( np.arange(-180.0, 181.0,90 ) )

    ax2.semilogx(data._f,data._cohphase,linewidth=0.5,label='b',color='black')
    cpidx = confidential_peak_index(data._f,clfunc(cl))
    ax2.semilogx(data._f[cpidx],data._cohphase[cpidx],'ro',markersize=4)
    ax1.set_ylim([0,1])
    # Close Graph
    ave    = ave # 16回平均
    nFFT   = data._nlen/ave
    window = np.hanning(nFFT)
    enbw   = spectrum.enbw(spectrum.create_window(nFFT, 'hanning'))*data._fs/nFFT
    text = '''StartGPSTime:{0}, Average:{1}, Overrap:50%, Window:Hanning, ENBW:{2:3.2e} Hz'''.format(123,ave,enbw)
    ax3 = fig.text(0.08, 0.02, text)              # footter
    fig.suptitle(fn)                
    print 'saved',fn
    plt.savefig(fn+'.png')    
    plt.close()
    #return fig

    
def plot_coh(ax,f,coh,label,ave=None,**kwargs):
    color = ['black','red','green']
    for i,f in enumerate(f):
        ax.semilogx(f,coh[i],
                    linewidth=0.5,
                    color=color[i],
                    label=label[i],
                    alpha=1.0-0.2*i,                    
                        )
    ax.set_ylabel("Coherence")
    ax.legend()
    ax.set_ylim([0,1])        
    return ax


def plot_coh_cl(ax,f,cl=5.0,ave=None,**kwargs):
    print(clfunc(ave,cl))
    for i,f in enumerate(f):    
        ax.plot(f,np.ones(len(f))*clfunc(cl,ave),
                'k--',
                linewidth=1,
                label='{0}%'.format(cl)
                )    
    ax.legend()
    return ax


def plot_deg(ax,f,deg,label,**kwargs):
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Phase")
    ax.set_yticks( np.arange(-180.0, 181.0,90 ) )
    color = ['black','red','green']    
    for i,f in enumerate(f):    
        ax.semilogx(f,deg[i],
                    linewidth=0.5,
                    label=label[i],
                    color=color[i],
                    alpha=1.0-0.2*i,                                        
                        )
    return ax


def plot21_coherence(f,coh,deg,title=None,label=None,**kwargs):
    '''
    
    '''
    if type(f)==list:
        pass
    elif type(f)==np.ndarray:
        f = [f]
        coh = [coh]
        deg = [deg]
        label = [label]
    else:
        raise ValueError('error!')
    fig = plt.figure(dpi=320)
    ax1 = fig.add_axes([0.12, 0.43, 0.80, 0.47])  # coherence
    ax2 = fig.add_axes([0.12, 0.13, 0.80, 0.25])  # phase
    ax1 = plot_coh(ax1,f,coh,label,**kwargs)
    ax2 = plot_deg(ax2,f,deg,label,**kwargs)
    plt.suptitle(title)
    fn = title+format('.png')
    print 'saved',fn
    plt.savefig(fn)    
    plt.close()   
