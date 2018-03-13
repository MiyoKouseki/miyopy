#
#! coding:utf-8

import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import base64
import binascii
import numpy as np
import matplotlib.pyplot as plt

def readFromExportedAscii():
    data_ascii = np.loadtxt('./psd_ex1_ns_ascii')
    f_ascii = data_ascii[:,0]
    psd_ascii = data_ascii[:,1]
    return f_ascii,psd_ascii

def readFromExportedBinary():
    data = np.fromfile('./psd_ex1_ns_binary',np.float32)
    f_binary = data[0::2]
    psd_binary = data[1::2]
    return f_binary,psd_binary

text_ = ''' 
  <LIGO_LW Name="Result[0]" Type="Spectrum">
    <Param Name="Flag" Type="string">Result</Param>
    <Param Name="Subtype" Type="int">1</Param>
    <Param Name="f0" Type="double" Unit="Hz">0</Param>
    <Param Name="df" Type="double" Unit="Hz">0.0078125</Param>
    <Time Name="t0" Type="GPS">1204009841.0</Time>
    <Param Name="dt" Type="double" Unit="s">0.0078125</Param>
    <Param Name="BW" Type="double" Unit="Hz">0.0117178</Param>
    <Param Name="Window" Type="int">1</Param>
    <Param Name="AverageType" Type="int">0</Param>
    <Param Name="Averages" Type="int">10</Param>
    <Param Name="N" Type="int">115201</Param>
    <Param Name="M" Type="int">1</Param>
    <Param Name="ChannelA" Type="string" Unit="channel">K1:PEM-EX1_SEIS_NS_SENSINF_IN1_DQ</Param>
    <Param Name="ChannelB[12]" Type="string" Unit="channel">K1:PEM-EX1_SEIS_NS_SENSINF_IN1_DQ</Param>
    <Array Type="float">
      <Dim>115201</Dim>
      <Stream Encoding="LittleEndian,base64">huge</Stream>
    </Array>
    </LIGO_LW>
'''

def main_re():
    fn = './psdETMXallfree20180303v0.xml'
    fn = './test.xml'
    #fn = './coverShake.xml'
    with open(fn) as f:
        text = f.read()#.replace('\n','')
    #text = text_#.replace('\n','')
    import re
    pattern = r'<Param Name="dt".*>(.*)</Param>' # dt を取得
    pattern = r'<Param Name="(Channel[AB][\[\d+\]]*)".*>(.*)</Param>' # chnameを取得
    #pattern = r'<Param Name="(Channel(B.\d*.))".*>(.*)</Param>' # chnameを取得    
    #pattern = r'<LIGO_LW.*>(.*)</LIGO_LW>'
    #flag = (re.MULTILINE | re.DOTALL)
    matchs = re.finditer(pattern, text)#,flags=flag)
    for match in matchs:
        print match.groups()
    pattern = r'<LIGO_LW Name="(.*)" Type="(.*)">'
    matchs = re.finditer(pattern, text)#,flags=re.MULTILINE)
    #for match in matchs:
    #    print match.groups()

def main():
    fn = './psdETMXallfree20180303v0.xml'
    fn = './test.xml'
    #fn = './coverShake.xml'
    with open(fn) as f:
        text = f.read()#.replace('\n','')
    #text = text_#.replace('\n','')
   
        
if __name__ == '__main__':
    main()
