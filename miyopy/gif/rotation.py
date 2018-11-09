# coding:utf-8

import numpy as np


def rotate2d(strain_x,strain_y,shear,theta,**kwargs):
    ''' Rotate timeseries strain data


    ref. http://www.continuummechanics.org/stressxforms.html

        
    Parameters
    ----------
    strain_x : numpy.array
        timeseries data of x axis principal strain

    strain_y : numpy.array
        timeseries data of y axis principal strain        

    shear : numpy.array 
        timeseries data of shear strain

    theta : float
        rotation angle. [rad]

    Returns
    -------
    _x : numpy.array
        new timeseries data of x axis principal strain

    _y : numpy.array
        new timeseries data of y axis principal strain

    _shear : numpy.array
        timeseries data of shear strain
              
    '''
    sin = np.sin(theta)
    cos = np.cos(theta)
    
    _x = strain_x*cos*cos + strain_x*sin*sin + 2*shear*sin*cos
    _y = strain_y*sin*sin + strain_x*cos*cos - 2*shear*sin*cos
    _shear = -strain_y*sin*cos + strain_x*sin*cos + shear*( cos**2 - sin**2 )           
    return _x,_y,_shear

