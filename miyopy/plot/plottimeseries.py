import matplotlib.pyplot as plt




def plottimeseries(data,fname='./tmp.png',label=['Time','Value']):
    print 'plot {0}'.format(fname)        
    plt.plot(data._time,data.timeseries,label=data._name)
    plt.ylabel(label[0])
    plt.xlabel(label[1])
    plt.legend()
    plt.title(fname)            
    plt.savefig(fname)
    plt.close()
