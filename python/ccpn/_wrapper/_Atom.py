"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author: rhfogh $"
__date__ = "$Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__version__ = "$Revision: 7686 $"

#=========================================================================================
# Start of code
#=========================================================================================

from ccpncore.util import Pid
from ccpn import AbstractWrapperObject
from ccpn import Project
from ccpn import Residue
from ccpncore.api.ccp.molecule.MolSystem import Atom as ApiAtom

# NBNB TBD add settable linkedAtoms link for non-ChemComp links ???

class Atom(AbstractWrapperObject):
  """Molecular Atom."""

  #: Class name and Short class name, for PID.
  shortClassName = 'MA'
  # Attribute it necessary as subclasses must use superclass className
  className = 'Atom'

  #: Name of plural link to instances of class
  _pluralLinkName = 'atoms'
  
  #: List of child classes.
  _childClasses = []
  

  # CCPN properties
  @property
  def _apiAtom(self) -> ApiAtom:
    """ CCPN atom matching Atom"""
    return self._wrappedData


  @property
  def _parent(self) -> Residue:
    """Residue containing Atom."""
    return self._project._data2Obj[self._wrappedData.residue]
  
  residue = _parent
    
  @property
  def _key(self) -> str:
    """Atom name string (e.g. 'HA') regularised as used for ID"""
    return self._wrappedData.name.translate(Pid.remapSeparators)

  @property
  def name(self) -> str:
    """Atom name string (e.g. 'HA')"""
    return self._wrappedData.name

  # Utility functions
    
  # Implementation functions

  def rename(self, value:str):
    """Change object id, modifying entire project to maintain consistency.
    NBNB TBD to be implemented"""
    raise NotImplementedError("Atom rename not implemented yet")

  @classmethod
  def _getAllWrappedData(cls, parent: Residue)-> list:
    """get wrappedData (MolSystem.Atoms) for all Atom children of parent Residue"""
    return parent._wrappedData.sortedAtoms()

# No 'new' function - chains are made elsewhere
    
# Connections to parents:

Residue._childClasses.append(Atom)

# Notifiers:
className = ApiAtom._metaclass.qualifiedName()
Project._apiNotifiers.extend(
  ( ('_newObject', {'cls':Atom}, className, '__init__'),
    ('_finaliseDelete', {}, className, 'delete'),
    ('_finaliseUnDelete', {}, className, 'undelete'),
  )
)
