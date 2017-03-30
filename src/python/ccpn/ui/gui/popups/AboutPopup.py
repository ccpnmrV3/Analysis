"""Module Documentation here

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
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================

import os
from ccpn.util import Path
from PyQt4 import QtGui, QtCore
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.ButtonList import ButtonList

# This text is being copied on the clipboard only. Is not the source of the image in the popup.
# The image is in ccpn.ui.gui.widgets

TEXT = ''' Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - 2017
| 
            **Please cite: **
            Skinner et al, J Biomol NMR (2016) 66:111–124; DOI 10.1007/s10858-016-0060-y

            **Written by: **
            Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan, Simon P Skinner & Geerten W Vuister

            **This programs uses:**
            The CCPN data model: J Biomol NMR (2006) 36:147–155, DOI 10.1007/s10858-006-9076-z 
            PyQtGraph (http://www.pyqtgraph.org)
            PyQt (http://pyqt.sourceforge.net)
            Miniconda, subject to Anaconda End User Licence Agreement (https://docs.continuum.io/anaconda/eula)

            **Disclaimer:**
            This program is offered 'as-is'. Under no circumstances will the authors, CCPN, the Department of Molecular 
            and Cell Biology, or the University of Leicester be liable of any damage, loss of data, loss of revenue or 
            any other undesired consequences originating from the usage of this software.
        '''


class AboutPopup(QtGui.QDialog):
  def __init__(self, parent=None, **kw):
    super(AboutPopup, self).__init__(parent)
    self.setWindowTitle("About CcpNmr")
    self.setContentsMargins(5, 5, 5, 5)

    pathPNG = os.path.join(Path.getPathToImport('ccpn.ui.gui.widgets'), 'About_CcpNmr.png')
    self.label = Label(self, grid=(0, 0))
    self.label.setPixmap(QtGui.QPixmap(pathPNG))
    self.buttons = ButtonList(self, texts=['Close', 'Copy'],
                              callbacks=[self.accept, self.copyToClipboard],
                              tipTexts=['Close window', 'Copy text to clipboard'],
                              grid=(1, 0), hAlign='r')

    self.setMaximumWidth(self.size().width())

  def copyToClipboard(self):
    '''TEXT being copied on the clipboard '''
    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard)
    cb.setText(TEXT, mode=cb.Clipboard)

