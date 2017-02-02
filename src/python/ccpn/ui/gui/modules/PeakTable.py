"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
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
from ccpn.core.Peak import Peak

from ccpn.ui.gui.widgets.Base import Base
from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.Module import CcpnModule
from ccpn.ui.gui.widgets.GroupBox import GroupBox
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.PulldownList import PulldownList

from ccpn.ui.gui.DropBase import DropBase
from ccpn.ui.gui.modules.GuiTableGenerator import GuiTableGenerator
from ccpn.ui.gui.modules.peakUtils import getPeakPosition, getPeakAnnotation, getPeakLinewidth

from ccpn.ui.gui.popups.SelectObjectsPopup import SelectObjectsPopup


from PyQt4 import QtGui, QtCore

UNITS = ['ppm', 'Hz', 'point']

class PeakTable(CcpnModule):

  includeSettingsWidget = True

  def __init__(self, project, selectedList=None):
    CcpnModule.__init__(self, name='Peak List')

    self.application = QtCore.QCoreApplication.instance()._ccpnApplication

    if not project.peakLists:
      project._logger.warn('Project has no peaklists. Peak table cannot be displayed')
      return

    self.checkBoxDict = {}
    self.selectionBox = GroupBox(self.settingsWidget, grid=(0, 0))

    columnsLabel = Label(self.selectionBox, 'Columns to display', grid=(0, 0), gridSpan=(1, 2))

    serialCheckLabel = Label(self.selectionBox, text='Serial', grid=(1, 0), hAlign='r')
    serialCheckBox = self.checkBoxDict['serial'] = CheckBox(self.selectionBox, grid=(1, 1), hAlign='l', checked=True)
    assignCheckLabel = Label(self.selectionBox, text='Assign', grid=(1, 2), hAlign='r')
    assignCheckBox = self.checkBoxDict['assign'] = CheckBox(self.selectionBox, grid=(1, 3), hAlign='l', checked=True)
    positionCheckLabel = Label(self.selectionBox, text='Position', grid=(1, 4), hAlign='r')
    positionCheckBox = self.checkBoxDict['position'] = CheckBox(self.selectionBox, grid=(1, 5), hAlign='l', checked=True)
    heightCheckLabel = Label(self.selectionBox, text='Height', grid=(1, 6), hAlign='r')
    heightCheckBox = self.checkBoxDict['height'] = CheckBox(self.selectionBox, grid=(1, 7), hAlign='l', checked=True)
    volumeCheckLabel = Label(self.selectionBox, text='Volume', grid=(1, 8), hAlign='r')
    volumeCheckBox = self.checkBoxDict['volume'] = CheckBox(self.selectionBox, grid=(1, 9), hAlign='l', checked=True)
    linewidthCheckLabel = Label(self.selectionBox, text='Line Width', grid=(1, 10), hAlign='r')
    linewidthCheckBox = self.checkBoxDict['linewidth'] = CheckBox(self.selectionBox, grid=(1, 11), hAlign='l', checked=False)
    detailsCheckLabel = Label(self.selectionBox, text='Details', grid=(1, 12), hAlign='r')
    detailsCheckBox = self.checkBoxDict['details'] = CheckBox(self.selectionBox, grid=(1, 13), hAlign='l', checked=True)


    self.peakList = PeakListSimple(self.mainWidget, selectedList=selectedList, columnSettings=self.checkBoxDict)
    self.layout.addWidget(self.peakList)
    self.current = self.application.current
    self.settingsButton = self.placeSettingsButton(buttonParent=self.peakList, buttonGrid=(0, 4))

    if self.current.strip:
      peakList = self.current.strip.spectrumViews[0].spectrum.peakLists[0]
      self.peakList.peakListPulldown.setCurrentIndex(self.peakList.peakListPulldown.findText(peakList.pid))

    for checkBox in self.checkBoxDict.values():
      checkBox.toggled.connect(self.peakList.peakTable.updateTable)

  def _closeModule(self):
    """
    Re-implementation of closeModule function from CcpnModule to unregister notification on current.peaks
    """
    #self.current.unRegisterNotify(self.peakList._selectPeakInTable, 'peak')
    self.peakList._deregisterNotifiers()
    self.close()



