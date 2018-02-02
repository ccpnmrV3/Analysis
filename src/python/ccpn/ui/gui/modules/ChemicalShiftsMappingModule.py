"""
Module Documentation here
# TODO : when update module, keep focus on selected item in the table, keep same zoom on the plot
check zoom

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
__dateModified__ = "$dateModified: 2017-07-07 16:32:46 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Luca Mureddu $"
__date__ = "$Date: 2017-04-07 10:28:43 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import numpy as np
from ccpn.ui.gui.modules.CcpnModule import CcpnModule
from ccpn.ui.gui.modules.NmrResidueTable import NmrResidueTable
from ccpn.ui.gui.widgets.BarGraph import BarGraph, CustomViewBox , CustomLabel
from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.ui.gui.widgets.SpectraSelectionWidget import SpectraSelectionWidget
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.RadioButtons import RadioButtons
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.ScrollArea import ScrollArea
from ccpn.ui.gui.widgets.FileDialog import LineEditButtonDialog
from ccpn.ui.gui.widgets.Spacer import Spacer
from ccpn.ui.gui.widgets.Column import Column, ColumnClass
from ccpn.core.lib.Notifiers import Notifier
from ccpn.util.Colour import spectrumColours, hexToRgb
from ccpn.util.Scripting import getScriptsDirectoryPath
from ccpn.ui.gui.widgets.Table import ObjectTable, Column
from ccpn.core.lib.peakUtils import getDeltaShiftsNmrResidue
from ccpn.core.lib import CcpnSorting
from ccpn.util.Logging import getLogger
from ccpn.ui.gui.widgets.BarGraphWidget import BarGraphWidget
from ccpn.ui.gui.widgets import MessageDialog
from ccpn.ui.gui.widgets.Splitter import Splitter
from ccpn.ui.gui.widgets.Icon import Icon
from ccpn.util import Colour
import random

def chemicalShiftMappingPymolTemplate(filePath, pdbPath, aboveThresholdResidues, belowThresholdResidues,
                                      missingdResidues, colourMissing, colourAboveThreshold,
                                      colourBelowThreshold, selection):

  if os.path.exists(pdbPath):
    warn = 'This script is auto-generated. Any changes here will be lost.'
    with open(filePath, 'w') as f:
      f.write('''\n"""''' + warn + '''"""''')
      f.write('''\nfrom pymol import cmd''')
      f.write('''\n''')
      f.write('''\ncmd.load("''' + pdbPath + '''") ''')
      f.write('''\ncmd.hide('lines')''')
      f.write('''\ncmd.show('cartoon')''')
      f.write('''\ncmd.color('white')''')
      f.write('''\ncmd.select('aboveThreshold', 'res  ''' + aboveThresholdResidues + ''' ')''')
      f.write('''\ncmd.set_color("AboveColour", " ''' + str(colourAboveThreshold) + ''' ")''')
      f.write('''\ncmd.color('AboveColour', 'aboveThreshold')''')
      f.write('''\ncmd.select('belowThreshold', 'res  ''' + belowThresholdResidues + ''' ')''')
      f.write('''\ncmd.set_color("BelowColour", " ''' + str(colourBelowThreshold) + ''' ")''')
      f.write('''\ncmd.color('BelowColour', 'belowThreshold')''')
      f.write('''\ncmd.select('missing', 'res  ''' + missingdResidues + ''' ')''')
      f.write('''\ncmd.set_color("MissingColour", " ''' + str(colourMissing) + ''' ")''')
      f.write('''\ncmd.color('MissingColour', 'missing')''')
      if len(selection)>0:
        f.write('''\ncmd.select('Selected', 'res  ''' + selection + ''' ')''')
      else:
        f.write('''\ncmd.deselect()''')

  return filePath

DefaultAtoms = ['H', 'N']
DefaultAtomWeight = {'H':7.00, 'N':1.00, 'C':4.00, 'Other':1.00}
DefaultThreshould = 0.1
LightColourSchemeCurrentLabel = '#3333ff'
DarkColourSchemeCurrentLabel = '#00ff00'
PymolScriptName = 'chemicalShiftMapping_Pymol_Template.py'


class CustomNmrResidueTable(NmrResidueTable):
  """
  Custon nmrResidue Table with extra Delta Shifts column
  """
  deltaShiftsColumn = ('Delta Shifts', lambda nmrResidue: nmrResidue._deltaShift, '', None)

  # columnDefs = [
  #   ('#', lambda nmrResidue: nmrResidue.serial, 'NmrResidue serial number', None),
  #   ('Index', lambda nmrResidue: NmrResidueTable._nmrIndex(nmrResidue), 'Index of NmrResidue in the NmrChain', None),
  #   ('Sequence', lambda nmrResidue: nmrResidue.sequenceCode, 'Sequence code of NmrResidue', None),
  #   ('Type', lambda nmrResidue: nmrResidue.residueType, 'NmrResidue type', None),
  #   ('Selected NmrAtoms', lambda nmrResidue: CustomNmrResidueTable._getSelectedNmrAtomNames(nmrResidue), 'NmrAtoms selected in NmrResidue', None),
  #   ('Selected Spectra count', lambda nmrResidue: CustomNmrResidueTable._getNmrResidueSpectraCount(nmrResidue)
  #    , 'Number of spectra selected for calculating the delta shift', None),
  #   ('Delta Shifts', lambda nmrResidue: nmrResidue._deltaShift, '', None),
  #   ('Comment', lambda nmr: NmrResidueTable._getCommentText(nmr), 'Notes', lambda nmr, value: NmrResidueTable._setComment(nmr, value))
  # ]
  #
  # columnDefs = NmrResidueTable.columnDefs+[deltaShiftsColumn,]
  # columnDefs[-1], columnDefs[-2] = columnDefs[-2], columnDefs[-1]

  def __init__(self, parent=None, mainWindow=None, moduleParent=None, actionCallback=None, selectionCallback=None,
               checkBoxCallback=None, nmrChain=None, **kwds):

    # NmrResidueTable.__init__(self, parent=parent, application=application,actionCallback=actionCallback,
    #                          selectionCallback=selectionCallback, nmrChain=nmrChain, multiSelect = True, **kwds)

    NmrResidueTable.__init__(self, parent=parent, mainWindow=mainWindow
                             , moduleParent=moduleParent
                             , actionCallback=actionCallback
                             , selectionCallback=selectionCallback
                             , checkBoxCallback = checkBoxCallback
                             , nmrChain=nmrChain
                             , multiSelect=True,
                             **kwds)

    self.NMRcolumns = ColumnClass([
        ('#', lambda nmrResidue: nmrResidue.serial, 'NmrResidue serial number', None),
        ('Pid', lambda nmrResidue:nmrResidue.pid, 'Pid of NmrResidue', None),
        ('_object', lambda nmrResidue:nmrResidue, 'Object', None),
        ('Index', lambda nmrResidue: NmrResidueTable._nmrIndex(nmrResidue), 'Index of NmrResidue in the NmrChain', None),
        ('Sequence', lambda nmrResidue: nmrResidue.sequenceCode, 'Sequence code of NmrResidue', None),
        ('Type', lambda nmrResidue: nmrResidue.residueType, 'NmrResidue type', None),
        ('Selected NmrAtoms', lambda nmrResidue: CustomNmrResidueTable._getSelectedNmrAtomNames(nmrResidue), 'NmrAtoms selected in NmrResidue', None),
        ('Selected Spectra count', lambda nmrResidue: CustomNmrResidueTable._getNmrResidueSpectraCount(nmrResidue)
         , 'Number of spectra selected for calculating the delta shift', None),
        ('Delta Shifts', lambda nmrResidue: nmrResidue._deltaShift, '', None),
        ('include in Map', lambda nmrResidue: nmrResidue._includeInDeltaShift, 'Include this residue in the Mapping calculation', lambda nmr, value: CustomNmrResidueTable._setChecked(nmr, value)),
        # ('Flag', lambda nmrResidue: nmrResidue._flag,  '',  None),
        ('Comment', lambda nmr: NmrResidueTable._getCommentText(nmr), 'Notes', lambda nmr, value: NmrResidueTable._setComment(nmr, value))
      ])        #[Column(colName, func, tipText=tipText, setEditValue=editValue) for colName, func, tipText, editValue in self.columnDefs]

    self._widget.setFixedHeight(45)


  @staticmethod
  def _setChecked(obj, value):
    """
    CCPN-INTERNAL: Insert a comment into QuickTable
    """

    obj._includeInDeltaShift = value
    obj._finaliseAction('change')

  @staticmethod
  def _getNmrResidueSpectraCount(nmrResidue):

    """
    CCPN-INTERNAL: Insert an index into ObjectTable
    """
    try:
      return nmrResidue.spectraCount
    except:
      return None

  @staticmethod
  def _getSelectedNmrAtomNames(nmrResidue):

    """
    CCPN-INTERNAL: Insert an index into ObjectTable
    """
    try:
      return ', '.join(nmrResidue.selectedNmrAtomNames)
    except:
      return None


class ChemicalShiftsMapping(CcpnModule):

  includeSettingsWidget = True
  maxSettingsState = 2  # states are defined as: 0: invisible, 1: both visible, 2: only settings visible
  settingsPosition = 'left'
  className = 'ChemicalShiftsMapping'

  def __init__(self, mainWindow, name='Chemical Shift Mapping', nmrChain= None, **kw):
    CcpnModule.__init__(self, mainWindow=mainWindow, name=name, settingButton=True)

    BarGraph.mouseClickEvent = self._mouseClickEvent
    BarGraph.mouseDoubleClickEvent = self._mouseDoubleClickEvent

    self.mainWindow = mainWindow
    self.application = None
    self.OtherAtoms = set()
    self.Natoms = set()
    self.Hatoms = set()
    self.Catoms = set()
    self.atomCheckBoxes = []
    self.atomWeightSpinBoxes = []
    self.atomRadioButtons = []
    self.atomNames = []
    if self.mainWindow is not None:
      self.project = self.mainWindow.project
      self.application = self.mainWindow.application
      self.current = self.application.current

      if len(self.project.nmrResidues):

        for i in self.project.nmrResidues:
          for atom in i.nmrAtoms:
            # self.atoms.add(atom.name)
            if 'N' in atom.name:
              self.Natoms.add(atom.name)
              self.atomNames.append('N')
            if 'H' in atom.name:
              self.Hatoms.add(atom.name)
              self.atomNames.append('H')
            if 'C' in atom.name:
              self.Hatoms.add(atom.name)
              self.atomNames.append('C')
            else:
              self.OtherAtoms.add(atom.name)
              self.atomNames.append('Others')


    self.thresholdLinePos = DefaultThreshould

    self.showStructureIcon = Icon('icons/showStructure')
    self.updateIcon = Icon('icons/update')

    self._setWidgets()
    self._setSettingsWidgets()
    if self.mainWindow:
      self._selectCurrentNmrResiduesNotifier = Notifier(self.current , [Notifier.CURRENT] , targetName='nmrResidues'
                                                       , callback=self._selectCurrentNmrResiduesNotifierCallback)
      self._peakDeletedNotifier = Notifier(self.project, [Notifier.DELETE], 'Peak',
                                                self._peakDeletedCallBack)

      # self._peakChangedNotifier = Notifier(self.project, [Notifier.CHANGE], 'Peak',
      #                                        self._peakChangedCallBack, onceOnly=True)
      # self._peakChangedNotifier.lastPeakPos = None

      self._nrChangedNotifier = Notifier(self.project, [Notifier.CHANGE, Notifier.DELETE], 'NmrResidue',
                                           self._nmrResidueChanged)
      self._nrDeletedNotifier = Notifier(self.project, [Notifier.CHANGE, Notifier.DELETE], 'NmrResidue',
                                         self._nmrResidueDeleted)

      if self.project:
        if len(self.project.nmrChains) > 0:
          self.nmrResidueTable.ncWidget.select(self.project.nmrChains[-1].pid)
          self._setThresholdLineBySTD()

  def _setWidgets(self):
    self.nmrResidueTable = None
    self.barGraphWidget = None

    if self.application:
      self.splitter = Splitter(QtCore.Qt.Vertical)

      self.barGraphWidget = BarGraphWidget(self.mainWidget, application=self.application, grid = (1, 0))

      self.barGraphWidget.xLine.setPos(DefaultThreshould)
      self.barGraphWidget.customViewBox.mouseClickEvent = self._viewboxMouseClickEvent
      self.nmrResidueTable = CustomNmrResidueTable(parent=self.mainWidget, mainWindow=self.mainWindow,
                                                   actionCallback= self._customActionCallBack, checkBoxCallback=self._checkBoxCallback,
                                                   setLayout=True, grid = (0, 0))
      self.showOnViewerButton = Button(self.nmrResidueTable._widget, tipText='Show on Molecular Viewer',
                                       icon=self.showStructureIcon,
                                       callback=self._showOnMolecularViewer,
                                       grid = (1, 1), hAlign='l')
      self.showOnViewerButton.setFixedHeight(25)

      self.updateButton1 = Button(self.nmrResidueTable._widget, text='', icon=self.updateIcon,
                                  tipText='Update all', callback=self.updateModule,
                                 grid=(1, 2), hAlign='r' )
      self.updateButton1.setFixedHeight(25)
      # self.showOnViewerButton.setFixedWidth(150)

      self.nmrResidueTable.displayTableForNmrChain = self._displayTableForNmrChain
      self.barGraphWidget.customViewBox.selectAboveThreshold = self._selectNmrResiduesAboveThreshold

      self.splitter.addWidget(self.nmrResidueTable)
      self.splitter.addWidget(self.barGraphWidget)
      self.mainWidget.getLayout().addWidget(self.splitter)
      self.mainWidget.setContentsMargins(5, 5, 5, 5)  # l,t,r,b

  def _checkSpectraWithPeakListsOnly(self):
    for cb in self.spectraSelectionWidget.allSpectraCheckBoxes:
      sp = self.project.getByPid(cb.text())
      lsts = []
      if sp:
        for pl in sp.peakLists:
          if len(pl.peaks)>0:
            lsts.append(True)
      if not any(lsts):
        cb.setChecked(False)

  def _setSettingsWidgets(self):

    self.scrollArea = ScrollArea(self, setLayout=False, )
    self.scrollArea.setWidgetResizable(True)
    self.scrollAreaWidgetContents = Frame(self, setLayout=True)
    self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    # self.scrollAreaWidgetContents.getLayout().setAlignment(QtCore.Qt.AlignTop)
    self.settingsWidget.getLayout().addWidget(self.scrollArea)
    self.scrollArea.setContentsMargins(10, 10, 10, 15) #l,t,r,b
    self.scrollAreaWidgetContents.setContentsMargins(10, 10, 10, 15) #l,t,r,b

    i = 0
    self.inputLabel = Label(self.scrollAreaWidgetContents, text='Select Data Input', grid=(i, 0), vAlign='t')
    self.spectraSelectionWidget = SpectraSelectionWidget(self.scrollAreaWidgetContents, parent=self.mainWindow, mainWindow=self.mainWindow, grid=(i,1), gridSpan=(1,2))
    self._checkSpectraWithPeakListsOnly()

    # self.spectraSelectionWidget.setMaximumHeight(150)
    i += 2
    self.atomWeightLabel = Label(self.scrollAreaWidgetContents, text='Relative Contribution ', grid=(i, 0))
    j = 0

    self._scrollAreaSpinBoxFrame = Frame(self.scrollAreaWidgetContents, setLayout=True, grid=(i, 1))
    i += 1

    # original by Luca
    # for k in sorted(DefaultAtomWeight.keys(), key=CcpnSorting.stringSortKey):
    #   if k in self.atomNames:
    #     j += 1
    #     # weightLabel = Label(self.scrollAreaWidgetContents, text=str(k), grid=(i, j), hAlign='l')
    #     self.atomWeightSpinBox = Spinbox(self.scrollAreaWidgetContents, value=DefaultAtomWeight[k],
    #                                      prefix=str(k+(' '*10)), grid=(i,j), hAlign='l')
    #     self.atomWeightSpinBox.setObjectName(str(k))
    #     self.atomWeightSpinBoxes.append(self.atomWeightSpinBox)
    #     j += 1

    # slight change by Ed
    j = 0
    for k in sorted(DefaultAtomWeight.keys(), key=CcpnSorting.stringSortKey):
      if k in self.atomNames:
        self.atomWeightSpinBox = DoubleSpinbox(self._scrollAreaSpinBoxFrame, value=DefaultAtomWeight[k],
                                         prefix=str(k+(' '*10)), grid=(0, j), hAlign='l')
        self.atomWeightSpinBox.setObjectName(str(k))
        self.atomWeightSpinBoxes.append(self.atomWeightSpinBox)
        j += 1

    i += 1
    self.atomLabel = Label(self.scrollAreaWidgetContents,text='Select Atoms', grid=(i,0))
    col = 1
    if len(self.Hatoms)>0:
      self._addAtomCheckBoxes(self.Hatoms, i, col)
      col += 1
    if len(self.Natoms)>0:
      self._addAtomCheckBoxes(self.Natoms, i, col)
      col += 1
    if len(self.Catoms)>0:
      self._addAtomCheckBoxes(self.Catoms, i, col)
      col += 1
    if len(self.OtherAtoms)>0:
      self._addAtomCheckBoxes(self.Catoms, i, col)
      col += 1
    i = max([len(self.Hatoms),len(self.Natoms),len(self.Catoms),len(self.OtherAtoms)])

    i += 1
    self.thresholdLAbel = Label(self.scrollAreaWidgetContents, text='Threshold value', grid=(i, 0))
    self.thresholdSpinBox = DoubleSpinbox(self.scrollAreaWidgetContents, value=DefaultThreshould, step=0.01,
                                          decimals=3, callback=self.updateThresholdLineValue, tipText = 'Deafult: STD of delta shifts',
                                          grid=(i, 1))
    i += 1
    self.aboveThresholdColourLabel =  Label(self.scrollAreaWidgetContents,text='Above Threshold Colour', grid=(i,0))
    self.aboveThresholdColourBox = PulldownList(self.scrollAreaWidgetContents,  grid=(i, 1))
    for item in spectrumColours.items():
      pix = QtGui.QPixmap(QtCore.QSize(20, 20))
      pix.fill(QtGui.QColor(item[0]))
      self.aboveThresholdColourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
    self.aboveThresholdColourBox.select(list(spectrumColours.values())[-1])

    i += 1
    self.belowThresholdColourLabel = Label(self.scrollAreaWidgetContents, text='Below Threshold Colour', grid=(i, 0))
    self.belowThresholdColourBox = PulldownList(self.scrollAreaWidgetContents, grid=(i, 1))
    for item in spectrumColours.items():
      pix = QtGui.QPixmap(QtCore.QSize(20, 20))
      pix.fill(QtGui.QColor(item[0]))
      self.belowThresholdColourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
    self.belowThresholdColourBox.setCurrentIndex(0)

    i += 1
    disappearedTipText = 'Mark NmrResidue bar with selected colour where assigned peaks have disapperead from the spectra'
    self.disappearedColourLabel = Label(self.scrollAreaWidgetContents, text='Disappeared Peaks Colour', grid=(i, 0))
    self.disappearedColourBox = PulldownList(self.scrollAreaWidgetContents, grid=(i, 1))
    for item in spectrumColours.items():
      pix = QtGui.QPixmap(QtCore.QSize(20, 20))
      pix.fill(QtGui.QColor(item[0]))
      self.disappearedColourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
    try:
      self.disappearedColourBox.select('dark grey')
    except:
      self.disappearedColourBox.select(random.choice(self.disappearedColourBox.texts))

    i += 1
    self.disappearedBarThreshold = Label(self.scrollAreaWidgetContents, text='Disappeared value', grid=(i, 0))
    self.disappearedBarThresholdSpinBox = DoubleSpinbox(self.scrollAreaWidgetContents, value=1, step=0.01,
                                          decimals=3, callback=None, grid=(i, 1))
    i += 1


    # molecular Structure
    self.molecularStructure= Label(self.scrollAreaWidgetContents, text='Molecular Structure', grid=(i, 0))
    texts = ['PDB','CCPN Ensembles','Fetch From Server']
    self.molecularStructureRadioButton = RadioButtons(self.scrollAreaWidgetContents, texts=texts, direction='h',
                                        grid=(i, 1))
    self.molecularStructureRadioButton.set(texts[0])
    self.molecularStructureRadioButton.setEnabled(False)
    self.molecularStructureRadioButton.setToolTip('Not implemented yet')

    i += 1
    self.mvWidgetContents = Frame(self.scrollAreaWidgetContents, setLayout=True, grid=(i, 1))
    self.pdbLabel = Label(self.mvWidgetContents, text='PDB File Path', grid=(0, 0))
    scriptPath = None
    if self.mainWindow:
      scriptPath = os.path.join(getScriptsDirectoryPath(self.project),'pymol')

    self.pathPDB = LineEditButtonDialog(self.mvWidgetContents, textDialog='Select PDB File',
                                        filter="PDB files (*.pdb)", directory=scriptPath, grid=(0,1))


    i += 1

    self.updateButton = Button(self.scrollAreaWidgetContents, text='Update All', callback=self.updateModule,
                               grid=(i, 1),  gridSpan=(i, 2))
    i += 1
    Spacer(self.scrollAreaWidgetContents, 3, 3
           , QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
           , grid=(i,3), gridSpan=(1,1))

  def _setThresholdLineBySTD(self):
    nc = self.project.getByPid(self.nmrResidueTable.ncWidget.getText())
    if nc:
      deltaShifts = [ n._deltaShift for n in nc.nmrResidues]
      if len(deltaShifts)>0:
        if not None in deltaShifts:
          std = np.std(deltaShifts)
          if std:
            self.thresholdLinePos = std
            self.thresholdSpinBox.set(std)

  def _addAtomCheckBoxes(self, atoms, rowPos, colPos ):
    texts = sorted(atoms, key=CcpnSorting.stringSortKey)
    self.atomRadioButton = RadioButtons(self.scrollAreaWidgetContents, texts=texts, direction='v', grid=(rowPos, colPos))
    self.atomRadioButtons.append(self.atomRadioButton)
    if len(texts)>0:
      self.atomRadioButton.radioButtons[0].setChecked(True)

  def updateTable(self, nmrChain):
    self.nmrResidueTable.ncWidget.select(nmrChain.pid)
    # self.nmrResidueTable.setColumns(self.nmrResidueTable.NMRcolumns)

    # self.nmrResidueTable.setObjects([nr for nr in nmrChain.nmrResidues if nr._deltaShift])

    self.nmrResidueTable._update(nmrChain)

    self.nmrResidueTable._selectOnTableCurrentNmrResidues(self.current.nmrResidues)

  def _displayTableForNmrChain(self, nmrChain):
    self.updateModule()

    # self.updateTable(nmrChain)
    # self.updateBarGraph()

  def _peakDeletedCallBack(self, data):
    if len(self.current.peaks) == 0:
      self.updateModule()

  # def _peakChangedCallBack(self, data):
  #
  #   peak = data[Notifier.OBJECT]
  #   if self._peakChangedNotifier.lastPeakPos != peak.position:
  #     self._peakChangedNotifier.lastPeakPos = peak.position
  #     self.updateModule()

  def _checkBoxCallback(self, data):
    '''
    Callback from checkboxes inside a table
    '''
    # objs = data[Notifier.OBJECT]

    # itemSelection = data['rowItem']
    # att = self.nmrResidueTable.horizontalHeaderItem(itemSelection.column()).text()
    # if att == 'Included':
    # objs = data[Notifier.OBJECT]
    # print(objs)
    # if objs:
    #   obj = objs[0]
    # #     print(obj)
    # #   obj._includeInDeltaShift = data['checked']
    #   obj._finaliseAction('change')
    # self.updateModule()
    pass
    # print(data)

  def _nmrResidueChanged(self, data):
    nmrResidue =  data[Notifier.OBJECT]
    self.updateModule()

  def _nmrResidueDeleted(self, data):
    if len(self.current.nmrResidues) == 0:
      self.updateModule()

  def _selectNmrResiduesAboveThreshold(self):
    if self.aboveObjects:
      self.current.nmrResidues = self.aboveObjects

  def updateBarGraph(self):
    xs = []
    ys = []
    obs = []
    self.disappearedX = []
    self.disappearedY = []
    self.disappereadObjects = []
    self.aboveX = []
    self.aboveY = []
    self.aboveObjects = []
    self.belowX = []
    self.belowY = []
    self.belowObjects = []
    self.aboveBrush = 'g'
    self.belowBrush = 'r'
    self.disappearedPeakBrush = 'b'
    thresholdPos = self.thresholdSpinBox.value()

    if self.barGraphWidget.xLine:
      self.thresholdLinePos = self.thresholdSpinBox.value()

      if self.nmrResidueTable._dataFrameObject:
        for nmrResidue in self.nmrResidueTable._dataFrameObject.objects:
          if nmrResidue:
            nmrResidue.missingPeaks = False
            if hasattr(nmrResidue, '_spectraWithMissingPeaks'):
              if len(nmrResidue._spectraWithMissingPeaks) != 0:
                if nmrResidue.sequenceCode:
                  x = int(nmrResidue.sequenceCode)
                  if nmrResidue._deltaShift:
                    y = nmrResidue._deltaShift
                  else:
                    if nmrResidue._includeInDeltaShift:
                      y = self.disappearedBarThresholdSpinBox.value()
                    else:
                      y = 0
                  self.disappearedY.append(y)
                  self.disappearedX.append(x)
                  self.disappereadObjects.append(nmrResidue)
                  nmrResidue.missingPeaks = True
            if nmrResidue._deltaShift:
              if not nmrResidue.missingPeaks:
                if nmrResidue.sequenceCode:
                  x = int(nmrResidue.sequenceCode)
                  y = float(nmrResidue._deltaShift)
                  xs.append(x)
                  ys.append(y)
                  obs.append(nmrResidue)
                  if y > self.thresholdLinePos:
                    self.aboveY.append(y)
                    self.aboveX.append(x)
                    self.aboveObjects.append(nmrResidue)
                  else:
                    self.belowX.append(x)
                    self.belowY.append(y)
                    self.belowObjects.append(nmrResidue)


    selectedNameColourA = self.aboveThresholdColourBox.getText()
    for code, name in spectrumColours.items():
      if name == selectedNameColourA:
        self.aboveBrush = code

    selectedNameColourB = self.belowThresholdColourBox.getText()
    for code, name in spectrumColours.items():
      if name == selectedNameColourB:
        self.belowBrush = code

    selectedNameColourC = self.disappearedColourBox.getText() #disappeared peaks
    for code, name in spectrumColours.items():
      if name == selectedNameColourC:
        self.disappearedPeakBrush = code

    # self.barGraphWidget.deleteLater()
    # self.barGraphWidget = None
    # self.barGraphWidget = BarGraphWidget(self.mainWidget, application=self.application,
    #                                      xValues=xs, yValues=ys, objects=obs,threshouldLine = thresholdPos,
    #                                      grid=(10, 0))
    self.barGraphWidget.setMinimumHeight(100)
    self.barGraphWidget.customViewBox.mouseClickEvent = self._viewboxMouseClickEvent
    self.barGraphWidget.xLine.sigPositionChangeFinished.connect(self._updateThreshold)
    self.barGraphWidget.customViewBox.addSelectionBox()
    self.barGraphWidget.customViewBox.selectAboveThreshold = self._selectNmrResiduesAboveThreshold
    self.barGraphWidget.clearBars()
    self.barGraphWidget._lineMoved(aboveX=self.aboveX,
                                   aboveY=self.aboveY,
                                   aboveObjects=self.aboveObjects,
                                   belowX=self.belowX,
                                   belowY=self.belowY,
                                   belowObjects=self.belowObjects,
                                   belowBrush=self.belowBrush,
                                   aboveBrush=self.aboveBrush,
                                   disappearedX = self.disappearedX,
                                   disappearedY=self.disappearedY,
                                   disappearedObjects = self.disappereadObjects,
                                   disappearedBrush = self.disappearedPeakBrush,
                                   )
    # self.splitter.addWidget(self.barGraphWidget)
    # self._colourDeltaShiftTableValues()

  # def _colourDeltaShiftTableValues(self):
  #   print(self.nmrResidueTable.deltaShiftsColumn)
    # self.nmrResidueTable.item(0, 0).setBackground(QtGui.QColor(100, 100, 150))

  def updateThresholdLineValue(self, value):
    if self.barGraphWidget:
      self.barGraphWidget.xLine.setPos(value)

  def _updateThreshold(self):
    self.thresholdSpinBox.setValue(self.barGraphWidget.xLine.pos().y())
    self.updateBarGraph()
    # self.barGraphWidget._lineMoved()

  def _viewboxMouseClickEvent(self, event):

    if event.button() == QtCore.Qt.RightButton:
      event.accept()
      self.barGraphWidget.customViewBox._raiseContextMenu(event)
      self.barGraphWidget.customViewBox._resetBoxes()

    elif event.button() == QtCore.Qt.LeftButton:
      self.barGraphWidget.customViewBox._resetBoxes()
      self.application.current.clearNmrResidues()
      event.accept()

  # def _customActionCallBack(self, nmrResidue, *args):
  def _customActionCallBack(self, data):
    from ccpn.ui.gui.lib.Strip import navigateToNmrAtomsInStrip, _getCurrentZoomRatio

    nmrResidue = data[Notifier.OBJECT]

    if nmrResidue:
      xPos = int(nmrResidue.sequenceCode)
      yPos = nmrResidue._deltaShift
      self.barGraphWidget.customViewBox.setRange(xRange=[xPos-10, xPos+10], yRange=[0, yPos],)
      self.application.ui.mainWindow.clearMarks()
      if self.current.strip is not None:
        strip = self.current.strip
        if len(nmrResidue.selectedNmrAtomNames) == 2:
          nmrAtom1 = nmrResidue.getNmrAtom(str(nmrResidue.selectedNmrAtomNames[0]))
          nmrAtom2 = nmrResidue.getNmrAtom(str(nmrResidue.selectedNmrAtomNames[1]))
          if nmrAtom1 and nmrAtom2:
            navigateToNmrAtomsInStrip(strip,
                                      nmrAtoms=[nmrAtom1, nmrAtom2],
                                      widths=_getCurrentZoomRatio(strip.viewBox.viewRange()),
                                      markPositions=True
                                      )
      else:
        getLogger().warning('Impossible to navigate to peak position. Set a current strip first')

  def updateModule(self):

    weights = {}
    for atomWSB in self.atomWeightSpinBoxes:
      weights.update({atomWSB.objectName():atomWSB.value()})

    # selectedAtomNames = [cb.text() for cb in self.atomCheckBoxes if cb.isChecked()]
    selectedAtomNames = [rb.getSelectedText() for rb in self.atomRadioButtons if rb.getSelectedText()]
    if self.nmrResidueTable:
      if self.nmrResidueTable._nmrChain:
        for nmrResidue in self.nmrResidueTable._nmrChain.nmrResidues:

          spectra = self.spectraSelectionWidget.getSelections()
          self._updatedPeakCount(nmrResidue, spectra)
          if nmrResidue._includeInDeltaShift:
            nmrResidue.spectraCount = len(spectra)
            nmrResidueAtoms = [atom.name for atom in nmrResidue.nmrAtoms]
            nmrResidue.selectedNmrAtomNames =  [atom for atom in nmrResidueAtoms if atom in selectedAtomNames]
            nmrResidue._deltaShift = getDeltaShiftsNmrResidue(nmrResidue, selectedAtomNames, spectra=spectra, atomWeights=weights)
          else:
            nmrResidue._deltaShift = None
        self.updateTable(self.nmrResidueTable._nmrChain)
        self.updateBarGraph()


  def _updatedPeakCount(self, nmrResidue, spectra):
    if len(nmrResidue.nmrAtoms)>0:
      peaks = [p for p in nmrResidue.nmrAtoms[0].assignedPeaks if p.peakList.spectrum in spectra]


      spectraWithPeaks = [peak.peakList.spectrum for peak in peaks]
      spectraWithMissingPeaks = [spectrum for spectrum in spectra if spectrum not in spectraWithPeaks]
      nmrResidue._spectraWithMissingPeaks = spectraWithMissingPeaks
      return nmrResidue._spectraWithMissingPeaks


  def _showOnMolecularViewer(self):
    """
    1) write the script in the scripts/pymol dir
    2) run pymol with the script
    """
    import json
    import subprocess

    filePath = os.path.join(getScriptsDirectoryPath(self.project),'pymol', PymolScriptName)

    pymolPath = self.application.preferences.externalPrograms.pymol
    pdbPath = self.pathPDB.get()

    if not os.path.exists(pymolPath):
      ok = MessageDialog.showOkCancelWarning('Molecular Viewer not Set'
                                             , 'Select the executable file on preferences')
      if ok:
        from ccpn.ui.gui.popups.PreferencesPopup import PreferencesPopup
        pp = PreferencesPopup(parent=self.mainWindow, mainWindow=self.mainWindow, preferences=self.application.preferences)
        pp.tabWidget.setCurrentIndex(pp.tabWidget.count()-1)
        pp.exec_()
        return


    while not pdbPath.endswith('.pdb'):
      sucess = self.pathPDB._openFileDialog()
      if sucess:
        pdbPath = self.pathPDB.get()
      else:
        return


    aboveThresholdResidues = "+".join([str(x) for x in self.aboveX])
    belowThresholdResidues = "+".join([str(x) for x in self.belowX])
    missingdResidues = "+".join([str(x) for x in self.disappearedX])
    selection = "+".join([str(x.sequenceCode) for x in self.current.nmrResidues])

    colourAboveThreshold = hexToRgb(self.aboveBrush)
    colourBelowThreshold = hexToRgb(self.belowBrush)
    colourMissing = hexToRgb(self.disappearedPeakBrush)


    scriptPath = chemicalShiftMappingPymolTemplate(filePath, pdbPath, aboveThresholdResidues, belowThresholdResidues,
                                                   missingdResidues, colourMissing, colourAboveThreshold, colourBelowThreshold,
                                                   selection)


    try:
      self.pymolProcess = subprocess.Popen(pymolPath+' -r '+scriptPath,
                       shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    except Exception as e:
      getLogger().warning('Pymol not started. Check executable.', e)



  def _selectCurrentNmrResiduesNotifierCallback(self, data):
    for bar in self.barGraphWidget.barGraphs:
      for label in bar.labels:
        if label.data(int(label.text())) is not None:
          if self.application is not None:

            if label.data(int(label.text())) in self.current.nmrResidues:

              if self.application.colourScheme == 'light':
                highlightColour = '#3333ff'
              else:
                highlightColour = '#00ff00'
              label.setBrush(QtGui.QColor(highlightColour))
              label.setVisible(True)
              label.setSelected(True)

            else:
              label.setSelected(False)
              label.setBrush(QtGui.QColor(bar.brush))
              if label.isBelowThreshold and not self.barGraphWidget.customViewBox.allLabelsShown:
                label.setVisible(False)


  def _mouseClickEvent(self, event):

    position = event.pos().x()
    self.clicked = int(position)
    if event.button() == QtCore.Qt.LeftButton:
      for bar in self.barGraphWidget.barGraphs:
        for label in bar.labels:
          if label.text() == str(self.clicked):
            self.current.nmrResidue = label.data(self.clicked)
            label.setSelected(True)
      event.accept()

  def _mouseDoubleClickEvent(self, event):
    from ccpn.ui.gui.lib.Strip import navigateToNmrAtomsInStrip, _getCurrentZoomRatio

    self.nmrResidueTable.scrollToSelectedIndex()

    self.application.ui.mainWindow.clearMarks()
    position = event.pos().x()
    self.doubleclicked = int(position)
    if event.button() == QtCore.Qt.LeftButton:
      for bar in self.barGraphWidget.barGraphs:
        for label in bar.labels:
          if label.text() == str(self.doubleclicked):
           nmrResidue =  label.data(self.doubleclicked)
           if nmrResidue:
             if self.current.strip is not None:
               strip = self.current.strip
               if len(nmrResidue.selectedNmrAtomNames) == 2:
                 nmrAtom1 = nmrResidue.getNmrAtom(str(nmrResidue.selectedNmrAtomNames[0]))
                 nmrAtom2 = nmrResidue.getNmrAtom(str(nmrResidue.selectedNmrAtomNames[1]))
                 if nmrAtom1 and nmrAtom2:

                   navigateToNmrAtomsInStrip(strip,
                                             nmrAtoms=[nmrAtom1, nmrAtom2],
                                             widths=_getCurrentZoomRatio(strip.viewBox.viewRange()),
                                             markPositions=True
                                             )
             else:
               getLogger().warning('Impossible to navigate to peak position. Set a current strip first')

  def close(self):
    """
    Close the table from the commandline
    """
    self._closeModule()

  def _closeModule(self):
    """
    Re-implementation of closeModule function from CcpnModule to unregister notification on current
    """
    if self._selectCurrentNmrResiduesNotifier is not None:
      self._selectCurrentNmrResiduesNotifier.unRegister()
    # self._peakChangedNotifier.unRegister()
    if self._peakDeletedNotifier:
      self._peakDeletedNotifier.unRegister()
    if self._nrChangedNotifier:
      self._nrChangedNotifier.unRegister()
    if self._nrDeletedNotifier:
      self._nrDeletedNotifier.unRegister()

    super(ChemicalShiftsMapping, self)._closeModule()

