"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Geerten Vuister"
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

import operator
from ccpn._wrapper._AbstractWrapperObject import AbstractWrapperObject
from ccpn._wrapper._AbstractWrapperObject import AtomAssignment
from ccpn._wrapper._Project import Project
from ccpn._wrapper._NmrResidue import NmrResidue
from ccpncore.api.ccp.nmr.Nmr import Resonance
from ccpncore.lib import MoleculeQuery
from ccpncore.lib import pid as Pid

class NmrAtom(AbstractWrapperObject):
  """Nmr Atom (corresponds to Resonance."""
  
  #: Short class name, for PID.
  shortClassName = 'MA'

  #: Name of plural link to instances of class
  _pluralLinkName = 'atoms'
  
  #: List of child classes.
  _childClasses = []
  

  # CCPN properties  
  @property
  def ccpnResonance(self) -> Resonance:
    """ CCPN atom matching Atom"""
    return self._wrappedData


  @property
  def _parent(self) -> NmrResidue:
    """Parent (containing) object."""
    return self._project._data2Obj[self._wrappedData.resonanceGroup]
  
  residue = _parent
    
  @property
  def id(self) -> str:
    """Atom name string (e.g. 'HA')"""
    return self._wrappedData.name.translate(Pid.remapSeparators)

  name = id

  @property
  def assignment(self) -> str:
    """AtomAssignment named tuple (chainCode, sequenceCode, residueType, name)"""
    return AtomAssignment( *(self._parent.assignment + (self.name,)))
    
  # Implementation functions
  @classmethod
  def _getAllWrappedData(cls, parent: NmrResidue)-> list:
    """get wrappedData (Resonances) for all Atom children of parent Residue"""
    return sorted(parent._wrappedData.resonances, key=operator.attrgetter('name'))
    
    
def newNmrAtom(parent:NmrResidue, name:str=None, isotopeCode:str=None) -> NmrAtom:
  """Create new child NmrAtom. If name is None, use nucleus@serial"""
  nmrProject = parent._project
  resonanceGroup = parent._wrappedData

  if not isotopeCode:
    if name:
      isotopeCode = MoleculeQuery.DEFAULT_ISOTOPES.get(name[0])
    else:
      raise ValueError("newNmrAtom requires either name or isotopeCode as input")


  return nmrProject.newResonance(resonanceGroup=resonanceGroup, name=name,
                                 isotopeCode=isotopeCode)


def fetchNmrAtom(parent:NmrResidue, name:str):
  """Fetch NmrAtom with name=name, creating it if necessary"""
  resonanceGroup = parent._wrappedData
  return (parent._project._data2Obj.get(resonanceGroup.findFirstResonance(name=name)) or
          parent.newNmrAtom(name=name))
    
# Connections to parents:

NmrResidue._childClasses.append(NmrAtom)

NmrResidue.newNmrAtom = newNmrAtom
NmrResidue.fetchNmrAtom = fetchNmrAtom

# Notifiers:
className = Resonance._metaclass.qualifiedName()
Project._apiNotifiers.extend(
  ( ('_newObject', {'cls':NmrAtom}, className, '__init__'),
    ('_finaliseDelete', {}, className, 'delete')
  )
)
