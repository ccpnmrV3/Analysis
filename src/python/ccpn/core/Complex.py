"""

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Luca G Mureddu, Simon P Skinner & Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                 " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================

import typing

from ccpnmodel.ccpncore.lib import Util as coreUtil
from ccpn.core.Project import Project
from ccpn.core.Chain import Chain
from ccpn.core._implementation.AbstractWrapperObject import AbstractWrapperObject
from ccpn.core.lib import Pid
from ccpnmodel.ccpncore.api.ccp.molecule.MolSystem import Chain as ApiChain
from ccpnmodel.ccpncore.api.ccp.molecule.MolSystem import ChainGroup as ApiChainGroup

class Complex(AbstractWrapperObject):
  """A group of Chains, which can be used as a single object to describe a
  molecular complex."""

  #: Class name and Short class name, for PID.
  shortClassName = 'MX'
  # Attribute it necessary as subclasses must use superclass className
  className = 'Complex'

  _parentClass = Project

  #: Name of plural link to instances of class
  _pluralLinkName = 'complexes'

  #: List of child classes.
  _childClasses = []

  # Qualified name of matching API class
  _apiClassQualifiedName = ApiChainGroup._metaclass.qualifiedName()


  # CCPN properties
  @property
  def _apiChainGroup(self) -> ApiChainGroup:
    """ CCPN Project ChainGroup"""
    return self._wrappedData

  @property
  def _key(self) -> str:
    """Residue local ID"""
    return self._wrappedData.name.translate(Pid.remapSeparators)

  @property
  def name(self) -> str:
    """Name of Complex, part of identifier"""
    return self._wrappedData.name

  @property
  def _parent(self) -> Project:
    """Parent (containing) object."""
    return self._project


  @property
  def chains(self) -> typing.Tuple[Chain, ...]:
    """Chains that make up Complex."""
    data2Obj = self._project._data2Obj
    return tuple(data2Obj[x] for x in self._wrappedData.sortedChains())

  @chains.setter
  def chains(self, value):
    getDataObj = self._project._data2Obj.get
    value = [getDataObj(x) if isinstance(x,str) else x for x in value]
    self._wrappedData.chains = [x._wrappedData for x in value]

  # Implementation functions
  def rename(self, value:str):
    """Rename Complex, changing its name and Pid"""
    oldName = self.name
    self._startFunctionCommandBlock('rename', value)
    undo = self._project._undo
    if undo is not None:
      undo.increaseBlocking()

    try:
      if not value:
        raise ValueError("Complex name must be set")
      elif Pid.altCharacter in value:
        raise ValueError("Character %s not allowed in ccpn.Complex.name" % Pid.altCharacter)
      else:
        coreUtil._resetParentLink(self._wrappedData, 'chainGroups', {'name':value})
        self._finaliseAction('rename')
        self._finaliseAction('change')

    finally:
      if undo is not None:
        undo.decreaseBlocking()
      self._project._appBase._endCommandBlock()

    undo.newItem(self.rename, self.rename, undoArgs=(oldName,),redoArgs=(value,))

  # Implementation functions
  @classmethod
  def _getAllWrappedData(cls, parent:Project)-> list:
    """get wrappedData for all Complexes linked to NmrProject"""
    molSystem =  parent._wrappedData.molSystem
    if molSystem is None:
      return []
    else:
      return molSystem.sortedChainGroups()



def _newComplex(self:Project, name:str, chains=()) -> Complex:
  """Create new Complex"""

  if name and Pid.altCharacter in name:
    raise ValueError("Character %s not allowed in ccpn.Complex.name" % Pid.altCharacter)

  if chains:
    getByPid = self._project.getByPid
    chains = [getByPid(x) if isinstance(x, str) else x for x in chains]
    values = {'chains':tuple(x.pid for x in chains)}
  else:
    values = {}

  self._startFunctionCommandBlock('newComplex', name, values=values,
                                  parName='newComplex')
  self._project.blankNotification()
  try:
    result =  self._data2Obj.get(self._wrappedData.molSystem.newChainGroup(name=name))
    if chains:
      result.chains = chains
  finally:
    self._project._appBase._endCommandBlock()
    self._project.unblankNotification()

  # DO creation notifications
  result._finaliseAction('create')
  return result

# Connections to parents:
Project.newComplex = _newComplex
del _newComplex


# reverse link Chain.complexes
def getter(self:Chain) -> typing.Tuple[Complex, ...]:
  data2Obj = self._project._data2Obj
  return tuple(data2Obj[x] for x in self._wrappedData.sortedChainGroups())
def setter(self:Chain, value):
  self._wrappedData.chainGroups = [x._wrappedData for x in value]
#
Chain.complexes = property(getter, setter, None, "Complexes that contain Chain")
del getter
del setter

# Extra Notifiers to notify changes in Chain-Complex link
className = ApiChainGroup._metaclass.qualifiedName()
Project._apiNotifiers.extend(
  ( ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'addChain'),
    ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'removeChain'),
    ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'setChains'),
  )
)
className = ApiChain._metaclass.qualifiedName()
Project._apiNotifiers.extend(
  ( ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'addChainGroup'),
    ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'removeChainGroup'),
    ('_modifiedLink', {'classNames':('Chain','Complex')}, className, 'setChainGroups'),
  )
)
