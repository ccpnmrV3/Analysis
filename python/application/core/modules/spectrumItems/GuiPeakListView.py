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
from PyQt4 import QtCore, QtGui

import pyqtgraph as pg

from ccpn import Project
from ccpn import Peak
from ccpn import PeakList
from ccpncore.api.ccp.nmr.Nmr import AbstractPeakDimContrib as ApiAbstractPeakDimContrib
from ccpncore.api.ccp.nmr.Nmr import Resonance as ApiResonance
from ccpncore.api.ccp.nmr.Nmr import ResonanceGroup as ApiResonanceGroup
from ccpncore.api.ccp.nmr.Nmr import NmrChain as ApiNmrChain
from ccpncore.api.ccp.nmr.Nmr import PeakDim as ApiPeakDim
from ccpncore.api.ccp.nmr.Nmr import Peak as ApiPeak
from ccpncore.api.ccp.nmr.Nmr import DataDimRef as ApiDataDimRef
from ccpncore.api.ccp.nmr.Nmr import FreqDataDim as ApiFreqDataDim

NULL_RECT = QtCore.QRectF()
IDENTITY = QtGui.QTransform()
IDENTITY.reset()
# class PeakLayer(QtGui.QGraphicsItem):
#
#   def __init__(self, scene):
#
#     QtGui.QGraphicsItem.__init__(self, scene=scene)
#
#     # self.glWidget = glWidget
#     self.peaks = {}
#     self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, True)
#
#
#   def boundingRect(self):
#
#     return NULL_RECT
#
#   def paint(self, painter, option, widget):

    # return
#
# def peakItemNotifier(project, apiPeak):
#   apiPeakListViews = apiPeak.PeakList.PeakListViews
#   for apiPeakListView in apiPeakListViews:
#     for apiStripPeakListView in apiPeakListView._apiStripPeakListViews:

def _getPeakAnnotation(peak):

  peakLabel = []
  for dimension in range(peak.peakList.spectrum.dimensionCount):
    if len(peak.dimensionNmrAtoms[dimension]) == 0:
      if len(peak.dimensionNmrAtoms) == 1:
        peakLabel.append('1H')
      else:
        peakLabel.append('-')
    else:
      peakNmrResidues = [atom[0].nmrResidue.id for atom in peak.dimensionNmrAtoms if len(atom) != 0]
      if all(x==peakNmrResidues[0] for x in peakNmrResidues):
        for item in peak.dimensionNmrAtoms[dimension]:
          if len(peakLabel) > 0:
            peakLabel.append(item.name)
          else:
            peakLabel.append(item.pid.id)

      else:
        for item in peak.dimensionNmrAtoms[dimension]:
          label = item.nmrResidue.id+item.name
          peakLabel.append(label)

  text = ', '.join(peakLabel)

  return text

