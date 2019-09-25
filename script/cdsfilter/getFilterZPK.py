#
#! coding:utf-8
'''
フィルターバンクの"# DESIGN ~"に書かれている文字列を抜き出したい。
'''
import re
fbname = 'ETMX_IP_BLEND_ACCL'
fname = './chans/K1VISETMXT.txt'
with open(fname,'r') as f:
    txt = f.read()
    regex = r'^# DESIGN.*{0} ([0-9]+) (([a-z]+\([^\)]*\))+)'.format(fbname)
    pattern = re.compile(regex, flags=(re.DOTALL|re.MULTILINE))
    #pattern = re.compile(regex, flags=(re.DOTALL))
    matches = re.findall(pattern, txt)
    print matches#[0][1]
