""" Helper python functions. """

__author__ = "lego_engineer"
__maintainer__ = "lego_engineer"
__email__ = "protopeters@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2018, lego_engineer"

import string
import random
import pathlib
from csv import reader as csv_reader

def id_generator(length=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Generate random alpha-numeric sequences.

    Taken from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python

    :param int length: The length of sequence to generate.
    :param str chars: The characters to include in the sequence.
    """
    return ''.join(random.choice(chars) for _ in range(length))

def flatten(lst):
    """ Recursively flatten a list.

    Taken from https://stackoverflow.com/questions/12472338/flattening-a-list-recursively

    :param list lst: The list to flatten.
    """
    if not lst:
        return list(lst)
    if isinstance(lst[0], (list, set, tuple)):
        return list(flatten(lst[0])) + list(flatten(lst[1:]))
    return list(lst[:1]) + list(flatten(lst[1:]))

def validated_question(question, possible_answers, case_sensitive=False, invalid=False):
    """ A method for validating user input.

    :param str question: The queston you want to ask. (e.g. 'What is your name?')
    :param list-like possible_answers: The possible answers to the question. (e.g. 'Mary')
    :param bool case_sensitive: Check for case sensitivity in when selecting a preset.
    :param bool invalid: Has the user given a invalid response previously?
    """
    if invalid:
        print('Sorry, that input is invalid. Please try again. Valid Responses include:')
        print(str(possible_answers))
    response = input(question)

    if case_sensitive:
        if response not in possible_answers:
            return validated_question(question, possible_answers, case_sensitive, invalid=True)
    else:
        if response.upper() not in map(str.upper, possible_answers):
            return validated_question(question, possible_answers, case_sensitive, invalid=True)
    return response


def ask_yes_no(question):
    """ Ask a yes or no question.

    :param str question: The queston you want to ask. (e.g. 'Do you have a name?')

    >>> ask_yes_no('Do you like ice cream?')
    >>> y
    True
    """
    valid_answers = ['YES', 'yes', 'Yes', 'y', 'Y', 'NO', 'no', 'No', 'n', 'N']
    response = validated_question(question + ' [y/n]: ', valid_answers)
    return response[0].lower() == 'y'

def ask_path(question, validate_file_exists=True, invalid=False):
    """ A method for validating user path input.

    :param str question: The queston you want to ask. (e.g. 'What is your file?')
    :param bool validate_file_exists: Should we validate the file exists?
    :param bool invalid: Had the user given an invalid response previously?
    """
    if invalid:
        print('Sorry, that path is invalid/no file exists.'
              'Please try again (be careful with whitespaces).')
    path = pathlib.Path(input(question + ': '))

    if validate_file_exists:
        if not path.is_file():
            path = ask_path(question, validate_file_exists, invalid=True)

    return path

def choose_preset(presets, invalid=False):
    """ Choose a value from a set of presets.

    :param list-like presets: A list of presets from which to choose.
    :param bool case_sensitive: Check for case sensitivity in when selecting a preset.
    :param bool invalid: Has the user given a invalid response previously?
    """
    presets_list = list(presets)

    if invalid:
        print('Sorry, that input is invalid. Please try again.')

    selection = input('Please select a preset by number/index.\n' \
                      'Valid Responses include: {}\n'.format(list(enumerate(presets_list))))

    try:
        selection = int(selection)
    except ValueError:
        selection = choose_preset(presets, invalid=True)

    if selection not in range(len(presets_list)):
        selection = choose_preset(presets, invalid=True)

    if invalid:
        return int(selection)

    return presets_list[selection]

def input_int(message, invalid=False):
    """ Get an integer input.

    :param str message: The question string.
    :param bool invalid: Has the user given a invalid response previously?
    """
    if invalid:
        print('Sorry, that input is not castable to an integer. Please try again.')

    try:
        return int(input(message + ': '))
    except ValueError:
        return input_int(message, invalid=True)

def csv_filter(input_str, valid_delimiter=None):
    """ Convert a string to a csv string.

    :param str input_str: The string to convert.
    """

    if valid_delimiter is None:
        valid_delimiter = [" ", ","]

    for delimiter in valid_delimiter:
        input_str = input_str.replace(delimiter, ",")
    return ",".join(filter(len, input_str.split(",")))

def input_csv(message):
    """ Get a csv input (string type).

    :param str message: The question string.
    :param list of str valid_delimiter: The valid delimiters. Defaults to space and comma.
    :param bool invalid: Has the user given a invalid response previously?
    """

    return csv_filter(input(message + ': '))

def fileio_csv(path_request):
    """ Get a csv input file.

    :param path path_request: The string to display when requesting a path.
    :param bool invalid: Has the user given a invalid response previously?
    """
    csv_path = ask_path(path_request)
    with csv_path.open('r') as file_obj:
        csv_as_list = list(csv_reader(file_obj))
    return str(",".join(str(elem) for elem in flatten(csv_as_list)))

def input_str_not_empty(message, invalid=False):
    """ Something. """
    if invalid:
        print('Sorry, that input is not valid. Perhaps its empty or only contains whitespaces?')

    response = input(message + ': ')

    if not response.replace(' ', ''):
        # An empty string
        return input_str_not_empty(message, invalid=True)
    return response
