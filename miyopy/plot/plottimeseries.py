import matplotlib.pyplot as plt




def plottimeseries(data,fname='./tmp.png',label=['Time','Value']):
    print 'plot {0}'.format(fname)        
    plt.plot(data._time,data.timeseries,label=data._name)
    plt.xlabel('Time [{0}]'.format(data._time._unit))
    plt.ylabel('{0} [{1}]'.format(data.unit,data.timeseries._unit))
    plt.legend()
    plt.title(fname)            
    plt.savefig(fname)
    plt.close()
