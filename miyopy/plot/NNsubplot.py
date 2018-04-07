import matplotlib
import matplotlib.pyplot as plt

def ax_plot(ax,x,y,xlabel=None,ylabel=None,legend='None'):    
    ax.plot(x,y,label=legend,color='k',linewidth=0.8)
    ax.set_ylim(-5e-6,5e-6)
    ax.grid(color='black', linestyle='--', linewidth=0.6,alpha=0.3)
    ax.legend()
    return ax

def subplot33(data,fname,label):
    matplotlib.rc('font',family='Arial')
    fig, ax = plt.subplots(3, 3, figsize=(17, 10))
    fig.suptitle(fname.split('.')[0],fontsize=20,fontname='Arial')
    ax_ = ax.reshape(1,9)[0]
    for i in range(len(ax_)):
        ax_[i] = ax_plot(
            ax_[i],
            data[i][0],
            data[i][1],           
            xlabel='Time',
            ylabel='Value',
            legend=label[i]            
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
    
