#
#! coding:utf-8

import numpy as np
from astropy.units.quantity import Quantity


class Series(Quantity):
    '''
    Parameter
    ---------
    value:
    unit:
    t0
    dt
    name
    '''
    def __new__(cls, value, vunit=None, # Quantity attrs
                dx=None, x0=None, xunit=None, name=None, # Series attrs
                dtype=None, copy=True, order=None, # ndarray attrs
                subok=True, ndmin=0): # ndarray attrs
        new = super(Series, cls).__new__(cls, value, unit=vunit, dtype=dtype,
                                         copy=copy, order=order, subok=subok,
                                         ndmin=ndmin)        
        if copy:
            new = new.copy()
            
        if name is not None:
            new.name = name
            
        if dx is not None:
            new.dx = Quantity(dx,unit=xunit)
            
        if x0 is not None:
            new.x0 = x0
            
        new.nlen = len(value)        
        new._series = Quantity(np.arange(new.nlen)*dx,unit=xunit)        
        return new
    
    @property
    def x0(self):
        """X-axis coordinate of the first data point
        :type: `~astropy.units.Quantity` scalar
        """
        try:
            return self._x0
        except AttributeError:
            self._x0 = Quantity(0, self.xunit)
            return self._x0

    @x0.setter
    def x0(self, value):
        if value is None:
            del self.x0
            return
        if not isinstance(value, Quantity):
            try:
                value = Quantity(value, self.xunit)
            except TypeError:
                value = Quantity(float(value), self.xunit)
        # if setting new x0, delete xindex
        '''
        try:
            x0 = self._x0
        except AttributeError:
            del self.xindex
        else:
            if value is None or self.x0 is None or value != x0:
                del self.xindex
        '''
        self._x0 = value

    # xunit
    @property
    def xunit(self):
        """Unit of x-axis index
        :type: `~astropy.units.Unit`
        """
        try:
            return self._dx.unit
        except AttributeError:
            try:
                return self._x0.unit
            except AttributeError:
                return self._default_xunit

    @xunit.setter
    def xunit(self, unit):
        unit = Unit(unit)
        try:  # set the index, if present
            self.xindex = self._xindex.to(unit)
        except AttributeError:  # or just set the start and step
            self.dx = self.dx.to(unit)
            self.x0 = self.x0.to(unit)            

    @property
    def dx(self):
        """X-axis sample separation
        :type: `~astropy.units.Quantity` scalar
        """
        try:
            return self._dx
        except AttributeError:
            try:
                self._xindex
            except AttributeError:
                self._dx = Quantity(1, self.xunit)
            else:
                if not self.xindex.regular:
                    raise AttributeError("This series has an irregular x-axis "
                                         "index, so 'dx' is not well defined")
                self._dx = self.xindex[1] - self.xindex[0]
            return self._dx


    @dx.setter
    def dx(self, value):
        '''                
        # delete if None
        if value is None:
            del self.dx
            return
        # convert float to Quantity
        if not isinstance(value, Quantity):
            value = Quantity(value, self.xunit)
        # if value is changing, delete xindex

        try:
            dx = self._dx
        except AttributeError:
            del self.xindex
        else:
            if value is None or self.dx is None or value != dx:
                del self.xindex
        '''
        self._dx = value

    @classmethod        
    def read(cls,t0,tlen,chname,fs=1,*kwargs):
        from .. import gif
        return gif.read(t0,tlen,chname,fs=fs)
        
        
    def plot(self, **kwargs):
        """Plot the data for this timeseries
        All keywords are passed to `~gwpy.plotter.TimeSeriesPlot`
        Returns
        -------
        plot : `~gwpy.plotter.TimeSeriesPlot`
            the newly created figure, with populated Axes.
        See Also
        --------
        matplotlib.pyplot.figure
            for documentation of keyword arguments used to create the
            figure
        matplotlib.figure.Figure.add_subplot
            for documentation of keyword arguments used to create the
            axes
        matplotlib.axes.Axes.plot
            for documentation of keyword arguments used in rendering the data
        """
        from ..plotter import TimeSeriesPlot
        return TimeSeriesPlot(self, **kwargs)
        
        
    def __str__(self):
        return '{4}\n- name:\t{0}\n- val:\t{1} {5}\n- dx:\t{2}\n- x0:\t{3}'.format(
            self.name,self.value,self.dx,self.x0,self.__class__,self.unit)
    
    
'''
if __name__=='__main__':
value=[0,1,2,3,4,5]
    dt=0.1
    t0=1212143472
    q = Series(value,dx=dt,x0=t0,vunit='um/s',xunit='us',name='hoge')
'''
