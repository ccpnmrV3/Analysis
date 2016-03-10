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

import os, sys

from PyQt4 import QtGui, QtCore

from ccpncore.gui.Base import Base
from ccpncore.gui.Button import Button
from ccpncore.gui.ColourDialog import ColourDialog
from ccpncore.util.Colour import spectrumColours
from ccpncore.gui.ButtonList import ButtonList
from ccpncore.gui.Label import Label
from ccpncore.gui.LineEdit import LineEdit
from ccpncore.gui.PulldownList import PulldownList
from ccpncore.gui.CheckBox import CheckBox
from ccpncore.gui.Spinbox import Spinbox
from ccpncore.gui.DoubleSpinbox import DoubleSpinbox


from functools import partial

SPECTRA = ['1H', 'STD', 'Relaxation Filtered', 'Water LOGSY']

class SpectrumPropertiesPopup(QtGui.QDialog, Base):
  def __init__(self, spectrum, parent=None, **kw):

    super(SpectrumPropertiesPopup, self).__init__(parent)
    layout = QtGui.QGridLayout()
    self.setLayout(layout)
    tabWidget = QtGui.QTabWidget()
    tabWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    if spectrum.dimensionCount == 1:
      tabWidget.addTab(GeneralTab(spectrum), "General")
      tabWidget.addTab(DimensionsTab(spectrum, spectrum.dimensionCount), "Dimensions")

    else:
      tabWidget.addTab(GeneralTab(spectrum), "General")
      tabWidget.addTab(DimensionsTab(spectrum, spectrum.dimensionCount), "Dimensions")
      tabWidget.addTab(ContoursTab(spectrum), "Contours")


    self.layout().addWidget(tabWidget, 0, 0, 2, 2)
    buttonBox = Button(self, grid=(3, 1), callback=self.accept, text='Close',
                           vPolicy='fixed')
    if sys.platform.lower() == 'linux':
      if spectrum.project._appBase.preferences.general.colourScheme == 'dark':
        self.setStyleSheet("QTabWidget > QWidget{ background-color:  #2a3358; color: #f7ffff;} QTabBar::tab {background-color:  #2a3358; color: #f7ffff;} ")
      elif spectrum.project._appBase.preferences.general.colourScheme == 'light':
        self.setStyleSheet("QTabWidget > QWidget { background-color: #fbf4cc;} QTabWidget { background-color: #fbf4cc;}")
  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Enter:
      pass



