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
from PyQt4 import QtGui, QtCore

from ccpncore.gui.Base import Base

class Action(QtGui.QAction, Base):
  def __init__(self, parent, text, callback=None, shortcut=None, checkable=False, icon=None, **kw):
    text = self.translate(text)
    if shortcut:
      if type(shortcut) == type(''):
        shortcut = QtGui.QKeySequence(", ".join(tuple(shortcut)))
      QtGui.QAction.__init__(self, text, parent, shortcut=shortcut,triggered=callback, checkable=checkable)
      QtGui.QAction.setShortcutContext(self, QtCore.Qt.ApplicationShortcut)
      QtGui.QFontDatabase.addApplicationFont('/Users/simon/Downloads/Lato-Black.ttf')
      font = QtGui.QFont('Lato-Black')
      QtGui.QAction.setFont(self, font)
    # elif icon:
    #   QtGui.QAction.__init__(self, icon, text, parent, triggered=callback, checkable=checkable)

    else:
      QtGui.QAction.__init__(self, text, parent, triggered=callback, checkable=checkable)

    # Base.__init__(self, **kw)