class GuiPeakListView(QtGui.QGraphicsItem):

  # def __init__(self, scene, strip, peakList):
  def __init__(self):
    """ peakList is the CCPN wrapper object
    """

    strip = self.spectrumView.strip
    scene = strip.plotWidget.scene()
    QtGui.QGraphicsItem.__init__(self, scene=scene)
    ###self.strip = strip
    ###self.peakList = peakList
    self.peakItems = {}  # CCPN peak -> Qt peakItem
    self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, True)
    self._appBase = strip._appBase
    
    strip.viewBox.addItem(self)
    ###self.parent = parent
    # self.displayed = True
    # self.symbolColour = None
    # self.symbolStyle = None
    # self.isSymbolDisplayed = True
    # self.textColour = None
    # self.isTextDisplayed = True
    # self.regionChanged()

  # def showIcons(self, peakItem):
  #
  #   self.assignIcon.syncPeak(peakItem)
  #   self.deleteIcon.syncPeak(peakItem)
  #   self.moveIcon.syncPeak(peakItem)
  #   self.cleanIcon.syncPeak(peakItem)
  #   self.menuIcon.syncPeak(peakItem)
  #
  # def hideIcons(self):
  #
  #   self.assignIcon.hide()
  #   self.deleteIcon.hide()
  #   self.moveIcon.hide()
  #   self.cleanIcon.hide()
  #   self.menuIcon.hide()

  def printToFile(self, printer):

    width = printer.width
    height = printer.height
    scale = 0.02
    peakHalfSize = scale * max(width, height)
    strip = self.spectrumView.strip
    plotWidget = strip.plotWidget
    viewRegion = plotWidget.viewRange()
    dataDims = self.spectrumView._wrappedData.spectrumView.orderedDataDims
    
    x1, x0 = viewRegion[0]  # TBD: relies on axes being backwards
    xScale = width / (x1 - x0)
    xTranslate = printer.x0 - x0 * xScale
    
    y1, y0 = viewRegion[1]  # TBD: relies on axes being backwards
    yScale = width / (y1 - y0)
    yTranslate = printer.y0 - y0 * yScale
        
    for peak in self.peakList.peaks:
      if strip.peakIsInPlane(peak):
        xPpm = xScale*peak.position[dataDims[0].dimensionIndex] + xTranslate
        yPpm = yScale*peak.position[dataDims[1].dimensionIndex] + yTranslate
        a0 = xPpm - peakHalfSize
        b0 = height - (yPpm - peakHalfSize)
        a1 = xPpm + peakHalfSize
        b1 = height - (yPpm + peakHalfSize)
        printer.writeLine(a0, b0, a1, b1)
        printer.writeLine(a0, b1, a1, b0)

        text = _getPeakAnnotation(peak)
        if text:
          offset = 0.5 * peakHalfSize
          printer.writeText(text, a1+offset, b1-offset)

  def regionChanged(self):

    parent = self.parent
    xValRange = parent.orderedAxes[0].region
    yValRange = parent.orderedAxes[1].region

    xr1, xr2 = xValRange
    yr1, yr2 = yValRange

    dx = xr1-xr2
    dy = yr1-yr2

    w, h, = self.parent.geometry()[:2]

    self.setTransform(IDENTITY)
    self.scale(-w/dx, h/dy)

    xPos = w * xr1/dx
    yPos = h - (h * yr1/dy)

    inverse, isOk = self.transform().inverted()

    self.setPos(xPos, yPos)

    # for peak in peakList.peaks:
    #   peakItem = Peak1d(scene, parent, peak, peakList)
    #   peakItem.setParentItem(self)
      # scene.addItem(peakItem)
      # self.addToGroup(peakItem)
    # print(self)

  # def createPeakItems(self):
  #   for peak in self.peakList.peaks:
  #     print(peak, peak.pid)
  #     self.peakItems[peak.pid] = PeakItem(self, peak)
  def boundingRect(self):

    return NULL_RECT


  def paint(self, painter, option, widget):

    return

class Peak1d(QtGui.QGraphicsItem):
  """ A GraphicsItem that is not actually drawn itself, but is the parent of the peak symbol and peak annotation.
      TODO: Add hover effect for 1D peaks. """

  def __init__(self, peakListView, peak):


    scene = peakListView.spectrumView.strip.plotWidget.scene()
    QtGui.QGraphicsItem.__init__(self, parent=peakListView, scene=scene)

    self.peakHeight = peak.height
    self.peak = peak
    self.peakListView = peakListView
    self.dim = 0
    self.spectrum = peak.peakList.spectrum
    # self.spectrumView, spectrumMapping = self.spectrumWindow.getViewMapping(analysisSpectrum)
    # self.setZValue(10)
    self.screenPos = []

    self.annotation = Peak1dAnnotation(self, scene)
    self.setupPeakItem(peakListView, peak)
    self.press = False
    self.setAcceptHoverEvents(True)
    self.annotationScreenPos = []
    self.bbox = NULL_RECT
    self.setCacheMode(self.NoCache)
    self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, True)
    self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
    # self.scene().sigMouseClicked.connect(self.peakClicked)
    self.pointPos = peak.pointPosition
    self.ppm = peak.position[self.dim]

    # self.height = self.peak.height
    # if not self.height:
    #   height = self.peak._apiPeak.findFirstPeakIntensity(intensityType = 'height')
    #   if height:
    #     self.height = height.value
    #   else:
    #     self.height = 0
    # # self.height *= self.spectrum.scale
    #
    # # if peakDims[dim].numAliasing:
    # #   self.isAliased = True
    # # else:
    # #   self.isAliased = False
    # if self.ppm and self.height:
    #   self.setPos(self.ppm, self.height)

    # try:
    self.symbol = Peak1dSymbol(scene, self)
    # except AttributeError:
    #   return

    # group.addToGroup(self)
  #
  def setupPeakItem(self, peakListView, peak):

    self.peakListView = peakListView
    self.peak = peak
    if not hasattr(peak, 'isSelected'):
      peak.isSelected = False
    self.setSelected(peak.isSelected)
    # This code does not make sense - you need its own spectrumView, not the zero'th
    # dimensionOrdering = peakListView.spectrumView.strip.spectrumViews[0].dimensionOrdering
    # dimensionOrdering deprecated
    dataDims = peakListView.spectrumView._wrappedData.spectrumView.orderedDataDims
    xPpm = peak.position[dataDims[0].dimensionIndex]
    # dimensionOrdering = peakListView.spectrumView.strip.spectrumViews[0].dimensionOrdering
    # xDim = dimensionOrdering[0] - 1
    # yDim = dimensionOrdering[1] - 1
    # xPpm = peak.position[xDim]
    # yPpm = peak.position[yDim]
    self.setPos(xPpm, peak.height)
    self.annotation.setupPeakAnnotation(self)
    peakListView.peakItems[self.peak] = self

  def mousePressEvent(self, event):

    self.press = True
    self.hover = True
    print('pressed')

  # def mousePressEvent(self, event):
  #
  #   if (event.button() == QtCore.Qt.LeftButton) and (
  #             event.modifiers() & QtCore.Qt.ControlModifier) and not (
  #             event.modifiers() & QtCore.Qt.ShiftModifier):
  #
  #     event.accept()
  #     self.scene.clearSelection()
  #     self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
  #     QtGui.QGraphicsSimpleTextItem.mousePressEvent(self, event)
  #     self.setSelected(True)
  #     print(self.peak)


  def boundingRect(self):

    return NULL_RECT


  def paint(self, painter, option, widget):

    return

