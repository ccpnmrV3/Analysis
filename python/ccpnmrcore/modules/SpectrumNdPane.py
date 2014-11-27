"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Geerten Vuister"
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
import operator

from PySide import QtCore, QtGui, QtOpenGL

from ccpnmrcore.modules.SpectrumPane import SpectrumPane, SPECTRUM_COLOURS
from ccpncore.gui.Action import Action
from ccpncore.gui.DoubleSpinbox import DoubleSpinbox
from ccpnmrcore.modules.spectrumPane.SpectrumNdItem import SpectrumNdItem
from ccpncore.gui.Menu import Menu
from ccpncore.gui.Icon import Icon
from ccpncore.gui.Label import Label
from ccpncore.lib.NmrExpPrototype import resetAllAxisCodes
from ccpncore.gui.LineEdit import LineEdit
from ccpn.lib import Spectrum as LibSpectrum
import numpy
import math
from functools import partial
import pyqtgraph as pg
from scipy import signal
from ccpncore.gui.Button import Button
from ccpncore.gui.Arrow import Arrow

class SpectrumNdPane(SpectrumPane):

  def __init__(self, *args, **kw):
    
    SpectrumPane.__init__(self, *args, **kw)

    self.plotItem.setAcceptDrops(True)
    
    self.setViewport(QtOpenGL.QGLWidget())
    self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
    self.crossHairShown = True
    self.fillToolBar()
    self.viewBox.menu = self.get2dContextMenu()
    self.viewBox.invertX()
    self.viewBox.invertY()
    # self.viewBox.keyPressEvent = self.keyPressEvent
    self.showGrid(x=True, y=True)
    self.gridShown = True
    self.region = None
    self.colourIndex = 0
    self.spectrumUtilToolbar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    self.traceMarkers = []
    self.traceScale = 1e6
    self.traces = []
    self.phaseButtonShown = False
    self.phasedData = None
    self.pivot = None
    self.planeLabel = None
    self.axesSwapped = False
    self.setShortcuts()


          
  ##### functions used externally #####

  # overrides superclass function
  def wheelEvent(self, event):
    if event.modifiers() & QtCore.Qt.ShiftModifier:
      for spectrumItem in self.spectrumItems:
        if event.delta() > 0:
            spectrumItem.raiseBaseLevel()
            spectrumItem.update()
        else:
          spectrumItem.lowerBaseLevel()
          spectrumItem.update()
    elif not event.modifiers():
      QtGui.QGraphicsView.wheelEvent(self, event)
      sc = 1.001 ** event.delta()
      #self.scale *= sc
      #self.updateMatrix()
      self.scale(sc, sc)
    elif event.modifiers() & QtCore.Qt.ControlModifier:
      if event.delta() > 0:
         self.increaseTraceScale()
      else:
        self.decreaseTraceScale()
    else:
      event.ignore

  def setShortcuts(self):
    self.removeTraces = QtGui.QShortcut(QtGui.QKeySequence("R, T"), self, self.clearTraceMarkers)
    self.phasingShortcut = QtGui.QShortcut(QtGui.QKeySequence('P, P'), self, self.addPivot)
    self.hTraceShortcut = QtGui.QShortcut(QtGui.QKeySequence("H, T"), self, self.addHTraceMarker)
    self.vTraceShortcut = QtGui.QShortcut(QtGui.QKeySequence("V, T"), self, self.addVTraceMarker)
    self.nextZPlaneShortcut = QtGui.QShortcut(QtGui.QKeySequence("Z, N"), self, self.nextZPlane)
    self.prevZPlaneShortcut = QtGui.QShortcut(QtGui.QKeySequence("Z, P"), self, self.prevZPlane)
    self.zoomFullShortcut = QtGui.QShortcut(QtGui.QKeySequence("Z, F"), self, self.zoomFull)
    self.flipXYShortcut = QtGui.QShortcut(QtGui.QKeySequence("X, Y"), self, self.swapXY)
    # self.flipXYShortcut.setShortcutContext(QtCore.Qt.WidgetShortcut)
    self.flipXZShortcut = QtGui.QShortcut(QtGui.QKeySequence("Y, Z"), self, self.rotateAboutX)
    self.flipXZShortcut = QtGui.QShortcut(QtGui.QKeySequence("X, Z"), self, self.rotateAboutY)

  def zoomFull(self):
    # self.zoomToRegion(self.region)
    self.setXRange(self.region[0][0],self.region[0][1])
    self.setYRange(self.region[1][0],self.region[1][1])
    print(self.region)

  def get2dContextMenu(self):

    self.contextMenu = Menu(self, isFloatWidget=True)
    # self.contextMenu.addAction(self.hTraceAction)
    # self.contextMenu.addAction(self.vTraceAction)
    self.crossHairAction = QtGui.QAction("Crosshair", self, triggered=self.toggleCrossHair,
                                         checkable=True)

    if self.crossHairShown == True:
      self.crossHairAction.setChecked(True)
    else:
      self.crossHairAction.setChecked(False)
    self.contextMenu.addAction(self.crossHairAction, isFloatWidget=True)
    self.contextMenu.addItem("Increase Trace Level", callback=self.increaseTraceScale)
    self.contextMenu.addItem("Decrease Trace Level", callback=self.decreaseTraceScale)

    return self.contextMenu

  def rotateAboutY(self):

    for spectrumItem in self.spectrumItems:
      spectrumItem.xDim = spectrumItem.dimMapping[2]
      spectrum = spectrumItem.spectrum
      dimensionCount = spectrum.dimensionCount
      pointCounts = spectrum.pointCounts
      zDims = set(range(spectrumItem.spectrum.dimensionCount)) - {spectrumItem.xDim, spectrumItem.yDim}
      zDim = zDims.pop()
      newDimMapping = {0:spectrumItem.xDim, 1:spectrumItem.yDim, 2:zDim}
      spectrumItem.dimMapping = newDimMapping
      self.xAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[0]])
      self.yAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[1]])
      self.xAxis.mappedDim = int(spectrumItem.dimMapping[0])
      self.yAxis.mappedDim = int(spectrumItem.dimMapping[1])
      pntRegion = dimensionCount * [None]
      for dim in range(dimensionCount):
        if dim in (spectrumItem.xDim, spectrumItem.yDim):
          region = (0, pointCounts[dim])
        else:
          n = pointCounts[dim] // 2
          region = (n, n+1)
        pntRegion[dim] = region
      ppmRegion = []
      for dim in range(dimensionCount):
        (firstPpm, lastPpm) = LibSpectrum.getDimValueFromPoint(spectrum, dim, pntRegion[dim])
        ppmRegion.append((firstPpm, lastPpm))

      self.region = ppmRegion
      spectrumItem.update()
      self.zoomX(ppmRegion[spectrumItem.xDim])
      self.zoomY(ppmRegion[spectrumItem.yDim])
      dataDimRef = spectrumItem.spectrum.ccpnSpectrum.sortedDataDims()[zDim].findFirstDataDimRef()
      self.planeLabel.setText('%0.3f' % (dataDimRef.pointToValue(self.current.spectrum.pointCounts[zDim]/2)))
      # self.planeLabel.textChanged.connect(self.changeZPlane)


  def rotateAboutX(self):

    for spectrumItem in self.spectrumItems:
      spectrumItem.yDim = spectrumItem.dimMapping[2]
      spectrum = spectrumItem.spectrum
      dimensionCount = spectrum.dimensionCount
      pointCounts = spectrum.pointCounts
      zDims = set(range(spectrumItem.spectrum.dimensionCount)) - {spectrumItem.xDim, spectrumItem.yDim}
      zDim = zDims.pop()
      newDimMapping = {0:spectrumItem.xDim, 1:spectrumItem.yDim, 2:zDim}
      spectrumItem.dimMapping = newDimMapping
      self.xAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[0]])
      self.yAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[1]])
      self.xAxis.mappedDim = int(spectrumItem.dimMapping[0])
      self.yAxis.mappedDim = int(spectrumItem.dimMapping[1])
      pntRegion = dimensionCount * [None]
      for dim in range(dimensionCount):
        if dim in (spectrumItem.xDim, spectrumItem.yDim):
          region = (0, pointCounts[dim])
        else:
          n = pointCounts[dim] // 2
          region = (n, n+1)
        pntRegion[dim] = region
      ppmRegion = []
      for dim in range(dimensionCount):
        (firstPpm, lastPpm) = LibSpectrum.getDimValueFromPoint(spectrum, dim, pntRegion[dim])
        ppmRegion.append((firstPpm, lastPpm))

      self.region = ppmRegion
      spectrumItem.update()
      self.zoomX(ppmRegion[spectrumItem.xDim])
      self.zoomY(ppmRegion[spectrumItem.yDim])
      # self.planeLabel.textChanged.disconnect(self.changeZPlane)
      dataDimRef = spectrumItem.spectrum.ccpnSpectrum.sortedDataDims()[zDim].findFirstDataDimRef()
      self.planeLabel.setText('%0.3f' % (dataDimRef.pointToValue(self.current.spectrum.pointCounts[zDim]/2)))
      # self.planeLabel.textChanged.connect(self.changeZPlane)


  def swapXY(self):

    for spectrumItem in self.spectrumItems:

      spectrumItem.xDim = spectrumItem.dimMapping[1]
      spectrumItem.yDim = spectrumItem.dimMapping[0]
      spectrum = spectrumItem.spectrum
      dimensionCount = spectrum.dimensionCount
      if dimensionCount > 2:
        zDims = set(range(spectrumItem.spectrum.dimensionCount)) - {spectrumItem.xDim, spectrumItem.yDim}
        zDim = zDims.pop()
        newDimMapping = {0:spectrumItem.xDim, 1:spectrumItem.yDim, 2:zDim}
      else:
        newDimMapping = {0:spectrumItem.xDim, 1:spectrumItem.yDim}
      spectrumItem.dimMapping = newDimMapping
      self.xAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[0]])
      self.yAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[1]])
      self.xAxis.mappedDim = int(spectrumItem.dimMapping[0])
      self.yAxis.mappedDim = int(spectrumItem.dimMapping[1])
      pointCounts = spectrum.pointCounts
      pntRegion = dimensionCount * [None]
      for dim in range(dimensionCount):
        if dim in (spectrumItem.xDim, spectrumItem.yDim):
          region = (0, pointCounts[dim])
          # print('region1',region)
        else:
          n = pointCounts[dim] // 2
          region = (n, n+1)
          # print('region2',region)
        pntRegion[dim] = region
      ppmRegion = []
      for dim in range(dimensionCount):
        (firstPpm, lastPpm) = LibSpectrum.getDimValueFromPoint(spectrum, dim, pntRegion[dim])
        ppmRegion.append((firstPpm, lastPpm))

      self.region = ppmRegion
      spectrumItem.update()
      self.zoomX(ppmRegion[spectrumItem.xDim])
      self.zoomY(ppmRegion[spectrumItem.yDim])
      if self.axesSwapped == False:
        self.axesSwapped = True
      else:
        self.axesSwapped = False

  def clearSpectra(self):
    
    SpectrumPane.clearSpectra(self)    
    self.region = None
    
  # implements superclass function
  def addSpectrum(self, spectrumVar, dimMapping=None):
    
    resetAllAxisCodes(self.project._wrappedData)
    spectrum = self.getObject(spectrumVar)
    # refExpDims = list(spectrum._wrappedData.experiment.refExperiment.getRefExpDims())
    # print(refExpDims)
    # for i in range(len(refExpDims)):
    #   print(i, refMap[refExpDims[i].sortedRefExpDimRefs()[0]])
    # #
    # # for refExpDim in refExpDims:
    # #   print((refExpDim.dim))
    # #   axisCode = refMap[refExpDim.sortedRefExpDimRefs()[0]]
    #   axisCodeMap[refExpDim.dim] = axisCode
    # print(axisCodeMap)
    if spectrum.dimensionCount < 1:
      # TBD: logger message
      return

    # TBD: check if dimensions make sense
    self.posColors = list(SPECTRUM_COLOURS.keys())[self.colourIndex]
    self.negColors = list(SPECTRUM_COLOURS.keys())[self.colourIndex+1]
    if len(self.spectrumItems) >= 1:
      spectrumItem = SpectrumNdItem(self, spectrum, self.spectrumItems[0].dimMapping, self.region, self.posColors, self.negColors)
    else:
      spectrumItem = SpectrumNdItem(self, spectrum, dimMapping, self.region, self.posColors, self.negColors)
    spectrumItem.axisCodeMap = {}
    # for dim in range(spectrum.dimensionCount):
      # dataDimRef = spectrum.ccpnSpectrum.sortedDataDims()[dim].findFirstDataDimRef()
      # spectrumItem.axisCodeMap[dim] = (refMap[dataDimRef.getExpDimRef().refExpDimRef])
    newItem = self.scene().addItem(spectrumItem)
    # self.xAxis.setAxisCode()
    self.xAxis.mappedDim = spectrumItem.dimMapping[0]
    self.yAxis.mappedDim = spectrumItem.dimMapping[1]
    self.xAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[0]])
    self.yAxis.setAxisCode(spectrum.axisCodes[spectrumItem.dimMapping[1]])


    self.mainWindow.pythonConsole.write("current.pane.addSpectrum(%s)\n" % (spectrum))
    spectrumItem.name = spectrum.name
    spectrum.spectrumItem = spectrumItem
    if self.colourIndex != len(SPECTRUM_COLOURS) - 2:
      self.colourIndex +=2
    else:
      self.colourIndex = 0

    if self.spectrumIndex < 10:
      shortcutKey = "s,"+str(self.spectrumIndex)
      self.spectrumIndex+=1
    else:
      shortcutKey = None

    pix=QtGui.QPixmap(60,10)
    # pix2=QtGui.QPixmap(30,10)
    # pix.scaled(60,20)
    # pix.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    pix.fill(QtGui.QColor(self.posColors))
    spectrumItem.newAction = self.spectrumToolbar.addAction(spectrumItem.name, QtGui.QToolButton)
    newIcon = QtGui.QIcon(pix)
    # newIcon.actualSize(QtCore.QSize(80,60))
    spectrumItem.newAction.setIcon(newIcon)
    spectrumItem.newAction.setCheckable(True)
    spectrumItem.newAction.setChecked(True)
    spectrumItem.newAction.setShortcut(QtGui.QKeySequence(shortcutKey))
    spectrumItem.newAction.toggled.connect(spectrumItem.setVisible)
    self.spectrumToolbar.addAction(spectrumItem.newAction)
    spectrumItem.widget = self.spectrumToolbar.widgetForAction(spectrumItem.newAction)
    spectrumItem.widget.clicked.connect(partial(self.clickedNd, spectrum))
    spectrumItem.widget.setFixedSize(60,30)
    self.current.spectrum = spectrum
    if spectrum.dimensionCount > 2 and self.planeLabel is None:
      self.planeToolbar = QtGui.QToolBar()
      tileButton = Button(self, 'T')
      tileButton.setFixedWidth(30)
      tileButton.setFixedHeight(30)
      self.planeToolbar.addWidget(tileButton)
      self.spinSystemLabel = Label(self)
      self.spinSystemLabel.setMaximumWidth(1150)
      self.spinSystemLabel.setScaledContents(True)
      self.spinSystemLabel.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
      # self.spinSystemLabel.setFixedWidth(900)
      self.planeToolbar.addWidget(self.spinSystemLabel)
      prevPlaneButton = Button(self,'<')
      prevPlaneButton.setFixedWidth(30)
      prevPlaneButton.setFixedHeight(30)
      prevPlaneButton.clicked.connect(self.prevZPlane)
      self.planeLabel = LineEdit(self)
      self.planeLabel.setAlignment(QtCore.Qt.AlignHCenter)
      zDims = set(range(spectrum.dimensionCount)) - {spectrumItem.xDim, spectrumItem.yDim}
      zDim = zDims.pop()
      dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[zDim].findFirstDataDimRef()
      self.current.spectrum.pointCounts[zDim]/2
      self.planeLabel.setText('%0.3f' % (dataDimRef.pointToValue(self.current.spectrum.pointCounts[zDim]/2)))
      self.planeLabel.setFixedWidth(100)
      self.planeLabel.setFixedHeight(30)
      # self.planeLabel.textChanged.connect(self.changeZPlane)
      nextPlaneButton = Button(self,'>')
      nextPlaneButton.setFixedWidth(30)
      nextPlaneButton.setFixedHeight(30)
      nextPlaneButton.clicked.connect(self.nextZPlane)
      self.planeToolbar.addWidget(prevPlaneButton)
      self.planeToolbar.addWidget(self.planeLabel)
      self.planeToolbar.addWidget(nextPlaneButton)
      self.planeToolbar.setContentsMargins(0,0,0,0)
      self.dock.addWidget(self.planeToolbar, 3, 0, 1, 11)

  # def changeZPosition(self, value):
  #   dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[2].findFirstDataDimRef()
  #   newPlaneNumber = dataDimRef.valueToPoint(float(value))
  #   if newPlaneNumber > self.current.spectrum.pointCounts[2]:
  #     pass
  #   else:
  #     region = [float(value), float(value)+self.current.spectrum.spectrumItem.zPlaneSize()]
  #
  #     self.changeZPlane(region=region)
  #     for spectrumItem in self.spectrumItems:
  #       spectrumItem.update()  # is this best way to force a re-draw??


  def decreaseTraceScale(self):
    self.traceScale*=1.41
    for trace in self.traces:
      self.removeItem(trace.spectrumItemTrace)
      self.plotTrace(trace.spectrumItemTrace.position, traceMarker=trace)

  def addPivot(self):
    if self.current.traceMarker.angle == 0:
      angle = -90
    elif self.current.traceMarker.angle == 90:
      angle = 0
    self.pivot = Arrow(pos=(self.mousePoint.toTuple()[0],self.mousePoint.toTuple()[1]), angle=angle, movable=True)
    self.addItem(self.pivot)


  def increaseTraceScale(self):
    self.traceScale/=1.41
    for trace in self.traces:
      self.removeItem(trace.spectrumItemTrace)
      self.plotTrace(trace.spectrumItemTrace.position, traceMarker=trace)

  #
  # def updateTrace(self, xData, yData):
  #   for trace in self.traces:
  #     self.removeItem(trace)
  #     trace.newSpectrumItemTrace = pg.PlotDataItem(xData,yData)
  #     self.addItem(trace.SpectrumItemTrace)
    
  def nextZPlane(self):

    self.changeZPlane(-1) # -1 because ppm units are backwards
    dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[2].findFirstDataDimRef()
    newPlaneNumber = dataDimRef.valueToPoint(float(self.planeLabel.text())) + 1
    newPoint = dataDimRef.pointToValue(newPlaneNumber)
    self.planeLabel.setText('%0.3f' % newPoint)
    
  def prevZPlane(self):

    self.changeZPlane(1)
    dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[2].findFirstDataDimRef()
    newPlaneNumber = dataDimRef.valueToPoint(float(self.planeLabel.text())) - 1
    newPoint = dataDimRef.pointToValue(newPlaneNumber)
    self.planeLabel.setText('%0.3f' % newPoint)

  def changeZPlane(self, planeCount=1):
    
    if len(self.region) < 3:
      return
      
    smallest = None
    # take smallest inter-plane distance
    for spectrumItem in self.spectrumItems:
      zPlaneSize = spectrumItem.zPlaneSize()
      if zPlaneSize is not None:
        if smallest is None or zPlaneSize < smallest:
          smallest = zPlaneSize

    if smallest is None:
      smallest = 1.0 # arbitrary
      
    zDim = spectrumItem.dimMapping[2]
    delta = smallest * planeCount
    zregion = list(self.region[zDim])
    for n in range(2):
      zregion[n] += delta
    self.region[zDim] = tuple(zregion)
    for spectrumItem in self.spectrumItems:
      spectrumItem.update()  # is this best way to force a re-draw??

  def upBy2(self):
    for spectrumItem in self.spectrumItems:
      spectrumItem.baseLevel*=1.4
      spectrumItem.levels = spectrumItem.getLevels()

  def downBy2(self):
    for spectrumItem in self.spectrumItems:
      spectrumItem.baseLevel/=1.4
      spectrumItem.levels = spectrumItem.getLevels()

  def addOne(self):
    self.current.spectrum.spectrumItem.numberOfLevels +=1
    self.current.spectrum.spectrumItem.levels = self.current.spectrum.spectrumItem.getLevels()


  def subtractOne(self):
    self.current.spectrum.spectrumItem.numberOfLevels -=1
    self.current.spectrum.spectrumItem.levels = self.current.spectrum.spectrumItem.getLevels()

  def addHTraceMarker(self):
    traceMarker = pg.InfiniteLine(angle=0, movable=True, pos=self.mousePoint)
    self.current.traceMarker = traceMarker
    self.addItem(traceMarker)
    traceMarker.axis = self.xAxis
    traceMarker.positionAxis = self.yAxis
    self.traceMarkers.append(traceMarker)
    trace = self.plotTrace(position=self.mousePoint.toTuple(), traceMarker=traceMarker)
    self.traces.append(trace)
    traceMarker.sigPositionChanged.connect(self.markerMoved)
    proxy = pg.SignalProxy(traceMarker.sigPositionChanged, slot=(self.markerMoved))
    # if self.phaseButtonShown == False:
    #   print('showingbutton')
    #   self.phasingAction = QtGui.QAction("phasing", self, checkable=True)
    #   self.phasingAction.toggled.connect(self.togglePhasingBar)
    #   self.phasingAction.setShortcut("P, C")
    #   self.spectrumUtilToolbar.addAction(self.phasingAction)
    #   self.phaseButtonShown = True

  def addVTraceMarker(self):
    traceMarker = pg.InfiniteLine(angle=90, movable=True, pos=self.mousePoint)
    self.current.traceMarker = traceMarker
    self.addItem(traceMarker)
    traceMarker.axis = self.yAxis
    traceMarker.positionAxis = self.xAxis
    self.traceMarkers.append(traceMarker)
    trace = self.plotTrace(position=self.mousePoint.toTuple(), traceMarker=traceMarker)
    self.traces.append(trace)
    traceMarker.sigPositionChanged.connect(self.markerMoved)
    proxy = pg.SignalProxy(traceMarker.sigPositionChanged, slot=(self.markerMoved))
    # if self.phaseButtonShown == False:
    #   self.phasingAction = QtGui.QAction("phasing", self, checkable=True)
    #   self.phasingAction.toggled.connect(self.togglePhasingBar)
    #   self.phasingAction.setShortcut("P, C")
    #   self.spectrumUtilToolbar.addAction(self.phasingAction)
    #   self.phaseButtonShown = True


  def markerMoved(self, traceMarker):
    self.removeItem(traceMarker.spectrumItemTrace)
    # if traceMarker.angle== 0:
    #   axis =
    positions = [traceMarker.getXPos(),traceMarker.getYPos()]
    # elif traceMarker.angle== 90:
    #   positions = [traceMarker.getXPos(),traceMarker.getYPos()]
    #   dim = 0
    # if self.phasedData is None:
    self.plotTrace(position=positions, traceMarker=traceMarker)
    # else:
    # self.phasing(0, traceMarker, position=positions)


  def phasing(self, value, movingTrace=None, position=None, axis=None):

    phaseList0 = list(self.current.spectrum.phases0)
    phaseList1 = list(self.current.spectrum.phases1)

    if movingTrace == None:

      for trace in self.traces:
        self.phasedData = []
        proportionality = 0
        if self.pivot is not None:
          pivotPosition = self.pivot.pos().toTuple()
        else:
          pivotPosition = (0, 0)
        transformedData = signal.hilbert(trace.data)
        dim = trace.spectrumItemTrace.dim
        phaseList0[dim] = self.zeroPhaseSlider.value()
        phaseList1[dim] = self.firstPhaseSlider.value()
        self.current.spectrum.phases0 = phaseList0
        self.current.spectrum.phases1 = phaseList1

        # if dim == 0:
        #   dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[1].findFirstDataDimRef()
        #   nptsOrig = self.current.spectrum.totalPointCounts[1]
        #   pivot = dataDimRef.valueToPoint(pivotPosition[1])
        #   proportionality = pivot/nptsOrig
        # if dim == 1:
        dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[axis.mappedDim].findFirstDataDimRef()
        nptsOrig = self.current.spectrum.totalPointCounts[axis.mappedDim]
        pivot = dataDimRef.valueToPoint(pivotPosition[axis.mappedDim])
        proportionality = pivot/nptsOrig
        phaseCorr = math.radians(float(self.current.spectrum.phases1[dim]))
        phase0 = math.radians(self.current.spectrum.phases0[dim])+((proportionality*phaseCorr)*-1)


        phaseAngles = [phase0 + ((ii/len(transformedData))*phaseCorr) for ii in range(len(transformedData))]

        for ii in range(len(phaseAngles)):
          self.phasedData.append(((transformedData[ii].real * math.cos(phaseAngles[ii])) + (transformedData[ii].imag * math.sin(phaseAngles[ii]))))
        self.current.spectrum.phase0 = math.degrees(phase0)
        # self.zeroPhaseSlider.setValue(self.current.spectrum.phase0)
        self.removeItem(trace.spectrumItemTrace)
        self.plotTrace(trace.spectrumItemTrace.dim,trace.spectrumItemTrace.position, traceMarker=trace, phasedData=self.phasedData)
    if movingTrace is not None:
      self.phasedData = []
      proportionality = 0
      if self.pivot is not None:
        pivotPosition = self.pivot.pos().toTuple()
      else:
        pivotPosition = (0, 0)
      transformedData = signal.hilbert(movingTrace.data)
      dim = movingTrace.spectrumItemTrace.dim
      phaseList0[dim] = self.zeroPhaseSlider.value()
      phaseList1[dim] = self.firstPhaseSlider.value()
      self.current.spectrum.phases0 = phaseList0
      self.current.spectrum.phases1 = phaseList1

      dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[axis.mappedDim].findFirstDataDimRef()
      nptsOrig = self.current.spectrum.totalPointCounts[axis.mappedDim]
      pivot = dataDimRef.valueToPoint(pivotPosition[axis.mappedDim])
      proportionality = pivot/nptsOrig
      phaseCorr = math.radians(float(self.current.spectrum.phases1[dim]))
      phase0 = math.radians(self.current.spectrum.phases0[dim])+((proportionality*phaseCorr)*-1)

      phaseAngles = [phase0 + ((ii/len(transformedData))*phaseCorr) for ii in range(len(transformedData))]

      for ii in range(len(phaseAngles)):
        self.phasedData.append(((transformedData[ii].real * math.cos(phaseAngles[ii])) + (transformedData[ii].imag * math.sin(phaseAngles[ii]))))
      self.current.spectrum.phase0 = math.degrees(phase0)
      # self.zeroPhaseSlider.setValue(self.current.spectrum.phase0)
      self.removeItem(movingTrace.spectrumItemTrace)
      # print(movingTrace.data)
      movingTrace.spectrumItemTrace.position = position
      self.plotTrace(movingTrace.spectrumItemTrace.dim,movingTrace.spectrumItemTrace.position, traceMarker=movingTrace, phasedData=self.phasedData)



  def plotTrace(self, position=None, traceMarker=None, phasedData=None):

    positions = []
    if position is None:
      position = [self.mousePoint.toTuple()[0],self.mousePoint.toTuple()[1]]

    else:
      position = list(position)
      if self.axesSwapped == True:
        position.reverse()
    if self.current.spectrum.dimensionCount > 2:
      zDims = set(range(self.current.spectrum.dimensionCount)) - {self.xAxis.mappedDim, self.yAxis.mappedDim}
      zDim = zDims.pop()
      position.append(int(self.region[zDim][0]))

    # for i in range(len(position)):
    #   positions.append(math.floor(LibSpectrum.getDimPointFromValue(self.current.spectrum, i, position[i])))
    # print(positions)
    dimensionCount = self.current.spectrum.dimensionCount
    ppmRegion = dimensionCount * [None]
    pointCounts = self.current.spectrum.pointCounts
    for dim in range(dimensionCount):
      # if dim in (self.current.spectrum.spectrumItem.xDim, self.current.spectrum.spectrumItem.yDim):
      region = (position[self.current.spectrum.spectrumItem.dimMapping[dim]])
      # else:
      #   n = position[dim]
      #   region = n
      ppmRegion[dim] = region
    pntRegion = []
    for dim in range(dimensionCount):
        pnt = LibSpectrum.getDimPointFromValue(self.current.spectrum, dim, ppmRegion[dim])
        pntRegion.append(math.floor(pnt))
    spectrum = self.current.spectrum
    dataDimRef = self.current.spectrum.ccpnSpectrum.sortedDataDims()[traceMarker.axis.mappedDim].findFirstDataDimRef()
    data = LibSpectrum.getSliceData(spectrum.ccpnSpectrum,position=pntRegion, sliceDim=traceMarker.axis.mappedDim)
    firstPoint = dataDimRef.pointToValue(0)
    pointCount = len(data)
    lastPoint = dataDimRef.pointToValue(pointCount)
    pointSpacing = (lastPoint-firstPoint)/pointCount
    positions2 = numpy.array([firstPoint + n*pointSpacing for n in range(pointCount)],dtype=numpy.float32)
    # positions2 = positions2[::-1]
    if phasedData is not None:
      data2 = (numpy.array(phasedData)/self.traceScale)*-1
    else:
      data2 = (data/self.traceScale)*-1
    if traceMarker.angle == 0:
      data3 = numpy.array([x+ppmRegion[traceMarker.positionAxis.mappedDim] for x in data2])
      traceMarker.spectrumItemTrace = pg.PlotDataItem(positions2, data3)
    else:
      # positions2 = positions2[::-1]
      data3 = numpy.array([x+ppmRegion[traceMarker.positionAxis.mappedDim] for x in data2])
      traceMarker.spectrumItemTrace = pg.PlotDataItem(data3,positions2)
    traceMarker.spectrumItemTrace.dim = traceMarker.axis.mappedDim
    traceMarker.data = data
    traceMarker.spectrumItemTrace.position = position
    self.addItem(traceMarker.spectrumItemTrace)


    return traceMarker

  def changeValue(self, label, value):

    floatValue = float(value)
    label.setText(str(floatValue))

  def changeSliderValue(self, slider, value):

    floatValue = float(value)
    slider.setValue(floatValue)


  def clearTraceMarkers(self):
    for item in self.traceMarkers:
      self.removeItem(item)
      self.removeItem(item.spectrumItemTrace)
    for item in self.traces:
      self.removeItem(item)
      self.removeItem(item)
    self.spectrumUtilToolbar.removeAction(self.phasingAction)
    self.phaseButtonShown = False
    self.traces = []

  def fillToolBar(self):
    plusOneAction = self.spectrumUtilToolbar.addAction("+1", self.addOne)
    plusOneIcon = Icon('icons/contourAdd')
    plusOneAction.setIcon(plusOneIcon)
    plusOneAction.setToolTip('Add One Level')
    minusOneAction = self.spectrumUtilToolbar.addAction("+1", self.subtractOne)
    minusOneIcon = Icon('icons/contourRemove')
    minusOneAction.setIcon(minusOneIcon)
    minusOneAction.setToolTip('Remove One Level ')
    upBy2Action = self.spectrumUtilToolbar.addAction("*1.4", self.upBy2)
    upBy2Icon = Icon('icons/contourBaseUp')
    upBy2Action.setIcon(upBy2Icon)
    upBy2Action.setToolTip('Raise Contour Base Level')
    downBy2Action = self.spectrumUtilToolbar.addAction("*1.4", self.downBy2)
    downBy2Icon = Icon('icons/contourBaseDown')
    downBy2Action.setIcon(downBy2Icon)
    downBy2Action.setToolTip('Lower Contour Base Level')
    storeZoomAction = self.spectrumUtilToolbar.addAction("Store Zoom", self.storeZoom)
    storeZoomIcon = Icon('icons/zoom-store')
    storeZoomAction.setIcon(storeZoomIcon)
    storeZoomAction.setToolTip('Store Zoom')
    restoreZoomAction = self.spectrumUtilToolbar.addAction("Restore Zoom", self.restoreZoom)
    restoreZoomIcon = Icon('icons/zoom-restore')
    restoreZoomAction.setIcon(restoreZoomIcon)
    restoreZoomAction.setToolTip('Restore Zoom')

  def togglePhasingBar(self):
    if self.phasingAction.isChecked() == True:
      self.raisePhasingToolBar()
    if self.phasingAction.isChecked() == False:
      self.phasingToolBar.hide()

  def raisePhasingToolBar(self):
    self.phasingToolBar = QtGui.QToolBar()
    self.zeroPhaseSlider  = QtGui.QSlider(self)
    self.zeroPhaseSlider.setOrientation(QtCore.Qt.Horizontal)
    self.zeroPhaseSlider.setRange(-180.0, 180.0)
    self.zeroPhaseSlider.setValue(0)
    self.zeroPhaseSlider.setFixedWidth(350)
    self.zeroPhaseSlider.setTickInterval(0.1)
    zeroPhaseLabel = QtGui.QLineEdit(self)
    zeroPhaseLabel.setFixedWidth(50)
    zeroLabel = Label(self,text="P0")
    zeroLabel.setFixedWidth(30)
    self.phasingToolBar.addWidget(zeroLabel)
    self.phasingToolBar.addWidget(self.zeroPhaseSlider)
    zeroPhaseLabel.setText(str(self.zeroPhaseSlider.value()))
    self.zeroPhaseSlider.valueChanged.connect(partial(self.changeValue,zeroPhaseLabel))
    self.zeroPhaseSlider.valueChanged.connect(self.phasing)
    zeroPhaseLabel.textChanged.connect(partial(self.changeSliderValue,self.zeroPhaseSlider))
    # zeroPhaseLabel.textChanged.connect(self.phasingZeroOrder)
    self.phasingToolBar.addWidget(zeroPhaseLabel)
    self.firstPhaseSlider  = QtGui.QSlider(self)
    self.firstPhaseSlider.setFixedWidth(350)
    self.firstPhaseSlider.setOrientation(QtCore.Qt.Horizontal)
    self.firstPhaseSlider.setRange(-360.0, 360.0)
    self.firstPhaseSlider.setValue(0)
    self.firstPhaseSlider.setTickInterval(0.1)
    firstLabel = Label(self,text="P1")
    firstLabel.setFixedWidth(30)
    firstPhaseLabel = QtGui.QLineEdit(self)
    firstPhaseLabel.setFixedWidth(50)
    firstPhaseLabel.setText(str(self.firstPhaseSlider.value()))
    self.firstPhaseSlider.valueChanged.connect(partial(self.changeValue,firstPhaseLabel))
    firstPhaseLabel.textChanged.connect(partial(self.changeSliderValue,self.firstPhaseSlider))
    self.firstPhaseSlider.valueChanged.connect(self.phasing)
    # self.firstPhaseLabel.textChanged.connect(self.phasingFirstOrder)
    # self.pivotButton = Button(self, text='pivot', callback=self.addPivot)
    self.phasingToolBar.addWidget(firstLabel)
    self.phasingToolBar.addWidget(self.firstPhaseSlider)
    self.phasingToolBar.addWidget(firstPhaseLabel)
    # self.phasingToolBar.addWidget(self.pivotButton)
    self.dock.addWidget(self.phasingToolBar, 3, 0, 1, 11)




