#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2019"
__credits__ = ("Ed Brooksbank, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license")
__reference__ = ("Skinner, S.P., Fogh, R.H., Boucher, W., Ragan, T.J., Mureddu, L.G., & Vuister, G.W.",
                 "CcpNmr AnalysisAssign: a flexible platform for integrated NMR analysis",
                 "J.Biomol.Nmr (2016), 66, 111-124, http://doi.org/10.1007/s10858-016-0060-y")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:32:52 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.dockarea.Dock import DockLabel, Dock
from ccpn.ui.gui.guiSettings import moduleLabelFont


class CcpnDock(Dock):
    def __init__(self, name):
        super().__init__(name=name, area=self)
        self.label.hide()
        self.label = CcpnDockLabel(name.upper(), self)
        self.label.show()
        self.label.closeButton.clicked.connect(self.closeModule)
        self.label.fixedWidth = True
        self.autoOrientation = False
        self.mainWidget = QtWidgets.QWidget(self)
        self.settingsWidget = QtWidgets.QWidget(self)
        self.addWidget(self.mainWidget, 0, 0)
        self.addWidget(self.settingsWidget, 1, 0)

    def resizeEvent(self, event):
        self.setOrientation('vertical', force=True)
        self.resizeOverlay(self.size())

    def closeDock(self):
        self.close()


class CcpnDockLabel(DockLabel):

    def __init__(self, *args):
        super().__init__(showCloseButton=True, *args)
        self.setFont(moduleLabelFont)

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.pressPos = ev.pos()
            self.startedDrag = False
            ev.accept()