class Peak1dAnnotation(QtGui.QGraphicsSimpleTextItem):
  """ A text annotation of a peak.
      The text rotation is currently always +-45 degrees (depending on peak height). """

  def __init__(self, peakItem, scene):

    QtGui.QGraphicsSimpleTextItem.__init__(self, scene=scene)

    self.setParentItem(peakItem)
    self.peakItem = peakItem # When exporting to e.g. PDF the parentItem is temporarily set to None, which means that there must be a separate link to the PeakItem.
    self.scene = scene
    font = self.font()
    font.setPointSize(10)
    self.setFont(font)
    # self.setCacheMode(self.DeviceCoordinateCache)
    self.setFlag(self.ItemIgnoresTransformations, True)
    # self.setFlag(self.ItemIsMovable, True)
    # self.setFlag(self.ItemIsSelectable, True)
    # self.setFlag(self.ItemSendsScenePositionChanges, True)
    # if self.isSelected():
    #   print(self)
    self.colourScheme = peakItem.peakListView._appBase.preferences.general.colourScheme
    # color.setRgbF(*self.peakItem.glWidget._hexToRgba(textColor))
    self.setColour()
    self.updatePos()
    self.setupPeakAnnotation(peakItem)

  def sceneEventFilter(self, watched, event):
    print(event)

  def mousePressEvent(self, event):

    if (event.button() == QtCore.Qt.LeftButton) and (
              event.modifiers() & QtCore.Qt.ControlModifier) and not (
              event.modifiers() & QtCore.Qt.ShiftModifier):

      event.accept()
      self.scene.clearSelection()
      self.setFlag(QtGui.QGraphicsSimpleTextItem.ItemIsMovable)
      QtGui.QGraphicsSimpleTextItem.mousePressEvent(self, event)
      self.setSelected(True)
      self.update()


  def setupPeakAnnotation(self, peakItem):
    self.peakItem = peakItem # When exporting to e.g. PDF the parentItem is temporarily set to None, which means that there must be a separate link to the PeakItem.
    self.setParentItem(peakItem)

    peak = peakItem.peak
    text = _getPeakAnnotation(peak)
    self.setText(text)

  def updatePos(self):

    peakItem = self.peakItem
    if peakItem.peakHeight >= 0:
      # Translate first to rotate around bottom left corner
      self.translate(0, -self.boundingRect().height())
      self.setRotation(0)
      self.setPos(0, min(peakItem.pos().y()*0.75, peakItem.spectrum.positiveContourBase * peakItem.spectrum.scale))
      # print(peakItem.height, max(peakItem.pos().y()*0.75, peakItem.spectrum.positiveContourBase * peakItem.spectrum.scale))
    else:
      self.setPos(0, min(peakItem.pos().y()*0.75, -peakItem.spectrum.positiveContourBase * peakItem.spectrum.scale))
      self.setRotation(45)

  def setColour(self):
    if self.colourScheme == 'light':
      colour = QtGui.QColor('#080000')
    else:
      colour = QtGui.QColor('#f7ffff')
    self.setBrush(colour)
    textColor = colour

  def paint(self, painter, option, widget):

    QtGui.QGraphicsSimpleTextItem.paint(self, painter, option, widget)
    # if self.peakItem.peak in self.analysisLayout.currentPeaks:
    # painter.drawRect(self.boundingRect())

