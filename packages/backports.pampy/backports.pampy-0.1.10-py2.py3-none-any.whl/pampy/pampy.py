# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import itertools
from collections import Iterable
from typing import Tuple, List
from typing import Pattern as RegexPattern
import inspect
import six
if hasattr(itertools, 'zip_longest'):
    zip_longest = itertools.zip_longest
else:
    zip_longest = itertools.izip_longest


class UnderscoreType(object):

    def __repr__(self):
        return '_'


class HeadType(object):

    def __repr__(self):
        return 'HEAD'


class TailType(object):

    def __repr__(self):
        return 'TAIL'


class PaddedValueType(object):

    def __repr__(self):
        return 'PaddedValue'


PaddedValue = PaddedValueType()


class BoxedArgs(object):

    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj


def pairwise(l):
    i = 0
    while i < len(l):
        yield l[i], l[i + 1]
        i += 2


def get_lambda_args_error_msg(action, var, err):
    try:
        code = inspect.getsource(action)
        return 'Error passing arguments %s here:\n%s\n%s' % (var, code, err)
    except OSError:
        return 'Error passing arguments %s:\n%s' % (var, err)


def is_dataclass(value):
    """
    Dataclass support is only enabled in Python 3.7+, or in 3.6 with the `dataclasses` backport installed
    """
    try:
        from dataclasses import is_dataclass
        return is_dataclass(value)
    except ImportError:
        return False


ValueType = int, float, six.text_type, bool
_ = ANY = UnderscoreType()
HEAD = HeadType()
REST = TAIL = TailType()


def run(action, var):
    if callable(action):
        if isinstance(var, Iterable):
            try:
                return action(*var)
            except TypeError as err:
                raise MatchError(get_lambda_args_error_msg(action, var, err))
        elif isinstance(var, BoxedArgs):
            return action(var.get())
        else:
            return action(var)
    else:
        return action


def match_value(pattern, value):
    if value is PaddedValue:
        return False, []
    elif isinstance(pattern, ValueType):
        eq = pattern == value
        type_eq = type(pattern) == type(value)
        return eq and type_eq, []
    elif pattern is None:
        return value is None, []
    elif isinstance(pattern, type):
        if isinstance(value, pattern):
            return True, [value]
        else:
            return False, []
    elif isinstance(pattern, list):
        return match_iterable(pattern, value)
    elif isinstance(pattern, tuple):
        return match_iterable(pattern, value)
    elif isinstance(pattern, dict):
        return match_dict(pattern, value)
    elif callable(pattern):
        return_value = pattern(value)
        if return_value is True:
            return True, [value]
        elif return_value is False:
            pass
        else:
            raise MatchError(
                'Warning! pattern function %s is not returning a boolean, but instead %s'
                 % (pattern, return_value))
    elif isinstance(pattern, RegexPattern):
        rematch = pattern.search(value)
        if rematch is not None:
            return True, list(rematch.groups())
    elif pattern is _:
        return True, [value]
    elif pattern is HEAD or pattern is TAIL:
        raise MatchError(
            'HEAD or TAIL should only be used inside an Iterable (list or tuple).'
            )
    elif is_dataclass(pattern):
        return match_dict(pattern.__dict__, value.__dict__)
    return False, []


def match_dict(pattern, value):
    if not isinstance(value, dict) or not isinstance(pattern, dict):
        return False, []
    total_extracted = []
    still_usable_value_keys = set(value.keys())
    still_usable_pattern_keys = set(pattern.keys())
    for pkey, pval in pattern.items():
        if pkey not in still_usable_pattern_keys:
            continue
        matched_left_and_right = False
        for vkey, vval in value.items():
            if vkey not in still_usable_value_keys:
                continue
            if pkey not in still_usable_pattern_keys:
                continue
            key_matched, key_extracted = match_value(pkey, vkey)
            if key_matched:
                value_matched, value_extracted = match_value(pval, vval)
                if value_matched:
                    total_extracted += key_extracted + value_extracted
                    matched_left_and_right = True
                    still_usable_pattern_keys.remove(pkey)
                    still_usable_value_keys.remove(vkey)
                    break
        if not matched_left_and_right:
            return False, []
    return True, total_extracted


def only_padded_values_follow(padded_pairs, i):
    i += 1
    while i < len(padded_pairs):
        pattern, value = padded_pairs[i]
        if pattern is not PaddedValue:
            return False
        i += 1
    return True


def match_iterable(patterns, values):
    if not isinstance(patterns, Iterable) or not isinstance(values, Iterable):
        return False, []
    total_extracted = []
    padded_pairs = list(zip_longest(patterns, values, fillvalue=PaddedValue))
    for i, (pattern, value) in enumerate(padded_pairs):
        if pattern is HEAD:
            if i != 0:
                raise MatchError(
                    'HEAD can only be in first position of a pattern.')
            elif value is PaddedValue:
                return False, []
            else:
                total_extracted += [value]
        elif pattern is TAIL:
            if not only_padded_values_follow(padded_pairs, i):
                raise MatchError(
                    'TAIL must me in last position of the pattern.')
            else:
                tail = [value for pattern, value in padded_pairs[i:] if 
                    value is not PaddedValue]
                total_extracted.append(tail)
                break
        else:
            matched, extracted = match_value(pattern, value)
            if not matched:
                return False, []
            else:
                total_extracted += extracted
    return True, total_extracted


def match(var, *args, **kwargs):
    strict = kwargs.get('strict', True)
    if len(args) % 2 != 0:
        raise MatchError('Every guard must have an action.')
    pairs = list(pairwise(args))
    patterns = [patt for patt, action in pairs]
    for patt, action in pairs:
        matched_as_value, args = match_value(patt, var)
        if matched_as_value:
            lambda_args = args if len(args) > 0 else BoxedArgs(var)
            return run(action, lambda_args)
    if strict:
        if _ not in patterns:
            raise MatchError(
                "'_' not provided. This case is not handled:\n%s" % six.
                text_type(var))
    else:
        return False


class MatchError(Exception):

    def __init__(self, msg):
        super(MatchError, self).__init__(msg)
