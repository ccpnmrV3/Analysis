"""

Frame(QtGui.QFrame, Base)


  From: http://pyqt.sourceforge.net/Docs/PyQt4/qframe.html#details

  The QFrame class is the base class of widgets that can have a frame. More...

  Inherits QWidget.

  Inherited by QAbstractScrollArea, QLabel, QLCDNumber, QSplitter, QStackedWidget and QToolBox.

  Types

  enum Shadow { Plain, Raised, Sunken }
  enum Shape { NoFrame, Box, Panel, WinPanel, ..., StyledPanel }
  enum StyleMask { Shadow_Mask, Shape_Mask }
  Methods

  __init__ (self, QWidget parent = None, Qt.WindowFlags flags = 0)
  changeEvent (self, QEvent)
  drawFrame (self, QPainter)
  bool event (self, QEvent e)
  QRect frameRect (self)
  Shadow frameShadow (self)
  Shape frameShape (self)
  int frameStyle (self)
  int frameWidth (self)
  int lineWidth (self)
  int midLineWidth (self)
  paintEvent (self, QPaintEvent)
  setFrameRect (self, QRect)
  setFrameShadow (self, Shadow)
  setFrameShape (self, Shape)
  setFrameStyle (self, int)
  setLineWidth (self, int)
  setMidLineWidth (self, int)
  QSize sizeHint (self)

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author: Geerten Vuister $"
__date__ = "$Date: 2017-04-11 22:04:47 +0100 (Tue, April 11, 2017) $"

#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtGui

from ccpn.ui.gui.widgets.Base import Base

class Frame(QtGui.QFrame, Base):

  def __init__(self, parent=None, showBorder=False, **kwds):
    """
    Initialise a Frame with optional border and layout
    """

    QtGui.QFrame.__init__(self, parent)

    #TODO: replace with proper stylesheet routines once inplemented
    styleSheet = ''
    if 'bgColor' in kwds:
      #rgb = QtGui.QColor(kwds["bgColor"]).getRgb()[:3]
      styleSheet += "background-color: rgb(%d, %d, %d); " % kwds["bgColor"]
      del(kwds['bgColor'])
    if 'fgColor' in kwds:
      styleSheet += "foreground-color: rgb(%d, %d, %d); " % kwds["fgColor"]
      del (kwds['fgColor'])
    if showBorder:
      styleSheet += "border: 1px solid black; "
    else:
      styleSheet += "border: 0px; "
    if len(styleSheet) > 0:
      #print('>>', styleSheet)
      self.setStyleSheet('QFrame {' + styleSheet + '}')

    Base.__init__(self, **kwds)



if __name__ == '__main__':

  from ccpn.ui.gui.widgets.Application import TestApplication
  from ccpn.ui.gui.widgets.BasePopup import BasePopup

  class TestPopup(BasePopup):
    def body(self, parent):
      frame1 = Frame(parent=parent, showBorder=True, bgColor=(255, 255, 0), grid=(0,0))
      frame2 = Frame(parent=parent, showBorder=False, bgColor=(255, 0, 0), grid=(1,0))

  app = TestApplication()
  popup = TestPopup(title='Test Frame')
  popup.resize(400, 400)
  app.start()