class Peak1dSymbol(QtGui.QGraphicsItem):
  """ A graphical symbol representing the peak.
      Currently only a dashed line from the peak to the peak annotation is used. This can be improved.
      The length of the line is related to the height of the peak. """

  def __init__(self, scene, parent):

    QtGui.QGraphicsItem.__init__(self, scene=scene)

    self.setParentItem(parent)
    self.peakItem = parent
    self.setCacheMode(self.DeviceCoordinateCache)
    # self.setFlag(self.ItemIsMovable, True)
    # self.setFlag(self.ItemIsSelectable, True)
    self.lineWidth = 0
    self.setPos(0, 0)
    self.setBbox()
    self.update()

  def boundingRect(self):

    return self.bbox

  def setBbox(self):

    peakItem = self.peakItem

    if self.pos().x() < peakItem.annotation.pos().x():
      left = self.pos().x()
      right = peakItem.annotation.pos().x()
    else:
      left = peakItem.annotation.pos().x()
      right = self.pos().x()

    if self.pos().y() < peakItem.annotation.pos().y():
      upper = self.pos().y()
      lower = peakItem.annotation.pos().y()
    else:
      upper = peakItem.annotation.pos().y()
      lower = self.pos().y()
    # print(left, right)
    self.bbox = QtCore.QRectF(QtCore.QPointF(left, upper), QtCore.QPointF(right, lower))

  def paint(self, painter, option, widget):

    peakItem = self.peakItem

    pos = QtCore.QPointF(0, 0) # When exporting to e.g. pdf the symbol has no parent item, which means that its position is its screen pos.
                               # To compensate for that the line pos needs to be explicitly (0, 0).
    if self.parentItem():
      annotationPos = peakItem.annotation.pos()
    else:
      annotationPos = peakItem.annotation.scenePos() - self.scenePos() - QtCore.QPointF(5, 5) # Fix for export to e.g. PDF

    pen = painter.pen()
    pen.setStyle(QtCore.Qt.DashLine)
    pen.setWidth(self.lineWidth)
    self.colourScheme = peakItem.peakListView._appBase.preferences.general.colourScheme
    if self.colourScheme == 'light':
      colour = QtGui.QColor('#080000')
    else:
      colour = QtGui.QColor('#f7ffff')
    # self.setBrush(colour)
    # lineColor = peakItem.analysisPeakList.symbolColor
    # color.setRgbF(*peakItem.glWidget._hexToRgba(lineColor))
    #
    # if peakItem.peak not in self.analysisLayout.currentPeaks:
    #   color.setAlphaF(0.5)

    pen.setColor(colour)
    painter.setPen(pen)

    painter.drawLine(pos, annotationPos)

    self.setBbox()

  def mousePressEvent(self, event):

    if (event.button() == QtCore.Qt.LeftButton) and (
              event.modifiers() & QtCore.Qt.ControlModifier) and not (
              event.modifiers() & QtCore.Qt.ShiftModifier):

      event.accept()
      self.scene.clearSelection()
      self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
      QtGui.QGraphicsSimpleTextItem.mousePressEvent(self, event)
      self.setSelected(True)
      self.update()



