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

class SubstanceTest(WrapperTesting):

  # Path of project to load (None for new project)
  projectPath = None

  def test_simple_create(self):
    substance1 = self.project.newSimpleSubstance('MolComp1', userCode='userCode',smiles=':-)')
    print ("@~@~", substance1, type(substance1), substance1.id, type(substance1.id))
    self.assertEqual(substance1.id, 'MolComp1.std')
    self.assertEqual(substance1.smiles, ':-)')
    self.assertEqual(substance1.substanceType, 'Molecule')

    substance2 = self.project.newSimpleSubstance('Cell1', substanceType='Cell', labeling='moxy',
                                                 smiles=':-)')
    self.assertEqual(substance2.id, 'Cell1.moxy')
    self.assertEqual(substance2.smiles, None)
    self.assertEqual(substance2.substanceType, 'Cell')
    

