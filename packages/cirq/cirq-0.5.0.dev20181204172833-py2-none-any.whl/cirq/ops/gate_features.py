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

u"""Marker classes for indicating which additional features gates support.

For example: some gates are reversible, some have known matrices, etc.
"""

from __future__ import absolute_import
from typing import Iterable

import abc

from cirq.ops import op_tree, raw_types


class InterchangeableQubitsGate(object):
    __metaclass__ = abc.ABCMeta
    u"""Indicates operations should be equal under some qubit permutations."""

    def qubit_index_to_equivalence_group_key(self, index):
        u"""Returns a key that differs between non-interchangeable qubits."""
        return 0


class SingleQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly one qubit."""

    def validate_args(self, qubits):
        if len(qubits) != 1:
            raise ValueError(
                u'Single-qubit gate applied to multiple qubits: {}({})'.
                format(self, qubits))

    def on_each(self, targets):
        u"""Returns a list of operations apply this gate to each of the targets.

        Args:
            targets: The qubits to apply this gate to.

        Returns:
            Operations applying this gate to the target qubits.
        """
        return [self.on(target) for target in targets]


class TwoQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly two qubits."""

    def validate_args(self, qubits):
        if len(qubits) != 2:
            raise ValueError(
                u'Two-qubit gate not applied to two qubits: {}({})'.
                format(self, qubits))


class ThreeQubitGate(raw_types.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A gate that must be applied to exactly three qubits."""

    def validate_args(self, qubits):
        if len(qubits) != 3:
            raise ValueError(
                u'Three-qubit gate not applied to three qubits: {}({})'.
                format(self, qubits))
