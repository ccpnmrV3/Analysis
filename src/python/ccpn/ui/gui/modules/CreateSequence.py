"""
Module Documentation here
"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = ""
__credits__ = ""
__licence__ = ("")
__reference__ = ("")
#=========================================================================================
# Last code modification:
#=========================================================================================
__modifiedBy__ = "$modifiedBy$"
__dateModified__ = "$dateModified$"
__version__ = "$Revision$"
#=========================================================================================
# Created:
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date$"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtGui
from ccpn.ui.gui.widgets.Base import Base
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.ui.gui.widgets.TextEditor import TextEditor
from ccpn.ui.gui.popups.Dialog import CcpnDialog      # ejb
from ccpn.ui.gui.widgets.ListWidget import ListWidgetSelector
from ccpn.ui.gui.widgets.MessageDialog import showWarning

class CreateSequence(CcpnDialog):
  def __init__(self, parent=None, mainWindow=None, title='Generate Chain', **kw):
    """
    Initialise the widget
    """
    CcpnDialog.__init__(self, parent, setLayout=True, windowTitle=title, **kw)

    self.mainWindow = mainWindow
    self.application = mainWindow.application
    self.project = mainWindow.application.project
    self.current = mainWindow.application.current

    label2a = Label(self, text="Molecule Name", grid=(2, 0))
    moleculeName = LineEdit(self, text="", grid=(2, 1), gridSpan=(1, 1))
    label2b = Label(self, text="Molecule Type", grid=(2, 2))
    self.molTypePulldown = PulldownList(self, grid=(2, 3))
    molTypes = ['protein','DNA', 'RNA']
    self.molTypePulldown.setData(molTypes)
    label3a = Label(self, text="sequence", grid=(3, 0))
    tipText = """Sequence may be entered a set of one letter codes without
                 spaces or a set of three letter codes with spaces inbetween"""
    self.sequenceEditor = TextEditor(self, grid=(3, 1), gridSpan=(1, 3), tipText=tipText)
    label4a = Label(self, 'Sequence Start', grid=(4, 0))
    lineEdit1a = Spinbox(self, grid=(4, 1), value=1, min=-1000000, max=1000000)
    label5a = Label(self, 'Chain code', grid=(4, 2))
    lineEdit2a = LineEdit(self, grid=(4, 3), text='A')

    # self.residueList = ListWidgetSelector(self, setLayout=True, grid=(5,0), gridSpan=(1,4), title='Residue Types')

    buttonBox = ButtonList(self, grid=(6, 3), texts=['Cancel', 'Create Sequence'],
                           callbacks=[self.reject, self._createSequence])
    self.sequenceStart = 1
    self.chainCode = 'A'
    self.sequence = self.sequenceEditor.toPlainText()
    self.moleculeName = None
    moleculeName.textChanged.connect(self._setMoleculeName)
    lineEdit1a.valueChanged.connect(self._setSequenceStart)
    lineEdit2a.textChanged.connect(self._setChainCode)
    self.sequenceEditor.textChanged.connect(self._setSequence)

  def _createSequence(self):
    """
    Creates a sequence using the values specified in the text widget.
    """
    try:
      self.project.createChain(sequence=self.sequence, compoundName=self.moleculeName,
                                   startNumber=self.sequenceStart, shortName=self.chainCode,
                                   molType=self.molTypePulldown.currentText())
      self.accept()
    except Exception as es:
      showWarning('Create Sequence', str(es))

  def _setSequenceStart(self, value:int):
    """
    Sets sequence start for sequence being created
    """
    self.sequenceStart = int(value)

  def _setChainCode(self, value:str):
    """
    Sets chain code for sequence being created.
    """
    self.chainCode = value

  def _setSequence(self):

    sequence = self.sequenceEditor.toPlainText()
    if not ' ' in sequence:
      self.sequence = self.sequenceEditor.toPlainText()
    else:
      self.sequence = tuple(sequence.split())

  def _setMoleculeName(self, value:str):
    """
    Sets name of molecule being created.
    """
    self.moleculeName = value


