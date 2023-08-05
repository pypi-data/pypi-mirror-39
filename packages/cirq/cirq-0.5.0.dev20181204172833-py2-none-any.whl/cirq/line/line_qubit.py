# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import functools
from typing import List

from cirq import ops

class LineQubit(ops.QubitId):
    u"""A qubit on a 1d lattice with nearest-neighbor connectivity."""

    def __init__(self, x):
        u"""Initializes a line qubit at the given x coordinate."""
        self.x = x

    def _comparison_key(self):
        return self.x

    def is_adjacent(self, other):
        u"""Determines if two qubits are adjacent line qubits."""
        return isinstance(other, LineQubit) and abs(self.x - other.x) == 1

    @staticmethod
    def range(*range_args):
        u"""Returns a range of line qubits.

        Args:
            *range_args: Same arguments as python's built-in range method.

        Returns:
            A list of line qubits.
        """
        return [LineQubit(i) for i in xrange(*range_args)]

    def __repr__(self):
        return u'cirq.LineQubit({})'.format(self.x)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{}'.format(self.x)

LineQubit = functools.total_ordering(LineQubit)
