#
#! coding:utf-8
from .core import plot21
from ..utils import magphase

def _plotbode(ax0,ax1,w,h,label=None):
    w, mag,phase = magphase(w,h)
    ax0.loglog(w, mag, label=label,color='k')
    ax0.grid(which='major',linestyle='-', linewidth=1)
    ax0.grid(which='minor',linestyle=':', linewidth=1)
    ax0.set_ylabel('Magnitude')            
    ax1.semilogx(w,phase,label=label,color='k')
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
    ax0.legend(loc='lower right',framealpha=0.8)    
    ax1.legend(loc='lower right',framealpha=0.8)
    return ax0,ax1


def bodeplot(w,h,fname='./bode.png',ylim=None,xlim=None,**kwargs):
    fig, (ax0, ax1) = plot21(sharex=True,dpi=640)    
    ax0,ax1 = _plotbode(ax0,ax1,w,h,label='hoge')
    ax1.set_yticks(range(-180,181,90))
    ax1.set_yticklabels(range(-180,181,90))
    ax1.set_ylim([-200,200])
    ax1.set_ylabel('Phase [Degree]')                
    ax1.set_xlabel('Frequency [Hz]')
    ax0.set_ylim(ylim)
    ax0.set_xlim(xlim)
    ax1.set_xlim(xlim)
    fig.savefig(fname)    
    print('plot {0}'.format(fname))        
