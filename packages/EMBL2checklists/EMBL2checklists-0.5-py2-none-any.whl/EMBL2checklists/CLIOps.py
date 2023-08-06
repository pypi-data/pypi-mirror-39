# -*- coding: utf-8 -*-

'''
CLI operations in EMBL2checklists
'''

#####################
# IMPORT OPERATIONS #
#####################
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'EMBL2checklists'))

import EMBL2checklistsMain as E2C
import globalVariables as GlobVars

###############
# AUTHOR INFO #
###############
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2018 Michael Gruenstaeudl'
__info__ = 'EMBL2checklists'
__version__ = '2018.11.30.1800'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

############
# ARGPARSE #
############

class CLI():

    def __init__(self):
        self.cli()

    def cli(self):

        import argparse
        parser = argparse.ArgumentParser(description="  --  ".join([__author__, __copyright__, __info__, __version__]))
        # Mandatory commandline arguments
        parser.add_argument('-i',
                            '--infile',
                            help='absolute path to infile; infile in EMBL or GenBank flatfile format; Example: /path_to_input/test.embl',
                            default='/home/username/Desktop/test.embl',
                            required=True)
        parser.add_argument('-o',
                            '--outfile',
                            help='absolute path to outfile; outfile in ENA Webin checklist format (tsv-format); Example: /path_to_output/test.tsv',
                            default='/home/username/Desktop/test.tsv',
                            required=True)
        parser.add_argument('-c',
                            '--cltype',
                            help='Any of the currently implemented checklist types:' + ", ".join(GlobVars.implemented_checklists),
                            default=None,
                            required=True)
        parser.add_argument('-e',
                            '--environmental',
                            help="Is your organism from an environmental/uncultured sample? (yes/no)",
                            required=True)
        parser.add_argument('--version',
                            help='Print version information and exit',
                            action='version',
                            version=__info__ + ", version: " + __version__)
        args = parser.parse_args()


        try:
            if args.cltype in GlobVars.implemented_checklists:
                if args.infile.split('.')[-1] == 'embl':
                    E2C.EMBL2checklists(args.infile, args.outfile, 'embl', args.cltype, args.environmental)
                    if len(GlobVars.warnings) != 0:
                        for warning in GlobVars.warnings:
                            print warning
                    print "PROCESS COMPLETE.\nOutput location: " + args.outfile
                elif args.infile.split('.')[-1] == 'gb':
                    E2C.EMBL2checklists(args.infile, args.outfile, 'gb', args.cltype, args.environmental)
                    if len(GlobVars.warnings) != 0:
                        for warning in GlobVars.warnings:
                            print warning
                    print "PROCESS COMPLETE.\nOutput location: " + args.outfile
                else:
                    raise Exception('ERROR: The file ending of ´%s´ does not match any of the permissible flatfile formats (.embl, .gb).' % (args.infile))
            else:
                raise Exception('ERROR: The selection ´%s´ is not an implemented checklist type.' % (args.cltype))
        except Exception as e:
            print e


########
# MAIN #
########

def start_EMBL2checklists_CLI():
    CLI()
