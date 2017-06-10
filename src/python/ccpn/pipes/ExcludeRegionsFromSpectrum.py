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
from ccpn.framework.lib.Pipe import SpectraPipe



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
    self.addRemoveButtons = ButtonList(self.pipeFrame, texts=["+", "-"], callbacks=[self._addRegion,self._deleteRegions], grid=(0, 1))
    self.count = 1

    self.excludeRegion1Label = Label(self.pipeFrame, text="Select Region "+str(self.count), grid=(self.count , 0))
    self.excludeRegion1 = TargetButtonSpinBoxes(self.pipeFrame, application=self.application, orientation='v',
                                                grid=(self.count , 1))
    self.count += 1

  ############       Gui Callbacks      ###########

  def _addRegion(self):
    self.excludeRegionLabel = Label(self.pipeFrame, text="Select Region " + str(self.count), grid=(self.count, 0))
    w = setattr(self, 'region'+str(self.count), TargetButtonSpinBoxes(self.pipeFrame, application=self.application, orientation='v',
                                                grid=(self.count , 1)))

    self.count+=1

  def _deleteRegions(self):
    '''  delete the widget from layout. '''
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
              if isinstance(w,TargetButtonSpinBoxes):
                w._turnOffPositionPicking()
              w.deleteLater()
        self.count -= 1



########################################################################################################################
##########################################       PIPE      #############################################################
########################################################################################################################




class ExcludeRegionsPipe(SpectraPipe):

  guiPipe = ExcludeRegionsGuiPipe
  pipeName = guiPipe.pipeName

  _kwargs = {
             'excludeRegions': [[],[]]
             }


  def runPipe(self, spectra):
    '''
    get excluded region of the spectrum and add to the pipeline kwargs.
    Spectra is not really needed for this pipe. But is essential for the base class pipe.
    '''
    regions = []
    for i in self._kwargs.values():
      if isinstance(i, list):
        if len(i) == 2:
          regions.append(i)

    self._kwargs = {'excludeRegions': regions}
    self.pipeline._kwargs.update(self._kwargs)

    return spectra




ExcludeRegionsPipe.register() # Registers the pipe in the pipeline

