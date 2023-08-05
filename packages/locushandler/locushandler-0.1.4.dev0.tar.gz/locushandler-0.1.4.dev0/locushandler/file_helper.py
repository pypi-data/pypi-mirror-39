"""
Helper functions for Locus code parsing

"""

from locushandler.params import ACT_GRAN_TO_FIELDS, RES_GRAN_TO_FIELDS


def gran_to_fields(str_gran, type_loci, dr=False, io=False):
    """
    Returns a list of the fields given a granularity and a type of field

    :param str_gran: (string) granularity with the format '4x6', '12x6x4x3', etc...
    :param type: (string) 'work' or 'resource'
    :param dr: (bool) True if you want to include the dr
    :param io: (bool) True if you want to include the io
    :return: (list of string) list of all corresponding Loci fields
    """
    try:
        if str_gran == 'full':
            str_gran='36x6x4x3'
            dr=True
            io=True
        actx = str_gran.find('x')
        fields_act = ACT_GRAN_TO_FIELDS[str_gran[:actx]]
        fields_res = RES_GRAN_TO_FIELDS[str_gran[actx + 1:]]

        # For a work Loci : [dr] + [act] + [res] + [io]
        if type_loci == 'work':
            if dr:
                fields_dr = ['d' + field for field in fields_res]
                all_f = fields_dr + fields_act + fields_res
            else:
                all_f = fields_act + fields_res
            if io:
                fields_io = ['io' + field[-1] for field in fields_res]
                all_f += fields_io
        # For a resource Loci : [sub] + [act] + [res]
        else:
            all_f = ['sub' + field[-1] for field in fields_res]
            all_f = all_f + fields_act + fields_res
        return all_f
    except KeyError:
        print('Make sure the granularity specified has the following format:')
        print(
            '{act}x{res} with act in [1,4,12,36] and res in [1, 6, 6x4, 6x4x3] ')
