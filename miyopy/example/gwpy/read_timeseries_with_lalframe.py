'''Read timeseriese from gwffile.

'''

__author__ = "Koseki Miyo"

from gwpy.timeseries import TimeSeries

source = 'K-K1_C-1231133824-32.gwf'
chname = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
data = TimeSeries.read(source,chname,format='gwf.lalframe')
print type(data)

data.override_unit('um/s') # bugs when use lalframe reader
<<<<<<< HEAD

=======
print(data)
>>>>>>> 8b8d6b023f6556273536da86b3c7dd3873dfb6c2
plot = data.plot()
print type(plot)

plot.savefig('result_timeseries.png')
plot.close()
