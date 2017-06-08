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


#### GUI IMPORTS
from ccpn.ui.gui.widgets.PipelineWidgets import GuiPipe
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.ButtonList import ButtonList
from ccpn.ui.gui.widgets.LinearRegionsPlot import TargetButtonSpinBoxes
from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.RadioButtons import RadioButtons
from ccpn.ui.gui.widgets.Label import Label

#### NON GUI IMPORTS
from ccpn.framework.lib.Pipe import Pipe



########################################################################################################################
##########################################      ALGORITHM       ########################################################
########################################################################################################################



########################################################################################################################
##########################################     GUI PIPE    #############################################################
########################################################################################################################



class ExcludeRegionsGuiPipe(GuiPipe):

  preferredPipe = True
  pipeName = 'Exclude Regions'

  def __init__(self, name=pipeName, parent=None, project=None,   **kw):
    super(ExcludeRegionsGuiPipe, self)
    GuiPipe.__init__(self, parent=parent, name=name, project=project, **kw )
    self.parent = parent

    self.addRemoveLabel = Label(self.pipeFrame, text="Add Region", grid=(0, 0))
    self.addRemoveLabel.isProtected = True
    self.addRemoveButtons = ButtonList(self.pipeFrame, texts=["+", "-"], callbacks=[self._addRegion,self._deleteRegions], grid=(0, 1))
    self.addRemoveButtons.isProtected = True
    self.count = 1


    self.excludeRegion1Label = Label(self.pipeFrame, text="Select Region "+str(self.count), grid=(self.count , 0))
    self.excludeRegion1 = TargetButtonSpinBoxes(self.pipeFrame, application=self.application, orientation='v',
                                                grid=(self.count , 1))

    self.count += 1

  def _addRegion(self):
    self.excludeRegionLabel = Label(self.pipeFrame, text="Select Region " + str(self.count), grid=(self.count, 0))
    w = setattr(self, 'region'+str(self.count), TargetButtonSpinBoxes(self.pipeFrame, application=self.application, orientation='v',
                                                grid=(self.count , 1)))

    self.count+=1

  def _deleteRegions(self):
    '''   '''
    positions = []
    for row in range(self.count):
      positions.append((row, 0))
      positions.append((row, 1))
    if (len(positions))>1:
      positions = positions[2:]
      if len(positions)>1:
        positions = positions[-2:]
        for position in positions:
          item = self.pipeFrame.getLayout().itemAtPosition(*position)
          if item:
            w = item.widget()
            if w:
              w.deleteLater()
        self.count -= 1


########################################################################################################################
##########################################       PIPE      #############################################################
########################################################################################################################




class ExcludeRegionsPipe(Pipe):

  guiPipe = ExcludeRegionsGuiPipe
  pipeName = guiPipe.pipeName



  def runPipe(self, params):
    '''
    :param data:
    :return:
    '''

    print(self._kwargs,)





ExcludeRegionsPipe.register() # Registers the pipe in the pipeline


