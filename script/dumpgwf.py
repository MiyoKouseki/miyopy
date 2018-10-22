#!/usr/bin/env python
# coding:utf-8
from glue import lal
from pylal import frutils
from gwpy.timeseries import TimeSeries

gst,get = 1209168018, 1209168018+2**10
chname = 'K1:PEM-EX1_SEIS_NS_SENSINF_INMON'
cachefname = './bKAGRAphase1.cache'
cache = lal.Cache.fromfile(open(cachefname))
data = TimeSeries.read(cache, chname, gst, get)
cachename = cachefname.split('.')[1][1:]
ch = chname.split(':')[1]
dumpedgwf_fname = '{0}_{1}_{2}.gwf'.format(gst,get,ch)
print dumpedgwf_fname
data.write(dumpedgwf_fname)
