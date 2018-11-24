"""
By Functionality:

Zoom and pan:
    Left-drag:                          pans the spectrum.

    shift-left-drag:                    draws a zooming box and zooms the viewbox.
    shift-middle-drag:                  draws a zooming box and zooms the viewbox.
    shift-right-drag:                   draws a zooming box and zooms the viewbox.
    Two successive shift-right-clicks:  define zoombox
    control-right click:                reset the zoom

Peaks:
    Left-click:                         select peak near cursor in a spectrum display, deselecting others
    Control(Cmd)-left-click:            (de)select peak near cursor in a spectrum display, adding/removing to selection.
    Control(Cmd)-left-drag:             selects peaks in an area specified by the dragged region.
    Middle-drag:                        Moves a selected peak.
    Control(Cmd)-Shift-Left-click:      picks a peak at the cursor position, adding to selection
    Control(Cmd)-shift-left-drag:       picks peaks in an area specified by the dragged region.

Others:
    Right-click:                        raises the context menu.


By Mouse button:

    Left-click:                         select peak near cursor in a spectrum display, deselecting others
    Control(Cmd)-left-click:            (de)select peak near cursor in a spectrum display, adding/removing to selection.
    Control(Cmd)-Shift-Left-click:      picks a peak at the cursor position, adding to selection

    Left-drag:                          pans the spectrum.
    shift-left-drag:                    draws a zooming box and zooms the viewbox.
    Control(Cmd)-left-drag:             selects peaks in an area specified by the dragged region.
    Control(Cmd)-shift-left-drag:       picks peaks in an area specified by the dragged region.


    shift-middle-drag:                  draws a zooming box and zooms the viewbox.

    Right-click:                        raises the context menu.
    control-right click:                reset the zoom
    Two successive shift-right-clicks:  define zoombox

    shift-right-drag:                   draws a zooming box and zooms the viewbox.
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
# Last code modification:
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified$"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created:
#=========================================================================================
__author__ = "$Author: Ed Brooksbank $"
__date__ = "$Date$"
#=========================================================================================
# Start of code
#=========================================================================================

import sys
import math
import time
# from threading import Thread
# from queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QSize, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from ccpn.util.Logging import getLogger
import numpy as np
from pyqtgraph import functions as fn
from ccpn.core.PeakList import PeakList
# from ccpn.core.IntegralList import IntegralList
from ccpn.ui.gui.lib.mouseEvents import getCurrentMouseMode
from ccpn.ui.gui.lib.GuiStrip import DefaultMenu, PeakMenu, IntegralMenu, \
    MultipletMenu, PhasingMenu

from ccpn.core.lib.Cache import cached

# from ccpn.util.Colour import getAutoColourRgbRatio
from ccpn.ui.gui.guiSettings import CCPNGLWIDGET_BACKGROUND, CCPNGLWIDGET_FOREGROUND, CCPNGLWIDGET_PICKCOLOUR, \
    CCPNGLWIDGET_GRID, CCPNGLWIDGET_HIGHLIGHT, CCPNGLWIDGET_INTEGRALSHADE, \
    CCPNGLWIDGET_LABELLING, CCPNGLWIDGET_PHASETRACE, getColours, \
    CCPNGLWIDGET_HEXBACKGROUND, CCPNGLWIDGET_ZOOMAREA, CCPNGLWIDGET_PICKAREA, \
    CCPNGLWIDGET_SELECTAREA, CCPNGLWIDGET_ZOOMLINE, CCPNGLWIDGET_MOUSEMOVELINE, \
    CCPNGLWIDGET_HARDSHADE
# from ccpn.ui.gui.lib.GuiPeakListView import _getScreenPeakAnnotation, _getPeakAnnotation  # temp until I rewrite
import ccpn.util.Phasing as Phasing
from ccpn.ui.gui.lib.mouseEvents import \
    leftMouse, shiftLeftMouse, controlLeftMouse, controlShiftLeftMouse, controlShiftRightMouse, \
    middleMouse, shiftMiddleMouse, rightMouse, shiftRightMouse, controlRightMouse, PICK
# from ccpn.core.lib.Notifiers import Notifier
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLNotifier import GLNotifier
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLGlobal import GLGlobalData
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLFonts import GLString
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLArrays import GLRENDERMODE_IGNORE, GLRENDERMODE_DRAW, \
    GLRENDERMODE_RESCALE, GLRENDERMODE_REBUILD, \
    GLREFRESHMODE_NEVER, GLREFRESHMODE_ALWAYS, \
    GLREFRESHMODE_REBUILD, GLVertexArray, \
    GLSymbolArray, GLLabelArray
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLViewports import GLViewports
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLWidgets import GLIntegralRegion, GLExternalRegion, \
    GLRegion, REGION_COLOURS, GLInfiniteLine
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLLabelling import GLpeakNdLabelling, GLpeak1dLabelling, \
    GLintegral1dLabelling, GLintegralNdLabelling, \
    GLmultiplet1dLabelling, GLmultipletNdLabelling
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGLExport import GLExporter
import ccpn.ui.gui.lib.OpenGL.CcpnOpenGLDefs as GLDefs
# from ccpn.util.Common import makeIterableList
from typing import Tuple
from ccpn.util.Constants import AXIS_FULLATOMNAME, AXIS_MATCHATOMTYPE
from ccpn.ui.gui.guiSettings import textFont, getColours, STRIPHEADER_BACKGROUND, \
    STRIPHEADER_FOREGROUND, GUINMRRESIDUE

import json
from ccpn.ui.gui.widgets.DropBase import DropBase
from ccpn.ui.gui.lib.mouseEvents import getMouseEventDict
import re


try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "OpenGL hellogl",
                                   "PyOpenGL must be installed to run this example.")
    sys.exit(1)

UNITS_PPM = 'ppm'
UNITS_HZ = 'Hz'
UNITS_POINT = 'point'
UNITS = [UNITS_PPM, UNITS_HZ, UNITS_POINT]

removeTrailingZero = re.compile(r'^(\d*[\d.]*?)\.?0*$')


class CcpnGLWidgetABC(QOpenGLWidget):
    """Widget to handle all visible spectra/peaks/integrals/multiplets
    """
    AXIS_MARGINRIGHT = 50
    AXIS_MARGINBOTTOM = 25
    AXIS_LINE = 7
    AXIS_OFFSET = 3
    YAXISUSEEFORMAT = False
    INVERTXAXIS = True
    INVERTYAXIS = True
    AXISLOCKEDBUTTON = True
    SPECTRUMXZOOM = 1.0e1
    SPECTRUMYZOOM = 1.0e1
    SHOWSPECTRUMONPHASING = True
    XAXES = GLDefs.XAXISUNITS
    YAXES = GLDefs.YAXISUNITS

    def __init__(self, parent=None, mainWindow=None, **kwds):
        super().__init__(parent=parent)

        # flag to display paintGL but keep an empty screen
        self._blankDisplay = False

        self.mainWindow = mainWindow
        if mainWindow:
            self.application = mainWindow.application
            self.project = mainWindow.application.project
            self.current = mainWindow.application.current
        else:
            self.application = None
            self.project = None
            self.current = None

        self._preferences = self.application.preferences.general
        self.globalGL = None

        # add a flag so that scaling cannot be done until the gl attributes are initialised
        self.glReady = False

        self.setMouseTracking(True)  # generate mouse events when button not pressed

        # always respond to mouse events
        self.setFocusPolicy(Qt.StrongFocus)

        # initialise all attributes
        self._initialiseAll()

        # set a minimum size so that everything resizes nicely
        self.setMinimumSize(self.AXIS_MARGINRIGHT + 10, self.AXIS_MARGINBOTTOM + 10)

        # set the pyqtsignal responders
        self.GLSignals = GLNotifier(parent=self)
        self.GLSignals.glEvent.connect(self._glEvent)

        # install handler to resize when moving between displays
        self.mainWindow.window().windowHandle().screenChanged.connect(self._screenChangedEvent)

    def _initialiseAll(self):
        """Initialise all attributes for the display
        """
        # if self.glReady: return

        self.w = self.width()
        self.h = self.height()

        self.lastPos = QPoint()
        self._mouseX = 0
        self._mouseY = 0
        self.pixelX = 1.0
        self.pixelY = 1.0
        self.deltaX = 1.0
        self.deltaY = 1.0

        self._devicePixelRatio = 1.0  # set in the initialiseGL routine

        # set initial axis limits - should be changed by strip.display..
        self.axisL = -1.0
        self.axisR = 1.0
        self.axisT = 1.0
        self.axisB = -1.0
        self.storedZooms = []

        self.base = None
        self.spectrumValues = []

        self.highlighted = False
        self._drawSelectionBox = False
        self._drawMouseMoveLine = False
        self._drawDeltaOffset = False
        self._selectionMode = 0
        self._startCoordinate = None
        self._endCoordinate = None
        self.cursorCoordinate = np.zeros((4,), dtype=np.float32)

        self._shift = False
        self._command = False
        self._key = ''
        self._isSHIFT = ''
        self._isCTRL = ''
        self._isALT = ''
        self._isMETA = ''

        self.buildMarks = True
        self._marksList = None
        self._infiniteLines = []
        self._regionList = None
        self._orderedAxes = None
        self._axisOrder = None
        self._axisCodes = None
        self._refreshMouse = False
        self._successiveClicks = None  # GWV: Store successive click events for zooming; None means first click not set
        self._dottedCursorCoordinate = None
        self._dottedCursorVisible = None

        self.gridList = []
        self._gridVisible = True
        self._crossHairVisible = True
        self._axesVisible = True
        self._axisLocked = False
        self._showSpectraOnPhasing = False
        self._xUnits = 0
        self._yUnits = 0

        self._drawRightAxis = True
        self._drawBottomAxis = True
        self.modeDecimal = [False, False]

        # here for completeness, although they should be updated in rescale
        self._currentView = GLDefs.MAINVIEW
        self._currentRightAxisView = GLDefs.RIGHTAXIS
        self._currentRightAxisBarView = GLDefs.RIGHTAXISBAR
        self._currentBottomAxisView = GLDefs.BOTTOMAXIS
        self._currentBottomAxisBarView = GLDefs.BOTTOMAXISBAR

        self._oldStripIDLabel = None
        self.stripIDString = None
        self._spectrumSettings = {}
        self._newStripID = False

        self._setColourScheme()

        self._gridVisible = self._preferences.showGrid
        self._updateHTrace = False
        self._updateVTrace = False
        self._lastTracePoint = {}  # [-1, -1]

        self._applyXLimit = self._preferences.zoomXLimitApply
        self._applyYLimit = self._preferences.zoomYLimitApply
        self._intensityLimit = self._preferences.intensityLimit

        self._GLIntegralLists = {}
        self._GLIntegralLabels = {}

        self._marksAxisCodes = []
        self._regions = []
        self._infiniteLines = []
        self._buildTextFlag = True

        self._buildMouse = True
        self._mouseCoords = [-1.0, -1.0]
        self.mouseString = None
        self.diffMouseString = None
        self.peakLabelling = 0

        self._contourList = {}

        self._uPMatrix = np.zeros((16,), dtype=np.float32)
        self._uMVMatrix = np.zeros((16,), dtype=np.float32)
        self._uVMatrix = np.zeros((16,), dtype=np.float32)
        self._dataMatrix = np.zeros((16,), dtype=np.float32)
        self._aMatrix = np.zeros((16,), dtype=np.float32)
        self._IMatrix = np.zeros((16,), dtype=np.float32)
        self._IMatrix[0:16] = [1.0, 0.0, 0.0, 0.0,
                               0.0, 1.0, 0.0, 0.0,
                               0.0, 0.0, 1.0, 0.0,
                               0.0, 0.0, 0.0, 1.0]

        self.vInv = None
        self.mouseTransform = None

        self._useTexture = np.zeros((1,), dtype=np.int)
        self._axisScale = np.zeros((4,), dtype=np.float32)
        self._background = np.zeros((4,), dtype=np.float32)
        self._parameterList = np.zeros((4,), dtype=np.int32)
        self._view = np.zeros((4,), dtype=np.float32)
        self.cursorCoordinate = np.zeros((4,), dtype=np.float32)

        self.resetRangeLimits()

        self._ordering = []
        self.glReady = True

    def close(self):
        self.GLSignals.glEvent.disconnect()

    @pyqtSlot()
    def _screenChangedEvent(self, *args):
        self._screenChanged(*args)
        self.update()

    def _screenChanged(self, *args):
        screens = QApplication.screens()
        if self.hasFocus():
            # follow the mouse if has focus
            screen = QApplication.desktop().screenNumber(QtGui.QCursor().pos())
        else:
            # otherwise follow the position of self
            screen = QApplication.desktop().screenNumber(self)
        self._devicePixelRatio = screens[screen].devicePixelRatio()
        self.viewports._devicePixelRatio = self._devicePixelRatio

    def resetRangeLimits(self, allLimits=True):
        # reset zoom limits for the display
        self._minXRange, self._maxXRange = GLDefs.RANGELIMITS
        self._minYRange, self._maxYRange = GLDefs.RANGELIMITS
        self._maxX, self._minX = GLDefs.AXISLIMITS
        self._maxY, self._minY = GLDefs.AXISLIMITS
        if allLimits:
            self._rangeXDefined = False
            self._rangeYDefined = False
            self._minXReached = False
            self._minYReached = False
            self._maxXReached = False
            self._maxYReached = False

            self._minReached = False
            self._maxReached = False

    def _setColourScheme(self):
        """Update colours from colourScheme
        """
        self.colours = getColours()
        self.hexBackground = self.colours[CCPNGLWIDGET_HEXBACKGROUND]
        self.background = self.colours[CCPNGLWIDGET_BACKGROUND]
        self.foreground = self.colours[CCPNGLWIDGET_FOREGROUND]
        self.mousePickColour = self.colours[CCPNGLWIDGET_PICKCOLOUR]
        self.gridColour = self.colours[CCPNGLWIDGET_GRID]
        self.highlightColour = self.colours[CCPNGLWIDGET_HIGHLIGHT]
        self._labellingColour = self.colours[CCPNGLWIDGET_LABELLING]

        self.zoomAreaColour = self.colours[CCPNGLWIDGET_ZOOMAREA]
        self.pickAreaColour = self.colours[CCPNGLWIDGET_PICKAREA]
        self.selectAreaColour = self.colours[CCPNGLWIDGET_SELECTAREA]
        self.zoomLineColour = self.colours[CCPNGLWIDGET_ZOOMLINE]
        self.mouseMoveLineColour = self.colours[CCPNGLWIDGET_MOUSEMOVELINE]

        self.zoomAreaColourHard = (*self.colours[CCPNGLWIDGET_ZOOMAREA][0:3], CCPNGLWIDGET_HARDSHADE)
        self.pickAreaColourHard = (*self.colours[CCPNGLWIDGET_PICKAREA][0:3], CCPNGLWIDGET_HARDSHADE)
        self.selectAreaColourHard = (*self.colours[CCPNGLWIDGET_SELECTAREA][0:3], CCPNGLWIDGET_HARDSHADE)

    @pyqtSlot(dict)
    def _glEvent(self, aDict):
        """process events from the application/popups and other strips
        :param aDict - dictionary containing event flags:
        """
        if aDict:
            if aDict[GLNotifier.GLSOURCE] != self:

                # check the params for actions and update the display
                triggers = aDict[GLNotifier.GLTRIGGERS]
                targets = aDict[GLNotifier.GLTARGETS]

                if triggers or targets:

                    if GLNotifier.GLPREFERENCES in triggers:
                        self._preferencesUpdate()
                        self._rescaleXAxis(update=False)
                        self.stripIDString.renderMode = GLRENDERMODE_REBUILD

        # repaint
        self.update()

    def _preferencesUpdate(self):
        """update GL values after the preferences have changed
        """
        self._setColourScheme()
        self.setBackgroundColour(self.background)

    def initializeGL(self):
        # GLversionFunctions = self.context().versionFunctions()
        # GLversionFunctions.initializeOpenGLFunctions()
        # self._GLVersion = GLversionFunctions.glGetString(GL.GL_VERSION)

        # initialise a common to all OpenGL windows
        self.globalGL = GLGlobalData(parent=self)

        # initialise the arrays for the grid and axes
        self.gridList = []
        for li in range(3):
            self.gridList.append(GLVertexArray(numLists=1,
                                               renderMode=GLRENDERMODE_REBUILD,
                                               blendMode=False,
                                               drawMode=GL.GL_LINES,
                                               dimension=2,
                                               GLContext=self))

        self._externalRegions = GLExternalRegion(project=self.project, GLContext=self, spectrumView=None,
                                                 integralListView=None)

        self._selectionBox = GLVertexArray(numLists=1,
                                           renderMode=GLRENDERMODE_REBUILD,
                                           blendMode=True,
                                           drawMode=GL.GL_QUADS,
                                           dimension=3,
                                           GLContext=self)
        self._selectionOutline = GLVertexArray(numLists=1,
                                               renderMode=GLRENDERMODE_REBUILD,
                                               blendMode=True,
                                               drawMode=GL.GL_LINES,
                                               dimension=3,
                                               GLContext=self)

        self.viewports = GLViewports()
        self._screenChanged()
        self.viewports.setDevicePixelRatio(self._devicePixelRatio)

        # define the main viewports
        self.viewports.addViewport(GLDefs.MAINVIEW, self, (0, 'a'), (self.AXIS_MARGINBOTTOM, 'a'),
                                   (-self.AXIS_MARGINRIGHT, 'w'), (-self.AXIS_MARGINBOTTOM, 'h'))

        self.viewports.addViewport(GLDefs.MAINVIEWFULLWIDTH, self, (0, 'a'), (self.AXIS_MARGINBOTTOM, 'a'),
                                   (0, 'w'), (-self.AXIS_MARGINBOTTOM, 'h'))

        self.viewports.addViewport(GLDefs.MAINVIEWFULLHEIGHT, self, (0, 'a'), (0, 'a'),
                                   (-self.AXIS_MARGINRIGHT, 'w'), (0, 'h'))

        # define the viewports for the right axis bar
        self.viewports.addViewport(GLDefs.RIGHTAXIS, self, (-(self.AXIS_MARGINRIGHT + self.AXIS_LINE), 'w'),
                                   (self.AXIS_MARGINBOTTOM, 'a'),
                                   (self.AXIS_LINE, 'a'), (-self.AXIS_MARGINBOTTOM, 'h'))

        self.viewports.addViewport(GLDefs.RIGHTAXISBAR, self, (-self.AXIS_MARGINRIGHT, 'w'),
                                   (self.AXIS_MARGINBOTTOM, 'a'),
                                   (0, 'w'), (-self.AXIS_MARGINBOTTOM, 'h'))

        self.viewports.addViewport(GLDefs.FULLRIGHTAXIS, self, (-(self.AXIS_MARGINRIGHT + self.AXIS_LINE), 'w'),
                                   (0, 'a'),
                                   (self.AXIS_LINE, 'a'), (0, 'h'))

        self.viewports.addViewport(GLDefs.FULLRIGHTAXISBAR, self, (-self.AXIS_MARGINRIGHT, 'w'), (0, 'a'),
                                   (0, 'w'), (0, 'h'))

        # define the viewports for the bottom axis bar
        self.viewports.addViewport(GLDefs.BOTTOMAXIS, self, (0, 'a'), (self.AXIS_MARGINBOTTOM, 'a'),
                                   (-self.AXIS_MARGINRIGHT, 'w'), (self.AXIS_LINE, 'a'))

        self.viewports.addViewport(GLDefs.BOTTOMAXISBAR, self, (0, 'a'), (0, 'a'),
                                   (-self.AXIS_MARGINRIGHT, 'w'), (self.AXIS_MARGINBOTTOM, 'a'))

        self.viewports.addViewport(GLDefs.FULLBOTTOMAXIS, self, (0, 'a'), (self.AXIS_MARGINBOTTOM, 'a'),
                                   (0, 'w'), (self.AXIS_LINE, 'a'))

        self.viewports.addViewport(GLDefs.FULLBOTTOMAXISBAR, self, (0, 'a'), (0, 'a'),
                                   (0, 'w'), (self.AXIS_MARGINBOTTOM, 'a'))

        # define the full viewport
        self.viewports.addViewport(GLDefs.FULLVIEW, self, (0, 'a'), (0, 'a'), (0, 'w'), (0, 'h'))

        # # define the remaining corner
        # self.viewports.addViewport(GLDefs.AXISCORNER, self, (-self.AXIS_MARGINRIGHT, 'w'), (0, 'a'), (0, 'w'), (self.AXIS_MARGINBOTTOM, 'a'))

        # set strings for the overlay text
        self.stripIDString = GLString(text='', font=self.globalGL.glSmallFont, x=0, y=0, GLContext=self, obj=None)

        # This is the correct blend function to ignore stray surface blending functions
        GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE)
        self.setBackgroundColour(self.background)
        self.globalGL._shaderProgramTex.setBlendEnabled(0)

    def paintGL(self):
        w = self.w
        h = self.h

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        if self._blankDisplay:
            return

        # stop notifiers interfering with paint event
        self.project.blankNotification()

        currentShader = self.globalGL._shaderProgram1.makeCurrent()

        # start with the grid mapped to (0..1, 0..1) to remove zoom errors here
        currentShader.setProjectionAxes(self._uPMatrix, 0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
        currentShader.setGLUniformMatrix4fv('pMatrix', 1, GL.GL_FALSE, self._uPMatrix)

        # draw the grid components
        # self.drawGrid()

        # set the scale to the axis limits, needs addressing correctly, possibly same as grid
        currentShader.setProjectionAxes(self._uPMatrix, self.axisL, self.axisR, self.axisB,
                                        self.axisT, -1.0, 1.0)
        currentShader.setGLUniformMatrix4fv('pMatrix', 1, GL.GL_FALSE, self._uPMatrix)

        # draw the spectra, need to reset the viewport
        self.viewports.setViewport(self._currentView)

        # change to the text shader
        currentShader = self.globalGL._shaderProgramTex.makeCurrent()

        currentShader.setProjectionAxes(self._uPMatrix, self.axisL, self.axisR, self.axisB, self.axisT, -1.0, 1.0)
        currentShader.setGLUniformMatrix4fv('pTexMatrix', 1, GL.GL_FALSE, self._uPMatrix)

        self._axisScale[0:4] = [self.pixelX, self.pixelY, 1.0, 1.0]
        currentShader.setGLUniform4fv('axisScale', 1, self._axisScale)

        self.enableTexture()
        currentShader = self.globalGL._shaderProgram1.makeCurrent()
        currentShader.setGLUniformMatrix4fv('mvMatrix', 1, GL.GL_FALSE, self._IMatrix)

        currentShader.setProjectionAxes(self._uPMatrix, 0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
        currentShader.setGLUniformMatrix4fv('pMatrix', 1, GL.GL_FALSE, self._uPMatrix)

        self.drawSelectionBox()
        self.drawCursors()

        currentShader = self.globalGL._shaderProgramTex.makeCurrent()

        self._setViewPortFontScale()
        self.drawMouseCoords()

        # make the overlay/axis solid
        self.globalGL._shaderProgramTex.setBlendEnabled(0)
        self.drawOverlayText()
        self.drawAxisLabels()
        self.globalGL._shaderProgramTex.setBlendEnabled(1)

        self.disableTexture()

        # use the current viewport matrix to display the last bit of the axes
        currentShader = self.globalGL._shaderProgram1.makeCurrent()
        currentShader.setProjectionAxes(self._uVMatrix, 0, w - self.AXIS_MARGINRIGHT, -1, h - self.AXIS_MARGINBOTTOM,
                                        -1.0, 1.0)

        self.viewports.setViewport(self._currentView)

        # why are these labelled the other way round?
        currentShader.setGLUniformMatrix4fv('pMatrix', 1, GL.GL_FALSE, self._uVMatrix)
        currentShader.setGLUniformMatrix4fv('mvMatrix', 1, GL.GL_FALSE, self._IMatrix)

        # cheat for the moment to draw the axes (if visible)
        if self.highlighted:
            colour = self.highlightColour
        else:
            colour = self.foreground

        GL.glDisable(GL.GL_BLEND)
        GL.glColor4f(*colour)
        GL.glBegin(GL.GL_LINES)

        if self._drawBottomAxis:
            GL.glVertex2d(0, 0)
            GL.glVertex2d(w - self.AXIS_MARGINRIGHT, 0)

        if self._drawRightAxis:
            GL.glVertex2d(w - self.AXIS_MARGINRIGHT, 0)
            GL.glVertex2d(w - self.AXIS_MARGINRIGHT, h - self.AXIS_MARGINBOTTOM)

        GL.glEnd()

        # re-enable notifiers
        self.project.unblankNotification()

    def setBackgroundColour(self, col, silent=False):
        """
        set all background colours in the shaders
        :param col - vec4, 4 element list e.g.: [0.05, 0.05, 0.05, 1.0], very dark gray
        """
        self.makeCurrent()
        GL.glClearColor(*col)
        self.background = col

        self.globalGL._shaderProgram1.makeCurrent()
        self.globalGL._shaderProgram1.setBackground(self.background)
        self.globalGL._shaderProgramTex.makeCurrent()
        self.globalGL._shaderProgramTex.setBackground(self.background)
        self.doneCurrent()
        if not silent:
            self.update()

        self.doneCurrent()
        self.update()

    def enableTexture(self):
        GL.glEnable(GL.GL_BLEND)
        # GL.glEnable(GL.GL_TEXTURE_2D)
        # GL.glBindTexture(GL.GL_TEXTURE_2D, self.globalGL.glSmallFont.textureId)

        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.globalGL.glSmallFont.textureId)
        GL.glActiveTexture(GL.GL_TEXTURE1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.globalGL.glSmallTransparentFont.textureId)

        # # specific blend function for text overlay
        # GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_DST_COLOR, GL.GL_ONE, GL.GL_ONE)

    def disableTexture(self):
        GL.glDisable(GL.GL_BLEND)

        # # reset blend function
        # GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE)




