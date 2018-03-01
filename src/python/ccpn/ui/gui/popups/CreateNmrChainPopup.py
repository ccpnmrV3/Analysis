"""
Module Documentation here
"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Luca Mureddu $"
__dateModified__ = "$dateModified: 2018-02-07 15:28:41 +0000 (Wed, February 02, 2018) $"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Luca Mureddu $"
__date__ = "$Date: 2018-02-07 15:28:41 +0000 (Wed, February 02, 2018) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt5 import QtGui, QtWidgets, QtCore

from ccpn.ui.gui.widgets.Base import Base
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.popups.Dialog import CcpnDialog      # ejb
from ccpn.ui.gui.widgets.RadioButtons import RadioButtons
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.TextEditor import TextEditor
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.PulldownListsForObjects import NmrChainPulldown, ChainPulldown, SELECT
from ccpn.core.NmrChain import NmrChain
from ccpn.core.Chain import Chain
from ccpn.util.Logging import getLogger

New, FromChain, FromNmrChain, = 'Empty', 'Chain', 'NmrChain'
SelectionOptions = [New, FromChain, FromNmrChain]

ATOM_TYPES = ['H', 'N', 'CA', 'CB', 'CO', 'HA', 'HB']

class CreateNmrChainPopup(CcpnDialog):
  def __init__(self, parent=None, mainWindow=None
               , title='Create NmrChain', **kw):
    CcpnDialog.__init__(self, parent, setLayout=True, windowTitle=title, **kw)

    self.parent = parent
    self.mainWindow = mainWindow
    self.project = None
    if self.mainWindow:
      self.project = self.mainWindow.project


    # GUI
    self.getLayout().setContentsMargins(15, 20, 25, 10)  # L,T,R,B
    vGrid = 0
    self.newFromLabel = Label(self, text="New from", grid=(vGrid,0))
    self.newNChainOptionsRButtons = RadioButtons(self, texts=SelectionOptions,
                                                 selectedInd=0,
                                                 callback=self._showOptions,
                                                 direction='v',
                                                 tipTexts=None,
                                                 grid=(vGrid, 1))
    vGrid += 1


    self.availableChainsPD = ChainPulldown(self, self.project,showSelectName=True, callback=self._populateWidgets, labelText='', grid=(vGrid, 1))
    self.availableChainsPD.label.hide()
    self.availableChainsPD.hide()
    vGrid += 1
    self.availableNmrChainsPD = NmrChainPulldown(self, self.project,showSelectName=True, callback=self._populateWidgets, labelText='', grid=(vGrid, 1))
    self.availableNmrChainsPD.label.hide()
    self.availableNmrChainsPD.hide()

    self.pulldownsOptions = {FromNmrChain:self.availableNmrChainsPD, FromChain:self.availableChainsPD}

    vGrid += 1
    self.labelName = Label(self, text="Name", grid=(vGrid, 0), )
    self.nameLineEdit = LineEdit(self, grid=(vGrid, 1), )

    vGrid += 1
    self.labelSequenceEditor = Label(self, text="Sequence", grid=(vGrid, 0),)

    tipText = """Sequence may be entered a set of one letter codes without
                     spaces or a set of three letter codes with spaces inbetween"""
    self.sequenceEditor = TextEditor(self, grid=(vGrid, 1), tipText=tipText)

    vGrid += 1
    self.labelBackboneAtoms = Label(self, text="Add backbone atoms", grid=(vGrid, 0), )
    self.checkboxBackboneAtoms = CheckBox(self, checked=True, grid=(vGrid, 1), )

    vGrid += 1
    self.labelSidechainAtoms = Label(self, text="Add sidechain atoms", grid=(vGrid, 0), )
    self.checkboxSideChainsAtoms = CheckBox(self, checked=True, grid=(vGrid, 1))
    # end

    vGrid += 1
    self.spacerLabel = Label(self, text="", grid=(vGrid,0))
    vGrid += 1

    self.spacerLabel = Label(self, text="", grid=(vGrid, 0))
    self.buttonBox = ButtonList(self, callbacks=[self.reject, self._createNmrChain], texts=['Cancel', 'Ok'], grid=(vGrid, 1))

    self._chain = None # used to create a new nmrChain from a previous one
    self._nmrChain  = None
    self._activateOptions()

  def _createNmrChain(self):
    nmrChainSequence = self.sequenceEditor.toPlainText()
    name = self.nameLineEdit.get()
    addBackboneAtoms =  self.checkboxBackboneAtoms.get()
    addSideChainAtoms = self.checkboxSideChainsAtoms.get()

    if self.project:
      # self.project.blankNotification()

      selectedOption = self.newNChainOptionsRButtons.getSelectedText()

      newNmrChain = self.project.newNmrChain()

      if self._chain:
        chainSequence = ''.join([residue.shortName for residue in self._chain.residues])
        if len(chainSequence) == len(nmrChainSequence):
          try:
            self.project._startCommandEchoBlock('_createNmrChain')
            for residue, ss in zip(self._chain.residues, nmrChainSequence):
              if residue.shortName == ss:
                nmrResidue = newNmrChain.newNmrResidue(sequenceCode=residue.sequenceCode, residueType=residue.shortName)
                nmrResidue.residue = residue
              else:
                nmrResidue = newNmrChain.newNmrResidue(sequenceCode=residue.sequenceCode, residueType=ss)
              if addBackboneAtoms:
                for atom in residue.atoms:
                  if atom.name in ATOM_TYPES:
                    nmrResidue.fetchNmrAtom(atom.name)
            if len(newNmrChain.nmrResidues) == 0:
              newNmrChain.delete() # no reason to keep an empty chain!
          finally:
            self.project._endCommandEchoBlock()
        else:
          for ss in nmrChainSequence:
            nmrResidue = newNmrChain.newNmrResidue(sequenceCode=None, residueType=ss)

      elif self._nmrChain:
        selectedNmrchainSequence = ''.join([residue.residueType for residue in self._nmrChain.nmrResidues])
        if len(selectedNmrchainSequence) == len(nmrChainSequence):
          try:
            self.project._startCommandEchoBlock('_createNmrChain')
            for nmrResidue, ss in zip(self._nmrChain.nmrResidues, nmrChainSequence):
              if nmrResidue.residueType == ss:
                newNmrResidue = newNmrChain.newNmrResidue(sequenceCode=nmrResidue.sequenceCode, residueType=nmrResidue.residueType)
                for nmrAtom in nmrResidue.nmrAtoms:
                  newNmrAtom = self.project.fetchNmrAtom(nmrAtom.name)
              else:
                newNmrResidue = newNmrChain.newNmrResidue(sequenceCode=nmrResidue.sequenceCode, residueType=ss)

          finally:
            self.project._endCommandEchoBlock()
      else:
        for ss in  nmrChainSequence:
          nmrResidue = newNmrChain.newNmrResidue(residueType=ss)

      try:
        newNmrChain.rename(newNmrChain.shortName + '-' + name)
      except Exception as e:
        getLogger().warn(e)




  def _populateWidgets(self, selected):
    obj = self.project.getByPid(selected)
    if isinstance(obj, NmrChain):
      self.nameLineEdit.clear()
      self.sequenceEditor.clear()
      self.nameLineEdit.setText(obj.shortName)
      self.sequenceEditor.setText(''.join([r.residueType for r in obj.nmrResidues]))
      self._nmrChain = obj

    if isinstance(obj, Chain):
      self.nameLineEdit.clear()
      self.sequenceEditor.clear()
      self.nameLineEdit.setText(obj.shortName)
      self.sequenceEditor.setText(''.join([r.shortName for r in obj.residues]))
      self._chain = obj


  def _activateOptions(self):
    # if self.availableNmrChainsPD.textList is None:

    # self.newNChainOptionsRButtons.radioButtons[2].setEnabled(False)
    if self.availableChainsPD.textList is None:
      self.newNChainOptionsRButtons.radioButtons[1].setEnabled(False)

  def _showOptions(self):
    selected = self.newNChainOptionsRButtons.getSelectedText()
    # needs to clear the previous selection otherwise has an odd behaviour from pulldownNofiers which remember the previous selection
    for pd in self.pulldownsOptions:
      self.pulldownsOptions[pd].select(SELECT)
      self._chain = None
    if selected in self.pulldownsOptions:
      self.pulldownsOptions[selected].show()
    hs = [x for x in self.pulldownsOptions if x != selected]
    for h in hs:
      self.pulldownsOptions[h].hide()



if __name__ == '__main__':
    from ccpn.ui.gui.widgets.Application import TestApplication
    from ccpn.ui.gui.popups.Dialog import CcpnDialog
    from ccpn.ui.gui.widgets.Widget import Widget


    app = TestApplication()
    popup = CreateNmrChainPopup()
    widget = Widget(parent=popup, grid=(0,0))

    popup.show()
    popup.raise_()
    app.start()
