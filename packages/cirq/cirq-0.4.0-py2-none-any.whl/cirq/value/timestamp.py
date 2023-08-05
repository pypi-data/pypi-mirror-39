# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
u"""A typed location in time that supports picosecond accuracy."""

from __future__ import absolute_import
from typing import Union, overload

from cirq.value.duration import Duration


class Timestamp(object):
    u"""A location in time with picosecond accuracy.

    Supports affine operations against Duration."""

    def __init__(self, **_3to2kwargs):
        if 'nanos' in _3to2kwargs: nanos = _3to2kwargs['nanos']; del _3to2kwargs['nanos']
        else: nanos =  0
        if 'picos' in _3to2kwargs: picos = _3to2kwargs['picos']; del _3to2kwargs['picos']
        else: picos =  0
        u"""Initializes a Timestamp with a time specified in ns and/or ps.

        The time is relative to some unspecified "time zero". If both picos and
        nanos are specified, their contributions away from zero are added.

        Args:
            picos: How many picoseconds away from time zero?
            nanos: How many nanoseconds away from time zero?
        """

        if picos and nanos:
            self._picos = picos + nanos * 1000
        else:
            # Try to preserve type information.
            self._picos = nanos * 1000 if nanos else picos

    def raw_picos(self):
        u"""The timestamp's location in picoseconds from arbitrary time zero."""
        return self._picos

    def __add__(self, other):
        if not isinstance(other, Duration):
            return NotImplemented
        return Timestamp(picos=self._picos + other.total_picos())

    def __radd__(self, other):
        return self.__add__(other)

    # pylint: disable=function-redefined
    @overload
    def __sub__(self, other):
        pass

    @overload
    def __sub__(self, other):
        pass

    def __sub__(self, other):
        if isinstance(other, Duration):
            return Timestamp(picos=self._picos - other.total_picos())
        if isinstance(other, type(self)):
            return Duration(picos=self._picos - other._picos)
        return NotImplemented
    # pylint: enable=function-redefined

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._picos == other._picos

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._picos > other._picos

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._picos < other._picos

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def __hash__(self):
        return hash((Timestamp, self._picos))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u't={}'.format(self._picos)

    def __repr__(self):
        return u'cirq.Timestamp(picos={})'.format(repr(self._picos))
