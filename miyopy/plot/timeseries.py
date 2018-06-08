
class TimeSeriesPlot(SeriesPlot):
    """`Figure` for displaying a `~gwpy.timeseries.TimeSeries`.
    Parameters
    ----------
    *series : `TimeSeries`
        any number of `~gwpy.timeseries.TimeSeries` to
        display on the plot
    **kwargs
        other keyword arguments as applicable for the
        `~gwpy.plotter.Plot`
    """
    _DefaultAxesClass = TimeSeriesAxes

    def __init__(self, *series, **kwargs):
        """Initialise a new TimeSeriesPlot
        """
        kwargs.setdefault('figsize', [12, 6])
        super(TimeSeriesPlot, self).__init__(*series, **kwargs)

        # set default epoch
        data = TimeSeriesPlot._get_axes_data(series, flat=True)
        for ax in self.axes[:-1]:
            if kwargs.get('sharex', None):
                ax.set_xlabel("")

    # -- properties ---------------------------------

    @property
    def epoch(self):
        """The GPS epoch of this plot
        """
        try:  # look for this class (allow for subclasses)
            axes = self._find_axes(self._DefaultAxesClass.name)
        except IndexError:  # look for base timeseries
            for ax in self.axes:
                if isinstance(ax, TimeSeriesAxes):
                    axes = ax
        return axes.epoch

    def get_epoch(self):
        """Return the GPS epoch of this plot
        """
        return self.epoch

    @auto_refresh
    def set_epoch(self, gps):
        """Set the GPS epoch of this plot
        """
        axeslist = self.get_axes(self._DefaultAxesClass.name)
        for axes in axeslist:
            axes.set_epoch(gps)

    # -- add_ methods -------------------------------

    def add_timeseries(self, timeseries, **kwargs):
        super(TimeSeriesPlot, self).add_timeseries(timeseries, **kwargs)
        if self.epoch is None:
            self.set_epoch(timeseries.epoch)

    def add_state_segments(self, segments, ax=None, height=0.2, pad=0.1,
                           location='bottom', plotargs=dict()):
        """Add a `SegmentList` to this `TimeSeriesPlot` indicating state
        information about the main Axes data.
        By default, segments are displayed in a thin horizontal set of Axes
        sitting immediately below the x-axis of the main
        Parameters
        ----------
        segments : `~gwpy.segments.flag.DataQualityFlag`
            A data-quality flag, or `SegmentList` denoting state segments
            about this Plot
        ax : `Axes`
            specific Axes set against which to anchor new segment Axes
        plotargs
            keyword arguments passed to
            :meth:`~gwpy.plotter.SegmentAxes.plot`
        """
        from .segments import SegmentAxes

        # get axes to anchor against
        if not ax:
            try:
                ax = self.get_axes(self._DefaultAxesClass.name)[-1]
            except IndexError:
                raise ValueError("No 'timeseries' Axes found, cannot anchor "
                                 "new segment Axes.")

        # add new axes
        if ax.get_axes_locator():
            divider = ax.get_axes_locator()._axes_divider
        else:
            divider = make_axes_locatable(ax)
        if location not in ['top', 'bottom']:
            raise ValueError("Segments can only be positoned at 'top' or "
                             "'bottom'.")
        segax = divider.append_axes(location, height, pad=pad,
                                    axes_class=SegmentAxes, sharex=ax,
                                    epoch=ax.get_epoch(), xlim=ax.get_xlim(),
                                    xlabel=ax.get_xlabel())

        # plot segments
        segax.plot(segments, **plotargs)
        segax.grid(b=False, which='both', axis='y')
        segax.autoscale(axis='y', tight=True)

        # update anchor axes
        pyplot.setp(ax.get_xticklabels(), visible=False)
        ax.set_xlabel("")

        return segax
