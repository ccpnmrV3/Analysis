"""
This widget implements the nD (n>2) strip. 
Strips are contained within a SpectrumDisplay.

Some of the available methods:

changeZPlane(n:int=0, planeCount:int=None, position:float=None): Changes the position 
    of the z axis of the strip by number of planes or a ppm position, depending
    on which is specified.
nextZPlane(n:int=0): Decreases z ppm position by one plane
prevZPlane(n:int=0): Decreases z ppm position by one plane

resetZoom(axis=None): Resets zoom of strip axes to limits of maxima and minima of 
    the limits of the displayed spectra.
    
toggleHorizontalTrace(self): Toggles display of the horizontal trace.
toggleVerticalTrace(self): Toggles display of the vertical trace.

setStripLabelText(text:str):  set the text of the stripLabel
getStripLabelText() -> str:  get the text of the stripLabel
showStripLabel(doShow:bool):  show/hide the stripLabel
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
__dateModified__ = "$dateModified: 2017-07-07 16:32:45 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Geerten Vuister $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtGui, QtCore

# import math
import numpy
from functools import partial
# import pyqtgraph as pg

# from ccpn.core.Project import Project
from ccpn.core.PeakList import PeakList
# from ccpn.core.Peak import Peak

# from ccpn.ui.gui.widgets.Button import Button
# from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.ui.gui.widgets.Icon import Icon
from ccpn.ui.gui.widgets.Menu import Menu
from ccpn.ui.gui.widgets.PlaneToolbar import PlaneToolbar #, PlaneSelectorWidget
# from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.util.Logging import getLogger
import typing

from ccpn.ui.gui.modules.GuiStrip import GuiStrip

# from ccpn.ui.gui.modules.spectrumItems.GuiPeakListView import GuiPeakListView


class GuiStripNd(GuiStrip):
  """
  Main Strip for Nd spectra object

  This module inherits the following attributes from the Strip wrapper class:

  serial          serial number of Strip, used in Pid and to identify the Strip
                    :return <str>
  axisCodes         Fixed string Axis codes in original display order
                      :return <tuple>:(X, Y, Z1, Z2, ...)
  axisOrder         String Axis codes in display order, determine axis display order
                      axisOrder = <sequence>:(X, Y, Z1, Z2, ...)
                      :return <tuple>:(X, Y, Z1, Z2, ...)
  positions         Axis centre positions, in display order
                      positions = <Tuple>
                      :return <Tuple>:(<float>, ...)
  widths            Axis display widths, in display order
                      widths = <Tuple>
                      :return <Tuple>:(<float>, ...)
  units             Axis units, in display order
                      :return <Tuple>
  spectra           List of the spectra attached to the strip
                    (whether display is currently turned on or not)
                      :return <Tuple>:(<Spectrum>, ...)

  delete            Delete a strip
  clone             Create new strip that duplicates this one, appending it at the end
  moveTo            Move strip to index newIndex in orderedStrips
                      moveTo(newIndex:int)
                        :param newIndex:<int> new index position
  resetAxisOrder    Reset display to original axis order
  findAxis          Find axis
                      findAxis(axisCode)
                        :param axisCode:
                        :return axis
  displaySpectrum   Display additional spectrum on strip, with spectrum axes ordered according to axisOrder
                      displaySpectrum(spectrum:Spectrum, axisOrder:Sequence=()
                        :param spectrum:<Spectrum> additional spectrum to display
                        :param axisOrder:<Sequence>=() new axis ordering
  peakIsInPlane     Return whether the peak is in currently displayed planes for strip
                      peakIsInPlane(peak:Peak)
                        :param peak:<Peak> peak of interest
                        :return <bool>
  peakIsInFlankingPlane   Return whether the peak is in planes flanking currently displayed planes for strip
                            peakIsInFlankingPlane(peak:Peak)
                              :param peak:<Peak> peak of interest
                              :return <bool>
  peakPickPosition  Pick peak at position for all spectra currently displayed in strip
                      peakPickPosition(position:List[float])
                        :param position:<List> coordinates to test
                        :return <Tuple>:(<Peak>, ...)
  peakPickRegion    Peak pick all spectra currently displayed in strip in selectedRegion
                      selectedRegion:List[List[float])
                        :param selectedRegion:<List>  of <List> of coordinates to test
                        :return <Tuple>:(<Peak>, ...)
  """
  # TODO:ED: complete the above; also port to GuiStrip1d

  def __init__(self, spectrumDisplay):
    """
    Initialise Nd spectra object

    :param spectrumDisplay: spectrumDisplay instance
    """
    #print('GuiStripNd>>', self.spectrumDisplay)
    GuiStrip.__init__(self, spectrumDisplay, useOpenGL=True)

    # the scene knows which items are in it but they are stored as a list and the below give fast access from API object to QGraphicsItem
    ###self.peakLayerDict = {}  # peakList --> peakLayer
    ###self.peakListViewDict = {}  # peakList --> peakListView
    self.spectrumActionDict = {}  # apiDataSource --> toolbar action (i.e. button); used in SpectrumToolBar

    self.haveSetupZWidgets = False
    self.viewBox.menu = self._get2dContextMenu()
    self.viewBox.invertX()
    self.viewBox.invertY()
    ###self.region = guiSpectrumDisplay.defaultRegion()
    self.planeLabel = None
    self.axesSwapped = False

    self.planeToolbar = None
    # TODO: this should be refactored; together with the 'Z-plane' mess: should general, to be used for other dimensions
    # Adds the plane toolbar to the strip.
    callbacks = [self.prevZPlane, self.nextZPlane, self._setZPlanePosition, self._changePlaneCount]
    self.planeToolbar = PlaneToolbar(self._stripToolBarWidget, strip=self, callbacks=callbacks,
                                     grid=(0,0), hPolicy='minimum', hAlign='center', vAlign='center')
    #self._stripToolBarWidget.addWidget(self.planeToolbar)
    #self.planeToolBar.hide()
    # test
    #PlaneSelectorWidget(qtParent=self._stripToolBarWidget, strip=self, axis=2, grid=(0,1))

    if len(self.orderedAxes) < 3:         # hide if only 2D
      self._stripToolBarWidget.setFixedHeight(0)

    #self.mouseDragEvent = self._mouseDragEvent
    self.updateRegion = self._updateRegion

    self.plotWidget.scene().sigMouseMoved.connect(self._mouseMoved)


  def _get2dContextMenu(self) -> Menu:
    """
    Creates and returns the Nd context menu
    """
    class tType:
      menu, item, actn = range(1,4)

    self._spectrumUtilActions = {}
    self.contextMenu = Menu('', self, isFloatWidget=True)     # generate new menu

    toolBarItems = [
       # type,      action name             icon                      tooltip/name                active  checked,    callback,                             method
      (tType.item, 'ToolBar',               'toolbarAction',          '',                         True,   True,       self.spectrumDisplay.toggleToolbar,   'toolbarAction'),
      (tType.item, 'Crosshair',             'crossHairAction',        '',                         True,   True,       self._toggleCrossHair,                'crossHairAction'),
      (tType.item, 'H Trace',               'hTraceAction',           '',                         True,   False,      self._updateTraces,                   'hTraceAction'),
      (tType.item, 'V Trace',               'vTraceAction',           '',                         True,   False,      self._updateTraces,                   'vTraceAction'),
      (tType.item, 'Grid',                  'gridAction',             '',                         True,   True,       self.toggleGrid,                      'gridAction'),

      (tType.actn, 'Add Contour Level',     'icons/contour-add',      'Add One Level',            True,   True,       self.spectrumDisplay.addContourLevel, ''),
      (tType.actn, 'Remove Contour Level',  'icons/contour-remove',   'Remove One Level',         True,   True,       self.spectrumDisplay.removeContourLevel,''),
      (tType.actn, 'Raise Base Level',      'icons/contour-base-up',  'Raise Contour Base Level', True,   True,       self.spectrumDisplay.raiseContourBase,''),
      (tType.actn, 'Lower Base Level',      'icons/contour-base-down','Lower Contour Base Level', True,   True,       self.spectrumDisplay.lowerContourBase,''),
      (tType.actn, 'Store Zoom',            'icons/zoom-store',       'Store Zoom',               True,   True,       self.spectrumDisplay._storeZoom,      ''),
      (tType.actn, 'Restore Zoom',          'icons/zoom-restore',     'Restore Zoom',             True,   True,       self.spectrumDisplay._restoreZoom,    ''),
      (tType.actn, 'Reset Zoom',            'icons/zoom-full',        'Reset Zoom',               True,   True,       self.resetZoom,                       ''),
      (tType.actn, 'Print to File...',      'icons/print',            'Print Spectrum Display to File', True, True, lambda:self.spectrumDisplay.window.printToFile(self.spectrumDisplay), ''),

      (tType.menu, 'Navigate To',           '',                       '',                         True,   True,       None,                                 'navigateToMenu')
    ]

    for aType, aName, icon, tooltip, active, checked, callback, attrib in toolBarItems:     # build the menu items/actions
      # self.contextMenu.navigateToMenu = self.contextMenu.addMenu('Navigate To')
      def tempMethod():           # ejb - how does this work?????
        return
      if aType == tType.menu:
        action = self.contextMenu.addMenu(aName)
        tempMethod.__doc__=''
        tempMethod.__name__=attrib
        setattr(self.contextMenu, tempMethod.__name__, action)      # add to the menu

      elif aType == tType.item:
        # self.gridAction = self.contextMenu.addItem("Grid", callback=self.toggleGrid, checkable=True)
        action = self.contextMenu.addItem(aName, callback=callback, checkable=active, checked=checked)
        tempMethod.__doc__=''
        tempMethod.__name__=attrib
        setattr(self, tempMethod.__name__, action)
        # add to self

      elif aType == tType.actn:
        # printAction = self.contextMenu.addAction("Print to File...", lambda: self.spectrumDisplay.window.printToFile(self.spectrumDisplay))
        action = self.contextMenu.addAction(aName, callback)
        if icon is not None:
          ic = Icon(icon)
          action.setIcon(ic)
        self._spectrumUtilActions[aName] = action

    # self.navigateToMenu = self.contextMenu.addMenu('Navigate To')
    # self.spectrumDisplays = self.getSpectrumDisplays()
    # for spectrumDisplay in self.spectrumDisplays:
    #   spectrumDisplayAction = self.navigateToMenu.addAction(spectrumDisplay.pid)
    #   receiver = lambda spectrumDisplay=spectrumDisplay.pid: self.navigateTo(spectrumDisplay)
    #   self.connect(spectrumDisplayAction, QtCore.SIGNAL('triggered()'), receiver)
    #   self.navigateToMenu.addAction(spectrumDisplay)

    self.crossHairAction.setChecked(self.crossHairIsVisible)
    self.gridAction.setChecked(self.gridIsVisible)

    return self.contextMenu

  def flipXYAxis(self):
    """
    Flip the X and Y axes
    """
    nDim = len(self.axisOrder)
    if nDim < 2:
      getLogger().warning('Too few dimensions for XY flip')
    else:
      axisOrder = [self.axisOrder[1], self.axisOrder[0]]
      if nDim > len(axisOrder):
        axisOrder.extend(self.axisOrder[2:])

      # create a new spectrum display with the new axis order
      newDisplay = self.mainWindow.createSpectrumDisplay(self.spectra[0], axisOrder=axisOrder)
      for spectrum in self.spectra:
        newDisplay.displaySpectrum(spectrum)

  def flipXZAxis(self):
    """
    Flip the X and Z axes
    """
    nDim = len(self.axisOrder)
    if nDim < 3:
      getLogger().warning('Too few dimensions for XZ flip')
    else:
      axisOrder = [self.axisOrder[2], self.axisOrder[1], self.axisOrder[0]]

      # add any remaining axes of the strip to the list
      if nDim > len(axisOrder):
        axisOrder.extend(self.axisOrder[3:])

      # create a new spectrum display with the new axis order
      newDisplay = self.mainWindow.createSpectrumDisplay(self.spectra[0], axisOrder=axisOrder)
      for spectrum in self.spectra:         #[1:]:
        newDisplay.displaySpectrum(spectrum)

  def flipYZAxis(self):
    """
    Flip the Y and Z axes
    """
    nDim = len(self.axisOrder)
    if nDim < 3:
      getLogger().warning('Too few dimensions for YZ flip')
    else:
      axisOrder = [self.axisOrder[0], self.axisOrder[2], self.axisOrder[1]]

      # add any remaining axes of the strip to the list
      if nDim > len(axisOrder):
        axisOrder.extend(self.axisOrder[3:])

      # create a new spectrum display with the new axis order
      newDisplay = self.mainWindow.createSpectrumDisplay(self.spectra[0], axisOrder=axisOrder)
      for spectrum in self.spectra:
        newDisplay.displaySpectrum(spectrum)

  def reorderSpectra(self):
    pass

  def resetZoom(self, axis=None):
    """
    Resets zoom of strip axes to limits of maxima and minima of the limits of the displayed spectra.
    """
    x = []
    y = []
    for spectrumView in self.spectrumViews:

      # Get spectrum dimension index matching display X and Y
      # without using axis codes, as they may not match
      spectrumIndices = spectrumView._displayOrderSpectrumDimensionIndices
      spectrumLimits = spectrumView.spectrum.spectrumLimits
      x.append(spectrumLimits[spectrumIndices[0]])
      y.append(spectrumLimits[spectrumIndices[1]])
      # xIndex = spectrumView.spectrum.axisCodes.index(self.axisCodes[0])
      # yIndex = spectrumView.spectrum.axisCodes.index(self.axisCodes[1])
      # x.append(spectrumView.spectrum.spectrumLimits[xIndex])
      # y.append(spectrumView.spectrum.spectrumLimits[yIndex])

    xArray = numpy.array(x).flatten()
    yArray = numpy.array(y).flatten()

    zoomXArray = ([min(xArray), max(xArray)])
    zoomYArray = ([min(yArray), max(yArray)])
    self.zoomToRegion(zoomXArray, zoomYArray)
    self.pythonConsole.writeConsoleCommand("strip.resetZoom()", strip=self)
    getLogger().info("strip = application.getByGid('%s')\nstrip.resetZoom()" % self.pid)
    return zoomXArray, zoomYArray

  def resetAxisRange(self, axis):
    if not axis:
      return

    positionArray = []

    for spectrumView in self.spectrumViews:

      # Get spectrum dimension index matching display X or Y
      # without using axis codes, as they may not match
      spectrumIndices = spectrumView._displayOrderSpectrumDimensionIndices
      spectrumLimits = spectrumView.spectrum.spectrumLimits
      positionArray.append(spectrumLimits[spectrumIndices[axis]])

    positionArrayFlat = numpy.array(positionArray).flatten()
    zoomArray = ([min(positionArrayFlat), max(positionArrayFlat)])
    if axis == 0:
      self.zoomX(*zoomArray)
    elif axis == 1:
      self.zoomY(*zoomArray)


  def _updateRegion(self, viewBox):
    # this is called when the viewBox is changed on the screen via the mouse

    GuiStrip._updateRegion(self, viewBox)
    self._updateTraces()

  def _updateTraces(self):

    cursorPosition = self.current.cursorPosition
    if cursorPosition:
      position = list(cursorPosition)
      for axis in self.orderedAxes[2:]:
        position.append(axis.position)
      point = QtCore.QPointF(cursorPosition[0], cursorPosition[1])
      pixel = self.viewBox.mapViewToScene(point)
      cursorPixel = (pixel.x(), pixel.y())
      updateHTrace = self.hTraceAction.isChecked()
      updateVTrace = self.vTraceAction.isChecked()
      for spectrumView in self.spectrumViews:
        spectrumView._updateTrace(position, cursorPixel, updateHTrace, updateVTrace)

  def toggleHorizontalTrace(self):
    """
    Toggles whether or not horizontal trace is displayed.
    """
    self.hTraceAction.setChecked(not self.hTraceAction.isChecked())
    self._updateTraces()

  def toggleVerticalTrace(self):
    """
    Toggles whether or not vertical trace is displayed.
    """
    self.vTraceAction.setChecked(not self.vTraceAction.isChecked())
    self._updateTraces()

  def _mouseMoved(self, positionPixel):

    if self.isDeleted:
      return

    #GuiStrip._mouseMoved(self, positionPixel)
    self._updateTraces()

  def _setZWidgets(self):
    """
    # CCPN INTERNAL - called in _changedBoundDisplayAxisOrdering function of GuiStripDisplayNd.py
    Sets values for the widgets in the plane toolbar.
    """

    for n, zAxis in enumerate(self.orderedAxes[2:]):
      minZPlaneSize = None
      minAliasedFrequency = maxAliasedFrequency = None
      for spectrumView in self.spectrumViews:
        # spectrum = spectrumView.spectrum
        # zDim = spectrum.axisCodes.index(zAxis.code)

        # position, width, totalPointCount, minFrequency, maxFrequency, dataDim = (
        #   spectrumView._getSpectrumViewParams(n+2))
        viewParams = spectrumView._getSpectrumViewParams(n+2)

        minFrequency = viewParams.minAliasedFrequency
        if minFrequency is not None:
         if minAliasedFrequency is None or minFrequency < minAliasedFrequency:
           minAliasedFrequency = minFrequency

        maxFrequency = viewParams.maxAliasedFrequency
        if maxFrequency is not None:
          if maxAliasedFrequency is None or maxFrequency < maxAliasedFrequency:
            maxAliasedFrequency = maxFrequency

        width = viewParams.valuePerPoint
        if minZPlaneSize is None or width < minZPlaneSize:
          minZPlaneSize = width

      if minZPlaneSize is None:
        minZPlaneSize = 1.0 # arbitrary
      else:
        # Necessary, otherwise it does not know what width it should have
        zAxis.width = minZPlaneSize

      planeLabel = self.planeToolbar.planeLabels[n]

      planeLabel.setSingleStep(minZPlaneSize)

      # have to do the following in order: maximum, value, minimum
      # otherwise Qt will set bogus value to guarantee that minimum <= value <= maximum

      if maxAliasedFrequency is not None:
        planeLabel.setMaximum(maxAliasedFrequency)

      planeLabel.setValue(zAxis.position)

      if minAliasedFrequency is not None:
        planeLabel.setMinimum(minAliasedFrequency)

      if not self.haveSetupZWidgets:
        # have to set this up here, otherwise the callback is called too soon and messes up the position
        planeLabel.editingFinished.connect(partial(self._setZPlanePosition, n, planeLabel.value()))

    self.haveSetupZWidgets = True

  def changeZPlane(self, n:int=0, planeCount:int=None, position:float=None):
    """
    Changes the position of the z axis of the strip by number of planes or a ppm position, depending
    on which is specified.
    """

    zAxis = self.orderedAxes[n+2]
    planeLabel = self.planeToolbar.planeLabels[n]
    planeSize = planeLabel.singleStep()

    # below is hack to prevent initial setting of value to 99.99 when dragging spectrum onto blank display
    if planeLabel.minimum() == 0 and planeLabel.value() == 99.99 and planeLabel.maximum() == 99.99:
      return

    if planeCount:
      delta = planeSize * planeCount
      position = zAxis.position + delta
      if planeLabel.minimum() <= position <= planeLabel.maximum():
        zAxis.position = position
      #planeLabel.setValue(zAxis.position)
    elif position is not None: # should always be the case
      if planeLabel.minimum() <= position <= planeLabel.maximum():
        zAxis.position = position
        self.pythonConsole.writeConsoleCommand("strip.changeZPlane(position=%f)" % position, strip=self)
        getLogger().info("strip = application.getByGid('%s')\nstrip.changeZPlane(position=%f)" % (self.pid, position))
        #planeLabel.setValue(zAxis.position)

      # else:
      #   print('position is outside spectrum bounds')

  def _changePlaneCount(self, n:int=0, value:int=1):
    """
    Changes the number of planes displayed simultaneously.
    """
    zAxis = self.orderedAxes[n+2]
    planeLabel = self.planeToolbar.planeLabels[n]
    zAxis.width = value * planeLabel.singleStep()

  def nextZPlane(self, n:int=0):
    """
    Increases z ppm position by one plane
    """
    self.changeZPlane(n, planeCount=-1) # -1 because ppm units are backwards
    self.pythonConsole.writeConsoleCommand("strip.nextZPlane()", strip=self)
    getLogger().info("application.getByGid(%r).nextZPlane()" % self.pid)

  def prevZPlane(self, n:int=0):
    """
    Decreases z ppm position by one plane
    """
    self.changeZPlane(n, planeCount=1) # -1 because ppm units are backwards
    self.pythonConsole.writeConsoleCommand("strip.prevZPlane()", strip=self)
    getLogger().info("application.getByGid(%r).prevZPlane()" % self.pid)

  def _setZPlanePosition(self, n:int, value:float):
    """
    Sets the value of the z plane position box if the specified value is within the displayable limits.
    """
    planeLabel = self.planeToolbar.planeLabels[n]
    if 1: # planeLabel.valueChanged: (<-- isn't that always true??)
      value = planeLabel.value()
    # 8/3/2016 Rasmus Fogh. Fixed untested (obvious bug)
    # if planeLabel.minimum() <= planeLabel.value() <= planeLabel.maximum():

    if planeLabel.minimum() <= value <= planeLabel.maximum():
      self.changeZPlane(n, position=value)

  # def setPlaneCount(self, n:int=0, value:int=1):
  #   """
  #   Sets the number of planes to be displayed simultaneously.
  #   """
  #   planeCount = self.planeToolbar.planeCounts[n]
  #   self.changePlaneCount(value=(value/planeCount.oldValue))
  #   planeCount.oldValue = value

  def _findPeakListView(self, peakList:PeakList):
    
    #peakListView = self.peakListViewDict.get(peakList)
    #if peakListView:
    #  return peakListView
      
    for spectrumView in self.spectrumViews:
      for peakListView in spectrumView.peakListViews:
        if peakList is peakListView.peakList:
          #self.peakListViewDict[peakList] = peakListView
          return peakListView
            
    return None
