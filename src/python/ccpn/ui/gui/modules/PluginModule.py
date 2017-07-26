"""

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:32:46 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: TJ Ragan $"
__date__ = "$Date: 2017-03-24 10:20:58 +0000 (Fri, March 24, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from functools import partial

from ccpn.ui.gui.modules.CcpnModule import CcpnModule
from ccpn.ui.gui.lib.GuiGenerator import generateWidget
from ccpn.ui.gui.lib.GuiGenerator import AUTOGEN_TAG
from ccpn.ui.gui.widgets.Button import Button

from ccpn.ui.gui.lib.GuiGenerator import generateWidget
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.CheckBox import CheckBox
from ccpn.ui.gui.widgets.ColourDialog import ColourDialog
from ccpn.ui.gui.widgets.DoubleSpinbox import DoubleSpinbox
from ccpn.ui.gui.widgets.Label import Label
from ccpn.ui.gui.widgets.LineEdit import LineEdit
from ccpn.ui.gui.widgets.PulldownList import PulldownList
from ccpn.ui.gui.widgets.RadioButton import RadioButton
from ccpn.ui.gui.widgets.RadioButtons import RadioButtons
from ccpn.ui.gui.widgets.Slider import Slider
from ccpn.ui.gui.widgets.Spinbox import Spinbox
from ccpn.ui.gui.widgets.TextEditor import TextEditor
from ccpn.ui.gui.widgets.FileDialog import LineEditButtonDialog
from ccpn.ui.gui.widgets.Widget import Widget
from ccpn.ui.gui.popups.PickPeaks1DPopup import ExcludeRegions
from ccpn.ui.gui.widgets.Icon import Icon

from ccpn.framework.lib.Pipeline import Pipeline
from ccpn.ui.gui.widgets.LinearRegionsPlot import TargetButtonSpinBoxes

commonWidgets =           {
                            CheckBox.__name__:              ('get',         'setChecked'),
                            ColourDialog.__name__:          ('getColor',    'setColor'  ),
                            DoubleSpinbox.__name__:         ('value',       'setValue'  ),
                            Label.__name__:                 ('get',         'setText'   ),
                            LineEdit.__name__:              ('get',         'setText'   ),
                            LineEditButtonDialog.__name__:  ('get',         'setText'   ),
                            PulldownList.__name__:          ('currentText', 'set'       ),
                            RadioButton.__name__:           ('get',         'set'       ),
                            RadioButtons.__name__:          ('get',         'set'       ),
                            Slider.__name__:                ('get',         'setValue'  ),
                            Spinbox.__name__:               ('value',       'set'       ),
                            TextEditor.__name__:            ('get',         'setText'   ),
                            TargetButtonSpinBoxes.__name__: ('get',         'setValues' ),
                            ExcludeRegions.__name__:        ('_getExcludedRegions', '_set' ),
                            # ObjectTable.__name__:    ('getSelectedRows',         '_highLightObjs'), works only with objs
                          }

# widgetGetters = {'CheckBox':      'get',  #returns Bool
#                  'PulldownList':  'get'               ,
#                  'LineEdit':      'get'               ,
#                  'Label':         'get'               ,
#                  'ListWidget':    'getSelectedObjects',  #returns list. Not Tested
#                  'DoubleSpinbox': 'value'             ,
#                  'Spinbox':       'value'             ,
#                  'Slider':        'get'               ,
#                  'RadioButton':   'isChecked'         ,  #returns Bool
#                  'RadioButtons':  'getIndex'          ,  # returns int index of the checked RB
#                  'ObjectTable':   'getSelectedObjects',  # returns int
#                  'TextEditor':    'getText'           ,
#                  'ToolButton':    'getText'           ,
#                  }

class PluginModule(CcpnModule):

  maxSettingsState = 2  # states are defined as: 0: invisible, 1: both visible, 2: only settings visible
  settingsPosition = 'top'

  className = 'PluginModule'

  def __init__(self, mainWindow=None, interactor=None, application=None):
    if interactor.settings is not None:
      self.includeSettingsWidget = True

    CcpnModule.__init__(self, mainWindow=mainWindow, name=interactor.PLUGINNAME)

    self.interactor = interactor
    self._kwargs = {}

    self._populateMainWidget()
    if interactor.settings is not None:
      self._populateSettingsWidget()


  def _populateMainWidget(self):
    generateWidget(self.interactor.params, widget=self.mainWidget, argsDict=self._kwargs)
    self.addRunButton()


  def _populateSettingsWidget(self):
    generateWidget(self.interactor.settings, widget=self.settingsWidget, argsDict=self._kwargs)


  def addRunButton(self):
    # TODO: put the run button at the bottom, not on the bottom right.
    self.goButton = Button(self.mainWidget, text='Run', callback=self._runButtonCallback)
    self.mainWidget.layout().addWidget(self.goButton)


  def _runButtonCallback(self):
    self.interactor.run(**self.widgetsState)


  def issueMessage(self, message):
    raise NotImplemented('Messages are not implemented yet.')

  @property
  def widgetsState(self):
    return self._widgetsState

  # @widgetsState.setter
  # def widgetsState(self, value):
  #   self._widgetsState = value

  @widgetsState.getter
  def widgetsState(self):
    '''return  {"variableName":"value"}  of all gui Variables  '''
    widgetsState = {}
    for varName, varObj in vars(self.mainWidget).items():
      if varObj.__class__.__name__ in commonWidgets.keys():
        try:  # try because widgets can be dynamically deleted
          widgetsState[varName] = getattr(varObj, commonWidgets[varObj.__class__.__name__][0])()
        except Exception as e:
          print('Error',e)
    self._kwargs = widgetsState
    return widgetsState


  def restoreWidgetsState(self, **widgetsState):
    'Restore the gui params. To Call it: _setParams(**{"variableName":"value"})  '
    for variableName, value in widgetsState.items():
      try:
        widget = getattr(self, str(variableName))
        if widget.__class__.__name__ in commonWidgets.keys():
          setWidget = getattr(widget, commonWidgets[widget.__class__.__name__][1])
          setWidget(value)
      except Exception as e:
        print('Impossible to restore %s value for %s.' % (variableName, self.interactor.PLUGINNAME), e)


##################### Qt Testing code #########################

from PyQt4 import QtGui
from pyqtgraph.dockarea import Dock, DockArea



class TestQt:
  def __init__(self, w=100, h=100):
    self.qtApp = QtGui.QApplication([])

    self.qtMainWindow = QtGui.QMainWindow()
    pgDockArea = DockArea()
    self.qtMainWindow.setCentralWidget(pgDockArea)

    # layout = QtGui.QGridLayout()      # ejb
    # layout.setContentsMargins(15,15,15,15)
    # self.qtMainWindow.setLayout(layout)

    self.pgDock = Dock("Dock", size=(w, h))
    pgDockArea.addDock(self.pgDock)


  def showWidget(self, widget):
    self.pgDock.addWidget(widget)

    self.qtMainWindow.show()
    QtGui.QApplication.exec_()


if __name__ == '__main__':
  from unittest.mock import Mock
  from ccpn.ui.gui.widgets.Application import TestApplication
  from ccpn.ui.gui.widgets.CcpnModuleArea import CcpnModuleArea

  qtTestHarness = TestQt()

  application = Mock()
  # application = TestApplication()
  application.colourScheme = 'light'  # HACK!!!
  qtTestHarness.qtApp._ccpnApplication = application

  interactor = Mock()
  interactor.PLUGINNAME = 'Test Plugin...Test'  # Same as above, but without checking
  interactor.params = [{'variable' : 'param1',
                        'value'    : ('Fast', 'Slow'),
                        'label'    : 'Param #1',
                        'default'  : 'Fast'},                        # List

                       {'variable' : 'param2',
                        'value'    : False,
                        'default'  : 0},                              # checkbox 0 unchecked 2 checked

                       {'variable': 'param3',
                        'value': (('White 1',False),('Red 2',True)),  #  RadioButtons
                        'default': 'Red 2'},

                       {'variable' : 'param4',
                        'value'    : ('0', '4'),
                        'default'  : 4},                                # List

                       {'variable' : 'param5',                         # Spinbox
                        'value'    : (0, 4),
                        'default'  : (3)},

                       {'variable' : 'param6',                         # Spinbox with default
                        'value'    : (0, 4),
                        'default'  : 2},

                       {'variable' : 'param7',                         # Spinbox with stepsize
                        'value'    : (0, 4),
                        'stepsize' : 2,
                        'default'  : 3},

                       {'variable' : 'param8',                         # Spinbox with default and stepsize
                        'value'    : (0, 4),
                        'stepsize' : 2,
                        'default'  : 2},

                       {'variable' : 'param9',                         # Double Spinbox
                        'value'    : (0., 1),
                        'default'  : 0.3},

                       {'variable' : 'param10',                         # Double Spinbox with default
                        'value'    : (0., 1.),
                        'default'  : 0.2},

                       {'variable' : 'param11',                         # Double Spinbox with stepsize
                        'value'    : (0., 1.),
                        'stepsize' : 0.1,
                        'default'  : 0.2},

                       {'variable' : 'param12',                         # Double Spinbox with default and stepsize
                        'value'    : (0., 1),
                        'stepsize' : 0.1,
                        'default'  : 0.2},

                       {'variable': 'param13',                         # LineEdit
                        'value': '',
                        'default'  :'param13'},

                       {'variable': 'param14',
                        'value': (('Ford', 'Focus'),                    # Mapped list
                                  ('BMW', '320'),
                                  ('Fiat', '500')
                                 ),
                        'default'  : 'Focus'},
                      ]
  interactor.settings = [{'variable' : 'param1s',
                          'value'    : ('Fast', 'Slow'),
                          'label'    : 'Param #1',
                          'default'  : 'Fast'},                        # List

                         {'variable' : 'param2s',
                          'value'    : False,
                          'default'  : 0},                              # checkbox 0 unchecked 2 checked

                         {'variable': 'param3s',
                          'value': (('White 1',False),('Red 2',True)),  #  RadioButtons
                          'default': 'Red 2'},

                         {'variable' : 'param4s',
                          'value'    : ('0', '4'),
                          'default'  : 4},                                # List

                         {'variable' : 'param5s',                         # Spinbox
                          'value'    : (0, 4),
                          'default'  : (3)},

                         {'variable' : 'param6s',                         # Spinbox with default
                          'value'    : (0, 4),
                          'default'  : 2},

                         {'variable' : 'param7s',                         # Spinbox with stepsize
                          'value'    : (0, 4),
                          'stepsize' : 2,
                          'default'  : 3},

                         {'variable' : 'param8s',                         # Spinbox with default and stepsize
                          'value'    : (0, 4),
                          'stepsize' : 2,
                          'default'  : 2},

                         {'variable' : 'param9s',                         # Double Spinbox
                          'value'    : (0., 1),
                          'default'  : 0.3},

                         {'variable' : 'param10s',                         # Double Spinbox with default
                          'value'    : (0., 1.),
                          'default'  : 0.2},

                         {'variable' : 'param11s',                         # Double Spinbox with stepsize
                          'value'    : (0., 1.),
                          'stepsize' : 0.1,
                          'default'  : 0.2},

                         {'variable' : 'param12s',                         # Double Spinbox with default and stepsize
                          'value'    : (0., 1),
                          'stepsize' : 0.1,
                          'default'  : 0.2},

                         {'variable': 'param13s',                         # LineEdit
                          'value': '',
                          'default'  :'param13'},

                         {'variable': 'param14s',
                          'value': (('Ford', 'Focus'),                    # Mapped list
                                    ('BMW', '320'),
                                    ('Fiat', '500')
                                   ),
                          'default'  : 'Focus'},
                      ]

  def run(**kwargs):
    print('Run clicked, ', kwargs)
  interactor.run = run

  qtTestHarness.qtMainWindow.moduleArea = CcpnModuleArea(mainWindow=qtTestHarness.qtMainWindow)
  # print('GuiMainWindow.moduleArea: layout:', qtTestHarness.qtMainWindow.moduleArea.layout)  ## pyqtgraph object
  # qtTestHarness.qtMainWindow.moduleArea.setGeometry(0, 0, 1000, 800)
  # qtTestHarness.qtMainWindow.setCentralWidget(qtTestHarness.qtMainWindow.moduleArea)

  # pluginModule = PluginModule(interactor)       # ejb - original line

  # pluginModule = PluginModule(interactor=interactor
  #                             , application=application
  #                             , mainWindow=application.mainWindow)

  pluginModule = PluginModule(mainWindow=qtTestHarness.qtMainWindow
                              , interactor=interactor
                              , application=application)
  qtTestHarness.showWidget(pluginModule)

  # pluginModule.show()
  # pluginModule.raise_()

  # application.start()
