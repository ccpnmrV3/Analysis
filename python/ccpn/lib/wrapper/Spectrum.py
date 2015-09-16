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

from ccpncore.util.typing import Sequence

# NBNB TBD Surely we do not need one-line wrappers around API-level utilities
# If the utility is needed here and not in the API, should we not move the code here?

# NBNB TBD parameters need renaming to distinguish api and wrapper objects

def getPlaneData(spectrum:'Spectrum', position:Sequence=None, xDim:int=0, yDim:int=1):

  return spectrum._apiDataSource.getPlaneData(position=position, xDim=xDim, yDim=yDim)
  
def getSliceData(spectrum:'Spectrum', position:Sequence=None, sliceDim:int=0):

  return spectrum._apiDataSource.getSliceData(position=position, sliceDim=sliceDim)

# Complex and not currently used. Let us keep it out. RHF
# def getRegionData(spectrum:object, startPoint:Sequence, endPoint:Sequence):
#
#   return spectrum._apiDataSource.getRegionData(startPoint, endPoint)

def automaticIntegration(spectrum, spectralData):

  return spectrum._apiDataSource.automaticIntegration(spectralData)


def estimateNoise(spectrum):
  return spectrum._apiDataSource.estimateNoise()

