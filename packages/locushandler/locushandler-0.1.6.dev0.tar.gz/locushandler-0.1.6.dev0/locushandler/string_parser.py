"""String parser for Locus strings. Parse a Locus string
to dict or list or string at specified levels of granularity"""

from locushandler.params import (DIVS, BARCODE_FIELDS, LOCUS_OUTPUT_TYPE,
                        RES_GRAN_TO_FIELDS, ACT_GRAN_TO_FIELDS)
import locushandler.string_helpers as shlp

def string_parser(locus_field, output_type, granularity="full",
                  barcode_field=None, dr=False, io=False):
    '''
    Read through the input string and identify the different Loci within
    the string.
    Calls work_parser and resource_parser on work and resource loci.
    The output type is specified by the user.

    Dependencies :
    call : work_parser, resource_parser

    :param locus_field: (string)
    :param output_type: (string) from LOCUS_OUTPUT_TYPE
    :param granularity: (string) from GRANULARITY
    :param barcode_field: (string) from BARCODE_FIELDS
    :param dr: (bool)
    :param io: (bool)
    :return: parsed : (string, dict or list)
    '''
    try:
        if barcode_field is None:
            # if barcode_field is not specified
            # automatically deduce field as work or resource
            field_type = shlp.work_or_resource(locus_field)
        else:
            field_type = BARCODE_FIELDS[barcode_field]

        if field_type == 'work':
            return work_parser(locus_field, output_type, granularity,
                               show_dr=dr, show_io=io)
    except KeyError:
        print(f"Key should be in {BARCODE_FIELDS.keys()}")
        raise

    else:
        return resource_parser(locus_field, output_type, granularity)


def work_parser(locus_field, output_type, granularity, show_dr=True, show_io=True):
    '''
    Read through the input string and identify each element at the finest
    granularity level.
    Return all those elements or only the one of interest based on the
    granularity argument.

    Dependencies :
    is called : string_parser

    :param locus_field: (string)
    :param output_type: (string) from LOCUS_OUTPUT_TYPE
    :param granularity: (string) from GRANULARITY
    :param show_io: (boolean)
    :param show_dr: (boolean)
    :return: parsed : (string, dict or list)
    '''
    assert isinstance(output_type, str), 'Expect output_type to be a string'
    assert output_type in LOCUS_OUTPUT_TYPE, f'Expect output_type to be from {LOCUS_OUTPUT_TYPE}'

    dr, io = shlp.extract_dr_io(locus_field)
    dr = dr if show_dr else None
    io = io if show_io else None

    locus_verb, locus_object = shlp.remove_dr_io(locus_field).split()
    verb_granularity, noun_granularity = shlp.parse_granularity(granularity)

    if output_type == 'dict':
        return work_dict_parser(dr, locus_verb, locus_object, io,
                                verb_granularity, noun_granularity)
    elif output_type == 'list':
        return work_list_parser(dr, locus_verb, locus_object, io,
                                verb_granularity, noun_granularity)
    elif output_type == 'string':
        return work_string_parser(dr, locus_verb, locus_object, io,
                                  verb_granularity, noun_granularity)


def work_string_parser(dr, locus_verb, locus_object, io,
                       verb_granularity, noun_granularity):
    '''
    Read through input strings and parse to string
    :param dr: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :param io: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (string)
    '''
    parsed_dict = work_dict_parser(dr, locus_verb, locus_object, io,
                                   verb_granularity, noun_granularity)

    act = parse_verb_to_string(parsed_dict['act'])
    res = parse_noun_to_string(parsed_dict['res'])

    # dr, io not always there. Have them be empty substrings
    # for concatenation later if that's the case
    dr = parse_noun_to_string(parsed_dict['dr']) if dr else ''
    io = parse_noun_to_string(parsed_dict['io']) if io else ''
    return f'{dr} {act} {res} {io}'.strip()


def work_list_parser(dr, locus_verb, locus_object, io,
                     verb_granularity, noun_granularity):
    '''
    Read through input strings and parse to list
    :param dr: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :param io: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (list)
    '''
    parsed_dict = work_dict_parser(dr, locus_verb, locus_object, io,
                                   verb_granularity, noun_granularity)
    return shlp.unravel_nested_dict_to_list(parsed_dict)


def work_dict_parser(dr, locus_verb, locus_object, io,
                     verb_granularity, noun_granularity):
    '''
    Read through input strings and parse to dict
    :param dr: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :param io: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (dict)
    '''
    assert isinstance(
        verb_granularity, str), 'Expect verb_granularity to be a string'
    assert isinstance(
        noun_granularity, str), 'Expect noun_granularity to be a string'

    parsed = {}
    if dr != None:
        parsed['dr'] = {}
    parsed['act'] = {}
    parsed['res'] = {}
    if io != None:
        parsed['io'] = {}
    # if we choose to exclude dr, io
    # their values would be None --> do not initialize field
    # if we choose to include but dr, io not found
    # their values would be empty string

    noun_fields = RES_GRAN_TO_FIELDS[noun_granularity]
    for field in noun_fields:
        parsed['res'][field] = noun_parser(
            locus_object)[field]

        if dr != None:
            parsed['dr'][field] = noun_parser(dr)[field]
        if io != None:
            parsed['io'][field] = noun_parser(io)[field]

    verb_fields = ACT_GRAN_TO_FIELDS[verb_granularity]
    for field in verb_fields:
        parsed['act'][field] = verb_parser(locus_verb)[field]

    return parsed


