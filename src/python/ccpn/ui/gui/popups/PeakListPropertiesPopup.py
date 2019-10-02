"""
Module Documentation here
"""
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
__dateModified__ = "$dateModified: 2017-07-07 16:32:48 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-03-30 11:28:58 +0100 (Thu, March 30, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import ccpn.util.Colour as Colour
from ccpn.ui.gui.widgets.MessageDialog import MessageDialog
from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.popups.Dialog import CcpnDialog, handleDialogApply
from ccpn.ui.gui.lib.OpenGL.CcpnOpenGL import GLNotifier
from ccpn.core.lib.ContextManagers import undoStackBlocking
from ccpn.ui.gui.popups.PeakListPropertiesPopupABC import PeakListPropertiesPopupABC
from ccpn.core.PeakList import PeakList


class PeakListPropertiesPopup(PeakListPropertiesPopupABC):
    """
    Popup to handle changing parameters in peakLists
    """
    # class of lists handled by popup
    _baseClass = PeakList
    _symbolColourOption = True
    _textColourOption = True
    _lineColourOption = True
    _meritColourOption = True
    _meritOptions = True

    def __init__(self, parent=None, mainWindow=None, peakList=None, title='Peak List Properties', **kwds):
        # CcpnDialog.__init__(self, parent, setLayout=True, windowTitle=title, **kwds)

        super().__init__(parent=parent, mainWindow=mainWindow, ccpnList=peakList,
                         title='%s Properties' % self._baseClass.className, **kwds)

    def _refreshGLItems(self):
        # emit a signal to rebuild all peaks and multiplets
        self.GLSignals.emitEvent(targets=[self.ccpnList], triggers=[GLNotifier.GLPEAKLISTS,
                                                                    GLNotifier.GLPEAKLISTLABELS])

    def _getListViews(self, ccpnList):
        """Return the listViews containing this list
        """
        return [peakListView for peakListView in ccpnList.project.peakListViews if peakListView.peakList == ccpnList]
