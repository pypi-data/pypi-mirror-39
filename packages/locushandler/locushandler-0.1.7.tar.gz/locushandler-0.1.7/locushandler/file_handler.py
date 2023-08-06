"""
Module for processing files with Locus codes
"""
import os
import re
import pandas as pd
from locushandler.params import BARCODE_FIELDS
import locushandler.file_helper as fh
import locushandler.string_parser as sp
from locushandler.validation import LocusValidationError

def find_errors(df, column_of_interest):
    """
    Take in a dataframe that has a column containing loci.
    Iterate through the column to find the specific errors
    associated with each line if they exist. 

    :param df: (DataFrame) 
    :param column_of_interest: (string) column to check for errors

    :return: (dict) line numbers in the dataframe that have errors,
            with respective error messages
    """
    errors = {}
    args = {'output_type': 'dict',
            'granularity': 'full',
            'dr': True, 'io': True}
    for idx, row in df.iterrows():
        try:
            sp.string_parser(row[column_of_interest], **args)
        except LocusValidationError as e:
            errors[idx] = str(e)
            continue
    return errors

def parse_file(file_path, column_of_interest, output_type, granularity, dr, io):
    """
    Take in a file that has or multiple columns with barcode field in them.
    Parse the column specified and break them down into multiple columns,
    each of them containing a very granular element of a field.
    The output path is standardized.

    :param file_path: (string) full path of the file with barcode field to
     parse
    :param column_of_interest: (string) column to parse from the locus
                                        Barcode, from BARCODE_FIELDS

    :param granularity: (string) in GRANULARITY
    :return: parsed_file: (string or dataframe) path of the parsed file
                        or dataframe with the file with added columns
    """
    try:
        df_data = pd.read_csv(file_path)
        df_data.dropna(subset=[column_of_interest], axis=0, inplace=True)

        # Parse column_of_interest into list
        args_parser = ('list', granularity, column_of_interest.lower(), dr, io,)
        df_data[column_of_interest] = df_data[column_of_interest].astype(str).apply(
            sp.string_parser,
            args=args_parser)

        # Expand list into dataframe columns
        type_column = BARCODE_FIELDS[column_of_interest.lower()]
        list_elements = fh.gran_to_fields(granularity, type_column, dr, io)
        df_data[list_elements] = pd.DataFrame(df_data[column_of_interest].values.tolist(),
                                              index=df_data.index)
        df_data.drop(column_of_interest, 1, inplace=True)

    except KeyError:
        print('Make sure column_of_interest appears in your file and is a valid barcode field.')
        raise
    except FileNotFoundError:
        print('The file you want to open doesn\'t exist.')
        raise
    except LocusValidationError:
        errors = find_errors(df_data, column_of_interest)
        print('The following errors were found in the file you want to parse:')
        for error in errors:
            print('line {}: {}'.format(error, errors[error]))

    if output_type == 'path':
        # Create standardized output path
        # 'data/intermediary/inpath_parsed_granularity_column.csv'
        if '/' in file_path:
            # If file is in another folder .../.../.../file.csv
            p = re.compile(r'(?P<file>(\w|\W)*(\w*/)*\w*).csv')
        else :
            # If file is in current folder file.csv
            p = re.compile(r'(?P<file>(\w|\W)*).csv')
        m = p.search(file_path)
        file_name = m.group('file')
        # Add suffix at end of file
        output = '_'.join([file_name, 'parsed',
                            granularity, column_of_interest]) + '.csv'
        df_data.to_csv(output, index=False)
        return output
    return df_data


def map_to_locus(file_path, code_column, classification_system, crosswalk_path, column_of_interest,
                 granularity, dr, io):
    """
    Takes in a file that uses a classification system, and uses the parsed
    crosswalk
    to translate codes into Locus function with the specified granularity.
    Either adds multiple columns to the table (one for each element of the
    barcode fields)or just add one column with the desired granularity.
    The output path is standardized.

    :param file_path: (string) full path of the input file
    :param code_column: (string) name of the column of the classification system in the file to map
    :param classification_system: (string) name of the column of the classification
            system in the crosswalk file
    :param crosswalk_path: (string) full path of the crosswalk csv
    :param output_type: (string) from TABLE_OUTPUT_TYPE
    :param granularity: (string) from GRANULARITY
    :param column_of_interest: (string) column to retrieve from the locus
                                        Barcode, from BARCODE_FIELDS
    :return:(string or dataframe) path of the mapped file
                        or dataframe with Locus fields

    """
    try:
        df_data = pd.read_csv(file_path)
        df_map = get_mapping(crosswalk_path=crosswalk_path,
                             classification_system=classification_system,
                             column_of_interest=column_of_interest,
                             granularity=granularity, dr=dr, io=io)
        df_data[code_column] = df_data[code_column].astype(str)
        df_map[classification_system] = df_map[classification_system].astype(str)
        df_data = df_data.merge(df_map, left_on=code_column,
                                right_on=classification_system).drop(classification_system, 1)
        return df_data
    except KeyError:
        print('Make sure you input the right name of column for the classification system '
              'in the file you want to map to Locus.')
        raise


def get_mapping(crosswalk_path, classification_system, column_of_interest, granularity, dr, io):
    """
       Takes in a classification system, and builds the locus mapping at the right granularity

       :param classification_system: (string) name of the column in the crosswalk file
       :param crosswalk_path: (string) full path of the crosswalk csv
       :param granularity: (string) from GRANULARITY
       :param column_of_interest: (string) column to retrieve from the locus
                                        Barcode, from BARCODE_FIELDS
       :param dr, io (bool) : include or not dr and io in the final df
       :return:(dataframe) dataframe with two columns, classification code and
                            associated Locus code
    """
    try:
        df_map = parse_file(file_path=crosswalk_path,
                            column_of_interest=column_of_interest,
                            output_type='df',
                            granularity=granularity, dr=dr, io=io)
        type_column = BARCODE_FIELDS[column_of_interest.lower()]
        cols = fh.gran_to_fields(granularity, type_column, dr=dr, io=io)
        df_map = df_map[[classification_system] + cols]
        return df_map
    except KeyError:
        print('Make sure you input the right name of column for the classification system.')
        raise
