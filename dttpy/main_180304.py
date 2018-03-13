#
#! coding-utf8

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

''' Format 
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
    <Array Type="float">
      <Dim>115201</Dim>
      <Stream Encoding="LittleEndian,base64">
'''


class Spectrum():
    def __init__(self,XMLelement,Name):
        self.Name = Name
        self._getAttribute(XMLelement)
        self._getStream(XMLelement)        
        
    def _getAttribute(self,child):
        self.Flag     = child.find("./Param[@Name='Flag']").text
        self.Subtype  = child.find("./Param[@Name='Subtype']").text
        self.f0       = child.find("./Param[@Name='f0']").text        
        self.df       = child.find("./Param[@Name='df']").text
        self.dt       = child.find("./Param[@Name='dt']").text
        self.t0       = child.find("./Time[@Type='GPS']").text        
        self.BW       = child.find("./Param[@Name='BW']").text
        self.Window   = child.find("./Param[@Name='Window']").text
        self.AveType  = child.find("./Param[@Name='AverageType']").text
        self.Averages = child.find("./Param[@Name='Averages']").text
        self.N        = int(child.find("./Param[@Name='N']").text)
        self.M        = int(child.find("./Param[@Name='M']").text)
        self.dim      = child.find('./Array/Dim').text
        channel = child.findall("./Param[@Unit='channel']")
        #print channel[0].attrib['Name']
        #self.Channel  = map(lambda x:x.text,child.findall("./Param[@Unit='channel']"))
        self.Channel  = map(lambda x:{x.attrib['Name']:x.text},channel)
        Channel = self.Channel[0]
        #print Channel
        for c in self.Channel:
            Channel.update(c)           
        self.Channel = Channel
        #print self.Channel
        #print self.Channel
        
    def _getStream(self,child):
        stream_str = child.find('./Array/Stream').text
        stream_bin = binascii.a2b_base64(stream_str)                   
        if self.Subtype == '1': # float : asd           
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            self.f        = np.arange(len(self.spectrum))*float(self.df)
            #print self.Subtype,self.N,len(self.spectrum),
        elif self.Subtype == '2': # floatcomplex : cross spectrum
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            #self.spectrum = self.spectrum.reshape(self.M,self.N*2)
            #print self.spectrum.shape
            #print self.spectrum[:115201]
            #print self.spectrum[115201:]
            #print self.spectrum[0::2]
            #print self.spectrum[1::2]
            #exit()
            real = self.spectrum[0::2]
            #print self.N,self.M
            real = real.reshape(self.M,self.N)
            imag = self.spectrum[1::2]
            imag = imag.reshape(self.M,self.N)
            self.spectrum = np.sqrt(real**2 + imag**2)
            self.f        = np.arange(len(self.spectrum[0]))*float(self.df)
            #print self.Subtype,self.N,len(self.spectrum)            
        elif self.Subtype == '3': # float : coherence?
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            self.f        = np.arange(len(self.spectrum))*float(self.df)
            #print self.Subtype,self.N,len(self.spectrum)

def hoge(root):
    LIGO_LW = root.findall("./LIGO_LW")
    for element in LIGO_LW:
        print element.attrib
    exit()

def plot_allASD():
    try:
        for s in spect:
            if s.Subtype=='1' and 'EX1_' in s.Channel[0]['ChannelA']: 
                label = s.Name + str(s.Channel[0])
                #print label
                plt.loglog(s.f,s.spectrum,label=label,linewidth=0.7)
                pass
    except Exception as e:
        print e
        exit()
        pass
    plt.legend(loc=3, prop={'size': 7})
    plt.savefig('./hoge.png')
    plt.close()

def plot_allCoherence():
    import traceback
    try:
        for s in spect:
            i = 0
            if s.Subtype=='3' and 'NS_' in s.Channel['ChannelA']:
                print s.Channel#.values()
                print s.Channel['ChannelB[6]']
                #print 'NS_' in s.Channel.values()               
                #print np.where('NS_' in s.Channel.values())                
                if 'NS_' in s.Channel['ChannelA']: 
                    #label = s.Name + str(s.Channel['ChannelB[6]'])+' / '+str(s.Channel['ChannelA'])
                    #print label
                    label = 'aa'
                    #print s.spectrum
                    plt.semilogx(s.f,s.spectrum,label=label,linewidth=0.8)
                    pass
    except Exception as e:
        print traceback.format_exc()
        print e
        exit()
        pass
    plt.legend(loc=3, prop={'size': 7})
    plt.savefig('./hoge.png')
    plt.close()

    
def plot_allCrossspectrum():
    try:
        for s in spect:
            i = 0
            if s.Subtype=='2' and 'EX1' in s.Channel[i]['ChannelA']: 
                label = s.Name + str(s.Channel[i+1])+' / '+str(s.Channel[i])
                print label
                plt.loglog(s.f,s.spectrum[i],label=label,linewidth=0.8)
                #break
                pass
    except Exception as e:
        print e
        exit()
        pass
    plt.legend(loc=3, prop={'size': 7})
    plt.savefig('./all_crossspectrm.png')
    plt.close()
    
    
def main():
    tree = ElementTree.parse('test.xml')
    #tree = ElementTree.parse('psdETMXallfree20180303v0.xml')
    #tree = ElementTree.parse('coverShake.xml')    
    root = tree.getroot()
    spect = [Spectrum(child,child.attrib['Name']) for child in root.findall("./LIGO_LW[@Type='Spectrum']")]
    #plot_allASD()
    #plot_allCrossspectrum()
    plot_allCoherence()
    exit()
    try:
        for s in spect[:6]:
            if s.Subtype=='3':
                #plt.semilogx(s.f,s.spectrum,label=' / '.join(s.Channel),linewidth=0.5)
                pass                
            elif s.Subtype=='2':
                #plt.loglog(s.f,s.spectrum,label=' / '.join(s.Channel),linewidth=0.5)
                pass
            elif s.Subtype=='1':
                print str(s.Channel[0])
                label = s.Name + str(s.Channel[0]) 
                plt.loglog(s.f,s.spectrum,label=label,linewidth=0.5)
                pass
    except Exception as e:
        print e
        exit()
        pass
    plt.legend(loc=3, prop={'size': 7})
    plt.savefig('./hoge.png')
    plt.close()

    
if __name__ == '__main__':
    main()
