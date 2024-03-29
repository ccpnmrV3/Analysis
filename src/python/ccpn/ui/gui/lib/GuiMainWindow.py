"""
This Module implements the main graphics window functionality
It works in concert with a wrapper object for storing/retrieving attibute values

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2020"
__credits__ = ("Ed Brooksbank, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license")
__reference__ = ("Skinner, S.P., Fogh, R.H., Boucher, W., Ragan, T.J., Mureddu, L.G., & Vuister, G.W.",
                 "CcpNmr AnalysisAssign: a flexible platform for integrated NMR analysis",
                 "J.Biomol.Nmr (2016), 66, 111-124, http://doi.org/10.1007/s10858-016-0060-y")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2020-02-12 20:44:58 +0000 (Wed, February 12, 2020) $"
__version__ = "$Revision: 3.0.1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: TJ Ragan $"
__date__ = "$Date: 2017-04-04 09:51:15 +0100 (Tue, April 04, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

#import datetime
import json
import os
import sys
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QSize
from ccpn.core.Project import Project
from ccpn.core.lib.ContextManagers import catchExceptions
from ccpn.ui.gui.widgets.MessageDialog import progressManager
from ccpn.util.Logging import getLogger
from ccpnmodel.ccpncore.lib.Io import Formats as ioFormats

from ccpn.util.Svg import Svg
from ccpn.ui.gui.lib.mouseEvents import SELECT, setCurrentMouseMode, getCurrentMouseMode
from ccpn.ui.gui.lib import GuiSpectrumDisplay
from ccpn.ui.gui.lib import GuiSpectrumView
from ccpn.ui.gui.lib import GuiStrip
from ccpn.ui.gui.lib import GuiPeakListView
from ccpn.ui.gui.lib.GuiWindow import GuiWindow

from ccpn.ui.gui.modules.MacroEditor import MacroEditor
from ccpn.ui.gui.widgets import MessageDialog
from ccpn.ui.gui.widgets.Action import Action
from ccpn.ui.gui.widgets.FileDialog import FileDialog
from ccpn.ui.gui.widgets.IpythonConsole import IpythonConsole
from ccpn.ui.gui.widgets.Menu import Menu, MenuBar, SHOWMODULESMENU, CCPNMACROSMENU, TUTORIALSMENU, PLUGINSMENU, CCPNPLUGINSMENU
from ccpn.ui.gui.widgets.SideBar import SideBar  #,SideBar
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.CcpnModuleArea import CcpnModuleArea
from ccpn.ui.gui.widgets.Splitter import Splitter
from ccpn.util.Common import uniquify
from ccpn.util import Logging
from ccpn.core.lib.ContextManagers import undoBlock, notificationEchoBlocking

from ccpn.core.lib.Notifiers import NotifierBase, Notifier
from ccpn.core.Peak import Peak
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication

#from ccpn.util.Logging import getLogger
#from collections import OrderedDict

from ccpn.ui.gui.widgets.DropBase import DropBase
from ccpn.ui.gui.lib.MenuActions import _openItemObject


# For readability there should be a class:
# _MainWindowShortCuts which (Only!) has the shortcut definitions and the callbacks to initiate them.
# The latter should all be private methods!
# For readability there should be a class:
# _MainWindowMenus which (Only!) has menu instantiations, the callbacks to initiate them, + relevant methods
# The latter should all be private methods!
#
# The docstring of GuiMainWindow should detail how this setup is

MAXITEMLOGGING = 4


class GuiMainWindow(GuiWindow, QtWidgets.QMainWindow):
    # inherits NotifierBase

    def __init__(self, application=None):

        # super(GuiMainWindow, self).__init__(parent=None)
        GuiWindow.__init__(self, application)
        QtWidgets.QMainWindow.__init__(self)

        # format = QtGui.QSurfaceFormat()
        # format.setSwapInterval(0)
        # QtGui.QSurfaceFormat.setDefaultFormat(format)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # Layout
        layout = self.layout()

        logger = Logging.getLogger()
        logger.debug('GuiMainWindow: layout: %s' % layout)

        if layout is not None:
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

        self.setGeometry(200, 40, 1100, 900)

        # connect a close event, cleaning up things as needed
        self.closeEvent = self._closeEvent
        # self.connect(self, QtCore.PYQT_SIGNAL('triggered()'), self._closeEvent)
        # self.triggered.connect(self._closeEvent)    # ejb

        # GuiWindow.__init__(self, application)
        self.application = application

        # Module area
        self.moduleArea = CcpnModuleArea(mainWindow=self)
        self._hiddenModules = CcpnModuleArea(mainWindow=self)
        self._hiddenModules.setVisible(False)

        logger.debug('GuiMainWindow.moduleArea: layout: %s' % self.moduleArea.layout)  ## pyqtgraph object
        self.moduleArea.setGeometry(0, 0, 1000, 800)
        # GST can't seem to do this with style sheets...
        self.moduleArea.setContentsMargins(0, 2, 2, 0)
        self.setCentralWidget(self.moduleArea)
        self._shortcutsDict = {}
        self.recordingMacro = False
        self._setupWindow()
        self._setupMenus()
        self._initProject()
        self._setShortcuts()
        self._setUserShortcuts(preferences=self.application.preferences, mainWindow=self)
        # Notifiers
        self._setupNotifiers()

        self.feedbackPopup = None
        self.updatePopup = None

        self.fileIcon = self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon, None, self)
        self.disabledFileIcon = self.makeDisabledFileIcon(self.fileIcon)

        # blank display opened later by the _initLayout if there is nothing to show otherwise
        # self.newBlankDisplay()
        self.pythonConsoleModule = None
        self.statusBar().showMessage('Ready')
        setCurrentMouseMode(SELECT)
        self.show()

        self._project._undo.undoChanged.add(self._undoChangeCallback)

        #   QtWidgets.QShortcut.installEventFilter(self)
        #   # for action in self.actions():
        #   #   print (action)
        #   # QtWidgets.QShortcut.activated.connect(self._activatedkeySequence)
        #     # action.activatedAmbiguously.connect(self._ambiguouskeySequence)
        #
        # def eventFilter(self, obj, event):
        #   # if event.type() == QtGui.QKeySequence.ExactMatch or event.type() == QtGui.QKeySequence.PartialMatch:
        #   #   try:
        #   #     print ('>>>key')
        #   #     self.statusBar().showMessage('key: %s' % str(event.key()))
        #   #     QtGui.QKeySequence.count = 0
        #   #
        #   #   except Exception as es:
        #   #     print (str(es))
        #
        #   if event.type() == QtCore.QEvent.KeyPress:
        #     print ('key: %s' % str(event.key()))
        #     return True
        #
        #   return False

        # install handler to resize when moving between displays
        self.window().windowHandle().screenChanged.connect(self._screenChangedEvent)

    def makeDisabledFileIcon(self, icon):
        return icon

    def _undoChangeCallback(self, message):

        amDirty = self._project._undo.isDirty()
        self.setWindowModified(amDirty)

        if not self._isTemporaryProject():
            self.setWindowFilePath(self.application.project.path)
        else:
            self.setWindowFilePath("")

        if self._isTemporaryProject():
            self.setWindowIcon(QtGui.QIcon())
        elif amDirty:
            self.setWindowIcon(self.disabledFileIcon)
        else:
            self.setWindowIcon(self.fileIcon)


    @pyqtSlot()
    def _screenChangedEvent(self, *args):
        self._screenChanged(*args)
        self.update()

    def _screenChanged(self, *args):
        getLogger().debug2('mainWindow screenchanged')
        project = self.application.project
        for spectrumDisplay in project.spectrumDisplays:
            for strip in spectrumDisplay.strips:
                strip.refreshDevicePixelRatio()

            # NOTE:ED - set pixelratio for extra axes
            if hasattr(spectrumDisplay, '_rightGLAxis'):
                spectrumDisplay._rightGLAxis.refreshDevicePixelRatio()
            if hasattr(spectrumDisplay, '_bottomGLAxis'):
                spectrumDisplay._bottomGLAxis.refreshDevicePixelRatio()

    @property
    def modules(self):
        "Return tuple of modules currently displayed"
        return tuple([m for m in self.moduleArea.modules.values()])

    def _setupNotifiers(self):
        """Setup notifiers connecting gui to current and project
        """
        # Marks
        self.setNotifier(self.application.project, [Notifier.CREATE, Notifier.DELETE, Notifier.CHANGE],
                         'Mark', GuiStrip._updateDisplayedMarks)
        # current notifiers
        self.setNotifier(self.application.current, [Notifier.CURRENT], 'strip', self._highlightCurrentStrip)
        self.setNotifier(self.application.current, [Notifier.CURRENT], 'peaks', GuiStrip._updateSelectedPeaks)
        self.setNotifier(self.application.current, [Notifier.CURRENT], 'integrals', GuiStrip._updateSelectedIntegrals)
        self.setNotifier(self.application.current, [Notifier.CURRENT], 'multiplets', GuiStrip._updateSelectedMultiplets)
        # Peaks
        # self.setNotifier(self.application.project, [Notifier.DELETE], 'Peak', GuiSpectrumDisplay._deletedPeak)
        # self.setNotifier(self.application.project, [Notifier.RENAME], 'NmrAtom', GuiPeakListView._updateAssignmentsNmrAtom)

    def _activatedkeySequence(self, ev):
        key = ev.key()
        self.statusBar().showMessage('key: %s' % str(key))

    def _ambiguouskeySequence(self, ev):
        key = ev.key()
        self.statusBar().showMessage('key: %s' % str(key))

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:

                # don't do anything on minimising
                pass

            elif event.oldState() & QtCore.Qt.WindowMinimized:

                # TODO:ED changeEvent: Normal/Maximised/FullScreen - call populate all modules
                pass

        event.ignore()

    def _initProject(self):
        """
        Puts relevant information from the project into the appropriate places in the main window.
        """
        #TODO:RASMUS: assure that isNew() and isTemporary() get added to Project; remove API calls
        isNew = self._apiWindow.root.isModified  # a bit of a hack this, but should be correct

        project = self.application.project
        path = project.path
        self.namespace['project'] = project
        self.namespace['runMacro'] = self.pythonConsole._runMacro

        msg = path + (' created' if isNew else ' opened')
        self.statusBar().showMessage(msg)
        msg2 = 'project = %sProject("%s")' % (('new' if isNew else 'open'), path)

        # write first console message to the console - not required
        # self.pythonConsole.writeConsoleCommand(msg2)

        self._fillRecentProjectsMenu()
        self.pythonConsole.setProject(project)
        self._updateWindowTitle()
        if hasattr(self.application.project._wrappedData.root, '_temporaryDirectory'):
            self.getMenuAction('Project->Archive').setEnabled(False)
        else:
            self.getMenuAction('Project->Archive').setEnabled(True)

    def _updateWindowTitle(self):
        """
        #CCPN INTERNAL - called in saveProject method of Framework
        """
        applicationName = self.application.applicationName
        version = self.application.applicationVersion

        #GST certainly on osx i would even remove the app name as it should be in the menu
        #GST switched order file name first its the most important info and on osx it
        # appears next to the proxy icon
        if not self._isTemporaryProject():
            filename = self.application.project.name
            windowTitle = '{} - {}[{}][*]'.format(filename, applicationName, version)
        else:
            windowTitle = '{}[{}][*]'.format(applicationName, version)

        self.setWindowTitle(windowTitle)

    def getMenuAction(self, menuString, topMenuAction=None):
        from ccpn.framework.Translation import translator

        if topMenuAction is None:
            topMenuAction = self._menuBar
        splitMenuString = menuString.split('->')
        splitMenuString = [translator.translate(text) for text in splitMenuString]
        if len(splitMenuString) > 1:
            topMenuAction = self.getMenuAction('->'.join(splitMenuString[:-1]), topMenuAction)
        for a in topMenuAction.actions():
            # print ('>>>', menuString, a.text())
            if a.text() == splitMenuString[-1]:
                return a.menu() or a
        raise ValueError('Menu item not found.')

    def searchMenuAction(self, menuString, topMenuAction=None):
        from ccpn.framework.Translation import translator

        found = None
        if topMenuAction is None:
            topMenuAction = self._menuBar
        splitMenuString = menuString.split('->')
        splitMenuString = [translator.translate(text) for text in splitMenuString]
        if len(splitMenuString) > 1:
            topMenuAction = self.getMenuAction('->'.join(splitMenuString[:-1]), topMenuAction)
        for a in topMenuAction.actions():
            # print ('>>>', menuString, a.text())
            if a.text() == splitMenuString[-1]:
                found = a.menu() if a.menu() else a
                break
            else:
                if a.menu():
                    found = self.searchMenuAction(menuString, topMenuAction=a.menu())
                    if found:
                        break
        return found

    def _setupWindow(self):
        """
        Sets up SideBar, python console and splitters to divide up main window properly.

        """
        self.namespace = {'application': self.application,
                          'current'    : self.application.current,
                          'preferences': self.application.preferences,
                          'redo'       : self.application.redo,
                          'undo'       : self.application.undo,
                          'get'        : self.application.get,

                          'ui'         : self.application.ui,
                          'mainWindow' : self,
                          'project'    : self.application.project,
                          'loadProject': self.application.loadProject,
                          # 'newProject' : self.application.newProject,
                          'info'       : getLogger().info,
                          'warning'    : getLogger().warning,
                          }
        self.pythonConsole = IpythonConsole(self)

        # create the sidebar
        self._sideBarFrame = Frame(self, setLayout=True)  # in this frame is inserted the search widget
        self._sideBarFrame.setContentsMargins(4, 2, 0, 0)

        # create a splitter for the sidebar
        self._sidebarSplitter = Splitter(self._sideBarFrame, horizontal=False)
        self._sidebarSplitter.setContentsMargins(0, 0, 0, 0)
        self._sideBarFrame.getLayout().addWidget(self._sidebarSplitter, 0, 0)  # must be inserted this way

        # create 2 more containers for the search bar and the results
        self.searchWidgetContainer = Frame(self._sideBarFrame, setLayout=True, grid=(1, 0))  # in this frame is inserted the search widget
        self.searchResultsContainer = Frame(self, setLayout=True)  # in this frame is inserted the search widget

        # create a SideBar pointing to the required containers
        self.sideBar = SideBar(parent=self, mainWindow=self,
                               searchWidgetContainer=self.searchWidgetContainer,
                               searchResultsContainer=self.searchResultsContainer)

        # insert into the splitter
        self._sidebarSplitter.insertWidget(0, self.sideBar)
        self._sidebarSplitter.insertWidget(1, self.searchResultsContainer)

        # GST resizing the splitter by hand causes problems so currently disable it!
        for i in range( self._sidebarSplitter.count()):
            self._sidebarSplitter.handle(i).setEnabled(False)

        # create a splitter to put the sidebar on the left
        self._horizontalSplitter = Splitter(horizontal=True)

        self._horizontalSplitter.addWidget(self._sideBarFrame)
        self._horizontalSplitter.addWidget(self.moduleArea)
        self.setCentralWidget(self._horizontalSplitter)

        self._temporaryWidgetStore = Frame(parent=self, showBorder=None, setLayout=False)
        self._temporaryWidgetStore.hide()

    def _setupMenus(self):
        """
        Creates menu bar for main window and creates the appropriate menus according to the arguments
        passed at startup.

        This currently pulls info on what menus to create from Framework.  Once GUI and Project are
        separated, Framework should be able to call a method to set the menus.
        """

        self._menuBar = self.menuBar()
        for m in self.application._menuSpec:
            self._createMenu(m)
        self._menuBar.setNativeMenuBar(self.application.preferences.general.useNativeMenus)

        self._fillRecentProjectsMenu()
        self._fillPredefinedLayoutMenu()
        self._fillRecentMacrosMenu()
        #TODO:ED needs fixing
        self._fillPluginsMenu()  # ejb - nothing to show, and crash anyway

        self._attachModulesMenuAction()
        self._attachCCPNMacrosMenuAction()
        self._attachTutorialsMenuAction()

    def _attachModulesMenuAction(self):
        # add a connect to call _fillModulesMenu when the menu item is about to show
        # so it is always up-to-date
        modulesMenu = self.searchMenuAction(SHOWMODULESMENU)
        modulesMenu.aboutToShow.connect(self._fillModulesMenu)

    def _attachCCPNMacrosMenuAction(self):
        # add a connect to call _fillCCPNMacrosMenu when the menu item is about to show
        # so it is always up-to-date
        modulesMenu = self.searchMenuAction(CCPNMACROSMENU)
        modulesMenu.aboutToShow.connect(self._fillCCPNMacrosMenu)

    def _attachTutorialsMenuAction(self):
        # add a connect to call _fillTutorialsMenu when the menu item is about to show
        # so it is always up-to-date
        modulesMenu = self.searchMenuAction(TUTORIALSMENU)
        modulesMenu.aboutToShow.connect(self._fillTutorialsMenu)

    def _createMenu(self, spec, targetMenu=None):
        menu = self._addMenu(spec[0], targetMenu)
        self._addMenuActions(menu, spec[1])

    def _addMenu(self, menuTitle, targetMenu=None):
        if targetMenu is None:
            targetMenu = self._menuBar
        if isinstance(targetMenu, MenuBar):
            menu = Menu(menuTitle, self)
            targetMenu.addMenu(menu)
        else:
            menu = targetMenu.addMenu(menuTitle)
        return menu

    def _storeShortcut(self, twoLetters, thecallable):
        if twoLetters is not None:
            twoLetters = twoLetters.replace(', ', '')
            twoLetters = twoLetters.lower()
            if twoLetters not in self._shortcutsDict:
                self._shortcutsDict[twoLetters] = thecallable
            else:
                alreadyUsed = self._shortcutsDict.get(twoLetters)
                getLogger().warning(" Ambiguous shortcut overload: %s. \n Assigning to: %s. \nAlready in use for: \n %s." %
                                    (twoLetters, thecallable, alreadyUsed))

    def _storeMainMenuShortcuts(self, actions):
        for action in actions:
            if len(action) == 3:
                name, thecallable, shortCutDefs = action
                kwDict = dict(shortCutDefs)
                twoLetters = kwDict.get('shortcut')
                self._storeShortcut(twoLetters, thecallable)

    def _addMenuActions(self, menu, actions):
        self._storeMainMenuShortcuts(actions)
        for action in actions:
            if len(action) == 0:
                menu.addSeparator()
            elif len(action) == 2:
                if callable(action[1]):
                    menu.addAction(Action(self, action[0], callback=action[1]))
                else:
                    self._createMenu(action, menu)
            elif len(action) == 3:
                kwDict = dict(action[2])
                for k, v in kwDict.items():
                    if (k == 'shortcut') and v.startswith('⌃'):  # Unicode U+2303, NOT the carrot on your keyboard.
                        kwDict[k] = QKeySequence('Ctrl+{}'.format(v[1:]))
                menuAction = Action(self, action[0], callback=action[1], **kwDict)
                menu.addAction(menuAction)

    def _isTemporaryProject(self):
        """Return true if the project is temporary, i.e., not saved or updated.
        """
        apiProject = self._project._wrappedData.root
        return hasattr(apiProject, '_temporaryDirectory')

    def _queryCloseProject(self, title, phrase):

        apiProject = self._project._wrappedData.root
        if hasattr(apiProject, '_temporaryDirectory'):
            return True

        if apiProject.isProjectModified():
            ss = ' and any changes will be lost'
        else:
            ss = ''
        result = MessageDialog.showYesNo(title,
                                         'Do you really want to %s project (current project will be closed%s)?' % (phrase, ss))

        return result

    def _loadProjectSingleTry(self, projectDir):
        """Load/Reload project after load dialog.
        """
        from ccpn.ui.gui.widgets.MessageDialog import showWarning

        try:
            project = self.application.loadProject(projectDir)

            if project:
                project._mainWindow.sideBar.buildTree(project)
                project._mainWindow.show()
                QtWidgets.QApplication.setActiveWindow(project._mainWindow)

                # if the new project contains invalid spectra then open the popup to see them
                # badSpectra = [str(spectrum) for spectrum in project.spectra if not spectrum.isValidPath]
                badSpectra = []
                for spectrum in project.spectra:
                    valid = False
                    try:
                        valid = spectrum.isValidPath        # can raise error if None
                    except:
                        pass
                    finally:
                        if not valid:
                            badSpectra.append(str(spectrum))

                if badSpectra:
                    showWarning('Spectrum file paths',
                                '''Detected invalid Spectrum file path(s) for: 
                                \n\t%s
                                
                                Use menu Spectrum-->Validate paths.. or "VP" shortcut to correct''' % '\n\t'.join(badSpectra)
                                )
                    # project.application.showValidateSpectraPopup(defaultSelected='invalid')
                    # project.save(createFallback=False, overwriteExisting=True)

                undo = self._project._undo
                if undo is not None:
                    undo.markClean()
                return project

            else:
                showWarning('Load Project', 'Error loading project')

        except Exception as es:
            raise ValueError("Error loading project: %s" %  str(es))

    def _loadProjectLastValid(self, projectDir):
        """Try and load a new project, if error try and load the last valid project.
        """
        lastValidProject = self.project.path
        lastProjectisTemporary = self._isTemporaryProject()

        # try and load the new project
        # try:
        project = self._loadProjectSingleTry(projectDir)
        if project:
            undo = self._project._undo
            if undo is not None:
                undo.markClean()
            return project

        # except Exception as es:
        #     MessageDialog.showError('loadProject', 'Error loading project:\n%s\n\n%s\n\nReloading last saved position.' % (str(projectDir), str(es)))
        #     Logging.getLogger().warning('Error loading project: %s - Reloading last saved position.' % str(projectDir))
        #
        #     if not lastProjectisTemporary:
        #         # try and load the previous project (only one try)
        #         try:
        #             project = self._loadProjectSingleTry(lastValidProject)
        #             return project
        #
        #         except Exception as es:
        #             MessageDialog.showError('loadProject', 'Error loading last project:\n%s\n\n%s' % (str(lastValidProject), str(es)))
        #             Logging.getLogger().warning('Error loading last project: %s' % str(lastValidProject))
        #     else:
        #         # open a new project again
        #         project = self.application.newProject()
        #         project._mainWindow.sideBar.buildTree(project)
        #         project._mainWindow.show()
        #         QtWidgets.QApplication.setActiveWindow(project._mainWindow)
        #         return project

    def loadProject(self, projectDir=None):
        """
        Opens a loadProject dialog box if project directory is not specified.
        Loads the selected project.
        """
        result = self._queryCloseProject(title='Open Project', phrase='open another')
        lastValidProject = self.project.path

        project = None
        if result:
            if projectDir is None:
                dialog = FileDialog(self, fileMode=FileDialog.Directory, text="Open Project",
                                    acceptMode=FileDialog.AcceptOpen, preferences=self.application.preferences.general)
                projectDir = dialog.selectedFile()

            if projectDir:
                # try and load the new project
                try:
                    project = self._loadProjectLastValid(projectDir)

                except Exception as es:
                    MessageDialog.showError('loadProject', 'Fatal error loading project:\n%s' % str(projectDir))
                    Logging.getLogger().warning('Fatal error loading project: %s' % str(projectDir))

                # try:
                #     project = self._loadProject(projectDir)
                #
                # except Exception as es:
                #     MessageDialog.showError('loadProject', 'Fatal error loading project:\n%s\nReloading last saved position.' % str(projectDir))
                #     Logging.getLogger().warning('Fatal error loading project: %s - Reloading last saved position.' % str(projectDir))
                #
                #     # try and load the previous project (only one try)
                #     try:
                #         project = self._loadProject(lastValidProject)
                #
                #     except Exception as es:
                #         MessageDialog.showError('loadProject', 'Fatal error loading previous project:\n%s' % str(lastValidProject))
                #         Logging.getLogger().warning('Fatal error loading previous project: %s' % str(lastValidProject))

        undo = self._project._undo
        if undo is not None:
            undo.markClean()
        return project

    def _fillRecentProjectsMenu(self):
        """
        Populates recent projects menu with 10 most recently loaded projects
        specified in the preferences file.
        """
        recentFileLocations = self.application._getRecentFiles()
        recentFileMenu = self.getMenuAction('Project->Open Recent')
        recentFileMenu.clear()
        for recentFile in recentFileLocations:
            # action = Action(self, text=recentFile, translate=False,
            #                callback=partial(self.application.loadProject, path=recentFile))

            action = Action(self, text=recentFile, translate=False,
                            callback=partial(self.loadProject, projectDir=recentFile))
            recentFileMenu.addAction(action)
        recentFileMenu.addSeparator()
        recentFileMenu.addAction(Action(recentFileMenu, text='Clear',
                                        callback=self.application.clearRecentProjects))

    def _fillPredefinedLayoutMenu(self):
        """
        Populates predefined Layouts
        """
        from ccpn.util import Layout
        from ccpn.framework.PathsAndUrls import predefinedLayouts

        userDefinedLayoutDirPath = self.application.preferences.general.get('userLayoutsPath')
        prelayouts = Layout._dictLayoutsNamePath(Layout._getPredefinedLayouts(predefinedLayouts))
        prelayoutMenu = self.getMenuAction('Project->Layout->Open pre-defined')
        prelayoutMenu.clear()
        for name, path in prelayouts.items():
            action = Action(self, text=name, translate=False,
                            callback=partial(self.application.restoreLayoutFromFile, path))
            prelayoutMenu.addAction(action)
        prelayoutMenu.addSeparator()
        userLayouts = Layout._dictLayoutsNamePath(Layout._getPredefinedLayouts(userDefinedLayoutDirPath))
        for name, path in userLayouts.items():
            action = Action(self, text=name, translate=False,
                            callback=partial(self.application.restoreLayoutFromFile, path))
            prelayoutMenu.addAction(action)
        prelayoutMenu.addSeparator()
        action = Action(self, text='Update', translate=False,
                        callback=self._fillPredefinedLayoutMenu)
        prelayoutMenu.addAction(action)

    def _fillMacrosMenu(self):
        """
        Populates recent macros menu with last ten macros ran.
        """
        #TODO: make sure that running a macro adds it to the prefs and calls this function

        recentMacrosMenu = self.getMenuAction('Macro->Run Recent')
        recentMacrosMenu.clear()

        from ccpn.framework.PathsAndUrls import macroPath as ccpnMacroPath

        try:
            ccpnMacros = os.listdir(ccpnMacroPath)
            ccpnMacros = [f for f in ccpnMacros if
                          os.path.isfile(os.path.join(ccpnMacroPath, f))]
            ccpnMacros = [f for f in ccpnMacros if f.split('.')[-1] == 'py']
            ccpnMacros = [f for f in ccpnMacros if not f.startswith('.')]
            ccpnMacros = [f for f in ccpnMacros if not f.startswith('_')]
            ccpnMacros = sorted(ccpnMacros)

            recentMacrosMenu.clear()
            for macro in ccpnMacros:
                action = Action(self, text=macro, translate=False,
                                callback=partial(self.runMacro,
                                                 macroFile=os.path.join(ccpnMacroPath, macro)))
                recentMacrosMenu.addAction(action)
            if len(ccpnMacros) > 0:
                recentMacrosMenu.addSeparator()
        except FileNotFoundError:
            pass

    def _fillRecentMacrosMenu(self):
        """
        Populates recent macros menu with last ten macros ran.
        TODO: make sure that running a macro adds it to the prefs and calls this function
        """
        recentMacrosMenu = self.getMenuAction('Macro->Run Recent')
        recentMacros = self.application.preferences.recentMacros
        if len(recentMacros) < 0:
            self._fillMacrosMenu()  #uses the default Macros

        else:
            recentMacros = recentMacros[-10:]
            recentMacrosMenu.clear()
            for recentMacro in sorted(recentMacros, reverse=True):
                action = Action(self, text=recentMacro, translate=False,
                                callback=partial(self.application.runMacro, macroFile=recentMacro))
                recentMacrosMenu.addAction(action)
            recentMacrosMenu.addSeparator()

        recentMacrosMenu.addAction(Action(recentMacrosMenu, text='Refresh',
                                          callback=self._fillRecentMacrosMenu))
        recentMacrosMenu.addAction(Action(recentMacrosMenu, text='Browse...',
                                          callback=self.application.runMacro))
        recentMacrosMenu.addAction(Action(recentMacrosMenu, text='Clear',
                                          callback=self.application.clearRecentMacros))

    def _addPluginSubMenu(self, Plugin):
        targetMenu = pluginsMenu = self.searchMenuAction(CCPNPLUGINSMENU)
        if '...' in Plugin.PLUGINNAME:
            package, name = Plugin.PLUGINNAME.split('...')
            try:
                targetMenu = self.getMenuAction(package, topMenuAction=pluginsMenu)
            except ValueError:
                targetMenu = self._addMenu(package, targetMenu=pluginsMenu)
        else:
            name = Plugin.PLUGINNAME
        action = Action(self, text=name, translate=False,
                        callback=partial(self.startPlugin, Plugin=Plugin))
        targetMenu.addAction(action)

    def _fillModulesMenu(self):
        modulesMenu = self.searchMenuAction(SHOWMODULESMENU)
        modulesMenu.clear()

        moduleSize = self.sideBar.size()
        visible = moduleSize.width() != 0 and moduleSize.height() != 0 and self.sideBar.isVisible()
        modulesMenu.addAction(Action(modulesMenu, text='Sidebar',
                                     checkable=True, checked=visible,
                                     # callback=partial(self._showSideBarModule, self._sideBarFrame, self, visible)))
                                     callback=partial(self._showSideBarModule, self._sideBarFrame, self, visible)))

        for module in self.moduleArea.ccpnModules:
            moduleSize = module.size()
            visible = moduleSize.width() != 0 and moduleSize.height() != 0

            modulesMenu.addAction(Action(modulesMenu, text=module.name(),
                                         checkable=True, checked=visible,
                                         callback=partial(self._showModule, module, self, visible)))

    def _showModule(self, module, modulesMenu, visible):
        try:
            menuItem = self.searchMenuAction(module.name())
            if menuItem:
                # if module.size().height() != 0 and module.size().width() != 0:  #menuItem.isChecked():    # opposite as it has toggled

                if visible:
                    module.setStretch(0, 0)
                else:
                    module.setStretch(1, 1)
        except Exception as es:
            Logging.getLogger().warning('Error expanding module: %s', module.name())

    def _fillCCPNMacrosMenu(self):
        modulesMenu = self.searchMenuAction(CCPNMACROSMENU)
        modulesMenu.clear()

        from ccpn.framework.PathsAndUrls import macroPath
        from os import walk

        # read the macros file directory - only top level
        macroFiles = []
        for (dirpath, dirnames, filenames) in walk(os.path.expanduser(macroPath)):
            macroFiles.extend([os.path.join(dirpath, filename) for filename in filenames])
            break

        for file in macroFiles:
            filename, fileExt = os.path.splitext(file)

            if fileExt == '.py':
                modulesMenu.addAction(Action(modulesMenu, text=os.path.basename(filename),
                                             callback=partial(self._runCCPNMacro, file, self)))

    def _runCCPNMacro(self, filename, modulesMenu):
        """Run a CCPN macro from the populated menu
        """
        try:
            self.application.runMacro(filename)

        except Exception as es:
            Logging.getLogger().warning('Error running CCPN Macro: %s' % str(filename))

    def _fillTutorialsMenu(self):
        modulesMenu = self.searchMenuAction(TUTORIALSMENU)
        modulesMenu.clear()

        from ccpn.framework.PathsAndUrls import tutorialsPath, beginnersTutorialPath, \
            backboneAssignmentTutorialPath, cspTutorialPath, solidStateTutorialPath

        from os import walk

        importantList = (('Beginners Tutorial', beginnersTutorialPath),
                         ('Backbone Tutorial', backboneAssignmentTutorialPath),
                         ('CSP Tutorial', cspTutorialPath),
                         ('Solid State Tutorial', solidStateTutorialPath))

        # add link to website videos
        modulesMenu.addAction(Action(modulesMenu, text='Video Tutorials',
                                     callback=self._showCCPNTutorials))
        modulesMenu.addSeparator()

        # add priority list for the important ones
        # and solid State

        # read the tutorials file directory - only top level
        tutorialsFiles = []
        for (dirpath, dirnames, filenames) in walk(os.path.expanduser(tutorialsPath)):
            tutorialsFiles.extend([os.path.join(dirpath, filename) for filename in filenames])
            break

        # add the main tutorials
        for text, file in importantList:
            filename, fileExt = os.path.splitext(file)

            if os.path.exists(file) and fileExt == '.pdf':
                modulesMenu.addAction(Action(modulesMenu, text=text,
                                             callback=partial(self._showTutorial, file, self)))

        modulesMenu.addSeparator()

        # add the remaining tutorials
        for file in sorted(tutorialsFiles, key=lambda ff: os.path.basename(ff)):
            filename, fileExt = os.path.splitext(file)

            if file not in [ff[1] for ff in importantList] and fileExt == '.pdf':
                modulesMenu.addAction(Action(modulesMenu, text=os.path.basename(filename),
                                             callback=partial(self._showTutorial, file, self)))

    def _showCCPNTutorials(self):
        from ccpn.framework.PathsAndUrls import ccpnVideos
        import webbrowser

        webbrowser.open(ccpnVideos)

    def _showTutorial(self, filename, modulesMenu):
        """Run a CCPN macro from the populated menu
        """
        try:
            self.application._systemOpen(filename)

        except Exception as es:
            Logging.getLogger().warning('Error opening tutorial: %s' % str(filename))

    def _showSideBarModule(self, module, modulesMenu, visible):
        try:
            # if module.size().height() != 0 and module.size().width() != 0:  #menuItem.isChecked():    # opposite as it has toggled

            if visible:
                module.hide()
            else:
                module.show()
        except Exception as es:
            Logging.getLogger().warning('Error expanding module: sideBar')

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:
            # Reset Mouse Mode
            mode = getCurrentMouseMode()
            if mode != SELECT:
                self.setMouseMode(SELECT)

    def _fillPluginsMenu(self):

        from ccpn.plugins import loadedPlugins

        pluginsMenu = self.searchMenuAction(CCPNPLUGINSMENU)
        pluginsMenu.clear()
        for Plugin in loadedPlugins:
            self._addPluginSubMenu(Plugin)
        pluginsMenu.addSeparator()
        pluginsMenu.addAction(Action(pluginsMenu, text='Reload',
                                     callback=self._reloadPlugins))

    def _reloadPlugins(self):
        from ccpn import plugins
        from importlib import reload

        reload(plugins)
        self._fillPluginsMenu()

    def startPlugin(self, Plugin):
        plugin = Plugin(application=self.application)
        self.application.plugins.append(plugin)
        if plugin.guiModule is None:
            if not plugin.UiPlugin:
                plugin.run()
                return
            else:
                from ccpn.ui.gui.modules.PluginModule import AutoGeneratedPluginModule

                pluginModule = AutoGeneratedPluginModule(mainWindow=self,
                                                         plugin=plugin,
                                                         application=self.application)  # ejb

        else:
            pluginModule = plugin.guiModule(name=plugin.PLUGINNAME, parent=self,
                                            plugin=plugin, application=self.application,
                                            mainWindow=self)
        plugin.ui = pluginModule
        if not pluginModule.aborted:
            self.application.ui.pluginModules.append(pluginModule)
            self.moduleArea.addModule(pluginModule)
        # TODO: open as pop-out, not as part of MainWindow
        # self.moduleArea.moveModule(pluginModule, position='above', neighbor=None)

    def _updateRestoreArchiveMenu(self):

        action = self.getMenuAction('Project->Restore From Archive...')
        action.setEnabled(bool(self.application._archivePaths()))

    def undo(self):
        self._project._undo.undo()

    def redo(self):
        self._project._undo.redo()

    def saveLogFile(self):
        pass

    def clearLogFile(self):
        pass

    def displayProjectSummary(self):
        info = MessageDialog.showInfo('Not implemented yet',
                                      'This function has not been implemented in the current version')

    def _closeWindowFromUpdate(self, event=None, disableCancel=True):
        # set the active window to mainWindow so that the quit popup centres correctly.
        self._closeWindow(event=event, disableCancel=disableCancel)
        os._exit(0)

    def _closeEvent(self, event=None, disableCancel=False):
        # set the active window to mainWindow so that the quit popup centres correctly.
        self._closeWindow(event=event, disableCancel=disableCancel)

    def _closeWindow(self, event=None, disableCancel=False):
        """
        Saves application preferences. Displays message box asking user to save project or not.
        Closes Application.
        """
        #GWV 20181214: moved to Framework._savePreferences
        #from ccpn.framework.PathsAndUrls import userPreferencesPath
        #prefPath = os.path.expanduser("~/.ccpn/v3settings.json")
        # directory = os.path.dirname(userPreferencesPath)
        # if not os.path.exists(directory):
        #     try:
        #         os.makedirs(directory)
        #     except Exception as e:
        #         self._project._logger.warning('Preferences not saved: %s' % (directory, e))
        #         return
        #
        # prefFile = open(userPreferencesPath, 'w+')
        # json.dump(self.application.preferences, prefFile, sort_keys=True, indent=4, separators=(',', ': '))
        # prefFile.close()

        undos = self.application.project._undo

        # set the active window to mainWindow so that the quit popup centres correctly.
        QtWidgets.QApplication.setActiveWindow(self)

        QUIT = 'Quit Program'
        MESSAGE = QUIT
        CANCEL = 'Cancel'
        QUIT_WITHOUT_SAVING =  'Quit without saving'
        SAVE_DATA = 'Save changes'
        DETAIL = "Do you want to save changes before quitting?"

        if disableCancel:
            reply = MessageDialog.showMulti(MESSAGE, DETAIL, [QUIT],checkbox=SAVE_DATA,okText=QUIT,
                                            checked=True)
        else:
            if undos.isDirty():
                reply = MessageDialog.showMulti(MESSAGE, DETAIL, [QUIT,CANCEL], checkbox=SAVE_DATA,okText=QUIT,
                                                checked=True)
            else:
                reply = QUIT_WITHOUT_SAVING

        if (QUIT in reply) and (SAVE_DATA in reply):
            if event:
                event.accept()
            # prefFile = open(userPreferencesPath, 'w+')
            # json.dump(self.application.preferences, prefFile, sort_keys=True, indent=4, separators=(',', ': '))
            # prefFile.close()

            self.application._savePreferences()
            success = self.application.saveProject()
            if success is True:
                # Close and clean up project
                self.deleteAllNotifiers()
                self.application._closeProject()  # close if saved
                QtWidgets.QApplication.quit()
                os._exit(0)

            else:
                if event:  # ejb - don't close the project
                    event.ignore()

        elif (QUIT in reply and SAVE_DATA not in reply) or (reply == QUIT_WITHOUT_SAVING):
            if event:
                event.accept()
            # prefFile = open(userPreferencesPath, 'w+')
            # json.dump(self.application.preferences, prefFile, sort_keys=True, indent=4, separators=(',', ': '))
            # prefFile.close()

            self.application._savePreferences()
            self.deleteAllNotifiers()
            self.application._closeProject()
            QtWidgets.QApplication.quit()
            os._exit(0)

        else:
            if event:
                event.ignore()

    def newMacroFromLog(self):
        """
        Displays macro editor with contents of the log.
        """
        editor = MacroEditor(self.moduleArea, self, "Macro Editor")
        with open(self.project._logger.logPath, 'r') as fp:
            l = fp.readlines()
        text = ''.join([line.strip().split(':', 6)[-1] + '\n' for line in l])
        editor.textBox.setText(text)

    #Framework owns the command, this part juts get the file to run
    # def runMacro(self, macroFile:str=None):
    #   """
    #   Runs a macro if a macro is specified, or opens a dialog box for selection of a macro file and then
    #   runs the selected macro.
    #   """
    #   if macroFile is None:
    #     dialog = FileDialog(self, fileMode=FileDialog.ExistingFile, text="Run Macro",
    #                         acceptMode=FileDialog.AcceptOpen, preferences=self.application.preferences.general)
    #     if os.path.exists(self.application.preferences.general.userMacroPath):
    #       dialog.setDirectory(self.application.preferences.general.userMacroPath)
    #     macroFile = dialog.selectedFile()
    #     if not macroFile:
    #       return
    #
    #   # Don't do this here
    #   # if os.path.isfile(macroFile):
    #   #   self.application.preferences.recentMacros.append(macroFile)
    #     # self._fillRecentMacrosMenu()
    #     self.pythonConsole._runMacro(macroFile)

    # GWV 20181127: commented not used
    # def _resetRemoveStripAction(self, strips):
    #     "Callback on current"
    #     for spectrumDisplay in self.spectrumDisplays:
    #         pass  # GWV: poor solution spectrumDisplay._resetRemoveStripAction()

    def _highlightCurrentStrip(self, data):
        "Callback on current to highlight the strip"
        previousStrip = data[Notifier.PREVIOUSVALUE]
        currentStrip = data[Notifier.VALUE]
        if previousStrip and not previousStrip.isDeleted:
            previousStrip._highlightStrip(False)
        if currentStrip and not currentStrip.isDeleted:
            currentStrip._highlightStrip(True)

    def printToFile(self):
        self.application.showPrintSpectrumDisplayPopup()

    # Not in use, Broken after refactoring to a new GL
    # def printToFile(self, spectrumDisplayOrStrip=None, path=None, width=800, height=800):
    #   #TODO:LUCA: Docstring needed
    #
    #   try:
    #     saveName = spectrumDisplayOrStrip.title+'.svg'
    #   except:
    #     saveName=''
    #
    #   current = self.application.current
    #   if not spectrumDisplayOrStrip:
    #     spectrumDisplayOrStrip = current.spectrumDisplay
    #   if not spectrumDisplayOrStrip and current.strip:
    #     spectrumDisplayOrStrip = current.strip.spectrumDisplay
    #   if not spectrumDisplayOrStrip and self.spectrumDisplays:
    #     spectrumDisplayOrStrip = self.spectrumDisplays[0]
    #   if spectrumDisplayOrStrip:
    #     if isinstance(spectrumDisplayOrStrip, GuiSpectrumDisplay):
    #       strips = spectrumDisplayOrStrip.strips
    #       if not strips:
    #         return
    #
    #     if not path:
    #       dialog = FileDialog(parent=self,
    #                           directory=saveName, fileMode=FileDialog.AnyFile, text='Print to File',
    #                           acceptMode=FileDialog.AcceptSave, preferences=self.application.preferences.general,
    #                           filter='SVG (*.svg)')
    #       path = dialog.selectedFile()
    #       if not path:
    #         return
    #       if not path.endswith(".svg"):
    #         path = path+".svg"
    #
    #     xCount = yCount = 1
    #     if isinstance(spectrumDisplayOrStrip, GuiSpectrumDisplay):
    #       if spectrumDisplayOrStrip.stripArrangement == 'X':
    #         yCount = len(strips)
    #       else:
    #         xCount = len(strips)
    #
    #     with Svg(path, xCount=xCount, yCount=yCount, width=width, height=height) as printer:
    #
    #       # box
    #       printer.writeLine(0, 0, width, 0)
    #       printer.writeLine(width, 0, width, height)
    #       printer.writeLine(width, height, 0, height)
    #       printer.writeLine(0, height, 0, 0)
    #
    #       xNumber = yNumber = 0
    #       if isinstance(spectrumDisplayOrStrip, GuiSpectrumDisplay):
    #         for n, strip in enumerate(strips):
    #           if spectrumDisplayOrStrip.stripArrangement == 'X':
    #             xOutputRegion = (0, width)
    #             yOutputRegion = (n * height / yCount, (n + 1) * height / yCount)
    #             yNumber = n
    #             if n > 0:
    #               # strip separator
    #               printer.writeLine(0, yOutputRegion[0], width, yOutputRegion[0])
    #           else:
    #             xOutputRegion = (n * width / xCount, (n + 1) * width / xCount)
    #             yOutputRegion = (0, height)
    #             xNumber = n
    #             if n > 0:
    #               # strip separator
    #               printer.writeLine(xOutputRegion[0], 0, xOutputRegion[0], height)
    #           printer.startRegion(xOutputRegion, yOutputRegion, xNumber, yNumber)
    #           strip._printToFile(printer)
    #       else:
    #         xOutputRegion = (0, width)
    #         yOutputRegion = (0, height)
    #         printer.startRegion(xOutputRegion, yOutputRegion)
    #         spectrumDisplayOrStrip._printToFile(printer)

    # _mouseMovedSignal = QtCore.pyqtSignal(dict)

    def _mousePositionMoved(self, strip: GuiStrip.GuiStrip, position: QtCore.QPointF):
        """ CCPN INTERNAL: called from ViewBox
        This is called when the mouse cursor position has changed in some strip
        :param strip: The strip the mouse cursor is hovering over
        :param position: The cursor position in "natural" (e.g. ppm) units
        :return: None
        """
        assert 0 == 1

    def _processDroppedItems(self, data):
        """Handle the dropped urls
        """
        # CCPN INTERNAL. Called also from module area and GuiStrip. They should have same behaviour
        # use an undoBlock, and ignore logging if 5 or more items
        # to stop overloading of the log
        objs = []
        urls = data.get('urls', [])
        if urls and len(urls) > 0:

            project = self._checkUrlsForProject(urls)

            if project:
                objs = self._processUrls(urls)

            else:
                with undoBlock():
                    getLogger().info('Handling urls...')
                    if len(urls) > MAXITEMLOGGING:
                        with notificationEchoBlocking():
                            objs = self._processUrls(urls)
                    else:
                        objs = self._processUrls(urls)

        return objs

    def _processPids(self, data, position=None, relativeTo=None):
        """Handle the urls passed to the drop event
        """
        # CCPN INTERNAL. Called also from CcpnModule and CcpnModuleArea. They should have same behaviour

        pids = data[DropBase.PIDS]
        if pids and len(pids) > 0:
            getLogger().debug('>>> dropped pids...')

            objs = [self.project.getByPid(pid) for pid in pids]

            # check whether a new spectrumDisplay is needed, check axisOrdering
            # add show popup for ordering if required
            from ccpn.ui.gui.popups.AxisOrderingPopup import checkSpectraToOpen

            checkSpectraToOpen(self, objs)

            _openItemObject(self, objs, position=position, relativeTo=relativeTo)

    def _checkUrlsForProject(self, urls):
        """Check whether there is a project in the dropped url list,
        and return the first project
        """
        for url in urls:
            getLogger().debug('>>> dropped: ' + str(url))

            dataType, subType, usePath = ioFormats.analyseUrl(url)
            if dataType == 'Project' and subType in (ioFormats.CCPN,
                                                     ioFormats.NEF,
                                                     ioFormats.NMRSTAR,
                                                     ioFormats.SPARKY):
                return url

    def _processUrls(self, urls):
        """Handle the dropped urls
        """
        # CCPN INTERNAL. Called also from module area and GuiStrip. They should have same behaviour

        objs = []
        # for url in data.get('urls', []):

        for url in urls:
            getLogger().debug('>>> dropped: ' + str(url))

            dataType, subType, usePath = ioFormats.analyseUrl(url)
            if subType == ioFormats.NMRSTAR:  # NMRStar file is available only as import of metadata not as stand alone project
                self.application._loadNMRStarFile(url)
                return objs

            if dataType == 'Project' and subType in (ioFormats.CCPN,
                                                     ioFormats.NEF,
                                                     ioFormats.SPARKY):

                try:
                    okToContinue = self._queryCloseProject(title='Load %s project' % subType,
                                                           phrase='create a new')
                    if okToContinue:
                        with progressManager(self, 'Loading project... ' + url):
                            obj = None
                            obj = self._loadProjectLastValid(url)

                except Exception as es:
                    MessageDialog.showError('Load Project', 'loadProject Error: %s' % str(es))
                    getLogger().warning('loadProject Error: %s' % str(es))

            else:
                # with progressManager(self.mainWindow, 'Loading data... ' + url):
                try:  #  Why do we need this try?
                    spectraPathsCount = len(ioFormats._searchSpectraPathsInSubDir(url))
                    askBeforeOpen_lenght = 20  # Ask user if want to open all (spectra) before start loading the full set.
                    if spectraPathsCount > askBeforeOpen_lenght:
                        okToOpenAll = MessageDialog.showYesNo('Load data', 'The directory contains multiple items (~%s).'
                                                                           ' Do you want to open all?' % str(spectraPathsCount))
                        if not okToOpenAll:
                            continue
                    with notificationEchoBlocking():
                        data = self.project.loadData(url)
                        if data:
                            objs.extend(data)

                except Exception as es:
                    MessageDialog.showError('Load Data', 'loadData Error: %s' % str(es))
                    getLogger().warning('loadData Error: %s' % str(es))
        return objs
