'''Read timeseriese from gwffile.

'''

__author__ = "Koseki Miyo"


from gwpy.timeseries import TimeSeries
from gwpy.plot import Plot

start = '2019 Jan 10 05:36:46'
end = '2019 Jan 10 06:07:18'
chname = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'

data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088)

sg = data.spectrogram2(fftlength=2**7, overlap=2**6, window='hanning') ** (1/2.)
median = sg.percentile(50)
low = sg.percentile(5)
high = sg.percentile(95)

plot = Plot()
ax = plot.gca(xscale='log', xlim=(0.01, 100), xlabel='Frequency [Hz]',
              yscale='log', #ylim=(3e-24, 2e-20),
              ylabel=r'Strain noise [1/\rtHz]')
ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
ax.set_title('LIGO-Hanford strain noise variation around GW170817',
             fontsize=16)
plot.savefig('result_asd.png')
