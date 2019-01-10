#!/usr/bin/env python 
#! coding:utf-8

from gwpy.time import tconvert

from miyopy.files import get_specgram

from miyopy.plot import plot_spectrogram

import argparse 

parser = argparse.ArgumentParser(description='aa')   
parser.add_argument('-c','--channel', help='')
parser.add_argument('-s','--start', help='')
parser.add_argument('-e','--end', help='')
parser.add_argument('--ave',default=256)
parser.add_argument('--fftlen',default=2**9)
parser.add_argument('--overlap',default=2**9)
parser.add_argument('--nproc',default=2)
parser.add_argument('--prefix',default='./')
args = parser.parse_args()
kwargs = {}
kwargs['start'] = args.start
kwargs['end'] = args.end
kwargs['replot'] = True
kwargs['fftlength'] = args.fftlen
kwargs['nproc'] = args.nproc
kwargs['prefix'] = args.prefix


if __name__ == '__main__':
    chname = args.channel
    psd_specgram1 = get_specgram(chname,**kwargs)
    plot_spectrogram(psd_specgram1,**kwargs)
