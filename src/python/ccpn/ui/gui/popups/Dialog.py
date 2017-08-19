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
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-07-04 15:21:16 +0000 (Tue, July 04, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================


from PyQt4 import QtGui
from ccpn.ui.gui.widgets.Base import Base

class CcpnDialog(QtGui.QDialog, Base):
  def __init__(self, parent=None, windowTitle='', setLayout=False, size=(200,100), **kw):
    QtGui.QDialog.__init__(self, parent)
    Base.__init__(self, setLayout=setLayout, **kw)

    self.setWindowTitle(windowTitle)
    self.setContentsMargins(15, 15, 15, 15)
    self.resize(*size)

    # self.mainLayout = QtGui.QGridLayout()   # ejb - handled inside Base
    # self.setLayout(self.mainLayout)

  def fixedSize(self):
    self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    self.sizePolicy.setHorizontalStretch(0)
    self.sizePolicy.setVerticalStretch(0)
    self.setSizePolicy(self.sizePolicy)
    self.setFixedSize(self.maximumWidth(), self.maximumHeight())
    self.setSizeGripEnabled(False)

  #TODO:ED include widget here for self.centralWidget, self.buttonWidget and undo functionality
