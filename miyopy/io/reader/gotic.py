#
#! coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

class gotic2():
    def __init__(self,filename='./tides.out'):
        data = np.loadtxt(filename)
        self.time  = data[:,0]/60.0/24.0
        ns    = data[:,1]
        we    = data[:,2]
        shear = data[:,3]
        self.ex = we*np.cos(np.pi/6.0)*np.cos(np.pi/6.0)\
        +ns*np.sin(np.pi/6.0)*np.sin(np.pi/6.0)+shear*np.sin(2.0*np.pi/6.0)
        self.ey = we*np.sin(np.pi/6.0)*np.sin(np.pi/6.0)+\
        ns*np.cos(np.pi/6.0)*np.cos(np.pi/6.0)-shear*np.sin(2.0*np.pi/6.0)
        plt.figure(num=None, figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
        plt.plot(self.time[43200:],self.ex[43200:])
        plt.savefig('gotic2_ex.png')
        plt.close()
        
if __name__ == '__main__':
    g = gotic2('./tides.out')
