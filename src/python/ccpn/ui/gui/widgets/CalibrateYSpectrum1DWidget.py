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
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:32:47 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Luca Mureddu $"
__date__ = "$Date: 2017-07-25 11:28:58 +0100 (Tue, July 25, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.core.lib.SpectrumLib import _calibrateY1D
import pyqtgraph as pg

OP = 'Original Position: '
NP = 'New Position: '

ToolTip = 'Click the line to select. Hold left click and drag. Release the mouse to set the original ' \
          'position to the new position '

class CalibrateY1DWidgets(Frame):
  def __init__(self, parent=None, mainWindow=None,  **kw):
    Frame.__init__(self, parent, setLayout=True, **kw)

    if mainWindow is None:  # This allows opening the popup for graphical tests
      self.mainWindow = None
      self.project = None
    else:
      self.mainWindow = mainWindow
      self.project = self.mainWindow.project
      self.application = self.mainWindow.application
      self.current = self.application.current

    self.originalPosition = None
    self.newPosition = None

    i=0
    self.labelOriginalPosition = Label(self, OP,grid=(0, i))
    i += 1
    self.boxOriginalPosition = DoubleSpinbox(self, step=0.001, decimals=3, grid=(0, i))
    i += 1
    self.labelNewPosition = Label(self, NP, grid=(0, i))
    i += 1
    self.boxNewPosition = DoubleSpinbox(self, step=0.001, decimals=3, grid=(0, i))
    i += 1
    self.okButtons = ButtonList(self, ['Cancel', 'Apply'], callbacks=[self._close, self._calibrateSpectra],
                                grid=(0,i))

    self.infiniteLine = pg.InfiniteLine(movable=True, angle=0)
    self.originalPosInfiniteLine = pg.InfiniteLine(movable=False, angle=0, pen='g')

    # self.infiniteLine.sigPositionChangeFinished.connect(self._calibrateSpectra)
    self.infiniteLine.sigPositionChanged.connect(self._newPositionLineCallback)

    self.boxOriginalPosition.valueChanged.connect(self._originalPositionBoxCallback)
    self.boxNewPosition.valueChanged.connect(self._newPositionBoxCallback)

    self._initLines()

  def _initLines(self):
    if self.mainWindow is not None:
      if self.current.strip is not None:
        self.current.strip.plotWidget.addItem(self.infiniteLine)
        self.current.strip.plotWidget.addItem(self.originalPosInfiniteLine)

      if len(self.current.cursorPosition)>0:
        self.originalPosition = self.current.cursorPosition[1]
        self.infiniteLine.setValue(self.originalPosition)
        self.originalPosInfiniteLine.setValue(self.originalPosition)
        self.boxOriginalPosition.setValue(round(self.originalPosition,3))


  def _newBoxCallback(self):
    spinboxValue = self.sender().value()
    self.infiniteLine.setValue(spinboxValue)

  def _newPositionLineCallback(self):
    self.newPosition = self.infiniteLine.pos().y()
    self.boxNewPosition.setValue(round(self.newPosition, 3))

  def _newPositionBoxCallback(self):
    box = self.sender()
    self.newPosition = round(box.value(),3)
    self.infiniteLine.setValue(self.newPosition)

  def _originalPositionBoxCallback(self):
    box = self.sender()
    self.originalPosition = round(box.value(),3)
    self.originalPosInfiniteLine.setValue(self.originalPosition)


  def _removeLines(self):
    if self.mainWindow is not None:
      if self.current.strip is not None:
        self.current.strip.plotWidget.removeItem(self.infiniteLine)
        self.current.strip.plotWidget.removeItem(self.originalPosInfiniteLine)


  def _toggleLines(self):
    if self.isVisible():
      self._initLines()
    else:
      self._removeLines()

  def _calibrateSpectra(self):

    if self.mainWindow is not None:
      if self.current.strip is not None:
        for spectrumView in self.current.strip.spectrumViews:
          if spectrumView.plot.isVisible():
            spectrum = spectrumView.spectrum
            _calibrateY1D(spectrum, self.originalPosition, self.newPosition)

    self.originalPosInfiniteLine.setValue(self.infiniteLine.pos().y())
    self._close()


  def _close(self):
    self.setVisible(False)
    self._toggleLines()


if __name__ == '__main__':
  from ccpn.ui.gui.widgets.Application import TestApplication
  from ccpn.ui.gui.popups.Dialog import CcpnDialog

  app = TestApplication()
  popup = CcpnDialog()
  f = CalibrateY1DWidgets(popup)

  popup.show()
  popup.raise_()

  app.start()