class PeakNd(QtGui.QGraphicsItem):

  def __init__(self, peakListView, peak):

    self._appBase = peakListView._appBase
    scene = peakListView.spectrumView.strip.plotWidget.scene()
    #QtGui.QGraphicsItem.__init__(self, scene=scene)
    self.colourScheme =self._appBase.preferences.general.colourScheme
    QtGui.QGraphicsItem.__init__(self, parent=peakListView, scene=scene)
    ###QtGui.QGraphicsItem.__init__(self, peakLayer)
    ###scene.addItem(self)
    ###strip.plotWidget.plotItem.vb.addItem(self)
    # turn off ItemIsSelectable because it fails miserably when you zoom in (have to pick exactly in the centre)
    self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable + self.ItemIgnoresTransformations)
    self.setFlag(self.ItemIgnoresTransformations)
    self.peakListView = peakListView
    self.annotation = PeakNdAnnotation(self, scene)
    self.setupPeakItem(peakListView, peak)
    # self.glWidget = peakLayer.glWidget
    #self.setParentItem(peakLayer)
    ###self.peakLayer = peakLayer
    # self.spectrumWindow = spectrumWindow
    # self.panel = spectrumWindow.panel
    #self.peakList = peak._parent
    ##self.strip = strip
    #self.parent = strip.plotWidget
    #self.spectrum = self.peakList.spectrum
    #self.setCacheMode(self.NoCache)
    #self.setFlags(self.ItemIgnoresTransformations)
    # self.setSelected(False)
    #self.hover = False
    #self.press = False
    #self.setAcceptHoverEvents(True)
    #self.bbox  = NULL_RECT
    #self.color = NULL_COLOR
    #self.brush = NULL_COLOR
    ###self.peak = peak
    ###xPpm = peak.position[0]
    ###yPpm = peak.position[1]
    # self.setPos(self.parent.viewBox.mapSceneToView
    sz = peakListView.spectrumView.strip.viewBox.peakWidthPixels
    hz = sz/2.0
    # self.bbox = QtCore.QRectF(-hz, -hz, sz, sz)
    # self.drawData = (hz, sz, QtCore.QRectF(-hz, -hz, sz, sz))
    """
    self.rectItem = QtGui.QGraphicsRectItem(-hz, -hz, sz, sz, self.peakLayer, scene)
    color = QtGui.QColor('cyan')
    self.rectItem.setBrush(QtGui.QBrush(color))
    """
    self.drawData = (hz, sz)#, QtCore.QRectF(-hz, -hz, sz, sz))
    ###xDim = strip.spectrumViews[0].dimensionOrdering[0] - 1
    ###yDim = strip.spectrumViews[0].dimensionOrdering[1] - 1
    ###xPpm = peak.position[xDim] # TBD: does a peak have to have a position??
    ###yPpm = peak.position[yDim]
    ###self.setPos(xPpm, yPpm)
    # self.inPlane = self.isInPlane()

    # from ccpncore.gui.Action import Action
    # self.deleteAction = QtGui.QAction(self, triggered=self.deletePeak, shortcut=QtCore.Qt.Key_Delete)
    #peakLayer.peakItems.append(self)
  #
  
  def setupPeakItem(self, peakListView, peak):

    self.peakListView = peakListView
    self.peak = peak
    if not hasattr(peak, 'isSelected'):
      peak.isSelected = False
    self.setSelected(peak.isSelected)
    # This code does not make sense - you need its own spectrumView, not the zero'th
    # dimensionOrdering = peakListView.spectrumView.strip.spectrumViews[0].dimensionOrdering
    # dimensionOrdering deprecated
    dataDims = peakListView.spectrumView._wrappedData.spectrumView.orderedDataDims
    xPpm = peak.position[dataDims[0].dimensionIndex]
    yPpm = peak.position[dataDims[1].dimensionIndex]
    # dimensionOrdering = peakListView.spectrumView.strip.spectrumViews[0].dimensionOrdering
    # xDim = dimensionOrdering[0] - 1
    # yDim = dimensionOrdering[1] - 1
    # xPpm = peak.position[xDim]
    # yPpm = peak.position[yDim]
    self.setPos(xPpm, yPpm)
    self.annotation.setupPeakAnnotationItem(self)
    peakListView.peakItems[self.peak] = self

  # replaced by Strip.peakIsInPlane
  # def isInPlane(self):
  #
  #   orderedAxes = self.peakListView.spectrumView.strip.orderedAxes
  #   for ii,zDataDim in enumerate(self.peakListView._wrappedData.spectrumView.orderedDataDims[2:]):
  #     zPosition = self.peak.position[zDataDim.dimensionIndex]
  #     zPlaneSize = zDataDim.getDefaultPlaneSize()
  #     zRegion = orderedAxes[2+ii].region
  #     if zPosition < zRegion[0]-zPlaneSize or zPosition > zRegion[1]+zPlaneSize:
  #       return False
  #   #
  #   return True

    # strip = self.peakListView.spectrumView.strip
    #
    # if len(strip.orderedAxes) > 2:
    #   zDim = strip.spectrumViews[0].dimensionOrdering[2] - 1
    #   zPlaneSize = strip.spectrumViews[0].zPlaneSize()
    #   zPosition = self.peak.position[zDim]
    #
    #   zRegion = strip.orderedAxes[2].region
    #   if zRegion[0]-zPlaneSize <= zPosition <= zRegion[1]+zPlaneSize:
    #     return True
    #   else:
    #     return False
    # else:
    #   return True

  # def hoverEnterEvent(self, event):
  #
  #   self.hover = True
  #   self.annotation.hoverEnterEvent(event)
  #   self.update()
  #
  # def hoverLeaveEvent(self, event):
  #
  #   self.hover = False
  #   self.press = False
  #   r, w, box = self.drawData
  #   self.bbox = box
  #   self.peakLayer.hideIcons()
  #   self.annotation.hoverLeaveEvent(event)
  #   self.update()

  ###def mousePressEvent(self, event):

    ###print(event)
    # self.setSelected(True)
    # self.press = True
    # self.hover = True
    ###r, w, box = self.drawData
    ###self.bbox = box.adjusted(-26,-51, 2, 51)
    # # self.peakLayer.showIcons(self)
    # self.update()
    # QtGui.QGraphicsItem.mousePressEvent(self, event)


  def boundingRect(self):

    ###return self.bbox # .adjust(-2,-2, 2, 2)
    
    r, w  = self.drawData
    
    return QtCore.QRectF(-r,-r,2*r,2*r)

  def itemChange(self, change, value):
    
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged:
      peak = self.peak
      selected = peak.isSelected = self.isSelected()
      current = self._appBase.current
      if selected:
        if peak not in current.peaks:
          current.addPeak(peak)
      else:
        if peak in current.peaks:
          current.removePeak(peak)
    
    return QtGui.QGraphicsItem.itemChange(self, change, value)
    
  def paint(self, painter, option, widget):

    if self.peakListView.isDeleted: # strip has been deleted
      return
      
    if self.peak: # TBD: is this ever not true??
      self.setSelected(self.peak.isSelected) # need this because dragging region to select peaks sets peak.isSelected but not self.isSelected()
      if self.peakListView.spectrumView.strip.peakIsInPlane(self.peak):
      # if self.isInPlane():
        # r, w, box = self.drawData
        r, w = self.drawData

        # if self.hover:
        # self.setZValue(10)
        #painter.setBrush(NULL_COLOR)

        # painter.setPen(QtGui.QColor('white'))
        # if self.press:
        #   painter.drawRect(self.bbox)
        ###strip = self.strip
        ###peak = self.peak
        ###xDim = strip.spectrumViews[0].dimensionOrdering[0] - 1
        ###yDim = strip.spectrumViews[0].dimensionOrdering[1] - 1
        ###xPpm = peak.position[xDim] # TBD: does a peak have to have a position??
        ###yPpm = peak.position[yDim]
        ###self.setPos(xPpm, yPpm)

        if widget:
          if self.colourScheme == 'light':
            painter.setPen(QtGui.QColor('#080000'))
          else:
            painter.setPen(QtGui.QColor('#f7ffff'))
        else:
          painter.setPen(QtGui.QColor('black'))
        # painter.drawEllipse(box)

        # else:
        #   painter.setPen(self.color)
        #   self.setZValue(0)
        painter.drawLine(-r,-r,r,r)
        painter.drawLine(-r,r,r,-r)
        ###painter.drawLine(xPpm-r,yPpm-r,xPpm+r,yPpm+r)
        ###painter.drawLine(xPpm-r,yPpm+r,xPpm+r,yPpm-r)
        
        if self.peak.isSelected:
          painter.drawLine(-r,-r,-r,r)
          painter.drawLine(-r,r,r,r)
          painter.drawLine(r,r,r,-r)
          painter.drawLine(r,-r,-r,-r)
        #
        # if self.isSelected:
        #   painter.setPen(QtGui.QColor('white'))
        #   painter.drawRect(-r,-r,w,w)


