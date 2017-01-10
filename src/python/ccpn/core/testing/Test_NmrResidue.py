"""Test code for NmrResidue

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
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revisgion: 8885 $"

#=========================================================================================
# Start of code
#=========================================================================================
from ccpn.core.testing.WrapperTesting import WrapperTesting

class NmrStretchTest(WrapperTesting):

  # Path of project to load (None for new project
  projectPath = None

  def setUp(self):

    with self.initialSetup():
      self.chain = self.project.createChain(sequence='QWERTYIPASD', molType='protein',
                                            shortName='X')

  def test_connect_nmr_residues_1(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'GLY', 'CYS', 'GLN'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    self.assertEqual([x.id for x in nmrChain.nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL', '@-.@3.GLY', '@-.@4.CYS', '@-.@5.GLN', ])

    nmrResidues[0].connectPrevious(nmrResidues[1])
    self.assertEqual([x.id for x in nmrResidues[0].nmrChain.mainNmrResidues],
                     ['#2.@2.VAL', '#2.@1.ALA', ])
    self.assertEqual(nmrResidues[0].nextNmrResidue, None)
    self.assertEqual(nmrResidues[0].previousNmrResidue, nmrResidues[1])

    nmrResidues[-1].connectNext(nmrResidues[-2])
    self.assertEqual([x.id for x in nmrResidues[-1].nmrChain.mainNmrResidues],
                     ['#3.@5.GLN', '#3.@4.CYS', ])
    self.assertEqual(nmrResidues[-1].nextNmrResidue, nmrResidues[-2])
    self.assertEqual(nmrResidues[-1].previousNmrResidue, None)

    nmrResidues[2].connectNext(nmrResidues[-1])
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues[2].nmrChain.mainNmrResidues],
                     ['#3.@3.GLY', '#3.@5.GLN', '#3.@4.CYS', ])

    nmrResidues[2].connectPrevious(nmrResidues[0])

    stretch = nmrResidues[2].nmrChain.mainNmrResidues
    stretch[-2].deassign()
    self.assertEqual([x.id for x in stretch],
                     ['#3.@2.VAL', '#3.@1.ALA','#3.@3.GLY', '#3.@5.', '#3.@4.CYS', ])

    self.assertRaises(ValueError,  stretch[-1].connectNext, stretch[0])

  def test_connected_nmr_residues(self):
    nmrChain = self.project.newNmrChain()
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'GLY', 'CYS', 'GLN'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))

    with self.assertRaises(AttributeError):
      nmrChain.nmrResidues = nmrResidues
    self.assertRaises(ValueError, nmrResidues[2].connectNext, None)
    self.assertIs(nmrResidues[2].nextNmrResidue, None)
    self.assertIs(nmrResidues[2].previousNmrResidue, None)

  def test_disconnect_triplet_1(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[1].disconnectPrevious()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '#2.@2.VAL', '#2.@3.', ])

  def test_disconnect_triplet_2(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[2].disconnectPrevious()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '@-.@3.', ])

  def test_disconnect_triplet_3(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[0].disconnectNext()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '#2.@2.VAL', '#2.@3.', ])

  def test_disconnect_triplet_4(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[1].disconnectNext()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '@-.@3.', ])


  def test_disconnect_triplet_5(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[0].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '#2.@2.VAL', '#2.@3.', ])


  def test_disconnect_triplet_6(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[1].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL', '@-.@3.', ])
    self.assertEquals([x.id for x in self.project.nmrChains], ['@-'])


  def test_disconnect_triplet_7(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[2].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '@-.@3.', ])


  def test_disconnect_double(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[0].disconnectNext()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL'])

  def test_disconnect_midchain_1(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'SER', None, 'ILE'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[1].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL', '#2.@3.SER', '#2.@4.', '#2.@5.ILE' ])

  def test_disconnect_midchain_2(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'SER', None, 'ILE'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[2].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '@-.@3.SER', '#3.@4.', '#3.@5.ILE' ])

  def test_disconnect_midchain_3(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'SER', None, 'ILE'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[3].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.SER', '@-.@4.', '@-.@5.ILE' ])

  def test_disconnect_midchain_4(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'SER', None, 'ILE'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[2].disconnectNext()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.SER', '#3.@4.', '#3.@5.ILE' ])

  def test_disconnect_midchain_5(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'SER', None, 'ILE'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    nmrChain.mainNmrResidues = nmrResidues
    nmrResidues[2].disconnectPrevious()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#3.@1.ALA', '#3.@2.VAL', '#2.@3.SER', '#2.@4.', '#2.@5.ILE' ])


  def test_disconnect_nmr_residues_2(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'GLY', 'CYS', 'GLN'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))

    nmrChain.mainNmrResidues = nmrResidues
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.GLY', '#2.@4.CYS', '#2.@5.GLN', ])

    nmrResidues[3].disconnectPrevious()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#3.@1.ALA', '#3.@2.VAL', '#3.@3.GLY', '#2.@4.CYS', '#2.@5.GLN', ])


  def test_disconnect_nmr_residues_3(self):
    nmrChain0 = self.project.fetchNmrChain(shortName='@-')
    nmrChain = self.project.newNmrChain(isConnected=True)
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'GLY', 'CYS', 'GLN'):
      nmrResidues.append(nmrChain0.fetchNmrResidue(residueType=residueType))
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL', '@-.@3.GLY', '@-.@4.CYS', '@-.@5.GLN', ])

    nmrChain.mainNmrResidues = nmrResidues
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.GLY', '#2.@4.CYS', '#2.@5.GLN', ])

    nmrResidues[-1].disconnectNext()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.GLY', '#2.@4.CYS', '#2.@5.GLN', ])

    nmrResidues[-1].disconnectPrevious()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '#2.@3.GLY', '#2.@4.CYS', '@-.@5.GLN'])

    nmrResidues[2].disconnect()
    self.assertEqual([x.id for x in nmrResidues],
                     ['#2.@1.ALA', '#2.@2.VAL', '@-.@3.GLY', '@-.@4.CYS', '@-.@5.GLN'])

    nmrResidues[1].disconnectPrevious()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrResidues],
                     ['@-.@1.ALA', '@-.@2.VAL', '@-.@3.GLY', '@-.@4.CYS', '@-.@5.GLN'])
    self.assertEqual([x.id for x in self.project.nmrChains], ['@-'])

  def test_disconnect_nmr_residue_triplet(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    nmrResidues = []
    for residueType in ('TRP', 'THR', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    self.assertEqual([x.id for x in sorted(nmrChain.mainNmrResidues)],
                     ['@-.@1.TRP', '@-.@2.THR', '@-.@3.', ])

    nmrChain2 = self.project.newNmrChain(isConnected=True)
    nmrChain2.mainNmrResidues = reversed(nmrResidues)
    self.assertEqual([x.id for x in sorted(nmrChain2.nmrResidues)],
                     ['#2.@3.',  '#2.@2.THR', '#2.@1.TRP',])

    nmrChain2.mainNmrResidues[1].disconnect()
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in nmrChain.nmrResidues],
                     ['@-.@1.TRP', '@-.@2.THR', '@-.@3.', ])

  def test_disconnect_nmr_residue_triplet2(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    nmrResidues = []
    for residueType in ('TRP', 'THR', None):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    self.assertEqual([x.id for x in nmrChain.mainNmrResidues],
                     ['@-.@1.TRP', '@-.@2.THR', '@-.@3.', ])

    nmrChain2 = self.project.newNmrChain(isConnected=True)
    nmrChain2.mainNmrResidues = reversed(nmrResidues)
    self.assertEqual([x.id for x in sorted(nmrChain2.nmrResidues)],
                     ['#2.@3.',  '#2.@2.THR', '#2.@1.TRP',])

    nmrChain2.mainNmrResidues[1].moveToNmrChain(nmrChain)
    self.undo.undo()
    self.undo.redo()
    self.assertEqual([x.id for x in sorted(nmrChain.nmrResidues)],
                     ['@-.@1.TRP', '@-.@2.THR', '@-.@3.', ])

  def test_assigning_connected_stretch(self):
    nmrChain = self.project.newNmrChain(isConnected=True)
    residues = self.chain.residues
    nmrResidues = []
    for residueType in ('ALA', 'VAL', 'GLY', 'CYS', 'GLN'):
      nmrResidues.append(nmrChain.fetchNmrResidue(residueType=residueType))
    #
    # self.assertRaises(ValueError,  nmrResidues[1].assignTo, chainCode=nmrChain.shortName,
    #                   sequenceCode=nmrResidues[2])

    nmrResidues[0].residue = residues[5]

    self.assertRaises(ValueError,  nmrChain.assignConnectedResidues, residues[3])

    self.assertRaises(ValueError,  nmrChain.assignConnectedResidues, residues[-2])

    nmrChain.assignConnectedResidues(residues[1])
    assignedNmrChain = self.project.getByPid('NC:X')

    mergedResidue = nmrResidues[1].assignTo(chainCode=residues[2].chain.shortName,
                                            sequenceCode=residues[2].sequenceCode,
                                            mergeToExisting=True)
    self.assertIs(mergedResidue, nmrResidues[2])
    self.undo.undo()
    self.assertEqual([x.id for x in sorted(self.project.getByPid('NC:X').nmrResidues)],
                     ['X.2.TRP', 'X.3.GLU', 'X.4.ARG', 'X.5.THR', 'X.6.TYR',])
    self.undo.redo()
    self.assertEqual([x.id for x in sorted(self.project.getByPid('NC:X').nmrResidues)],
                     ['X.3.GLU', 'X.4.ARG', 'X.5.THR', 'X.6.TYR',])


class NmrResidueTest(WrapperTesting):

  # Path of project to load (None for new project
  projectPath = 'CcpnCourse2c'

  def test_reassign_attributes(self):
    nchain = self.project.getByPid('NC:A')
    nchain0 = self.project.getByPid('NC:@-')

    nr1, nr2 = sorted(nchain.nmrResidues)[8:10]
    res1 = nr1.residue
    res2 = nr2.residue
    res3 = sorted(self.project.chains[0].residues)[2]
    nr3 = res3.nmrResidue
    nr2.residue = None
    self.assertEqual(nr2.longPid, "NmrResidue:A.@2.ARG")
    target =  self.project.getByPid('NR:A.2.LYS')
    target.rename('.LYS')
    self.assertEqual(target.longPid, "NmrResidue:A.@11.LYS")
    newNr = nchain0.newNmrResidue()
    self.assertEqual(newNr.longPid, "NmrResidue:@-.@89.")
    nr3.moveToNmrChain(nchain0)
    self.assertEqual(nr3.longPid, "NmrResidue:@-.3.GLU")
    newNr.residue = res3
    self.assertEqual(newNr.longPid, "NmrResidue:A.3.GLU")
    nchain.rename('X')
    self.assertEqual(nchain.longPid, "NmrChain:X")
    self.assertEqual(nr2.longPid, "NmrResidue:X.@2.ARG")
    newNr.rename(None)
    self.assertEqual(newNr.longPid, "NmrResidue:X.@89.")
    self.undo.undo()
    self.undo.redo()
    self.assertEqual(newNr.longPid, "NmrResidue:X.@89.")

  def test_rename(self):
    nchain = self.project.getByPid('NC:A')
    nr1, nr2 = sorted(nchain.nmrResidues)[8:10]
    self.assertEqual(nr1.id, "A.10.TYR")
    nr1.deassign()
    self.assertEqual(nr1.id, "A.@1.")
    nr1.rename('999')
    self.assertEqual(nr1.id, "A.999.")
    nr1.rename('999.ALA')
    self.assertEqual(nr1.id, "A.999.ALA")
    nr1.rename('998.VAL')
    self.assertEqual(nr1.id, "A.998.VAL")
    nr1.rename('.TYR')
    self.assertEqual(nr1.id, "A.@1.TYR")
    nr1.rename('997')
    nr1.moveToNmrChain()
    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertEqual(nr1.id, "@-.997.")

  def test_reassign(self):
    nchain = self.project.getByPid('NC:A')
    nr1, nr2 = sorted(nchain.nmrResidues)[8:10]
    self.assertEqual(nr1.id, "A.10.TYR")
    nr1 = nr1.assignTo(chainCode='A', sequenceCode=999)
    self.assertEqual(nr1.id, "A.999.TYR")
    nr1 = nr1.assignTo()
    # This is a no-op
    self.assertEqual(nr1.id, "A.999.TYR")

    with self.assertRaises(ValueError):
      nr2 = nr2.assignTo(sequenceCode=15)

    nr2 = nr2.assignTo(sequenceCode=515, residueType='XXX')
    self.assertEqual(nr2.id, 'A.515.XXX')
    obj = nchain.newNmrResidue(sequenceCode=777)
    self.assertEqual(obj.id, 'A.777.')

    self.assertTrue(len(nr1.nmrAtoms) == 2)

    self.assertRaises(ValueError,  nr2.assignTo, chainCode=nr1.nmrChain.shortName,
                      sequenceCode=nr1.sequenceCode, residueType=nr1.residueType,)

    nrx = nr2.assignTo(chainCode=nr1.nmrChain.shortName, sequenceCode=nr1.sequenceCode,
                       residueType=nr1.residueType, mergeToExisting=True)
    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertIs(nrx, nr1)
    self.assertIsNone(nr2._apiResonanceGroup)
    self.assertTrue(len(nr1.nmrAtoms) == 4)


  def test_fetchNmrResidue(self):
    nmrChain = self.project.fetchNmrChain()
    res1 = nmrChain.fetchNmrResidue(sequenceCode="127B", residueType="ALA")
    res2 = nmrChain.fetchNmrResidue(sequenceCode="127B", residueType="ALA")
    self.assertIs(res1, res2)
    obj = nmrChain.fetchNmrResidue(sequenceCode=515)
    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertEqual(obj.pid, 'NR:@%s.515.' % nmrChain._wrappedData.serial)

  def test_fetchEmptyNmrResidue(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    res1 = nmrChain.fetchNmrResidue(sequenceCode=None, residueType="ALA")
    sequenceCode = '@%s' % res1._wrappedData.serial
    self.assertEqual(res1.sequenceCode, sequenceCode)
    res2 = nmrChain.fetchNmrResidue(sequenceCode=sequenceCode)
    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertIs(res1, res2)

  def test_offsetNmrResidue(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    res1 = nmrChain.fetchNmrResidue(sequenceCode="127B", residueType="ALA")
    res2 = nmrChain.fetchNmrResidue(sequenceCode="127B-1", residueType="ALA")
    self.assertIs(res2._wrappedData.mainResonanceGroup, res1._wrappedData)
    res3 = nmrChain.fetchNmrResidue(sequenceCode="127B-1", residueType="ALA")
    self.assertIs(res2, res3)

    self.assertIs(res2.mainNmrResidue, res1)
    self.assertEqual(res1.offsetNmrResidues, (res2,))
    self.assertIs(res1.getOffsetNmrResidue(-1), res2)
    self.assertIsNone(res2.getOffsetNmrResidue(1))

    res1.delete()

    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertIsNone( res2._wrappedData)

  def test_get_by_serialName(self):
    nmrChain = self.project.fetchNmrChain(shortName='@-')
    res1 = nmrChain.fetchNmrResidue(sequenceCode=None, residueType="ALA")
    serialName = '@%s' % res1._wrappedData.serial
    res2 = nmrChain.fetchNmrResidue(sequenceCode=serialName)
    self.assertIs(res1, res2)
    res3 = nmrChain.fetchNmrResidue(sequenceCode=serialName + '+0')
    self.assertIs(res3._wrappedData.mainResonanceGroup, res1._wrappedData)
    # Undo and redo all operations
    self.undo.undo()
    self.undo.redo()
    self.assertIs(res3._wrappedData.mainResonanceGroup, res1._wrappedData)