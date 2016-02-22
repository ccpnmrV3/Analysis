__author__ = 'simon1'

from PyQt4 import QtGui

from ccpncore.gui.Button import Button
from ccpncore.gui.Base import Base
from ccpncore.gui.CheckBox import CheckBox
from ccpncore.gui.Dock import CcpnDock
from ccpncore.gui.DoubleSpinbox import DoubleSpinbox
from ccpncore.gui.Label import Label
from ccpncore.gui.ListWidget import ListWidget
from ccpncore.gui.PulldownList import PulldownList
from ccpncore.gui.ScrollArea import ScrollArea

from ccpncore.lib.spectrum.Spectrum import name2IsotopeCode
from application.core.modules.NmrResidueTable import NmrResidueTable
from ccpncore.lib.spectrum import Spectrum as spectrumLib

from application.core.lib.Window import navigateToNmrResidue

class PickAndAssignModule(CcpnDock, Base):

  def __init__(self, parent=None, project=None, **kw):

    CcpnDock.__init__(self, parent=None, name='Pick And Assign')
    Base.__init__(self, **kw)
    self.project = project
    self.current = project._appBase.current
    self.nmrResidueTable = NmrResidueTable(self.widget1, project=project, callback=self.goToPositionInModules, grid=(0, 0), gridSpan=(1, 5), stretch=(1, 1))
    self.restrictedPickButton = Button(self.nmrResidueTable, text='Restricted Pick', callback=self.restrictedPick, grid=(0, 2))
    self.assignSelectedButton = Button(self.nmrResidueTable, text='Assign Selected', callback=self.assignSelected, grid=(0, 3))
    self.refreshButton = Button(self.nmrResidueTable, text='Refresh', callback=self.refresh, grid=(0, 4))
    self.settingsButton = Button(self.nmrResidueTable, icon='iconsNew/applications-system', grid=(0, 5), hPolicy='fixed', toggle=True)
    self.settingsButton.toggled.connect(self.toggleWidget2)
    self.settingsButton.setChecked(False)
    displaysLabel = Label(self.widget2, 'Selected Displays', grid=(0, 0))
    self.displaysPulldown = PulldownList(self.widget2, grid=(1, 0), callback=self.updateListWidget)
    self.displaysPulldown.setData([sd.pid for sd in project.spectrumDisplays])
    self.displayList = ListWidget(self.widget2, grid=(0, 1), gridSpan=(4, 1))
    self.displayList.addItem('<All>')
    self.displayList.setFixedWidth(self.displaysPulldown.width())
    self.scrollArea = ScrollArea(self.widget2, grid=(0, 2), gridSpan=(4, 4))
    self.spectrumSelectionWidget = SpectrumSelectionWidget(self.scrollArea, project, self.displayList)
    self.scrollArea.setWidget(self.spectrumSelectionWidget)
    self.displayList.removeItem = self.removeListWidgetItem

    # self.layout.addWidget(self.nmrResidueTable, 4, 0, 1, 4)
    # # self.moreButton = Button(self, "More...", callback=self.showNmrResiduePopup)
    # # self.layout.addWidget(self.moreButton, 5, 0, 1, 1)

    # parent.window().showAtomSelector()

  def updateListWidget(self, item):
    if self.displayList.count() == 1 and self.displayList.item(0).text() == '<All>':
      self.displayList.takeItem(0)
    self.displayList.addItem(self.project.getByPid(item).pid)
    self.spectrumSelectionWidget.update()



  def removeListWidgetItem(self):
    self.displayList.takeItem(self.displayList.currentRow())
    if self.displayList.count() == 0:
      self.displayList.addItem('<All>')
    self.spectrumSelectionWidget.update()



  def toggleWidget2(self):
    if self.settingsButton.isChecked():
      self.widget2.show()
    else:
      self.widget2.hide()

  def refresh(self):
    pass

  def assignSelected(self):
    shiftDict = {}
    for atom in self.current.nmrResidue.nmrAtoms:
      shiftDict[atom.isotopeCode] = []

    for peak in self.current.peaks:
      shiftList = peak.peakList.spectrum.chemicalShiftList
      spectrum = peak.peakList.spectrum
      for nmrAtom in self.current.nmrResidue.nmrAtoms:
        if atom.isotopeCode in shiftDict.keys():
          shiftDict[nmrAtom.isotopeCode].append((nmrAtom, shiftList.getChemicalShift(nmrAtom.id).value))
      for ii, isotopeCode in enumerate(spectrum.isotopeCodes):
        for shift in shiftDict[isotopeCode]:
          sValue = shift[1]
          pValue = peak.position[ii]
          if abs(sValue-pValue) <= spectrum.assignmentTolerances[ii]:
            peak.assignDimension(spectrum.axisCodes[ii], [shift[0]])


  def restrictedPick(self, nmrResidue=None):
    # position = self.selectedPeak.position
    # axisCodes = self.selectedPeak.peakList.spectrum.axisCodes
    if nmrResidue:
      self.current.nmrResidue = nmrResidue
    elif not self.current.nmrResidue:
      print('No current nmrResidue')
      return
    else:
      nmrResidueIsotopeCodes = [atom.isotopeCode for atom in self.current.nmrResidue.nmrAtoms]
      for module in self.project.spectrumDisplays:
        # if len(module.strips[0].orderedAxes) > 2:
        for spectrumView in module.strips[0].spectrumViews:
          if spectrumView.isVisible():
            spectrum = spectrumView.spectrum
            shiftList = spectrum.chemicalShiftList
            nmrResidueShifts = [shiftList.getChemicalShift(nmrAtom.id).value for nmrAtom in self.current.nmrResidue.nmrAtoms]

            shiftDict = dict(zip(nmrResidueIsotopeCodes, nmrResidueShifts))
            stripAxisCodes = module.strips[0].axisCodes
            mappingArray = spectrumLib._axisCodeMapIndices(stripAxisCodes, spectrum.axisCodes)

            selectedRegion = [['']*len(module.axisCodes), ['']*len(module.axisCodes)]
            console = spectrum.project._appBase.mainWindow.pythonConsole
            for ii, stripAxisCode in enumerate(stripAxisCodes):
              if len(module.axisCodes) >= 3:
                if ii != 1:
                    isotopeCode = name2IsotopeCode(stripAxisCodes[ii])
                    tol = spectrum.assignmentTolerances[ii]
                    selectedRegion[0][ii] = shiftDict[isotopeCode]-tol
                    selectedRegion[1][ii] = shiftDict[isotopeCode]+tol
                else:
                    selectedRegion[0][ii] = spectrum.spectrumLimits[mappingArray[ii]][0]
                    selectedRegion[1][ii] = spectrum.spectrumLimits[mappingArray[ii]][1]
              else:
                isotopeCode = name2IsotopeCode(stripAxisCodes[ii])
                tol = spectrum.assignmentTolerances[ii]
                selectedRegion[0][ii] = shiftDict[isotopeCode]-tol
                selectedRegion[1][ii] = shiftDict[isotopeCode]+tol
            peakList = spectrumView.spectrum.peakLists[0]
            if spectrumView.spectrum.dimensionCount > 1:
              apiSpectrumView = spectrumView._wrappedData
              peaks = peakList.pickPeaksNd(selectedRegion, apiSpectrumView.spectrumView.orderedDataDims,
                                              doPos=apiSpectrumView.spectrumView.displayPositiveContours,
                                              doNeg=apiSpectrumView.spectrumView.displayNegativeContours)

              console.writeConsoleCommand(
                "peakList.pickPeaksNd(selectedRegion={0}, doPos={1}, doNeg={2})".format(
                  selectedRegion, apiSpectrumView.spectrumView.displayPositiveContours,
                  apiSpectrumView.spectrumView.displayNegativeContours
                ), peakList=peakList
              )
            if len(peaks) > 0:
              for strip in module.strips:
                strip.showPeaks(peakList)
                for peakListView in strip.peakListViews:
                  peakItems = [peakListView.peakItems[peak] for peak in peaks]
                  for peakItem in peakItems:
                    peakItem.setSelected(True)



  def goToPositionInModules(self, nmrResidue=None, row=None, col=None):
    navigateToNmrResidue(self.project, nmrResidue, markPositions=True)
    self.current.nmrResidue = nmrResidue

  def showNmrResiduePopup(self):
    from application.core.popups.NmrResiduePopup import NmrResiduePopup
    NmrResiduePopup(self, self.project).exec_()


