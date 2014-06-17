import numpy

from ccpncore.util.Color import Color

import pyqtgraph as pg

from ccpnmrcore.modules.spectrumPane.SpectrumItem import SpectrumItem

from ccpn.lib import Spectrum as LibSpectrum  # TEMP (should be direct function call on spectrum object some day)

class Spectrum1dItem:

  def __init__(self, parent, spectrumVar, region=None, dimMapping=None):
    """ spectrumPane is the parent
        spectrumVar is the Spectrum name or object
        region is in units of parent, ordered by spectrum dimensions
        dimMapping is from spectrum numerical dimensions to spectrumPane numerical dimensions
        (for example, xDim is what gets mapped to 0 and yDim is what gets mapped to 1)
    """

    self.spectrum = spectrumVar  # TEMP
    self.spectralData = self.getSliceData()
    self.spectrumItem = pg.PlotDataItem(self.spectralData)
    dimMapping = {} # this block of code TEMP
    for i in range(len(self.spectrum.pointCount)):
      dimMapping[i] = i
    # SpectrumItem.__init__(self, parent, spectrumVar, region, dimMapping)


  def getSliceData(self):

    spectrum = self.spectrum
    if spectrum.dimensionCount == 1: # TBD
      pointCount = spectrum.pointCount # this block of code TEMP
    region = [(0, pointCount[0])]
    dataDimRef = spectrum.ccpnSpectrum.findFirstDataDim().findFirstDataDimRef()

    firstPoint = dataDimRef.pointToValue(0)
    numpts = spectrum.ccpnSpectrum.findFirstDataDim().numPoints
    lastPoint = dataDimRef.pointToValue(numpts-1)
    pointSpacing = (lastPoint-firstPoint)/numpts

    position = numpy.array([firstPoint + n*pointSpacing for n in range(numpts)],numpy.float32)

   # below does not work yet
   #planeData = spectrum.getPlaneData(xDim=xDim, yDim=yDim)
    sliceData = LibSpectrum.getSliceData(spectrum)
    print(type(sliceData))
    spectrumData = []
    for x,y in zip(position,sliceData):
      spectrumData.append([x,y])
    return numpy.array(spectrumData,numpy.float32)