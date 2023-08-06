# -*- coding: utf-8 -*-

'''
Prerequisites for generating ENA checklists
'''

#####################
# IMPORT OPERATIONS #
#####################
import Bio
import globalVariables as GlobVars

###############
# AUTHOR INFO #
###############
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2018 Michael Gruenstaeudl'
__info__ = 'EMBL2checklists'
__version__ = '2018.09.18.1600'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

###########
# CLASSES #
###########
class Checker:
    ''' This class contains functions to check the minimal requirements for a sequence record. '''

    def __init__(self):
        pass

    def checkMinimalFeaturePrerequisites(self, checklist_type, marker_abbrev):
        '''Various checks to see if the checklist type matches the marker abbreviations
        Args:
            checklist_type [string]: user input that contains checklist abbreviation
            marker_abbrev  [list]  : list of the abbreviations of the sequence record
        Returns:
            Boolean: True if it matched, False if not
        Raises:
            Exception
        '''
        try:
            if checklist_type == 'ETS':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_ETS):
                    return True
            elif checklist_type == 'ITS':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_ITS):
                    return True
            elif checklist_type == 'rRNA':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_rRNA):
                    return True
            elif checklist_type == 'trnK_matK':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_trnKmatK):
                    return True
            elif checklist_type == 'IGS':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_IGS):
                    return True
            elif checklist_type == 'gene_intron':
                if any(e in " ".join(marker_abbrev) for e in GlobVars.keywords_gene_intron):
                    return True
            else:
                raise Exception('ERROR: Variable ´checklist_type´ not identified.')
        except:
            raise Exception('WARNING: Not checklist-specific keyword is found among the marker abbreviations.')