class SpectrumSelectionWidget(QtGui.QWidget, Base):

  def __init__(self, parent, project, displayList, **kw):
    QtGui.QWidget.__init__(self, parent)
    Base.__init__(self, **kw)
    self.project = project
    self.spectrumLabel = Label(self, 'Spectrum')
    self.layout().addWidget(self.spectrumLabel, 0, 0)
    self.useLabel = Label(self, 'Use?', grid=(0, 1), hAlign='c')
    self.refreshBox = CheckBox(self, grid=(0, 4))
    self.checkBoxLabel = Label(self, 'Auto Refresh', grid=(0, 5))
    self.displayList = displayList
    self.update()

  def update(self):
    rowCount = self.layout().rowCount()
    colCount = self.layout().columnCount()

    for r in range(1, rowCount):
      for m in range(colCount):
        item = self.layout().itemAtPosition(r, m)
        if item:
          if item.widget():
            item.widget().hide()
        self.layout().removeItem(item)
    if self.displayList.count() == 1 and self.displayList.item(0).text() == '<All>':
      spectra = set([spectrumView.spectrum for spectrumDisplay in self.project.spectrumDisplays
                     for spectrumView in spectrumDisplay.spectrumViews])
    else:
      spectra = [spectrumView.spectrum for ii in range(self.displayList.count())
                 for spectrumView in self.project.getByPid(self.displayList.item(ii).text()).spectrumViews]

    for ii, spectrum in enumerate(spectra):
      spectrumLabel1 = Label(self, spectrum.pid, grid=(ii+1, 0), vAlign='t')
      spectrumCheckBox1 = CheckBox(self, grid=(ii+1, 1), hAlign='c', vAlign='t')
      spectrumCheckBox1.setChecked(True)
      spectrumTol1 = Label(self, spectrum.axisCodes[0], grid=(ii+1, 2), vAlign='t')
      spectrumTol1Value = DoubleSpinbox(self, grid=(ii+1, 3), vAlign='t')
      spectrumTol1Value.setDecimals(3)
      spectrumTol1Value.setSingleStep(0.001)
      spectrumTol1Value.setValue(spectrum.assignmentTolerances[0])

      spectrumTol2 = Label(self, spectrum.axisCodes[1], grid=(ii+1, 4), vAlign='t')
      spectrumTol2Value = DoubleSpinbox(self, grid=(ii+1, 5), vAlign='t')
      spectrumTol2Value.setDecimals(3)
      spectrumTol2Value.setSingleStep(0.001)
      spectrumTol2Value.setValue(spectrum.assignmentTolerances[1])

      if spectrum.dimensionCount > 2:
        for jj in range(spectrum.dimensionCount-2):
          spectrumTol3 = Label(self, spectrum.axisCodes[2+jj], grid=(ii+1+jj, 6), vAlign='t')
          spectrumTol3Value = DoubleSpinbox(self, grid=(ii+jj+1, 7), vAlign='t')
          spectrumTol3Value.setDecimals(3)
          spectrumTol3Value.setSingleStep(0.001)
          spectrumTol3Value.setValue(spectrum.assignmentTolerances[2+jj])