###FONT = QtGui.QFont("DejaVu Sans Mono", 9)
###FONT_METRIC = QtGui.QFontMetricsF(FONT)
###NULL_COLOR = QtGui.QColor()
###NULL_RECT = QtCore.QRectF()

class PeakNdAnnotation(QtGui.QGraphicsSimpleTextItem):
  """ A text annotation of a peak.
      The text rotation is currently always +-45 degrees (depending on peak height). """

  def __init__(self, peakItem, scene):

    QtGui.QGraphicsSimpleTextItem.__init__(self, scene=scene)

    ###self.setParentItem(peakItem)
    ###self.peakItem = peakItem # When exporting to e.g. PDF the parentItem is temporarily set to None, which means that there must be a separate link to the PeakItem.
    ###self.setText(text)
    ###self.scene = scene
    ###self.setColor()
    # self.analysisLayout = parent.glWidget.analysisLayout
    font = self.font()
    font.setPointSize(10)
    self.setFont(font)
    # self.setCacheMode(self.DeviceCoordinateCache)
    self.setFlag(self.ItemIgnoresTransformations)#+self.ItemIsMovable+self.ItemIsSelectable)
    # self.setFlag(self.ItemSendsScenePositionChanges, True)

    # self.text = (' , ').join('-' * peakItem.peak.peakList.spectrum.dimensionCount)
    # if self.isSelected():
    #   print(self)
    self.colourScheme = peakItem.peakListView._appBase.preferences.general.colourScheme
    if self.colourScheme == 'light':
      colour = QtGui.QColor('#080000')
    else:
      colour = QtGui.QColor('#f7ffff')
    self.setBrush(colour)
    ###self.setColor()
    self.setPos(15, -15)
    # self.updatePos()
        
  def setupPeakAnnotationItem(self, peakItem):
    
    self.peakItem = peakItem # When exporting to e.g. PDF the parentItem is temporarily set to None, which means that there must be a separate link to the PeakItem.
    self.setParentItem(peakItem)
    
    peak = peakItem.peak
    text = _getPeakAnnotation(peak)
        
    self.setText(text)

  """
  def setColor(self):

    color = QtGui.QColor('white')
    textColor = color
    # color.setRgbF(*self.peakItem.glWidget._hexToRgba(textColor))
    self.setBrush(QtGui.QBrush(color))

  def paint(self, painter, option, widget):
    if self.peakItem.isInPlane():
      peakItem = self.peakItem
      peakLabel = []
      for dimension in range(peakItem.peak.peakList.spectrum.dimensionCount):
        if len(peakItem.peak.dimensionNmrAtoms[dimension]) == 0:
          peakLabel.append('-')
        else:
          for item in peakItem.peak.dimensionNmrAtoms[dimension]:

            if len(peakLabel) > 0:
              # print(, peakLabel[-1])
              peakLabel.append(item.pid.id.split('.')[-1])

            else:
              peakLabel.append(item.pid.id)

      text = ','.join(peakLabel)
      painter.setBrush(QtGui.QBrush(QtGui.QColor('white')))

      painter.drawText(0, 0, text)
    # if self.peakItem.peak in self.analysisLayout.currentPeaks:
    # painter.drawRect(self.boundingRect())

  #def sceneEventFilter(self, watched, event):
  #  print(event)
"""
  def mousePressEvent(self, event):


    if (event.button() == QtCore.Qt.LeftButton):# and (
              # event.modifiers() & QtCore.Qt.ControlModifier) and not (
              # event.modifiers() & QtCore.Qt.ShiftModifier):
      event.accept()
      # self.scene.clearSelection()
      # self.setFlag(QtGui.QGraphicsSimpleTextItem.ItemIsMovable)
      # QtGui.QGraphicsSimpleTextItem.mousePressEvent(self, event)
      # self.setSelected(True)
      # print(self.peakItem)
      # self.update()



