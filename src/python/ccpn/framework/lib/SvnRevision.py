"""Module Documentation here
"""

#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2019"
__credits__ = ("Ed Brooksbank, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license")
__reference__ = ("Skinner, S.P., Fogh, R.H., Boucher, W., Ragan, T.J., Mureddu, L.G., & Vuister, G.W.",
                 "CcpNmr AnalysisAssign: a flexible platform for integrated NMR analysis",
                 "J.Biomol.Nmr (2016), 66, 111-124, http://doi.org/10.1007/s10858-016-0060-y")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:32:37 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: TJ Ragan $"
__date__ = "$Date: 2016-05-16 06:41:02 +0100 (Mon, 16 May 2016) $"
#=========================================================================================
# Start of code
#=========================================================================================

import os
import subprocess
import re


__all__ = ['applicationVersion', 'revision']

applicationVersion = '3.0.0.m0'
REVISION = '9565'
__revision = None


def revision(update=True):
    global __revision
    if __revision is None:
        try:
            __revision = _getRevisionNumber()
        except:
            __revision = REVISION
        if update is True:
            _changeStoredRevisionNumber()
    return __revision


def _getRevisionNumber():
    thisScriptDir = os.path.dirname(os.path.realpath(__file__))
    svnInfo = str(subprocess.check_output(["svn", "info"], cwd=thisScriptDir))
    m = re.search('Revision:\s([0-9]+)', svnInfo)
    revisionNumber = m.group(1)
    return revisionNumber


def _changeStoredRevisionNumber():
    thisScript = os.path.realpath(__file__)
    with open(thisScript) as f:
        s = re.sub("""(REVISION\s*=\s*')[0-9]*'""",
                   "\g<1>{}'".format(revision()),
                   f.read())
    with open(thisScript, 'w') as f:
        f.write(s)


def main():
    print(revision(update=True))


if __name__ == '__main__':
    import sys


    sys.exit(main())