class GeneralTab(QtGui.QWidget, Base):
  def __init__(self, spectrum, parent=None, item=None):
    super(GeneralTab, self).__init__(parent)
    self.item = item
    self.spectrum = spectrum
    self.experimentTypes = spectrum._project._experimentTypeMap
    nameLabel = Label(self, text="Spectrum name ", grid=(1, 0))
    self.nameData = LineEdit(self, vAlign='t', grid=(1, 1))
    self.nameData.setText(spectrum.name)
    self.nameData.editingFinished.connect(self.changeSpectrumName)
    pathLabel = Label(self, text="Path", vAlign='t', hAlign='l', grid=(2, 0))
    self.pathData = LineEdit(self, vAlign='t', grid=(2, 1))
    self.pathButton = Button(self, grid=(2, 2), callback=self.getSpectrumFile, icon='iconsNew/applications-system')

    self.pythonConsole = self.spectrum.project._appBase.mainWindow.pythonConsole
    self.logger = self.spectrum.project._logger

    self.setWindowTitle("Spectrum Information")

    apiDataStore = spectrum._apiDataSource.dataStore
    if apiDataStore.dataLocationStore.name == 'standard':
      dataUrlName = apiDataStore.dataUrl.name
      if dataUrlName == 'insideData':
        self.pathData.setText('$INSIDE/%s' % apiDataStore.path)
      elif dataUrlName == 'alongsideData':
        self.pathData.setText('$ALONGSIDE/%s' % apiDataStore.path)
      elif dataUrlName == 'remoteData':
        self.pathData.setText('$DATA/%s' % apiDataStore.path)
      else:
        self.pathData.setText(apiDataStore.fullPath)
    else:
      self.pathData.setText(apiDataStore.fullPath)
    self.pathData.editingFinished.connect(self.setSpectrumPath)
    chemicalShiftListLabel = Label(self, text="Chemical Shift List ", vAlign='t', hAlign='l', grid=(3, 0))
    self.chemicalShiftListPulldown = PulldownList(self, vAlign='t', grid=(3, 1), texts=[csList.pid
                                                for csList in spectrum.project.chemicalShiftLists]
                                                +['<New>'],callback=self.setChemicalShiftList)
    pidLabel = Label(self, text="PID ", vAlign='t', hAlign='l', grid=(5, 0))
    pidData = Label(self, text=spectrum.pid, vAlign='t', grid=(5, 1))
    if spectrum.dimensionCount == 1:
      colourLabel = Label(self, text="Colour", vAlign='t', hAlign='l', grid=(6, 0))
      self.colourBox = PulldownList(self, vAlign='t', hAlign='l', grid=(6, 1))
      for item in spectrumColours.items():
        pix=QtGui.QPixmap(QtCore.QSize(20, 20))
        pix.fill(QtGui.QColor(item[0]))
        self.colourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
      self.colourBox.setCurrentIndex(list(spectrumColours.keys()).index(spectrum.sliceColour))
      self.colourBox.currentIndexChanged.connect(partial(self.changedColourComboIndex, spectrum))
      colourButton = Button(self, vAlign='t', hAlign='l', grid=(6, 2), hPolicy='fixed',
                    callback=partial(self.changeSpectrumColour, spectrum), icon='iconsNew/colours')
      spectrumTypeLabel = Label(self, text="Experiment Type ", vAlign='t', hAlign='l', grid=(7, 0))
      spectrumType = PulldownList(self, vAlign='t', grid=(7, 1))
      spectrumType.addItems(SPECTRA)
      print(spectrumType.findText(spectrum.experimentName))
      spectrumType.setCurrentIndex(spectrumType.findText(spectrum.experimentName))
      spectrumScalingLabel = Label(self, text='Spectrum Scaling', vAlign='t', hAlign='l', grid=(8, 0))
      self.spectrumScalingData = LineEdit(self, text=str(self.spectrum.scale), vAlign='t', hAlign='l', grid=(8, 1))
      self.spectrumScalingData.editingFinished.connect(self.setSpectrumScale)

      recordingDataLabel = Label(self, text="Date Recorded ", vAlign='t', hAlign='l', grid=(10, 0))
      noiseLevelLabel = Label(self, text="Noise Level ", vAlign='t', hAlign='l', grid=(11, 0))
      noiseLevelData = LineEdit(self)
      if spectrum._apiDataSource.noiseLevel is not None:
        noiseLevelData.setText(str('%.3d' % spectrum._apiDataSource.noiseLevel))
      else:
        noiseLevelData.setText('None')
    else:
      spectrumTypeLabel = Label(self, text="Spectrum Type ", vAlign='t', hAlign='l', grid=(6, 0))
      self.spectrumType = PulldownList(self, vAlign='t', grid=(6, 1))
      axisCodes = []
      for isotopeCode in spectrum.isotopeCodes:
        axisCodes.append(''.join([code for code in isotopeCode if not code.isdigit()]))

      self.atomCodes = tuple(sorted(axisCodes))
      self.spectrumType.addItems(sorted(list(self.experimentTypes[spectrum.dimensionCount].get(self.atomCodes).keys())))
      self.spectrumType.setCurrentIndex(self.spectrumType.findText(spectrum.experimentName))
      self.spectrumType.currentIndexChanged.connect(self.changeSpectrumType)
      self.spectrumType.setMinimumWidth(self.pathData.width()*1.95)
      self.spectrumType.setFixedHeight(25)
      spectrumScalingLabel = Label(self, text='Spectrum Scaling', vAlign='t', grid=(8, 0))
      self.spectrumScalingData = LineEdit(self, text=str(self.spectrum.scale), vAlign='t', grid=(8, 1))
      self.spectrumScalingData.editingFinished.connect(self.setSpectrumScale)
      noiseLevelLabel = Label(self, text="Noise Level ", vAlign='t', hAlign='l', grid=(9, 0))
      noiseLevelData = LineEdit(self, vAlign='t', grid=(9, 1))


      if spectrum._apiDataSource.noiseLevel is None:
        noiseLevelData.setText(str('%.3d' % spectrum._apiDataSource.estimateNoise()))
      else:

        noiseLevelData.setText('%.3d' % spectrum._apiDataSource.noiseLevel)


  def writeLoggingMessage(self, command):
    self.logger.info("spectrum = project.getByPid('%s')" % self.spectrum.pid)
    self.logger.info(command)

  def changeSpectrumName(self):
    if self.nameData.isModified():
      self.spectrum.rename(self.nameData.text())
      self.writeLoggingMessage("spectrum.rename('%s')" % self.nameData.text())
      self.pythonConsole.writeConsoleCommand("spectrum.rename('%s')" % self.nameData.text(), spectrum=self.spectrum)


  def setSpectrumScale(self):
    self.spectrum.scale = float(self.spectrumScalingData.text())
    self.writeLoggingMessage("spectrum.scale = %s" % self.spectrumScalingData.text())
    self.pythonConsole.writeConsoleCommand("spectrum.scale = %s" % self.spectrumScalingData.text(), spectrum=self.spectrum)


  def setChemicalShiftList(self, item):
    if item == '<New>':
      newChemicalShiftList = self.spectrum.project.newChemicalShiftList()
      insertionIndex = len(self.chemicalShiftListPulldown.texts)-1
      self.chemicalShiftListPulldown.texts.insert(insertionIndex, newChemicalShiftList.pid)
      self.chemicalShiftListPulldown.setData(self.chemicalShiftListPulldown.texts)
      self.chemicalShiftListPulldown.setCurrentIndex(insertionIndex)
      self.spectrum.chemicalShiftList = newChemicalShiftList
      self.writeLoggingMessage("""newChemicalShiftList = project.newChemicalShiftList()\n
                                  spectrum.chemicalShiftList = newChemicalShiftList""")
      self.pythonConsole.writeConsoleCommand('spectrum.chemicalShiftList = chemicalShiftList', chemicalShiftList=newChemicalShiftList, spectrum=self.spectrum)
      self.logger.info('spectrum.chemicalShiftList = chemicalShiftList')
    else:
      self.spectrum.chemicalShiftList = self.spectrum.project.getByPid(item)
      self.pythonConsole.writeConsoleCommand('spectrum.newChemicalShiftList = chemicalShiftList', chemicalShiftList=self.spectrum.chemicalShiftList, spectrum=self.spectrum)
      self.writeLoggingMessage("""chemicalShiftList = project.getByPid('%s')\n
                                  spectrum.chemicalShiftList = chemicalShiftList""")

  def changeSpectrumType(self, value):
    expType = self.experimentTypes[self.spectrum.dimensionCount].get(self.atomCodes).get(self.spectrumType.currentText())
    self.spectrum.experimentType = expType
    self.pythonConsole.writeConsoleCommand('spectrum.experimentType = experimentType', experimentType=expType, spectrum=self.spectrum)
    self.writeLoggingMessage("spectrum.experimentType = '%s'" % expType)

  def getSpectrumFile(self):
    if os.path.exists('/'.join(self.pathData.text().split('/')[:-1])):
      currentSpectrumDirectory = '/'.join(self.pathData.text().split('/')[:-1])
    else:
      currentSpectrumDirectory = os.path.expanduser('~')
    directory = QtGui.QFileDialog.getOpenFileName(self, 'Select Spectrum File', currentSpectrumDirectory)
    if len(directory) > 0:
      self.pathData.setText(directory)
      self.spectrum.filePath = directory


      apiDataStore = self.spectrum._apiDataSource.dataStore
      if apiDataStore.dataLocationStore.name == 'standard':
        dataUrlName = apiDataStore.dataUrl.name
        if dataUrlName == 'insideData':
          self.pathData.setText('$INSIDE/%s' % apiDataStore.path)
        elif dataUrlName == 'alongsideData':
          self.pathData.setText('$ALONGSIDE/%s' % apiDataStore.path)
        elif dataUrlName == 'remoteData':
          self.pathData.setText('$DATA/%s' % apiDataStore.path)
        else:
          self.pathData.setText(apiDataStore.fullPath)

  def setSpectrumPath(self):
    if self.pathData.isModified():
      if os.path.exists(self.pathData.text()):
        self.spectrum.filePath = self.pathData.text()
        self.writeLoggingMessage("spectrum.filePath = '%s'" % self.pathData.text())
        self.pythonConsole.writeConsoleCommand("spectrum.filePath('%s')" % self.pathData.text(), spectrum=self.spectrum)
        apiDataStore = self.spectrum._apiDataSource.dataStore
        if apiDataStore.dataLocationStore.name == 'standard':
          dataUrlName = apiDataStore.dataUrl.name
          if dataUrlName == 'insideData':
            self.pathData.setText('$INSIDE/%s' % apiDataStore.path)
          elif dataUrlName == 'alongsideData':
            self.pathData.setText('$ALONGSIDE/%s' % apiDataStore.path)
          elif dataUrlName == 'remoteData':
            self.pathData.setText('$DATA/%s' % apiDataStore.path)
          else:
            self.pathData.setText(apiDataStore.fullPath)
      else:
        self.logger.error('Cannot set spectrum path to %s. Path does not exist' % self.pathData.text())
        return


  def changeSpectrumColour(self, spectrum):
    dialog = ColourDialog()
    newColour = dialog.getColor()
    spectrum._apiDataSource.setSliceColour(newColour.name())
    self.writeLoggingMessage("spectrum.sliceColour = '%s'" % newColour.name())
    self.pythonConsole.writeConsoleCommand("spectrum.sliceColour = '%s'" % newColour.name(), spectrum=self.spectrum)
    spectrum.guiSpectrumView.plot.setPen(spectrum._apiDataSource.sliceColour)
    pix = QtGui.QPixmap(QtCore.QSize(20, 20))
    pix.fill(QtGui.QColor(newColour))
    newIndex = str(len(spectrumColours.items())+1)
    self.colourBox.addItem(icon=QtGui.QIcon(pix), text='Colour %s' % newIndex)
    spectrumColours[newColour.name()] = 'Colour %s' % newIndex
    self.colourBox.setCurrentIndex(int(newIndex)-1)

  def changedColourComboIndex(self, spectrum, value):
    spectrum.sliceColour = list(spectrumColours.keys())[value]
    pix = QtGui.QPixmap(60, 10)
    pix.fill(QtGui.QColor(spectrum.sliceColour))
    self.writeLoggingMessage("spectrum.sliceColour = '%s'" % list(spectrumColours.keys())[value])
    self.pythonConsole.writeConsoleCommand("spectrum.sliceColour '%s'" % list(spectrumColours.keys())[value], spectrum=self.spectrum)



