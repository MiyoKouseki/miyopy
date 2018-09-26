#
#! coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from miyopy.signal import asd,cf


def plotspectrum(datalist,lim,label=['xlabel','ylabel'],filename='./noname',**kwargs):
    '''スペクトルを描画する関数
    
    
    Parameter
    ---------
    datalist : list of mptypes.spectrumdata

    
        
    '''
    if not isinstance(datalist,list):
        datalist = [datalist]
        
    print 'LogLogPlot..'
    for i,data in enumerate(datalist):
        print '\t',i,data._name
        if i==0:
            plt.loglog(data._f,data.psd,label=data._name,linewidth=4.0)
        #elif data._name=='Baro_x500':
        #    plt.loglog(data._f,data.psd,label=data._name,linewidth=1.0,color='brown')
        else:
            plt.loglog(data._f,data.psd,label=data._name,linewidth=1.0,alpha=0.9)
            
    plt.legend(fontsize=10,loc='upper right')
    plt.xlabel('Frequency [Hz]',fontsize=15)
    plt.ylabel(label[1],fontsize=15)
    plt.title(filename[2:],fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.ylim(lim[1])
    plt.xlim(lim[0])
    plt.savefig(filename+'.png')
    plt.close()


def _plotASD(ax,datalist,fname='asd',labels=None,
             ave=None,
             tlen=None,
             disp=True,model=None,adcnoise=True,
             unit=None,selfnoiseplot=True,trillium=None,ylim=None,
             linestyle=['r-','b-','g-'],**kwargs):

    '''時系列データからASDをAxesにプロットする関数。

    与えられたAxesにASDをプロットする。

    
    Parameter
    ---------
    ax : matplotlib.axes
        Axesのオブジェクト。これにプロットする。
    datalist : list of numpy.array
        時系列データ。複数個可。

    Return
    ------
    ax : matplotlib.axes
        ASDが描かれたAxesオブジェクト。

    '''
    
    ax.set_xlim([1e-3, 1e2])
    ax.set_ylim(ylim)    
    if tlen==None:
        raise ValueError('tlen is not defined. tlen {}'.format(tlen))
    
    plotOK = [True,True,False]
    
    for i,_data in enumerate(datalist):
        print(i,_data.shape,len(_data)/tlen)
        f,Asd = asd(_data,fs=len(_data)/tlen,ave=ave,**kwargs)
        ax.loglog(f, Asd, linestyle[i], label=labels[i], linewidth=2)            
        if (True in np.isnan(Asd)):
            print('Data has nan value!')    
    
        
    cfmin,cfmax = cf(alpha=0.05,k=ave*2)    
    ax.errorbar(1.0, 1e-6, yerr=[[(1-cfmin)*1e-6],[(cfmax-1)*1e-6]], fmt='ko',markersize=2,capsize=3,label='{0:3.0f}%, DoF={1}'.format((1-0.05)*100,ave*2))        
    ax.set_xlabel('Frequency [Hz]')
    ax.legend(loc='upper right',fontsize=8)
    ax.tick_params(axis='both',direction='in',which='both')
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)
    return ax

    

def plotASD(data,fname='NoTile',title='No title',
         labels1=None,labels2=None,text=None,
         tlen=None,**kwargs):
    '''AmplitudeSpectrumDensity(ASD)を描く関数
    
    1画面にASDを描く関数。複数データに対応。    

    Parameter
    ---------
    data : list of np.array
        時系列データ。複数個でも可
    fname : str
        ファイル名。                

    Return
    ------    
    '''
    start = kwargs.get('start',None)
            
    fig, ax1 = plt.subplots(1, 1, sharex=True, dpi=640)
    ax1 = _plotASD(ax1,data,labels=labels1,ave=32,tlen=tlen,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,
             text,
             rotation=90,verticalalignment='bottom')
    
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.1,0.5)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Velocity [m/sec/sqrtHz]')
    plt.savefig('{0}.png'.format(fname))
    plt.close()
    print('plot {}.png'.format(fname))    