# Notifiers for assignment annotation change
# Needed for:
# AbstractPeakDimContrib init and delete
# Resonance.setImplName, setResonanceGroup
# ResonanceGroup.setResonances, .setAssignedResidue, .setSequenceCode, .setResidueType
#   .setNmrChain
# NmrChain.setCode - NOT setResonanceGroups, as this calls setNmrChain on the other side.

def _refreshPeakAnnotation(peak:Peak):
  data2Obj = peak._project._data2Obj
  for apiPeakListView in peak._wrappedData.peakList.peakListViews:
    for apiStripPeakListView in apiPeakListView.stripPeakListViews:
      guiPeakListView = data2Obj[apiStripPeakListView]
      peakItem = guiPeakListView.peakItems.get(peak)
      if peakItem:
        peakItem.annotation.setupPeakAnnotation(peakItem)

Peak._refreshPeakAnnotation = _refreshPeakAnnotation

def _upDateAssignmentsPeakDimContrib(project:Project,
                                     apiPeakDimContrib:ApiAbstractPeakDimContrib):
  peak = project._data2Obj[apiPeakDimContrib.peakDim.peak]
  peak._refreshPeakAnnotation()
#
Project._setupNotifier(_upDateAssignmentsPeakDimContrib, ApiAbstractPeakDimContrib, 'postInit')
Project._setupNotifier(_upDateAssignmentsPeakDimContrib, ApiAbstractPeakDimContrib, 'preDelete')

