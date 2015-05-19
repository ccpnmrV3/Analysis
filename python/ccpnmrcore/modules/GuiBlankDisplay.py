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
from PyQt4 import QtCore

from pyqtgraph.dockarea import Dock

from ccpn import Spectrum

from ccpncore.gui.Label import Label

from ccpnmrcore.DropBase import DropBase


def _findPpmRegion(spectrum, axisDim, spectrumDim):

  pointCount = spectrum.pointCounts[spectrumDim]
  if axisDim < 2: # want entire region
    region = (0, pointCount)
  else:
    n = pointCount // 2
    region = (n, n+1)

  firstPpm, lastPpm = spectrum.getDimValueFromPoint(spectrumDim, region)

  return 0.5*(firstPpm+lastPpm), abs(lastPpm-firstPpm)

class GuiBlankDisplay(DropBase, Dock): # DropBase needs to be first, else the drop events are not processed

  def __init__(self, dockArea):
    
    self.dockArea = dockArea
    
    Dock.__init__(self, name='BlankDisplay', size=(1100,1300))
    dockArea.addDock(self)

    self.label = Label(self, text='Drag Spectrum Here', textColor='#999', dragDrop=True)
    self.label.setAlignment(QtCore.Qt.AlignCenter)
    self.layout.addWidget(self.label)
    self.label.dropEvent = self.dropCallback

    DropBase.__init__(self, dockArea.guiWindow._appBase, self.dropCallback)

  def dropCallback(self, dropObject):
    
    dropObject.accept()
    data = dropObject.mimeData().data('application/x-qabstractitemmodeldatalist')
    pidData = str(data.data(),encoding='utf-8')
    pidData = [ch for ch in pidData if 32 < ord(ch) < 127]  # strip out junk
    actualPid = ''.join(pidData)
    wrapperObject = self.getObject(actualPid)
    if isinstance(wrapperObject, Spectrum):
      spectrum = wrapperObject
      spectrumDisplay = self.dockArea.guiWindow.createSpectrumDisplay(spectrum)
      spectrumView = self.getWrapperObject(spectrumDisplay._wrappedData.findFirstSpectrumView(dataSource=spectrum._wrappedData))
      for strip in spectrumView.strips:
        strip.displaySpectrum(spectrum)
      self.dockArea.guiWindow.removeBlankDisplay()
    import os
    if dropObject.mimeData().hasUrls():
      filePaths = [url.path() for url in dropObject.mimeData().urls()]
      if len(filePaths) > 1:
        for filePath in filePaths:
          spectrum = self.dockArea.guiWindow.project.loadSpectrum(filePath)
          self.dockArea.guiWindow.leftWidget.addSpectrum(spectrum)
          spectrumDisplay = self.dockArea.guiWindow.createSpectrumDisplay(spectrum)
        self.dockArea.guiWindow.removeBlankDisplay()
      else:
        if [dirpath.endswith('memops') and 'Implementation' in dirnames for dirpath, dirnames, filenames in os.walk(filePaths[0])]:
          self.dockArea.guiWindow._appBase.openProject(filePaths[0])
        else:
          spectrum = self.dockArea.guiWindow.project.loadSpectrum(filePaths[0])
          self.dockArea.guiWindow.leftWidget.addSpectrum(spectrum)
          spectrumDisplay = self.dockArea.guiWindow.createSpectrumDisplay(spectrum)
          self.dockArea.guiWindow.removeBlankDisplay()




