#
#! coding:utf-8


import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 1
    
def plot21(title='NoTitle',**kwargs):
    #fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, dpi=640)
    fig, (ax0, ax1) = plt.subplots(2, 1, **kwargs)
    plt.subplots_adjust(hspace=0.05,top=0.92)
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.suptitle(title)
    return fig,(ax0,ax1)

def plot11(title='NoTitle',**kwargs):
    fig, ax0, = plt.subplots(1, 1, **kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    fig.suptitle(title,fontsize=12)
    plt.grid(which='major',linestyle='-', linewidth=1)
    plt.grid(which='minor',linestyle=':', linewidth=1)       
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('ASD [m/sec/sqrtHz]')    
    return fig,ax0


