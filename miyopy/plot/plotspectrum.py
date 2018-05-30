#
#! coding:utf-8

import matplotlib.pyplot as plt

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
