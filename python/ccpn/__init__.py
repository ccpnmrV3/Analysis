"""CCPN data. High level interface for normal data access

The standard ways of starting a project are:

- ccpn.openProject(*path*, ...)
- ccpn.newProject(*projectName*, ...)
- ccpn.Project(*ccpncore.api.ccp.nmr.Nmr.NmrProject*)


.. currentmodule:: ccpn

.. autosummary::

  openProject
  newProject
   _Project.Project
   _Molecule.Molecule
   _Chain.Chain
   _Residue.Residue
   _Atom.Atom
   _ChemicalShiftList.ChemicalShiftList
   _ChemicalShift.ChemicalShift
   _Spectrum.Spectrum
   _SpectrumReference.SpectrumReference
   _PeakList.PeakList
   _Peak.Peak
   _AbstractWrapperClass.AbstractWrapperClass

ccpn.Project class
------------------

.. autoclass:: ccpn._wrapper._Project.Project

ccpn.Molecule class
-------------------

.. autoclass:: ccpn._wrapper._Molecule.Molecule

ccpn.Chain class
----------------

.. autoclass:: ccpn._wrapper._Chain.Chain

ccpn.Residue class
------------------

.. autoclass:: ccpn._wrapper._Residue.Residue

ccpn.Atom class
---------------

.. autoclass:: ccpn._wrapper._Atom.Atom

ccpn.ChemicalShiftList class
----------------------------

.. autoclass:: ccpn._wrapper._ChemicalShiftList.ChemicalShiftList

ccpn.ChemicalShift class
------------------------

.. autoclass:: ccpn._wrapper._ChemicalShift.ChemicalShift

ccpn.Spectrum class
-------------------

.. autoclass:: ccpn._wrapper._Spectrum.Spectrum

ccpn.SpectrumReference class
----------------------------

.. autoclass:: ccpn._wrapper._SpectrumReference.SpectrumReference

ccpn.PeakList class
-------------------

.. autoclass:: ccpn._wrapper._PeakList.PeakList

ccpn.Peak class
---------------

.. autoclass:: ccpn._wrapper._Peak.Peak


ccpn.AbstractWrapperClass class
-------------------------------

.. autoclass:: ccpn._wrapper._AbstractWrapperClass.AbstractWrapperClass

"""

# import sys
# print ('sys.path=', sys.path)
# for key in sorted(sys.modules):
#   print(' - ', key)

from ccpncore.util import Io as ioUtil

# All classes must be imported in correct order for subsequent code
# to work, as connections between classes are set when child class is imported
from ccpn._wrapper._AbstractWrapperObject import AbstractWrapperObject
from ccpn._wrapper._Project import Project
from ccpn._wrapper._Chain import Chain
from ccpn._wrapper._Residue import Residue
from ccpn._wrapper._Atom import Atom
from ccpn._wrapper._NmrChain import NmrChain
from ccpn._wrapper._NmrResidue import NmrResidue
from ccpn._wrapper._NmrAtom import NmrAtom
from ccpn._wrapper._ChemicalShiftList import ChemicalShiftList
from ccpn._wrapper._ChemicalShift import ChemicalShift
from ccpn._wrapper._Spectrum import Spectrum
from ccpn._wrapper._SpectrumReference import SpectrumReference
from ccpn._wrapper._PeakList import PeakList
from ccpn._wrapper._Peak import Peak
from ccpn._wrapper._RestraintSet import RestraintSet
from ccpn._wrapper._RestraintList import RestraintList
from ccpn._wrapper._Restraint import Restraint
from ccpn._wrapper._RestraintContribution import RestraintContribution
# from ccpn._wrapper._AbstractRestraintList import AbstractRestraintList
# from ccpn._wrapper._AbstractRestraint import AbstractRestraint
# from ccpn._wrapper._AbstractRestraintContribution import AbstractRestraintContribution
# from ccpn._wrapper._DistanceRestraintList import DistanceRestraintList
# from ccpn._wrapper._DistanceRestraint import DistanceRestraint
# from ccpn._wrapper._DistanceContribution import DistanceContribution
# from ccpn._wrapper._DihedralRestraintList import DihedralRestraintList
# from ccpn._wrapper._DihedralRestraint import DihedralRestraint
# from ccpn._wrapper._DihedralContribution import DihedralContribution
# from ccpn._wrapper._RdcRestraintList import RdcRestraintList
# from ccpn._wrapper._RdcRestraint import RdcRestraint
# from ccpn._wrapper._RdcContribution import RdcContribution
# from ccpn._wrapper._HBondRestraintList import HBondRestraintList
# from ccpn._wrapper._HBondRestraint import HBondRestraint
# from ccpn._wrapper._HBondContribution import HBondContribution

# Set up interclass links and related functions
Project._linkWrapperClasses()


def openProject(path:str, nmrProjectName:str=None) -> Project:
  """Open project at path, and create a wrapper project.

  Will use named nmrProject, first NmrProject if no name given,
  and will create a new NmrProject if none exists"""
  apiProject = ioUtil.loadProject(path)
  if apiProject is None:
    raise ValueError("No valid project loaded from %s" % path )
  else:
    nmrProjects = apiProject.sortedNmrProjects()
    if nmrProjects:
      if nmrProjectName:
        nmrProject = apiProject.findFirstNmrProject(name=nmrProjectName)
        if nmrProject is None:
          raise ValueError("No NmrProject found with name: %s" % nmrProjectName)
      else:
        nmrProject = nmrProjects[0]
    else:
      nmrProject = apiProject.newNmrProject(name=nmrProjectName or 'default')

    return Project(nmrProject)

def newProject(projectName:str, path:str=None) -> Project:
  """Make new project at path, and create a wrapper project"""
  apiProject = ioUtil.newProject(projectName, path, removeExisting=True)
  if apiProject is None:
    raise ValueError("New project could not be created (overlaps exiting project?) name:%s, path:%s"
                     % (projectName, path) )
  else:
    return Project(apiProject.newNmrProject(name=projectName))
