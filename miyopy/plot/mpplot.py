#
#! coding:utf-8
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#from control import matlab
from scipy.signal import argrelmax
from matplotlib import rcParams
#import spectrum
from matplotlib.colors import LogNorm
import matplotlib
import matplotlib.pyplot as plt
import spectrum

#plt.grid(which='major',color='gray',linestyle=':',alpha=1)
#plt.grid(which='minor',color='gray',linestyle=':',alpha=1)
param ={
    'font.family'       : 'Arial', #使用するフォント
    'xtick.direction'   : 'in', #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
    'ytick.direction'   : 'in', #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
    'xtick.major.width' : 1.0, #x軸主目盛り線の線幅
    'ytick.major.width' : 1.0, #y軸主目盛り線の線幅
    'axes.linewidth'    : 1.0, # 軸の線幅edge linewidth。囲みの太さ
    'axes.labelsize'    : 12,
    'font.size'         : 10,
    'legend.fontsize'   : 12,
    'xtick.labelsize'   : 10,
    'ytick.labelsize'   : 10,
    'text.usetex'       : False,
    'figure.figsize'    : [8, 5]
   }
plt.rcParams.update(param)

def tsplot(t,data):
    return None

def spectrogram(data,ave):    
    return f,t,Sxx

def plotSpectrogram(data,ave):
    vmax = data._Sxx.max()
    vmin = vmax/1.e3        
    enbw = spectrum.enbw(spectrum.create_window(data._nFFT, 'hanning'))*data._fs/data._nFFT
    print(enbw)
    text = 'StartGPSTime:{0}, Average:{1}, Overrap:50%, Bin:{3:3.2f} sec,' \
           'Window:Hanning, ENBW:{2:3.2e} Hz'.format(data._gps,ave,enbw,data._duration/ave*data._ovlp)
    fig = plt.figure()    
    ax1 = fig.add_axes([0.12, 0.13, 0.70, 0.57])  # spectrogram
    ax1.set_ylabel('Frequency [Hz]')
    ax1.set_xlabel('Time [sec]')
    ax1.grid(which='major',color='gray',linestyle=':',alpha=1)
    ax1.grid(which='minor',color='gray',linestyle=':',alpha=1)
    ax2 = fig.add_axes([0.12, 0.75, 0.70, 0.15])  # timeseriese
    #ax2.set_xlim(xmin=data._t[0]/2.0,xmax=data._t[-1]+(data._t[0]/2.0))
    ax2.set_xlim(xmin=data._t[0],xmax=data._t[-1])
    #print '!',data._name, data.timeseriese.shape[0], data._duration,1024, '?'
    ax2.plot(data._time,data.timeseriese,'k',lw=0.5,label=data._channelname)
    ax2.set_ylabel(data._unit)
    ax2.grid(which='major',color='gray',linestyle=':',alpha=1)
    ax2.grid(which='minor',color='gray',linestyle=':',alpha=1)
    ax2.legend(bbox_to_anchor=(0., 1.05, 1, 0.2),mode="expand", borderaxespad=0.) 
    ax3 = fig.add_axes([0.85, 0.13, 0.03, 0.57])  # colorbar
    ax3.yaxis.set_label_position("right")
    ax3.set_ylabel('PSD [dB]')
    #
    ax4 = fig.text(0.08, 0.02, text)              # footter
    im = ax1.pcolormesh(data._t, data._f, data._Sxx,norm=LogNorm(vmin=vmin, vmax=vmax))
    fig.colorbar(im, cax=ax3,label='Normalized ASD [{0}/rtHz]'.format(data._unit))
    plt.savefig('huge.png')
    plt.close()
    #return fig

    
