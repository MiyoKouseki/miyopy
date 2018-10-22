#
#! coding:utf-8
from glue import lal
from pylal import frutils
from gwpy.timeseries import TimeSeries
start,end = 1209168018, 1209168018+2**12
'''
c = lal.Cache.fromfile(open("../K-K1_C.bKAGRAphase1.cache"))
#d = frutils.FrameCache(c, scratchdir="/tmp", verbose=True)
data = TimeSeries.read(c, 'K1:PEM-EX1_SEIS_NS_SENSINF_INMON',start,end)
print data.shape[0]/2**12
data.write('phase1_ex1_ns.gwf')
'''
data = TimeSeries.read('./phase1_ex1_ns.gwf', 'K1:PEM-EX1_SEIS_NS_SENSINF_INMON',start,end)
print data.shape[0]/2**12
print data
