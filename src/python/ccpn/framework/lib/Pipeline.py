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
__modifiedBy__ = "$modifiedBy: Luca Mureddu $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:14 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: Luca Mureddu $"

__date__ = "$Date: 2017-04-07 10:28:42 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#====================================



class Pipeline(object):
  '''
  Pipeline class.

  '''


  def __init__(self, application=None, pipelineName=None, pipes=None ):
    self._kwargs = {}
    self.pipes = pipes
    self.inputData = set()
    self.queue = [] # Pipes to be ran
    self.finishedPipe = [] # Pipes already ran


    if application is not None:
      self.application = application
      self.current = self.application.current
      self.preferences = self.application.preferences
      self.ui = self.application.ui
      self.project = self.application.project
      try:
        self.mainWindow = self.ui.mainWindow
      except AttributeError:
        pass


  @property
  def pipes(self):
    return self._pipes

  @pipes.setter
  def pipes(self, pipes):
    '''
    '''

    if pipes is not None:
      allPipes = []
      for pipe in pipes:
          allPipes.append(pipe)
      self._pipes = allPipes
    else:
      self._pipes = []


  def runPipeline(self):
    '''Run all pipes in the specified order '''
    print('Running Pipeline')
    if len(self.queue)>0:
      for pipe in self.pipes:
        if pipe is not None:
          pipe.runPipe(self, pipe._kwargs)
          self.queue.remove(pipe)
          self.finishedPipe.append(pipe)

    print(' self.queue',  self.queue)
    print(' self.self.finishedPipe', self.finishedPipe)