def _upDateAssignmentsResonance(project:Project, apiResonance:ApiResonance):
  data2Obj = project._data2Obj
  peaks = set(x.peakDim.peak
              for x in apiResonance.peakDimContribs.union(apiResonance.peakDimContribNs))
  for peak in peaks:
    data2Obj[peak]._refreshPeakAnnotation()
#
Project._setupNotifier(_upDateAssignmentsResonance, ApiResonance, 'setImplName')
Project._setupNotifier(_upDateAssignmentsResonance, ApiResonance, 'setResonanceGroup')

def _upDateAssignmentsResonanceGroup(project:Project,
                                     apiResonanceGroup:ApiResonanceGroup):
  data2Obj = project._data2Obj
  peaks = set(y.peakDim.peak for x in apiResonanceGroup.resonances
                             for y in x.peakDimContribs.union(x.peakDimContribNs))
  for peak in peaks:
     data2Obj[peak]._refreshPeakAnnotation()
#
Project._setupNotifier(_upDateAssignmentsResonanceGroup, ApiResonanceGroup, 'setResonances')
# Project._setupNotifier(_upDateAssignmentsResonanceGroup, ApiResonanceGroup, 'setAssignedResidue')
Project._setupNotifier(_upDateAssignmentsResonanceGroup, ApiResonanceGroup, 'setSequenceCode')
Project._setupNotifier(_upDateAssignmentsResonanceGroup, ApiResonanceGroup, 'setResidueType')
Project._setupNotifier(_upDateAssignmentsResonanceGroup, ApiResonanceGroup, 'setDirectNmrChain')


def _upDateAssignmentsNmrChain(project:Project, apiNmrChain:ApiNmrChain):
  data2Obj = project._data2Obj
  peaks = set(z.peakDim.peak for x in apiNmrChain.resonanceGroups
                             for y in x.resonances
                             for z in (y.peakDimContribs.union(y.peakDimContribNs)))
  for peak in peaks:
     data2Obj[peak]._refreshPeakAnnotation()
#
Project._setupNotifier(_upDateAssignmentsNmrChain, ApiNmrChain, 'setCode')

# Notifiers for peak positin change.
# Needed for:
# PeakDim.position, PeakDim.dataDimRef (will not be used but does not cost anything to add
# PeakDim.numAliasing, DataDim.numPointsOrig
# DataDimRef.refPopint, refValue, valuePerPint
# Also changes in DimensinScaling, but that REALLY will nver be used in V3, so we skip it


def _refreshPeakPosition(peak:Peak):
  for peakListView in peak.peakList.peakListViews:
    peakItem = peakListView.peakItems.get(peak)
    if peakItem:
      peakItem.setPos(*peak.position)
Peak._refreshPeakPosition = _refreshPeakPosition

def _refreshPeakListPosition(peakList:PeakList):
  for peakListView in peakList.peakListViews:
    peakItems = peakListView.peakItems
    for peak in peakList.peaks:
      peakItem = peakItems.get(peak)
      if peakItem:
        peakItem.setPos(*peak.position)
PeakList._refreshPeakListPosition = _refreshPeakListPosition

def _updatePositionPeakDim(project:Project, apiPeakDim:ApiPeakDim):
  project._data2Obj[apiPeakDim.peak]._refreshPeakPosition()
Project._setupNotifier(_updatePositionPeakDim, ApiPeakDim, 'setPosition')
Project._setupNotifier(_updatePositionPeakDim, ApiPeakDim, 'setDataDimRef')
Project._setupNotifier(_updatePositionPeakDim, ApiPeakDim, 'setNumAliasing')

def _updatePositionDataDimRef(project:Project, apiDataDimRef:ApiDataDimRef):
  data2Obj = project._data2Obj
  for apiPeakList in apiDataDimRef.dataDim.dataSource.sortedPeakLists():
    data2Obj[apiPeakList]._refreshPeakListPosition()
Project._setupNotifier(_updatePositionDataDimRef, ApiDataDimRef, 'setValuePerPoint')
Project._setupNotifier(_updatePositionDataDimRef, ApiDataDimRef, 'setRefPoint')
Project._setupNotifier(_updatePositionDataDimRef, ApiDataDimRef, 'setRefValue')


def _updatePositionDataDim(project:Project, apiDataDim:ApiFreqDataDim):
  data2Obj = project._data2Obj
  for apiPeakList in apiDataDim.dataSource.sortedPeakLists():
    data2Obj[apiPeakList]._refreshPeakListPosition()
Project._setupNotifier(_updatePositionDataDim, ApiFreqDataDim, 'setNumPointsOrig')
