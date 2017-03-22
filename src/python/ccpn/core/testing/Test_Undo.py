"""Module Documentation here

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

from ccpn.core.testing.WrapperTesting import WrapperTesting
from ccpn.util.Undo import Undo


class ComplexUndoTest(WrapperTesting):

  # Path of project to load (None for new project)
  projectPath = 'CcpnCourse2c'

  def test_loaded_project(self):
    project = self.project._wrappedData.root
    project.checkAllValid()

  def test_make_chain_undo(self):
    project = self.project._wrappedData.root
    project._undo = Undo()
    project._undo.newWaypoint()
    molSystem = project.findFirstMolSystem(code='MS1')
    chainA = molSystem.findFirstChain(code='A')
    self.project.blankNotification()
    try:
      chainB = molSystem.newChain(code='X', molecule=chainA.molecule)
      project._undo.undo()
    finally:
      self.project.unblankNotification()
    project.checkAllValid()

  def test_make_chain_undo_redo(self):
    project = self.project._wrappedData.root
    project._undo = Undo()
    project._undo.newWaypoint()
    molSystem = project.findFirstMolSystem(code='MS1')
    chainA = molSystem.findFirstChain(code='A')
    self.project.blankNotification()
    try:
      chainB = molSystem.newChain(code='X', molecule=chainA.molecule)
      project._undo.undo()
      project._undo.redo()
    finally:
      self.project.unblankNotification()
    project.checkAllValid()


  def test_copy_chain_undo(self):
    apiProject = self.project._wrappedData.root
    apiProject._undo = Undo()
    apiProject._undo.newWaypoint()
    molSystem = apiProject.findFirstMolSystem(code='MS1')
    apiChainA = molSystem.findFirstChain(code='A')
    chainA = self.project._data2Obj.get(apiChainA)
    chainB = chainA.clone()
    apiProject._undo.undo()
    apiProject.checkAllValid()

  def test_copy_chain_undo_redo(self):
    apiProject = self.project._wrappedData.root
    apiProject._undo = Undo()
    apiProject._undo.newWaypoint()
    molSystem = apiProject.findFirstMolSystem(code='MS1')
    apiChainA = molSystem.findFirstChain(code='A')
    chainA = self.project._data2Obj.get(apiChainA)
    chainB = chainA.clone()
    apiProject._undo.undo()
    apiProject._undo.redo()
    apiProject.checkAllValid(complete=True)

  def test_delete_residues_undo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      residues = molSystem.findFirstChain(code='A').sortedResidues()
      residues[22].delete()
      residues[45].delete()
      residues[21].delete()
      residues[20].delete()
      project._undo.undo()
      project.checkAllValid()

  def test_delete_residues_undo_redo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      residues = molSystem.findFirstChain(code='A').sortedResidues()
      residues[22].delete()
      residues[45].delete()
      residues[21].delete()
      residues[20].delete()
      project._undo.undo()
      project._undo.redo()
      project.checkAllValid()

  def test_delete_chain_undo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      chain = molSystem.findFirstChain(code='A')
      chain.delete()
      project._undo.undo()
      project.checkAllValid()

  def test_delete_chain_undo_redo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      chain = molSystem.findFirstChain(code='A')
      chain.delete()
      project._undo.undo()
      project._undo.redo()
      project.checkAllValid()

  def test_delete_molSystem_undo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      molSystem.delete()
      project._undo.undo()
      project.checkAllValid()

  def test_delete_molSystem_undo_redo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      molSystem = project.findFirstMolSystem(code='MS1')
      molSystem.delete()
      project._undo.undo()
      project._undo.redo()
      project.checkAllValid()

  def test_delete_resonances_undo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      resonances = project.findFirstNmrProject().sortedResonances()
      for ii in range(1,10):
        resonances[ii].delete()
        resonances[-ii].delete()
      project._undo.undo()
      project.checkAllValid()

  def test_delete_resonances_undo_redo(self):
      project = self.project._wrappedData.root
      project._undo = Undo()
      project._undo.newWaypoint()
      resonances = project.findFirstNmrProject().sortedResonances()
      for ii in range(1,10):
        resonances[ii].delete()
        resonances[-ii].delete()
      project._undo.undo()
      project._undo.redo()
      project.checkAllValid()

