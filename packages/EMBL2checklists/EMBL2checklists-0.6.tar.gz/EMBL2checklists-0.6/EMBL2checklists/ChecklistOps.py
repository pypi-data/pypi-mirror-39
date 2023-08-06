# -*- coding: utf-8 -*-

'''
Custom operations to generate ENA checklists
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
__version__ = '2018.09.25.1600'

#############
# DEBUGGING #
#############
import pdb
# pdb.set_trace()

###########
# CLASSES #
###########

class Writer:
    ''' This class contains functions to write tab-separated 
    spreadsheets (checklists) for submission via the interactive WEBIN 
    checklist submission system. '''

    def __init__(self):
        pass

    def deleteEmptyKeys(self, checklist_type, outp_handle):
        ''' This function deletes unnecessary keys
        Args:
            checklist_type (string)
            outp_handle (list)
        Returns:
            keys (list)
        '''
        keys = GlobVars.GlobalVariables().getQualifiers(checklist_type, 'om')
        toDelete = []
        for i in keys:
            prev = ''
            isEmpty = False
            for j in range(len(outp_handle)):
                try:
                    if prev == outp_handle[j][i]:
                        prev = outp_handle[j][i]
                        isEmpty = True
                    else:
                        isEmpty = False
                        break
                except:
                    isEmpty = True
            if isEmpty:
                toDelete.append(i)
        for delete in toDelete:
            j = 0
            for i in range(len(keys)):
                if keys[j] == delete:
                    del keys[j]
                else:
                    j = j + 1
        return keys

    def writer(self, checklist_type, outp_handle, outp_file):
        ''' This function writes a tab-separated spreadsheet 
        (checklist) for submission via the interactive WEBIN 
        checklist submission system.
        Args:
            checklist_type (string)
            outp_handle (list)
            outp_file (obj)
        Returns:
            currently nothing; writes string to file
        '''
        translator = GlobVars.GlobalVariables().getTranslator(checklist_type)
        keys = self.deleteEmptyKeys(checklist_type, outp_handle)
        for out_list in outp_handle:
            for key in keys:
                try:
                    out_list[translator[key]] = out_list.pop(key)
                except:
                    pass
        for i in range(len(keys)):
            keys[i] = translator[keys[i]]
        out_string = '\t'.join(keys) + '\n'
        outp_file.write(out_string)
        for out_list in outp_handle:
            out_array = []
            for key in keys:
                    try:
                        out_array.append(out_list[key])
                    except:
                        out_array.append('')
            out_string = '\t'.join(out_array) + '\n'
            outp_file.write(out_string)

class Parser:
    ''' This class contains functions to parse information from
    BioPython sequence records. '''

    def __init__(self):
        pass

########################################################################

    def extract_features_by_type(self, feature_list, feature_type):
        ''' This function extracts specific features from a feature list.
        Args:
            feature_list (list)
            feature_type (string)
        Returns:
            out_feature_list (list)
        Raises:
            GlobVars.warnings
        '''
        try:
            out_feature_list = []
            for f in [f for f in feature_list if f.type==feature_type]:
                if any(x in f.qualifiers for x in GlobVars.standard_qualifiers):
                    out_feature_list.append(f)
        except:
            GlobVars.warnings.append('WARNING: Extraction of feature `%s` unsuccessful.' % (feature_type))
        return out_feature_list

    def extract_qualifier_info(self, feature_list, qualifier_name):
        ''' This function extracts qualifier info from a feature list.
        Args:
            feature_list (list)
            qualifier_name (string)
        Returns:
            qualifier_info (string)
        Raises:
            GlobVars.warnings
        '''
        try:
            qualifier_list = sum([f.qualifiers[qualifier_name] for f in feature_list], [])
            qualifier_info = " ".join(qualifier_list)
        except:
            GlobVars.warnings.append('WARNING: Extraction of qualifier `%s` unsuccessful.' % (qualifier_name))
        return qualifier_info

    def extract_organism_name(self, feature_list):
        ''' This function extracts the organism name from a full 
        feature table (i.e., one that includes the source feature).
        Args:
            feature_list (list)
        Returns:
            organism_name (string)
        Raises:
            Exception
        '''
        try:
            organism_name = [f.qualifiers['organism'] for f in feature_list if f.type=='source'][0][0]
        except:
            raise Exception('ERROR: The mandatory source-qualifier ´%s´ is missing from record.' % ('organism'))
        return organism_name


    def extract_sequence(self, seq_record):
        ''' This function extracts the organism name from a full 
        feature table (i.e., one that includes the source feature).
        Args:
            seq_record (object)
        Returns:
            full_sequence (string)
        Raises:
            Exception
        '''
        try:
            full_sequence = str(seq_record.seq)
        except:
            raise Exception('ERROR: The DNA sequence could not be parsed from record ´%s´.' % (seq_record.id))
        return full_sequence


    def parse_marker_abbrevs(self, seq_record, target_qualifiers):
        ''' This function extracts the marker abbreviations from a 
        sequence record.
        Args:
            seq_record (SeqIO)
            target_qualifiers (list)
        Returns:
            marker_abbrev (list)
        Raises:
            Exception
        '''
        gene_qualifiers = [f.qualifiers for f in seq_record.features if not f.type=='source'] # Produces a list of dictionaries
        marker_abbrev = []
        # Extract marker abbreviations
        for keyw in target_qualifiers:
            for dct in gene_qualifiers:
                try:
                    marker_abbrev.extend(dct[keyw])
                except KeyError:
                    marker_abbrev = marker_abbrev
        # Parse raw list of marker abbreviations
        if marker_abbrev:
            # Extract all unique values in list, keep order of original list
            seen = set()
            marker_abbrev = [elem for elem in marker_abbrev if elem not in seen and not seen.add(elem)]
            # Remove any multi-word elements
            #marker_abbrev = [elem for elem in marker_abbrev if len(elem.split(" ")) == 1]
        else:
            raise Exception('ERROR: No marker abbreviation parsed successfully for record `%s`' % (seq_record.id))
        return marker_abbrev

########################################################################

##########################
## MANDATORY QUALIFIERS ##
##########################
    def mandatoryQualifiers(self, seq_record, marker_abbrev, counter, checklist_type, env_sample):
        ''' Fills the mandatory qualifiers for a specific checklist_type.
        Args:
            seq_record (BioPython object)
            marker_abbrev (list)
            counter (int)
            checklist_type (string)
            env_sample (string)
        Returns:
            outdict (dict) : if everything was successful
            False          : when something went wrong so the main function can skip
                             this seq_record
        Raises:
            nothing, as it give warnings for the specific seq_record
        '''

        outdict = GlobVars.GlobalVariables().getOutdict(GlobVars.GlobalVariables().getQualifiers(checklist_type, 'm'))

## CHECKLIST: INTERGENIC SPACER ##
##################################
        if checklist_type == 'IGS':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)
            
            # IGS
            try:
                misc_features = Parser().extract_features_by_type(seq_record.features, "misc_feature")
                misc_qualifiers = Parser().extract_qualifier_info(misc_features, "product")
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('misc_feature', seq_record.id))
                return False
            # GENES
            try:
                gene_features = Parser().extract_features_by_type(seq_record.features, "gene")
                gene_qualifiers = Parser().extract_qualifier_info(gene_features, "note")
            except:
                GlobVars.warnings.append('WARNING: The feature ´%s´ is missing from record ´%s´.' % ('gene', seq_record.id))
                return False

            # GENE1, G1PRESENT and GENE2, G2PRESENT
            try:
                IGS_qualifier = [i for i in misc_qualifiers.split() if "-" in i][0]
                gene1 = IGS_qualifier.split('-')[0]
                gene2 = IGS_qualifier.split('-')[1]
                outdict["gene1"] = gene1
                outdict["gene2"] = gene2
            except:
                GlobVars.warnings.append('WARNING: Parsing of ´%s´ from record ´%s´ was unsuccessful.' % ('the intergenic spacer qualifier', seq_record.id))
                return False
            try:
                if gene1 in gene_qualifiers:
                    outdict["g1present"] = 'yes'
                else:
                    outdict["g1present"] = 'no'
                if gene2 in gene_qualifiers:
                    outdict["g2present"] = 'yes'
                else:
                    outdict["g2present"] = 'no'
            except:
                GlobVars.warnings.append('WARNING: No genes detected to parse from record ´%s´.' % (seq_record.id))
                return False

                
## CHECKLIST: GENE_INTRON ##
############################
        elif checklist_type == 'gene_intron':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)

            # GENE
            try:
                gene_features = Parser().extract_features_by_type(seq_record.features, "gene")
                outdict["gene"] = [f.qualifiers['note'] for f in gene_features][0][0]
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('gene', seq_record.id))
                return False
            # INTRON
            try:
                intron_features = Parser().extract_features_by_type(seq_record.features, "intron")
                intron = [f for f in intron_features][0]
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('intron', seq_record.id))
                return False

            # 5' PARTIAL, 3' PARTIAL, 5' INTRON, 3' INTRON
            try:
                if type(intron.location.start) == Bio.SeqFeature.ExactPosition:
                    outdict["fiveprime_partial"] = 'no'
                if type(intron.location.start) == Bio.SeqFeature.BeforePosition:
                    outdict["fiveprime_partial"] = 'yes'
                if type(intron.location.end) == Bio.SeqFeature.ExactPosition:
                    outdict["threeprime_partial"] = 'no'
                if type(intron.location.end) == Bio.SeqFeature.AfterPosition:
                    outdict["threeprime_partial"] = 'yes'
                outdict["fiveprime_cds"] = str(intron.location.start.position+1)
                outdict["threeprime_cds"] = str(intron.location.end.position)
            except:
                GlobVars.warnings.append('WARNING: The parsing of ´%s´ from record ´%s´ was unsuccessful.' % ("the 5' and the 3' location information", seq_record.id))
                return False
            # INTRON NUMBER
            try:
                outdict["number"] = [f.qualifiers['number'] for f in intron_features][0][0]
            except:
                GlobVars.warnings.append('WARNING: The parsing of ´%s´ from record ´%s´ was unsuccessful.' % ("the intron number", seq_record.id))
                return False


## CHECKLIST: TRNK_MATK ##
##########################
        elif checklist_type == 'trnK_matK':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)
            
            # TRNK_INTRON
            try:
                intron_features = Parser().extract_features_by_type(seq_record.features, "intron")
                intron_qualifiers = Parser().extract_qualifier_info(intron_features, "gene")
                if len(intron_qualifiers) != 0:
                    try:
                        if 'trnK' in intron_qualifiers:
                            outdict['trnK_intron_present'] = 'yes'
                        else:
                            outdict['trnK_intron_present'] = 'no'
                    except:
                        GlobVars.warnings.append('WARNING: The parsing of %s from record ´%s´ was unsuccessful.' % ("the trnK intron information", seq_record.id))
                        return False
                else:
                    raise Exception
            except:
                try:
                    tRNA_features = Parser().extract_features_by_type(seq_record.features, "tRNA")
                    tRNA_qualifiers = Parser().extract_qualifier_info(tRNA_features, "gene")
                    if len(tRNA_qualifiers) != 0:
                        try:
                            if 'trnK' in tRNA_qualifiers:
                                outdict['trnK_intron_present'] = 'yes'
                            else:
                                outdict['trnK_intron_present'] = 'no'
                        except:
                            GlobVars.warnings.append('WARNING: The parsing of %s from record ´%s´ was unsuccessful.' % ("the trnK intron information", seq_record.id))
                            return False
                except:
                    GlobVars.warnings.append("WARNING: The mandatory feature combination of ´%s´ is missing from record ´%s´." % ("either an intron feature or a tRNA feature for trnK", seq_record.id))
                    return False
            
            # MATK GENE
            try:
                gene_features = Parser().extract_features_by_type(seq_record.features, "gene")
                matK_gene = [f for f in gene_features if 'matK' in f.qualifiers['note']][0]
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ for matK with qualifier ´%s´ is missing from record ´%s´.' % ('gene', 'note', seq_record.id))
                return False

            # 5'_CDS, 3'_CDS, 5'_PARTIAL and 3'_PARTIAL
            try:
                # 5'_CDS and 5'_PARTIAL
                # 5'_CDS: Start of the matK coding region relative to the submitted sequence. For a full length CDS this is the position of the first base of the start codon.
                # NOTE: One nucleotide position has to be added to the start position to make it correct.
                outdict["fiveprime_cds"] = str(matK_gene.location.start.position+1)
                # 5'_PARTIAL: cds partial at 5'? (yes/no) For an incomplete CDS with the start codon upstream of the submitted sequence.
                if type(matK_gene.location.start) == Bio.SeqFeature.ExactPosition:
                    outdict["fiveprime_partial"] = 'no'
                if type(matK_gene.location.start) == Bio.SeqFeature.BeforePosition:
                    outdict["fiveprime_partial"] = 'yes'
                # 3'_CDS and 3'_PARTIAL
                # 3'_CDS: End of the matK coding region relative to the submitted sequence. For a full length CDS this is the position of the last base of the stop codon.
                outdict["threeprime_cds"] = str(matK_gene.location.end.position)
                # 3'_PARTIAL: cds partial at 3'? (yes/no) For an incomplete CDS with the stop codon downstream of the submitted sequence.
                if type(matK_gene.location.end) == Bio.SeqFeature.ExactPosition:
                    outdict["threeprime_partial"] = 'no'
                if type(matK_gene.location.end) == Bio.SeqFeature.AfterPosition:
                    outdict["threeprime_partial"] = 'yes'
            except:
                GlobVars.warnings.append('WARNING: The parsing of ´%s´ from record ´%s´ was unsuccessful.' % ("the 5' and the 3' location information", seq_record.id))
                return False


## CHECKLIST: RRNA ##
#####################
        elif checklist_type == 'rRNA':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)
            # SEDIMENT
            try:
                rRNA_features = Parser().extract_features_by_type(seq_record.features, "rRNA")
                sediment_info = [f.qualifiers['product'] for f in rRNA_features][0][0]
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('rRNA', seq_record.id))
                return False
            try:
                if '5S' in sediment_info:
                    outdict["sediment"] = '5S'
                if '5.8S' in sediment_info:
                    outdict["sediment"] = '5.8S'
                if '12S' in sediment_info:
                    outdict["sediment"] = '12S'
                if '16S' in sediment_info:
                    outdict["sediment"] = '16S'
                if '18S' in sediment_info:
                    outdict["sediment"] = '18S'
                if '23S' in sediment_info:
                    outdict["sediment"] = '23S'
                if '25S' in sediment_info:
                    outdict["sediment"] = '25S'
                if '26S' in sediment_info:
                    outdict["sediment"] = '26S'
                if '28S' in sediment_info:
                    outdict["sediment"] = '28S'
            except:
                GlobVars.warnings.append('WARNING: No sediment info parsed from record ´%s´.' % (seq_record.id))
                return False


## CHECKLIST: ITS ##
####################
        elif checklist_type == 'ITS':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)
            
            # ISOLATION_SOURCE
            if env_sample.lower() == "yes":
                try:
                    source_features = Parser().extract_features_by_type(seq_record.features, "source")
                    outdict["isolation_source"] = [f.qualifiers['isolation_source'] for f in source_features][0][0]
                except:
                    GlobVars.warnings.append('WARNING: The mandatory source-qualifier ´%s´ is missing from record ´%s´.' % ('isolation_source', seq_record.id))
                    return False

            # 18S, 26S/28S
            try:
                rRNA_features = Parser().extract_features_by_type(seq_record.features, "rRNA")
                rRNA_qualifiers = Parser().extract_qualifier_info(rRNA_features, "gene")
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('rRNA', seq_record.id))
                return False
            # ITS1, ITS2
            try:
                    ITS_features = Parser().extract_features_by_type(seq_record.features, "misc_RNA")
                    ITS_qualifiers = Parser().extract_qualifier_info(ITS_features, "note")
            except:
                GlobVars.warnings.append('WARNING: The mandatory feature ´%s´ is missing from record ´%s´.' % ('misc_RNA', seq_record.id))
                return False
            # 18S, 26S/28S, ITS1, ITS2
            try:
                # 18S
                if '18S' in rRNA_qualifiers:
                    outdict["RNA_18S"] = 'yes'
                else:
                    outdict["RNA_18S"] = 'no'
                # 26S/28S
                if '28S' in rRNA_qualifiers or '26S' in rRNA_qualifiers:
                    outdict["RNA_28S"] = 'yes'
                else:
                    outdict["RNA_28S"] = 'no'
                # ITS1
                if 'ITS1' in ITS_features or '18S' in rRNA_qualifiers:
                    outdict["ITS1_feat"] = 'yes'
                else:
                    outdict["ITS1_feat"] = 'no'
                # ITS2
                if 'ITS' in ITS_features or ('28S' in rRNA_qualifiers or '26S' in rRNA_qualifiers):
                    outdict["ITS2_feat"] = 'yes'
                else:
                    outdict["ITS2_feat"] = 'no'
                # 5.8S # Note: The completeness of the rDNA gene 5.8S is inferred based on the presence of ITS1 and ITS2.
                if '5.8S' in rRNA_qualifiers:
                    outdict["RNA_58S"] = 'yes'
                elif 'ITS1' in ITS_features and 'ITS2' in ITS_features:
                    outdict["RNA_58S"] = 'yes'
                elif '28S' in rRNA_qualifiers and '26S' in rRNA_qualifiers:
                    outdict["RNA_58S"] = 'yes'
                else:
                    outdict["RNA_58S"] = 'no'
            except:
                GlobVars.warnings.append('WARNING: The parsing of ´%s´ from record ´%s´ was unsuccessful.' % ("the rDNA type", seq_record.id))
                return False


## CHECKLIST: ETS ##
####################
        elif checklist_type == 'ETS':
            # ENTRYNUMBER
            outdict["entrynumber"] = str(counter+1)
            # ORGANISM_NAME
            outdict["organism"] = Parser().extract_organism_name(seq_record.features)
            # ENV_SAMPLE
            outdict["env_sample"] = env_sample
            # SEQUENCE
            outdict["sequence"] = Parser().extract_sequence(seq_record)
            
            # INFER ETS TYPE
            try:
                rRNA_features = Parser().extract_features_by_type(seq_record.features, "rRNA")
                rRNA_qualifiers = Parser().extract_qualifier_info(rRNA_features, "gene")
            except:
                try:
                    ETS_features = Parser().extract_features_by_type(seq_record.features, "misc_RNA")
                    ETS_qualifiers = Parser().extract_qualifier_info(ETS_features, "note")
                except:
                    GlobVars.warnings.append("WARNING: The mandatory feature combination of ´%s´ is missing from record ´%s´." % ("either an rRNA feature for 18S or 26S/28S, or a misc_RNA for 5'ETS or 3'ETS", seq_record.id))
                    return False
            # ETS
            try:
                if '18S' in rRNA_qualifiers:
                    outdict["ets_type"] = "5'"
                elif '26S' in rRNA_qualifiers or '28S' in rRNA_qualifiers:
                    outdict["ets_type"] = "3'"
                else:
                    if "ETS" in ETS_qualifiers and "5'" in ETS_qualifiers:
                        outdict["ets_type"] = "5'"
                    if "ETS" in ETS_qualifiers and "3'" in ETS_qualifiers:
                        outdict["ets_type"] = "3'"
                    else:
                        outdict["ets_type"] = "5'"
            except:
                GlobVars.warnings.append('WARNING: The parsing of ´%s´ from record ´%s´ was unsuccessful.' % ("the ETS type", seq_record.id))
                return False


## RETURN OUTDICT
        return outdict

########################################################################

#########################
## OPTIONAL QUALIFIERS ##
#########################
    def optionalQualifiers(self, seq_record, cl_specific_opt_quals):
        ''' Fills the optional qualifiers for a specific checklist_type.
        Args:
            seq_record (SeqIO)
            cl_specific_opt_quals (list)
        Returns:
            opt_outdict (dict) : if everything was successful
            False          : when something went wrong so the main function can skip
                             this seq_record
        Raises:
            nothing, as it give warnings for the specific seq_record
        '''
        opt_outdict = {}

    # Check if qualifiers in checklist-specific qualifier list
        for i in seq_record.features:
            for j in [q for q in i.qualifiers if q in cl_specific_opt_quals]:
                opt_outdict.update({j:i.qualifiers[j][0]})

    ## PCR PRIMER ##
    ################
        try:
            pcrPrimers = [ i.split(",]") for i in [f.qualifiers['PCR_primers'] for f in seq_record.features if f.type=='source'][0][0].replace(" ","").split(",[") ]
            tmp = []
            for t in pcrPrimers:
                for i in t:
                    tmp.append(i.split(":"))
            pcrPrimers = tmp
            print pcrPrimers
            fwd_name = []
            fwd_seq = []
            rev_name = []
            rev_seq = []
            for i in pcrPrimers:
                if i[0].replace("[","").replace("]","") == 'fwd_name':
                    fwd_name.append(i[1])
                if i[0].replace("[","").replace("]","") == 'fwd_seq':
                    fwd_seq.append(i[1])
                if i[0].replace("[","").replace("]","") == 'rev_name':
                    rev_name.append(i[1])
                if i[0].replace("[","").replace("]","") == 'rev_seq':
                    rev_seq.append(i[1])
            for counter, elem in enumerate(fwd_name):
                opt_outdict.update({'fwd_name'+str(counter+1):elem})
            for counter, elem in enumerate(fwd_seq):
                opt_outdict.update({'fwd_seq'+str(counter+1):elem})
            for counter, elem in enumerate(rev_name):
                opt_outdict.update({'rev_name'+str(counter+1):elem})
            for counter, elem in enumerate(rev_seq):
                opt_outdict.update({'rev_seq'+str(counter+1):elem})
        except:
            pass

## RETURN OUTDICT
        return opt_outdict

########################################################################

