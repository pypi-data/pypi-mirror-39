

import logging
import os

from rcsb.utils.config.ConfigUtil import ConfigUtil

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MakeConfig(object):

    def __init__(self):
        #
        self.__inpPathConfigIni = os.path.join(HERE, 'dbload-setup-example.cfg')
        cfgOb = ConfigUtil(configPath=self.__inpPathConfigIni, mockTopPath=os.path.join(TOPDIR, 'rcsb', 'mock-data'))
        oD = cfgOb.exportConfig()
        for ky in oD:
            logger.info("section name %s" % ky)
            for k, v in oD[ky].items():
                logger.info("op:  %s val: %s" % (k, v))

        self.__outPathConfigYamlExport1 = os.path.join(TOPDIR, 'rcsb', 'mock-data', 'config', 'dbload-setup-example.yml')
        self.__outPathConfigYamlExport2 = os.path.join(TOPDIR, 'rcsb', 'mock-data', 'config', 'dbload-setup-example-copy.yml')
        #cfgOb = ConfigUtil(configPath=self.__inpPathConfigIni, mockTopPath=os.path.join(TOPDIR, 'rcsb', 'mock-data'))
        cfgOb = ConfigUtil(mockTopPath=os.path.join(TOPDIR, 'rcsb', 'mock-data'))
        #
        cD = self.__setup()
        #
        oD.update(cD)
        #
        cfgOb.importConfig(oD)
        #
        ok = cfgOb.writeConfig(self.__outPathConfigYamlExport1, configFormat='yaml')
        logger.info("status %r" % ok)
        cfgOb = ConfigUtil(configPath=self.__outPathConfigYamlExport1, configFormat='yaml', mockTopPath=os.path.join(TOPDIR, 'rcsb', 'mock-data'))
        cfgOb.exportConfig()
        #logger.info("recovered config %r" % rD['dictionary_helper']['selection_filters'])
        #
        ok = cfgOb.writeConfig(self.__outPathConfigYamlExport2, configFormat='yaml')

    def __setup(self):
        dH = {}
        sD = {}
        dD = {}
        cfgD = {'dictionary_helper': dH, 'schemadef_helper': sD, 'document_helper': dD}
        #
        # Data items requiring a particular data transformation -
        dH['item_transformers'] = {
            'STRIP_WS': [
                {'CATEGORY_NAME': 'entity_poly', 'ATTRIBUTE_NAME': 'pdbx_c_terminal_seq_one_letter_code'},
                {'CATEGORY_NAME': 'entity_poly', 'ATTRIBUTE_NAME': 'pdbx_n_terminal_seq_one_letter_code'},
                {'CATEGORY_NAME': 'entity_poly', 'ATTRIBUTE_NAME': 'pdbx_seq_one_letter_code'},
                {'CATEGORY_NAME': 'entity_poly', 'ATTRIBUTE_NAME': 'pdbx_seq_one_letter_code_can'},
                {'CATEGORY_NAME': 'entity_poly', 'ATTRIBUTE_NAME': 'pdbx_seq_one_letter_code_sample'},
                {'CATEGORY_NAME': 'struct_ref', 'ATTRIBUTE_NAME': 'pdbx_seq_one_letter_code'}
            ]
        }

        dH['cardinality_parent_items'] = {
            'bird': {'CATEGORY_NAME': 'pdbx_reference_molecule', 'ATTRIBUTE_NAME': 'prd_id'},
            'bird_family': {'CATEGORY_NAME': 'pdbx_reference_molecule_family', 'ATTRIBUTE_NAME': 'family_prd_id'},
            'chem_comp': {'CATEGORY_NAME': 'chem_comp', 'ATTRIBUTE_NAME': 'id'},
            'bird_chem_comp': {'CATEGORY_NAME': 'chem_comp', 'ATTRIBUTE_NAME': 'id'},
            'pdbx': {'CATEGORY_NAME': 'entry', 'ATTRIBUTE_NAME': 'id'},
            'pdbx_core': {'CATEGORY_NAME': 'entry', 'ATTRIBUTE_NAME': 'id'}
        }
        dH['cardinality_category_extras'] = ['rcsb_load_status']
        #
        dH['selection_filters'] = {('PUBLIC_RELEASE', 'pdbx'): [{'CATEGORY_NAME': 'pdbx_database_status', 'ATTRIBUTE_NAME': 'status_code', 'VALUES': ['REL']}],
                                   ('PUBLIC_RELEASE', 'pdbx_core'): [{'CATEGORY_NAME': 'pdbx_database_status', 'ATTRIBUTE_NAME': 'status_code', 'VALUES': ['REL']}],
                                   ('PUBLIC_RELEASE', 'chem_comp'): [{'CATEGORY_NAME': 'chem_comp', 'ATTRIBUTE_NAME': 'pdbx_release_status', 'VALUES': ['REL', 'OBS', 'REF_ONLY']}],
                                   ('PUBLIC_RELEASE', 'bird_chem_comp'): [{'CATEGORY_NAME': 'chem_comp', 'ATTRIBUTE_NAME': 'pdbx_release_status', 'VALUES': ['REL', 'OBS', 'REF_ONLY']}],
                                   ('PUBLIC_RELEASE', 'bird'): [{'CATEGORY_NAME': 'pdbx_reference_molecule', 'ATTRIBUTE_NAME': 'release_status', 'VALUES': ['REL', 'OBS']}],
                                   ('PUBLIC_RELEASE', 'bird_family'): [{'CATEGORY_NAME': 'pdbx_reference_molecule_family', 'ATTRIBUTE_NAME': 'release_status', 'VALUES': ['REL', 'OBS']}]
                                   }
        #
        dH['type_code_classes'] = {'iterable': ['ucode-alphanum-csv', 'id_list', 'alphanum-scsv', 'alphanum-csv']}
        dH['query_string_selectors'] = {'iterable': ['comma separate']}
        # Put the non default iterable delimiter cases here -
        dH['iterable_delimiters'] = [{'CATEGORY_NAME': 'chem_comp', 'ATTRIBUTE_NAME': 'pdbx_synonyms', 'DELIMITER': ';'},
                                     {'CATEGORY_NAME': 'citation', 'ATTRIBUTE_NAME': 'rcsb_authors', 'DELIMITER': ';'}]
        #
        # Categories/Attributes that will be included in a schema definitions even if they are not populated in any tabulated instance data -
        #
        #
        #
        dH['content_classes'] = {('GENERATED_CONTENT', 'pdbx'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']},
                                                                 {'CATEGORY_NAME': 'pdbx_struct_assembly_gen', 'ATTRIBUTE_NAME_LIST': ['ordinal']}],
                                 ('GENERATED_CONTENT', 'pdbx_core'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']},
                                                                      {'CATEGORY_NAME': 'citation', 'ATTRIBUTE_NAME_LIST': ['rcsb_authors']},
                                                                      {'CATEGORY_NAME': 'pdbx_struct_assembly_gen', 'ATTRIBUTE_NAME_LIST': ['ordinal']},
                                                                      {'CATEGORY_NAME': 'pdbx_struct_assembly', 'ATTRIBUTE_NAME_LIST': ['rcsb_details', 'rcsb_candidate_assembly']},
                                                                      {'CATEGORY_NAME': 'rcsb_entry_container_identifiers', 'ATTRIBUTE_NAME_LIST': [
                                                                          'entry_id', 'entity_ids', 'polymer_entity_ids', 'non-polymer_entity_ids', 'assembly_ids']},
                                                                      {'CATEGORY_NAME': 'rcsb_entity_container_identifiers', 'ATTRIBUTE_NAME_LIST': [
                                                                          'entry_id', 'entity_id', 'asym_ids', 'auth_asym_ids']},
                                                                      {'CATEGORY_NAME': 'rcsb_assembly_container_identifiers', 'ATTRIBUTE_NAME_LIST': ['entry_id', 'assembly_id']},
                                                                      {'CATEGORY_NAME': 'rcsb_entity_source_organism', 'ATTRIBUTE_NAME_LIST': ['entity_id', 'pdbx_src_id', 'source_type',
                                                                                                                                               'scientific_name', 'common_name', 'ncbi_taxonomy_id',
                                                                                                                                               'provenance_code', 'beg_seq_num', 'end_seq_num']},
                                                                      {'CATEGORY_NAME': 'rcsb_entity_host_organism', 'ATTRIBUTE_NAME_LIST': ['entity_id', 'pdbx_src_id',
                                                                                                                                             'scientific_name', 'common_name', 'ncbi_taxonomy_id',
                                                                                                                                             'provenance_code', 'beg_seq_num', 'end_seq_num']},
                                                                      {'CATEGORY_NAME': 'entity', 'ATTRIBUTE_NAME_LIST': ['rcsb_multiple_source_flag', 'rcsb_source_part_count']},
                                                                      ],
                                 ('GENERATED_CONTENT', 'data_exchange'): [{'CATEGORY_NAME': 'rcsb_data_exchange_status',
                                                                           'ATTRIBUTE_NAME_LIST': ['update_id', 'database_name', 'object_name', 'update_status_flag', 'update_begin_timestamp', 'update_end_timestamp']}],
                                 ('EVOLVING_CONTENT', 'pdbx_core'): [{'CATEGORY_NAME': 'diffrn', 'ATTRIBUTE_NAME_LIST': ['pdbx_serial_crystal_experiment']},
                                                                     {'CATEGORY_NAME': 'diffrn_detector', 'ATTRIBUTE_NAME_LIST': ['pdbx_frequency']},
                                                                     {'CATEGORY_NAME': 'pdbx_serial_crystallography_measurement',
                                                                      'ATTRIBUTE_NAME_LIST': ['diffrn_id',
                                                                                              'pulse_energy',
                                                                                              'pulse_duration',
                                                                                              'xfel_pulse_repetition_rate',
                                                                                              'pulse_photon_energy',
                                                                                              'photons_per_pulse',
                                                                                              'source_size',
                                                                                              'source_distance',
                                                                                              'focal_spot_size',
                                                                                              'collimation',
                                                                                              'collection_time_total']},

                                                                     {'CATEGORY_NAME': 'pdbx_serial_crystallography_sample_delivery',
                                                                      'ATTRIBUTE_NAME_LIST': ['diffrn_id', 'description', 'method']},

                                                                     {'CATEGORY_NAME': 'pdbx_serial_crystallography_sample_delivery_injection',
                                                                      'ATTRIBUTE_NAME_LIST': ['diffrn_id',
                                                                                              'description',
                                                                                              'injector_diameter',
                                                                                              'injector_temperature',
                                                                                              'injector_pressure',
                                                                                              'flow_rate',
                                                                                              'carrier_solvent',
                                                                                              'crystal_concentration',
                                                                                              'preparation',
                                                                                              'power_by',
                                                                                              'injector_nozzle',
                                                                                              'jet_diameter',
                                                                                              'filter_size']},

                                                                     {'CATEGORY_NAME': 'pdbx_serial_crystallography_sample_delivery_fixed_target',
                                                                      'ATTRIBUTE_NAME_LIST': ['diffrn_id',
                                                                                              'description',
                                                                                              'sample_holding',
                                                                                              'support_base',
                                                                                              'sample_unit_size',
                                                                                              'crystals_per_unit',
                                                                                              'sample_solvent',
                                                                                              'sample_dehydration_prevention',
                                                                                              'motion_control',
                                                                                              'velocity_horizontal',
                                                                                              'velocity_vertical',
                                                                                              'details']},

                                                                     {'CATEGORY_NAME': 'pdbx_serial_crystallography_data_reduction',
                                                                      'ATTRIBUTE_NAME_LIST': ['diffrn_id',
                                                                                              'frames_total',
                                                                                              'xfel_pulse_events',
                                                                                              'frame_hits',
                                                                                              'crystal_hits',
                                                                                              'droplet_hits',
                                                                                              'frames_failed_index',
                                                                                              'frames_indexed',
                                                                                              'lattices_indexed',
                                                                                              'xfel_run_numbers']},
                                                                     ],
                                 ('GENERATED_CONTENT', 'chem_comp'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']}],
                                 ('GENERATED_CONTENT', 'bird_chem_comp'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']}],
                                 ('GENERATED_CONTENT', 'bird'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']}],
                                 ('GENERATED_CONTENT', 'bird_family'): [{'CATEGORY_NAME': 'rcsb_load_status', 'ATTRIBUTE_NAME_LIST': ['datablock_name', 'load_date', 'locator']}],
                                 #
                                 ('REPO_HOLDINGS_CONTENT', 'repository_holdings'): [{'CATEGORY_NAME': 'rcsb_repository_holdings_current',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'repository_content_types']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_update',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'repository_content_types']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_removed',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'repository_content_types', 'deposit_date',
                                                                                                             'release_date', 'remove_date', 'title', 'details', 'audit_authors', 'id_codes_replaced_by']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_unreleased',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'status_code', 'deposit_date', 'deposit_date_coordinates',
                                                                                                             'deposit_date_structure_factors', 'deposit_date_nmr_restraints', 'hold_date_coordinates',
                                                                                                             'hold_date_structure_factors', 'hold_date_nmr_restraints', 'release_date', 'title',
                                                                                                             'audit_authors', 'author_prerelease_sequence_status']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_removed_audit_author',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'ordinal_id', 'audit_author']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_superseded',
                                                                                     'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id', 'id_codes_superseded']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_transferred', 'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id',
                                                                                                                                                                      'status_code',
                                                                                                                                                                      'deposit_date',
                                                                                                                                                                      'release_date',
                                                                                                                                                                      'title',
                                                                                                                                                                      'audit_authors',
                                                                                                                                                                      'remote_accession_code',
                                                                                                                                                                      'remote_repository_name',
                                                                                                                                                                      'repository_content_types']},
                                                                                    {'CATEGORY_NAME': 'rcsb_repository_holdings_insilico_models', 'ATTRIBUTE_NAME_LIST': ['update_id', 'entry_id',
                                                                                                                                                                          'status_code',
                                                                                                                                                                          'deposit_date',
                                                                                                                                                                          'release_date',
                                                                                                                                                                          'title',
                                                                                                                                                                          'audit_authors',
                                                                                                                                                                          'remove_date',
                                                                                                                                                                          'id_codes_replaced_by']},
                                                                                    ],
                                 ('SEQUENCE_CLUSTER_CONTENT', 'entity_sequence_clusters'): [{'CATEGORY_NAME': 'rcsb_entity_sequence_cluster_list',
                                                                                             'ATTRIBUTE_NAME_LIST': ['data_set_id', 'entry_id', 'entity_id', 'cluster_id', 'identity']},
                                                                                            {'CATEGORY_NAME': 'rcsb_instance_sequence_cluster_list',
                                                                                             'ATTRIBUTE_NAME_LIST': ['data_set_id', 'entry_id', 'instance_id', 'cluster_id', 'identity']}]
                                 }
        #
        #
        # _diffrn.pdbx_serial_crystal_experiment
        # _diffrn_detector.pdbx_frequency
        #
        #
        dH['slice_parent_items'] = {('ENTITY', 'pdbx_core'): [{'CATEGORY_NAME': 'entity', 'ATTRIBUTE_NAME': 'id'}],
                                    ('ASSEMBLY', 'pdbx_core'): [{'CATEGORY_NAME': 'pdbx_struct_assembly', 'ATTRIBUTE_NAME': 'id'}]
                                    }
        dH['slice_parent_filters'] = {('ENTITY', 'pdbx_core'): [{'CATEGORY_NAME': 'entity', 'ATTRIBUTE_NAME': 'type', 'VALUES': ['polymer', 'non-polymer', 'macrolide', 'branched']}]
                                      }

        dH['slice_cardinality_category_extras'] = {('ENTITY', 'pdbx_core'): ['rcsb_load_status', 'rcsb_entity_container_identifiers'],
                                                   ('ASSEMBLY', 'pdbx_core'): ['rcsb_load_status', 'rcsb_assembly_container_identifiers']
                                                   }
        dH['slice_category_extras'] = {('ENTITY', 'pdbx_core'): ['rcsb_load_status'], ('ASSEMBLY', 'pdbx_core'): ['rcsb_load_status', 'pdbx_struct_oper_list']}

        # included or excluded schema identifiers
        #
        sD['schema_content_filters'] = {'pdbx': {'INCLUDE': [],
                                                 'EXCLUDE': ['ATOM_SITE',
                                                             'ATOM_SITE_ANISOTROP'
                                                             ]
                                                 },
                                        'pdbx_core': {'INCLUDE': [],
                                                      'EXCLUDE': ['ATOM_SITE',
                                                                  'ATOM_SITE_ANISOTROP'
                                                                  ]
                                                      },
                                        'repository_holdings': {'INCLUDE': ['rcsb_repository_holdings_update', 'rcsb_repository_holdings_current',
                                                                            'rcsb_repository_holdings_unreleased', 'rcsb_repository_holdings_removed',
                                                                            'rcsb_repository_holdings_removed_audit_author',
                                                                            'rcsb_repository_holdings_superseded',
                                                                            'rcsb_repository_holdings_transferred', 'rcsb_repository_holdings_insilico_models'],
                                                                'EXCLUDE': []
                                                                },
                                        'entity_sequence_clusters': {'INCLUDE': ['rcsb_instance_sequence_cluster_list', 'rcsb_entity_sequence_cluster_list',
                                                                                 'software', 'citation', 'citation_author'],
                                                                     'EXCLUDE': []},
                                        'data_exchange': {'INCLUDE': ['rcsb_data_exchange_status'],
                                                          'EXCLUDE': []},
                                        }

        sD['block_attributes'] = {'pdbx': {'ATTRIBUTE_NAME': 'structure_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 12, 'METHOD': 'datablockid()'},
                                  'bird': {'ATTRIBUTE_NAME': 'db_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 10, 'METHOD': 'datablockid()'},
                                  'bird_family': {'ATTRIBUTE_NAME': 'db_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 10, 'METHOD': 'datablockid()'},
                                  'chem_comp': {'ATTRIBUTE_NAME': 'component_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 10, 'METHOD': 'datablockid()'},
                                  'bird_chem_comp': {'ATTRIBUTE_NAME': 'component_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 10, 'METHOD': 'datablockid()'},
                                  'pdb_distro': {'ATTRIBUTE_NAME': 'structure_id', 'CIF_TYPE_CODE': 'code', 'MAX_WIDTH': 12, 'METHOD': 'datablockid()'},
                                  }
        sD['database_names'] = {'pdbx': {'NAME': 'pdbx_v5', 'VERSION': '0_2'},
                                'pdbx_core': {'NAME': 'pdbx_v5', 'VERSION': '0_2'},
                                'bird': {'NAME': 'bird_v5', 'VERSION': '0_1'},
                                'bird_family': {'NAME': 'bird_v5', 'VERSION': '0_1'},
                                'chem_comp': {'NAME': 'chem_comp_v5', 'VERSION': '0_1'},
                                'bird_chem_comp': {'NAME': 'chem_comp_v5', 'VERSION': '0_1'},
                                'pdb_distro': {'NAME': 'stat', 'VERSION': '0_1'},
                                'repository_holdings': {'NAME': 'repository_holdings', 'VERSION': 'v5'},
                                'entity_sequence_clusters': {'NAME': 'sequence_clusters', 'VERSION': 'v5'},
                                'data_exchange': {'NAME': 'data_exchange', 'VERSION': 'v5'},
                                }
        #
        #
        dD['schema_collection_names'] = {'pdbx': ['pdbx_v5_0_2', 'pdbx_ext_v5_0_2'],
                                         'pdbx_core': ['pdbx_core_entity_v5_0_2', 'pdbx_core_entry_v5_0_2', 'pdbx_core_assembly_v5_0_2'],
                                         'bird': ['bird_v5_0_2'],
                                         'bird_family': ['family_v5_0_2'],
                                         'chem_comp': ['chem_comp_v5_0_2'],
                                         'bird_chem_comp': ['bird_chem_comp_v5_0_2'],
                                         'pdb_distro': [],
                                         'repository_holdings': ['repository_holdings_update_v0_1', 'repository_holdings_current_v0_1', 'repository_holdings_unreleased_v0_1',
                                                                 'repository_holdings_removed_v0_1', 'repository_holdings_removed_audit_authors_v0_1',
                                                                 'repository_holdings_superseded_v0_1', 'repository_holdings_transferred_v0_1',
                                                                 'rcsb_repository_holdings_insilico_models_v0_1'],
                                         'entity_sequence_clusters': ['cluster_members_v0_1', 'cluster_provenance_v0_1', 'entity_members_v0_1']
                                         }
        #
        # RCSB_LOAD_STATUS must be included in all INCLUDE filters -
        #
        dD['schema_content_filters'] = {'pdbx_v5_0_2': {'INCLUDE': [],
                                                        'EXCLUDE': ['NDB_STRUCT_CONF_NA',
                                                                    'NDB_STRUCT_FEATURE_NA',
                                                                    'NDB_STRUCT_NA_BASE_PAIR',
                                                                    'NDB_STRUCT_NA_BASE_PAIR_STEP',
                                                                    'PDBX_VALIDATE_CHIRAL',
                                                                    'PDBX_VALIDATE_CLOSE_CONTACT',
                                                                    'PDBX_VALIDATE_MAIN_CHAIN_PLANE',
                                                                    'PDBX_VALIDATE_PEPTIDE_OMEGA',
                                                                    'PDBX_VALIDATE_PLANES',
                                                                    'PDBX_VALIDATE_PLANES_ATOM',
                                                                    'PDBX_VALIDATE_POLYMER_LINKAGE',
                                                                    'PDBX_VALIDATE_RMSD_ANGLE',
                                                                    'PDBX_VALIDATE_RMSD_BOND',
                                                                    'PDBX_VALIDATE_SYMM_CONTACT',
                                                                    'PDBX_VALIDATE_TORSION',
                                                                    'STRUCT_SHEET',
                                                                    'STRUCT_SHEET_HBOND',
                                                                    'STRUCT_SHEET_ORDER',
                                                                    'STRUCT_SHEET_RANGE',
                                                                    'STRUCT_CONF',
                                                                    'STRUCT_CONF_TYPE',
                                                                    'STRUCT_CONN',
                                                                    'STRUCT_CONN_TYPE',
                                                                    'ATOM_SITE',
                                                                    'ATOM_SITE_ANISOTROP',
                                                                    'PDBX_UNOBS_OR_ZERO_OCC_ATOMS',
                                                                    'PDBX_UNOBS_OR_ZERO_OCC_RESIDUES'],
                                                        'SLICE': None
                                                        },

                                        'pdbx_ext_v5_0_2': {'INCLUDE': ['ENTRY', 'NDB_STRUCT_CONF_NA',
                                                                        'NDB_STRUCT_FEATURE_NA',
                                                                        'NDB_STRUCT_NA_BASE_PAIR',
                                                                        'NDB_STRUCT_NA_BASE_PAIR_STEP',
                                                                        'PDBX_VALIDATE_CHIRAL',
                                                                        'PDBX_VALIDATE_CLOSE_CONTACT',
                                                                        'PDBX_VALIDATE_MAIN_CHAIN_PLANE',
                                                                        'PDBX_VALIDATE_PEPTIDE_OMEGA',
                                                                        'PDBX_VALIDATE_PLANES',
                                                                        'PDBX_VALIDATE_PLANES_ATOM',
                                                                        'PDBX_VALIDATE_POLYMER_LINKAGE',
                                                                        'PDBX_VALIDATE_RMSD_ANGLE',
                                                                        'PDBX_VALIDATE_RMSD_BOND',
                                                                        'PDBX_VALIDATE_SYMM_CONTACT',
                                                                        'PDBX_VALIDATE_TORSION',
                                                                        'STRUCT_SHEET',
                                                                        'STRUCT_SHEET_HBOND',
                                                                        'STRUCT_SHEET_ORDER',
                                                                        'STRUCT_SHEET_RANGE',
                                                                        'STRUCT_CONF',
                                                                        'STRUCT_CONF_TYPE',
                                                                        'STRUCT_CONN',
                                                                        'STRUCT_CONN_TYPE',
                                                                        'RCSB_LOAD_STATUS'],
                                                            'EXCLUDE': [],
                                                            'SLICE': None
                                                            },
                                        'pdbx_core_entity_v5_0_2': {'INCLUDE': [], 'EXCLUDE': [], 'SLICE': 'ENTITY'},
                                        'pdbx_core_assembly_v5_0_2': {'INCLUDE': [], 'EXCLUDE': [], 'SLICE': 'ASSEMBLY'},
                                        'pdbx_core_entry_v5_0_2': {'INCLUDE': ['AUDIT_AUTHOR', 'CELL',
                                                                               'CITATION', 'CITATION_AUTHOR', 'DIFFRN', 'DIFFRN_DETECTOR', 'DIFFRN_RADIATION', 'DIFFRN_SOURCE', 'EM_2D_CRYSTAL_ENTITY',
                                                                               'EM_3D_CRYSTAL_ENTITY', 'EM_3D_FITTING', 'EM_3D_RECONSTRUCTION', 'EM_EMBEDDING', 'EM_ENTITY_ASSEMBLY', 'EM_EXPERIMENT',
                                                                               'EM_HELICAL_ENTITY', 'EM_IMAGE_RECORDING', 'EM_IMAGING', 'EM_SINGLE_PARTICLE_ENTITY', 'EM_SOFTWARE', 'EM_SPECIMEN',
                                                                               'EM_STAINING', 'EM_VITRIFICATION', 'ENTRY', 'EXPTL', 'EXPTL_CRYSTAL_GROW', 'PDBX_AUDIT_REVISION_DETAILS',
                                                                               'PDBX_AUDIT_REVISION_HISTORY', 'PDBX_AUDIT_SUPPORT', 'PDBX_DATABASE_PDB_OBS_SPR', 'PDBX_DATABASE_STATUS', 'PDBX_DEPOSIT_GROUP',
                                                                               'PDBX_MOLECULE', 'PDBX_MOLECULE_FEATURES', 'PDBX_NMR_DETAILS', 'PDBX_NMR_ENSEMBLE', 'PDBX_NMR_EXPTL', 'PDBX_NMR_EXPTL_SAMPLE_CONDITIONS',
                                                                               'PDBX_NMR_REFINE', 'PDBX_NMR_SAMPLE_DETAILS', 'PDBX_NMR_SOFTWARE', 'PDBX_NMR_SPECTROMETER', 'PDBX_SG_PROJECT',
                                                                               'RCSB_ATOM_COUNT', 'RCSB_BINDING', 'RCSB_EXTERNAL_REFERENCES', 'RCSB_HAS_CHEMICAL_SHIFT_FILE', 'RCSB_HAS_ED_MAP_FILE',
                                                                               'RCSB_HAS_FOFC_FILE', 'RCSB_HAS_NMR_V1_FILE', 'RCSB_HAS_NMR_V2_FILE', 'RCSB_HAS_STRUCTURE_FACTORS_FILE', 'RCSB_HAS_TWOFOFC_FILE',
                                                                               'RCSB_HAS_VALIDATION_REPORT', 'RCSB_LATEST_REVISION', 'RCSB_MODELS_COUNT', 'RCSB_MOLECULAR_WEIGHT', 'RCSB_PUBMED', 'RCSB_RELEASE_DATE',
                                                                               'REFINE', 'REFINE_ANALYZE', 'REFINE_HIST', 'REFINE_LS_RESTR', 'REFLNS', 'REFLNS_SHELL', 'SOFTWARE', 'STRUCT', 'STRUCT_KEYWORDS', 'SYMMETRY',
                                                                               'RCSB_LOAD_STATUS', 'RCSB_ENTRY_CONTAINER_IDENTIFIERS', 'PDBX_SERIAL_CRYSTALLOGRAPHY_MEASUREMENT',
                                                                               'PDBX_SERIAL_CRYSTALLOGRAPHY_SAMPLE_DELIVERY',
                                                                               'PDBX_SERIAL_CRYSTALLOGRAPHY_SAMPLE_DELIVERY_INJECTION',
                                                                               'PDBX_SERIAL_CRYSTALLOGRAPHY_SAMPLE_DELIVERY_FIXED_TARGET',
                                                                               'PDBX_SERIAL_CRYSTALLOGRAPHY_DATA_REDUCTION'],
                                                                   'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_update_v0_1': {'INCLUDE': ['rcsb_repository_holdings_update'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_current_v0_1': {'INCLUDE': ['rcsb_repository_holdings_current'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_unreleased_v0_1': {'INCLUDE': ['rcsb_repository_holdings_unreleased'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_removed_v0_1': {'INCLUDE': ['rcsb_repository_holdings_removed'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_removed_audit_authors_v0_1': {'INCLUDE': ['rcsb_repository_holdings_removed_audit_author'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_superseded_v0_1': {'INCLUDE': ['rcsb_repository_holdings_superseded'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_transferred_v0_1': {'INCLUDE': ['rcsb_repository_holdings_transferred'], 'EXCLUDE': [], 'SLICE': None},
                                        'repository_holdings_insilico_models_v0_1': {'INCLUDE': ['rcsb_repository_holdings_insilico_models'], 'EXCLUDE': [], 'SLICE': None},
                                        'cluster_members_v0_1': {'INCLUDE': ['rcsb_entity_sequence_cluster_list'], 'EXCLUDE': [], 'SLICE': None},
                                        'cluster_provenance_v0_1': {'INCLUDE': ['software', 'citation', 'citation_author'], 'EXCLUDE': [], 'SLICE': None},
                                        'entity_members_v0_1': {'INCLUDE': ['rcsb_entity_sequence_cluster_list'], 'EXCLUDE': [], 'SLICE': None},
                                        'rcsb_data_exchange_status_v0_1': {'INCLUDE': ['rcsb_data_exchange_status'], 'EXCLUDE': [], 'SLICE': None},
                                        }

        dD['collection_attribute_names'] = {'pdbx_v5_0_2': ['entry.id'],
                                            'pdbx_ext_v5_0_2': ['entry.id'],
                                            'pdbx_core_entity_v5_0_2': ['entry.id', 'entity.id'],
                                            'pdbx_core_assembly_v5_0_2': ['entry.id', 'pdbx_struct_assembly.id'],
                                            'pdbx_core_entry_v5_0_2': ['entry.id'],
                                            'bird_v5_0_2': ['pdbx_reference_molecule.prd_id'],
                                            'family_v5_0_2': ['pdbx_reference_molecule_family.family_prd_id'],
                                            'chem_comp_v5_0_2': ['chem_comp.component_id'],
                                            'bird_chem_comp_v5_0_2': ['chem_comp.component_id'],
                                            'repository_holdings_update_v0_1': ['update_id'],
                                            'repository_holdings_current_v0_1': ['update_id'],
                                            'repository_holdings_unreleased_v0_1': ['update_id'],
                                            'repository_holdings_removed_v0_1': ['update_id'],
                                            'repository_holdings_removed_audit_authors': ['update_id'],
                                            'repository_holdings_superseded_v0_1': ['update_id'],
                                            'repository_holdings_transferred_v0_1': ['update_id'],
                                            'repository_holdings_insilico_models_v0_1': ['update_id'],
                                            'cluster_members_v0_1': ['update_id'],
                                            'cluster_provenance_v0_1': ['software.name'],
                                            'entity_members_v0_1': ['update_id'],
                                            'rcsb_data_exchange_status_v0_1': ['update_id', 'database_name', 'object_name'],
                                            }
        #
        dD['collection_subcategory_aggregates'] = {'cluster_members_v0_1': ['sequence_membership'],
                                                   'entity_members_v0_1': ['cluster_membership']
                                                   }
        #
        return cfgD


if __name__ == '__main__':
    mc = MakeConfig()
    #
