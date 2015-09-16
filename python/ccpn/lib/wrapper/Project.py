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
# import collections

import os
from ccpncore.lib.Io import Formats as ioFormats
from ccpncore.lib.Io import Fasta as fastaIo
from ccpncore.lib.spectrum.formats.Lookup import readXls,readCsv

# def loadSpectrum(project:object, filePath:str, reReadSpectrum:object=None):
#   """Load spectrum from file a filePath"""
#
#   if reReadSpectrum is not None:
#     # NBNB TBD Rasmus - this is clearly not working yet
#     raise NotImplementedError("reReadSpectrum parameter not implemented yet")
#
#   if reReadSpectrum:
#     spectrum = reReadSpectrum
#     # NBNB TBD BROKEN - spectrum is overwritten lower down
#   else:
#     dataSource = project._apiNmrProject.loadDataSource(filePath)
#     if not dataSource:
#       return None
#
#   # NBNB TBD BROKEN - dataSource is not always set.
#   spectrum = project._data2Obj[dataSource]
#
#   return spectrum

def loadData(project:'Project', path:str) -> (list,None):
  """Load data in url, determining type first."""

  dataType, subType, usePath = ioFormats.analyseUrl(path)

  # urlInfo is list of triplets of (type, subType, modifiedUrl),

  # e.g. ('Spectrum', 'Bruker', newUrl)
  if dataType is None:
    print("Skipping: file data type not recognised for %s" % usePath)
  elif not os.path.exists(usePath):
    print("Skipping: no file found at %s" % usePath)
  else:

    funcname = 'load' + dataType
    if funcname == 'loadProject':
      return [project.loadProject(usePath, subType)]

    # elif funcname == 'loadLookupFile':
    #   return project.loadLookupFile(usePath, subType)

    elif hasattr(project, funcname):
      pids = getattr(project, funcname)(usePath, subType)
      return pids
    else:
      print("Skipping: project has no function %s" % funcname)

  return None

# Data loaders and dispatchers
def loadSequence(project:"Project", path:str, subType:str) -> list:
  """Load sequence(s) from file into Wrapper project"""

  if subType == ioFormats.FASTA:
    sequences = fastaIo.parseFastaFile(path)
  else:
    raise ValueError("Sequence file type %s is not recognised" % subType)

  chains = []
  for sequence in sequences:
    chains.append(project.makeSimpleChain(sequence=sequence[1], compoundName=sequence[0],
                                          molType='protein'))
  #
  return chains

def loadProject(project:"Project", path:str, subType:str) -> "Project":
  """Load project from file into application and return the new project"""

  if subType == ioFormats.CCPN:
    return project._appBase.loadProject(path)
  else:
    raise ValueError("Sequence file type %s is not recognised" % subType)

def loadSpectrum(project:"Project", path:str, subType:str) -> list:
  """Load spectrum from file into application"""

  apiDataSource = project._wrappedData.loadDataSource(path, subType)
  if apiDataSource is None:
    return []
  else:
    return [project._data2Obj[apiDataSource]]

#
#
def loadLookupFile(project:None, path:str, subType:str, ):
  """Load data from a look-up file, csv or xls ."""

  if subType == ioFormats.CSV:
    readCsv(project, path=path)

  elif subType == ioFormats.XLS:
    readXls(project, path=path)




