# -*- coding: utf-8 -*-

'''
Setting global variables
'''

#####################
# IMPORT OPERATIONS #
#####################
#import collections

###############
# AUTHOR INFO #
###############
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>,\
              Yannick Hartmaring <yanjo@zedat.fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2018 Michael Gruenstaeudl'
__info__ = 'EMBL2checklists'
__version__ = '2018.09.25.1600'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

#############
# VARIABLES #
#############

implemented_checklists = ['IGS', 'gene_intron', 'trnK_matK', 'rRNA', 'ITS', 'ETS']

standard_qualifiers = ['gene', 'note', 'product', 'standard_name', 'number']

keywords_IGS = ['IGS', 'spacer', 'intergenic spacer']
keywords_gene_intron = ['gene', 'intron']
keywords_trnKmatK = ['trnK', 'matK']
keywords_rRNA = ['18S', '28S', '5.8S']
keywords_ITS = ['ITS', 'ITS1', 'ITS2', 'internal transcribed']
keywords_ETS = ['ETS', 'external transcribed']

warnings = []

###########
# CLASSES #
###########
class GlobalVariables():

    def __init__(self):
        self.ITS_translator = {}
        self.qualifiers = {'rRNA':[['entrynumber','m'],['organism','m'],['organelle','o'],['env_sample','m'],['sediment','m'],
                                   ['strain','o'],['clone','o'],['isolate','o'],['isolation_source','o'],['cultivar','o'],
                                   ['variety','o'],['ecotype','o'],['breed','o'],['specimen_voucher','o'],['bio_material','o'],
                                   ['country','o'],['locality','o'],['lat_lon','o'],['haplotype','o'],['collection_date','o'],
                                   ['sex','o'],['mating_type','o'],['tissue_type','o'],['host','o'],['lab_host','o'],['fwd_name1','o'],
                                   ['fwd_seq1','o'],['rev_name1','o'],['rev_seq1','o'],['fwd_name2','o'],['fwd_seq2','o'],['rev_name2','o'],
                                   ['rev_seq2','o'],['sequence','m']],
                            'ITS':[['entrynumber','m'],['organism','m'],['strain','o'],['clone','o'],['isolate','o'],
                                   ['env_sample','m'],['isolation_source','o'],['culture_collection','o'],['country','o'],['locality','o'],
                                   ['lat_lon','o'],['host','o'],['collection_date','o'],['collected_by','o'],['identified_by','o'],
                                   ['variety','o'],['cultivar','o'],['ecotype','o'],['specimen_voucher','o'],['fwd_name1','o'],
                                   ['fwd_seq1','o'],['rev_name1','o'],['rev_seq1','o'],['fwd_name2','o'],['fwd_seq2','o'],['rev_name2','o'],
                                   ['rev_seq2','o'],['RNA_18S','m'],['ITS1_feat','m'],['RNA_58S','m'],['ITS2_feat','m'],['RNA_28S','m'],
                                   ['sequence','m']],
                      'trnK_matK':[['entrynumber','m'],['organism','m'],['fiveprime_cds','m'],['threeprime_cds','m'],
                                   ['fiveprime_partial','m'],['threeprime_partial','m'],['codon_start','o'],
                                   ['trnK_intron_present','m'],['clone','o'],['isolate','o'],['tissue_type','o'],
                                   ['subspecies','o'],['cultivar','o'],['variety','o'],['ecotype','o'],['specimen_voucher','o'],
                                   ['bio_material','o'],['locality','o'],['lat_lon','o'],['isolation_source','o'],
                                   ['collection_date','o'],['fwd_name1','o'],['fwd_seq1','o'],['rev_name1','o'],['rev_seq1','o'],
                                   ['fwd_name2','o'],['fwd_seq2','o'],['rev_name2','o'],['rev_seq2','o'],['sequence','m']],
                            'IGS':[['entrynumber','m'],['organism','m'],['env_sample','m'],['strain','o'],['haplotype','o'],
                                   ['gene1','m'],['g1present','m'],['gene2','m'],['g2present','m'],['organelle','o'],
                                   ['clone','o'],['isolate','o'],['isolation_source','o'],['cultivar','o'],['variety','o'],
                                   ['ecotype','o'],['breed','o'],['culture_collection','o'],['specimen_voucher','o'],
                                   ['bio_material','o'],['country','o'],['locality','o'],['lat_lon','o'],['collection_date','o'],
                                   ['collected_by','o'],['sex','o'],['mating_type','o'],['tissue_type','o'],['dev_stage','o'],
                                   ['cell_type','o'],['host','o'],['lab_host','o'],['fwd_name1','o'],['fwd_seq1','o'],
                                   ['rev_name1','o'],['rev_seq1','o'],['fwd_name2','o'],['fwd_seq2','o'],['rev_name2','o'],
                                   ['rev_seq2','o'],['sequence','m']],
                            'ETS':[['entrynumber','m'],['organism','m'],['ets_type','m'],['isolate','o'],['clone','o'],
                                   ['strain','o'],['variety','o'],['breed','o'],['ecotype','o'],['mating_type','o'],
                                   ['sex','o'],['isolation_source','o'],['host','o'],['tissue_type','o'],['country','o'],
                                   ['locality','o'],['lat_lon','o'],['collection_date','o'],['collected_by','o'],
                                   ['culture_collection','o'],['specimen_voucher','o'],['bio_material','o'],['fwd_name1','o'],
                                   ['fwd_seq1','o'],['rev_name1','o'],['rev_seq1','o'],['fwd_name2','o'],['fwd_seq2','o'],['rev_name2','o'],
                                   ['rev_seq2','o'],['sequence','m']],
                    'gene_intron':[['entrynumber','m'],['organism','m'],['organelle','o'],['env_sample','m'],['gene','m'],
                                   ['fiveprime_partial','m'],['threeprime_partial','m'],['fiveprime_intron','m'],['threeprime_intron','m'],
                                   ['number','m'],['strain','o'],['clone','o'],['isolate','o'],['isolation_source','o'],['plasmid','o'],
                                   ['chromosome','o'],['haplotype','o'],['cultivar','o'],['variety','o'],['ecotype','o'],['breed','o'],
                                   ['culture_collection','o'],['specimen_voucher','o'],['bio_material','o'],['country','o'],['locality','o'],
                                   ['lat_lon','o'],['collection_date','o'],['sex','o'],['mating_type','o'],['tissue_type','o'],['host','o'],
                                   ['lab_host','o'],['fwd_name1','o'],['fwd_seq1','o'],['rev_name1','o'],['rev_seq1','o'],['fwd_name2','o'],
                                   ['fwd_seq2','o'],['rev_name2','o'],['rev_seq2','o'],['sequence','m']]
                                }

        self.translator = {'rRNA':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM_NAME','organelle':'ORGANELLE','env_sample':'ENV_SAMPLE',
                                   'sediment':'SEDIMENT','strain':'STRAIN','clone':'CLONE','isolate':'ISOLATE','isolation_source':'ISOLATION_SOURCE',
                                   'cultivar':'CULTIVAR','variety':'VARIETY','ecotype':'ECOTYPE','breed':'BREED','specimen_voucher':'SPEC_VOUCH',
                                   'bio_material':'BIO_MAT','country':'COUNTRY','locality':'LOCALITY','lat_lon':'LAT_LON','haplotype':'HAPLOTYPE',
                                   'collection_date':'COLDATE','sex':'SEX','mating_type':'MATING_TYPE','tissue_type':'TISSUE','host':'HOST',
                                   'lab_host':'LAB_HOST','fwd_name1':'FWD_NAME1','fwd_seq1':'FWD_SEQ1','rev_name1':'REV_NAME1','rev_seq1':'REV_SEQ1',
                                   'fwd_name2':'FWD_NAME2','fwd_seq2':'FWD_SEQ2','rev_name2':'REV_NAME2','rev_seq2':'REV_SEQ2','sequence':'SEQUENCE'},
                            'ITS':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM','strain':'STRAIN','clone':'CLONE','isolate':'ISOLATE',
                                   'env_sample':'ENVSAM','isolation_source':'ISOSOURCE','culture_collection':'CULTCOLL','country':'COUNTRY',
                                   'locality':'LOCALITY','lat_lon':'LATLON','host':'HOST','collection_date':'COLDATE','collected_by':'COLBY',
                                   'identified_by':'IDBY','variety':'VARIETY','cultivar':'CULTIVAR','ecotype':'ECOTYPE','specimen_voucher':'SPECHVOUCH',
                                   'fwd_name1':'PFNAME1','fwd_seq1':'PFSEQ1','rev_name1':'PRNAME1','rev_seq1':'PRSEQ1','fwd_name2':'PFNAME2',
                                   'fwd_seq2':'PFSEQ2','rev_name2':'PRNAME2','rev_seq2':'PRSEQ2','RNA_18S':'18S','ITS1_feat':'ITS1',
                                   'RNA_58S':'5.8S','ITS2_feat':'ITS2','RNA_28S':'28S','sequence':'SEQUENCE'},
                      'trnK_matK':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM_NAME','fiveprime_cds':"5'_CDS",'threeprime_cds':"3'_CDS",
                                   'fiveprime_partial':"5'_PARTIAL",'threeprime_partial':"3'_PARTIAL",'codon_start':'CODONSTART','trnK_intron_present':'INTRON',
                                   'clone':'CLONE','isolate':'ISOLATE','tissue_type':'TISSUE','subspecies':'SUBSPECIES','cultivar':'CULTIVAR','variety':'VARIETY',
                                   'ecotype':'ECOTYPE','specimen_voucher':'SPEC_VOUCH','bio_material':'BIO_MAT','locality':'LOCALITY',
                                   'lat_lon':'LAT_LON','isolation_source':'ISOLATION_SOURCE','collection_date':'COLDATE','collected_by':'COL_BY',
                                   'fwd_name1':'FWD_NAME1','fwd_seq1':'FWD_SEQ1','rev_name1':'REV_NAME1','rev_seq1':'REV_SEQ1',
                                   'fwd_name2':'FWD_NAME2','fwd_seq2':'FWD_SEQ2','rev_name2':'REV_NAME2','rev_seq2':'REV_SEQ2',
                                   'sequence':'SEQUENCE'},
                            'IGS':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM_NAME','env_sample':'ENV_SAMPLE','strain':'STRAIN',
                                   'haplotype':'HAPLOTYPE','gene1':'GENE1','g1present':'G1PRESENT','gene2':'GENE2','g2present':'G2PRESENT',
                                   'organelle':'ORGANELLE','clone':'CLONE','isolate':'ISOLATE','isolation_source':'ISOLATION_SOURCE',
                                   'cultivar':'CULTIVAR','variety':'VARIETY','ecotype':'ECOTYPE','breed':'BREED','culture_collection':'CULT_COLL',
                                   'specimen_voucher':'SPEC_VOUCH','bio_material':'BIO_MAT','country':'COUNTRY','locality':'LOCALITY',
                                   'lat_lon':'LAT_LON','collection_date':'COLDATE','collected_by':'COL_BY','sex':'SEX','mating_type':'MATING_TYPE',
                                   'tissue_type':'TISSUE','dev_stage':'DEV_STAGE','cell_type':'CELL_TYPE','host':'HOST','lab_host':'LAB_HOST',
                                   'fwd_name1':'FWD_NAME1','fwd_seq1':'FWD_SEQ1','rev_name1':'REV_NAME1','rev_seq1':'REV_SEQ1',
                                   'fwd_name2':'FWD_NAME2','fwd_seq2':'FWD_SEQ2','rev_name2':'REV_NAME2','rev_seq2':'REV_SEQ2',
                                   'sequence':'SEQUENCE'},
                            'ETS':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM_NAME','ets_type':'ETS_TYPE','isolate':'ISOLATE',
                                   'clone':'CLONE','strain':'STRAIN','variety':'VARIETY','cultivar':'CULTIVAR','breed':'BREED', 'culture_collection':'CULT_COLL',
                                   'ecotype':'ECOTYPE','mating_type':'MATING_TYPE','sex':'SEX','isolation_source':'ISOLATION_SOURCE',
                                   'host':'HOST','tissue_type':'TISSUE','country':'COUNTRY','locality':'LOCALITY','lat_lon':'LAT_LON',
                                   'collection_date':'COLDATE','collected_by':'COL_BY','specimen_voucher':'SPEC_VOUCH','bio_material':'BIO_MAT',
                                   'fwd_name1':'FWD_NAME1','fwd_seq1':'FWD_SEQ1','rev_name1':'REV_NAME1','rev_seq1':'REV_SEQ1',
                                   'fwd_name2':'FWD_NAME2','fwd_seq2':'FWD_SEQ2','rev_name2':'REV_NAME2','rev_seq2':'REV_SEQ2',
                                   'sequence':'SEQUENCE'},
                    'gene_intron':{'entrynumber':'ENTRYNUMBER','organism':'ORGANISM_NAME','env_sample':'ENV_SAMPLE','organelle':'ORGANELLE',
                                   'gene':'GENE','fiveprime_partial':"5'_PARTIAL",
                                   'threeprime_partial':"3'_PARTIAL",'fiveprime_intron':"5'_INTRON",'threeprime_intron':"3'_INTRON",
                                   'number':'NUMBER','strain':'STRAIN','clone':'CLONE','isolate':'ISOLATE','isolation_source':'ISOLATION_SOURCE',
                                   'plasmid':'PLASMID','chromosome':'CHROMOSOME','haplotype':'HAPLOTYPE','cultivar':'CULTIVAR','variety':'VARIETY',
                                   'ecotype':'ECOTYPE','breed':'BREED','culture_collection':'CULT_COLL','specimen_voucher':'SPEC_VOUCH',
                                   'bio_material':'BIO_MAT','country':'COUNTRY','locality':'LOCALITY','lat_lon':'LAT_LON','collection_date':'COLDATE',
                                   'sex':'SEX','mating_type':'MATING_TYPE','tissue_type':'TISSUE','host':'HOST','lab_host':'LAB_HOST',
                                   'fwd_name1':'FWD_NAME1','fwd_seq1':'FWD_SEQ1','rev_name1':'REV_NAME1','rev_seq1':'REV_SEQ1',
                                   'fwd_name2':'FWD_NAME2','fwd_seq2':'FWD_SEQ2','rev_name2':'REV_NAME2','rev_seq2':'REV_SEQ2',
                                   'sequence':'SEQUENCE'}
                                }

#############
# FUNCTIONS #
#############
    def getQualifiers(self, checklist_type, status):
        ''' Combine mandatory and optional qualifiers for specific checklist type
        Args:
            checklist_type (string)
            status [string]: 'o' for optional, 'm' manatory and 'om' for both
        Returns:
            qualifiers (list)
        '''
        qualifiers = []
        for quali in self.qualifiers[checklist_type]:
            if quali[1] in status:
                qualifiers.append(quali[0])
        return qualifiers

    def getOutdict(self, outlist):
        outdict = {}
        for elem in outlist:
            outdict.update({elem:''})
        return outdict

    def getTranslator(self, checklist_type):
        return self.translator[checklist_type]
