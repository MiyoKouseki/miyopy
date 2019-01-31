'''Read timeseriese from nds0.

'''

__author__ = "Koseki Miyo"


#import sys
#sys.path.insert(0,'/users/Miyo/gwpy')
from gwpy.timeseries import TimeSeries
start = '2019 Jan 29 00:00:00 JST'
end = '2019 Jan 29 01:00:00 JST'
chname = 'K1:PEM-SEIS_IXV_GND_UD_IN1_DQ'
data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088)
print(data)
plot = data.plot()
plot.savefig('hoge.png')
plot.close()
