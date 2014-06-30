import os

moduleDoc = '''"""Module Documentation here

"""
'''

template='''#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date: 2014-06-04 18:13:10 +0100 (Wed, 04 Jun 2014) $"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Geerten Vuister"
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
'''

excludeFiles = {'__init__.py'}
excludeDirs = {'api', 'apiDoc', 'xml'}
suffixMatch = '.py'

startMatchCount = 3
endMatchCount = 3

templateLines = template.split('\n')
startMatch = '\n'.join(templateLines[:startMatchCount])
endMatch = '\n'.join(templateLines[-endMatchCount:])

curDir = os.getcwd()
thisFile = os.path.join(curDir, __file__)

def updateFile(fileName):

  #print('HERE100', fileName)
  #print('HERE200', startMatch)
  #print('HERE201', endMatch)
  fp = open(fileName, 'rU')
  data = fp.read()
  fp.close()
  #print('HERE202', endMatch[:1000])
  n1 = data.find(startMatch)
  n2 = data.find(endMatch)
  #print('HERE203', n1)
  #print('HERE204', n2)
  #import sys; sys.exit()
  if n1 >= 0 and n2 > n1: # have a match
    data = data[:n1] + template + data[n2+len(endMatch):]
  else:
    data = moduleDoc + template + data
  fp = open(fileName, 'w')
  data = fp.write(data)
  fp.close()

def visitDirectory(directory):

  relFiles = os.listdir(directory)
  for relFile in relFiles:
    absFile = os.path.join(directory, relFile)
    if os.path.isfile(absFile) and absFile != thisFile:
      if relFile.endswith(suffixMatch) and relFile not in excludeFiles:
        updateFile(absFile)
    elif os.path.isdir(absFile):
      if relFile not in excludeDirs:
        visitDirectory(absFile)
      
if __name__ == '__main__':

  visitDirectory(curDir)
