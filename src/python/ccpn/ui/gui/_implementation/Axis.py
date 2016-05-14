"""GUI Display Strip class

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================
from typing import Sequence, Tuple
from ccpn.util import Pid
from ccpn.core._implementation.AbstractWrapperObject import AbstractWrapperObject
from ccpn.core.Project import Project
from ccpn.core.NmrAtom import NmrAtom
from ccpn.ui.gui._implementation.Strip import Strip
from ccpncore.api.ccpnmr.gui.Task import StripAxis as ApiStripAxis
from ccpncore.api.ccpnmr.gui.Task import Axis as ApiAxis
# from ccpncore.api.ccpnmr.gui.Task import Axis as ApiAxis


class Axis(AbstractWrapperObject):
  """Display Axis for 1D or nD spectrum"""

  #: Short class name, for PID.
  shortClassName = 'GA'
  # Attribute it necessary as subclasses must use superclass className
  className = 'Axis'

  #: Name of plural link to instances of class
  _pluralLinkName = 'axes'
  
  #: List of child classes.
  _childClasses = []

  # Qualified name of matching API class
  _apiClassQualifiedName = ApiStripAxis._metaclass.qualifiedName()
  

  # CCPN properties  
  @property
  def _apiStripAxis(self) -> ApiStripAxis:
    """ CCPN Axis matching Axis"""
    return self._wrappedData
    
  @property
  def _key(self) -> str:
    """local id, equal to Axis code"""
    return self._wrappedData.axis.code.translate(Pid.remapSeparators)

  code = _key

    
  @property
  def _parent(self) -> Strip:
    """Strip containing axis."""
    return self._project._data2Obj.get(self._wrappedData.strip)

  strip = _parent

  @property
  def position(self) -> float:
    """Centre point position for displayed region, in current unit."""
    return self._wrappedData.axis.position

  @position.setter
  def position(self, value):
    self._wrappedData.axis.position = value

  @property
  def width(self) -> float:
    """Width for displayed region, in current unit."""
    return self._wrappedData.axis.width

  @width.setter
  def width(self, value):
    self._wrappedData.axis.width = value

  @property
  def region(self) -> tuple:
    """Display region - position +/- width/2.."""
    position = self._wrappedData.axis.position
    halfwidth = self._wrappedData.axis.width / 2.
    return (position - halfwidth, position + halfwidth)

  @region.setter
  def region(self, value):
    self._wrappedData.axis.position = (value[0] + value[1]) / 2.
    self._wrappedData.axis.width = abs(value[1] - value[0])

  @property
  def unit(self) -> str:
    """Display unit for axis"""
    return self._wrappedData.axis.unit

  # NBNB TBD This should be settable, but changing it requires changing the position
  # values. For now we leave it unsettable.

  # NBNB TBD the 'regions' attribute may not be needed. leave it out

  @property
  def nmrAtoms(self) -> Tuple[NmrAtom]:
    """nmrAtoms connected to axis"""
    ff = self._project._data2Obj.get
    return tuple(sorted(ff(x) for x in self._wrappedData.axis.resonances))

  @nmrAtoms.setter
  def nmrAtoms(self, value):
    value = [self.getByPid(x) if isinstance(x, str) else x for x in value]
    self._wrappedData.axis.resonances = tuple(x._wrappedData for x in value)

  @property
  def strip(self):
    """Strip that Axis belongs to"""
    return self._project._data2Obj.get(self._wrappedData.strip)

  # Implementation functions
  @classmethod
  def _getAllWrappedData(cls, parent:Strip)-> list:
    """get wrappedData (ccpnmr.gui.Task.Axis) in serial number order"""
    apiStrip = parent._wrappedData
    dd = {x.axis.code:x for x in apiStrip.stripAxes}
    return [dd[x] for x in apiStrip.axisCodes]

  def delete(self):
    """Overrides normal delete"""
    raise  ValueError("Axes cannot be deleted independently")

def getter(self) -> Tuple[Axis, ...]:
  apiStrip = self._wrappedData
  ff = self._project._data2Obj.get
  return tuple(ff(apiStrip.findFirstStripAxis(axis=x)) for x in apiStrip.orderedAxes)
def setter(self, value:Sequence):
  value = [self.getByPid(x) if isinstance(x, str) else x for x in value]
  self._wrappedData.orderedAxes = tuple(x._wrappedData.axis for x in value)
Strip.orderedAxes = property(getter, setter, None,
                             "Axes in display order (X, Y, Z1, Z2, ...) ")

del getter
del setter

# Connections to parents:
Strip._childClasses.append(Axis)

# We should NOT have any newAxis functions

# Notifiers:
Project._apiNotifiers.append(
  ('_notifyRelatedApiObject', {'pathToObject':'stripAxes', 'action':'change'},
   ApiAxis._metaclass.qualifiedName(), '')
)

def _axisRegionChanged(axis:Axis):
  """Notifier function: Update strips etc. for when axis position or width changes"""

  position = axis.position
  width = axis.width
  region = (position - width/2., position + width/2.)

  strip = axis.strip

  index = strip.axisOrder.index(axis.code)
  if not strip.beingUpdated:

    strip.beingUpdated = True

    try:
      if index == 0:
        # X axis
        strip.viewBox.setXRange(*region)
      elif index == 1:
        # Y axis
        strip.viewBox.setYRange(*region)
      else:
        # One of the Z axes
        for spectrumView in strip.spectrumViews:
          if spectrumView.isVisible():
            for peakListView in spectrumView.peakListViews:
              if peakListView.isVisible():
                peakList = peakListView.peakList
                peaks = [peak for peak in peakList.peaks if strip.peakIsInPlane(peak)]
                strip.stripFrame.guiSpectrumDisplay.showPeaks(peakListView, peaks)

        if len(strip.axisOrder) > 2:
          n = index - 2
          if n >= 0:
            planeLabel = strip.planeToolbar.planeLabels[n]
            planeSize = planeLabel.singleStep()
            planeLabel.setValue(position)
            strip.planeToolbar.planeCounts[n].setValue(width/planeSize)

    finally:
      strip.beingUpdated = False

  if index == 1:  # ASSUMES that only do H phasing
    strip.updatePhasing()

Axis.setupCoreNotifier('change', _axisRegionChanged)