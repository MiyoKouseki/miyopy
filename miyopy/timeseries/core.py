#
#! coding:utf-8

import numpy as np
from astropy.units.quantity import Quantity

class SeriesBase(Quantity):
    '''
    Parameter
    ---------
    value:
    unit:
    x0:int
    dx:
    name:
    '''
    def __new__(cls, value, vunit=None, # Quantity attrs
                dx=None, x0=None, xunit=None, name=None, # Series attrs
                dtype=None, copy=True, order=None, # ndarray attrs
                subok=True, ndmin=0): # ndarray attrs
        new = super(SeriesBase, cls).__new__(cls, value, unit=vunit, dtype=dtype,
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
        self._x0 = value


    @x0.deleter
    def x0(self):
        try:
            del self._x0
        except AttributeError:
            pass        
        
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
        self._dx = value
        
    @dx.deleter
    def dx(self):
        try:
            del self._dx
        except AttributeError:
            pass
        
        
    @property
    def name(self):
        """Name for this data set
        :type: `str`
        """
        try:
            return self._name
        except AttributeError:
            self._name = None
            return self._name

        
    @name.setter
    def name(self, val):
        self._name = val


        
    
class TimeSeriesBase(SeriesBase):    
    '''
    Parameter
    ---------
    value:
    unit:
    t0:int
    dt:
    name:
    '''
    
    def __new__(cls, value, vunit=None, # Quantity attrs
                dt=None, t0=None, tunit=None, name=None, # Series attrs
                dtype=None, copy=True, order=None, # ndarray attrs
                subok=True, ndmin=0): # ndarray attrs
        new = super(TimeSeriesBase, cls).__new__(cls, value, vunit=vunit, dtype=dtype,
                                             dx=dt, x0=t0, xunit=tunit,
                                             copy=copy, order=order, subok=subok,
                                             ndmin=ndmin)
        if copy:
            new = new.copy()
            
        if name is not None:
            new.name = name

        if t0 is not None:
            new.t0 = Quantity(t0,tunit)
            
        if dt is not None:
            new.dt = Quantity(dt,tunit)
            
        return new
      
    t0 = SeriesBase.x0
    dt = SeriesBase.dx
    
    @classmethod        
    def read(cls,t0,tlen,chname,prefix=None,**kwargs):
        from .. import gif
        return gif.read(t0,tlen,chname,prefix=prefix,**kwargs)
    
    
    def plot(self, **kwargs):
        """Plot 
        """
        from ..plotter import TimeSeriesPlot
        # GWpyでエポックを使っているので、いれた
        kwargs['epoch'] = self.t0.value
        return TimeSeriesPlot(self, **kwargs)    
