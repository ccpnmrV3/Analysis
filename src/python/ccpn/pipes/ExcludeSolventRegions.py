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
from ccpn.ui.gui.widgets.Button import Button
from ccpn.ui.gui.popups.PickPeaks1DPopup import ExcludeRegions

#### NON GUI IMPORTS
from ccpn.framework.lib.Pipe import SpectraPipe


########################################################################################################################
##########################################      ALGORITHM       ########################################################
########################################################################################################################

## NONE

########################################################################################################################
##########################################     GUI PIPE    #############################################################
########################################################################################################################



class ExcludeRegionsGuiPipe(GuiPipe):

  preferredPipe = False
  pipeName = 'Exclude Solvent Regions'

  def __init__(self, name=pipeName, parent=None, project=None,   **kw):
    super(ExcludeRegionsGuiPipe, self)
    GuiPipe.__init__(self, parent=parent, name=name, project=project, **kw )
    self.parent = parent
    self.excludeRegions = ExcludeRegions(self)
    self.pipeLayout.addWidget(self.excludeRegions)




########################################################################################################################
##########################################       PIPE      #############################################################
########################################################################################################################




class ExcludeRegionsPipe(SpectraPipe):

  guiPipe = ExcludeRegionsGuiPipe
  pipeName = guiPipe.pipeName
  _kwargs = {
            'excludeRegions': [[], []]
            }

  def runPipe(self, spectra):
    '''
    :get excluded region of the spectrum and add to the pipeline kwargs.
    Spectra is not really needed for this pipe. But is essential for the base class pipe.
    '''

    self.pipeline._kwargs.update(self._kwargs)
    return spectra





ExcludeRegionsPipe.register() # Registers the pipe in the pipeline

