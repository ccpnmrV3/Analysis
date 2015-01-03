
# Packages, classElements and AbstractDataTypes skipped in new model
# (prefix, typeName, elemName, newGuid, elemType)
skipElements = [
 ('COOR', 'Atom', 'coords', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00063', 'MetaRole'), 
 ('COOR', 'Coord', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:55_00001', 'MetaClass'), 
 ('COOR', 'Model', 'coords', 'www.ccpn.ac.uk_Fogh_2007-11-23-12:00:15_00002', 'MetaRole'), 
 ('MOLS', 'Atom', 'chainStateSets', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:02_00011', 'MetaRole'), 
 ('MOLS', 'Chain', 'chainStateSets', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:31_00038', 'MetaRole'), 
 ('MOLS', 'Residue', 'chainStateSets', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:32_00036', 'MetaRole'), 
 ('NMR', 'ChainState', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00017', 'MetaClass'), 
 ('NMR', 'ChainStateSet', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00018', 'MetaClass'), 
 ('NMR', 'ChainStateSetType', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:49_00002', 'MetaDataType'), 
 ('NMR', 'ExpChainState', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00025', 'MetaClass'), 
 ('NMR', 'Experiment', 'expChainStates', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00014', 'MetaRole'), 
 ('NMR', 'NmrProject', 'chainStateSets', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:32_00002', 'MetaRole'), 
 ('NMR', 'Resonance', 'chainStates', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:10_00005', 'MetaRole'), 
 ('NMR', 'Resonance', 'resonanceProbs', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:21_00005', 'MetaRole'), 
 ('NMR', 'ResonanceGroup', 'resonanceProbs', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:10_00022', 'MetaRole'), 
 ('NMR', 'ResonanceProb', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:48_00032', 'MetaClass'), 
 ('NMRC', 'ChainStateLink', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:51_00033', 'MetaClass'), 
 ('NMRC', 'FixedResonance', 'chainStateLinks', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:11_00008', 'MetaRole'), 
 ('NMRC', 'FixedResonance', 'resCoords', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:06_00010', 'MetaRole'), 
 ('NMRC', 'NmrConstraintStore', 'chainStates', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:12_00028', 'MetaRole'), 
 ('NMRC', 'NmrConstraintStore', 'resStructures', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:06_00006', 'MetaRole'), 
 ('NMRC', 'ResCoord', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:51_00005', 'MetaClass'), 
 ('NMRC', 'ResStructure', None, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:51_00004', 'MetaClass'), 
 ('SYMM', 'MolSystemSymmetrySet', 'memopsRoot', 'ccpn_automatic_molsim.Symmetry.MolSystemSymmetrySet.memopsRoot', 'MetaRole'), 
]

# classElements skipped in new model, but available for simple data transfer
# (prefix, typeName, elemName, newGuid, elemMap, valueTypeGuid)
delayElements = [
 ('NMR', 'ExpDim', 'refExpDim', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:00_00002', {'name': 'refExpDim', 'type': 'exolink', 'tag': 'NMR.ExpDim.refExpDim', 'eType': 'cplx'}, None), 
 ('NMR', 'ResonanceGroup', 'clusterCode', 'www.ccpn.ac.uk_Fogh_2011-08-05-11:56:26_00003', {'name': 'clusterCode', 'type': 'attr', 'tag': 'NMR.ResonanceGroup.clusterCode', 'eType': 'cplx'}, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'), 
 ('NMR', 'ResonanceGroup', 'isActive', 'www.ccpn.ac.uk_Fogh_2011-08-05-11:56:26_00004', {'name': 'isActive', 'type': 'attr', 'tag': 'NMR.ResonanceGroup.isActive'}, 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00028'), 
]

# MetaConstraints added in new model
# (qualifiedName, guid)
newConstraints = [
 ('ccp.molecule.MolSystem.Atom.non_single_atoms_have_components', 'www.ccpn.ac.uk_Fogh_2014-07-31-11:44:56_00001'), 
 ('ccp.nmr.Nmr.ConnectedStretch.activeResonanceGroups_must_go_with_active_SequentialAssignments', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:36_00001'), 
 ('ccp.nmr.Nmr.Resonance.implName.name_is_unique_in_resonanceGroup', 'www.ccpn.ac.uk_Fogh_2014-12-30-13:36:29_00001'), 
 ('ccp.nmr.Nmr.ResonanceGroup.satellite_resonance_group_must_have_offset', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:38_00002'), 
 ('ccp.nmr.Nmr.ResonanceGroup.satellite_resonance_groups_must_be_unique', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:38_00001'), 
 ('ccp.nmr.NmrConstraint.DihedralItem.no_Dihedral_item_with_resonances_in_opposite_order', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00003'), 
 ('ccpnmr.gui.Task.BoundDisplay.axisOrder.bound_axis_order_is_reordering_of_axis_codes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:43:15_00001'), 
 ('ccpnmr.gui.Task.BoundDisplay1d.Y_axis_is_intensity', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00011'), 
 ('ccpnmr.gui.Task.BoundDisplay1d.only_one_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00012'), 
 ('ccpnmr.gui.Task.BoundDisplayNd.no_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00014'), 
 ('ccpnmr.gui.Task.BoundStrip.axiscodes_same_as_parent_display', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00019'), 
 ('ccpnmr.gui.Task.Display1d.XY_axes_only', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00021'), 
 ('ccpnmr.gui.Task.DisplayNd.no_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00023'), 
 ('ccpnmr.gui.Task.FreeStrip.axisCodes.axis_code_length_matches_display', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:45:29_00001'), 
 ('ccpnmr.gui.Task.FreeStrip.axisOrder.free_axis_order_is_reordering_of_axis_codes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:06_00001'), 
 ('ccpnmr.gui.Task.FreeStrip1d.Y_axis_is_intensity', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:36_00002'), 
 ('ccpnmr.gui.Task.FreeStripDisplay1d.Y_axis_is_intensity', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00027'), 
 ('ccpnmr.gui.Task.FreeStripDisplay1d.only_one_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00028'), 
 ('ccpnmr.gui.Task.FreeStripDisplayNd.no_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00032'), 
 ('ccpnmr.gui.Task.FreeStripNd.no_intensity_axis', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:36_00004'), 
 ('ccpnmr.gui.Task.FrequencyAxis.code.frequency_axis_code_starts_with_upper_case', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:36_00003'), 
 ('ccpnmr.gui.Task.FrequencyAxis.unit.frequency_unit_is_ppm_or_Hz_or_point', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00001'), 
 ('ccpnmr.gui.Task.IntensityAxis.code.intensity_axis_code_is_intensity', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00003'), 
 ('ccpnmr.gui.Task.IntensityAxis.unit.inteisyty_unit_is_number', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00005'), 
 ('ccpnmr.gui.Task.SampledAxis.code.value_axis_code_starts_with_lower_case', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00007'), 
 ('ccpnmr.gui.Task.SpectrumView.free_displays_are_linked_to_specific_strip_bound_displays_are_not', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00001'), 
 ('ccpnmr.gui.Task.SpectrumView.stripSerial.only_free_strip_displays_have_individual_spectrum_views', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00014'), 
 ('ccpnmr.gui.Task.Strip.only_one_struip_in_non_strip_displays', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00007'), 
 ('ccpnmr.gui.Task.ValueAxis.code.value_axis_code_starts_with_lower_case', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00010'), 
]

# Mandatory classElements added in new model
# New ClassElements with locard !=0, no default, not derived or Implementation
# (prefix, typeName, elemName, newGuid)
newMandatories = [
 ('GUIT', 'Axis', 'code', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00005'), 
 ('GUIT', 'Axis', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00010'), 
 ('GUIT', 'Axis', 'unit', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00010'), 
 ('GUIT', 'AxisPositionGroup', 'axes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00001'), 
 ('GUIT', 'AxisPositionGroup', 'guiTask', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:42:29_00008'), 
 ('GUIT', 'AxisPositionGroup', 'serial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:42:29_00009'), 
 ('GUIT', 'AxisWidthGroup', 'axes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00003'), 
 ('GUIT', 'AxisWidthGroup', 'guiTask', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00011'), 
 ('GUIT', 'AxisWidthGroup', 'serial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:42:29_00010'), 
 ('GUIT', 'BoundDisplay', 'axisOrder', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:42:29_00011'), 
 ('GUIT', 'FreeStrip', 'axisCodes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:44:49_00001'), 
 ('GUIT', 'FreeStrip', 'axisOrder', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:44:00_00007'), 
 ('GUIT', 'FreeStrip1d', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00003'), 
 ('GUIT', 'FreeStripNd', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00005'), 
 ('GUIT', 'FrequencyAxis', 'code', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:36_00002'), 
 ('GUIT', 'GuiTask', 'memopsRoot', 'ccpn_automatic_ccpnmr.gui.Task.GuiTask.memopsRoot'), 
 ('GUIT', 'GuiTask', 'name', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00014'), 
 ('GUIT', 'GuiTask', 'nmrProjectName', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00016'), 
 ('GUIT', 'Mark', 'colour', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00004'), 
 ('GUIT', 'Mark', 'guiTask', 'www.ccpn.ac.uk_Fogh_2014-11-11-18:25:59_00001'), 
 ('GUIT', 'Mark', 'serial', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00003'), 
 ('GUIT', 'Mark', 'style', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00005'), 
 ('GUIT', 'Module', 'guiTask', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00007'), 
 ('GUIT', 'Module', 'name', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00023'), 
 ('GUIT', 'PeakListView', 'peakListSerial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00030'), 
 ('GUIT', 'PeakListView', 'spectrumView', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00007'), 
 ('GUIT', 'PeakView', 'peakListView', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00028'), 
 ('GUIT', 'PeakView', 'peakSerial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:18_00004'), 
 ('GUIT', 'Ruler', 'axisCode', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00008'), 
 ('GUIT', 'Ruler', 'mark', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00001'), 
 ('GUIT', 'Ruler', 'position', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00007'), 
 ('GUIT', 'Ruler', 'serial', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00006'), 
 ('GUIT', 'SampledAxis', 'code', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00006'), 
 ('GUIT', 'SampledAxis', 'unit', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00008'), 
 ('GUIT', 'SpectrumDisplay', 'axisCodes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00012'), 
 ('GUIT', 'SpectrumView', 'axisCodes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00015'), 
 ('GUIT', 'SpectrumView', 'dataSourceSerial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00012'), 
 ('GUIT', 'SpectrumView', 'experimentName', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00011'), 
 ('GUIT', 'SpectrumView', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00006'), 
 ('GUIT', 'Strip', 'index', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00016'), 
 ('GUIT', 'Strip', 'serial', 'www.ccpn.ac.uk_Fogh_2014-11-05-12:31:24_00002'), 
 ('GUIT', 'Strip', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00003'), 
 ('GUIT', 'Strip1d', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:43:15_00002'), 
 ('GUIT', 'StripNd', 'spectrumDisplay', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:43:15_00004'), 
 ('GUIT', 'ValueAxis', 'code', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00009'), 
 ('GUIT', 'ValueAxis', 'unit', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00011'), 
 ('GUIT', 'ZoomRegion', 'axisOrder', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:57:48_00003'), 
 ('GUIT', 'ZoomRegion', 'positions', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00024'), 
 ('GUIT', 'ZoomRegion', 'serial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00023'), 
 ('GUIT', 'ZoomRegion', 'strip', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00014'), 
 ('GUIT', 'ZoomRegion', 'units', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:57:48_00002'), 
 ('GUIT', 'ZoomRegion', 'widths', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:57:48_00001'), 
 ('GUIW', 'Window', 'serial', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00013'), 
 ('GUIW', 'Window', 'title', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00014'), 
 ('GUIW', 'Window', 'windowStore', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00002'), 
 ('GUIW', 'WindowStore', 'mainWindow', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00008'), 
 ('GUIW', 'WindowStore', 'memopsRoot', 'ccpn_automatic_ccpnmr.gui.Window.WindowStore.memopsRoot'), 
 ('GUIW', 'WindowStore', 'nmrProject', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00001'), 
 ('NMR', 'ConnectedStretch', 'nmrProject', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:39_00010'), 
 ('NMR', 'ConnectedStretch', 'sequentialAssignment', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00012'), 
 ('NMR', 'ConnectedStretch', 'serial', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:39_00005'), 
 ('NMR', 'NmrChain', 'nmrProject', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00007'), 
 ('NMR', 'NmrChain', 'serial', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00004'), 
 ('NMR', 'SequentialAssignment', 'nmrProject', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:39_00008'), 
 ('NMRC', 'ChemShiftItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00003'), 
 ('NMRC', 'ChemShiftItem', 'resonance', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00006'), 
 ('NMRC', 'ChemicalShiftContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00001'), 
 ('NMRC', 'ConstraintContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00001'), 
 ('NMRC', 'ConstraintContribution', 'serial', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00005'), 
 ('NMRC', 'ConstraintItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00003'), 
 ('NMRC', 'CsaContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00007'), 
 ('NMRC', 'CsaItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00009'), 
 ('NMRC', 'CsaItem', 'resonance', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00003'), 
 ('NMRC', 'DihedralContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00004'), 
 ('NMRC', 'DihedralItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00006'), 
 ('NMRC', 'DihedralItem', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00009'), 
 ('NMRC', 'DistanceContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00002'), 
 ('NMRC', 'DistanceItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00004'), 
 ('NMRC', 'DistanceItem', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00007'), 
 ('NMRC', 'HBondContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00009'), 
 ('NMRC', 'HBondItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00011'), 
 ('NMRC', 'HBondItem', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00014'), 
 ('NMRC', 'JCouplingContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00016'), 
 ('NMRC', 'JCouplingItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00018'), 
 ('NMRC', 'JCouplingItem', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00021'), 
 ('NMRC', 'RdcContribution', 'constraint', 'www.ccpn.ac.uk_Fogh_2014-07-29-17:21:12_00001'), 
 ('NMRC', 'RdcItem', 'contribution', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00012'), 
 ('NMRC', 'RdcItem', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00015'), 
 ('SYMM', 'MolSystemSymmetrySet', 'memopsRoot', 'ccpn_automatic_ccp.molecule.Symmetry.MolSystemSymmetrySet.memopsRoot'), 
]

# Packages, classElements and AbstractDataTypes added in new model
# Optional, i.e. excluding mandatory classElements given above
# (prefix, typeName, elemName, newGuid)
newElements = [
 (None, None, None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:25_00001'), 
 (None, None, None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:25_00002'), 
 ('COOR', 'Atom', 'iupacNames', 'www.ccpn.ac.uk_Fogh_2014-10-23-17:02:39_00001'), 
 ('COOR', 'Residue', 'code3Letter', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00010'), 
 ('GUIT', None, None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00004'), 
 ('GUIT', 'Axis', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00005'), 
 ('GUIT', 'Axis', 'axisPositionGroup', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00002'), 
 ('GUIT', 'Axis', 'axisWidthGroup', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00004'), 
 ('GUIT', 'Axis', 'position', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00008'), 
 ('GUIT', 'Axis', 'regions', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00011'), 
 ('GUIT', 'Axis', 'resonanceSerials', 'www.ccpn.ac.uk_Fogh_2014-11-10-13:39:28_00002'), 
 ('GUIT', 'Axis', 'resonances', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:39_00002'), 
 ('GUIT', 'Axis', 'stripSerial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00006'), 
 ('GUIT', 'Axis', 'width', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:40_00009'), 
 ('GUIT', 'AxisArea', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00004'), 
 ('GUIT', 'AxisPositionGroup', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00002'), 
 ('GUIT', 'AxisWidthGroup', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00003'), 
 ('GUIT', 'BoundDisplay', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00009'), 
 ('GUIT', 'BoundDisplay1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00010'), 
 ('GUIT', 'BoundDisplay1d', 'strips', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:43:15_00003'), 
 ('GUIT', 'BoundDisplayNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00013'), 
 ('GUIT', 'BoundDisplayNd', 'strips', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:43:15_00005'), 
 ('GUIT', 'BoundStrip', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00018'), 
 ('GUIT', 'Display1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00020'), 
 ('GUIT', 'DisplayNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00022'), 
 ('GUIT', 'FreeStrip', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00030'), 
 ('GUIT', 'FreeStrip1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:36_00001'), 
 ('GUIT', 'FreeStripDisplay', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00029'), 
 ('GUIT', 'FreeStripDisplay1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00026'), 
 ('GUIT', 'FreeStripDisplay1d', 'strips', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00004'), 
 ('GUIT', 'FreeStripDisplayNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00031'), 
 ('GUIT', 'FreeStripDisplayNd', 'strips', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00006'), 
 ('GUIT', 'FreeStripNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:36_00003'), 
 ('GUIT', 'FrequencyAxis', None, 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:33_00002'), 
 ('GUIT', 'FrequencyAxis', 'unit', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:36_00004'), 
 ('GUIT', 'GuiTask', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00013'), 
 ('GUIT', 'GuiTask', 'axisPositionGroups', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:42:29_00007'), 
 ('GUIT', 'GuiTask', 'axisWidthGroups', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00012'), 
 ('GUIT', 'GuiTask', 'details', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00017'), 
 ('GUIT', 'GuiTask', 'marks', 'www.ccpn.ac.uk_Fogh_2014-11-11-18:25:59_00002'), 
 ('GUIT', 'GuiTask', 'modules', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00008'), 
 ('GUIT', 'GuiTask', 'nameSpace', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00013'), 
 ('GUIT', 'GuiTask', 'nmrProject', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00010'), 
 ('GUIT', 'IntensityAxis', None, 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:33_00001'), 
 ('GUIT', 'IntensityAxis', 'code', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00002'), 
 ('GUIT', 'IntensityAxis', 'unit', 'www.ccpn.ac.uk_Fogh_2014-11-06-10:53:15_00004'), 
 ('GUIT', 'Mark', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00002'), 
 ('GUIT', 'Mark', 'rulers', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00002'), 
 ('GUIT', 'Module', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00006'), 
 ('GUIT', 'Module', 'details', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00027'), 
 ('GUIT', 'Module', 'gridCell', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00024'), 
 ('GUIT', 'Module', 'gridSpan', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00025'), 
 ('GUIT', 'Module', 'window', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00011'), 
 ('GUIT', 'Module', 'windowId', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00026'), 
 ('GUIT', 'PeakListView', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00007'), 
 ('GUIT', 'PeakListView', 'isSymbolDisplayed', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:47:47_00001'), 
 ('GUIT', 'PeakListView', 'isTextDisplayed', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:18_00001'), 
 ('GUIT', 'PeakListView', 'peakList', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00008'), 
 ('GUIT', 'PeakListView', 'peakViews', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00029'), 
 ('GUIT', 'PeakListView', 'symbolColour', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00032'), 
 ('GUIT', 'PeakListView', 'symbolStyle', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00031'), 
 ('GUIT', 'PeakListView', 'textColour', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00033'), 
 ('GUIT', 'PeakView', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00008'), 
 ('GUIT', 'PeakView', 'peak', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00004'), 
 ('GUIT', 'PeakView', 'textOffset', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:18_00005'), 
 ('GUIT', 'Ruler', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:25_00004'), 
 ('GUIT', 'Ruler', 'label', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00010'), 
 ('GUIT', 'Ruler', 'unit', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00009'), 
 ('GUIT', 'SampledAxis', None, 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:33_00004'), 
 ('GUIT', 'SpectrumDisplay', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00005'), 
 ('GUIT', 'SpectrumDisplay', 'axes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00011'), 
 ('GUIT', 'SpectrumDisplay', 'resonanceGroup', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00009'), 
 ('GUIT', 'SpectrumDisplay', 'resonanceGroupSerial', 'www.ccpn.ac.uk_Fogh_2014-11-10-13:49:17_00006'), 
 ('GUIT', 'SpectrumDisplay', 'spectrumViews', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00007'), 
 ('GUIT', 'SpectrumDisplay', 'stripDirection', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00001'), 
 ('GUIT', 'SpectrumDisplay', 'strips', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00004'), 
 ('GUIT', 'SpectrumView', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00010'), 
 ('GUIT', 'SpectrumView', 'dataSource', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00010'), 
 ('GUIT', 'SpectrumView', 'dimensionOrdering', 'www.ccpn.ac.uk_Fogh_2014-11-11-18:29:24_00003'), 
 ('GUIT', 'SpectrumView', 'displayNegativeContours', 'www.ccpn.ac.uk_Fogh_2014-12-02-18:39:42_00002'), 
 ('GUIT', 'SpectrumView', 'displayPositiveContours', 'www.ccpn.ac.uk_Fogh_2014-12-02-18:39:42_00001'), 
 ('GUIT', 'SpectrumView', 'experimentType', 'www.ccpn.ac.uk_Fogh_2014-11-28-21:31:23_00002'), 
 ('GUIT', 'SpectrumView', 'isDisplayed', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00001'), 
 ('GUIT', 'SpectrumView', 'negativeContourBase', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00008'), 
 ('GUIT', 'SpectrumView', 'negativeContourColour', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00007'), 
 ('GUIT', 'SpectrumView', 'negativeContourCount', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00006'), 
 ('GUIT', 'SpectrumView', 'negativeContourFactor', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00009'), 
 ('GUIT', 'SpectrumView', 'peakListViews', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00008'), 
 ('GUIT', 'SpectrumView', 'positiveContourBase', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00004'), 
 ('GUIT', 'SpectrumView', 'positiveContourColour', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00002'), 
 ('GUIT', 'SpectrumView', 'positiveContourCount', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00003'), 
 ('GUIT', 'SpectrumView', 'positiveContourFactor', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00005'), 
 ('GUIT', 'SpectrumView', 'sliceColour', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00010'), 
 ('GUIT', 'SpectrumView', 'stripSerial', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00013'), 
 ('GUIT', 'Strip', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00006'), 
 ('GUIT', 'Strip', 'zoomRegions', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:53:34_00015'), 
 ('GUIT', 'Strip1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00015'), 
 ('GUIT', 'StripDirection', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00017'), 
 ('GUIT', 'StripDisplay1d', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00024'), 
 ('GUIT', 'StripDisplayNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00025'), 
 ('GUIT', 'StripNd', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00016'), 
 ('GUIT', 'TaskModule', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00012'), 
 ('GUIT', 'ValueAxis', None, 'www.ccpn.ac.uk_Fogh_2014-11-06-10:52:33_00003'), 
 ('GUIT', 'ZoomRegion', None, 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:35_00008'), 
 ('GUIW', None, None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:25_00003'), 
 ('GUIW', 'Window', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00001'), 
 ('GUIW', 'Window', 'modules', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00012'), 
 ('GUIW', 'Window', 'position', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00015'), 
 ('GUIW', 'Window', 'size', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00001'), 
 ('GUIW', 'WindowStore', None, 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00003'), 
 ('GUIW', 'WindowStore', 'windows', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00003'), 
 ('IMPL', 'MemopsRoot', 'currentGuiTask', 'ccpn_automatic_memops.Implementation.MemopsRoot.currentGuiTask'), 
 ('IMPL', 'MemopsRoot', 'currentWindowStore', 'ccpn_automatic_memops.Implementation.MemopsRoot.currentWindowStore'), 
 ('IMPL', 'MemopsRoot', 'guiTasks', 'ccpn_automatic_memops.Implementation.MemopsRoot.guiTask'), 
 ('IMPL', 'MemopsRoot', 'windowStores', 'ccpn_automatic_memops.Implementation.MemopsRoot.windowStore'), 
 ('MOLE', 'MolResidue', 'code3Letter', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:24_00001'), 
 ('MOLS', 'Atom', 'atomGroups', 'www.ccpn.ac.uk_Fogh_2014-07-31-11:46:10_00001'), 
 ('MOLS', 'Atom', 'atomSetName', 'www.ccpn.ac.uk_Fogh_2014-09-09-11:30:10_00002'), 
 ('MOLS', 'Atom', 'atomType', 'www.ccpn.ac.uk_Fogh_2014-07-31-11:46:10_00003'), 
 ('MOLS', 'Atom', 'boundAtoms', 'www.ccpn.ac.uk_Fogh_2014-07-31-11:45:35_00002'), 
 ('MOLS', 'Atom', 'components', 'www.ccpn.ac.uk_Fogh_2014-07-31-11:46:10_00002'), 
 ('MOLS', 'Atom', 'elementSymbol', 'www.ccpn.ac.uk_Fogh_2014-09-09-11:30:10_00001'), 
 ('MOLS', 'AtomType', None, 'www.ccpn.ac.uk_Fogh_2014-07-31-11:44:56_00002'), 
 ('MOLS', 'MolSystem', 'nmrProjects', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:34_00008'), 
 ('NMR', 'AbstractPeakDimContrib', 'annotation', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:34_00003'), 
 ('NMR', 'AbstractPeakDimContrib', 'expDimRefSerial', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:34_00005'), 
 ('NMR', 'AbstractPeakDimContrib', 'scalingFcator', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:34_00004'), 
 ('NMR', 'ConnectedStretch', None, 'www.ccpn.ac.uk_Fogh_2014-11-17-17:48:52_00002'), 
 ('NMR', 'ConnectedStretch', 'activeResonanceGroups', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00003'), 
 ('NMR', 'ConnectedStretch', 'resonanceGroupSerials', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:39_00006'), 
 ('NMR', 'DataSource', 'negativeContourBase', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00006'), 
 ('NMR', 'DataSource', 'negativeContourColour', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00008'), 
 ('NMR', 'DataSource', 'negativeContourCount', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00005'), 
 ('NMR', 'DataSource', 'negativeContourFactor', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00007'), 
 ('NMR', 'DataSource', 'positiveContourBase', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00002'), 
 ('NMR', 'DataSource', 'positiveContourColour', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00004'), 
 ('NMR', 'DataSource', 'positiveContourCount', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00001'), 
 ('NMR', 'DataSource', 'positiveContourFactor', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00003'), 
 ('NMR', 'DataSource', 'sliceColour', 'www.ccpn.ac.uk_Fogh_2014-10-28-16:32:31_00009'), 
 ('NMR', 'DataSource', 'spectrumViews', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:52:44_00009'), 
 ('NMR', 'Experiment', 'experimentType', 'www.ccpn.ac.uk_Fogh_2014-11-28-21:31:22_00004'), 
 ('NMR', 'NmrChain', None, 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:22_00001'), 
 ('NMR', 'NmrChain', 'code', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00005'), 
 ('NMR', 'NmrChain', 'details', 'www.ccpn.ac.uk_Fogh_2014-12-30-11:21:22_00001'), 
 ('NMR', 'NmrChain', 'resonanceGroups', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00002'), 
 ('NMR', 'NmrProject', 'connectedStretchs', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:40_00001'), 
 ('NMR', 'NmrProject', 'guiTasks', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:46:55_00009'), 
 ('NMR', 'NmrProject', 'molSystem', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:34_00009'), 
 ('NMR', 'NmrProject', 'nmrChains', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00008'), 
 ('NMR', 'NmrProject', 'sequentialAssignments', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:49:39_00009'), 
 ('NMR', 'NmrProject', 'windowStore', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00002'), 
 ('NMR', 'Peak', 'heightError', 'www.ccpn.ac.uk_Fogh_2014-10-21-17:40:17_00001'), 
 ('NMR', 'Peak', 'peakViews', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00005'), 
 ('NMR', 'Peak', 'volumeError', 'www.ccpn.ac.uk_Fogh_2014-10-21-17:40:17_00002'), 
 ('NMR', 'PeakList', 'peakListViews', 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00009'), 
 ('NMR', 'PeakList', 'symbolColour', 'www.ccpn.ac.uk_Fogh_2014-10-28-18:26:00_00002'), 
 ('NMR', 'PeakList', 'symbolStyle', 'www.ccpn.ac.uk_Fogh_2014-10-28-18:26:00_00001'), 
 ('NMR', 'PeakList', 'textColour', 'www.ccpn.ac.uk_Fogh_2014-10-28-18:26:00_00003'), 
 ('NMR', 'Resonance', 'displayAxes', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:39:39_00001'), 
 ('NMR', 'Resonance', 'implName', 'www.ccpn.ac.uk_Fogh_2014-12-30-11:21:22_00002'), 
 ('NMR', 'ResonanceGroup', 'activeStretch', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00004'), 
 ('NMR', 'ResonanceGroup', 'mainResonanceGroup', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:41_00004'), 
 ('NMR', 'ResonanceGroup', 'nmrChain', 'www.ccpn.ac.uk_Fogh_2014-07-30-17:44:23_00001'), 
 ('NMR', 'ResonanceGroup', 'relativeOffset', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:41_00006'), 
 ('NMR', 'ResonanceGroup', 'residueType', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:41_00005'), 
 ('NMR', 'ResonanceGroup', 'satelliteResonanceGroups', 'www.ccpn.ac.uk_Fogh_2014-08-01-13:41:41_00003'), 
 ('NMR', 'ResonanceGroup', 'seqCode', 'www.ccpn.ac.uk_Fogh_2014-09-09-15:47:03_00001'), 
 ('NMR', 'ResonanceGroup', 'seqInsertCode', 'www.ccpn.ac.uk_Fogh_2014-09-09-15:47:03_00002'), 
 ('NMR', 'ResonanceGroup', 'spectrumDisplays', 'www.ccpn.ac.uk_Fogh_2014-11-04-17:51:55_00008'), 
 ('NMR', 'SequentialAssignment', None, 'www.ccpn.ac.uk_Fogh_2014-11-17-17:48:52_00001'), 
 ('NMR', 'SequentialAssignment', 'connectedStretchs', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00013'), 
 ('NMR', 'SequentialAssignment', 'isActive', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00015'), 
 ('NMR', 'SequentialAssignment', 'name', 'www.ccpn.ac.uk_Fogh_2014-11-17-17:50:06_00014'), 
 ('NMR', 'ShiftList', 'autoUpdate', 'www.ccpn.ac.uk_Fogh_2014-10-21-17:40:17_00003'), 
 ('NMRC', 'AbstractConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00002'), 
 ('NMRC', 'AbstractConstraintList', 'potentialType', 'www.ccpn.ac.uk_Fogh_2014-12-30-17:00:55_00001'), 
 ('NMRC', 'ChemShiftItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00008'), 
 ('NMRC', 'ChemicalShiftConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00002'), 
 ('NMRC', 'ChemicalShiftContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00007'), 
 ('NMRC', 'ChemicalShiftContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00004'), 
 ('NMRC', 'ConstraintContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00001'), 
 ('NMRC', 'ConstraintContribution', 'additionalLowerLimit', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00011'), 
 ('NMRC', 'ConstraintContribution', 'additionalUpperLimit', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00010'), 
 ('NMRC', 'ConstraintContribution', 'combinationId', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00012'), 
 ('NMRC', 'ConstraintContribution', 'error', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00007'), 
 ('NMRC', 'ConstraintContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00004'), 
 ('NMRC', 'ConstraintContribution', 'lowerLimit', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00009'), 
 ('NMRC', 'ConstraintContribution', 'targetValue', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00006'), 
 ('NMRC', 'ConstraintContribution', 'upperLimit', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:51_00008'), 
 ('NMRC', 'ConstraintContribution', 'weight', 'www.ccpn.ac.uk_Fogh_2014-12-30-17:17:11_00001'), 
 ('NMRC', 'ConstraintItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00004'), 
 ('NMRC', 'CsaConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00008'), 
 ('NMRC', 'CsaContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00009'), 
 ('NMRC', 'CsaContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00001'), 
 ('NMRC', 'CsaItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00010'), 
 ('NMRC', 'DihedralConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00005'), 
 ('NMRC', 'DihedralContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00001'), 
 ('NMRC', 'DihedralContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00007'), 
 ('NMRC', 'DihedralItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00002'), 
 ('NMRC', 'DistanceConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00003'), 
 ('NMRC', 'DistanceContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00002'), 
 ('NMRC', 'DistanceContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00005'), 
 ('NMRC', 'DistanceItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00003'), 
 ('NMRC', 'FixedResonance', 'chainCode', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:33_00001'), 
 ('NMRC', 'FixedResonance', 'chemShiftItems', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:25_00005'), 
 ('NMRC', 'FixedResonance', 'csaItems', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00002'), 
 ('NMRC', 'FixedResonance', 'dihedralItems', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00008'), 
 ('NMRC', 'FixedResonance', 'distanceItems', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00006'), 
 ('NMRC', 'FixedResonance', 'hBondItems', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00013'), 
 ('NMRC', 'FixedResonance', 'jCouplingItem', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00020'), 
 ('NMRC', 'FixedResonance', 'rdcItems', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00014'), 
 ('NMRC', 'FixedResonance', 'residueType', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:33_00003'), 
 ('NMRC', 'FixedResonance', 'sequenceCode', 'www.ccpn.ac.uk_Fogh_2014-07-18-18:10:33_00002'), 
 ('NMRC', 'HBondConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00010'), 
 ('NMRC', 'HBondContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00005'), 
 ('NMRC', 'HBondContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00012'), 
 ('NMRC', 'HBondItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00006'), 
 ('NMRC', 'JCouplingConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00017'), 
 ('NMRC', 'JCouplingContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00007'), 
 ('NMRC', 'JCouplingContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-22-17:05:55_00019'), 
 ('NMRC', 'JCouplingItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-22-17:02:49_00008'), 
 ('NMRC', 'NmrConstraintStore', 'details', 'www.ccpn.ac.uk_Fogh_2014-12-30-14:45:38_00001'), 
 ('NMRC', 'RdcConstraint', 'contributions', 'www.ccpn.ac.uk_Fogh_2014-07-29-17:21:12_00002'), 
 ('NMRC', 'RdcConstraintList', 'tensorChainCode', 'www.ccpn.ac.uk_Fogh_2015-01-01-08:17:19_00003'), 
 ('NMRC', 'RdcConstraintList', 'tensorMagnitude', 'www.ccpn.ac.uk_Fogh_2015-01-01-08:17:19_00001'), 
 ('NMRC', 'RdcConstraintList', 'tensorResidueType', 'www.ccpn.ac.uk_Fogh_2015-01-01-08:17:19_00005'), 
 ('NMRC', 'RdcConstraintList', 'tensorRhombicity', 'www.ccpn.ac.uk_Fogh_2015-01-01-08:17:19_00002'), 
 ('NMRC', 'RdcConstraintList', 'tensorSequenceCode', 'www.ccpn.ac.uk_Fogh_2015-01-01-08:17:19_00004'), 
 ('NMRC', 'RdcContribution', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00004'), 
 ('NMRC', 'RdcContribution', 'items', 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:26_00013'), 
 ('NMRC', 'RdcItem', None, 'www.ccpn.ac.uk_Fogh_2014-07-29-12:54:23_00005'), 
 ('NMRX', 'RefExpDimRef', 'axisCode', 'www.ccpn.ac.uk_Fogh_2014-11-28-21:31:23_00001'), 
]

# Class elements that exist in both models but that require handcode for
# transfer. E.g. elements that go from derived to non-derived.
# Note that old derivation functions can not be relied on to work during
# data transfer
# (prefix, typeName, elemName, newGuid, elemType)
neutraliseElements = [
]

# Differences between equivalent classElements and AbstractDataTypes :

# name changes
# (prefix, typeName, elemName, newName, newGuid
renames = [
 ('NMR', 'ExpDimRef', 'name', 'axisCode', 'www.ccpn.ac.uk_Fogh_2008-04-10-18:39:49_00006'), 
 ('NMRC', 'ChemShiftConstraint', None, 'ChemicalShiftConstraint', 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:51_00029'), 
 ('NMRC', 'ChemShiftConstraint', 'parentList', 'ChemicalShiftConstraint', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:10_00035'), 
 ('NMRC', 'ChemShiftConstraint', 'resonance', 'ChemicalShiftConstraint', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:10_00033'), 
 ('NMRC', 'ChemShiftConstraintList', None, 'ChemicalShiftConstraintList', 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:51_00030'), 
 ('NMRC', 'ChemShiftConstraintList', 'constraints', 'ChemicalShiftConstraintList', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:10_00036'), 
 ('NMRC', 'ChemShiftConstraintList', 'isotopeCode', 'ChemicalShiftConstraintList', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:10_00038'), 
 ('NMRC', 'FixedResonance', 'chemShiftConstraints', 'chemicalShiftConstraints', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:10_00032'), 
]

# ValueType changes
# change types are : 'ignore': do nothing, 'delay': available for calculation
# (prefix, typeName, elemName, action, newGuid, elemMap, valueTypeGuid)
typeChanges = [
]

# Different elements with matching qualifiedNames
# (element.qName, differentTags, oldGuid, newGuid
nameMatches = [
]

# Differences for matching elements, 
# excluding those where only names and/or valueTypes differ
# (oldElem.qName, newElem.name, oldGuid, newGuid, differentTags
allDiffs = [
 ('ccp.nmr.Nmr.ExpDimRef.refExpDimRef', 'refExpDimRef', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00025', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00025', {'isDerived'}), 
 ('ccp.nmr.Nmr.Experiment.refExperiment', 'refExperiment', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:06_00008', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:06_00008', {'isDerived', 'partitionsChildren'}), 
 ('ccp.nmr.Nmr.Resonance.name', 'name', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:10_00009', 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:10_00009', {'locard', 'documentation', 'isDerived'}), 
 ('molsim.Symmetry.MolSystemSymmetrySet', 'MolSystemSymmetrySet', 'www.ccpn.ac.uk_Fogh_2008-02-20-18:17:09_00001', 'www.ccpn.ac.uk_Fogh_2008-02-20-18:17:09_00001', {'parentRole'}), 
]
