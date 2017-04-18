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
__dateModified__ = "$dateModified: 2017-04-07 11:40:41 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: luca $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtGui, QtCore
from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.widgets.DateTime import DateTime
from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.TextEditor import TextEditor
from ccpn.ui.gui.widgets.RadioButtons import RadioButtons



OTHER_UNIT = ['µ','m', 'n', 'p']
CONCENTRATION_UNIT = ['µM', 'mM', 'nM', 'pM']
VOLUME_UNIT = ['µL', 'mL', 'nL', 'pL']
MASS_UNIT = ['µg','kg','g','mg', 'ng', 'pg']
SAMPLE_STATES = ['Liquid', 'Solid', 'Ordered', 'Powder', 'Crystal', 'Other']

AMOUNT_UNIT = ['L', 'g', 'mole']

class SamplePropertiesPopup(QtGui.QDialog):

  def __init__(self, sample, parent=None, project=None, **kw):
    super(SamplePropertiesPopup, self).__init__(parent)
    self.project = project
    self.sample = sample
    self._setMainLayout()
    self._setWidgets()
    self._addWidgetsToLayout(widgets=self._getAllWidgets(), layout= self.mainLayout)

  def _setMainLayout(self):
    self.mainLayout = QtGui.QGridLayout()
    self.setLayout(self.mainLayout)
    self.mainLayout.setContentsMargins(20, 20, 20, 10) #L,T,R,B
    self.setWindowTitle("Sample Properties")
    self.setMinimumWidth(400)
    self.setMaximumWidth(500)
    self.setMinimumHeight(410)
    self.setMaximumHeight(420)

  def _getWidgetsToSet(self):
    return (
            self._setSampleNameWidgets,
            self._setsampleAmountUnitWidgets,
            self._setsampleAmountWidgets,
            self._setsampleIonicStrengthWidgets,
            self._setSample_pHWidgets,
            # self._setSampleDateWidgets,
            self._setBatchIdentifierWidgets,
            self._setPlateIdentifierWidgets,
            self._setSampleRowNumberWidgets,
            self._setSampleColumnNumberWidgets,
            self._setSampleCommentWidgets,
            self._setPerformButtonWidgets
          )

  def _setWidgets(self):
    for setWidget in self._getWidgetsToSet():
      setWidget()


  def _addWidgetsToLayout(self, widgets, layout):
    count = int(len(widgets) / 2)
    self.positions = [[i + 1, j] for i in range(count) for j in range(2)]
    for position, widget in zip(self.positions, widgets):
      i, j = position
      layout.addWidget(widget, i, j)

  def _getAllWidgets(self):
    '''
    All widgets are ordered in the way they will be added to the layout EG:
    1)Label1 -> grid 0,0  ---- 2)LineEdit1 --> grid 0,1
    In this list are excluded the 'Cancel, Apply, Ok Buttons' '''

    return (
              self.sampleNameLabel, self.sampleNameLineEdit,
              self.sampleAmountUnitLabel, self.sampleAmountUnitRadioButtons,
              self.amountQuantityLabel, self.sampleAmountLineEdit,
              self.ionicStrengthLabel, self.ionicStrengthLineEdit,
              self.samplepHLabel, self.samplepHDoubleSpinbox,
              # self.sampleDate, self.sampleDateWidget,
              self.sampleBatchIdentifierLabel, self.batchIdentifierLineEdit,
              self.samplePlateIdentifierLabel, self.plateIdentifierLineEdit,
              self.samplerowNumberLabel, self.rowNumberLineEdit,
              self.sampleColumnNumberLabel, self.columnNumberLineEdit,
              self.sampleCommentLabel, self.commentTextEditor
           )

  def _setSampleNameWidgets(self):
    self.sampleNameLabel = Label(self, text="Name")
    self.sampleNameLineEdit = LineEdit(self)
    # self.sampleNameLineEdit.setFixedWidth(203)
    self.sampleNameLineEdit.setFixedHeight(25)
    self.sampleNameLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    self.sampleNameLineEdit.setText(self.sample.name)

  def _setsampleStateWidgets(self):
    self.sampleStateLabel = Label(self, text="State")
    self.sampleStatePulldownList = PulldownList(self)
    self.sampleStatePulldownList.addItems(SAMPLE_STATES)
    self.sampleStatePulldownList.setMinimumWidth(50)
    self.sampleStatePulldownList.setFixedHeight(25)
    self.sampleStatePulldownList.activated[str].connect(self._sampleStateChanged)

  def _setsampleAmountUnitWidgets(self):
    self.sampleAmountUnitLabel = Label(self, text="Amount Unit")
    self.sampleAmountUnitRadioButtons = RadioButtons(self, texts=AMOUNT_UNIT,
                                         selectedInd=1,
                                         callback=None,
                                         direction='h',
                                         tipTexts=None)
    if self.sample.amountUnit is not None:
      self.sampleAmountUnitRadioButtons.set(str(self.sample.amountUnit))

  def _setsampleAmountWidgets(self):
    self.amountQuantityLabel = Label(self, text='Amount')
    self.sampleAmountLineEdit = LineEdit(self)
    # self.sampleAmountLineEdit.setFixedWidth(203)
    self.sampleAmountLineEdit.setFixedHeight(25)
    self.sampleAmountLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if self.sample.amount is not None:
      self.sampleAmountLineEdit.setText(str(self.sample.amount))

  def _setsampleIonicStrengthWidgets(self):
    self.ionicStrengthLabel = Label(self, text='Ionic Strength')
    self.ionicStrengthLineEdit = LineEdit(self)
    self.ionicStrengthLineEdit.setFixedHeight(25)
    self.ionicStrengthLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if self.sample.ionicStrength is not None:
      self.ionicStrengthLineEdit.setText(str(self.sample.ionicStrength))

  def _setSample_pHWidgets(self):
    self.samplepHLabel = Label(self, text="pH ")
    self.samplepHDoubleSpinbox = DoubleSpinbox(self)
    self.samplepHDoubleSpinbox.setRange(0.00, 14.00)
    self.samplepHDoubleSpinbox.setSingleStep(0.01)
    # self.samplepHDoubleSpinbox.setFixedWidth(203)
    self.samplepHDoubleSpinbox.setFixedHeight(25)
    if self.sample.pH is not None:
      self.samplepHDoubleSpinbox.setValue(self.sample.pH)

  def _setSampleDateWidgets(self):
    self.sampleDate = Label(self, text="Sample Creation Date")
    self.sampleDateWidget = DateTime(self)
    # self.sampleDateWidget.setFixedWidth(203)
    self.sampleDateWidget.setFixedHeight(25)
    if self.sample.creationDate is None:
      setToday = QtCore.QDate.currentDate()
      self.sampleDateWidget.setDate(setToday)

  def _setBatchIdentifierWidgets(self):
    self.sampleBatchIdentifierLabel = Label(self, text="Sample Batch Identifier")
    self.batchIdentifierLineEdit = LineEdit(self)
    # self.plateIdentifierLineEdit.setFixedWidth(203)
    self.batchIdentifierLineEdit.setFixedHeight(25)
    self.batchIdentifierLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if hasattr(self.sample, 'batchIdentifier'):
      self.batchIdentifierLineEdit.setText(str(self.sample.batchIdentifier))

  def _setPlateIdentifierWidgets(self):
    self.samplePlateIdentifierLabel = Label(self, text="Sample Plate Identifier")
    self.plateIdentifierLineEdit = LineEdit(self)
    # self.plateIdentifierLineEdit.setFixedWidth(203)
    self.plateIdentifierLineEdit.setFixedHeight(25)
    self.plateIdentifierLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if self.sample.plateIdentifier is not None:
      self.plateIdentifierLineEdit.setText(str(self.sample.plateIdentifier))

  def _setSampleRowNumberWidgets(self):
    self.samplerowNumberLabel = Label(self, text="Sample Row Number")
    self.rowNumberLineEdit = LineEdit(self)
    # self.rowNumberLineEdit.setFixedWidth(203)
    self.rowNumberLineEdit.setFixedHeight(25)
    self.rowNumberLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if self.sample.rowNumber is not None:
      self.rowNumberLineEdit.setText(str(self.sample.rowNumber))

  def _setSampleColumnNumberWidgets(self):
    self.sampleColumnNumberLabel = Label(self, text="Sample Column Number")
    self.columnNumberLineEdit = LineEdit(self)
    # self.columnNumberLineEdit.setFixedWidth(203)
    self.columnNumberLineEdit.setFixedHeight(25)
    self.columnNumberLineEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    if self.sample.columnNumber is not None:
      self.columnNumberLineEdit.setText(str(self.sample.columnNumber))

  def _setSampleCommentWidgets(self):
    self.sampleCommentLabel = Label(self, text="Comment")
    self.commentTextEditor = LineEdit(self)
    self.commentTextEditor.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    # self.commentTextEditor.setFixedWidth(215)
    self.commentTextEditor.setFixedHeight(25)
    self.commentTextEditor.setText(self.sample.comment)

  def _setPerformButtonWidgets(self):
    self.buttonBox = ButtonList(self, callbacks=[self.reject, self._applyChanges, self._okButton], texts=['Cancel', 'Apply', 'Ok'])
    lastWidgetCount = int(len(self._getAllWidgets()) / 2)
    self.mainLayout.addWidget(self.buttonBox, lastWidgetCount+1, 1,)

  ######### Callbacks #########

  def _changeSampleName(self, value):
    if str(value) != self.sample.name:
      self.sample.rename(value)

  def _sampleAmountChanged(self, value):
    if value:
     self.sample.amount = float(value)

  def _sampleAmountUnitChanged(self, value):
    if value:
      self.sample.amountUnit = str(value)

  def _samplepHchanged(self, value):
    if value != self.sample.pH:
      self.sample.pH = value

  def _sampleIonicStrengthChanged(self, value):
    if value:
      self.sample.ionicStrength = float(value)

  def _sampleDateChanged(self, pressed):
    print(pressed, 'DateTime not yet implemented')

  def _batchIdentifierChanged(self, value):
    if value:
      self.sample.batchIdentifier = str(value)

  def _plateIdentifierChanged(self, value):
    if value:
      self.sample.plateIdentifier = str(value)

  def _rowNumberChanged(self,value):
    if value:
      self.sample.rowNumber = int(value)

  def _columnNumberChanged(self, value):
    if value:
      self.sample.columnNumber = int(value)

  def _commentChanged(self, value):
    self.sample.comment = value

  def _getCallBacksDict(self):
    return {
      self._changeSampleName: self.sampleNameLineEdit.text(),
      self._sampleAmountUnitChanged: self.sampleAmountUnitRadioButtons.get(),
      self._sampleAmountChanged: self.sampleAmountLineEdit.text(),
      self._samplepHchanged: self.samplepHDoubleSpinbox.value(),
      self._sampleIonicStrengthChanged: self.ionicStrengthLineEdit.text(),
      self._batchIdentifierChanged: self.batchIdentifierLineEdit.text(),
      self._plateIdentifierChanged: self.plateIdentifierLineEdit.text(),
      self._rowNumberChanged: self.rowNumberLineEdit.text(),
      self._columnNumberChanged: self.columnNumberLineEdit.text(),
      self._commentChanged: self.commentTextEditor.text()
    }

  def _applyChanges(self):
    for property, value in self._getCallBacksDict().items():
      property(value)

  def _okButton(self):
    self._applyChanges()
    self.accept()

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Enter:
      self._okButton()
    if event.key() == QtCore.Qt.Key_Escape:
      self.reject()
