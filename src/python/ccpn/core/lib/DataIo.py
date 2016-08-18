"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Luca G Mureddu, Simon P Skinner & Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                 " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================



import os
import sys
import math
from collections import  OrderedDict
from ccpn.util.nef import StarIo
from ccpn.core.lib import CcpnNefIo
from ccpn.core.lib import MoleculeLib

def parseNmrPipeScript(path):
  """Extract data of form -xABC valuex -yABC valuey -zABC valuez
  as a dictionary of {'ABC:(valuex, valuey, valuez)} from nmrpipr input script"""
  tokens = []
  result = {}
  for line in open(path):
    ss = line.strip()
    if ss and ss[0] not in '#!':
      ll = ss.split()
      if ll[-1] == '\'':
        del ll[-1]
      tokens.extend(ll)
      ii = 0
      while ii < len(tokens):
        tag = tokens[ii]
        if tag[:2] in ('-x', '-y', '-z'):
          indx = 'xyz'.index(tag[1])
          tag = tag[2:]
          ll = result.get(tag, [None, None, None])
          ii += 1
          ll[indx] = tokens[ii]
          result[tag] = ll
          ii += 1
        else:
          ii += 1
  #
  return result

def importCyanaRestraints(project, dataPath, restraintType='Distance'):
  text = open(dataPath).read()

  dataSet = project.dataSets[-1]
  restraintList = dataSet.newRestraintList(restraintType=restraintType,
                                           comment="Cyana restraint list load")
  extractCyanaRestraints(restraintList, text)

def getProject(projectPath):
  from ccpn.framework.Framework import getFramework
  projectPath = os.path.normpath(os.path.abspath(projectPath))
  application = getFramework()
  application.loadProject(projectPath)
  project = application.project
  #
  return project


def extractCyanaRestraints(restraintList, text):
  """Extract CYANA restraints from tect. NBNB HACK!

  This is an ad-hoc function to read information from PDB=-deposited
  restraint blocks, customised for (a) particular case(s)

  residueTypes are not read, to avoid complications with non-standard
  DNA/RNA names. User beware"""
  project = restraintList._project
  sequenceCodeMap = {}
  for residue in project.residues:
    sequenceCode = residue.sequenceCode
    if sequenceCode in sequenceCodeMap:
      raise ValueError("Duplicate sequenceCode %s in project chains. Aborting" % sequenceCode)
    # NB we convert sequenceCode to int 1) for sorting, 2) because non-int examples will not appear
    sequenceCodeMap[sequenceCode] = (residue.chain.shortName, int(sequenceCode), residue.residueType)

  for line in text.splitlines():

    # ignore empty and comment lines
    line = line.upper().strip()
    if not line or line[0] in '#!':
      continue

    ll = line.split()[:7]
    value = float(ll[-1])

    ids = []
    for start in 0,3:
      sequenceCode, residueType, atomName = ll[start:start+3]
      tt = sequenceCodeMap[sequenceCode]
      if atomName.startswith('QQ'):
        atomName = 'H' + atomName[2:] + '%'
      elif atomName.startswith('Q'):
        if atomName[-1] == "'":
          atomName = 'H' + atomName[1:] + '*'
        elif atomName[-1] in ('1', '2') and residueType not in ('THR', 'ILE'):
          # NB this hardwires that these methyl groups are NOT stereospecific
          # nThat may not be correct, but ...
          ss = 'X' if atomName[-1] == '1' else 'Y'
          atomName = 'H' + atomName[1:-1]+ ss + '%'
        else:
          atomName = 'H' + atomName[1:] + '%'
      ids.append(tt + (atomName,))
    items = ['%s.%s.%s.%s' % (tt) for tt in ids]
    restraintList.createSimpleRestraint(upperLimit=value, restraintItems=(items,))



