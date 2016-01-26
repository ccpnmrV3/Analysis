"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author: rhfogh $"
__date__ = "$Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__version__ = "$Revision: 7686 $"

#=========================================================================================
# Start of code
#=========================================================================================

from ccpncore.testing.CoreTesting import CoreTesting

from ccpncore.lib.spectrum import Peak

class PeakTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = 'CcpnCourse1b'

  def Test_PeakFit(self, *args, **kw):
    print('project.name = %s' % self.project.name)
    nmrProject = self.project.findFirstNmrProject()
    experiment = nmrProject.findFirstExperiment(name='HSQC')
    dataSource = experiment.findFirstDataSource()
    peakList = dataSource.findFirstPeakList()
    print('peakList = %s' % peakList)
    peak = peakList.findFirstPeak(serial=42)
    peaks = [peak]
    result = Peak.fitExistingPeaks(peaks, fitMethod='gaussian')
    print('result = %s' % result)
    