class DimensionsTab(QtGui.QWidget, Base):
  def __init__(self, spectrum, dimensions, parent=None):
    super(DimensionsTab, self).__init__(parent)
    self.spectrum = spectrum
    self.pythonConsole = self.spectrum.project._appBase.mainWindow.pythonConsole
    self.logger = self.spectrum.project._logger
    dimensionalityLabel = Label(self, text="Dimension ", grid=(0, 0),hAlign='l', vAlign='t',)
    for i in range(dimensions):
      dimLabel = Label(self, text='%s' % str(i+1), grid =(0, i+1), vAlign='t', hAlign='l')
    for i in range(dimensions):
      axisLabel = Label(self, text="Axis Code ", grid=(1, 0), vAlign='t', hAlign='l')
      axisLabelData = Label(self, text=str(spectrum.axisCodes[i]), grid=(1, i+1),  hAlign='l', vAlign='t',)
      pointsLabel = Label(self, text="Point Counts ", grid=(2, 0), vAlign='t', hAlign='l')
      pointsData = Label(self, text=str(spectrum.pointCounts[i]), grid=(2, i+1), vAlign='t', hAlign='l')
      axisTypeLabel = Label(self, text="Dimension Type ", grid=(3, 0), vAlign='t', hAlign='l')
      axisTypeData = Label(self, text=spectrum.dimensionTypes[i], grid=(3, i+1), vAlign='t', hAlign='l')
      spectralWidthLabel = Label(self, text="Spectrum Width (ppm) ", grid=(4, 0), vAlign='t', hAlign='l')
      spectralWidthData = Label(self, text=str("%.3f" % spectrum.spectralWidths[i]), grid=(4, i+1), vAlign='t', hAlign='l')
      spectralWidthHzLabel = Label(self, text="Spectral Width (Hz) ", grid=(5, 0), vAlign='t', hAlign='l')
      spectralWidthHzData = Label(self, text=str("%.3f" % spectrum.spectralWidthsHz[i]), grid=(5, i+1), vAlign='t', hAlign='l')
      spectralReferencingLabel = Label(self, text="Referencing ", grid=(6, 0), vAlign='t', hAlign='l')
      spectralReferencingData = LineEdit(self, text=str("%.3f" % spectrum.referenceValues[i]), grid=(6, i+1), vAlign='t', hAlign='l')
      spectralReferencingData.textChanged.connect(partial(self.setDimensionReferencing, spectrum, i))
      spectralReferencingData.setMaximumWidth(100)
      spectralAssignmentToleranceLabel = Label(self, text="Assignment Tolerance ", grid=(7, 0),  hAlign='l')

      spectralAssignmentToleranceData = LineEdit(self, grid=(7, i+1),  hAlign='l')
      spectralAssignmentToleranceData.setMaximumWidth(100)

      if spectrum.assignmentTolerances[i] is not None:
        spectralAssignmentToleranceData.setText(str("%.3f" % spectrum.assignmentTolerances[i]))
      spectralAssignmentToleranceData.textChanged.connect(partial(self.setAssignmentTolerances, spectrum, i))
      # spectralShiftWeightingLabel = Label(self, text=DIMENSIONS[i]+"-Shift Weighting", grid=(j+8, 0))
      # spectralShiftWeightingData = LineEdit(self, grid=(j+8, 1))

  def writeLoggingMessage(self, command):
    self.logger.info("spectrum = project.getByPid('%s')" % self.spectrum.pid)
    self.logger.info(command)

  def setAssignmentTolerances(self, spectrum, dim, value):
    assignmentTolerances = list(spectrum.assignmentTolerances)
    assignmentTolerances[dim] = float(value)
    spectrum.assignmentTolerances = assignmentTolerances
    self.pythonConsole.writeConsoleCommand("spectrum.assignmentTolerances = {0}".format(assignmentTolerances), spectrum=spectrum)
    self.writeLoggingMessage("spectrum.assignmentTolerances = {0}".format(assignmentTolerances))


  def setDimensionReferencing(self, spectrum, dim, value):
    spectrumReferencing = list(spectrum.referenceValues)
    spectrumReferencing[dim] = float(value)
    spectrum.referenceValues = spectrumReferencing
    self.pythonConsole.writeConsoleCommand("spectrum.referenceValues = {0}".format(spectrumReferencing), spectrum=spectrum)
    self.writeLoggingMessage("spectrum.referenceValues = {0}".format(spectrumReferencing))



