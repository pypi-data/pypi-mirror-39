'''
Module that validates loci
'''
from locushandler.params import (DR_LOCI, IO_LOCI)

class LocusValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def validate_activity(locus_field):
    '''
    Read through the input dictionary. Check each value against a list of
    valid values for that key. Raises LocusValidationError for any errors 
    found

    Dependencies :
    is called : validate_locus

    :param locus_field: (dict)
    :return: 
    '''
    
    act_fields = locus_field['act']
    
    part_4 = act_fields.get('a1')
    part_12 = act_fields.get('a2')
    part_36 = act_fields.get('a3')
    
    if part_4 not in ['1', '2', '3', '4', 'V']:
        raise LocusValidationError('Phase 4 activity must be 1-4 or V.')
    for field in [part_12, part_36]:
        if field and field not in ['1', '2', '3']:
            raise LocusValidationError('Phase 12 and 36 activities must be 1-3.')
    if part_36 and not part_12:
        raise LocusValidationError('Phase 36 cannot be defined without Phase 12.')
    parts = set([part_4, part_12, part_36])
    if 'V' in parts and len(parts) != 1:
        raise LocusValidationError('All phases must be V for V activities.')

    return

def validate_resource(locus_field):
    '''
    Read through the input dictionary and validates each resource present. 
    Check each value against a list of valid values for that key. Raises
    LocusValidationError for any error found.

    Dependencies :
    is called : validate_locus

    :param locus_field: (dict)
    :return: 
    '''
    for r in [rs for rs in locus_field.keys() if rs != 'act']:
        res_fields = locus_field[r]

        category = res_fields.get('r1')
        stage = res_fields.get('r2')
        substage = res_fields.get('r3')

        if category not in ['A', 'B', 'C', 'D', 'E', 'F', 'V']:
            raise LocusValidationError('Resource category must be A-F or V.')
        if substage and not stage:
            raise LocusValidationError('Resource substage cannot be defined without the stage.')
        if stage and stage not in ['1', '2', '3', '4', 'V']:
            raise LocusValidationError('Resource stage must be 1-4 or V.')
        if substage and substage not in ['i', 'ii', 'iii', 'V']:
            raise LocusValidationError('Resource substage must be i-iii or V.')
        if category == 'V' and (stage != 'V' or substage != 'V'):
            raise LocusValidationError('Resource staging must be V for V resources.')
        if stage == 'V' and substage != 'V':
            raise LocusValidationError('Resource substage must be V for V stages.')

    return

def validate_dr(locus_field):
    '''
    Read through the input dictionary. If the activity and object combination
    contain values that indicate that a DR is required, check the existence
    of a DR. Raises LocusValidationError for any errors found.

    Dependencies :
    is called : validate_locus

    :param locus_field: (dict)
    :return: (boolean or dict)
    '''
    act = flatten(locus_field, 'act')
    dr = flatten(locus_field, 'dr')
    obj = flatten(locus_field, 'res')
    
    if act not in DR_LOCI:
        if dr != '':
            raise LocusValidationError('{} never takes a DR. {} given.'.format(act, dr))
    else:
        dr_req = DR_LOCI[act]
        if dr_req == 'all': 
            if dr == '':
                raise LocusValidationError('{} always takes a DR. None given.'.format(act))
        elif dr_req == 'some':
            pass
        else:
            if obj != dr_req:
                raise LocusValidationError('{} only takes a DR when the object is F. {} given.'.format(act, dr))
    return
            
## FIXME 
## can be more comprehensive to check that the C resource given is proper stage
## (view reference handbook)
def validate_io(locus_field):
    '''
    Read through the input dictionary. If the activity and object combination
    contain values that indicate that an IO is required, check the existence
    of a IO. In addition, check that the IO is a C resource. Raises 
    LocusValidationError for any errors found

    Dependencies :
    is called : validate_locus

    :param locus_field: (dict)
    :return: 
    '''
    act = flatten(locus_field, 'act')
    io = flatten(locus_field, 'io')
    if io and io[0] != 'C':
        raise LocusValidationError('IO is always a C resource. {} given.'.format(io))
 
    if act not in IO_LOCI:
        if io != '':
            raise LocusValidationError('{} never takes an IO. {} given.'.format(act, io))
    else:
        io_req = IO_LOCI[act]
        if io_req == 'all' and io == '':
           raise LocusValidationError('{} always takes an IO. None given.'.format(act))
    
    return
     

def validate_locus(locus_field, locus_type):
    '''
    Read through the input string and validate that it is in accordance with
    Locus theory: activity domain, resource domain, io domain. For work loci,
    check whether a dr or an io are required and supplied.   

    Dependencies :
    call : validate_activity , validate_resource, validate_dr, validate_io
    is called : work_parser, resource_parser

    :param locus_field: (dict)
    :param locus_type: (string)
    :return: ()  
    '''
    try:
        validate_activity(locus_field)
        validate_resource(locus_field)
    except LocusValidationError:
        raise
    if locus_type == 'work':
        try:
            if 'dr' in locus_field:
                validate_dr(locus_field)
            if 'io' in locus_field:
                validate_io(locus_field)
        except LocusValidationError:
            raise
    return 
    
## HELPER
def flatten(locus_field, field):
    '''
    Given a dictionary of locus fields, concatenate fields
    field: dr, act, res, or io
    '''
    fields = sorted(list(locus_field[field]))
    if field == 'act':
        flat = '.'.join(locus_field[field][x] for x in fields)
        if 'V' in flat:
            flat = 'V'
    else: # resource 
        flat = ''.join(locus_field[field][x] for x in fields)
        if flat:
            # only take first letter for F and V resources
            # F or V instead of FVV or VVV
            if flat[0] == 'V' or flat[0] == 'F':
                flat = flat[0]
            # only take first two letters for div stage
            # AV instead of AVV
            elif flat[1] == 'V':
                flat = flat[:2]
    
    return flat


