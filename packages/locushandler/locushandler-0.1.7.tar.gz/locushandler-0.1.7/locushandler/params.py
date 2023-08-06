"""
Parameters for Locus Codes
"""

DIVS = set(['div', 'diva', 'divs', 'div4div', 'diva4diva'])

GRANULARITY = [
    '1x6', '1x6x4'
    '4x1', '4x6', '4x6x4',
    '12x1', '12x6', '12x6x4',
    '36x1', '36x6', '36x6x4', 'full']

LOCUS_OUTPUT_TYPE = ['list', 'dict', 'string']

TABLE_OUTPUT_TYPE = ['path', 'df']

BARCODE_FIELDS = {'enterprise_locus': 'work', 'intermediary_1_locus': 'work',
                  'intermediary_2_locus': 'work', 'customer_locus': 'work',
                  'constituent_resource_1': 'resource',
                  'constituent_resource_2': 'resource',
                  'work_group_1': 'work'}

LOCUS_FIELDS = {'work': ['dr1', 'dr2', 'dr3', 'a1', 'a2', 'a3',
                         'r1', 'r2', 'r3', 'io1', 'io2', 'io3'],
                'resource': ['sub1', 'sub2', 'sub3', 'a1', 'a2', 'a3', 'r1', 'r2', 'r3']}

ACT_GRAN_TO_FIELDS = {'1': [], '4': ['a1'],
                      '12': ['a1', 'a2'], '36': ['a1', 'a2', 'a3']}
RES_GRAN_TO_FIELDS = {'1': [], '6': ['r1'], '6x4': [
    'r1', 'r2'], '6x4x3': ['r1', 'r2', 'r3']}

# {activity: requirement}
DR_LOCI = {'1': 'some', '2': 'some', '3': 'some', '1.2': 'some',
           '1.3': 'some', '2.2': 'some', '3.1': 'some', '3.2': 'some',
           '1.2.2': 'all', '1.2.3': 'all', '2.2.2': 'F',
           '1.3.2': 'some', '3.1.2': 'some', '3.2.2': 'all'}

IO_LOCI = {'1': 'some', '2': 'some', '3': 'some',  '4':'some',
           '1.1': 'all', '1.2': 'some', '1.3': 'some', '2.1': 'all',
           '2.2': 'some', '2.3': 'some', '3.1': 'some', '3.2': 'some',
           '3.3': 'some', '4.1': 'all', '4.2': 'some', '4.3': 'some',
           '1.1.1': 'all', '1.1.2': 'all', '1.1.3': 'all',
           '1.2.1': 'all', '1.3.1': 'some', '1.3.3': 'all',
           '2.1.1': 'all', '2.1.2': 'all', '2.1.3': 'all',
           '2.2.1': 'some', '2.3.1': 'all', '2.3.3': 'all',
           '3.1.1': 'all', '3.1.2': 'some', '3.1.3': 'all',
           '3.2.1': 'all', '3.2.3': 'all', '3.3.1': 'some',
           '3.3.3': 'all', '4.1.1': 'all', '4.1.2': 'all',
           '4.1.3': 'all', '4.2.1': 'all', '4.2.2': 'some',
           '4.2.3': 'some', '4.3.1': 'all', '4.3.2': 'all',
           '4.3.3': 'all'}
