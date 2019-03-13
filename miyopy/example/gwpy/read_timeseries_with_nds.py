'''Read timeseriese from nds0.

'''

__author__ = "Koseki Miyo"

from gwpy.timeseries import TimeSeries

start = '2019 Mar 10 05:36:46'
end = '2019 Mar 10 06:07:18'
chname = 'K1:PEM-SEIS_IXV_GND_X_OUT_DQ'
data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088)
print(data)
plot = data.plot()
plot.savefig('result_timeseries.png')
plot.close()
