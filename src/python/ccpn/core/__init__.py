"""CCPN package. High level interface for normal data access

All data are organised in Projects. The standard ways of starting a project are:

- myProject = :ref:`ccpn-loadProject-ref` (*path*, ...)
- myProject = :ref:`ccpn-newProject-ref` (*projectName*, ...)

Projects are saved by myProject.save(path, ...)

Within the CcpNmr suite there is always a project open, assigned to the variable 'project'.

Module Organisation
-------------------

Class Hierarchy
^^^^^^^^^^^^^^^

Classes are organised in a hierarchy, with all data objects ultimately contained within the Project:

::

  Project
  |       Spectrum
  |       |       SpectrumReference
  |       |       PeakList
  |       |       |       Peak
  |       |       IntegralList
  |       |       |       Integral
  |       |       PseudoDimension
  |       |       SpectrumHit
  |       SpectrumGroup
  |       Sample
  |       |       SampleComponent
  |       Substance
  |       Chain
  |       |       Residue
  |       |       |       Atom
  |       Bond
  |       NmrChain
  |       |       NmrResidue
  |       |       |       NmrAtom
  |       ChemicalShiftList
  |       |       ChemicalShift
  |       DataSet
  |       |       RestraintList
  |       |       |       Restraint
  |       |       |       |       RestraintContribution
  |       |       CalculationStep
  |       |       Data
  |       StructureEnsemble
  |       |       Model
  |       Note


Common Class elements
^^^^^^^^^^^^^^^^^^^^^

All classes in this module are subclasses of the :ref:`ccpn-AbstractWrapperObject-ref`,
and inherit the following elements:

**project** - *ccpn.Project*

The Project (root) containing the object.

**pid** - *ccpn.util.Pid.Pid*

Identifier for the object, unique within the project.
Set automatically from the short class name and object.id
E.g. 'NA:A.102.ALA.CA'

**longPid** - *ccpn.util.Pid.Pid*

Identifier for the object, unique within the project.
Set automatically from the full class name and object.id
E.g. 'NmrAtom:A.102.ALA.CA'

**id** - *str*

Identifier for the object, used to generate the pid and longPid.
Generated by combining the id of the containing object, with the
value of one or more key attributes that uniquely identify the
object in context.
E.g. the id for an Atom, 'A.55.VAL.HA' is generated from:

    - 'A' *Chain.shortName*

    - '55' *Residue.sequenceCode*

    - 'VAL' *Residue.residueType*

    - 'HA' *Atom.name*

**delete()**

Delete object, with all contained objects and underlying data.

**getByPid(pidString)**

Get an arbitrary ccpn.Object from either its pid (e.g. 'SP:HSQC2') or its longPid
(e.g. 'Spectrum:HSQC2'

Returns None for invalid or unrecognised input strings.

**rename(newName)**

Change the object name or other key attribute(s), changing the object id, pid,
and all internal references to maintain consistency.
A number of Objects (Chain, Residue, Atom, Peak, cannot be renamed

Data access
^^^^^^^^^^^

The data of objects are accessed with the normal Python syntax (x = object.value; object.value = x.
There are no public getter and setter functions. For collections you will get an unmodifiable copy
of the internal collection, to prevent accidental modification of the data
(e.g. myPeakList.peaks will return a tuple, not a list)

Each object has a link to the containing object (e.g. myPeakList.spectrum)

Each class has a link to contained objects,
and a function to get a contained object by relative id.
E.g. myProject.peaks, mySpectrum.peaks, and myPeakList.peaks will each get
all peaks contained within the relevant object, sorted by Peak id.
Similarly, a given peak can be found by either myProject.getPeak('HSQC2.1.593'),
mySpectrum.getPeak('1.593'), or myPeakList.getPeak('593')

Most objects can be created using a *newXyzObject* method on the parent.
E.g. you can create a new Restraint object with the myRestraintList.newRestraint(...) function.
'new' functions create a single objects, using the passed-in parameters.
There is no 'newSpectrum' function; spectra are created with 'loadSpectrum' as a complete spectrum
object requires an external file with the data.

More complex object creation is done with 'create...()' functions, that may create multiple
objects, and use heuristics to fill in missing parameters.
E.g. the myRestraintList.createRestraint(....) function creates a Restraint with the
contained RestraintContributions and restraintItems.

Functions whose names start with 'get' (e.g. getNmrAtom(...)) mostly take some kind of identifier
as an argument and returns the identified object if it exists, None otherwise.

Functions whose names start with 'fetch' (e.g. fetchNmrAtom(...)) also take some kind of identifier
as an argument.
These will return the identified object if it exists, but will create a new object otherwise.

Other common prefixes for function names include 'add' and 'remove' (which add and remove
pre-existing objects to collections), 'copy', 'clear', 'load', 'process' and 'toggle',
all of which should be self-explanatory.



.. currentmodule:: ccpn

Module level functions :
------------------------

.. _ccpn-loadProject-ref:

ccpn.loadProject
^^^^^^^^^^^^^^^^

.. autofunction:: ccpn.loadProject

.. _ccpn-newProject-ref:

ccpn.newProject
^^^^^^^^^^^^^^^

.. autofunction:: ccpn.newProject

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Geerten Vuister"
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

import importlib

# Import classes and set to this module
# All classes must be imported in correct order for subsequent code
# to work, as connections between classes are set when child class is imported
# _wrappedClassNames gives import order
_importOrder = [
  'Project',  'Spectrum',  'SpectrumReference',  'SpectrumGroup',  'PeakList',  'Peak',
  'IntegralList',  'Integral',  'PseudoDimension',  'SpectrumHit',  'Sample',  'SampleComponent',
  'Substance',  'Chain',  'Residue', 'Atom',  'Bond',  'NmrChain',  'NmrResidue',  'NmrAtom',
  'ChemicalShiftList',  'ChemicalShift',  'DataSet',  'RestraintList',  'Restraint',
  'RestraintContribution',  'CalculationStep',  'Data',  'StructureEnsemble',  'Model', 'Note'
]
_wrappedClasses = []
for className in _importOrder:
  cls = getattr(importlib.import_module('ccpn.core.%s' % className), className)
  parentClass = cls._parentClass
  if parentClass is not None:
    parentClass._childClasses.append(cls)
  _wrappedClasses.append(cls)

# set main starting functions in namespace. Must be done after importing Project
# to avoid circular import problems
from ccpn.core.lib import Io as ccpnIo

loadProject = ccpnIo.loadProject
newProject = ccpnIo.newProject

# NB Project is _wrappedClasses[0]
_wrappedClasses[0]._linkWrapperClasses()