def resource_parser(locus_field, output_type, granularity):
    '''
    Read through the input string and identify each element at the finest
    granularity level.
    Return all those elements or only the one of interest based on the
    granularity argument.

    Dependencies:
    is called: string_parser

    :param locus_field: (string)
    :param output_type: (string) from LOCUS_OUTPUT_TYPE
    :param granularity: (string) from GRANULARITY
    :return: parsed : (string, dict or list)
    '''
    assert isinstance(output_type, str), 'Expect output_type to be a string'
    assert output_type in LOCUS_OUTPUT_TYPE, f'Expect output_type to be from {LOCUS_OUTPUT_TYPE}'

    locus_subject, locus_verb, locus_object = locus_field.split()
    verb_granularity, noun_granularity = shlp.parse_granularity(granularity)
    if output_type == 'dict':
        return resource_dict_parser(locus_subject, locus_verb, locus_object,
                                    verb_granularity, noun_granularity)
    elif output_type == 'list':
        return resource_list_parser(locus_subject, locus_verb, locus_object,
                                    verb_granularity, noun_granularity)
    elif output_type == 'string':
        return resource_string_parser(locus_subject, locus_verb, locus_object,
                                      verb_granularity, noun_granularity)


def resource_string_parser(locus_subject, locus_verb, locus_object,
                           verb_granularity, noun_granularity):
    '''
    Read through inputs and parse to a string
    :param locus_subject: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (string)
    '''
    parsed_dict = resource_dict_parser(locus_subject, locus_verb, locus_object,
                                       verb_granularity, noun_granularity)
    sub = parse_noun_to_string(parsed_dict['sub'])
    act = parse_verb_to_string(parsed_dict['act'])
    res = parse_noun_to_string(parsed_dict['res'])
    return f'{sub} {act} {res}'


def resource_list_parser(locus_subject, locus_verb, locus_object,
                         verb_granularity, noun_granularity):
    '''Read through inputs and parse to list
    :param locus_subject: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (list)'''
    parsed_dict = resource_dict_parser(locus_subject, locus_verb, locus_object,
                                       verb_granularity, noun_granularity)
    return shlp.unravel_nested_dict_to_list(parsed_dict)


def resource_dict_parser(locus_subject, locus_verb, locus_object,
                         verb_granularity, noun_granularity):
    '''
    Read through input strings and parse to dict
    :param locus_subject: (string)
    :param locus_verb: (string)
    :param locus_object: (string)
    :verb_granularity: (string)
    :noun_granularity: (string)
    :return: parsed (dict)
    '''
    assert isinstance(
        verb_granularity, str), 'Expect verb_granularity to be a string'
    assert isinstance(
        noun_granularity, str), 'Expect noun_granularity to be a string'

    parsed = {'sub': {}, 'act': {}, 'res': {}}

    noun_fields = RES_GRAN_TO_FIELDS[noun_granularity]
    for field in noun_fields:
        parsed['sub'][field] = noun_parser(
            locus_subject)[field]
        parsed['res'][field] = noun_parser(
            locus_object)[field]

    verb_fields = ACT_GRAN_TO_FIELDS[verb_granularity]
    for field in verb_fields:
        parsed['act'][field] = verb_parser(locus_verb)[field]

    return parsed


def verb_parser(locus_verb):
    '''
    Given single Locus verb (e.g. 1.3.2), parse
    to full granularity.
    :param locus_verb: (string)
    :return: parsed (dict)
    '''
    assert isinstance(
        locus_verb, str), f'Expect locus_verb: {locus_verb} to be a string'
    if locus_verb.lower() in DIVS:
        a1, a2, a3 = 'V', 'V', 'V'
    else:
        a1, a2, a3 = locus_verb.split('.')

    return {'a1': a1, 'a2': a2, 'a3': a3}


def noun_parser(locus_noun):
    '''
    Given single Locus noun (e.g. C4iii), parse
    to full granularity.
    :param locus_noun: (string)
    :return: parsed (dict)
    '''
    assert isinstance(
        locus_noun, str), f'Expect locus_noun: {locus_noun} to be a string'

    if shlp.dediv_noun(locus_noun):
        # if the noun has some Divvy fields in it
        r1, r2, r3 = shlp.dediv_noun(locus_noun)
    elif locus_noun == 'F':
        r1, r2, r3 = 'F', 'V', 'V'
    elif locus_noun == '':
        r1, r2, r3 = '', '', ''
    else:
        r1, r2, r3 = locus_noun[0], locus_noun[1], locus_noun[2:]

    return {'r1': r1, 'r2': r2, 'r3': r3}

# HELPER for functions that parse to strings


def parse_noun_to_string(locus_noun_field):
    '''Given parse dictionary field that is a locus noun
    Parse to appropriate string, handling Div's and F
    :param locus_noun_field: (dict)
    :return: parsed (string)
    '''
    to_parse = []
    for value in locus_noun_field.values():
        if value == 'V':
            # the whole resource is Div, return immediately
            return 'V'
        elif value == 'F':
            # F has no staging
            return 'F'
        else:
            to_parse.append(value)
    return ''.join(to_parse)


def parse_verb_to_string(locus_verb_field):
    '''Given parse dictionary field that is a locus verb
    Parse to appropriate string, handling Div's
    :param locus_noun_field: (dict)
    :return: parsed (string)
    '''
    to_parse = []
    for value in locus_verb_field.values():
        if value == 'V':
            # the whole resource is Div, return immediately
            return 'V'
        else:
            to_parse.append(value)
    return '.'.join(to_parse)
