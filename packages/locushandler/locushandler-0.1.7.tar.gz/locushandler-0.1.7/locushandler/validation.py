'''
Module that validates loci
'''
import locushandler.params as par

class LocusValidationError(Exception):
    '''
    Custom Exception class for errors thrown when validating loci
    '''
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def validate_activity(locus_fields):
    '''
    Read through the input dictionary. Check each value against a list of
    valid values for that key. Raises LocusValidationError for any errors
    found

    Dependencies :
    is called : validate_locus

    :param locus_fields: (dict)
    :return:
    '''

    act_fields = locus_fields['act']

    part_4 = act_fields.get('a1')
    part_12 = act_fields.get('a2')
    part_36 = act_fields.get('a3')
    
    if part_4 not in ['1', '2', '3', '4', 'V']:
        raise LocusValidationError(f'Phase 4 activity must be 1-4 or V. {part_4} given.')
    
    if part_12:
        if part_12 not in ['1', '2', '3', 'V']:
            raise LocusValidationError(f'Phase 12 activity must be 1-3 or V. {part_12} given.')
        if part_12 == 'V' and part_4 != 'V':
            raise LocusValidationError(f'Phase 12 is V, Phase 4 is {part_4}. Div values not allowed unless Phase 4 is div.')
        if part_12 != 'V' and part_4 == 'V':
             raise LocusValidationError(f'Phase 4 is V, but Phase 12 and 36 are {part_12} and {part_36}. All phases must be V for V activities.')
 
    if part_36:
        if part_36 not in ['1', '2', '3', 'V']:
            raise LocusValidationError(f'Phase 36 activity must be 1-3 or V. {part_36} given.')
        if part_36 == 'V' and part_4 != 'V':
            raise LocusValidationError(f'Phase 36 is V, Phase 4 is {part_4}. Div values not allowed unless Phase 4 is div.')
        if part_36 != 'V' and part_4 == 'V':
            raise LocusValidationError(f'Phase 4 is V, but Phase 12 and 36 are {part_12} and {part_36}. All phases must be V for V activities.')
 

    return

def validate_resource(locus_fields):
    '''
    Read through the input dictionary and validates each resource present.
    Check each value against a list of valid values for that key. Raises
    LocusValidationError for any error found.

    Dependencies :
    is called : validate_locus

    :param locus_fields: (dict)
    :return:
    '''
    for rsrc in ['subj', 'res']:
        if rsrc not in locus_fields:
            continue
        
        res_fields = locus_fields[rsrc]

        category = res_fields.get('r1')
        stage = res_fields.get('r2')
        substage = res_fields.get('r3')

        if category not in ['A', 'B', 'C', 'D', 'E', 'F', 'V']:
            raise LocusValidationError(f'Resource category must be A-F or V. {category} given.')
        
        if stage:
            if stage not in ['1', '2', '3', '4', 'V']:
                raise LocusValidationError(f'Resource stage must be 1-4 or V. {stage} given.')
            if stage != 'V' and category == 'V':
                raise LocusValidationError(f'Resource staging must be V for V resources. {stage} and {substage} given as the stage and substage.')
        
        if substage:
            if substage not in ['i', 'ii', 'iii', 'V']:
                raise LocusValidationError(f'Resource substage must be i-iii or V. {substage} given.')            
            if substage != 'V' and stage == 'V':
                raise LocusValidationError(f'Resource substage must be V for V stages. {substage} given as the substage.')
            if substage != 'V' and category == 'V':
                raise LocusValidationError(f'Resource staging must be V for V resources. {stage} and {substage} given as the stage and substage.')
 
    return

def validate_dr(locus_fields):
    '''
    Read through the input dictionary. If the activity and object combination
    contain values that indicate that a DR is required, check the existence
    of a DR. Raises LocusValidationError for any errors found.

    Dependencies :
    is called : validate_locus

    :param locus_fields: (dict)
    :return: (boolean or dict)
    '''
    act = _flatten(locus_fields, 'act')
    dr = _flatten(locus_fields, 'dr')
    obj = _flatten(locus_fields, 'res')

    if act not in par.DR_LOCI:
        if dr != '':
            raise LocusValidationError('{} never takes a DR. {} given.'.format(act, dr))
    else:
        dr_req = par.DR_LOCI[act]
        if dr_req == 'all':
            if dr == '':
                raise LocusValidationError('{} always takes a DR. None given.'.format(act))
        elif dr_req == 'some':
            pass
        else:
            if dr and obj != dr_req:
                raise LocusValidationError('{} only takes a DR when the object is F. {} given.'.format(act, dr))
    return

## can be more comprehensive to check that the C resource given is proper stage
## (view reference handbook)
def validate_io(locus_fields):
    '''
    Read through the input dictionary. If the activity and object combination
    contain values that indicate that an IO is required, check the existence
    of a IO. In addition, check that the IO is a C resource. Raises
    LocusValidationError for any errors found

    Dependencies :
    is called : validate_locus

    :param locus_fields: (dict)
    :return:
    '''
    act = _flatten(locus_fields, 'act')
    io = _flatten(locus_fields, 'io')
    if io and io[0] != 'C':
        raise LocusValidationError('IO is always a C resource. {} given.'.format(io))

    if act not in par.IO_LOCI:
        if io != '':
            raise LocusValidationError('{} never takes an IO. {} given.'.format(act, io))
    else:
        io_req = par.IO_LOCI[act]
        if io_req == 'all' and io == '':
            raise LocusValidationError('{} always takes an IO. None given.'.format(act))
    return


def validate_locus(locus_fields):
    '''
    Read through the input string and validate that it is in accordance with
    Locus theory: activity domain, resource domain, io domain. For work loci,
    check whether a dr or an io are required and supplied.

    Dependencies :
    call : validate_activity , validate_resource, validate_dr, validate_io
    is called : work_parser, resource_parser

    :param locus_fields: (dict)
    :param locus_type: (string)
    :return: ()
    '''
    try:
        validate_activity(locus_fields)
        validate_resource(locus_fields)
        if 'dr' in locus_fields:
            validate_dr(locus_fields)
        if 'io' in locus_fields:
            validate_io(locus_fields)
    except LocusValidationError:
        raise
    return

## HELPER
def _flatten(locus_fields, field):
    '''
    Given a dictionary of locus fields, concatenate fields
    field: dr, act, res, or io
    '''
    fields = sorted(list(locus_fields[field]))
    if field == 'act':
        flat = '.'.join(locus_fields[field][x] for x in fields)
        if 'V' in flat:
            flat = 'V'
    else: # resource
        flat = ''.join(locus_fields[field][x] for x in fields)
        if flat:
            # only take first letter for F and V resources
            # F or V instead of FVV or VVV
            if len(flat) == 1 or flat[0] == 'V' or flat[0] == 'F':
                flat = flat[0]
            # only take first two letters for div stage
            # AV instead of AVV
            elif flat[1] == 'V':
                flat = flat[:2]

    return flat


