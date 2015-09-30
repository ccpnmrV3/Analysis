"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================
from ccpn.testing.WrapperTesting import WrapperTesting
# from ccpncore.lib.spectrum import Spectrum as libSpectrum

class ChemicalShiftTest(WrapperTesting):

  # Path of project to load (None for new project
  projectPath = 'CcpnCourse2b'
    
  def test_rename_list(self):

    shiftList = self.project.chemicalShiftLists[0]

    self.assertEqual(shiftList.pid,'CL:ShiftList_2')
    self.assertEqual(shiftList.chemicalShifts[5].pid,'CS:ShiftList_2.A.63.ALA.H')
    shiftList.rename('RenamedList')
    self.assertEqual(shiftList.pid,'CL:RenamedList')
    self.assertEqual(shiftList.chemicalShifts[5].pid,'CS:RenamedList.A.63.ALA.H')