class ContoursTab(QtGui.QWidget, Base):
  def __init__(self, spectrum, parent=None):
    super(ContoursTab, self).__init__(parent)

    self.spectrum = spectrum
    self.pythonConsole = self.spectrum.project._appBase.mainWindow.pythonConsole
    self.logger = self.spectrum.project._logger
    positiveContoursLabel = Label(self, text="Show Positive Contours", grid=(0, 0), vAlign='t', hAlign='l')
    positiveContoursCheckBox = CheckBox(self, grid=(0, 1), checked=True, vAlign='t', hAlign='l')
    for spectrumView in self.spectrum.spectrumViews:
      if spectrumView._wrappedData.spectrumView.displayPositiveContours is True:
        positiveContoursCheckBox.setChecked(True)
      else:
        positiveContoursCheckBox.setChecked(False)

    positiveContoursCheckBox.stateChanged.connect(self.changePositiveContourDisplay)
    positiveBaseLevelLabel = Label(self, text="Positive Base Level", grid=(1, 0), vAlign='t', hAlign='l')
    positiveBaseLevelData = DoubleSpinbox(self, grid=(1, 1), vAlign='t')
    positiveBaseLevelData.setMaximum(1e12)
    positiveBaseLevelData.setMinimum(0)
    positiveBaseLevelData.setValue(spectrum.positiveContourBase)
    positiveBaseLevelData.valueChanged.connect(partial(self.lineEditTextChanged1, spectrum))
    positiveMultiplierLabel = Label(self, text="Positive Multiplier", grid=(2, 0), vAlign='t', hAlign='l')
    positiveMultiplierData = DoubleSpinbox(self, grid=(2, 1), vAlign='t')
    positiveMultiplierData.setSingleStep(0.1)
    positiveMultiplierData.setValue(float(spectrum.positiveContourFactor))
    positiveMultiplierData.valueChanged.connect(partial(self.lineEditTextChanged2, spectrum))
    positiveBaseLevelData.setSingleStep(positiveBaseLevelData.value()*(positiveMultiplierData.value()-1))
    positiveContourCountLabel = Label(self, text="Number of positive contours", grid=(3, 0), vAlign='t', hAlign='l')
    positiveContourCountData = Spinbox(self, grid=(3, 1), vAlign='t')
    positiveContourCountData.setValue(int(spectrum._apiDataSource.positiveContourCount))
    positiveContourCountData.valueChanged.connect(partial(self.lineEditTextChanged3, spectrum))
    positiveContourColourLabel = Label(self, text="Positive Contour Colour", grid=(4, 0), vAlign='t', hAlign='l')
    self.positiveColourBox = PulldownList(self, grid=(4, 1), vAlign='t')

    for item in spectrumColours.items():
      pix=QtGui.QPixmap(QtCore.QSize(20,20))
      pix.fill(QtGui.QColor(item[0]))
      self.positiveColourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
    try:
      self.positiveColourBox.setCurrentIndex(list(spectrumColours.keys()).index(spectrum.positiveContourColour))
      self.positiveColourBox.currentIndexChanged.connect(partial(self.changePosColourComboIndex, spectrum))
    except ValueError:
      pass
    self.positiveColourButton = Button(self, grid=(4, 2), vAlign='t', hAlign='l',
                                       icon='iconsNew/colours', hPolicy='fixed')
    self.positiveColourButton.clicked.connect(partial(self.changePosSpectrumColour, spectrum))


    negativeContoursLabel = Label(self, text="Show Negative Contours", grid=(6 ,0), vAlign='t', hAlign='l')
    negativeContoursCheckBox = CheckBox(self, grid=(6, 1), checked=True, vAlign='t', hAlign='l')
    for spectrumView in self.spectrum.spectrumViews:
      if spectrumView._wrappedData.spectrumView.displayNegativeContours is True:
        negativeContoursCheckBox.setChecked(True)
      else:
        negativeContoursCheckBox.setChecked(False)
    negativeContoursCheckBox.stateChanged.connect(self.displayNegativeContours)
    negativeBaseLevelLabel = Label(self, text="Negative Base Level", grid=(7, 0), vAlign='t', hAlign='l')
    negativeBaseLevelData = DoubleSpinbox(self, grid=(7, 1), vAlign='t')
    negativeBaseLevelData.setMaximum(0)
    negativeBaseLevelData.setMinimum(-1e12)
    negativeBaseLevelData.setValue(spectrum.negativeContourBase)
    negativeBaseLevelData.valueChanged.connect(partial(self.lineEditTextChanged4, spectrum))
    negativeMultiplierLabel = Label(self, text="Negative Multiplier", grid=(8, 0), vAlign='t', hAlign='l')
    negativeMultiplierData = DoubleSpinbox(self, grid=(8, 1), vAlign='t')
    negativeMultiplierData.setValue(spectrum.negativeContourFactor)
    negativeMultiplierData.setSingleStep(0.1)

    negativeMultiplierData.valueChanged.connect(partial(self.lineEditTextChanged5, spectrum))
    negativeBaseLevelData.setSingleStep((negativeBaseLevelData.value()*-1)*negativeMultiplierData.value()-1)
    negativeContourCountLabel = Label(self, text="Number of negative contours", grid=(9, 0), vAlign='t', hAlign='l')
    negativeContourCountData = Spinbox(self, grid=(9, 1), vAlign='t')
    negativeContourCountData.setValue(spectrum.negativeContourCount)
    negativeContourCountData.valueChanged.connect(partial(self.lineEditTextChanged6, spectrum))
    negativeContourColourLabel = Label(self, text="Colour",grid=(10, 0), vAlign='t', hAlign='l')
    self.negativeColourBox = PulldownList(self, grid=(10, 1), vAlign='t')
    for item in spectrumColours.items():
      pix=QtGui.QPixmap(QtCore.QSize(20,20))
      pix.fill(QtGui.QColor(item[0]))
      self.negativeColourBox.addItem(icon=QtGui.QIcon(pix), text=item[1])
    try:
      self.negativeColourBox.setCurrentIndex(list(spectrumColours.keys()).index(spectrum.negativeContourColour))
      self.negativeColourBox.currentIndexChanged.connect(partial(self.changeNegColourComboIndex, spectrum))
    except ValueError:
      pass

    self.negativeColourButton = Button(self, grid=(10, 2), icon='iconsNew/colours', hPolicy='fixed',
                                       vAlign='t', hAlign='l')
    self.negativeColourButton.clicked.connect(partial(self.changeNegSpectrumColour, spectrum))


  def writeLoggingMessage(self, command):
    self.logger.info("spectrum = project.getByPid('%s')" % self.spectrum.pid)
    self.logger.info(command)

  def changePositiveContourDisplay(self, state):
    if state == QtCore.Qt.Checked:
      for spectrumView in self.spectrum.spectrumViews:
        spectrumView.displayPositiveContours = True
        self.logger.info("spectrumView = project.getByPid('%s')" % spectrumView.pid)
        self.logger.info("spectrumView.displayPositiveContours = True")

    else:
      for spectrumView in self.spectrum.spectrumViews:
        spectrumView.displayPositiveContours = False
        self.logger.info("spectrumView = project.getByPid('%s')" % spectrumView.pid)
        self.logger.info("spectrumView.displayPositiveContours = False")

  def displayNegativeContours(self, state):
    if state == QtCore.Qt.Checked:
      for spectrumView in self.spectrum.spectrumViews:
        spectrumView.displayNegativeContours = True
        self.logger.info("spectrumView = project.getByPid('%s')" % spectrumView.pid)
        self.logger.info("spectrumView.displayNegativeContours = True")
    else:
      for spectrumView in self.spectrum.spectrumViews:
        spectrumView.displayNegativeContours = False
        self.logger.info("spectrumView = project.getByPid('%s')" % spectrumView.pid)
        self.logger.info("spectrumView.displayNegativeContours = False")


  def lineEditTextChanged1(self, spectrum, value):
    spectrum.positiveContourBase = float(value)
    self.writeLoggingMessage("spectrum.positiveContourBase = %f" % float(value))
    self.pythonConsole.writeConsoleCommand("spectrum.positiveContourBase = %f" % float(value), spectrum=spectrum)

  def lineEditTextChanged2(self, spectrum, value):
    spectrum.positiveContourFactor = float(value)
    self.writeLoggingMessage("spectrum.positiveContourFactor = %f" % float(value))
    self.pythonConsole.writeConsoleCommand("spectrum.positiveContourFactor = %f" % float(value), spectrum=spectrum)

  def lineEditTextChanged3(self, spectrum, value):
    spectrum.positiveContourCount = int(value)
    self.writeLoggingMessage("spectrum.positiveContourCount = %f" % int(value))
    self.pythonConsole.writeConsoleCommand("spectrum.positiveContourCount = %f" % int(value), spectrum=spectrum)

  def lineEditTextChanged4(self, spectrum, value):
    spectrum.negativeContourBase = float(value)
    self.writeLoggingMessage("spectrum.negativeContourBase = %f" % float(value))
    self.pythonConsole.writeConsoleCommand("spectrum.negativeContourBase = %f" % float(value), spectrum=spectrum)

  def lineEditTextChanged5(self, spectrum, value):
    spectrum.negativeContourFactor = float(value)
    self.writeLoggingMessage("spectrum.negativeContourFactor = %f" % float(value))
    self.pythonConsole.writeConsoleCommand("spectrum.negativeContourFactor = %f" % float(value), spectrum=spectrum)

  def lineEditTextChanged6(self, spectrum, value):
    spectrum.negativeContourCount = int(value)
    self.writeLoggingMessage("spectrum.negativeContourCount = %f" % int(value))
    self.pythonConsole.writeConsoleCommand("spectrum.negativeContourCount = %f" % int(value), spectrum=spectrum)

  def changePosSpectrumColour(self, spectrum):
    dialog = ColourDialog()
    newColour = dialog.getColor()
    if newColour is not None:
      spectrum.positiveContourColour = newColour.name()
      self.writeLoggingMessage("spectrum.positiveContourColour = '%s'" % newColour.name())
      self.pythonConsole.writeConsoleCommand("spectrum.positiveContourColour = '%s'" % newColour.name(), spectrum=spectrum)
      pix=QtGui.QPixmap(QtCore.QSize(20,20))
      pix.fill(QtGui.QColor(newColour))
      newIndex = str(len(spectrumColours.items())+1)
      self.positiveColourBox.addItem(icon=QtGui.QIcon(pix), text='Colour %s' % newIndex)
      self.negativeColourBox.addItem(icon=QtGui.QIcon(pix), text='Colour %s' % newIndex)
      spectrumColours[newColour.name()] = 'Colour %s' % newIndex
      self.positiveColourBox.setCurrentIndex(int(newIndex)-1)


  def changeNegSpectrumColour(self, spectrum):
    dialog = ColourDialog()
    newColour = dialog.getColor()
    if newColour is not None:
      spectrum.negativeContourColour = newColour.name()
      self.writeLoggingMessage("spectrum.negativeContourColour = %s" % newColour.name())
      self.pythonConsole.writeConsoleCommand("spectrum.negativeContourColour = '%s'" % newColour.name(), spectrum=spectrum)
      pix=QtGui.QPixmap(QtCore.QSize(20,20))
      pix.fill(QtGui.QColor(newColour))
      newIndex = str(len(spectrumColours.items())+1)
      self.negativeColourBox.addItem(icon=QtGui.QIcon(pix), text='Colour %s' %newIndex)
      self.positiveColourBox.addItem(icon=QtGui.QIcon(pix), text='Colour %s' %newIndex)
      spectrumColours[newColour.name()] = 'Colour %s' % newIndex
      self.negativeColourBox.setCurrentIndex(int(newIndex)-1)


  def changePosColourComboIndex(self, spectrum, value):

    newColour = list(spectrumColours.keys())[value]
    spectrum.positiveContourColour = newColour
    self.writeLoggingMessage("spectrum.positiveContourColour = '%s'" % newColour)
    self.pythonConsole.writeConsoleCommand("spectrum.positiveContourColour = '%s'" % newColour, spectrum=spectrum)

  def changeNegColourComboIndex(self, spectrum, value):

    newColour = list(spectrumColours.keys())[value]
    spectrum._apiDataSource.negativeContourColour = newColour
    self.writeLoggingMessage("spectrum.negativeContourColour = %s" % newColour)
    self.pythonConsole.writeConsoleCommand("spectrum.negativeContourColour = '%s'" % newColour, spectrum=spectrum)