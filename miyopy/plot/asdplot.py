#
#! coding: utf-8

from .core import plot11
from ..signal import asd

class AsdPlotException(Exception):
    pass




def _plotasd(ax0,datalist,unit='Arbitrary Unit',**kwargs):
    print(len(datalist))
    if len(datalist)>4:
        raise AsdPlotException('Exeed available number of plot')
    
    legend = kwargs.get('legend',['data1','data2','data3','data4'])
    linestyle = kwargs.get('linestyle',['-','-','-','-'])
    for i,data in enumerate(datalist):        
        ax0.loglog(data[0], data[1], linestyle[i], label=legend[i], linewidth=2)
    ax0.set_xlabel('Frequency [Hz]')
    ax0.set_ylabel('ASD [{0}/sqrtHz]'.format(unit))
    return ax0


def asdplot(datalist,fname='NoTile',title='No title',**kwargs):   
    fig, ax1 = plot11(dpi=640)
    ax1 = _plotasd(ax1,datalist,**kwargs)
    #
    start = kwargs.get('start',None)
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,
             'GPS:{0}\nHanning,ovlp=50%'.format(start),
                 rotation=90,verticalalignment='bottom')
    #
    fig.savefig('{0}.png'.format(fname))
