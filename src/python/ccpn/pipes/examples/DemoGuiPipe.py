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
__modifiedBy__ = "$modifiedBy: Luca Mureddu $"
__dateModified__ = "$dateModified: 2017-05-28 10:28:42 +0000 (Sun, May 28, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Luca Mureddu $"
__date__ = "$Date: 2017-05-28 10:28:42 +0000 (Sun, May 28, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================


from ccpn.ui.gui.widgets.PipelineWidgets import GuiPipe, PipelineDropArea , AutoGeneratedGuiPipe
from ccpn.ui.gui.widgets.PulldownList import PulldownList

class DemoGuiPipe(GuiPipe):
  preferredPipe = True
  pipeName = 'AlignSpectra'

  def __init__(self, name=pipeName, parent=None, project=None,   **kw):
    super(DemoGuiPipe, self)
    GuiPipe.__init__(self, parent=parent, name=name, project=project, **kw )
    self.parent = parent

    # add widgets to pipeFrame using Base grid=(i,ii) or self.pipeLayout.addWidget(widgetName)
    self.demoPulldownList = PulldownList(self.pipeFrame, texts=['spectrum1', 'spectrum2'], grid=(0,0))



# run this file to test the gui
if __name__ == '__main__':
  from PyQt4 import QtGui
  from ccpn.ui.gui.widgets.Application import TestApplication

  app = TestApplication()
  win = QtGui.QMainWindow()

  pipeline = PipelineDropArea()
  demoGuiPipe = DemoGuiPipe(parent=pipeline)
  pipeline.addDock(demoGuiPipe)

  win.setCentralWidget(pipeline)
  win.resize(1000, 500)
  win.show()

  app.start()