def parseCyanaPeakList(path):
  """Parse cyana peakList, returning labels (in order) and a list of lines, one per peak"""

  labels = [None] * 3
  lines = []
  for line in open(path):
    line = line.strip()
    if line.startswith('#'):
      upperline = line.upper()
      if ' DIMENSIONS' in upperline:
        ll = line.split()
        dimensionCount = int(ll[-1])
        labels = [None] * dimensionCount
      elif 'INAME' in upperline:
        ll = line.split()
        labels[int(ll[-2]) - 1] = ll[-1]
    else:
      lines.append(line)
  #
  return labels, lines

def loadCasdRdcList(project, path):
  """Load RDC constraint lists from CASD rdc file"""
  chainCode = project.chains[0].shortName

  dataSet = project.dataSets[-1]

  # Get list name
  dirname, basename = os.path.split(path)
  if not basename:
    dirname, basename = os.path.split(dirname)
  name, dummy = os.path.splitext(basename)

  restraintLists = {}
  project._appBase._echoBlocking += 1
  try:
    for line in open(path):
      line = line.strip()
      if line and line[0] not in  '#!':
        if 'H' in line:
          # restraint
          ll = line.split()
          sq1, type1, atom1, sq2, type2, atom2 = ll[:6]
          restraintItems = (('.'.join((chainCode, sq1, type1, atom1)),
                             '.'.join((chainCode, sq2, type2, atom2))
                             ),)
          value, error, weight, orientation = [eval(x) for x in ll[6:10]]
          restraintList = restraintLists[orientation]
          restraintList.createSimpleRestraint(targetValue=value, error=error, weight=weight,
                                              restraintItems=restraintItems)
        else:
          # Restraint list description
          ll = line.split()
          orientation, magnitude, rhombicity = [eval(x) for x in ll[:3]]
          sequenceCode = ll[3]
          usename = '%s-%s' % (name, orientation)
          restraintList = dataSet.newRestraintList('Rdc', name=usename, serial=orientation,
                                                   tensorMagnitude=magnitude,
                                                   tensorRhombicity=rhombicity,
                                                   tensorSequenceCode=sequenceCode)
          restraintLists[orientation] = restraintList
  finally:
    project._appBase._echoBlocking -= 1

def loadCyanaPeakList(spectrum, peakFile, axisCodes=None):
  """Load unassigned Cyana peak file into spectrum.
  axisCodes (or spectrum.axisCodes) must be the axisCodes of the sepctrum
  in the order dimensions appear in the cyana peak file"""

  project = spectrum.project

  dummy, lines = parseCyanaPeakList(peakFile)

  if axisCodes:
    reordering = [axisCodes.index(x) for x in spectrum.axisCodes]

  peakList = spectrum.newPeakList()
  project._appBase._echoBlocking += 1
  try:
    for line in lines:
      params = {}
      ll = line.split()
      params['serial'] = int(ll[0])
      position = [float(x) for x in ll[1:4]]
      if axisCodes:
        position = [position[x] for x in reordering]
      params['position'] = position
      params['volume'] = float(ll[6])
      params['volumeError'] = float(ll[7])
      peakList.newPeak(**params)
  finally:
    project._appBase._echoBlocking -= 1

