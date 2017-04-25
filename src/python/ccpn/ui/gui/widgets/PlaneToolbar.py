"""
This module defines a specific Toolbar class for the strip display 
The NmrResidueLabel allows drag and drop of the ids displayed in them

"""

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
__dateModified__ = "$dateModified: 2017-04-07 11:40:43 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: simon1 $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from functools import partial

from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.ui.gui.widgets.ToolBar import ToolBar

import json
from ccpn.ui.gui.widgets.DropBase import DropBase
from ccpn.ui.gui.lib.mouseEvents import getMouseEventDict
from ccpn.core.NmrResidue import NmrResidue


from PyQt4 import QtGui, QtCore


class _StripLabel(Label):
  """
  Specific Label to be used in Strip displays
  """
  def __init__(self, parent, text, appBase, **kwds):

    Label.__init__(self, parent, text, **kwds)
    self.parent = parent
    self.mousePressEvent = self._mousePressEvent
    self.dragMoveEvent= self._dragMoveEvent
    self.setAcceptDrops(True)
    #self.setDragEnabled(True) not possile for Label

    # disable any drop event callback's until explicitly defined later
    self.setDropEventCallback(None)

  def _dragMoveEvent(self, event:QtGui.QMouseEvent):
    """
    Required function to enable dragging and dropping within the sidebar.
    """
    event.accept()

  def _mousePressEvent(self, event:QtGui.QMouseEvent):
    """
    Re-implementation of the mouse press event to enable a NmrResidue label to be dragged as a json object
    containing its id and a modifier key to encode the direction to drop the strip.
    """
    event.accept()
    mimeData = QtCore.QMimeData()
    # create the dataDict
    dataDict = {'ids':[self.text()]}
    # update the dataDict with all mouseEvents
    dataDict.update(getMouseEventDict(event))
    # convert into json
    itemData = json.dumps(dataDict)
    mimeData.setData(DropBase.JSONDATA, self.text())
    mimeData.setText(itemData)
    drag = QtGui.QDrag(self)
    drag.setMimeData(mimeData)
    if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
      pass
    else:
      self.show()

  @staticmethod
  def _updateLabelText(nmrResidue:NmrResidue, oldPid:str):
    """Effect rename for NmrResidueLabel
       For notifiers
       #CCPN INTERNAL: used in ui.gui.Gui.py to set a notifier on rename of NmrResidue  
    """
    #oldId = oldPid.split(Pid.PREFIXSEP, 1)[-1]
    oldId = oldPid.id
    for strip in nmrResidue.project.strips:
      if strip.planeToolbar.spinSystemLabel.text() == oldId:
        strip.planeToolbar.spinSystemLabel.setText(nmrResidue.id)


class PlaneToolbar(ToolBar):
  #TODO: undocumented and needs refactoring ;
  def __init__(self, strip, callbacks, **kw):

    ToolBar.__init__(self, strip.stripFrame, **kw)

    self.stripIdLabel = Label(self, text='.'.join(strip.pid.id.split('.')[2:]),
                            hAlign='center', vAlign='top')
    self.stripIdLabel.setFixedHeight(15)
    self.stripIdLabel.setFont(QtGui.QFont('Lucida Grande', 10))
#    self.spinSystemLabel = Label(self, text='',
#                                 hAlign='center', vAlign='top')
    # Drop/draggable label
    self.spinSystemLabel = _StripLabel(self, text='',
                                      appBase=strip._parent._appBase,
                                      hAlign='center', vAlign='top'
    )

    self.spinSystemLabel.setFixedHeight(15)
    self.spinSystemLabel.setFont(QtGui.QFont('Lucida Grande', 10))
    self.addWidget(self.stripIdLabel)
    self.addWidget(self.spinSystemLabel)

    self.planeLabels = []
    self.planeCounts = []
    for i in range(len(strip.orderedAxes)-2):
      self.prevPlaneButton = Button(self, '<', callback=partial(callbacks[0], i))
      self.prevPlaneButton.setFixedWidth(19)
      self.prevPlaneButton.setFixedHeight(19)
      planeLabel = DoubleSpinbox(self, showButtons=False)
      planeLabel.setFixedHeight(19)
      # below does not work because it allows wheel events to behave but not manual text entry (some Qt stupidity)
      # so instead use a wheelEvent to deal with the wheel events and editingFinished (in GuiStripNd) to do text
      #planeLabel.valueChanged.connect(partial(callbacks[2], i))
      if callbacks[2]:
        planeLabel.wheelEvent = partial(self._wheelEvent, i)
        self.prevPlaneCallback = callbacks[0]
        self.nextPlaneCallback = callbacks[1]
      self.nextPlaneButton = Button(self,'>', callback=partial(callbacks[1], i))
      self.nextPlaneButton.setFixedWidth(19)
      self.nextPlaneButton.setFixedHeight(19)
      planeCount = Spinbox(self, showButtons=False, hAlign='c')
      planeCount.setMinimum(1)
      planeCount.setValue(1)
      planeCount.oldValue = 1
      planeCount.valueChanged.connect(partial(callbacks[3], i))
      self.addWidget(self.prevPlaneButton)
      self.addWidget(planeLabel)
      self.addWidget(self.nextPlaneButton)
      self.addWidget(planeCount)
      self.planeLabels.append(planeLabel)
      self.planeCounts.append(planeCount)

  def _wheelEvent(self, n, event):
    if event.delta() > 0: # note that in Qt5 this becomes angleDelta()
      if self.prevPlaneCallback:
        self.prevPlaneCallback(n)
    else:
      if self.nextPlaneCallback:
        self.nextPlaneCallback(n)
