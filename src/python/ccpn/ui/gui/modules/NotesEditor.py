#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan"
               "Simon P Skinner & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:40:40 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Ed Brooksbank $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtGui

from ccpn.ui.gui.modules.CcpnModule import CcpnModule
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.TextEditor import TextEditor
from ccpn.ui.gui.widgets.Widget import Widget
from ccpn.ui.gui.widgets.PulldownListsForObjects import NotesPulldown
from ccpn.ui.gui.widgets.Spacer import Spacer
from ccpn.core.lib.Notifiers import Notifier
from ccpn.core.Note import Note


class NotesEditorModule(CcpnModule):
  """
  This class implements the module for editing the NotesList.
  """
  includeSettingsWidget = False
  maxSettingsState = 2  # states are defined as: 0: invisible, 1: both visible, 2: only settings visible
  settingsPosition = 'top'

  className = 'NotesEditorModule'
  attributeName = 'notes'         # self.project.notes

  def __init__(self, mainWindow=None, name='Notes Editor', note=None):
    """
    Initialise the widgets for the module.
    :param mainWindow: required
    :param name: optional
    :param note: leave as None to let window handle item selection
    """
    CcpnModule.__init__(self, mainWindow=mainWindow, name=name)

    # Derive application, project, and current from mainWindow
    self.mainWindow = mainWindow
    self.application = mainWindow.application
    self.project = mainWindow.application.project
    self.current = mainWindow.application.current
    self.note = note

    self.spacer = Spacer(self.mainWidget, 5, 5
                         , QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed
                         , grid=(0,0), gridSpan=(1,1))
    self.noWidget = NotesPulldown(parent=self.mainWidget
                                   , project=self.project, default=0
                                   , grid=(1,0), gridSpan=(1,1), minimumWidths=(0,100)
                                   , showSelectName=True
                                   , callback=self._selectionPulldownCallback)
    self.spacer = Spacer(self.mainWidget, 5, 5
                         , QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed
                         , grid=(2,0), gridSpan=(1,1))

    #~~~~~~~~~~ define noteWidget box to contain man editing
    self.noteWidget = Widget(self.mainWidget, grid=(3,0), gridSpan=(4,5), setLayout=True)
    self.noteWidget.hide()

    self.label1 = Label(self.noteWidget, text='Note name', grid=(1,0), vAlign='centre', hAlign='right')
    self.lineEdit1 = LineEdit(self.noteWidget, grid=(1,1), gridSpan=(1,2), vAlign='top')
    self.spacer = Spacer(self.noteWidget, 5, 5
                         , QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed
                         , grid=(2,3), gridSpan=(1,1))
    self.textBox = TextEditor(self.noteWidget, grid=(3,0), gridSpan=(1,6))

    if self.note:                            # if note exists then populate the widget
      self.textBox.setText(self.note.text)
      self.lineEdit1.setText(self.note.name)

    self.buttonBox = ButtonList(self.noteWidget, texts=['Apply', 'Delete']
                                , callbacks=[self._applyNote, self._deleteNote]
                                , grid=(6,4), gridSpan=(1,2))
    self.buttonBox.setFixedWidth(self.buttonBox.sizeHint().width()*1.5)
    #~~~~~~~~~~ end of noteWidget box

    # this spacer is expanding, will fill the space when the textbox is invisible
    self.spacer = Spacer(self.mainWidget, 5, 5
                         , QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding
                         , grid=(7,4), gridSpan=(1,1))

    self.mainWidget.setContentsMargins(5, 5, 5, 5)

    self._noteNotifier = None
    self._setNotifier()

  def _setNotifier(self):
    """
    Set a Notifier to call when a note is created/deleted/renamed/changed
    rename calls on name
    change calls on any other attribute
    """
    self._clearNotifier()
    self._noteNotifier = Notifier(self.project
                                  , [Notifier.CREATE, Notifier.DELETE, Notifier.RENAME, Notifier.CHANGE]
                                  , Note.__name__
                                  , self._updateCallback)

  def _clearNotifier(self):
    """
    clean up the notifiers
    """
    if self._noteNotifier is not None:
      self._noteNotifier.unRegister()

  def _applyNote(self):
    """
    Called by clicking the apply button in the module.
    Temporarily disable notifiers, and define commandEchoBlock so all changes
    are treated as a single undo/redo event
    """
    self._clearNotifier()             # disable the notifier while updating object other
    if self.note:                     # calls _updateCallBack during _applyNote
      name = self.lineEdit1.text()
      text = self.textBox.toPlainText()

      self.note._startCommandEchoBlock('_applyNote')

      self.note.rename(name)          # ejb - order doesn't matter inside the commandEchoBlock
      self.note.text = text

      self.note._endCommandEchoBlock()

      self.noWidget.select(self.note.pid)
    self._setNotifier()

  def _reject(self):
    """
    Closes the note editor ignoring all changes.
    """
    self._closeModule()

  def _selectionPulldownCallback(self, item):
    """
    Notifier Callback for selecting Note from the pull down menu
    """
    self.note = self.project.getByPid(item)
    if self.note is not None:
      self._update(self.note)
    else:
      self.noteWidget.hide()

  def _updateCallback(self, data):
    """
    Notifier callback for updating module when a Note is create/delete/rename/change
    """
    thisNoteList = getattr(data[Notifier.THEOBJECT], self.attributeName)   # get the notesList
    modifiedNote = data[Notifier.OBJECT]

    if self.note in thisNoteList:
      self._update(self.note)
    else:
      self.noteWidget.hide()

  def _update(self, note):
    """
    Update the Note widgets
    """
    self.noWidget.select(note.pid)
    self.textBox.setText(note.text)
    self.lineEdit1.setText(note.name)
    self.noteWidget.show()
    self.show()

  def _deleteNote(self):
    """
    Delete the current note with the delete button
    """
    if self.note:
      self.note.delete()

  def _closeModule(self):
    """
    CCPN-INTERNAL: used to close the module
    """
    self._clearNotifier()
    super(NotesEditorModule, self)._closeModule()