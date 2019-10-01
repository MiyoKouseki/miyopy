
from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries

def kagra_seis(axis='X',pctl=90):
    if axis in ['X','Y','Z']:
        prefix = '/Users/miyo/Dropbox/Git/miyopy/miyopy/seismodel/JGW-T1910436-v5/'
        fname = 'LongTerm_{axis}_{pctl}_VELO.txt'.format(axis=axis,pctl=pctl)
        vel_asd = FrequencySeries.read(prefix+fname)
        return vel_asd
    elif axis == 'H':
        vel_x = kagra_seis('X',pctl)
        vel_y = kagra_seis('Y',pctl)
        vel_h = (vel_x**2+vel_y**2)**(1./2)
        return vel_h
    elif axis == 'V':
        return kagra_seis('Z',pctl)   
    else:
        raise ValueError('hoge')

def kagra_seis_now(start,end,fftlen=2**8,ovlp=2**7,axis='X',verbose=True):
    if axis in ['X','Y','Z']:
        chname = 'K1:PEM-SEIS_EXV_GND_{0}_OUT_DQ'.format(axis)
        vel = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=verbose)
        vel_asd = vel.asd(fftlength=fftlen,overlap=ovlp)
        return vel_asd
    elif axis == 'H':
        vel_x = kagra_seis_now(start,end,axis='X')
        vel_y = kagra_seis_now(start,end,axis='Y')
        vel_h = (vel_x**2+vel_y**2)**(1./2)
        return vel_h
    elif axis == 'V':
        return kagra_seis('Z',pctl)
    elif axis == 'GIF':
        chname = 'K1:GIF-X_STRAIN_OUT16'
        vel = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=verbose) # strain
        vel = vel*3000*1e6
        vel_asd = vel.asd(fftlength=fftlen,overlap=ovlp)
        return vel_asd
    elif axis == 'L_diff':
        chname = 'K1:PEM-SEIS_EXV_GND_X_OUT16'
        exv = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=verbose) 
        chname = 'K1:PEM-SEIS_IXV_GND_X_OUT16'
        ixv = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=verbose) 
        vel_diff = exv - ixv
        vel_asd = vel_diff.asd(fftlength=fftlen,overlap=ovlp)
        return vel_asd    
    elif axis == 'OpLev_L':
        chname = 'K1:VIS-ETMX_TM_DAMP_L_IN1_DQ'
        vel = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=verbose)
    else:
        raise ValueError('hoge')

    
if __name__ == '__main__':
    x = kagra_seis('X',90)
    y = kagra_seis('Y',90)
    #print kagra_seis('H',90)
