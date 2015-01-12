
from PySide import QtGui

from ccpnmrcore.Base import Base as GuiBase

from pyqtgraph.dockarea import Dock

class GuiModule(Dock, GuiBase):

  def __init__(self, dockArea, apiModule):
    Dock.__init__(self, name=apiModule.name, size=(1100,1300))
    dockArea.addDock(self)
    self.module = apiModule
    self.appBase = dockArea.guiWindow.appBase
    GuiBase.__init__(self, self.appBase)
