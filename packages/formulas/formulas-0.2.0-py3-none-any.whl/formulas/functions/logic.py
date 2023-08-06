#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2018 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
Python equivalents of logical Excel functions.
"""
from . import wrap_ufunc, Error, flatten, get_error, value_return

FUNCTIONS = {}


def xif(condition, x=True, y=False):
    if isinstance(condition, str):
        return Error.errors['#VALUE!']
    return x if condition else y


def solve_cycle(*args):
    return not args[0]


FUNCTIONS['IF'] = {
    'function': wrap_ufunc(
        xif, input_parser=lambda *a: a, return_func=value_return,
        check_error=lambda cond, *a: get_error(cond)
    ),
    'solve_cycle': solve_cycle
}


def xiferror(val, val_if_error):
    from .info import iserror
    return val_if_error if iserror(val) else val


# noinspection PyUnusedLocal
def xiferror_return(res, val, val_if_error):
    res._collapse_value = list(flatten(val_if_error, None))[0]
    return res


FUNCTIONS['IFERROR'] = {
    'function': wrap_ufunc(
        xiferror, input_parser=lambda *a: a, check_error=lambda *a: False,
        return_func=xiferror_return
    ),
    'solve_cycle': solve_cycle
}
