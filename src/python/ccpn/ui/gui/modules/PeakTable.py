"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-07-07 16:32:46 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:41 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from PyQt5 import QtGui, QtWidgets
from ccpn.core.lib.Notifiers import Notifier
from ccpn.ui.gui.modules.CcpnModule import CcpnModule
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.PulldownListsForObjects import PeakListPulldown
# from ccpn.ui.gui.widgets.Table import ObjectTable, Column, ColumnViewSettings,  ObjectTableFilter
from ccpn.ui.gui.widgets.GuiTable import GuiTable
from ccpn.ui.gui.widgets.Column import ColumnClass, Column
from ccpn.ui.gui.widgets.Widget import Widget
from ccpn.core.lib.peakUtils import getPeakPosition, getPeakAnnotation, getPeakLinewidth
from ccpn.core.PeakList import PeakList
from ccpn.core.Peak import Peak
from ccpn.core.NmrAtom import NmrAtom
from ccpn.util.Logging import getLogger
from ccpn.ui.gui.widgets.DropBase import DropBase
from ccpn.ui.gui.lib.GuiNotifier import GuiNotifier
from ccpn.core.lib.CallBack import CallBack
from ccpn.ui.gui.widgets.ScrollArea import ScrollArea
from ccpn.ui.gui.widgets.Spacer import Spacer


logger = getLogger()

UNITS = ['ppm', 'Hz', 'point']


class PeakTableModule(CcpnModule):
    """
    This class implements the module by wrapping a PeakListTable instance
    """

    includeSettingsWidget = False
    maxSettingsState = 2
    settingsPosition = 'top'

    className = 'PeakTableModule'

    def __init__(self, mainWindow=None, name='Peak Table',
                 peakList=None, selectFirstItem=False):
        super().__init__(mainWindow=mainWindow, name=name)

        # Derive application, project, and current from mainWindow
        self.mainWindow = mainWindow
        self.application = mainWindow.application
        self.project = mainWindow.project
        self.current = mainWindow.application.current

        # mainWidget
        self.peakListTable = PeakListTableWidget(parent=self.mainWidget,
                                                 mainWindow=self.mainWindow,
                                                 moduleParent=self,
                                                 setLayout=True,
                                                 grid=(0, 0))

        if peakList is not None:
            self.selectPeakList(peakList)
        elif selectFirstItem:
            self.peakListTable.pLwidget.selectFirstItem()

        self.installMaximiseEventHandler(self._maximise, self._closeModule)

    @property
    def _dataFrame(self):
        if self.peakListTable._dataFrameObject:
            return self.peakListTable._dataFrameObject.dataFrame

    def _maximise(self):
        """
        Maximise the attached table
        """
        self.peakListTable._maximise()

    def selectPeakList(self, peakList=None):
        """
        Manually select a peakList from the pullDown
        """
        self.peakListTable._selectPeakList(peakList)

    def _closeModule(self):
        """Re-implementation of closeModule function from CcpnModule to unregister notification """
        self.peakListTable._close()
        super()._closeModule()

    def close(self):
        """
        Close the table from the commandline
        """
        self._closeModule()


