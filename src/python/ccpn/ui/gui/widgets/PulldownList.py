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
__author__ = "$Author: Geerten Vuister $"
__date__ = "$Date: 2017-04-11 22:04:47 +0100 (Tue, April 11, 2017) $"

#=========================================================================================
# Start of code
#=========================================================================================

from PyQt4 import QtCore, QtGui

from ccpn.ui.gui.widgets.Base import Base
from ccpn.ui.gui.widgets.Icon import Icon
from ccpn.ui.gui.widgets.Frame import Frame
from ccpn.ui.gui.widgets.Label import Label

# TBD: Cascading categories, prob via Menu

NULL = object()

class PulldownListCompoundWidget(Frame):
  """
  Compound class comprising a Label and a PulldownList, combined in a Frame
  """
  def __init__(self, parent, showBorder=False, orientation='left', minimumWidths=None, labelText='',
                             texts=None, objects=None, icons=None, callback=None, index=0, **kwds):
    """
    :param parent: parent widget
    :param showBorder: flag to display the border of Frame (True, False)
    :param orientation: flag to determine the orientation of the labelText relative to the pulldown widget.
                        Allowed values: 'left', 'right', 'top', 'bottom'
    :param minimumWidths: tuple of two values specifying the minimum width of the Label and Pulldown widget, respectively
    :param labelText: Text for the Label
    :param texts: list of (optional) text values for the Pulldown
    :param objects: list of (optional) objects for the Pulldown
    :param icons: list of (optional) icons for the Pulldown
    :param callback: callback for the Pulldown
    :param index: initially selected element of the Pulldown
    :param kwds: (optional) keyword, value pairs for the gridding
    """

    Frame.__init__(self, parent=parent, showBorder=showBorder, **kwds)

    self.label = Label(parent=self, text=labelText, vAlign='center')
    self.pulldownList = PulldownList(parent=self, texts=texts, objects=objects,
                                     icons=icons, callback=callback, index=index)

    if minimumWidths is not None and len(minimumWidths) == 2:
      self.label.setMinimumWidth(minimumWidths[0])
      self.pulldownList.setMinimumWidth(minimumWidths[1])

    layoutDict = dict(
      # grid positions for label and pulldown
      left =   [(0, 0), (0, 1)],
      right =  [(0, 1), (0, 0)],
      top =    [(0, 0), (1, 0)],
      bottom = [(1, 0), (0, 0)],
    )
    if orientation in layoutDict:
      lbl, pld = layoutDict[orientation]
      self.layout().addWidget(self.label, lbl[0], lbl[1])
      self.layout().addWidget(self.pulldownList, pld[0], pld[1])

    else:
      raise RuntimeError('Invalid parameter "orientation" (%s)' % orientation)


class PulldownList(QtGui.QComboBox, Base):

  def __init__(self, parent, texts=None, objects=None,
               icons=None, callback=None, index=0, **kw):

    QtGui.QComboBox.__init__(self, parent)
    Base.__init__(self, **kw)
    
    self.text = None
    self.object = None
    self.texts = []
    self.objects = []
    
    # self.setIconSize(QtCore.QSize(22,22))

    PulldownList.setData(self, texts, objects, index, icons)
    self.setCallback(callback)