def MultiPlot_new(data,label,filename,legend):
    '''
    一枚のFigureの上に複数のグラフを載せる。
    '''
    if len(data) != 3:
        print('[Error] please 3 channels',len(data))
        exit()
    fig = plt.figure(figsize=(10,5))
    fig.subplots_adjust(right=0.75)
    host = fig.add_subplot(1, 1, 1)
    host.set_xlabel(label[0])
    host.set_ylabel(label[1])
    ax1 = host.twinx()
    ax2 = host.twinx()
    ax1.set_ylabel(label[1])
    ax2.set_ylabel(label[1])   
    i = 0
    p1, = host.plot(data[i]._time,data[i].timeseries,label=legend[i],linewidth=0.5,color='r')
    i = 1
    p2, = ax1.plot(data[i]._time,data[i].timeseries,label=legend[i],linewidth=0.5,color='b')
    i = 2
    ax2.spines["right"].set_position(("axes", 1.2))
    p3, = ax2.plot(data[i]._time,data[i].timeseries,label=legend[i],linewidth=0.5,color='g')
    #host.legend((ax), ("post","keyword"), loc=0, shadow=True)
    for ax in [ax1, ax2]:
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        plt.setp(ax.spines.values(), visible=False)
        ax.spines["right"].set_visible(True)
    host.legend([p1,p2,p3], [l.get_label() for l in [p1,p2,p3]],loc='upper right')
    host.yaxis.label.set_color(p1.get_color())
    ax1.yaxis.label.set_color(p2.get_color())
    ax2.yaxis.label.set_color(p3.get_color())
    ax1.spines["right"].set_edgecolor(p2.get_color())
    ax2.spines["right"].set_edgecolor(p3.get_color())
    host.tick_params(axis='y', colors=p1.get_color())
    ax1.tick_params(axis='y', colors=p2.get_color())
    ax2.tick_params(axis='y', colors=p3.get_color())
    plt.title(filename)
    print filename
    plt.savefig(filename)
    plt.close()

def MultiPlot(data,label,style,filename,legend,lim):
    for i in range(len(data)):
        alpha=1.0-i*0.1
        plt.plot(data[i][0],
                 data[i][1],
                 style[i],
                 label=legend[i],
                 linewidth=0.5,
                 alpha=alpha)
    plt.legend()
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    plt.title(filename)
    plt.savefig(filename)
    plt.close()
    
    
def MultiSemiLogyPlot(data,label,style,filename,legend,lim):
    for i in range(len(data)):
        alpha=1.0-i*0.1
        plt.semilogy(data[i][0],data[i][1],style[i],label=legend[i],linewidth=0.5,alpha=alpha)
    plt.legend()
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    plt.xlim(lim[0])
    plt.ylim(lim[1])
    #plt.title(filename)
    #plt.savefig(filename+'.png')
    #plt.close()
    
def MultiBodePlot(f,sys,fn,label,style):
    def getNearestValue(list, num):
        idx = np.abs(np.asarray(list) - num).argmin()
        return list[idx],idx
    N = len(sys)
    mag, phase, f = matlab.bode(sys,f,Plot=False,dB=False)
    val, idx = getNearestValue(f,1.0)
    print(mag[idx])
    # Start Graph
    fig = plt.figure()
    fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(8,5))
    # Gain
    ax = axes[0]
    ax.grid(True, which="major",linestyle='-')
    ax.grid(True, which="minor",linestyle=':')
    for i in range(N):
        #ax.loglog(f[i],mag[i],style[i],linewidth=0.5,label=label[i]) #for multi
        ax.loglog(f/(2.*np.pi),mag,style[i],linewidth=0.5,label=label[i])  # for one
    ax.set_ylabel("Gain")
    #ax.legend()
    # Phase
    ax2 = axes[1]
    ax2.grid(True, which="major",linestyle='-')
    ax2.grid(True, which="minor",linestyle=':')
    ax2.set_xlabel("Frequency [Hz]")
    ax2.set_ylabel("Phase")
    wrap = lambda phase: ( phase + np.pi) % (2.0 * np.pi ) - np.pi
    phase = np.rad2deg(wrap(np.deg2rad(phase)))
    for i in range(N):
        #ax2.semilogx(f[i],phase[i],style[i],linewidth=0.5,label=label[i])
        ax2.semilogx(f/(2.*np.pi),phase,style[i],linewidth=0.5,label=label[i])  # for one
    ax2.set_yticks( np.arange(-180.0, 181.0,90 ) )
    ax2.set_ylim([-230,230])
    # Close Graph
    ax2.legend(loc='upper right')
    ax.legend(loc='upper right')
    plt.savefig(fn)
    plt.close()



    
def TF_V2Vel(f):
    H_V2vel, phase, omega = matlab.bode(1/H,f*(2.*np.pi),Plot=False,dB=False)
    return H_V2vel


def readDiaggui_PSD(filename):
    # return ( Frequency[Hz], PSD [Volt/rtHz] )
    data  = np.loadtxt(filename)
    f,psd = data[1:,0],data[1:,1]*c2V
    return f,psd


