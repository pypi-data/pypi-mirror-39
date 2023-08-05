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

u"""Basic types defining qubits, gates, and operations."""

from __future__ import absolute_import
from typing import (
    Optional, Sequence, FrozenSet, Tuple, Union, TYPE_CHECKING,
    Any)

import numpy as np

from cirq import protocols, value
from cirq.ops import raw_types, gate_features
from cirq.type_workarounds import NotImplementedType

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Dict, List


class GateOperation(raw_types.Operation):
    u"""An application of a gate to a sequence of qubits."""

    def __init__(self,
                 gate,
                 qubits):
        u"""
        Args:
            gate: The gate to apply.
            qubits: The qubits to operate on.
        """
        self._gate = gate
        self._qubits = tuple(qubits)

    @property
    def gate(self):
        u"""The gate applied by the operation."""
        return self._gate

    @property
    def qubits(self):
        u"""The qubits targeted by the operation."""
        return self._qubits

    def with_qubits(self, *new_qubits):
        return self.gate.on(*new_qubits)

    def with_gate(self, new_gate):
        return new_gate.on(*self.qubits)

    def __repr__(self):
        # Abbreviate when possible.
        if self == self.gate.on(*self.qubits):
            return u'{!r}.on({})'.format(
                self.gate,
                u', '.join(repr(q) for q in self.qubits))

        return u'cirq.GateOperation(gate={!r}, qubits={!r})'.format(
            self.gate,
            list(self.qubits))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{}({})'.format(self.gate,
                               u', '.join(unicode(e) for e in self.qubits))

    def _group_interchangeable_qubits(self):

        if not isinstance(self.gate, gate_features.InterchangeableQubitsGate):
            return self.qubits

        groups = {}  # type: Dict[int, List[raw_types.QubitId]]
        for i, q in enumerate(self.qubits):
            k = self.gate.qubit_index_to_equivalence_group_key(i)
            if k not in groups:
                groups[k] = []
            groups[k].append(q)
        return tuple(sorted((k, frozenset(v)) for k, v in groups.items()))

    def _value_equality_values_(self):
        return self.gate, self._group_interchangeable_qubits()

    def _decompose_(self):
        return protocols.decompose_once_with_qubits(self.gate,
                                                    self.qubits,
                                                    NotImplemented)

    def _apply_unitary_(self, args
                        ):
        return protocols.apply_unitary(
            self.gate,
            args,
            default=NotImplemented)

    def _has_unitary_(self):
        return protocols.has_unitary(self._gate)

    def _unitary_(self):
        return protocols.unitary(self._gate, NotImplemented)

    def _is_parameterized_(self):
        return protocols.is_parameterized(self._gate)

    def _resolve_parameters_(self, resolver):
        resolved_gate = protocols.resolve_parameters(self._gate, resolver)
        return GateOperation(resolved_gate, self._qubits)

    def _circuit_diagram_info_(self,
                               args
                               ):
        return protocols.circuit_diagram_info(self.gate,
                                              args,
                                              NotImplemented)

    def _trace_distance_bound_(self):
        return protocols.trace_distance_bound(self.gate)

    def _phase_by_(self, phase_turns,
                   qubit_index):
        phased_gate = protocols.phase_by(self._gate, phase_turns, qubit_index,
                                         default=None)
        if phased_gate is None:
            return NotImplemented
        return GateOperation(phased_gate, self._qubits)

    def __pow__(self, exponent):
        u"""Raise gate to a power, then reapply to the same qubits.

        Only works if the gate implements cirq.ExtrapolatableEffect.
        For extrapolatable gate G this means the following two are equivalent:

            (G ** 1.5)(qubit)  or  G(qubit) ** 1.5

        Args:
            exponent: The amount to scale the gate's effect by.

        Returns:
            A new operation on the same qubits with the scaled gate.
        """
        new_gate = protocols.pow(self.gate,
                                 exponent,
                                 NotImplemented)
        if new_gate is NotImplemented:
            return NotImplemented
        return self.with_gate(new_gate)

    def _qasm_(self, args):
        return protocols.qasm(self.gate,
                              args=args,
                              qubits=self.qubits,
                              default=None)

GateOperation = value.value_equality(GateOperation)
