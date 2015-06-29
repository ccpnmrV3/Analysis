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
from ccpn import AbstractWrapperObject
from ccpn import Project
from ccpnmr import Strip
from ccpncore.api.ccpnmr.gui.Task import StripAxis as ApiStripAxis


class Axis(AbstractWrapperObject):
  """Display Axis for 1D or nD spectrum"""

  #: Short class name, for PID.
  shortClassName = 'GA'

  #: Name of plural link to instances of class
  _pluralLinkName = 'axes'
  
  #: List of child classes.
  _childClasses = []
  

  # CCPN properties  
  @property
  def apiStripAxis(self) -> ApiStripAxis:
    """ CCPN Axis matching Axis"""
    return self._wrappedData
    
  @property
  def _key(self) -> str:
    """local id, of form code.stripSerial"""
    return self._wrappedData.axis.code

  code = _key

    
  @property
  def _parent(self) -> Strip:
    """SpectrumDisplay containing axis."""
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
  def nmrAtoms(self) -> tuple:
    """nmrAtoms connected to axis"""
    ff = self._project._data2Obj.get
    return tuple(ff(x) for x in self._wrappedData.axis.resonances)

  @nmrAtoms.setter
  def nmrAtoms(self, value):
    value = [self.getById(x) if isinstance(x, str) else x for x in value]
    self._wrappedData.axis.resonances = tuple(x._wrappedData for x in value)

  @property
  def strip(self):
    """Strip that Axis belongs to"""
    return self._project._data2Obj.get(self._wrappedData.strip)

  # Implementation functions
  @classmethod
  def _getAllWrappedData(cls, parent:Strip)-> list:
    """get wrappedData (ccpnmr.gui.Task.Axis) in serial number order"""
    return parent._wrappedData.sortedStripAxes()

  def delete(self):
    """Overrides normal delete"""
    raise  ValueError("Axes cannot be deleted independently")

# Connections to parents:
Strip._childClasses.append(Axis)

# We should NOT have any newAxis functions


# Notifiers:
className = ApiStripAxis._metaclass.qualifiedName()
Project._apiNotifiers.extend(
  ( ('_newObject', {'cls':Axis}, className, '__init__'),
    ('_finaliseDelete', {}, className, 'delete')
  )
)
