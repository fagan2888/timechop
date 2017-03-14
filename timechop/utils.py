from datetime import datetime
from dateutil.relativedelta import relativedelta
import functools
import operator
import warnings

def convert_str_to_relativedelta(delta_string):
    """ Given a string in a postgres interval format (e.g., '1 month'),
    convert it to a dateutil.relativedelta.relativedelta.

    Assumptions:
    - the prediction_window string is in the format 'value unit', where
      value is an int and unit is one of year(s), month(s), day(s),
      week(s), hour(s), minute(s), second(s), microsecond(s).

    :param delta_string: the time interval to convert
    :type delta_string: str

    :return: the time interval as a relativedelta
    :rtype: dateutil.relativedelta.relativedelta

    :raises: ValueError if the delta_string is not in the expected format
    """
    units, value = parse_delta_string(delta_string)

    if units in ['year', 'years', 'y', 'Y']:
        delta = relativedelta(years = value)
    elif units in ['month', 'months', 'm', 'M']:
        delta = relativedelta(months = value)
        if units in ['m', 'M']:
            warnings.warn(
                'Time delta units "{}" converted to months.'.format(units),
                RuntimeWarning
            )
    elif units in ['day', 'days', 'd', 'D']:
        delta = relativedelta(days = value)
    elif units in ['week', 'weeks', 'w', 'W']:
        delta = relativedelta(weeks = value)
    elif units in ['hour', 'hours', 'h', 'H']:
        delta = relativedelta(hours = value)
    elif units in ['minute', 'minutes']:
        delta = relativedelta(minutes = value)
    elif units in ['second', 'seconds', 's', 'S']:
        delta = relativedelta(seconds = value)
    elif units == 'microsecond' or units == 'microseconds':
        delta = relativedelta(microseconds = value)
    else:
        raise ValueError(
            'Could not handle units. Units: {} Value: {}'.format(units, value)
        )

    return(delta)

def parse_delta_string(delta_string):
    if len(delta_string.split(' ')) == 2:
        try:
            units = delta_string.split(' ')[1]
        except:
            raise ValueError('''
                Could not parse units from time delta string: {}
            '''.format(delta_string))
        try:
            value = int(delta_string.split(' ')[0])
        except:
            raise ValueError('''
                Could not parse value from time delta string: {}
            '''.format(delta_string))
    elif len(delta_string) == 2:
        try:
            units = delta_string[1]
        except:
            raise ValueError('''
                Could not parse units from time delta string: {}
            '''.format(delta_string))
        try:
            value = int(delta_string[0])
        except:
            raise ValueError('''
                Could not parse value from time delta string: {}
            '''.format(delta_string))
    else:
        raise ValueError(
            'Could not parse time delta string: {}'.format(delta_string)
        )

    return(units, value)


def feature_list(feature_dictionary):
    """Convert a feature dictionary to a sorted list.

    Args: feature_dictionary (dict)

    Returns: sorted list of feature names
    """
    return sorted(functools.reduce(
        operator.concat,
        [feature_dictionary[key] for key in feature_dictionary.keys()]
    ))
