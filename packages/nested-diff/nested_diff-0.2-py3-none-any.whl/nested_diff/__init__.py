# -*- coding: utf-8 -*-
#
# Copyright 2018 Michael Samoglyadov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Recursive diff for nested structures, implementation of
https://github.com/mr-mixas/Nested-Diff

"""

from __future__ import unicode_literals

from difflib import SequenceMatcher as LCS
from pickle import dumps


__all__ = ['diff', 'patch']

__version__ = '0.2'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff.py'


def diff(a, b, **kwargs):
    """
    Return recursive diff for two passed objects.

    Dicts and lists traversed recursively, all other types compared by values.

    :param a: First object to diff.
    :param b: Second object to diff.
    :param **kwargs: A, N, O, R, U, when set to False will omit such subdiffs;
                     trimR: when set True will trim removed data in diff.

    """
    if a == b:
        if 'U' not in kwargs or kwargs['U']:
            ret = {'U': a}
        else:
            ret = {}

    elif isinstance(a, dict) and isinstance(a, type(b)):
        ret = {'D': {}}

        for k in set(list(a) + list(b)):
            if k in a and k in b:
                if a[k] == b[k]:
                    if 'U' not in kwargs or kwargs['U']:
                        ret['D'][k] = {'U': a[k]}
                else:
                    subdiff = diff(a[k], b[k], **kwargs)
                    if subdiff:
                        ret['D'][k] = subdiff

            elif k in a:  # removed
                if 'R' not in kwargs or kwargs['R']:
                    if 'trimR' in kwargs and kwargs['trimR']:
                        ret['D'][k] = {'R': None}
                    else:
                        ret['D'][k] = {'R': a[k]}

            elif k in b:  # added
                if 'A' not in kwargs or kwargs['A']:
                    ret['D'][k] = {'A': b[k]}

        if not ret['D']:
            del ret['D']

    elif isinstance(a, list) and isinstance(a, type(b)):
        lcs = LCS(None, [dumps(i) for i in a], [dumps(i) for i in b])

        ret = {'D': []}
        i = j = 0
        I = False

        for ai, bj, _ in lcs.get_matching_blocks():
            while i < ai and j < bj:
                subdiff = diff(a[i], b[j], **kwargs)
                if subdiff:
                    ret['D'].append(subdiff)
                    if I:
                        ret['D'][-1]['I'] = i
                        I = False
                else:
                    I = True

                i += 1
                j += 1

            while i < ai:  # removed
                if 'R' not in kwargs or kwargs['R']:
                    if 'trimR' in kwargs and kwargs['trimR']:
                        ret['D'].append({'R': None})
                    else:
                        ret['D'].append({'R': a[i]})

                    if I:
                        ret['D'][-1]['I'] = i
                        I = False
                else:
                    I = True

                i += 1

            while j < bj:  # added
                if 'A' not in kwargs or kwargs['A']:
                    ret['D'].append({'A': b[j]})
                    if I:
                        ret['D'][-1]['I'] = i
                        I = False
                else:
                    I = True

                j += 1

        if not ret['D']:
            del ret['D']

    else:
        ret = {}

        if 'N' not in kwargs or kwargs['N']:
            ret['N'] = b
        if 'O' not in kwargs or kwargs['O']:
            ret['O'] = a

    return ret


def patch(target, diff):
    """
    Return patched object.

    :param target: Object to patch.
    :param diff: Nested diff.

    """

    if 'D' in diff:
        if isinstance(diff['D'], dict):
            for key, subdiff in diff['D'].items():
                if 'D' in subdiff or 'N' in subdiff:
                    target[key] = patch(target[key], subdiff)
                elif 'A' in subdiff:
                    target[key] = subdiff['A']
                elif 'R' in subdiff:
                    del target[key]

        elif isinstance(diff['D'], list):
            i, j = 0, 0  # index, scatter

            for subdiff in diff['D']:
                if 'I' in subdiff:
                    i = subdiff['I'] + j

                if 'D' in subdiff or 'N' in subdiff:
                    target[i] = patch(target[i], subdiff)
                elif 'A' in subdiff:
                    target.insert(i, subdiff['A'])
                    j += 1
                elif 'R' in subdiff:
                    del target[i]
                    j -= 1
                    continue

                i += 1
        else:
            raise NotImplementedError("unsupported type for patch")
    elif 'N' in diff:
        target = diff['N']

    return target
