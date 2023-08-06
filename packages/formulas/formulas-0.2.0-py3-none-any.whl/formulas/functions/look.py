# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2018 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
Python equivalents of lookup and reference Excel functions.
"""
import regex
import functools
import collections
import numpy as np
from . import (
    wrap_func, wrap_ufunc, Error, flatten, get_error, XlError, FoundError, Array
)
from ..cell import CELL

FUNCTIONS = {}


def _get_type_id(obj):
    if isinstance(obj, bool):
        return 2
    elif isinstance(obj, str) and not isinstance(obj, XlError):
        return 1
    return 0


def _yield_vals(type_id, array):
    for i, v in enumerate(array, 1):
        if type_id == _get_type_id(v):
            yield i, v


def _xref(func, cell=None, ref=None):
    try:
        return func((ref or cell).ranges[0]).view(Array)
    except IndexError:
        return Error.errors['#NULL!']


def xrow(cell=None, ref=None):
    return _xref(
        lambda r: np.arange(int(r['r1']), int(r['r2']) + 1)[:, None], cell, ref
    )


def xcolumn(cell=None, ref=None):
    return _xref(lambda r: np.arange(r['n1'], r['n2'] + 1)[None, :], cell, ref)


FUNCTIONS['COLUMN'] = {
    'extra_inputs': collections.OrderedDict([(CELL, None)]),
    'function': wrap_func(xcolumn, ranges=True)
}
FUNCTIONS['ROW'] = {
    'extra_inputs': collections.OrderedDict([(CELL, None)]),
    'function': wrap_func(xrow, ranges=True)
}


def xmatch(lookup_value, lookup_array, match_type=1):
    res = [Error.errors['#N/A']]
    t_id = _get_type_id(lookup_value)
    if match_type > 0:
        def check(j, x, val, r):
            if x <= val:
                r[0] = j
                return x == val and j > 1
            return j > 1

    elif match_type < 0:
        def check(j, x, val, r):
            if x < val:
                return True
            r[0] = j
            return v == val

    else:
        t_id = _get_type_id(lookup_value)
        if t_id == 1:
            def sub(m):
                return {'\\': '', '?': '.', '*': '.*'}[m.groups()[0]]

            match = regex.compile(r'^%s$' % regex.sub(
                r'(?<!\\\~)\\(?P<sub>[\*\?])|(?P<sub>\\)\~(?=\\[\*\?])', sub,
                regex.escape(lookup_value)
            ), regex.IGNORECASE).match
        else:
            match = lambda x: x == lookup_value

        # noinspection PyUnusedLocal
        def check(j, x, val, r):
            if match(x):
                r[0] = j

    convert = lambda x: x
    if t_id == 1:
        convert = lambda x: x.upper()

    lookup_value = convert(lookup_value)
    for i, v in _yield_vals(t_id, lookup_array):
        if check(i, convert(v), lookup_value, res):
            break
    return res[0]


FUNCTIONS['MATCH'] = wrap_ufunc(
    xmatch,
    input_parser=lambda val, vec, match_type=1: (
        val, list(flatten(vec, None)), match_type
    ),
    check_error=lambda *a: get_error(a[:1]), excluded={1, 2}
)


def xlookup(lookup_val, lookup_vec, result_vec=None, match_type=1):
    result_vec = lookup_vec if result_vec is None else result_vec
    r = xmatch(lookup_val, lookup_vec, match_type)
    if not isinstance(r, XlError):
        r = result_vec[r - 1]
    return r


FUNCTIONS['LOOKUP'] = wrap_ufunc(
    xlookup,
    input_parser=lambda val, vec, res=None: (
        val, list(flatten(vec, None)),
        res if res is None else list(flatten(res, None))
    ),
    check_error=lambda *a: get_error(a[:1]), excluded={1, 2}
)


def _hlookup_parser(val, vec, index, match_type=1, transpose=False):
    index = list(flatten(index, None))[0] - 1
    vec = np.matrix(vec)
    if transpose:
        vec = vec.T
    try:
        ref = list(flatten(vec[index].A1, None))
    except IndexError:
        raise FoundError(err=Error.errors['#REF!'])
    vec = list(flatten(vec[0].A1, None))
    return val, vec, ref, bool(match_type)


FUNCTIONS['HLOOKUP'] = wrap_ufunc(
    xlookup, input_parser=_hlookup_parser,
    check_error=lambda *a: get_error(a[:1]), excluded={1, 2, 3}
)
FUNCTIONS['VLOOKUP'] = wrap_ufunc(
    xlookup, input_parser=functools.partial(_hlookup_parser, transpose=True),
    check_error=lambda *a: get_error(a[:1]), excluded={1, 2, 3}
)
