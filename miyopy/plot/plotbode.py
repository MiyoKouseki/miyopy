#
#! coding:utf-8

def _plotbode(ax0,ax1,w,h,label=None):
    mpl.rcParams['lines.linewidth'] = 3    
    mag = np.abs(h)
    phase = np.rad2deg(np.angle(h))
    if True in np.isinf(h):
        raise ValueError('Data have Inf value! \n Exit..')
    ax0.loglog((fs*0.5/np.pi)*w, mag, label=label)
    ax0.grid(which='major',linestyle='-', linewidth=1)
    ax0.grid(which='minor',linestyle=':', linewidth=1)
    ax0.set_ylim([1e-2,1.1e0])
    ax0.set_ylabel('Magnitude')            
    ax1.semilogx((fs*0.5/np.pi)*w,phase,label=label)
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
    ax0.legend(loc='lower right',framealpha=0.8)    
    ax1.legend(loc='lower right',framealpha=0.8)
    return ax0,ax1


def bodeplot(w,h,fname='./bode.png',**kwargs):
    fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, dpi=640)
    ax0,ax1 = _plotbode(ax0,ax1,w,h,label='hoge')
    plt.subplots_adjust(hspace=0.05,top=0.92)    
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_yticklabels(np.arange(-180,181,90))
    ax1.set_ylim([-200,200])
    ax1.set_ylabel('Phase [Degree]')                
    ax1.set_xlabel('Frequency [Hz]')                    
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.suptitle("Bandpass filter")
    plt.savefig(fname)
    plt.close()        
    print('plot {0}'.format(fname))        
