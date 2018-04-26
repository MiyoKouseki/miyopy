#
#! coding:utf-8
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import subprocess


def text_param(popt,pcov,title,data):
    para = ['a0','tau0','f0','phi0','b0',
            'a1','tau1','f1','phi1',
            'a2','tau2','f2','phi2',]
    p_sigma    = np.sqrt(np.diag(pcov))
    text = '-'*60+'\n'
    text += 'Title : {0}'.format(title)+'\n'
    text += 'Name : {0}'.format(data._name)+'\n'
    text += 'Start Time (GPS) : {0}'.format(data._t0)+'\n'
    text += 'Fitting Function: \n'
    text += '  func(t,a0,tau0,f0,phi0,b0,a1,tau1,f1,phi1)\n'
    text += '   = b0 \n'
    text += '   + a0*np.exp(-(t)/tau0)*np.cos(2*np.pi*(f0)*t+np.deg2rad(phi0))\n'
    text += '   + a1*np.exp(-(t)/tau1)*np.cos(2*np.pi*(f1)*t+np.deg2rad(phi1))\n'
    text += 'Fitting Result: \n'
    text += '  Num, Param, OptimalValues[A], sqrt(diag(pcov)[B], [B/A]%,\n'
    for i in range(len(popt)):
        fmt = '  {4}, {0: >5}, {1:+05.2e}, {2:+05.2e}, {3:+05.1f} %,\n'
        error = abs(p_sigma[i]/popt[i])*100.0
        text += fmt.format(para[i],popt[i],p_sigma[i],error,i)
    text += 'Result\n'
    fmt = '  Wave0 : Q={0:3.1f}, f={1:3.2f}\n'
    text += fmt.format(popt[2]*popt[1]*np.pi,popt[2])
    fmt = '  Wave1 : Q={0:3.1f}, f={1:3.2f}\n'
    text += fmt.format(popt[7]*popt[6]*np.pi,popt[7])
    text += '-'*60+'\n'
    return text


def plot_cov(cov,data,title):
    import matplotlib.colors as colors
    from matplotlib.ticker import LogLocator
    cov = np.abs(np.fliplr(cov).T)
    x = np.arange(len(cov)+1)
    y = np.arange(len(cov)+1)
    
    fig, ax = plt.subplots()    
    pcm = ax.pcolormesh(x, y, cov,
                    norm=colors.LogNorm(vmin=cov.min(), vmax=cov.max())
                    )
    para = ['a0','tau0','f0','phi0','b0','a1','tau1','f1','phi1']            
    ax.set_xticks(x+0.5)
    ax.set_xticklabels(para)
    ax.set_yticks(y+0.5)
    ax.set_yticklabels(reversed(para))    
    plt.xlim(x.min(),x.max())
    plt.ylim(y.min(),y.max())
    cb = fig.colorbar(pcm, ticks = LogLocator())
    cb.ax.minorticks_on()
    ax.xaxis.set_ticks_position('top')
    plt.title('abs(Covariance)',y=1.06)
    fname = '{0}/Covarience_{2}_{1}.png'.format(title,data._name.replace('K1:',''),data._t0)
    plt.savefig(fname)
    plt.close()
    cmd = 'open {0}'.format(fname)
    ret = subprocess.check_call(cmd.split(" "))


def QvalueFitting(data,title,plot=True,fitting=True):
    '''2成分の減衰振動を仮定して、Q値を求める関数。
    
    [メモ] boundに張り付いていない場合フィットできている気がする。張り付いていると、フィットはできていない。違う周波数を仮定したり、項を増やすとかそういうのが必要な感じがする。
    
    Parameter
    ---------
    data : miyopy.types.timeseries.Timeseries
        miyopyのTimeseriesクラス。なんちゃってStep応答の時系列をフィットするので、t=0で値がゼロになっていないとフィッティングができない。なので、予めデータの開始時刻を切り取る必要があることに注意。
    title : str
        タイトル。切り取ったデータのタイトル。../event/以下にこのタイトル名のディレクトリが作られる。
    plot : bool
        Trueならプロットをする。デフォルトではTrue。
    fitting : bool
        Trueならフィッティングをする。デフォルトではTrue。    
        
    Return
    ------
    f0 : 

    Q0 : 

    f0 : 

    Q0 : 

    '''
    def func(t,a0,tau0,f0,phi0,b0,a1,tau1,f1,phi1):
        y = b0+a0*np.exp(-(t)/tau0)*np.cos(2*np.pi*(f0)*t+np.deg2rad(phi0))
        y += a1*np.exp(-(t)/tau1)*np.cos(2*np.pi*(f1)*t+np.deg2rad(phi1))
        return y
            
    time = np.arange(len(data.timeseries))/data._fs
    data.timeseries = data.timeseries - data.timeseries[0]
    
    try:
        bounds = {'Other':([-10,0,0.9,-180,-10,-1,0,3.5,-180],
                           [+10,5,1.3,+180,+10,+1,5,3.9,+180]),
                    '20K':([-10,0,1.0,-180,-10,-1,0,3.6,-180],
                           [+10,5,1.2,+180,+10,+1,5,8.8,+180])}
        if '20K' in title:
            popt, pcov = curve_fit(func, time,
                                   data.timeseries,
                                   bounds=bounds['20K'],
                                   absolute_sigma=False,
                                   )
        else:
            popt, pcov = curve_fit(func, time,
                                   data.timeseries,
                                   bounds=bounds['Other'],
                                   absolute_sigma=False,
                                   )
    except Exception as e:
        print e
        exit()    

    text = text_param(popt,pcov,title,data)
    f0,Q0 = popt[2],popt[1]*popt[2]*np.pi
    f1,Q1 = popt[7],popt[6]*popt[7]*np.pi

    plot_cov(pcov,data,title)
        
    if plot:
        plt.figure(figsize=(20, 7))   
        plt.subplot(121)
        plt.plot(time,data.timeseries,label=data._name)
        plt.xlabel('Time [sec] ')
        plt.ylabel('Value')
        plt.title(title)
        plt.plot(data._time,func(data._time,*popt),'-',markersize=1,label='fit')
        plt.legend()
        plt.subplot(122)
        plt.tick_params(labelbottom="off",bottom="off")
        plt.tick_params(labelleft="off",left="off")
        plt.box("off")
        plt.text(0.0, -0.0,text,fontsize=15,fontname='monospace')
        fname = '{0}/Timeseries_{2}_{1}.png'.format(title,data._name.replace('K1:',''),data._t0)
        plt.savefig(fname)
        plt.close()
        cmd = 'open {0}'.format(fname)
        ret = subprocess.check_call(cmd.split(" "))
        
    return f0,Q0,f1,Q1