def ax_plot(ax,x,y,xlabel=None,ylabel=None,legend='None',ylim=[-1e-5,1e-5]):    
    ax.plot(x,y,label=legend,color='k',linewidth=0.8)
    ax.set_ylim(ylim[0],ylim[1])
    ax.grid(color='black', linestyle='--', linewidth=0.6,alpha=0.3)
    ax.legend()
    return ax


def ax_spectrogram(ax,x,y,xlabel=None,ylabel=None,legend='None',ylim=[-1e-5,1e-5]):    
    ax.plot(x,y,label=legend,color='k',linewidth=0.8)
    #ax.set_ylim(ylim[0],ylim[1])
    ax.grid(color='black', linestyle='--', linewidth=0.6,alpha=0.3)
    ax.legend()
    return ax


def subplot33(data,fname,ylim=[-1e-5,1e-5],title='No Title',**kwargs):
    matplotlib.rc('font',family='Arial')
    fig, ax = plt.subplots(3, 3, figsize=(17, 10))
    fig.suptitle(title,fontsize=25,fontname='Arial')
    ax_ = ax.reshape(1,9)[0]
    plot = ax_plot
    for i in range(len(ax_)):
        ax_[i] = plot(
            ax_[i],
            data[i]._time,
            data[i].timeseries,           
            xlabel='Time',
            ylabel='Value',
            legend=data[i]._name,
            ylim=ylim
        )        
    for i in filter(lambda x:x<6,range(6)):
        plt.setp(ax_[i].get_xticklabels(),visible=False)
    for i in filter(lambda x:(x%3)!=0,range(9)):
        plt.setp(ax_[i].get_yticklabels(),visible=False)
    for i in filter(lambda x:x==7,range(9)):
        ax_[i].set_xlabel('Time [sec]',fontsize=20,fontname='Arial')
    for i in filter(lambda x:x==3,range(9)):
        ax_[i].set_ylabel('Velocity [m/sec]',fontsize=20,fontname='Arial')
    fig.tight_layout(rect=[0, 0, 0.99, 0.95])
    plt.savefig(fname)
    plt.close()

    
def subplot31(data,fname,label):
    matplotlib.rc('font',family='Arial')
    fig, ax = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle(fname.split('.')[0],fontsize=20,fontname='Arial')
    ax_ = ax.reshape(1,3)[0]
    for i in range(len(ax_)):
        ax_[i] = ax_plot(
            ax_[i],
            data[i][0],
            data[i][1],           
            xlabel='Time',
            ylabel='Value',
            legend=label[i]            
        )
    '''
    for i in filter(lambda x:x<6,range(6)):
        plt.setp(ax_[i].get_xticklabels(),visible=False)
    for i in filter(lambda x:(x%3)!=0,range(9)):
        plt.setp(ax_[i].get_yticklabels(),visible=False)
    for i in filter(lambda x:x==7,range(9)):
        ax_[i].set_xlabel('Time [sec]',fontsize=20,fontname='Arial')
    for i in filter(lambda x:x==3,range(9)):
        ax_[i].set_ylabel('Velocity [m/sec]',fontsize=20,fontname='Arial')
'''
    fig.tight_layout(rect=[0, 0, 0.99, 0.95])
    plt.savefig(fname)
    plt.close()    

def subplot32(data,fname,label):
    matplotlib.rc('font',family='Arial')
    fig, ax = plt.subplots(2, 3, figsize=(14, 7))
    fig.suptitle(fname.split('.')[0],fontsize=20,fontname='Arial')
    ax_ = ax.reshape(1,6)[0]
    for i in range(len(ax_)):
        ax_[i] = ax_plot(
            ax_[i],
            data[i][0],
            data[i][1],           
            xlabel='Time',
            ylabel='Value',
            legend=label[i]            
        )        
    '''
    for i in filter(lambda x:x<6,range(6)):
        plt.setp(ax_[i].get_xticklabels(),visible=False)
    for i in filter(lambda x:(x%3)!=0,range(9)):
        plt.setp(ax_[i].get_yticklabels(),visible=False)
    for i in filter(lambda x:x==7,range(9)):
        ax_[i].set_xlabel('Time [sec]',fontsize=20,fontname='Arial')
    for i in filter(lambda x:x==3,range(9)):
        ax_[i].set_ylabel('Velocity [m/sec]',fontsize=20,fontname='Arial')
'''
    fig.tight_layout(rect=[0, 0, 0.99, 0.95])
    plt.savefig(fname)
    plt.close()    
    

