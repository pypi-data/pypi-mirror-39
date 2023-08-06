# -*- coding: utf-8 -*-

'''
Main operations in EMBL2checklists
'''

#####################
# IMPORT OPERATIONS #
#####################
import ChecklistOps as ClOps
import PrerequisiteOps as PreOps
import globalVariables as GlobVars

import sys, os
from Bio import SeqIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'EMBL2checklists'))

###############
# AUTHOR INFO #
###############
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2018 Michael Gruenstaeudl'
__info__ = 'EMBL2checklists'
__version__ = '2018.09.18.1700'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

#############
# FUNCTIONS #
#############

def EMBL2checklists(path_to_embl, path_to_outfile, file_format="embl", checklist_type=None, env_sample="no"):
    ''' Primary code function; it executes all subfunctions in the correct order
    Args:
        path_to_embl (string)
        path_to_outfile (string)
        checklist_type (string)
        file_format (string)
        env_sample (string)
    Returns:
        bool: True if nothing went wrong
    Raises:
        Pass exceptions to GUI or CMD interface
    '''

# 1. OPEN OUTHANDLE
    outp_handle = []

# 2. PARSE DATA FROM EMBL-FILE
    try:
        seq_records = SeqIO.parse(open(path_to_embl, "r"), file_format)
    except:
        raise Exception('ERROR: The file ´%s´ could not be parsed.' % (path_to_embl))

# 3. CONVERSION TO CHECKLISTS
    for counter, seq_record in enumerate(seq_records): # Looping through records
        try:
            outdict = {}
    # 3.1. Extraction of marker abbreviations
            marker_abbrevs = ClOps.Parser().parse_marker_abbrevs(seq_record, GlobVars.standard_qualifiers)

    # 3.2. Check if minimal feature prerequisites present; if not, skip this seq_record
            try:
                PreOps.Checker().checkMinimalFeaturePrerequisites(checklist_type, marker_abbrevs)
            except Exception as e:
                GlobVars.warnings.append('WARNING: %s \nSelected checklist type: `%s`; Identified marker abbrevs: `%s` \nSkipping record `%s`...' % (e, checklist_type, marker_abbrevs, seq_record.id))
                continue # Close current loop iteration and continue with next iteration

    # 3.3. Conversion to checklist format
            outdict = ClOps.Parser().mandatoryQualifiers(seq_record, marker_abbrevs, counter, checklist_type, env_sample)

    # 3.4. Optional qualifiers will be added as long as outdict true
            if outdict:
                optional_qualifiers = ClOps.Parser().optionalQualifiers(seq_record, GlobVars.GlobalVariables().getQualifiers(checklist_type, 'o'))
                outdict.update(optional_qualifiers)

    # 3.5. Write parsed record information to handle
            outp_handle.append(outdict)

        except Exception as error:
            raise error

# 4. CLOSE OUTFILE (unless uncaught exceptions)
    outp_file = open(path_to_outfile,"w")
    ClOps.Writer().writer(checklist_type, outp_handle, outp_file)
    outp_file.close()

# 5. RETURN TRUE (unless uncaught exceptions)
    return True
