#
#! coding:utf-8


def plot_coh(ax,data,fname='cdmr',tlen=None,ave=32,labels=None,disp=True,**kwargs):
    ''' Plot coherence on the axes.

    Parameter
    ---------
    
    
    Return
    ------
    
    '''
    if len(data)==3:
        data1, data2, gif = data
    else:
        data1, data2 = data
        
    if disp:
        integ=True
    else:
        integ=False
    #print(ave)
    dof = ave*2
    alpha = 0.05
    integ=False # kesu!
    #
    f,coh,deg = get_coh(data1,data2,fs=len(data1)/tlen,integ=integ,tlen=tlen,**kwargs)
    
    ax.semilogx(f, coh, label=labels[0],color='k',linewidth=2)
    #cl = np.arange(len(f))*
    cl = 1.0-alpha**(1./(float(dof)/2.0-1.0))
    ax.semilogx(f, cl*np.ones(len(f)),
                label='95% ',color='k',
                linewidth=1,linestyle='--')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Magnitude-Squared \n Coherence')
    ax.set_xlim([1e-2,1e2])
    ax.legend(fontsize=8)
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)        
    ax.tick_params(axis='both',direction='in',which='both')
    #ax.set_yticks(np.arange(10)[::1])
    ax.set_ylim([0,1])
    return ax

def plot_coh_deg(ax,data,tlen=None,fname='cdmr',labels=None,disp=True,**kwargs):
    if len(data)==3:
        data1, data2, gif = data
    else:
        data1, data2 = data
    if disp:
        integ=True
    else:
        integ=False
    
    f,coh,deg = get_coh(data1,data2,fs=len(data1)/tlen,tlen=tlen,integ=integ,**kwargs)
    ax.semilogx(f, deg, label=labels[0],color='k',linewidth=2)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Phase [deg]')
    ax.set_xlim([1e-2,1e2])
    ax.legend(fontsize=8,loc='upper right')
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)        
    ax.tick_params(axis='both',direction='in',which='both')
    ax.set_yticks(np.arange(-180,181,90))
    ax.set_ylim([-180,180])
    return ax


def coherenceplot(data,fname='seismometer',title='No title',ave=None,
                     labels1=None,labels2=None,start=None,tlen=None,**kwargs):
    """ Plot coherence on the 1 row 2 columns figure.

    Parameters
    ----------
    data : [numpy.array, numpy.array] 
        magnitude, phase.       
    fname : str
        output image filename.
    title : str
        Title of the figure
    labels1 : str
        legends for the magnitude axes
    labels2 : str
        legends for the phase axes        
    ave : int
        Averaging number.    
    """    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=340)
    ax1 = plot_coh(ax1,data,labels=labels1,ave=ave,tlen=tlen,disp=False,**kwargs)
    ax2 = plot_coh_deg(ax2,data,labels=labels2,ave=ave,tlen=tlen,disp=False,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    ax_pos = ax1.get_position()
    print(ax1_pos)
    fig.text(ax_pos.x1*1.01, ax_pos.y0,
             'GPS:{0}\nHanning,ovlp=50%'.format(start),
             rotation=90,verticalalignment='bottom')
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.09,0.5)
    ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()
