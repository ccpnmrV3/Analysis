"""Module Documentation here

"""
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
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:00 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhfogh $"

__date__ = "$Date: 2016-05-16 06:41:02 +0100 (Mon, 16 May 2016) $"
#=========================================================================================
# Start of code
#=========================================================================================
from ccpn.core.testing.WrapperTesting import WrapperTesting

from ccpn.core.lib import Summary

spectrumName = 'N-NOESY-182'

class SummaryTest(WrapperTesting):

  # Path of project to load (None for new project
  projectPath = 'CcpnCourse3e'

  def test_assignedPeakCount(self):
    #import time; t0 = time.time()
    spectrum = self.project.getSpectrum(spectrumName)
    peakList = spectrum.peakLists[0]
    assert len(peakList.peaks) == 1148
    assert Summary.partlyAssignedPeakCount(peakList) == 1029
    assert Summary.fullyAssignedPeakCount(peakList) == 262
    # t1 = time.time();
    #print('time elapsed = %.1f' % (t1 - t0))

  def test_assignedAtomCount(self):
    #import time; t0 = time.time()
    chain = self.project.chains[0]
    assert len(chain.atoms) == 2493
    # print ('@~@~ assignable', Summary.assignableAtomCount(chain))
    # print ('@~@~ assigned', Summary.assignedAtomCount(chain))
    # print ('@~@~ assignments', [(x.chain, len([y for y in x.nmrAtoms if y.atom]))
    #                             for x in self.project.nmrChains])
    # assert Summary.assignableAtomCount(chain) == 1405
    # assert Summary.assignedAtomCount(chain) == 890
    # NB The new numbers reflect the program as working on 17/10/2016, without deep analysis.
    # Since there are 864 assigned NmrAtoms, the new numbers are clearly better.
    assert Summary.assignableAtomCount(chain) == 1293
    assert Summary.assignedAtomCount(chain) == 864
    #t1 = time.time(); print('time elapsed = %.1f' % (t1-t0))