def loadCasdPeakList(project, nmrPipeScriptFile, peakFile, spectrumName=None):
  """NB this assumes unassigned, cyana format peak lists, and uses the nmrpipe
  script file to extract spectrum parameters"""
  if spectrumName is None:
    dirname, basename = os.path.split(peakFile)
    if not basename:
      dirname, basename = os.path.split(dirname)
    spectrumName, dummy = os.path.splitext(basename)
  inp = parseNmrPipeScript(nmrPipeScriptFile)
  labels, lines = parseCyanaPeakList(peakFile)

  reordering = [inp['LAB'].index(x) for x in labels]

  params = {}
  params['spectrometerFrequencies'] = [float(inp['OBS'][ii]) for ii in reordering]
  params['spectralWidthsHz'] = [float(inp['SW'][ii]) for ii in reordering]
  points = [int(inp['N'][ii]) for ii in reordering]
  for ii, pp in enumerate(points):
    points[ii] = 2**(math.ceil(math.log(pp, 2)))
  params['pointCounts'] = points
  params['referencePoints'] = [x // 2 + 1 for x in points]
  params['referenceValues'] = [float(inp['CAR'][ii]) for ii in reordering]

  # Map axis codes using std Cyana convention for NOESY
  # NBNB this is a HACK, and not generally valid
  axisCodes = list(labels)
  for ii, code in enumerate(axisCodes):
    if code == '1H':
      if '13C' in labels:
        axisCodes[ii] = 'Hc'
      elif '15N' in labels:
        axisCodes[ii] = 'Hn'
      else:
        axisCodes[ii] = 'H'
    elif code == '13C':
      if '1H' in labels:
        axisCodes[ii] = 'Ch'
      else:
        axisCodes[ii] = 'C'
    elif code == '15N':
      if '1H' in labels:
        axisCodes[ii] = 'Nh'
      else:
        axisCodes[ii] = 'N'
    elif code[-1] == '1' and '1H' in labels:
      axisCodes[ii] = code[:-1]
  params['axisCodes'] = axisCodes

  isotopeCodes = list(x.upper() for x in labels)
  isotopeCodeMap = {'H':'1H', 'C':'13C', 'N':'15N', 'F':'19F', 'P':'31P'}
  for ii, code in enumerate(isotopeCodes):
    isotopeCodes[ii] = isotopeCodeMap.get(code[0], code)
  params['isotopeCodes'] = isotopeCodes

  maxPoints = 0
  acquisitionAxisCode = params['axisCodes'][0]
  for ii, pointCount in enumerate(points):
    if pointCount > maxPoints:
      maxPoints = pointCount
      acquisitionAxisCode = params['axisCodes'][ii]

  spectrumParameters = {'acquisitionAxisCode':acquisitionAxisCode}

  spectrum = CcpnNefIo.createSpectrum(project, spectrumName, spectrumParameters=spectrumParameters,
                                      dimensionData=params)

  peakList = spectrum.newPeakList()
  project._appBase._echoBlocking += 1
  try:
    for line in lines:
      params = {}
      ll = line.split()
      params['serial'] = int(ll[0])
      params['position'] = [float(x) for x in ll[1:4]]
      params['volume'] = float(ll[6])
      params['volumeError'] = float(ll[7])
      peakList.newPeak(**params)
  finally:
    project._appBase._echoBlocking -= 1
  #
  return peakList

def readNmrStarChemicalShifts(project, path,  chainOrder='CAB'):
  """Read chemical shifts from star file at path into project

  chainOrder are the vhsinCOdes to use, in order of the BMRB entity codes"""
  dataExtent = StarIo.parseNmrStarFile(path, wrapInDataBlock=True)
  dataBlock = list(dataExtent.values())[0]
  newShiftList = loadNmrStarChemicalShifts(project, dataBlock, chainOrder=chainOrder)
  for nmrChain in project.nmrChains:
    alignNmrChain(nmrChain)
    collapseXH3Groups(nmrChain)
    convertBmrbAmbiguousAtoms(nmrChain)

def alignNmrChain(nmrChain):
  """Correct sequenceCodes in an assigned nmrChain to compensate for a sequence offset
  relative to the molecular system.

  Will only modify data if all residues match in the result, but not in the starting
  situation, and will choose the smallest (most negative) value of offset that achieves this."""

  chain = nmrChain.chain
  if chain is None:
    return

  reference = OrderedDict(((x.sequenceCode, x.residueType) for x in chain.residues
                           if x.residueType is not None))
  sequence = OrderedDict(((x.sequenceCode, x.residueType) for x in nmrChain.nmrResidues
                           if x.residueType is not None))
  offset = MoleculeLib.sequenceMatchOffset(reference, sequence)

  if offset:
    # reassign all NmrResidues in chain with offset
    # NB we need to deassign first, to avoid potential name clashes
    ll = []
    for nmrResidue in nmrChain.nmrResidues:
      ll.append((nmrResidue, nmrResidue.sequenceCode, nmrResidue.residueType))
      nmrResidue.deassign()
    for nmrResidue, sequenceCode, residueType in ll:
      nmrResidue.assignTo(sequenceCode=str(int(sequenceCode) + offset),
                          residueType=residueType)


def loadNmrStarChemicalShifts(project, nmrStarDatablock,chainOrder:str=None) -> 'ChemicalShiftList':
  """Extract NmrStar ChemicalShifts to new ChemicalShiftList.
  Chains will be named A, B, ... taking the next free letter

  NB This is a quick hack. E.g.No use is made of author naming info."""
  defaultChainCodeValues = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  chainCodes = {}
  chainCodeIndex = 0
  chainCodeValues = chainOrder or defaultChainCodeValues

  shiftFrames = [x for x in nmrStarDatablock.values() if x.category == 'assigned_chemical_shifts']

  if not shiftFrames:
    return
  if len(shiftFrames) > 1:
    print('WARNING, multiple shift lists:', *(x.name for x in shiftFrames))


  blockName = nmrStarDatablock.name
  for shiftSaveFrame in shiftFrames:
    loop = shiftSaveFrame.get('atom_chem_shift')
    if not loop:
      return

    if len(shiftFrames) == 1:
      name = blockName
    else:
      name = '%s_%s' % (blockName, shiftSaveFrame.name.split('_')[-1])

    chemicalShiftList = project.newChemicalShiftList(name=name,
                                                     autoUpdate=False,
                                                     comment='Loaded from NmrStar')
    project._appBase._echoBlocking += 1
    try:
      for row in loop.data:
        entityId = row.get('entity_assembly_id')
        if entityId is None:
          entityId = row.get('entity_id')
        chainCode = chainCodes.get(entityId)
        if chainCode is None:
          chainCode = chainCodeValues[chainCodeIndex]
          chainCodeIndex += 1
          chainCodes[entityId] = chainCode
        nmrChain = project.fetchNmrChain(chainCode)

        sequenceCode = row['seq_id']
        residueType = row['comp_id']

        nmrResidue = nmrChain.fetchNmrResidue(sequenceCode=sequenceCode, residueType=residueType)

        atomName = row['atom_id']
        nucleus = row.get('atom_type')
        massNumber = row.get('atom_isotope_number')
        if nucleus and massNumber:
          isotopeCode = '%s%s' % (massNumber, nucleus.upper())
        else:
          isotopeCode = None
        ambiguityCode = row.get('ambiguity_code')
        try:
          # Ungainly and slow.
          # But we want to use New, in order to pass in the isotopeCode
          # (just in case the name does nto start with the right letter)
          # And we want to get the previous atom when there is one.
          #' This also avoids messing with remapping names with dots in etc.
          nmrAtom = nmrResidue.newNmrAtom(name=atomName, isotopeCode=isotopeCode)
        except ValueError:
          nmrAtom = nmrResidue.fetchNmrAtom(name=atomName)
        dd = nmrAtom.ccpnInternalData
        if not dd:
          dd = nmrAtom.ccpnInternalData = {}
        # NB when the same NmrAtom appears twice we get the ambiguity code
        # and original name from the LAST occurrence
        dd.update({'ambiguityCode':ambiguityCode, 'originalName':atomName})

        value = row.get('val')
        error = row.get('val_err')
        chemicalShift = chemicalShiftList.newChemicalShift(nmrAtom=nmrAtom, value=value,
          valueError=error, comment='Original name: %s, ambiguityCode: %s' % (atomName, ambiguityCode)
        )
    finally:
      project._appBase._echoBlocking -= 1
  #
  return chemicalShiftList

def collapseXH3Groups(nmrChain:'NmrChain'):
  """Convert triplets of NmrAtoms to single CH3/NH3 NmrAtoms
  and change '*' to '%'.

  Triplets Habc1,Habc2,Habc3 will be converted to Habc%
  provided they are not of the form 'Hijk' or 'H@ijk' where 'ijk' is an integer.


  NB This will miss N-terminal NH3 groups, but the alternative might catch
  non-XH3 groups."""

  chainCode = nmrChain.shortName

  # group protons into potential XH3 groups
  for nmrResidue in nmrChain.nmrResidues:

    sequenceCode = nmrResidue.sequenceCode
    residueType = nmrResidue.residueType

    groups = {}
    for nmrAtom in nmrResidue.nmrAtoms:
      name = nmrAtom.name
      if name[0] == 'H' and name[-1] in '123':
        if (not (name[1:].isdigit() and len(name) == 3 and name[-2] in '123')
            and not (name[1] == '@' and name[2:].isdigit())):
          # The first line should recognise methyl groups, but not
          # E.g. H11,H12,H13, which could be a small molecule
          # This heuristic will treat anything up to H33 as single
          # and higher numbers as methyls if there is a triplet
          prefix = name[:-1]
          ll = groups.get(prefix, [])
          ll.append(nmrAtom)
          groups[prefix] = ll

      elif '*' in name:
        newName = name.replace('*', '%')
        nmrAtom.assignTo(chainCode, sequenceCode, residueType, newName)


    # Merge and rename XH3 group NmrAtoms
    for prefix, group in groups.items():
      if len(group) == 3:
        newName = prefix + '%'
        previous = nmrResidue.getNmrAtom(newName)
        if previous is None:
          # NB by the nature of the preceding loop the names CAN ONLY be
          # `prefix>`1, `prefix`2, `prefix`3
          for nmrAtom in sorted(group):
            nmrAtom.assignTo(chainCode, sequenceCode, residueType, newName, mergeToExisting=True)
        else:
          nmrChain._project._logger.info("Cannot create new XH3 group %s - group already exists"
                                         % previous.pid)

def convertBmrbAmbiguousAtoms(nmrChain):
  """Convert NmrAtoms with na.ccpnInternalData['ambiguityCode'] 2 or 3
  to the 'XY' convention.
  Names are of form 'Nabi'  or 'Nabi%' or 'NAbi*' where 'N' is a one-letter nucleus code.
  'ab' is any string that is not an integer or '@' followed by an integer
  and 'i' is 1, 2 or 3.
  The new names will be of the form 'NabX' or 'NabY' or 'NabX%', 'NabY%'

  If 'abi' for one nucleus name matches 'abi' for another nucleus name,
  (e.g. HG1 and CG1), both will match after name substitution (to e.g. HGX and CGX)
  In these cases, if ANY nucleus is ambiguous, all will be treated as ambiguous.

  If matching names are found for i==1, i==2, and i==3, (should not happen), no changes are made

  NBNB inconsistent ambiguity codes are NOT guaranteed to give sensible results
  """

  chainCode = nmrChain.shortName

  for nmrResidue in nmrChain.nmrResidues:

    sequenceCode = nmrResidue.sequenceCode
    residueType = nmrResidue.residueType

    # special cases, DNA H2', H2'', DNA/RNA H5', H5''

    # group NmrAtoms into potential matching groups
    groups = {}
    for nmrAtom in nmrResidue.nmrAtoms:
      name = nmrAtom.name

      if name.endswith("'"):
        # special case, ambigous atom pairs ending in ' or ''
        dd2 = nmrAtom.ccpnInternalData
        if dd2:
          xx = dd2.get('ambiguityCode')
          if xx in ('2','3'):
            # Ambiguous = set the name
            if name.endswith("''"):
              newName = name[:-2] + 'Y'
            else:
              newName = name[:-1] + 'X'
            # NB, if the name is already taken we get a nameclash
            nmrAtom.assignTo(chainCode, sequenceCode, residueType, newName)

      # elif name.endswith('"'):
      #   # Should not happen, but it looks like " can be used instead of ''        dd2 = nmrAtom.ccpnInternalData
      #   dd2 = nmrAtom.ccpnInternalData
      #   if dd2:
      #     xx = dd2.get('ambiguityCode')
      #     if xx in ('2','3'):
      #       # Ambiguous = set the name
      #       newName = name[:-1] + 'Y'
      #       # NB, if the name is already taken we get a nameclash
      #       print ('@~@~newName', newName)
      #       nmrAtom.assignTo(chainCode, sequenceCode, residueType, newName)
      #       nmrAtom.ccpnInternalData['originalName'] = name


      elif len(name) > 2:
        if name[-1] in '123':
          locator = name[1:-1]
          indx = int(name[-1]) - 1
        elif name[-1] in '%*' and name[-2] in '123':
          locator = name[1:-2]
          indx = int(name[-2]) - 1
        else:
          continue

        if not locator or locator.isdigit() or (locator[0] == '@' and locator[1:].isdigit):
          continue

        nucleus = name[0]
        dd = groups.get(locator, {})
        groups[locator] = dd
        ll = dd.get(nucleus, [None, None, None])
        dd[nucleus] = ll
        ll[indx] = nmrAtom

    # Rename to 'XY' name form
    for locator, dd in groups.items():

      # Remove indices where there are no NmrAtoms, and check for ambiguity codes:
      ambiguityCode = None
      for ii in (2,1,0):
        for ll in dd.values():

          na = ll[ii]
          if na is not None:
            dd2 = na.ccpnInternalData
            if dd2:
              xx = dd2.get('ambiguityCode')
              if xx in ('2','3'):
                ambiguityCode = xx
                break
        else:
          for ll2 in dd.values():
            del ll2[ii]

      if ambiguityCode:
        # There are ambiguous atoms (code 2=geminal or code 3=aromatic ring)
        # Set ALL matching names with ambiguous XY names

        if len(ll) <= 2:
          # We now have one or two atoms for each nucleus.
          # Rename first slot as X, second slot as Y
          tags = 'XY'
          for ll in dd.values():
            for ii, nmrAtom in enumerate(ll):
              if nmrAtom is not None:
                name = nmrAtom.name
                if name[-1] in '%*':
                  newName = name[:-2] + tags[ii] + '%'
                else:
                  newName = name[:-1] + tags[ii]
                # NB, if the name is already taken we get a nameclash
                nmrAtom.assignTo(chainCode, sequenceCode, residueType, newName)

        else:
          # There are NmrAtoms with names ending all of 1,2,3
          # This is not a clear case - do nothing
          nmrChain._project._logger.info(
            "ambigous assignments, code %s, not renamed to 'XY' name - inconsistent set: %s"
            % (ambiguityCode, [x for x in ll for ll in dd.values() if x is not None])
          )

def remapRestraintItems(project):
  """Remap restraintItems from original names to massaged names

  - relies on NmrAtom.ccpnInternalData['originalName'] being set"""
  remap = {}
  for nmrAtom in project.nmrAtoms:
    atomId = nmrAtom._id
    originalName = nmrAtom.ccpnInternalData.get('originalName')
    if originalName:
      if atomId.endswith('%'):
        if atomId[-2] in 'XY':
          origId = atomId[:-2] + originalName[-2] + '%'
        else:
          # CH3 groups are already correct
          origId = atomId
      else:
        stub, junk = atomId.rsplit('.', 1)
        origId = '%s.%s' % (stub, originalName)
      remap[origId] = atomId
    else:
      remap[atomId] = atomId

  for contribution in project.restraintContributions:
    items = []
    for tt in contribution.restraintItems:
      ll = []
      for ss in tt:
        val = remap.get(ss)
        if val is None:
          if ss[-1] not in 'O%':
            project._logger.info("---> Restraint item %s could not be found in restraint map - %s"
                                % (ss, contribution))
          val = ss
        ll.append(val)
      items.append(ll)
    contribution.restraintItems = items

def loadDocrProject(name, projectPath:str, bmrbEntryPath:str, casdDirectory=None,
                    chainOrder:str=None) -> 'Project':
  """Load DOCR project, reading chemical shifts from bmrbEntryPath,
  with allowance for ambiguity codes 2 and 3, mapping  restraints to match
  NmrAtom names

  If casdDirectory is given, read peak lists from std Montelions CASD-2013 file structure
  """

  # Get project
  from ccpn.framework.Framework import getFramework
  application = getFramework()
  project = application.loadProject(projectPath)

  # Save project with new name - done now to get right name and path for further operations
  dirname, basename = os.path.split(projectPath)
  if not basename:
    dirname, basename = os.path.split(dirname)
  projectPath = os.path.join(dirname, name)
  project.save(projectPath)

  nefPath = project.path + '.raw.nef'
  CcpnNefIo.saveNefProject(project, nefPath, overwriteExisting=True, skipPrefixes=('ccpn',))

  # Correct restraint item names to avoid ambiguous CCPN names
  cleanUpDocrProject(project)

  nefPath = project.path + '.cleaned.nef'
  CcpnNefIo.saveNefProject(project, nefPath, overwriteExisting=True, skipPrefixes=('ccpn',))

  # Load chemical shifts from BMRB file
  readNmrStarChemicalShifts(project, bmrbEntryPath, chainOrder=chainOrder)

  # remap restraint items to use new names
  remapRestraintItems(project)

  project.save()
  #
  return project

def loadCasdData(project, casdDirectory):
  """"AD-HOC function: Load Montelione CASD data - with file names hardwired"""

  # Remove restraint lists = we read in those from the CASD data
  dataSet = project.dataSets[-1]
  for restraintList in dataSet.restraintLists:
    if restraintList.restraintType == 'Rdc':
      restraintList.delete()

  # Read spectrum parameters and peakLists
  for peakFile, scriptFile in (
      #('simnoe_15N_final.peaks', 'simnoesy/Convert_N15_noesy_HSQC.csh'),
      ('final_peaks/alinoe_final.peaks', 'simnoesy/Convert_C13_noesy_HSQC.csh'),
      ('final_peaks/aronoe_final.peaks', 'aronoesy/Convert_C13_noesy_HSQC.csh'),
  ):
    scriptPath = os.path.join(casdDirectory, scriptFile)
    peakPath = os.path.join(casdDirectory, peakFile)
    loadCasdPeakList(project, scriptPath, peakPath)

  # # Read .rdc files - NB do not need remapping
  # for ss in os.listdir(casdDirectory):
  #   if ss.endswith('.rdc'):
  #     path = os.path.join(casdDirectory, ss)
  #     loadCasdRdcList(project, path)
  path = os.path.join(casdDirectory, 'final_peaks/cya.rdc')
  loadCasdRdcList(project, path)

  #
  project.save()

def cleanUpDocrProject(project):
  """Clean up DOCR project - converting restraints to ambiguous atoms
  (e.g. HBa/HBb) to restraints to % atoms (e.g. HB%).
  This is SPECIFIC for DOCR projects, since it appears that only HB% type
  restraints appear as HBa/HBb"""

  for contribution in project.restraintContributions:
    items = []
    for tt in contribution.restraintItems:
      ll = []
      for atomId in tt:
        if atomId[-2:] in ('5X', '5Y'):
          # Special case - DNA/RNA H5'/H5''
          # We cannot do that for H2'/H2'' as H2X could be other things as well
          atomId = atomId[:-1] + "'*"
        elif atomId[-1] in 'XY':
          atomId = atomId[:-1] + '%'
        elif atomId[-2:] in ('X%', 'Y%'):
          atomId = atomId[:-2] + '%'
        ll.append(atomId)
      if not ll in items:
        # Skip duplicates
        items.append(ll)
    contribution.restraintItems = items

if __name__ == '__main__':

  name, projectPath, bmrbEntryPath = sys.argv[1:4]
  projectPath = os.path.normpath(os.path.abspath(projectPath))
  bmrbEntryPath = os.path.normpath(os.path.abspath(bmrbEntryPath))
  project = loadDocrProject(name, projectPath, bmrbEntryPath, chainOrder='CAB')

  if len(sys.argv) > 4:
    casdDirectory = sys.argv[4]
    casdDirectory = os.path.normpath(os.path.abspath(casdDirectory))
    loadCasdData(project, casdDirectory)
    project.save()


  # projectPath, dataPath = sys.argv[1:3]
  # dataPath = os.path.normpath(os.path.abspath(dataPath))
  # project = getProject(projectPath)
  # importCyanaRestraints(project, dataPath)
  # remapRestraintItems(project)
  # project.save()



  nefPath = project.path + '.nef'
  CcpnNefIo.saveNefProject(project, nefPath, overwriteExisting=True, skipPrefixes=('ccpn',))
