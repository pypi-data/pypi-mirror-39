##
# File:    DictMethodRunnerHelper.py
# Author:  J. Westbrook
# Date:    18-Aug-2018
# Version: 0.001 Initial version
#
# Updates:
#  4-Sep-2018 jdw add methods to construct entry and entity identier categories.
# 10-Sep-2018 jdw add method for citation author aggregation
# 22-Sep-2018 jdw add method assignAssemblyCandidates()
# 27-Oct-2018 jdw add method consolidateAccessionDetails()
# 30-Oct-2018 jdw add category methods addChemCompRelated(), addChemCompInfo(),
#                 addChemCompDescriptor()
# 10-Nov-2018 jdw add addChemCompSynonyms(), addChemCompTargets(), filterBlockByMethod()
# 12-Nov-2018 jdw add InChIKey matching in addChemCompRelated()
# 15-Nov-2018 jdw add handling for antibody misrepresentation of multisource organisms
#
##
"""
This helper class implements external method references in the RCSB dictionary extension.

All data accessors and structures here refer to dictionary category and attribute names.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import datetime
import logging

from mmcif.api.DataCategory import DataCategory

from rcsb.db.helpers.DictMethodRunnerHelperBase import DictMethodRunnerHelperBase
from rcsb.utils.io.MarshalUtil import MarshalUtil

logger = logging.getLogger(__name__)


class DictMethodRunnerHelper(DictMethodRunnerHelperBase):
    """ Helper class implements external method references in the RCSB dictionary extension.

    """

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: (dict)  Placeholder for future key-value arguments

        """
        super(DictMethodRunnerHelper, self).__init__(**kwargs)
        self._thing = kwargs.get("thing", None)
        #
        self.__drugBankMappingFilePath = kwargs.get("drugBankMappingFilePath", None)
        self.__drugBankMappingDict = {}
        self.__csdModelMappingFilePath = kwargs.get("csdModelMappingFilePath", None)
        self.__csdModelMappingDict = {}
        self.__workPath = kwargs.get("workPath", None)
        logger.debug("Dictionary method helper init")
        #

    def echo(self, msg):
        logger.info(msg)

    def setDatablockId(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getName()
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLoadDateTime(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('load_date')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLocator(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('locator')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setRowIndex(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName):
                # exit if there is no category to index
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii, iRow in enumerate(range(numRows), 1):
                # Note - we set the integer value as a string  -
                cObj.setValue(str(ii), atName, iRow)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def aggregateCitationAuthors(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName) or not dataContainer.exists('citation_author'):
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            citIdL = cObj.getAttributeValueList('id')
            #
            tObj = dataContainer.getObj('citation_author')
            #
            citIdL = list(set(citIdL))
            tD = {}
            for ii, citId in enumerate(citIdL):
                tD[citId] = tObj.selectValuesWhere('name', citId, 'citation_id')
            for ii in range(cObj.getRowCount()):
                citId = cObj.getValue('id', ii)
                cObj.setValue(';'.join(tD[citId]), atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def buildContainerEntryIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entry_container_identifiers.entry_id
        _rcsb_entry_container_identifiers.entity_ids
        _rcsb_entry_container_identifiers.polymer_entity_ids_polymer
        _rcsb_entry_container_identifiers.non-polymer_entity_ids
        _rcsb_entry_container_identifiers.assembly_ids
        ...
        """
        try:
            if not dataContainer.exists('entry'):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_ids', 'polymer_entity_ids',
                                                                              'non-polymer_entity_ids', 'assembly_ids']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            cObj.setValue(','.join(entityIdL), 'entity_ids', 0)
            #
            #
            pIdL = tObj.selectValuesWhere('id', 'polymer', 'type')
            tV = ','.join(pIdL) if pIdL else '?'
            cObj.setValue(tV, 'polymer_entity_ids', 0)

            npIdL = tObj.selectValuesWhere('id', 'non-polymer', 'type')
            tV = ','.join(npIdL) if npIdL else '?'
            cObj.setValue(tV, 'non-polymer_entity_ids', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id') if tObj else []
            tV = ','.join(assemblyIdL) if assemblyIdL else '?'
            cObj.setValue(tV, 'assembly_ids', 0)

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerEntityIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entity_container_identifiers.entry_id
        _rcsb_entity_container_identifiers.entity_id
        #
        _rcsb_entity_container_identifiers.asym_ids
        _rcsb_entity_container_identifiers.auth_asym_ids

        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('entity')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_id', 'asym_ids', 'auth_asym_ids']))
            #
            cObj = dataContainer.getObj(catName)

            psObj = dataContainer.getObj('pdbx_poly_seq_scheme')
            npsObj = dataContainer.getObj('pdbx_nonpoly_scheme')
            #
            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            for ii, entityId in enumerate(entityIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(entityId, 'entity_id', ii)
                eType = tObj.getValue('type', ii)
                if eType == 'polymer':
                    asymIdL = psObj.selectValuesWhere('asym_id', entityId, 'entity_id')
                    authAsymIdL = psObj.selectValuesWhere('pdb_strand_id', entityId, 'entity_id')
                else:
                    asymIdL = npsObj.selectValuesWhere('asym_id', entityId, 'entity_id')
                    authAsymIdL = npsObj.selectValuesWhere('pdb_strand_id', entityId, 'entity_id')
                cObj.setValue(','.join(list(set(asymIdL))).strip(), 'asym_ids', ii)
                cObj.setValue(','.join(list(set(authAsymIdL))).strip(), 'auth_asym_ids', ii)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerAssemblyIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_assembly_container_identifiers.entry_id
        _rcsb_assembly_container_identifiers.assembly_id
        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('pdbx_struct_assembly')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'assembly_id']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id')
            for ii, assemblyId in enumerate(assemblyIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(assemblyId, 'assembly_id', ii)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addDepositedAssembly(self, dataContainer, catName, **kwargs):
        """ Add the deposited coordinates as a separate assembly labeled as 'deposited'.

        """
        try:
            if not dataContainer.exists('struct_asym'):
                return False
            if not dataContainer.exists('pdbx_struct_assembly'):
                dataContainer.append(DataCategory('pdbx_struct_assembly', attributeNameList=['id', 'details', 'method_details',
                                                                                             'oligomeric_details', 'oligomeric_count',
                                                                                             'rcsb_details', 'rcsb_candidate_assembly']))
            if not dataContainer.exists('pdbx_struct_assembly_gen'):
                dataContainer.append(DataCategory('pdbx_struct_assembly_gen', attributeNameList=['assembly_id', 'oper_expression', 'asym_id_list', 'ordinal']))

            if not dataContainer.exists('pdbx_struct_oper_list'):
                row = ['1', 'identity operation', '1_555', 'x, y, z', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000']
                atList = ['id', 'type', 'name', 'symmetry_operation', 'matrix[1][1]', 'matrix[1][2]', 'matrix[1][3]',
                          'vector[1]', 'matrix[2][1]', 'matrix[2][2]', 'matrix[2][3]', 'vector[2]',
                          'matrix[3][1]', 'matrix[3][2]', 'matrix[3][3]', 'vector[3]']
                dataContainer.append(DataCategory('pdbx_struct_oper_list', attributeNameList=atList, rowList=[row]))

            #
            logger.debug("Add deposited assembly for %s" % dataContainer.getName())
            cObj = dataContainer.getObj('struct_asym')
            asymIdL = cObj.getAttributeValueList('id')
            logger.debug("AsymIdL %r" % asymIdL)
            #
            # Ordinal is added by subsequent attribure-level method.
            tObj = dataContainer.getObj('pdbx_struct_assembly_gen')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'assembly_id', rowIdx)
            tObj.setValue('1', 'oper_expression', rowIdx)
            tObj.setValue(','.join(asymIdL), 'asym_id_list', rowIdx)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'id', rowIdx)
            tObj.setValue('deposited_coordinates', 'details', rowIdx)
            logger.debug("Full row is %r" % tObj.getRow(rowIdx))
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def filterAssemblyDetails(self, dataContainer, catName, atName, **kwargs):
        """ Filter _pdbx_struct_assembly.details -> _pdbx_struct_assembly.rcsb_details
            with a more limited vocabulary -

                'author_and_software_defined_assembly'
                'author_defined_assembly'
                'software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            logger.debug("Filter assembly details for %s" % dataContainer.getName())
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD:
                    tObj.setValue(mD[details], 'rcsb_details', iRow)
                else:
                    tObj.setValue('software_defined_assembly', 'rcsb_details', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def assignAssemblyCandidates(self, dataContainer, catName, atName, **kwargs):
        """ Flag candidate biological assemblies as 'author_defined_assembly' ad author_and_software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD and mD[details] in ['author_and_software_defined_assembly', 'author_defined_assembly']:
                    tObj.setValue('Y', 'rcsb_candidate_assembly', iRow)
                else:
                    tObj.setValue('N', 'rcsb_candidate_assembly', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def __getAttribList(self, sObj, atTupL):
        atL = []
        atSL = []
        if sObj:
            for (atS, at) in atTupL:
                if sObj.hasAttribute(atS):
                    atL.append(at)
                    atSL.append(atS)
        return atSL, atL

    def __normalizeCsvToList(self, entryId, colL, separator=','):
        """ Normalize a row containing some character delimited fields.

            Expand list of uneven lists into unifornm list of lists.
            Only two list lengths are logically support 1 and second
            maximum length.

            returns: list of expanded rows or the original input.

        """
        tcL = []
        countL = []
        for col in colL:
            cL = [t.strip() for t in col.split(separator)]
            tcL.append(cL)
            countL.append(len(cL))
        #
        tL = list(set(countL))
        if len(tL) == 1 and tL[0] == 1:
            return [colL]
        # Report pathological cases ...
        if (len(tL) > 2) or (tL[0] != 1 and len(tL) == 2):
            logger.error("%s integrated source data inconsistent %r colL" % (entryId, colL))
            return [colL]
        #
        # Expand the columns with uniform length
        #
        icL = []
        maxL = tL[1]
        for tc in tcL:
            if len(tc) == 1:
                tc = tc * maxL
            icL.append(tc)
        #
        logger.debug("%s icL %r" % (entryId, icL))
        # Convert back to a row list
        #
        iRow = 0
        rL = []
        for iRow in range(maxL):
            row = []
            for ic in icL:
                row.append(ic[iRow])
            rL.append(row)

        return rL

    def filterSourceOrganismDetails(self, dataContainer, catName, **kwargs):
        """  Select relevant source and host organism details from primary data categories.

        Build:
            loop_
            _rcsb_entity_source_organism.entity_id
            _rcsb_entity_source_organism.pdbx_src_id
            _rcsb_entity_source_organism.source_type
            _rcsb_entity_source_organism.scientific_name
            _rcsb_entity_source_organism.common_name
            _rcsb_entity_source_organism.ncbi_taxonomy_id
            _rcsb_entity_source_organism.provenance_code
            _rcsb_entity_source_organism.beg_seq_num
            _rcsb_entity_source_organism.end_seq_num
            1 1 natural 'Homo sapiens' human 9606  'PDB Primary Data' 1 202
            # ... abbreviated


            loop_
            _rcsb_entity_host_organism.entity_id
            _rcsb_entity_host_organism.pdbx_src_id
            _rcsb_entity_host_organism.scientific_name
            _rcsb_entity_host_organism.common_name
            _rcsb_entity_host_organism.ncbi_taxonomy_id
            _rcsb_entity_host_organism.provenance_code
            _rcsb_entity_host_organism.beg_seq_num
            _rcsb_entity_host_organism.end_seq_num
            1 1 'Escherichia coli' 'E. coli' 562  'PDB Primary Data' 1 102
            # ... abbreviated

            And two related items -

            _entity.rcsb_multiple_source_flag
            _entity.rcsb_source_part_count

        """
        hostCatName = 'rcsb_entity_host_organism'
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            if catName == hostCatName:
                logger.debug("Skipping method for %r %r" % (dataContainer.getName(), catName))
                return True
            #
            # if there is no source information then exit
            if not (dataContainer.exists('entity_src_gen') or dataContainer.exists('entity_src_nat') or dataContainer.exists('pdbx_entity_src_syn')):
                return False
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entity_id',
                                                                              'pdbx_src_id',
                                                                              'source_type',
                                                                              'scientific_name',
                                                                              'common_name',
                                                                              'ncbi_taxonomy_id',
                                                                              'beg_seq_num',
                                                                              'end_seq_num',
                                                                              'provenance_code']))
            #
            if not dataContainer.exists(hostCatName):
                dataContainer.append(DataCategory(hostCatName, attributeNameList=['entity_id',
                                                                                  'pdbx_src_id',
                                                                                  'scientific_name',
                                                                                  'common_name',
                                                                                  'ncbi_taxonomy_id',
                                                                                  'beg_seq_num',
                                                                                  'end_seq_num',
                                                                                  'provenance_code']))
            cObj = dataContainer.getObj(catName)
            hObj = dataContainer.getObj(hostCatName)
            #
            s1Obj = dataContainer.getObj('entity_src_gen')
            atHTupL = [('entity_id', 'entity_id'),
                       ('pdbx_host_org_scientific_name', 'scientific_name'),
                       ('pdbx_host_org_common_name', 'common_name'),
                       ('pdbx_host_org_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')]
            atHSL, atHL = self.__getAttribList(s1Obj, atHTupL)
            #
            at1TupL = [('entity_id', 'entity_id'),
                       ('pdbx_gene_src_scientific_name', 'scientific_name'),
                       ('gene_src_common_name', 'common_name'),
                       ('pdbx_gene_src_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')]
            at1SL, at1L = self.__getAttribList(s1Obj, at1TupL)
            #
            s2Obj = dataContainer.getObj('entity_src_nat')
            at2TupL = [('entity_id', 'entity_id'),
                       ('pdbx_organism_scientific', 'scientific_name'),
                       ('nat_common_name', 'common_name'),
                       ('pdbx_ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('pdbx_beg_seq_num', 'beg_seq_num'),
                       ('pdbx_end_seq_num', 'end_seq_num')
                       ]
            at2SL, at2L = self.__getAttribList(s2Obj, at2TupL)
            #
            s3Obj = dataContainer.getObj('pdbx_entity_src_syn')
            at3TupL = [('entity_id', 'entity_id'),
                       ('organism_scientific', 'scientific_name'),
                       ('organism_common_name', 'common_name'),
                       ('ncbi_taxonomy_id', 'ncbi_taxonomy_id'),
                       ('pdbx_src_id', 'pdbx_src_id'),
                       ('beg_seq_num', 'beg_seq_num'),
                       ('end_seq_num', 'end_seq_num')]
            at3SL, at3L = self.__getAttribList(s3Obj, at3TupL)
            #
            eObj = dataContainer.getObj('entity')
            entityIdL = eObj.getAttributeValueList('id')
            pCode = 'PDB Primary Data'
            #
            partCountD = {}
            srcL = []
            hostL = []
            for entityId in entityIdL:
                partCountD[entityId] = 1
                eL = []
                tf = False
                if s1Obj:
                    sType = 'genetically engineered'
                    vL = s1Obj.selectValueListWhere(at1SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at1L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        tf = True
                    #
                    vL = s1Obj.selectValueListWhere(atHSL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            hostL.append((entityId, sType, atHL, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                    if tf:
                        continue

                if s2Obj:
                    sType = 'natural'
                    vL = s2Obj.selectValueListWhere(at2SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at2L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        continue

                if s3Obj:
                    sType = 'synthetic'
                    vL = s3Obj.selectValueListWhere(at3SL, entityId, 'entity_id')
                    if vL:
                        for v in vL:
                            eL.append((entityId, sType, at3L, v))
                        logger.debug("%r entity %r - %r" % (sType, entityId, vL))
                        partCountD[entityId] = len(eL)
                        srcL.extend(eL)
                        continue

            iRow = 0
            for (entityId, sType, atL, tv) in srcL:
                ii = atL.index('ncbi_taxonomy_id') if 'ncbi_taxonomy_id' in atL else -1
                if ii > 0 and len(tv[ii].split(',')) > 1:
                    tvL = self.__normalizeCsvToList(dataContainer.getName(), tv)
                    ii = atL.index('pdbx_src_id') if 'pdbx_src_id' in atL else -1
                    for jj, row in enumerate(tvL, 1):
                        row[ii] = str(jj)
                    partCountD[entityId] = len(tvL)
                else:
                    tvL = [tv]
                for v in tvL:
                    cObj.setValue(sType, 'source_type', iRow)
                    cObj.setValue(pCode, 'provenance_code', iRow)
                    for ii, at in enumerate(atL):
                        cObj.setValue(v[ii], at, iRow)
                    logger.debug("%r entity %r - UPDATED %r %r" % (sType, entityId, atL, v))
                    iRow += 1
            #
            iRow = 0
            for (entityId, sType, atL, v) in hostL:
                hObj.setValue(pCode, 'provenance_code', iRow)
                for ii, at in enumerate(atL):
                    hObj.setValue(v[ii], at, iRow)
                logger.debug("%r entity %r - UPDATED %r %r" % (sType, entityId, atL, v))
                iRow += 1
            #
            # Update entity attributes
            #    _entity.rcsb_multiple_source_flag
            #    _entity.rcsb_source_part_count
            for atName in ['rcsb_source_part_count', 'rcsb_multiple_source_flag']:
                if not eObj.hasAttribute(atName):
                    eObj.appendAttribute(atName)
            #
            for ii in range(eObj.getRowCount()):
                entityId = eObj.getValue('id', ii)
                cFlag = 'Y' if partCountD[entityId] > 1 else 'N'
                eObj.setValue(partCountD[entityId], 'rcsb_source_part_count', ii)
                eObj.setValue(cFlag, 'rcsb_multiple_source_flag', ii)

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def consolidateAccessionDetails(self, dataContainer, catName, **kwargs):
        """  Consolidate accession details into a single object.

             _rcsb_accession_info.entry_id                1ABC
             _rcsb_accession_info.status_code             REL
             _rcsb_accession_info.deposit_date            2018-01-11
             _rcsb_accession_info.initial_release_date    2018-03-23
             _rcsb_accession_info.major_revision          1
             _rcsb_accession_info.minor_revision          2
             _rcsb_accession_info.revision_date           2018-10-25


            #

            _pdbx_database_status.entry_id                        3OQP
            _pdbx_database_status.deposit_site                    RCSB
            _pdbx_database_status.process_site                    RCSB
            _pdbx_database_status.recvd_initial_deposition_date   2010-09-03
            _pdbx_database_status.status_code                     REL
            _pdbx_database_status.status_code_sf                  REL
            _pdbx_database_status.status_code_mr                  ?
            _pdbx_database_status.status_code_cs                  ?
            _pdbx_database_status.pdb_format_compatible           Y
            _pdbx_database_status.methods_development_category    ?
            _pdbx_database_status.SG_entry                        Y
            #
            loop_
            _pdbx_audit_revision_history.ordinal
            _pdbx_audit_revision_history.data_content_type
            _pdbx_audit_revision_history.major_revision
            _pdbx_audit_revision_history.minor_revision
            _pdbx_audit_revision_history.revision_date
            1 'Structure model' 1 0 2010-10-13
            2 'Structure model' 1 1 2011-07-13
            3 'Structure model' 1 2 2011-07-20
            4 'Structure model' 1 3 2014-11-12
            5 'Structure model' 1 4 2017-10-25
            #
        """
        ##
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            #
            # if there is incomplete accessioninformation then exit
            if not (dataContainer.exists('pdbx_database_status') or dataContainer.exists('pdbx_audit_revision_history')):
                return False
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'status_code',
                                                                              'deposit_date',
                                                                              'initial_release_date',
                                                                              'major_revision',
                                                                              'minor_revision',
                                                                              'revision_date']))
            #
            cObj = dataContainer.getObj(catName)
            #
            tObj = dataContainer.getObj('pdbx_database_status')
            entryId = tObj.getValue('entry_id', 0)
            statusCode = tObj.getValue('status_code', 0)
            depositDate = tObj.getValue('recvd_initial_deposition_date', 0)
            #
            cObj.setValue(entryId, 'entry_id', 0)
            cObj.setValue(statusCode, 'status_code', 0)
            cObj.setValue(depositDate, 'deposit_date', 0)
            #
            tObj = dataContainer.getObj('pdbx_audit_revision_history')
            nRows = tObj.getRowCount()
            # Assuming the default sorting order from the release module -
            releaseDate = tObj.getValue('revision_date', 0)
            minorRevision = tObj.getValue('minor_revision', nRows - 1)
            majorRevision = tObj.getValue('major_revision', nRows - 1)
            revisionDate = tObj.getValue('revision_date', nRows - 1)
            cObj.setValue(releaseDate, 'initial_release_date', 0)
            cObj.setValue(minorRevision, 'minor_revision', 0)
            cObj.setValue(majorRevision, 'major_revision', 0)
            cObj.setValue(revisionDate, 'revision_date', 0)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def __fetchDrugBankMapping(self, filePath, workPath='.'):
        """

        """
        if self.__drugBankMappingDict:
            return self.__drugBankMappingDict
        rD = {}
        try:
            if not filePath:
                return rD
            mU = MarshalUtil(workPath=workPath)
            rD = mU.doImport(filePath, format="json")
            logger.debug("Fetching DrugBank mapping length %d" % len(rD))
            self.__drugBankMappingDict = rD
            return rD
        except Exception as e:
            logger.exception("For %s failing with %s" % (filePath, str(e)))
        return rD

    def __fetchCsdModelMapping(self, filePath, workPath='.'):
        """

        """
        if self.__csdModelMappingDict:
            return self.__csdModelMappingDict
        rD = {}
        try:
            if not filePath:
                return rD
            mU = MarshalUtil(workPath=workPath)
            rD = mU.doImport(filePath, format="json")
            logger.debug("Fetching CSD model length %d" % len(rD))
            self.__csdModelMappingDict = rD
            return rD
        except Exception as e:
            logger.exception("For %s failing with %s" % (filePath, str(e)))
        return rD

    def addChemCompRelated(self, dataContainer, catName, **kwargs):
        """

        Example:

             loop_
             _rcsb_chem_comp_related.comp_id
             _rcsb_chem_comp_related.ordinal
             _rcsb_chem_comp_related.resource_name
             _rcsb_chem_comp_related.resource_accession_code
             _rcsb_chem_comp_related.related_mapping_method
             ATP 1 DrugBank DB00171 'assigned by resource'
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('chem_comp_bond')):
                return False

            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            #
            ccId = dataContainer.getName()
            #
            dbMapD = dbD['id_map']
            inKeyD = dbD['inchikey_map']
            logger.debug("inKeyD length is %d" % len(inKeyD))
            dbId = None
            mType = None
            #
            if dataContainer.exists('rcsb_chem_comp_descriptor'):
                ccIObj = dataContainer.getObj('rcsb_chem_comp_descriptor')

                if ccIObj.hasAttribute('InChIKey'):
                    inky = ccIObj.getValue('InChIKey', 0)
                    logger.debug("inKeyD length is %d testing %r" % (len(inKeyD), inky))
                    if inky in inKeyD:
                        logger.debug("Matching inchikey for %s" % ccId)
                        dbId = inKeyD[inky][0]['drugbank_id']
                        mType = 'matching InChIKey'

            if not dbId and dbMapD and dataContainer.getName() in dbMapD:
                dbId = dbMapD[ccId]["drugbank_id"]
                mType = 'assigned by resource'
                logger.debug("Matching db assignment for %s" % ccId)

            if dbId:
                #
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'resource_name',
                                                                                  'resource_accession_code',
                                                                                  'related_mapping_method']))
                wObj = dataContainer.getObj(catName)
                logger.debug("Using DrugBank mapping length %d" % len(dbMapD))
                rL = wObj.selectIndices('DrugBank', 'resource_name')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                iRow = wObj.getRowCount()
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue('DrugBank', 'resource_name', iRow)
                wObj.setValue(dbId, 'resource_accession_code', iRow)
                wObj.setValue(mType, 'related_mapping_method', iRow)
            #
            #
            csdMapD = self.__fetchCsdModelMapping(self.__csdModelMappingFilePath, workPath=self.__workPath)
            self.__csdModelMappingDict = csdMapD
            #
            if csdMapD and dataContainer.getName() in csdMapD:
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'resource_name',
                                                                                  'resource_accession_code',
                                                                                  'related_mapping_method']))
                wObj = dataContainer.getObj(catName)
                self.__csdModelMappingDict = csdMapD
                logger.debug("Using CSD model mapping length %d" % len(csdMapD))
                ccId = dataContainer.getName()
                dbId = csdMapD[ccId][0]["db_code"]
                rL = wObj.selectIndices('CCDC/CSD', 'resource_name')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                iRow = wObj.getRowCount()
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue('CCDC/CSD', 'resource_name', iRow)
                wObj.setValue(dbId, 'resource_accession_code', iRow)
                wObj.setValue('assigned by PDB', 'related_mapping_method', iRow)
            #

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompTargets(self, dataContainer, catName, **kwargs):
        """

        Example:
             loop_
             _rcsb_chem_comp_target.comp_id
             _rcsb_chem_comp_target.ordinal
             _rcsb_chem_comp_target.name
             _rcsb_chem_comp_target.interaction_type
             _rcsb_chem_comp_target.target_actions
             _rcsb_chem_comp_target.organism_common_name
             _rcsb_chem_comp_target.reference_database_name
             _rcsb_chem_comp_target.reference_database_accession_code
             _rcsb_chem_comp_target.provenance_code
             ATP 1 "O-phosphoseryl-tRNA(Sec) selenium transferase" target cofactor Human UniProt Q9HD40 DrugBank

        DrugBank target info:
        {
            "type": "target",
            "name": "Alanine--glyoxylate aminotransferase 2, mitochondrial",
            "organism": "Human",
            "actions": [
               "cofactor"
            ],
            "known_action": "unknown",
            "uniprot_ids": "Q9BYV1"
         },

        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('chem_comp_bond')):
                return False

            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            dbMapD = dbD['id_map']
            #
            ccId = dataContainer.getName()
            if dbMapD and ccId in dbMapD and 'target_interactions' in dbMapD[ccId]:
                #
                # Create the new target category
                if not dataContainer.exists(catName):
                    dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                                  'ordinal',
                                                                                  'name',
                                                                                  'interaction_type',
                                                                                  'target_actions',
                                                                                  'organism_common_name',
                                                                                  'reference_database_name',
                                                                                  'reference_database_accession_code',
                                                                                  'provenance_code']))
                wObj = dataContainer.getObj(catName)
                logger.debug("Using DrugBank mapping length %d" % len(dbMapD))
                rL = wObj.selectIndices('DrugBank', 'provenance_code')
                if rL:
                    ok = wObj.removeRows(rL)
                    if not ok:
                        logger.debug("Error removing rows in %r %r" % (catName, rL))
                #
                iRow = wObj.getRowCount()
                iRow = wObj.getRowCount()
                for tD in dbMapD[ccId]['target_interactions']:
                    wObj.setValue(ccId, 'comp_id', iRow)
                    wObj.setValue(iRow + 1, 'ordinal', iRow)
                    wObj.setValue(tD['name'], 'name', iRow)
                    wObj.setValue(tD['type'], 'interaction_type', iRow)
                    if 'actions' in tD and len(tD['actions']) > 0:
                        wObj.setValue(';'.join(tD['actions']), 'target_actions', iRow)
                    if 'organism' in tD:
                        wObj.setValue(tD['organism'], 'organism_common_name', iRow)
                    if 'uniprot_ids' in tD:
                        wObj.setValue('UniProt', 'reference_database_name', iRow)
                        wObj.setValue(tD['uniprot_ids'], 'reference_database_accession_code', iRow)
                    wObj.setValue('DrugBank', 'provenance_code', iRow)
                    iRow += 1

            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompInfo(self, dataContainer, catName, **kwargs):
        """
        Example:
             _rcsb_chem_comp_info.comp_id                 BNZ
             _rcsb_chem_comp_info.atom_count              12
             _rcsb_chem_comp_info.atom_count_chiral        0
             _rcsb_chem_comp_info.bond_count              12
             _rcsb_chem_comp_info.bond_count_aromatic      6
             _rcsb_chem_comp_info.atom_count_heavy         6
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('chem_comp_bond')):
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'atom_count',
                                                                              'atom_count_chiral',
                                                                              'bond_count',
                                                                              'bond_count_aromatic',
                                                                              'atom_count_heavy']))
            # -------
            wObj = dataContainer.getObj(catName)
            #
            cObj = dataContainer.getObj('chem_comp_atom')
            numAtoms = cObj.getRowCount()
            numAtomsHeavy = 0
            numAtomsChiral = 0
            ccId = cObj.getValue('comp_id', 0)
            for ii in range(numAtoms):
                el = cObj.getValue('type_symbol', ii)
                if el != 'H':
                    numAtomsHeavy += 1
                chFlag = cObj.getValue('pdbx_stereo_config', ii)
                if chFlag != 'N':
                    numAtomsChiral += 1
            #  ------
            numBonds = 0
            numBondsAro = 0
            try:
                cObj = dataContainer.getObj('chem_comp_bond')
                numBonds = cObj.getRowCount()
                numBondsAro = 0
                for ii in range(numAtoms):
                    aroFlag = cObj.getValue('pdbx_aromatic_flag', ii)
                    if aroFlag != 'N':
                        numBondsAro += 1
            except Exception:
                pass

            #
            wObj.setValue(ccId, 'comp_id', 0)
            wObj.setValue(numAtoms, 'atom_count', 0)
            wObj.setValue(numAtomsChiral, 'atom_count_chiral', 0)
            wObj.setValue(numAtomsHeavy, 'atom_count_heavy', 0)
            wObj.setValue(numBonds, 'bond_count', 0)
            wObj.setValue(numBondsAro, 'bond_count_aromatic', 0)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompDescriptor(self, dataContainer, catName, **kwargs):
        """
        Parse the pdbx_chem_comp_descriptor category and extract SMILES/CACTVS and InChI descriptors -

        loop_
        _pdbx_chem_comp_descriptor.comp_id
        _pdbx_chem_comp_descriptor.type
        _pdbx_chem_comp_descriptor.program
        _pdbx_chem_comp_descriptor.program_version
        _pdbx_chem_comp_descriptor.descriptor
        ATP SMILES           ACDLabs              10.04 "O=P(O)(O)OP(=O)(O)OP(=O)(O)OCC3OC(n2cnc1c(ncnc12)N)C(O)C3O"
        ATP SMILES_CANONICAL CACTVS               3.341 "Nc1ncnc2n(cnc12)[C@@H]3O[C@H](CO[P@](O)(=O)O[P@@](O)(=O)O[P](O)(O)=O)[C@@H](O)[C@H]3O"
        ATP SMILES           CACTVS               3.341 "Nc1ncnc2n(cnc12)[CH]3O[CH](CO[P](O)(=O)O[P](O)(=O)O[P](O)(O)=O)[CH](O)[CH]3O"
        ATP SMILES_CANONICAL "OpenEye OEToolkits" 1.5.0 "c1nc(c2c(n1)n(cn2)[C@H]3[C@@H]([C@@H]([C@H](O3)CO[P@@](=O)(O)O[P@](=O)(O)OP(=O)(O)O)O)O)N"
        ATP SMILES           "OpenEye OEToolkits" 1.5.0 "c1nc(c2c(n1)n(cn2)C3C(C(C(O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N"
        ATP InChI            InChI                1.03  "InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3- ...."
        ATP InChIKey         InChI                1.03  ZKHQWZAMYRWXGA-KQYNXXCUSA-N

        To produce -
             _rcsb_chem_comp_descriptor.comp_id                 ATP
             _rcsb_chem_comp_descriptor.SMILES                  'Nc1ncnc2n(cnc12)[CH]3O[CH](CO[P](O)(=O)O[P](O)(=O)O[P](O)(O)=O)[CH](O)[CH]3O'
             _rcsb_chem_comp_descriptor.SMILES_stereo           'Nc1ncnc2n(cnc12)[C@@H]3O[C@H](CO[P@](O)(=O)O[P@@](O)(=O)O[P](O)(O)=O)[C@@H](O)[C@H]3O'
             _rcsb_chem_comp_descriptor.InChI                   'InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(17)6(16)4(26-10)1-25 ...'
             _rcsb_chem_comp_descriptor.InChIKey                'ZKHQWZAMYRWXGA-KQYNXXCUSA-N'
        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('chem_comp_atom') and dataContainer.exists('pdbx_chem_comp_descriptor')):
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'SMILES',
                                                                              'SMILES_stereo',
                                                                              'InChI',
                                                                              'InChIKey']))
            #
            wObj = dataContainer.getObj(catName)
            ccIObj = dataContainer.getObj('pdbx_chem_comp_descriptor')
            iRow = 0
            ccId = ''
            for ii in range(ccIObj.getRowCount()):
                ccId = ccIObj.getValue('comp_id', ii)
                nm = ccIObj.getValue('descriptor', ii)
                prog = ccIObj.getValue('program', ii)
                typ = ccIObj.getValue('type', ii)
                #
                if typ == 'SMILES_CANONICAL' and prog == "CACTVS":
                    wObj.setValue(nm, 'SMILES_stereo', iRow)
                elif typ == 'SMILES' and prog == "CACTVS":
                    wObj.setValue(nm, 'SMILES', iRow)
                elif typ == 'InChI' and prog == "InChI":
                    wObj.setValue(nm, 'InChI', iRow)
                elif typ == 'InChIKey' and prog == "InChI":
                    wObj.setValue(nm, 'InChIKey', iRow)
            #
            wObj.setValue(ccId, 'comp_id', iRow)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addChemCompSynonyms(self, dataContainer, catName, **kwargs):
        """
             loop_
                 _rcsb_chem_comp_synonyms.comp_id
                 _rcsb_chem_comp_synonyms.ordinal
                 _rcsb_chem_comp_synonyms.name
                 _rcsb_chem_comp_synonyms.provenance_code
                    ATP 1 "adenosine 5'-(tetrahydrogen triphosphate)"  'PDB Reference Data'
                    ATP 2 "Adenosine 5'-triphosphate"  'PDB Reference Data'
                    ATP 3 Atriphos  DrugBank
                    ATP 4 Striadyne DrugBank

            loop_
            _pdbx_chem_comp_identifier.comp_id
            _pdbx_chem_comp_identifier.type
            _pdbx_chem_comp_identifier.program
            _pdbx_chem_comp_identifier.program_version
            _pdbx_chem_comp_identifier.identifier
            ATP "SYSTEMATIC NAME" ACDLabs              10.04
            ;adenosine 5'-(tetrahydrogen triphosphate)
            ;
            ATP "SYSTEMATIC NAME" "OpenEye OEToolkits" 1.5.0
             "[[(2R,3S,4R,5R)-5-(6-aminopurin-9-yl)-3,4-dihydroxy-oxolan-2-yl]methoxy-hydroxy-phosphoryl] phosphono hydrogen phosphate"
            #

        """
        try:
            logger.debug("Starting with  %r %r" % (dataContainer.getName(), catName))
            if not (dataContainer.exists('chem_comp') and dataContainer.exists('pdbx_chem_comp_identifier')):
                return False
            #
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['comp_id',
                                                                              'ordinal',
                                                                              'name',
                                                                              'provenance_code']))
            else:
                # remove the rowlist -
                pass
            #
            wObj = dataContainer.getObj(catName)
            #
            # Get all of the names relevant names from the definition -
            #
            iRow = 0
            provCode = 'PDB Reference Data'
            ccObj = dataContainer.getObj('chem_comp')
            ccId = ccObj.getValue('id', 0)
            ccName = ccObj.getValue('name', 0)
            ccSynonymL = []
            if ccObj.hasAttribute('pdbx_synonyms'):
                ccSynonymL = str(ccObj.getValue('pdbx_synonyms', 0)).split(';')
            #
            wObj.setValue(ccId, 'comp_id', iRow)
            wObj.setValue(ccName, 'name', iRow)
            wObj.setValue(iRow + 1, 'ordinal', iRow)
            wObj.setValue(provCode, 'provenance_code', iRow)
            iRow += 1
            for nm in ccSynonymL:
                if nm in ['?', '.']:
                    continue
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(nm, 'name', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue(provCode, 'provenance_code', iRow)
                iRow += 1
            #
            ccIObj = dataContainer.getObj('pdbx_chem_comp_identifier')
            for ii in range(ccIObj.getRowCount()):
                nm = ccIObj.getValue('identifier', ii)
                prog = ccIObj.getValue('program', ii)
                wObj.setValue(ccId, 'comp_id', iRow)
                wObj.setValue(nm, 'name', iRow)
                wObj.setValue(iRow + 1, 'ordinal', iRow)
                wObj.setValue(prog, 'provenance_code', iRow)
                iRow += 1
            #
            dbD = self.__fetchDrugBankMapping(self.__drugBankMappingFilePath, workPath=self.__workPath)
            dbMapD = dbD['id_map']
            #
            if dbMapD and ccId in dbMapD and 'aliases' in dbMapD[ccId]:
                iRow = wObj.getRowCount()
                for nm in dbMapD[ccId]['aliases']:
                    wObj.setValue(ccId, 'comp_id', iRow)
                    wObj.setValue(nm, 'name', iRow)
                    wObj.setValue(iRow + 1, 'ordinal', iRow)
                    wObj.setValue('DrugBank', 'provenance_code', iRow)
                    iRow += 1

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))

        return False

    def __getPolymerComposition(self, polymerTypeList):
        """
        polymerTypeList contains entity_poly.type and entity_branch.type values:

        Current polymer type list:
             'polypeptide(D)'
             'polypeptide(L)'
             'polydeoxyribonucleotide'
             'polyribonucleotide'
             'polysaccharide(D)'
             'polysaccharide(L)'
             'polydeoxyribonucleotide/polyribonucleotide hybrid'
             'cyclic-pseudo-peptide'
             'peptide nucleic acid'
             'other'
             "other type pair (polymer type count = 2)"
             "other composition (polymer type count >= 3)"
        Current branch type list:
             'oligosaccharide'

        Output composition classes:

            'homomeric protein' 'Single protein entity'
            'heteromeric protein' 'Multiple protein entities'
            'DNA' 'DNA entity/entities only'
            'RNA' 'RNA entity/entities only'
            'NA-hybrid' 'DNA/RNA hybrid entity/entities only'
            'protein/NA' 'Both protein and nucleic acid polymer entities'
            'DNA/RNA' 'Both DNA and RNA polymer entities'
            'oligosaccharide' 'One of more oligosaccharide entities'
            'protein/oligosaccharide' 'Both protein and oligosaccharide entities'
            'NA/oligosaccharide' 'Both NA and oligosaccharide entities'

            'Other' 'Neither protein nor nucleic acid polymer entities'
        """

        compClass = 'other'
        # get type counts
        cD = {}
        for polymerType in polymerTypeList:
            if polymerType in ['polypeptide(D)', 'polypeptide(L)']:
                cD['protein'] = cD['protein'] + 1 if 'protein' in cD else 1
            elif polymerType in ['polydeoxyribonucleotide']:
                cD['DNA'] = cD['DNA'] + 1 if 'DNA' in cD else 1
            elif polymerType in ['polyribonucleotide']:
                cD['RNA'] = cD['RNA'] + 1 if 'RNA' in cD else 1
            elif polymerType in ['polydeoxyribonucleotide/polyribonucleotide hybrid']:
                cD['NA-hybrid'] = cD['NA-hybrid'] + 1 if 'NA-hybrid' in cD else 1
            elif polymerType in ['oligosaccharide']:
                cD['oligosaccharide'] = cD['oligosaccharide'] + 1 if 'oligosaccharide' in cD else 1
            else:
                cD['other'] = cD['other'] + 1 if 'other' in cD else 1
        #
        if len(cD) == 1:
            ky = list(cD.keys())[0]
            if 'protein' in cD:
                if cD['protein'] == 1:
                    compClass = 'homomeric protein'
                else:
                    compClass = 'heteromeric protein'
            elif ky in ['DNA', 'RNA', 'NA-hybrid', 'oligosaccharide', 'other']:
                compClass = ky
        elif len(cD) == 2:
            if 'protein' in cD:
                if ('DNA' in cD) or ('RNA' in cD) or ('NA-hybrid' in cD):
                    compClass = 'protein/NA'
                elif 'oligosaccharide' in cD:
                    compClass = 'protein/oligosaccharide'
            elif 'DNA' in cD and 'RNA' in cD:
                compClass = 'DNA/RNA'
            elif 'oligosaccharide' in cD and ('RNA' in cD or 'DNA' in cD):
                compClass = 'NA/oligosaccharide'
            else:
                compClass = "other type pair"
        elif len(cD) >= 3:
            compClass = "other type composition"

        return compClass

    def __filterExperimentalMethod(self, methodL):
        """
        'X-ray'            'X-RAY DIFFRACTION, FIBER DIFFRACTION, or POWDER DIFFRACTION'
        'NMR'              'SOLUTION NMR or SOLID-STATE NMR'
        'EM'               'ELECTRON MICROSCOPY or ELECTRON CRYSTALLOGRAPHY or ELECTRON TOMOGRAPHY'
        'Neutron'          'NEUTRON DIFFRACTION'
        'Multiple methods' 'Multiple experimental methods'
        'Other'            'SOLUTION SCATTERING, EPR, THEORETICAL MODEL, INFRARED SPECTROSCOPY or FLUORESCENCE TRANSFER'
        """
        methodCount = len(methodL)
        if methodCount > 1:
            expMethod = 'Multiple methods'
        else:
            #
            mS = methodL[0].upper()
            expMethod = 'Other'
            if mS in ['X-RAY DIFFRACTION', 'FIBER DIFFRACTION', 'POWDER DIFFRACTION']:
                expMethod = 'X-ray'
            elif mS in ['SOLUTION NMR', 'SOLID-STATE NMR']:
                expMethod = 'NMR'
            elif mS in ['ELECTRON MICROSCOPY', 'ELECTRON CRYSTALLOGRAPHY']:
                expMethod = 'EM'
            elif mS in ['NEUTRON DIFFRACTION']:
                expMethod = 'Neutron'
            elif mS in ['SOLUTION SCATTERING', 'EPR', 'THEORETICAL MODEL', 'INFRARED SPECTROSCOPY', 'FLUORESCENCE TRANSFER']:
                expMethod = 'Other'
            else:
                logger.error('Unexpected method ')

        return methodCount, expMethod

    def __filterEntityPolyType(self, pType):
        """
        Returns mappings:
            'Protein'   'polypeptide(D) or polypeptide(L)'
            'DNA'       'polydeoxyribonucleotide'
            'RNA'       'polyribonucleotide'
            'NA-hybrid' 'polydeoxyribonucleotide/polyribonucleotide hybrid'
            'Other'      'polysaccharide(D), polysaccharide(L), cyclic-pseudo-peptide, peptide nucleic acid, or other'

        """
        polymerType = pType.lower()
        if polymerType in ['polypeptide(d)', 'polypeptide(l)']:
            rT = 'Protein'
        elif polymerType in ['polydeoxyribonucleotide']:
            rT = 'DNA'
        elif polymerType in ['polyribonucleotide']:
            rT = 'RNA'
        elif polymerType in ['polydeoxyribonucleotide/polyribonucleotide hybrid']:
            rT = 'NA-hybrid'
        else:
            rT = 'Other'
        return rT

    def addEntryInfo(self, dataContainer, catName, **kwargs):
        """
        Add rcsb_entry_info, for example:
             _rcsb_entry_info.entry_id                      1ABC
             _rcsb_entry_info.polymer_composition           'heteromeric protein'
             _rcsb_entry_info.experimental_method           'multiple methods'
             _rcsb_entry_info.experimental_method_count     2
             _rcsb_entry_info.polymer_entity_count          2
             _rcsb_entry_info.entity_count                  2
             _rcsb_entry_info.nonpolymer_entity_count       2
             _rcsb_entry_info.branched_entity_count         0

        Also add the related field:

        _entity_poly.rcsb_entity_polymer_type

            'Protein'   'polypeptide(D) or polypeptide(L)'
            'DNA'       'polydeoxyribonucleotide'
            'RNA'       'polyribonucleotide'
            'NA-hybrid' 'polydeoxyribonucleotide/polyribonucleotide hybrid'
            'Other'      'polysaccharide(D), polysaccharide(L), cyclic-pseudo-peptide, peptide nucleic acid, or other'
    #
        """
        try:
            logger.debug("Starting with %r %r" % (dataContainer.getName(), catName))
            # Exit if source categories are missing
            if not (dataContainer.exists('exptl') and dataContainer.exists('entity') and dataContainer.exists('entity_poly')):
                return False
            #
            # Create the new target category
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id',
                                                                              'polymer_composition',
                                                                              'experimental_method',
                                                                              'experimental_method_count',
                                                                              'polymer_entity_count',
                                                                              'entity_count',
                                                                              'nonpolymer_entity_count',
                                                                              'branched_entity_count']))
            #
            cObj = dataContainer.getObj(catName)
            #
            eObj = dataContainer.getObj('entity')
            eTypeL = eObj.getAttributeValueList('type')

            numPolymers = 0
            numNonPolymers = 0
            numBranched = 0
            for eType in eTypeL:
                if eType == 'polymer':
                    numPolymers += 1
                elif eType == 'non-polymer':
                    numNonPolymers += 1
                elif eType == 'branched':
                    numBranched += 1
                elif eType != 'water':
                    logger.error("Unexpected entity type for %s %s" % (dataContainer.getName(), eType))
            totalEntities = numPolymers + numNonPolymers + numBranched
            #
            epObj = dataContainer.getObj('entity_poly')
            pTypeL = epObj.getAttributeValueList('type')
            #
            atName = 'rcsb_entity_polymer_type'
            if not epObj.hasAttribute(atName):
                epObj.appendAttribute(atName)
            for ii in range(epObj.getRowCount()):
                epObj.setValue(self.__filterEntityPolyType(pTypeL[ii]), atName, ii)
            #
            # Add any branched entity types to the
            if dataContainer.exists('entity_branch'):
                ebObj = dataContainer.getObj('entity_branch')
                pTypeL.extend(ebObj.getAttributeValueList('type'))
            #
            polymerCompClass = self.__getPolymerComposition(pTypeL)
            #
            xObj = dataContainer.getObj('exptl')
            entryId = xObj.getValue('entry_id', 0)
            methodL = xObj.getAttributeValueList('method')
            methodCount, expMethod = self.__filterExperimentalMethod(methodL)
            #
            cObj.setValue(entryId, 'entry_id', 0)
            cObj.setValue(polymerCompClass, 'polymer_composition', 0)
            cObj.setValue(numPolymers, 'polymer_entity_count', 0)
            cObj.setValue(numNonPolymers, 'nonpolymer_entity_count', 0)
            cObj.setValue(numBranched, 'branched_entity_count', 0)
            cObj.setValue(totalEntities, 'entity_count', 0)
            cObj.setValue(expMethod, 'experimental_method', 0)
            cObj.setValue(methodCount, 'experimental_method_count', 0)

            return True
        except Exception as e:
            logger.exception("For %s %r failing with %s" % (dataContainer.getName(), catName, str(e)))
        return False

    def filterBlockByMethod(self, dataContainer, blockName, **kwargs):
        """ Filter empty placeholder data categories by experimental method.

        """
        logger.debug("Starting with %r blockName %r" % (dataContainer.getName(), blockName))
        try:
            if not dataContainer.exists('exptl'):
                return False
            #
            xObj = dataContainer.getObj('exptl')
            methodL = xObj.getAttributeValueList('method')
            # Don't strip anything for multiple methods at this point
            if len(methodL) > 1:
                objNameL = []
            else:
                #
                mS = methodL[0].upper()
                if mS in ['X-RAY DIFFRACTION', 'FIBER DIFFRACTION', 'POWDER DIFFRACTION', 'ELECTRON CRYSTALLOGRAPHY', 'NEUTRON DIFFRACTION']:
                    objNameL = []
                elif mS in ['SOLUTION NMR', 'SOLID-STATE NMR']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                elif mS in ['ELECTRON MICROSCOPY']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                elif mS in ['SOLUTION SCATTERING', 'EPR', 'THEORETICAL MODEL', 'INFRARED SPECTROSCOPY', 'FLUORESCENCE TRANSFER']:
                    objNameL = ['cell', 'symmetry', 'refine', 'refine_hist', 'software', 'diffrn', 'diffrn_radiation']
                else:
                    logger.error('Unexpected method ')
            #
            for objName in objNameL:
                dataContainer.remove(objName)
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (dataContainer.getName(), str(e)))
        return False

    def deferredItemMethod(self, dataContainer, catName, atName, **kwargs):
        """ Placeholder method to
        """
        logger.debug("Called deferred method for %r %r %r" % (dataContainer.getName(), catName, atName))
        return True

    def __getTimeStamp(self):
        utcnow = datetime.datetime.utcnow()
        ts = utcnow.strftime("%Y-%m-%d:%H:%M:%S")
        return ts