class PeakListSimple(QtGui.QWidget, DropBase, Base):

  def __init__(self, parent=None, selectedList=None, columnSettings=None, **kw):

      
    QtGui.QWidget.__init__(self, parent)
    Base.__init__(self, **kw)

    self.setMinimumWidth(500)
    self.application = QtCore.QCoreApplication.instance()._ccpnApplication
    self.project = self.application.project
    self.columnSettings = columnSettings

    self.sampledDims = {}
    if not selectedList and self.project.peakLists:
      self.selectedList = self.project.peakLists[0]
    elif not selectedList:
      self.peakLists = []
    else:
      self.selectedList = selectedList
    self.peakLists = self.project.peakLists
    self.label = Label(self, 'Peak List')

    widget1 = QtGui.QWidget(self)
    l = QtGui.QGridLayout()
    widget1.setLayout(l)
    widget1.layout().addWidget(self.label, 0, 0, QtCore.Qt.AlignLeft)
    self.peakListPulldown = PulldownList(self)
    widget1.layout().addWidget(self.peakListPulldown, 0, 1)
    self.layout().addWidget(widget1, 0, 0)

    widget2 = QtGui.QWidget(self)
    l2 = QtGui.QGridLayout()
    widget2.setLayout(l2)
    label = Label(self, ' Position Unit')
    widget2.layout().addWidget(label, 0, 0, QtCore.Qt.AlignLeft)
    self.posUnitPulldown = PulldownList(self, texts=UNITS, callback=self._refreshTable)
    widget2.layout().addWidget(self.posUnitPulldown, 0, 1, QtCore.Qt.AlignLeft)
    self.layout().addWidget(widget2, 0, 1)

    self.subtractPeakListsButton = Button(self, text='Subtract \nPeakLists',
                                          callback=self._subtractPeakLists)

    self.deletePeakButton = Button(self, 'Delete \nSelected', callback=self._deleteSelectedPeaks)
    self.widget3 = QtGui.QWidget(self)
    l3 = QtGui.QGridLayout()
    self.widget3.setLayout(l3)
    self.widget3.layout().addWidget(self.subtractPeakListsButton, 0, 0)
    self.widget3.layout().addWidget(self.deletePeakButton, 0, 1)
    self.layout().addWidget(self.widget3, 0, 2)

    self.peakTable = GuiTableGenerator(self, objectLists=self.peakLists, actionCallback=self._actionCallback, selectionCallback=self._selectionCallback,
                                       getColumnsFunction=self.getExtraColumns, selector=self.peakListPulldown,
                                       multiSelect=True, unitPulldown=self.posUnitPulldown)

    self.layout().addWidget(self.peakTable, 1, 0, 1, 5)
    if selectedList is not None:
      self.peakListPulldown.setCurrentIndex(selectedList)

    self.__registerNotifiers()
    from functools import partial

    self.peakListPulldown.activated[str].connect(self.updateSelectionOnTable)



  def updateSelectionOnTable(self):

    self._selectOnTableCurrentPeaks(self.application.current.peaks)


  def getExtraColumns(self, peakList):

      columns = []

      if self.columnSettings['serial'].isChecked():
        columns.append(('#', 'serial'))

      if self.columnSettings['height'].isChecked():
        columns.append(('Height', lambda pk: pk.height))

      if self.columnSettings['volume'].isChecked():
        columns.append(('Volume', lambda pk: pk.volume))

      tipTexts=['Peak serial number',
              'Magnitude of spectrum intensity at peak center (interpolated), unless user edited',
              'Integral of spectrum intensity around peak location, according to chosen volume method',
              'Textual notes about the peak']
      k = 1
      numDim = peakList.spectrum.dimensionCount

      if self.columnSettings['assign'].isChecked():
        for i in range(numDim):
          j = i + 1
          c = ('Assign F%d' % j, lambda pk, dim=i:getPeakAnnotation(pk, dim))
          columns.insert(k, c)
          tipTexts.insert(k, 'NmrAtom assignments of peak in dimension %d' % j)
          k+=1


      if self.columnSettings['position'].isChecked():
        for i in range(numDim):
          j = i + 1
          sampledDim = self.sampledDims.get(i)
          if sampledDim:
            text = 'Sampled\n%s' % sampledDim.conditionVaried
            tipText='Value of sampled plane'
            unit = sampledDim

          else:
            text = 'Pos F%d' % j
            tipText='Peak position in dimension %d' % j
            unit = self.posUnitPulldown.currentText()
          c = (text, lambda pk, dim=i, unit=unit:getPeakPosition(pk, dim, unit))
          columns.insert(k, c)
          tipTexts.insert(k, tipText)
          k+=1

      if self.columnSettings['linewidth'].isChecked():
        for i in range(numDim):
          j = i + 1
          c = ('LW F%d (Hz)' % j, lambda pk, dim=i:getPeakLinewidth(pk, dim))
          columns.insert(k, c)
          tipTexts.insert(k, 'NmrAtom assignments of peak in dimension %d' % j)
          k+=1

      return columns, tipTexts


  def __registerNotifiers(self):

    self.project.registerNotifier('Peak', 'create', self._refreshPeakTable, onceOnly=True)
    self.project.registerNotifier('Peak', 'modify', self._refreshPeakTable, onceOnly=True)
    self.project.registerNotifier('Peak', 'rename', self._refreshPeakTable, onceOnly=True)
    self.project.registerNotifier('Peak', 'delete', self._refreshPeakTable, onceOnly=True)
    self.project.registerNotifier('PeakList', 'create', self._updatePeakLists, onceOnly=True)
    self.project.registerNotifier('PeakList', 'modify', self._updatePeakLists, onceOnly=True)
    self.project.registerNotifier('PeakList', 'rename', self._updatePeakLists, onceOnly=True)
    self.project.registerNotifier('PeakList', 'delete', self._updatePeakLists, onceOnly=True)
    self.application.current.registerNotify(self._selectOnTableCurrentPeaks, 'peaks')

  def _deregisterNotifiers(self):
    self.project.unRegisterNotifier('Peak', 'create', self._refreshPeakTable)
    self.project.unRegisterNotifier('Peak', 'modify', self._refreshPeakTable)
    self.project.unRegisterNotifier('Peak', 'rename', self._refreshPeakTable)
    self.project.unRegisterNotifier('Peak', 'delete', self._refreshPeakTable)
    self.project.unRegisterNotifier('PeakList', 'create', self._updatePeakLists)
    self.project.unRegisterNotifier('PeakList', 'modify', self._updatePeakLists)
    self.project.unRegisterNotifier('PeakList', 'rename', self._updatePeakLists)
    self.project.unRegisterNotifier('PeakList', 'delete', self._updatePeakLists)
    self.application.current.unRegisterNotify(self._selectOnTableCurrentPeaks, 'peaks')

  def _updatePeakLists(self, value):
    self.peakTable.objectLists = self.project.peakLists
    self.peakTable._updateSelectorContents()


  def _subtractPeakLists(self):
    """
    Subtracts a selected peak list from the peak list currently displayed in the peak table and
    produces a new peak list attached to the spectrum of the selected peak list.
    """

    peakList1 = self.project.getByPid(self.peakListPulldown.currentText())

    availablePeakLists = [peakList for peakList in peakList1.spectrum.peakLists
                         if peakList is not peakList1]

    selectPeakListPopup = SelectObjectsPopup(self, project=self.project, objects=availablePeakLists)
    selectPeakListPopup.exec_()
    for peakList in self.objects:
      peakList1._subtractPeakLists(self.project.getByPid(peakList))
    self.peakTable._updateSelectorContents()


  def _deleteSelectedPeaks(self):

    for peakObject in self.peakTable.table.getSelectedObjects():
      peakObject.delete()

    self._refreshTable()

  def _actionCallback(self, peak, *args):
    ''' If current strip contains the double clicked peak will navigateToPositionInStrip '''
    from ccpn.ui.gui.lib.Strip import navigateToPositionInStrip

    if self.application.current.strip is not None:
        navigateToPositionInStrip(strip = self.application.current.strip, positions=peak.position)
    else:
      self.project._logger.warn('Impossible to navigate to peak position. Set a current strip first')


  def _selectionCallback(self, peaks, *args):
    """
    set as current the selected peaks on the table
    """

    if peaks is None:
      self.application.current.clearPeaks()
    else:
      self.application.current.peaks = peaks

    # if peaks is not None :
    #   self.application.current.peaks = peaks
    #   self._deselectNonCurrentPeaks()
    #   self._selectCurrentPeaks()
    #
    # if peaks is None:
    #   self.application.current.clearPeaks()
    #   self._deselectNonCurrentPeaks()

  #
  # def _selectCurrentPeaks(self):
  #   if len(self.application.current.peaks) >0:
  #     for peak in self.application.current.peaks:
  #       peak.isSelected = True

  # def _deselectNonCurrentPeaks(self):
  #   for peak in self.project.peaks:
  #     if peak not in self.application.current.peaks:
  #       peak.isSelected = False


  def _selectOnTableCurrentPeaks(self, currentPeaks):
    ''' highlight current peaks on the opened peak table '''

    if len(currentPeaks)>0:
      self.peakTable.table._highLightObjs(currentPeaks)
    else:
      self.peakTable.table.clearSelection()


  def _refreshTable(self, item=None):
    # TODO: filter calls to only update if changes to the currently displayed peaklist
    self.peakTable.updateTable()


  def _refreshPeakTable(self, peak, dummy=None):
    # Dummy argument needed as the function is called for rename notifiers
    self.peakTable.updateTable()



