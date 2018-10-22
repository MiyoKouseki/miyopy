#
#! coding:utf8
# http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
# Direct Least Squares Fitting of Ellipses 
from scipy.optimize import curve_fit
import numpy as np
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import eig, inv
import matplotlib.animation as animation

def fitEllipse(x,y):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    # memo???
    # 自由度N-6のカイ二乗分布に従う。けど、自由度が大きいので正規分布にみなせる。
    # なので、期待値Nで分散2Nの正規分布に従う。
    # エラーバーは二乗和が1シグマずれるパラメータの幅を表す？から…
    return a 

def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])


def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))


def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return np.array([res1, res2])

def ellipse_angle_of_rotation2( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    if b == 0:
        if a > c:
            return 0
        else:
            return np.pi/2
    else:
        if a > c:
            return np.arctan(2*b/(a-c))/2
        else:
            return np.pi/2 + np.arctan(2*b/(a-c))/2

def theta(x,y,x0,y0,a0,b0,phi):
    COS = (x-x0)/a0
    SIN = (y-y0)/b0
    theta = np.arctan(np.sin(phi)/np.cos(phi)/COS-np.tan(phi))
    return theta



if __name__ == '__main__':
    fname = '/Users/miyo/KAGRA/lib/miyopy/example/data/1711290000.<ext>'
    mV = 1e-3
    # Read Data
    i,k = 0,2500
    pd1 = np.fromfile(fname.replace('<ext>','AD00'),np.int32)[i*k:(i+1)*k] * 5.525e-9*mV
    pd2 = np.fromfile(fname.replace('<ext>','AD01'),np.int32)[i*k:(i+1)*k] * 5.525e-9*mV
    pd3 = np.fromfile(fname.replace('<ext>','AD02'),np.int32)[i*k:(i+1)*k] * 5.525e-9*mV    
    pd1 = pd1/pd3
    pd2 = pd2/pd3
    # Fitting
    arc = 2.0
    R = np.arange(0,arc*np.pi, 0.01)
    a = fitEllipse(pd1,pd2)
    x0,y0 = ellipse_center(a)
    a0,b0 = ellipse_axis_length(a)
    phi   = ellipse_angle_of_rotation(a)
    xx = x0 + a0*np.cos(R)*np.cos(phi) - b0*np.sin(R)*np.sin(phi)
    yy = y0 + a0*np.cos(R)*np.sin(phi) + b0*np.sin(R)*np.cos(phi)
    text = '''    
-*- Fitting Result -*-
center : (x0, y0) = (%3.3f, %3.3f) [mV]
axes   : (a0, b0) = (%3.3f, %3.3f) [mV]
angle  : phi      = %3.2f          [deg]
''' %(x0,y0,a0,b0,np.rad2deg(phi))
    print text
    # Plot   
    plt.figure(figsize=(7,7))
    plt.subplot(211)
    plt.plot(pd1,pd2,'ko',markersize=3)
    plt.plot(xx,yy,'r--')
    plt.plot(x0,y0,'ko')
    plt.xlabel('PD1 [mV]')
    plt.ylabel('PD2 [mV]')
    #
    angle = theta(pd1,pd2,x0,y0,a0,b0,phi)
    angle_unwrap = np.unwrap(angle*2.0)/2.0
    plt.subplot(212)
    plt.plot(angle,'k',alpha=0.1)
    plt.plot(angle_unwrap,'k')
    plt.savefig('fitEllipse.png')
    plt.close()
       


        
