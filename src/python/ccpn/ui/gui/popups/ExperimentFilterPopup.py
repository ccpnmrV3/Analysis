__author__ = 'simon1'

from PyQt4 import QtGui, QtCore

from ccpn.ui.gui.widgets.Base import Base
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.FilteringPulldownList import FilteringPulldownList
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.GroupBox import GroupBox
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.RadioButton import RadioButton

from ccpnmodel.ccpncore.lib.spectrum.NmrExpPrototype import priorityNameRemapping

class ExperimentFilterPopup(QtGui.QDialog, Base):
  def __init__(self, spectrum=None, parent=None, application=None, **kw):
    super(ExperimentFilterPopup, self).__init__(parent)
    Base.__init__(self, **kw)

    detectionBox = GroupBox(self, grid=(0, 0), gridSpan=(1, 4))
    filterBox = GroupBox(self, grid=(1, 0), gridSpan=(2, 4))
    selectionBox = GroupBox(self, grid=(3, 0), gridSpan=(1, 4))

    self.transferSwitches = []

    self.experimentClassification = application.experimentClassifications

    # filter by detection nucleus
    self.cCheckBox = CheckBox(detectionBox, grid=(0, 0), hAlign='r', callback=self.updateChoices)
    cLabel = Label(detectionBox, text='C-detected', grid=(0, 1), hAlign='l')
    self.hCheckBox = CheckBox(detectionBox, grid=(0, 2), hAlign='r', callback=self.updateChoices)
    hLabel = Label(detectionBox, text='H-detected', grid=(0, 3), hAlign='l')
    self.otherCheckBox = CheckBox(detectionBox, grid=(0, 4), hAlign='r', callback=self.updateChoices)
    nLabel = Label(detectionBox, text='Other', grid=(0, 5), hAlign='l')

    # filter by transfer technique
    self.anyCheckbox = RadioButton(filterBox, grid=(0, 0), callback=self.updateChoices)
    Label(filterBox, grid=(0, 1), hAlign='l', text='Any')
    self.relayedCheckBox = RadioButton(filterBox, grid=(0, 2), callback=self.updateChoices)
    Label(filterBox, grid=(0, 3), hAlign='l', text='relayed')
    self.relaxationCheckBox = RadioButton(filterBox, grid=(0, 4), callback=self.updateChoices)
    Label(filterBox, grid=(0, 5), hAlign='l', text='relaxation')
    self.jResolvedCheckBox = RadioButton(filterBox, grid=(0, 6), callback=self.updateChoices)
    Label(filterBox, grid=(0, 7), hAlign='l', text='J resolved')
    self.mqCheckBox = RadioButton(filterBox, grid=(1, 0), callback=self.updateChoices)
    mqLabel = Label(filterBox, grid=(1, 1), hAlign='l', text='MQ')
    self.projectedCheckBox = RadioButton(filterBox, grid=(1, 2), callback=self.updateChoices)
    Label(filterBox, grid=(1, 3), hAlign='l', text='projection')
    self.quantificationCheckBox = RadioButton(filterBox, grid=(1, 4), callback=self.updateChoices)
    Label(filterBox, grid=(1, 5), hAlign='l', text='quantification')
    self.throughSpaceCheckbox = RadioButton(filterBox, grid=(1, 6), callback=self.updateChoices)
    Label(filterBox, grid=(1, 7), hAlign='l', text='through space')
    self.noneOfTheAboveCheckbox = RadioButton(filterBox, grid=(2, 0), callback=self.updateChoices)
    Label(filterBox, 'None of the Above', grid=(2, 1), gridSpan=(1, 2))

    if not spectrum.experimentType:
      self.anyCheckbox.setChecked(True)
      self.cCheckBox.setChecked(True)
      self.hCheckBox.setChecked(True)
      self.otherCheckBox.setChecked(True)

    experimentLabel = Label(selectionBox, text='experiment type', grid=(0, 0), hAlign='r')
    self.experimentPulldown = FilteringPulldownList(selectionBox, grid=(0, 1))

    self.experimentTypes = spectrum.project._experimentTypeMap
    axisCodes = []
    for isotopeCode in spectrum.isotopeCodes:
      axisCodes.append(''.join([char for char in isotopeCode if not char.isdigit()]))

    atomCodes = tuple(sorted(axisCodes))
    self.classifications = list(self.experimentClassification[spectrum.dimensionCount].get(atomCodes))
    self.experimentNames = self.experimentTypes[spectrum.dimensionCount].get(atomCodes)

    self.texts = []
    self.objects = []
    for k,v in self.experimentNames.items():
      self.objects.append([x for x in self.classifications if x.name == v][0])
      self.texts.append(k)


    self.updateChoices()

    self.buttonBox = ButtonList(self, grid=(4, 3), texts=['Close', 'Apply'],
                           callbacks=[self.close, self._setExperimentType])


  def _setExperimentType(self):
    expType = self.experimentPulldown.currentText()
    self.expType = expType
    self.accept()

  def close(self):
    self.expType = None
    self.reject()

  def updateChoices(self):
    filteredExperimentObjects = set()

    # filter by acquisition nucleus
    detectionNuclei = []
    if self.cCheckBox.isChecked():
      detectionNuclei.append('13C')
    if self.hCheckBox.isChecked():
      detectionNuclei.append('1H')
    if self.otherCheckBox.isChecked():
      detectionNuclei.extend(['15N', '19F', '23Na', '79Br'])

    if self.anyCheckbox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.acquisitionNucleus in detectionNuclei]
    if self.noneOfTheAboveCheckbox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if not x.isThroughSpace and
       not x.isRelayed and not x.isRelaxation and not x.isJResolved and not x.isMultipleQuantum
       and not x.isProjection and not x.isQuantification and x.acquisitionNucleus is detectionNuclei]
    if self.throughSpaceCheckbox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isThroughSpace and x.acquisitionNucleus in detectionNuclei]
    if self.relayedCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isRelayed and x.acquisitionNucleus in detectionNuclei]
    if self.relaxationCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isRelaxation and x.acquisitionNucleus in detectionNuclei]
    if self.jResolvedCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isJResolved and x.acquisitionNucleus in detectionNuclei]
    if self.mqCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isMultipleQuantum and x.acquisitionNucleus in detectionNuclei]
    if self.projectedCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isProjection and x.acquisitionNucleus in detectionNuclei]
    if self.quantificationCheckBox.isChecked():
      [filteredExperimentObjects.add(x) for x in self.objects if x.isQuantification and x.acquisitionNucleus in detectionNuclei]

    texts = []
    objects = []
    for ii, expObject in enumerate(self.objects):
      if expObject in filteredExperimentObjects:
        objects.append(expObject)
        texts.append(self.texts[ii])
    self.experimentPulldown.setData(texts=texts, objects=objects)
