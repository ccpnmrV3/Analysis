"""
Module Documentation here
"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = ""
__credits__ = ""
__licence__ = ("")
__reference__ = ("")
#=========================================================================================
# Last code modification:
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified$"
__version__ = "$Revision$"
#=========================================================================================
# Created:
#=========================================================================================
__author__ = "$Author: Ed Brooksbank $"
__date__ = "$Date$"
#=========================================================================================
# Start of code
#=========================================================================================

from ccpn.ui.gui.lib.GuiListView import GuiListViewABC


class GuiMultipletListView(GuiListViewABC):
    """multipletList is the CCPN wrapper object
    """

    def __init__(self):
        super().__init__()
