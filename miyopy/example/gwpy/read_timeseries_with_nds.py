'''Read timeseriese from nds0.

'''

__author__ = "Koseki Miyo"

from gwpy.timeseries import TimeSeries


start = '2019 Jan 10 05:36:46'
end = '2019 Jan 10 06:07:18'
chname = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088)
plot = data.plot()
plot.savefig('result_timeseries.png')
plot.close()