#    self.setStyleSheet("""QCombobox { padding: 0;}
#                          QCombobox QAbstractItemView::item {
#                           padding-top: 2px;
#                           padding-bottom: 2px;
#                           }
#                          """)
#    self.setMinimumWidth(100)
#    self.setMinimumHeight(18)
#    self.view().setMinimumHeight(18*3)
    self.setStyleSheet("""
    PulldownList {
      padding-top: 3px;
      padding-bottom: 3px;
      padding-left: 2px;
    }
    """)
    self.connect(self, QtCore.SIGNAL('currentIndexChanged(int)'), self._callback)

  def showPopup(self):
    super(PulldownList, self).showPopup()

  def currentObject(self):

    if self.objects:
      index = self.currentIndex()
      if index >= 0:
        return self.objects[index]

  def currentData(self):

    return (self.currentText(),self.currentObject())
    
  def select(self, item):
    # Works with an object or a text

    index = None
    
    if item in self.texts:
      index = list(self.texts).index(item)

    elif item in self.objects:
      index = list(self.objects).index(item)

    if index is not None:
      self.setCurrentIndex(index)

  def set(self, item):

    self.select(item)

  def setSelected(self, item, doCallback=False):

    print("ccpn.ui.gui.widgets.PulldownList.setSelected is depecated use; .select()")
    
    self.select(item)

  def setIndex(self, index):

    self.setCurrentIndex(index)
  
  def get(self):
    
    return self.currentObject()

  def getSelected(self):
  
    # print("ccpn.ui.gui.widgets.PulldownList.getSelected is depecated use; .currentData()")

    return self.currentData()

  def getObject(self):
    
    # print("ccpn.ui.gui.widgets.PulldownList.getObject is depecated use; .currentObject()")
    
    return self.currentObject()

  def getText(self):
    
    # print("ccpn.ui.gui.widgets.PulldownList.getText is depecated use; .currentText()")
   
    return self.currentText()

  def getSelectedIndex(self):
    
    # print("ccpn.ui.gui.widgets.PulldownList.getSelectedIndex is depecated use; .currentIndex()")

    return self.currentIndex()

  def setup(self):
    
    print("ccpn.ui.gui.widgets.PulldownList.setup is depecated use; .setData")

    return self.currentIndex()
 
  def setData(self, texts=None, objects=None, index=None, icons=None):

    texts = texts or []
    objects = objects or []

    self.texts = []
    self.objects = []
    self.icons = []
    
    n = len(texts)
    
    if objects:
      msg = 'len(texts) = %d, len(objects) = %d'
      assert n == len(objects), msg % (n, len(objects))
      
    else:
      objects = texts[:]
    
    if icons:
      while len(icons) < n:
        icons.append(None)
        
    else:
      icons = [None] * n
    
    self.clear()
    for i, text in enumerate(texts):
      self.addItem(text, objects[i], icons[i])
    
    if index is not None:  
      self.setCurrentIndex(index)

  def addItem(self, text, object=NULL, icon=None):
    
    if icon:
      QtGui.QComboBox.addItem(self, Icon(icon), text)
    else:
      QtGui.QComboBox.addItem(self, text)
    
    if object is NULL:
      object = text
    
    self.texts.append(text)  
    self.objects.append(object)

  def setItemText(self, index, text):
  
    QtGui.QComboBox.setItemText(self, index, text)
    
    self.text[index] = text
  
  def removeItem(self, index):
  
    QtGui.QComboBox.removeItem(self, index)
    
    if index is self.index:
      self.index = None
      self.text = None
      self.object = None
    
    self.texts.pop(index)
    self.objects.pop(index)
    
  def disable(self):

    self.setDisabled(True)

  def enable(self):

    self.setEnabled(True)
  
  def setCallback(self, callback):
    
    self.callback = callback

  def _callback(self, index):
    
    if index < 0:
      return
    self.index = index
    
    if self.objects:
      self.object = self.objects[index]
    else:
      self.object = None
    
    if self.callback:
      if self.objects:
        self.callback(self.objects[index])
      elif self.texts:
        self.callback(self.texts[index])

if __name__ == '__main__':

  from ccpn.ui.gui.widgets.Application import TestApplication
  from ccpn.ui.gui.widgets.BasePopup import BasePopup
  
  app = TestApplication()

  texts = ['Int','Float','String', '']
  objects = [int, float, str, 'Green']
  icons = [None, None, None, Icon(color='#008000')]

  def callback(object):
    print('callback', object)

  def callback2(object):
    print('callback2', object)

  popup = BasePopup(title='Test PulldownList')
  #popup.setSize(250,50)
  policyDict = dict(
    vAlign='top',
    hPolicy = 'expanding',
  )
  policyDict = dict(
    vAlign='top',
   # hAlign='left',
  )
  #policyDict = dict(
  #   hAlign='left',
  # )
  #policyDict = {}

  pulldownList = PulldownList(parent=popup, texts=texts, icons=icons,
                              objects=objects, callback=callback, grid=(0,0), **policyDict
                              )

  pulldownListwidget = PulldownListCompoundWidget(parent=popup, orientation='left', showBorder=True, minimumWidths=(150,100),
                                          labelText='test-label', texts=texts, icons=icons,
                                          objects=objects, callback=callback2, grid=(1,1),
                                          **policyDict )

  pulldownListwidget2 = PulldownListCompoundWidget(parent=popup, orientation='left', showBorder=True, minimumWidths=(150,100),
                                          labelText='test-label which is longer', texts=texts, icons=icons,
                                          objects=objects, callback=callback2, grid=(2,1),
                                           **policyDict )

  pulldownList.clearEditText()
  app.start()

