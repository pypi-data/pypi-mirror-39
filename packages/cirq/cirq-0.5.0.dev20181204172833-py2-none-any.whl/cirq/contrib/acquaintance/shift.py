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

from __future__ import absolute_import
from itertools import chain
from typing import Sequence, Dict, Tuple

from cirq import protocols
from cirq.ops import Gate, SWAP, OP_TREE, QubitId
from cirq.contrib.acquaintance.permutation import PermutationGate
from itertools import izip


class CircularShiftGate(PermutationGate):
    u"""Performs a cyclical permutation of the qubits to the left by a specified
    amount.

    Args:
        shift: how many positions to circularly left shift the qubits.
        swap_gate: the gate to use when decomposing.
    """

    def __init__(self,
                 shift,
                 swap_gate=SWAP):
        super(CircularShiftGate, self).__init__(swap_gate)
        self.shift = shift

    def __repr__(self):
        return u'CircularShiftGate'

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return ((self.shift == other.shift) and
                (self.swap_gate == other.swap_gate))

    def _decompose_(self, qubits):
        n = len(qubits)
        left_shift = self.shift % n
        right_shift = n - left_shift
        mins = chain(xrange(left_shift - 1, 0, -1),
                     xrange(right_shift))
        maxs = chain(xrange(left_shift, n),
                     xrange(n - 1, right_shift, -1))
        for i, j in izip(mins, maxs):
            for k in xrange(i, j, 2):
                yield self.swap_gate(*qubits[k:k+2])

    def _circuit_diagram_info_(self, args
                               ):
        if args.known_qubit_count is None:
            return NotImplemented
        direction_symbols = (
            (u'╲', u'╱') if args.use_unicode_characters else
            (u'\\', u'/'))
        wire_symbols = tuple(
                direction_symbols[int(i >= self.shift)] +
                unicode(i) +
                direction_symbols[int(i < self.shift)]
                for i in xrange(args.known_qubit_count))
        return wire_symbols

    def permutation(self, qubit_count):
        shift = self.shift % qubit_count
        permuted_indices = chain(xrange(shift, qubit_count),
                                 xrange(shift))
        return dict((s, i) for i, s in enumerate(permuted_indices))
