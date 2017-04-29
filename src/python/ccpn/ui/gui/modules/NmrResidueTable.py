"""
This file contains NmrResidueTableModule and NmrResidueTable classes

The NmrResidueModule allows for selection of displays, after which double-clicking a row 
navigates the displays to the relevant positions and marks the NmrAtoms of the selected 
NmrResidue.

Geerten 1-7/12/2016; 11/04/2017
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
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:04 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from ccpn.core.lib import CcpnSorting
from ccpn.ui.gui.modules.CcpnModule import CcpnModule
from ccpn.ui.gui.widgets.Widget import Widget
from ccpn.ui.gui.widgets.CompoundWidgets import CheckBoxCompoundWidget
from ccpn.ui.gui.widgets.CompoundWidgets import ListCompoundWidget
from ccpn.core.lib.Notifiers import Notifier
from ccpn.ui.gui.widgets.PulldownListsForObjects import NmrChainPulldown
from ccpn.ui.gui.widgets.MessageDialog import showWarning
from ccpn.ui.gui.widgets.Table import ObjectTable, Column

from ccpn.ui.gui.lib.Strip import navigateToNmrResidueInDisplay

from ccpn.util.Logging import getLogger
logger = getLogger()

ALL = '<all>'

class NmrResidueTableModule(CcpnModule):
  """
  This class implements the module by wrapping a NmrResidueTable instance
  """
  includeSettingsWidget = True
  maxSettingsState = 2  # states are defined as: 0: invisible, 1: both visible, 2: only settings visible
  settingsOnTop = True

  className = 'NmrResidueTableModule'

  # we are subclassing this Module, hence some more arguments to the init
  def __init__(self, mainWindow, name='NmrResidue Table'):

    CcpnModule.__init__(self, mainWindow=mainWindow, name=name)

    # Derive application, project, and current from mainWindow
    self.mainWindow = mainWindow
    self.application = mainWindow.application
    self.project = mainWindow.application.project
    self.current = mainWindow.application.current

    # settings

    # cannot set a notifier for displays, as these are not (yet?) implemented and the Notifier routines
    # underpinning the addNotifier call do not allow for it either
    self.displaysWidget = ListCompoundWidget(self.settingsWidget, grid=(0,0), vAlign='top',
                                             minimumWidths=(100, 0, 0),
                                             maximumWidths=(100, 100, 100),
                                             orientation = 'left',
                                             labelText="Display module(s):",
                                             texts=[ALL] + [display.pid for display in self.application.ui.mainWindow.spectrumDisplays]
                                            )
    #self.displaysWidget.listWidget.setHeight(40)

    self.sequentialStripsWidget = CheckBoxCompoundWidget(
                                             self.settingsWidget, grid=(1,0), vAlign='top',
                                             minimumWidths=(100, 0),
                                             maximumWidths=(100, 30),
                                             orientation = 'left',
                                             labelText = 'Show sequential strips:',
                                             checked = False
                                            )

    self.markPositionsWidget = CheckBoxCompoundWidget(
                                             self.settingsWidget, grid=(2,0), vAlign='top',
                                             minimumWidths=(100, 0),
                                             maximumWidths=(100, 30),
                                             orientation = 'left',
                                             labelText = 'Mark positions:',
                                             checked = True
                                            )
    self.autoClearMarksWidget = CheckBoxCompoundWidget(
                                             self.settingsWidget, grid=(3,0), vAlign='top',
                                             minimumWidths=(100, 0),
                                             maximumWidths=(100, 30),
                                             orientation = 'left',
                                             labelText = 'Auto clear marks:',
                                             checked = True
                                            )

    # main window
    self.nmrResidueTable = NmrResidueTable(parent=self.mainWidget, application=self.application,
                                           actionCallback=self.navigateToNmrResidue,
                                           grid=(0,0)
                                          )

  def _getDisplays(self):
    "return list of displays to navigate; done so BackboneAssignment module can subclass"
    displays = []
    # check for valid displays
    gids = self.displaysWidget.getTexts()
    if len(gids) == 0: return displays
    if ALL in gids:
        displays = self.application.ui.mainWindow.spectrumDisplays
    else:
        displays = [self.application.getByGid(gid) for gid in gids if gid != ALL]
    return displays

  def navigateToNmrResidue(self, nmrResidue, row=None, col=None):
    "Navigate in selected displays to nmrResidue; skip if none defined"
    logger.debug('nmrResidue=%s' % (nmrResidue.id))

    displays = self._getDisplays()
    if len(displays) == 0:
      logger.warn('Undefined display module(s); select in settings first')
      showWarning('startAssignment', 'Undefined display module(s);\nselect in settings first')
      return

    self.application._startCommandBlock('%s.navigateToNmrResidue(project.getByPid(%r))' %
        (self.className, nmrResidue.pid))
    try:
        # optionally clear the marks
        if self.autoClearMarksWidget.checkBox.isChecked():
            self.application.ui.mainWindow.clearMarks()

        # navigate the displays
        for display in displays:
            if len(display.strips) > 0:
                navigateToNmrResidueInDisplay(nmrResidue, display, stripIndex=0,
                                              widths=['full'] * len(display.strips[0].axisCodes),
                                              showSequentialResidues = (len(display.axisCodes) > 2) and
                                              self.sequentialStripsWidget.checkBox.isChecked(),
                                              markPositions = self.markPositionsWidget.checkBox.isChecked()
                )
    finally:
        self.application._endCommandBlock()


class NmrResidueTable(ObjectTable):
  """
  Class to present a NmrResidue Table and a NmrChain pulldown list, wrapped in a Widget
  """
  columnDefs = [
    ('#',          lambda nmrResidue: nmrResidue.serial, 'NmrResidue serial number'),
    ('Index',      lambda nmrResidue: nmrResidue.nmrChain.nmrResidues.index(nmrResidue), 'Index of NmrResidue in the NmrChain'),
#    ('NmrChain',   lambda nmrResidue: nmrResidue.nmrChain.id, 'NmrChain id'),
    ('Sequence',   lambda nmrResidue: nmrResidue.sequenceCode, 'Sequence code of NmrResidue'),
    ('Type',       lambda nmrResidue: nmrResidue.residueType, 'NmrResidue type'),
    ('NmrAtoms',   lambda nmrResidue: NmrResidueTable._getNmrAtomNames(nmrResidue), 'NmrAtoms in NmrResidue'),
    ('Peak count', lambda nmrResidue: '%3d ' % NmrResidueTable._getNmrResiduePeakCount(nmrResidue), 'Number of peaks assigned to NmrResidue')
  ]

  def __init__(self, parent, application, actionCallback=None, selectionCallback=None, **kwds):

    self._project = application.project
    self._current = application.current
    self._widget = Widget(parent=parent, **kwds)

    # create the column objects
    columns = [Column(colName, func, tipText=tipText) for colName, func, tipText in self.columnDefs]
    selectionCallback = self._selectionCallback if selectionCallback is None else selectionCallback
    # create the table; objects are added later via the displayTableForNmrChain method
    ObjectTable.__init__(self, parent=self._widget,
                         columns=columns, objects = [],
                         autoResize=True,
                         actionCallback=actionCallback, selectionCallback=selectionCallback,
                         grid = (1, 0), gridSpan = (1, 6)
                         )
    # Notifier object to update the table if the nmrChain changes
    self._chainNotifier = None
    #TODO: see how to handle peaks as this is too costly at present
    # Notifier object to update the table if the peaks change
    self._peaksNotifier = None
    # self._peaksNotifier = Notifier(self._project,
    #                                [Notifier.CREATE, Notifier.DELETE, Notifier.RENAME], 'Peak',
    #                                 self._updateCallback
    #                                )
    self._updateSilence = False  # flag to silence updating of the table

    # This widget will display a pulldown list of NmrChain pids in the project
    self.ncWidget = NmrChainPulldown(parent=self._widget,
                                     project=self._project, default=0,  #first NmrChain in project (if present)
                                     grid=(0,0), gridSpan=(1,2), minimumWidths=(0,100),
                                     callback=self._selectionPulldownCallback
                                     )

    if len(self._project.nmrChains) > 0:
      self.displayTableForNmrChain(self._project.nmrChains[0])

  def displayTableForNmrChain(self, nmrChain):
    "Display the table for all NmrResidue's of nmrChain"

    if self._chainNotifier is not None:
      # we have a new nmrChain and hence need to unregister the previous notifier
      self._chainNotifier.unRegister()
    # register a notifier for this nmrChain
    self._chainNotifier = Notifier(nmrChain,
                                   [Notifier.CREATE, Notifier.DELETE, Notifier.RENAME], 'NmrResidue',
                                    self._updateCallback
                                  )

    self.ncWidget.select(nmrChain.pid)
    self._update(nmrChain)

  def _update(self, nmrChain):
    "Update the table with NmrResidues of nmrChain"
    if not self._updateSilence:
      self.clearTable()
      self._silenceCallback = True
      self.setObjects(nmrChain.nmrResidues)
      self._silenceCallback = False
      self.show()

  def setUpdateSilence(self, silence):
    "Silences/unsilences the update of the table until switched again"
    self._updateSilence = silence

  def _selectionCallback(self, nmrResidue, row, col):
    "Callback for selecting a row in the table"
    self._project._appBase.current.nmrResidue = nmrResidue

  def _selectionPulldownCallback(self, item):
    "Callback for selecting NmrChain"
    nmrChain = self._project.getByPid(item)
    print('>selectionPulldownCallback>', item, type(item), nmrChain)
    if nmrChain is not None:
      self.displayTableForNmrChain(nmrChain)

  def _updateCallback(self, data):
    "callback for updating the table"
    nmrChain = data['theObject']
    print('>updateCallback>', data['notifier'], nmrChain, data['trigger'], data['object'], self._updateSilence)
    if nmrChain is not None:
      self._update(nmrChain)

  @staticmethod
  def _getNmrAtomNames(nmrResidue):
    "Returns a sorted list of NmrAtom names"
    return ', '.join(sorted(set([atom.name for atom in nmrResidue.nmrAtoms]),
                            key=CcpnSorting.stringSortKey))

  @staticmethod
  def _getNmrResiduePeakCount(nmrResidue):
    l1 = [peak for atom in nmrResidue.nmrAtoms for peak in atom.assignedPeaks]
    return len(set(l1))

  def destroy(self):
    "Cleanup of self"
    if self._chainNotifier is not None:
      self._chainNotifier.unRegister()
    self._peaksNotifier.unRegister()

