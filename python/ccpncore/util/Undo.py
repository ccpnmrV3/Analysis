"""General undo handle supporting undo/redo stack
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

from functools import partial
from collections import deque

def deleteAll(objects):
  """Delete each object in objects - utility for undoing multi-object creation functions"""
  for obj in objects:
    obj.delete()


def deleteAllApiObjects(objsToBeDeleted):
  """Delete all API objects in set, together.
  Does NOT look for additional deletes or do any checks. Programmer beware!!!
  Does NOT do undo handling, as it is designed to be used within the Undo machinery"""

  for obj in objsToBeDeleted:
    if (obj.__dict__.get('isDeleted')):
      raise ValueError("""%s: deleteAllApiObjects
       called on deleted object""" % obj.qualifiedName
      )

  for obj in objsToBeDeleted:
    for notify in obj.__class__._notifies.get('preDelete', ()):
      notify(obj)

  for obj in objsToBeDeleted:
    obj._singleDelete(objsToBeDeleted)

  # doNotifies
  for obj in objsToBeDeleted:
    for notify in obj.__class__._notifies.get('delete', ()):
      notify(obj)


def resetUndo(memopsRoot, maxWaypoints=20, maxOperations=10000,
              debug:bool=False):
  """Set or reset undo stack, using passed-in parameters.
  NB setting either parameter to 0 removes the undo stack."""

  undo = memopsRoot._undo
  if undo is not None:
    undo.clear()

  if maxWaypoints and maxOperations:
    memopsRoot._undo = Undo(maxWaypoints=maxWaypoints, maxOperations=maxOperations,
                            debug=debug)
  else:
   memopsRoot._undo = None

class Undo(deque):
  """Implementation of an undo and redo stack, with possibility of waypoints.
     A waypoint is the level at which an undo happens, and each of them could
     consist of multiple individual undo operations.

     To create a waypoint use newWaypoint().
  """

  def __init__(self, maxWaypoints=20, maxOperations=10000, debug=False):
    """Create Undo object with maximum stack length maxUndoCount"""

    self.maxWaypoints = maxWaypoints
    self.maxOperations = maxOperations
    self.nextIndex = 0   # points to next free slot (or first slot to redo)
    self.waypoints = []  # array of last item in each waypoint
    self._blocked = False # Block/unblock switch - internal use only
    self._blockingLevel = 0 # Blocking level - modify with increaseBlocking/decreaseBlocking only
    if maxWaypoints:
      self.newWaypoint()
    deque.__init__(self)

    # Reset to True to unblank errors during undo/redo
    self._debug = debug

  @property
  def blocking(self):
    """Undo blocking. If true (non-zero) undo setting is blocked.
    Allows multiple external functions to set blocking without trampling each other

    Modify with increaseBlocking/decreaseBlocking only"""
    return self._blockingLevel

  def increaseBlocking(self):
    """Set one more level of blocking"""
    self._blockingLevel += 1

  def decreaseBlocking(self):
    """Reduce level of blocking - when level reaches zero, undo is unblocked"""
    if self._blockingLevel > 0:
      self._blockingLevel -= 1



  def newWaypoint(self):
    """Start new waypoint"""
    if self.maxWaypoints < 1:
      raise ValueError("Attempt to set waypoint on Undo object that does not allow them ")

    waypoints = self.waypoints
    waypoints.append(self.nextIndex-1)

    if len(waypoints) > self.maxWaypoints:
      for ii in range(waypoints[0]):
        self.popleft()
      del waypoints[0]

  def newItem(self, undoMethod, redoMethod, undoArgs=None, undoKwargs=None,
              redoArgs=None, redoKwargs=None):
    """Add item to the undo stack.
    """

    if not undoArgs:
      undoArgs = ()
    if not redoArgs:
      redoArgs = ()

    if self._blocked or self._blockingLevel:
      return

    # clear out redos that are no longer going to be doable
    for n in range(len(self)-self.nextIndex):
      self.pop()

    # add new data
    if undoKwargs is None:
      undoCall = partial(undoMethod, *undoArgs)
    else:
      undoCall = partial(undoMethod, *undoArgs, **undoKwargs)
    if redoKwargs is None:
      redoCall = partial(redoMethod, *redoArgs)
    else:
      redoCall = partial(redoMethod, *redoArgs, **redoKwargs)
    self.append((undoCall, redoCall))

    # fix waypoints:
    ll = self.waypoints
    while ll and ll[-1] >= self.nextIndex:
      ll.pop()

    # correct for maxOperations
    if len(self) > self.maxOperations:
      self.popleft()
      ll = self.waypoints
      if ll:
        for n,val in enumerate(ll):
          ll[n] = val - 1
        if ll[0] < 0:
          del ll[0]
    else:
      self.nextIndex += 1


  # def newItem(self, undoMethod, undoData, redoMethod, redoData=None):
  #   """Add item to the undo stack.
  #      Note that might not know redoData until after we do undo.
  #      NBNB NO, we should know, so resetting facility disabled. Rasmus
  #   """
  #
  #   if self._blocked:
  #     return
  #
  #   # clear out redos that are no longer going to be doable
  #   for n in range(len(self)-self.nextIndex):
  #     self.pop()
  #
  #   # add new data
  #   self.append((undoMethod, undoData, redoMethod, redoData))
  #
  #   # fix waypoints:
  #   ll = self.waypoints
  #   while ll and ll[-1] >= self.nextIndex:
  #     ll.pop()
  #
  #   # correct for maxOperations
  #   if len(self) > self.maxOperations:
  #     self.popleft()
  #     ll = self.waypoints
  #     if ll:
  #       for n,val in enumerate(ll):
  #         ll[n] = val - 1
  #       if ll[0] < 0:
  #         del ll[0]
  #   else:
  #     self.nextIndex += 1


  def undo(self):
    """Undo one operation - or one waypoint if waypoints are not set

    For now errors are handled by printing a warning and clearing the undo object"""

    # TBD: what should we do if undoMethod() throws an exception?

    if self.nextIndex == 0:
      return

    elif self.maxWaypoints:
      undoTo = -1
      for val in self.waypoints:
        if val < self.nextIndex:
          undoTo = val
        else:
          break
    else:
      undoTo = max(self.nextIndex - 2, -1)

    # block addition of items while operating
    self._blocked = True
    try:
      for n in range(self.nextIndex-1,undoTo,-1):
        # undoMethod, undoData, redoMethod, redoData = self[n]
        # if undoData is None:
        #   undoMethod()
        # else:
        #   undoMethod(undoData)
        undoCall, redoCall = self[n]
        # if self._debug:
        #   print ("@~@~ undoing", undoCall)
        undoCall()
      self.nextIndex = undoTo + 1
    except Exception as e:
      from ccpncore.util.Logging import getLogger
      getLogger().warning ("Error while undoing (%s). Undo stack is cleared." % e)
      if self._debug:
        print ("UNDO DEBUG: error in undo. Last undo function was:", undoCall)
        raise
      self.clear()
    finally:
      # Addded by Rasmus March 2015. Surely we need to reset self._blocked?
      self._blocked = False

  def redo(self):
    """Redo one waypoint - or one operation if waypoints are not set.

    For now errors are handled by printing a warning and clearing the undo object"""

    # TBD: what should we do if redoMethod() throws an exception?

    if self.nextIndex > len(self):
      return

    elif self.maxWaypoints:
      redoTo = len(self) - 1
      for val in reversed(self.waypoints):
        if val >= self.nextIndex:
          redoTo = val
        else:
          break

    else:
      redoTo = min(self.nextIndex, len(self))

    # block addition of items while operating
    self._blocked = True
    try:
      for n in range(self.nextIndex,redoTo+1):
        # undoMethod, undoData, redoMethod, redoData = self[n]
        # if redoData is None:
        #   redoMethod()
        # else:
        #   redoMethod(redoData)
        undoCall, redoCall = self[n]
        # if self._debug:
        #   print ("@~@~ redoing", redoCall)
        redoCall()
      self.nextIndex = redoTo + 1
    except Exception as e:
      from ccpncore.util.Logging import getLogger
      getLogger().warning("Error while redoing (%s). Undo stack is cleared." % e)
      if self._debug:
        print ("REDO DEBUG: error in redo. Last redo call was:", redoCall)
        raise
      self.clear()
    finally:
      # Addded by Rasmus March 2015. Surely we need to reset self._blocked?
      self._blocked = False

  def clear(self):
    """Clear and reset undo object """
    self.nextIndex = 0
    self.waypoints.clear()
    self._blocked = False
    self._blockingLevel = 0
    deque.clear(self)

  def canUndo(self) -> bool:
    """Can an undo operation be performed?"""
    return self.nextIndex > 0

  def canRedo(self) -> bool:
    """can a redo operation be performed"""
    return self.nextIndex <= len(self)