class PeakListTableWidget(GuiTable):
    """
    Class to present a peakList Table
    """
    className = 'PeakListTable'
    attributeName = 'peakLists'

    positionsUnit = UNITS[0]  #default

    @staticmethod
    def _setFigureOfMerit(obj, value):
        """
        CCPN-INTERNAL: Set figureOfMerit from table
        Must be a floatRatio in range [0.0, 1.0]
        """
        # ejb - why is it blanking a notification here?
        # NmrResidueTable._project.blankNotification()

        # clip and set the figure of merit
        obj.figureOfMerit = min(max(float(value), 0.0), 1.0) if value else None
        # NmrResidueTable._project.unblankNotification()

    def __init__(self, parent=None, mainWindow=None, moduleParent=None, peakList=None, multiSelect=True,
                 actionCallback=None, selectionCallback=None, **kwds):
        """
        Initialise the table
        """
        # Derive application, project, and current from mainWindow
        self.mainWindow = mainWindow
        if mainWindow:
            self.application = mainWindow.application
            self.project = mainWindow.application.project
            self.current = mainWindow.application.current
        else:
            self.application = None
            self.project = None
            self.current = None

        PeakListTableWidget.project = self.project

        self.settingWidgets = None
        self._selectedPeakList = None
        kwds['setLayout'] = True  ## Assure we have a layout with the widget

        # strange, need to do this when using scrollArea, but not a Widget
        parent.getLayout().setHorizontalSpacing(0)
        self._widgetScrollArea = ScrollArea(parent=parent, scrollBarPolicies=('never', 'never'), **kwds)
        self._widgetScrollArea.setWidgetResizable(True)
        self._widget = Widget(parent=self._widgetScrollArea, setLayout=True)
        self._widgetScrollArea.setWidget(self._widget)
        self._widget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)

        row = 0
        self.spacer = Spacer(self._widget, 5, 5,
                             QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed,
                             grid=(row, 0), gridSpan=(1, 1))

        row += 1
        gridHPos = 0
        self.pLwidget = PeakListPulldown(parent=self._widget,
                                         mainWindow=self.mainWindow,
                                         grid=(row, gridHPos), gridSpan=(1, 1),
                                         showSelectName=True,
                                         minimumWidths=(0, 100),
                                         sizeAdjustPolicy=QtWidgets.QComboBox.AdjustToContents,
                                         callback=self._pulldownPLcallback)

        ## create widgets for selection of position units
        gridHPos += 1
        self.posUnitPulldownLabel = Label(parent=self._widget, text=' Position Unit', grid=(row, gridHPos))
        gridHPos += 1
        self.posUnitPulldown = PulldownList(parent=self._widget, texts=UNITS, callback=self._pulldownUnitsCallback, grid=(row, gridHPos))

        row += 1
        self.spacer = Spacer(self._widget, 5, 5,
                             QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed,
                             grid=(row, gridHPos + 1), gridSpan=(1, 1))
        self._widgetScrollArea.setFixedHeight(35)  # needed for the correct sizing of the table

        #TODO: this dhould be part of the definitions; extracted from there and paased to the
        #TODO constructor of the GuiTable module.
        self._hiddenColumns = ['Pid', 'Spectrum', 'PeakList', 'Id', 'HeightError', 'VolumeError']

        self.dataFrameObject = None
        selectionCallback = self._selectionCallback if selectionCallback is None else selectionCallback
        actionCallback = self._actionCallback if actionCallback is None else actionCallback

        super().__init__(parent=parent,
                            mainWindow=self.mainWindow,
                            dataFrameObject=None,
                            setLayout=True,
                            autoResize=True, multiSelect=multiSelect,
                            actionCallback=actionCallback,
                            selectionCallback=selectionCallback,
                            grid=(3, 0), gridSpan=(1, 6))
        self.moduleParent = moduleParent

        self.tableMenu.addAction('Copy Peaks...', self._copyPeaks)

        ## populate the table if there are peaklists in the project
        if peakList is not None:
            self._selectPeakList(peakList)

        self.setTableNotifiers(tableClass=PeakList,
                               rowClass=Peak,
                               cellClassNames=(NmrAtom, 'assignedPeaks'),
                               tableName='peakList', rowName='peak',
                               changeFunc=self._updateAllModule,
                               className=self.attributeName,
                               updateFunc=self._updateAllModule,
                               tableSelection='_selectedPeakList',
                               pullDownWidget=self.pLwidget,
                               callBackClass=Peak,
                               selectCurrentCallBack=self._selectOnTableCurrentPeaksNotifierCallback,
                               moduleParent=moduleParent)

        self.droppedNotifier = GuiNotifier(self,
                                           [GuiNotifier.DROPEVENT], [DropBase.PIDS],
                                           self._processDroppedItems)

    def _processDroppedItems(self, data):
        """CallBack for Drop events
        """
        # print('>>>_processDroppedItems')

        pids = data.get('pids', [])
        self._handleDroppedItems(pids, PeakList, self.pLwidget)

    def _getTableColumns(self, peakList):
        """Add default columns  plus the ones according with peakList.spectrum dimension
        format of column = ( Header Name, value, tipText, editOption)
        editOption allows the user to modify the value content by doubleclick
        """

        columnDefs = []

        # Serial column
        columnDefs.append(('#', 'serial', 'Peak serial number', None, None))
        columnDefs.append(('Pid', lambda pk: pk.pid, 'Pid of the Peak', None, None))
        columnDefs.append(('_object', lambda pk: pk, 'Object', None, None))

        columnDefs.append(('Spectrum', lambda pk: pk.peakList.spectrum.id, 'Spectrum containing the Peak', None, None))
        columnDefs.append(('PeakList', lambda pk: pk.peakList.serial, 'PeakList containing the Peak', None, None))
        columnDefs.append(('Id', lambda pk: pk.serial, 'Peak serial', None, None))

        # Assignment column
        for i in range(peakList.spectrum.dimensionCount):
            assignTipText = 'NmrAtom assignments of peak in dimension %s' % str(i + 1)
            columnDefs.append(
                    ('Assign F%s' % str(i + 1), lambda pk, dim=i: getPeakAnnotation(pk, dim), assignTipText, None, None)
            )

        # # Expanded Assignment columns
        # for i in range(peakList.spectrum.dimensionCount):
        #     assignTipText = 'NmrAtom assignments of peak in dimension %s' % str(i + 1)
        #     columnDefs.append(('Assign F%s' % str(i + 1), lambda pk, dim=i: self._getNmrChain(pk, dim), assignTipText, None, None))
        #     columnDefs.append(('Assign F%s' % str(i + 1), lambda pk, dim=i: self._getSequenceCode(pk, dim), assignTipText, None, None))
        #     columnDefs.append(('Assign F%s' % str(i + 1), lambda pk, dim=i: self._getResidueType(pk, dim), assignTipText, None, None))
        #     columnDefs.append(('Assign F%s' % str(i + 1), lambda pk, dim=i: self._getAtomType(pk, dim), assignTipText, None, None))

        # Peak positions column
        for i in range(peakList.spectrum.dimensionCount):
            positionTipText = 'Peak position in dimension %s' % str(i + 1)
            columnDefs.append(
                    ('Pos F%s' % str(i + 1),
                               lambda pk, dim=i, unit=self.positionsUnit: getPeakPosition(pk, dim, unit),
                               positionTipText, None, '%0.3f')
            )

        # linewidth column TODO remove hardcoded Hz unit
        for i in range(peakList.spectrum.dimensionCount):
            linewidthTipTexts = 'Peak line width %s' % str(i + 1)
            columnDefs.append(
                    ('LW F%s (Hz)' % str(i + 1), lambda pk, dim=i: getPeakLinewidth(pk, dim), linewidthTipTexts,
                     None, '%0.3f')
            )

        # height column
        heightTipText = 'Magnitude of spectrum intensity at peak center (interpolated), unless user edited'
        columnDefs.append(('Height', lambda pk: pk.height if pk.height else 'None', heightTipText, None, None))
        columnDefs.append(('HeightError', lambda pk: pk.heightError, 'Error of the height', None, None))

        # volume column
        volumeTipText = 'Integral of spectrum intensity around peak location, according to chosen volume method'
        columnDefs.append(('Volume', lambda pk: pk.volume if pk.volume else 'None', volumeTipText, None, None))
        columnDefs.append(('VolumeError', lambda pk: pk.volumeError, 'Error of the volume', None, None))

        # figureOfMerit column
        figureOfMeritTipText = 'Figure of merit'
        columnDefs.append(('Merit', lambda pk: pk.figureOfMerit, figureOfMeritTipText,
                           lambda pk, value: self._setFigureOfMerit(pk, value), None)
        )

        # comment column
        commentsTipText = 'Textual notes about the peak'
        columnDefs.append(('Comment', lambda pk: self._getCommentText(pk), commentsTipText,
                           lambda pk, value: self._setComment(pk, value), None)
        )

        return ColumnClass(columnDefs)

    ##################   Updates   ##################

    def _maximise(self):
        """Refresh the table on a maximise event
        """
        self._updateTable()

    def _updateAllModule(self, data=None):
        """Updates the table and the settings widgets
        """
        self._updateTable()

    def _updateTable(self, useSelectedPeakList=True, peaks=None, peakList=None):
        """Display the peaks on the table for the selected PeakList.
        Obviously, If the peak has not been previously deleted and flagged isDeleted
        """

        # print('>>>PeakTable _updateTable', repr(self))

        # self.setObjectsAndColumns(objects=[], columns=[]) #clear current table first
        self._selectedPeakList = self.project.getByPid(self.pLwidget.getText())

        if useSelectedPeakList:
            if self._selectedPeakList:

                self.populateTable(rowObjects=self._selectedPeakList.peaks,
                                   columnDefs=self._getTableColumns(self._selectedPeakList),
                                   selectedObjects=self.current.peaks)

                # self.project.blankNotification()
                # self._dataFrameObject = self.getDataFrameFromList(table=self,
                #                                                   buildList=self._selectedPeakList.peaks,
                #                                                   colDefs=self._getTableColumns(self._selectedPeakList),
                #                                                   hiddenColumns=self._hiddenColumns)
                #
                # # populate from the Pandas dataFrame inside the dataFrameObject
                # self.setTableFromDataFrameObject(dataFrameObject=self._dataFrameObject)
                # self._highLightObjs(self.current.peaks)
                # self.project.unblankNotification()

            else:
                self.clear()
        else:
            if peaks:
                if peakList:

                    self.populateTable(rowObjects=peaks,
                                       columnDefs=self._getTableColumns(peakList),
                                       selectedObjects=self.current.peaks)

                    # self.project.blankNotification()
                    # self._dataFrameObject = self.getDataFrameFromList(table=self,
                    #                                                   buildList=peaks,
                    #                                                   colDefs=self._getTableColumns(peakList),
                    #                                                   hiddenColumns=self._hiddenColumns)
                    #
                    # # populate from the Pandas dataFrame inside the dataFrameObject
                    # self.setTableFromDataFrameObject(dataFrameObject=self._dataFrameObject)
                    # self._highLightObjs(self.current.peaks)
                    # self.project.unblankNotification()

            else:
                self.clear()

        # if useSelectedPeakList:
        #   if self._selectedPeakList is not None:
        #     peaks = [peak for peak in self._selectedPeakList.peaks if not peak.isDeleted]
        #     self.setObjectsAndColumns(objects=peaks, columns=self._getTableColumns(self._selectedPeakList))
        #     self._selectOnTableCurrentPeaks(self.current.peaks)
        #   else:
        #     self.setObjects([]) #if not peaks, make the table empty
        # else: #set only specific peak of a peakList
        #   if peaks is not None:
        #     self.setObjectsAndColumns(objects=peaks, columns=self._getTableColumns(self._selectedPeakList))
        #     self._selectOnTableCurrentPeaks(self.current.peaks)
        #   else:
        #     self.setObjects([]) #if not peaks, make the table empty

    def _selectPeakList(self, peakList=None):
        """Manually select a PeakList from the pullDown
        """
        # print('>>>PeakTable _selectPeakList', repr(self))

        if peakList is None:
            # logger.warning('select: No PeakList selected')
            # raise ValueError('select: No PeakList selected')
            self.pLwidget.selectFirstItem()
        else:
            if not isinstance(peakList, PeakList):
                logger.warning('select: Object is not of type PeakList')
                raise TypeError('select: Object is not of type PeakList')
            else:
                for widgetObj in self.pLwidget.textList:
                    if peakList.pid == widgetObj:
                        self._selectedPeakList = peakList
                        self.pLwidget.select(self._selectedPeakList.pid)

    ##################   Widgets callbacks  ##################

    def _getPullDownSelection(self):
        return self.pLwidget.getText()

    # def _selectPullDown(self, value):
    #     self.pLwidget.select(value)
    #     self._updateTable()

    # def displayTableForPeakList(self, peakList):
    #     """Display the table for all NmrResidue's of nmrChain
    #     """
    #     # print('>>>displayTableForPeakList')
    #
    #     self.pLwidget.select(peakList.pid)
    #     self._updateTable(peaks=peakList.peaks)

    def _actionCallback(self, data, *args):
        """If current strip contains the double clicked peak will navigateToPositionInStrip
        """

        # print('>>>_actionCallback')

        from ccpn.ui.gui.lib.Strip import navigateToPositionInStrip, _getCurrentZoomRatio

        # multiselection table will return a list of objects
        objs = data[CallBack.OBJECT]
        if not objs:
            return
        if isinstance(objs, (tuple, list)):
            peak = objs[0]
        else:
            peak = objs

        if self.current.strip is not None:
            validPeakListViews = [pp.peakList for pp in self.current.strip.peakListViews if isinstance(pp.peakList, PeakList)]

            if peak and peak.peakList in validPeakListViews:
                widths = None

                if peak.peakList.spectrum.dimensionCount <= 2:
                    widths = _getCurrentZoomRatio(self.current.strip.viewRange())
                navigateToPositionInStrip(strip=self.current.strip,
                                          positions=peak.position,
                                          axisCodes=peak.axisCodes,
                                          widths=widths)
        else:
            logger.warning('Impossible to navigate to peak position. Set a current strip first')

    def _selectionCallback(self, data, *args):
        """
        set as current the selected peaks on the table
        """
        # print('>>>PeakTable _selectionCallback', repr(self))
        peaks = data[CallBack.OBJECT]
        if peaks is None:
            self.current.clearPeaks()
        else:
            self.current.peaks = peaks

    def _pulldownUnitsCallback(self, unit):
        # update the table with new units
        self._setPositionUnit(unit)
        self._updateAllModule()

    def _pulldownPLcallback(self, data):
        # print('>>>PeakTable _pulldownPLcallback', repr(self))

        self._updateAllModule()

    def _copyPeaks(self):
        from ccpn.ui.gui.popups.CopyPeaksPopup import CopyPeaks

        popup = CopyPeaks(parent=self.mainWindow, mainWindow=self.mainWindow)
        self._selectedPeakList = self.project.getByPid(self.pLwidget.getText())
        if self._selectedPeakList is not None:
            spectrum = self._selectedPeakList.spectrum
            popup._selectSpectrum(spectrum)
            popup._selectPeaks(self.current.peaks)
        popup.exec()
        popup.raise_()

    ##################   Notifiers callbacks  ##################

    # def _peakListNotifierCallback(self, data):
    #   '''Refreshs the table only if the peakList involved in the notification is the one displayed '''
    #   if self._selectedPeakList is not None:
    #     self.pLwidget.select(self._selectedPeakList.pid) #otherwise automatically reset from the compoundWidget pulldown notifiers
    #
    #   peakList = data['object']
    #   if self._selectedPeakList != peakList:
    #     return
    #   else:
    #     self._updateAllModule()

    # def _peakNotifierNotifierCallback(self, data):
    #   '''Callback for peak notifier. Refresh the table only if the peak belongs to the peakList displayed
    #   NB. Currently impossible to register and trigger the notifier dynamically for only the peaks in the peakList displayed.
    #   This because when deleting a peakList or spectrum from the project, the process starts by deleting one by one the peak and triggering the peak notifier automatically and therefore refreshing the table,
    #   TODO: better notifier that if a parent object is deleted it suspends all the children notifiers.
    #  '''
    #   peak = data['object']
    #   if peak is not None:
    #     if self._selectedPeakList != peak.peakList:
    #       return
    #     else:
    #       self._updateAllModule()

    def _selectOnTableCurrentPeaksNotifierCallback(self, data):
        """
        Callback from a notifier to highlight the peaks on the peak table
        :param data:
        """
        # print('>>>PeakTable _selectOnTableCurrentPeaksNotifierCallback', repr(self))

        currentPeaks = data['value']
        self._selectOnTableCurrentPeaks(currentPeaks)

    def _selectOnTableCurrentPeaks(self, currentPeaks):
        """
        Highlight the list of peaks on the table
        :param currentPeaks:
        """
        # print('>>>PeakTable _selectOnTableCurrentPeaks', repr(self))

        self.highlightObjects(currentPeaks)
        # if len(currentPeaks) > 0:
        #     self._highLightObjs(currentPeaks)
        # else:
        #     self.clearSelection()

    # @staticmethod
    # def _getCommentText(peak):
    #   if peak.comment == '' or not peak.comment:
    #     return ' '
    #   else:
    #     return peak.comment
    #
    # @staticmethod
    # def _setComment(peak, value):
    #   PeakListTableWidget.project.blankNotification()
    #   peak.comment = value
    #   PeakListTableWidget.project.unblankNotification()

    def _setPositionUnit(self, value):
        if value in UNITS:
            self.positionsUnit = value
