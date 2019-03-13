'''Read timeseriese from gwffile.

'''

__author__ = "Koseki Miyo"

from gwpy.timeseries import TimeSeries

source = '/frame0/full/12364/K-K1_C-1236493984-32.gwf'
chname = 'K1:PEM-SEIS_IXV_GND_X_OUT_DQ'
data = TimeSeries.read(source,chname,format='gwf.lalframe')
data.override_unit('um/s') # bugs when use lalframe reader
print(data)
plot = data.plot()
plot.savefig('result_timeseries.png')
plot.close()
