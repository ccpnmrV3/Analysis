#from imp import reload

from PyQt4 import QtGui
from ccpncore.gui.Base import Base
from ccpncore.gui.Dock import CcpnDock
#from ccpncore.gui.Frame import Frame
#from ccpncore.gui.ButtonList import ButtonList
from ccpncore.gui.Label import Label
from ccpncore.gui.ListWidget import ListWidget
#from ccpncore.gui.PulldownList import PulldownList
from ccpncore.gui.Table import ObjectTable, Column
from ccpncore.gui.CheckBox import CheckBox
import assignmentBasic
#reload(assignmentBasic)
from ccpnmrcore.modules.assignmentModuleLogic import (get_all_nmrAtoms, nmrAtoms_for_peaks,
                                                      peaks_are_on_line, intersection_of_all,
                                                      same_axis_codes,
                                                      get_axisCode_for_peak_dimension,
                                                      get_isotope_code_for_peak_dimension,
                                                      get_shift_list_for_peak)


class AssignmentModule(CcpnDock, Base):
  '''Module that can be used to assign nmrAtoms
     to peaks.

  '''

  #_instance = None

  def __init__(self, parent=None, project=None, peaks=None, **kw):
    '''Init.

    '''

    #self.__class__._instance = self
    CcpnDock.__init__(self, name="Assignment Module")
    Base.__init__(self, **kw)
    self.project = project

    # If self.vertically_stacked = True, it looks
    # more like the v2 assignment Popup.
    self.vertically_stacked = False

    #self.infoLabel = Label(self, text='', grid=(0, 0))

    # Added an extra grid layout because the amount
    # od dimensions can not be known on forhand and in
    # this way it can shrink,
    self.selectionLayout = QtGui.QGridLayout()
    self.filterLayout = QtGui.QGridLayout()
    self.layout.addLayout(self.selectionLayout, 0, 0)
    self.layout.addLayout(self.filterLayout, 1, 0)
    self.selectionLayout.setRowMinimumHeight(0, 0)
    self.selectionLayout.setRowStretch(0, 0)
    self.selectionLayout.setRowStretch(1, 1)
    self.listWidgets = []
    self.objectTables = []

    # double tolerance
    self.doubleToleranceCheckbox = CheckBox(self, checked=False)
    self.doubleToleranceCheckbox.stateChanged.connect(self.update)
    doubleToleranceCheckboxLabel = Label(self, text="Double Tolerances:")
    self.filterLayout.addWidget(self.doubleToleranceCheckbox, 0, 1)
    self.filterLayout.addWidget(doubleToleranceCheckboxLabel, 0, 0)

    # intra-residual only
    self.intraCheckbox = CheckBox(self, checked=False)
    self.intraCheckbox.stateChanged.connect(self.update)
    intraCheckboxLabel = Label(self, text="Only Intra-residual:")
    self.filterLayout.addWidget(self.intraCheckbox, 1, 1)
    self.filterLayout.addWidget(intraCheckboxLabel, 1, 0)

    # Allow multiple peaks to be selected and assigned at same time.
    self.multiCheckbox = CheckBox(self, checked=True)
    self.multiCheckbox.stateChanged.connect(self.update)
    multiCheckboxLabel = Label(self, text="Allow multiple peaks:")
    self.filterLayout.addWidget(self.multiCheckbox, 2, 1)
    self.filterLayout.addWidget(multiCheckboxLabel, 2, 0)

    self.update()

  def update(self):
    '''Updates the whole widget, including recalculation
       of which nmrAtoms fit to the peaks.

    '''
    self.update_peaks()
    self.empty_all_tables_and_lists()
    if not self.peaks or not self.peaks_are_compatible():
      return
    self.create_enough_tables_and_lists()
    self.update_tables()
    self.update_assigned_nmrAtoms_list_widgets()

  def peaks_are_compatible(self):
    '''If multiple peaks are selected, a check is performed
       to determine whether assignment of corresponding
       dimensions of a peak allowed.

    '''

    if len(self.peaks) == 1:
      return True
    if not self.multiCheckbox.isChecked():
      print('Multiple peaks selected, not allowed.')
      return False
    dimensionalities = set([len(peak.position) for peak in self.peaks])
    if len(dimensionalities) > 1:
      print('Not all peaks have the same number of dimensions.')
      return False
    for dim in range(len(self.peaks[0].position)):
      if not same_axis_codes(self.peaks, dim):
        print('''The combination of axiscodes is different for multiple
                 selected peaks.''')
        return False
    return True

  def update_peaks(self, peaks=None):
    '''If argument peaks is not given, the currently
       selected peaks are returned. This method is mostly
       necessary because when no peaks are selected,
       self.project._appBase.current.peaks is None instead
       of an empty list. Which would probably be handier.

    '''
    if not peaks:
      self.peaks = self.project._appBase.current.peaks or []
    else:
      self.peaks = peaks

  def update_tables(self):
    '''Updates the tables indicating the different assignment
       possibilities of the peak dimensions.

    '''

    peaks = self.peaks
    doubleTolerance = self.doubleToleranceCheckbox.isChecked()
    intraResidual = self.intraCheckbox.isChecked()
    all_nmrAtoms = get_all_nmrAtoms(self.project)
    nmrAtoms_for_tables = nmrAtoms_for_peaks(peaks, all_nmrAtoms,
                                             doubleTolerance=doubleTolerance,
                                             intraResidual=intraResidual)
    Ndimensions = len(nmrAtoms_for_tables)

    for dim, objectTable, nmrAtoms in zip(range(Ndimensions),
                                          self.objectTables,
                                          nmrAtoms_for_tables):
      if peaks_are_on_line(peaks, dim):
        objectTable.setObjects(sorted(nmrAtoms) + [NEW])
        objectTable.show()
      else:
        objectTable.setObjects([NOL])

  def create_enough_tables_and_lists(self):
    '''Makes sure there are enough tables for the amount
       of dimensions of the currently selected peak(s).
       This method only runs when all peaks have the same
       amount of dimensions as is guaranteed by running
       peaks_are_compatible.

    '''

    Ndimensions = len(self.peaks[0].position)

    # Create extra tables if needed.
    for dim in range(len(self.objectTables), Ndimensions):
      self.create_empty_nmrAtoms_table(dim)

    # Hide tables that superceed the amount of peak dimensions.
    for objectTable in self.objectTables[Ndimensions:]:
      objectTable.setObjects([])
      objectTable.hide()

    for dim in range(len(self.listWidgets), Ndimensions):
      self.create_empty_listWidget(dim)

    for listWidget in self.listWidgets[Ndimensions:]:
      listWidget.clear()
      listWidget.hide()

  def empty_all_tables_and_lists(self):
    '''Quick erase of all present information.

    '''

    for objectTable in self.objectTables:
      objectTable.setObjects([])
    for listWidget in self.listWidgets:
      listWidget.clear()

  def create_empty_nmrAtoms_table(self, dim):
    '''Can be used to add a new table before setting
       the content.

    '''

    columns = [Column('NMR Atom', lambda nmrAtom: str(nmrAtom.pid)),
               Column('Delta', lambda nmrAtom: self.delta_shift(nmrAtom, dim))]

    #callback = lambda nmrAtom, row, column: self.assign_nmrAtom_to_dim(nmrAtom, dim)
    objectTable = ObjectTable(self, columns,
                              callback=None,
                              objects=[])

    # Needed to use this syntax because wanted double click not single.
    objectTable.doubleClicked.connect(lambda index: self.assign_nmrAtom_to_dim(dim))
    self.objectTables.append(objectTable)
    if self.vertically_stacked:
      self.selectionLayout.addWidget(objectTable, dim, 1)
    else:
      self.selectionLayout.addWidget(objectTable, 1, dim)
    objectTable.show()

  def create_empty_listWidget(self, dim):
    '''Can be used to add a new listWidget before
       setting the content.

    '''
    listWidget = ListWidget(self)
    self.listWidgets.append(listWidget)
    if self.vertically_stacked:
      self.selectionLayout.addWidget(listWidget, dim, 0)
    else:
      self.selectionLayout.addWidget(listWidget, 0, dim)

  def update_assigned_nmrAtoms_list_widgets(self):
    '''Update the listWidget showing which nmrAtoms
       are assigned to which peak dimensions. If multiple
       peaks are selected, only the assignment that they
       have in common are shown. Maybe this should be all
       assignments. You can see that at the peak anotation
       though.

    '''

    Ndimensions = len(self.peaks[0].position)
    required_heights = [23]

    for dim, listWidget in zip(range(Ndimensions), self.listWidgets):

      nmrAtoms = [set(peak.dimensionNmrAtoms[dim]) for peak in self.peaks]
      nmrAtoms = intersection_of_all(nmrAtoms)
      listWidget.addItems([str(a.pid) for a in nmrAtoms])
      listWidget.show()
      required_heights.append(listWidget.sizeHintForRow(0) * len(nmrAtoms))

    required_height = max(required_heights) + 5

    if not self.vertically_stacked:
      for listWidget in self.listWidgets:
        listWidget.setMaximumHeight(required_height)

  def getPeakName(self, peak, dim):
    '''Get the name of a peak, not used yet.'''

    if peak.dimensionNmrAtoms[dim].name is not None:
      return peak.dimensionNmrAtoms[dim].name
    else:
      return None

  def assign_nmrAtom_to_dim(self, dim):
    '''Assign the nmrAtom that is clicked on to the
       the corresponding dimension of the selected
       peaks.

    '''
    objectTable = self.objectTables[dim]
    nmrAtom = objectTable.getCurrentObject()

    if nmrAtom is NOL:
      return
    elif nmrAtom is NEW:
      isotope = get_isotope_code_for_peak_dimension(self.peaks[0], dim)
      nmrAtom = self.project.newNmrChain().newNmrResidue().newNmrAtom(isotopeCode=isotope)

    for peak in self.peaks:
      axisCode = get_axisCode_for_peak_dimension(peak, dim)

      if nmrAtom not in peak.dimensionNmrAtoms[dim]:
        newAssignments = peak.dimensionNmrAtoms[dim] + [nmrAtom]
        peak.assignDimension(axisCode, newAssignments)
    self.update()

  def delta_shift(self, nmrAtom, dim):
    '''Calculation of delta shift to add to the table.

    '''
    print(self.peaks)
    self.update_peaks()
    if not self.peaks:
      return ''

    if nmrAtom is NEW or nmrAtom is NOL:
      return ''

    deltas = []
    for peak in self.peaks:
      shiftList = get_shift_list_for_peak(peak)
      if shiftList:
        shift = shiftList.findChemicalShift(nmrAtom)
        if shift:
          position = peak.position[dim]
          deltas.append(abs(shift.value-position))
    average = sum(deltas)/len(deltas)
    return round(average, 3)


class New(object):
  '''Small 'fake' object to get a non-nmrAtom in the objectTable.
     Maybe this should be solved differently. It works well though.

  '''

  def __init__(self):
    self.pid = 'New NMR Atom'


class NotOnLine(object):
  '''Small 'fake' object to get a message the user in the assignment
     Table that a specific dimension can not be assigned in one go
     since the frequencies of the peaks in this dimension are not on
     one line (i.e. the C frequencies of the CA and CB in a strip for
     instance).
     Maybe this should be solved differently. It works well though.

  '''

  def __init__(self):
    self.pid = 'Multiple selected peaks not on line.'

NEW = New()
NOL = NotOnLine()
