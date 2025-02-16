import pytest

import app.database.crud as functions

'''
def get_interval_int(interval_code):
    match interval_code:
        case 'd':
            return_value = 1
        case 'w':
            return_value = 7
        case 'm':
            return_value = 30
        case '3m':
            return_value = 90
        case '6m':
            return_value = 180
    return return_value
'''


def test_get_interval_int():
    assert functions.get_interval_int('d') == 1
    assert functions.get_interval_int('w') == 7
    assert functions.get_interval_int('m') == 30
    assert functions.get_interval_int('3m') == 90
    assert functions.get_interval_int('6m') == 180
