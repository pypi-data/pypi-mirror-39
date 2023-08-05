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

from __future__ import with_statement
from __future__ import absolute_import
from typing import Sequence, Union

import pytest

import numpy as np

import cirq
from cirq.type_workarounds import NotImplementedType


class GoodGate(cirq.SingleQubitGate):

    def __init__(self, **_3to2kwargs):
        if 'exponent' in _3to2kwargs: exponent = _3to2kwargs['exponent']; del _3to2kwargs['exponent']
        else: exponent =  1.0
        phase_exponent = _3to2kwargs['phase_exponent']; del _3to2kwargs['phase_exponent']
        self.phase_exponent = cirq.canonicalize_half_turns(phase_exponent)
        self.exponent = exponent

    def _unitary_(self):
        if cirq.is_parameterized(self):
            return NotImplemented
        z = cirq.unitary(cirq.ops.common_gates.Z**self.phase_exponent)
        x = cirq.unitary(cirq.ops.common_gates.X**self.exponent)
        return np.dot(np.dot(z, x), np.conj(z))

    def _apply_unitary_(self, args
                        ):
        if self.exponent != 1 or cirq.is_parameterized(self):
            return NotImplemented

        zero = cirq.slice_for_qubits_equal_to(args.axes, 0)
        one = cirq.slice_for_qubits_equal_to(args.axes, 1)
        c = np.exp(1j * np.pi * self.phase_exponent)

        args.target_tensor[one] *= c.conj()
        args.available_buffer[zero] = args.target_tensor[one]
        args.available_buffer[one] = args.target_tensor[zero]
        args.available_buffer[one] *= c

        return args.available_buffer

    def _decompose_(self, qubits):
        assert len(qubits) == 1
        q = qubits[0]
        z = cirq.ops.common_gates.Z(q)**self.phase_exponent
        x = cirq.ops.common_gates.X(q)**self.exponent
        if cirq.is_parameterized(z):
            # coverage: ignore
            return NotImplemented
        return z**-1, x, z

    def _phase_by_(self, phase_turns, qubit_index):
        assert qubit_index == 0
        return GoodGate(
            exponent=self.exponent,
            phase_exponent=self.phase_exponent + phase_turns * 2)

    def __pow__(self, exponent):
        new_exponent = cirq.mul(self.exponent, exponent, NotImplemented)
        if new_exponent is NotImplemented:
            # coverage: ignore
            return NotImplemented
        return GoodGate(phase_exponent=self.phase_exponent,
                        exponent=new_exponent)

    def __repr__(self):
        args = [u'phase_exponent={!r}'.format(self.phase_exponent)]
        if self.exponent != 1:
            args.append(u'exponent={!r}'.format(self.exponent))
        return u'cirq.testing.consistent_protocols_test.GoodGate({})'.format(
                u', '.join(args))

    def _is_parameterized_(self):
        return (isinstance(self.exponent, cirq.Symbol) or
                isinstance(self.phase_exponent, cirq.Symbol))

    def _identity_tuple(self):
        return (GoodGate,
                self.phase_exponent,
                self.exponent)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            # coverage: ignore
            return NotImplemented
        return self._identity_tuple() == other._identity_tuple()


class BadGateApplyUnitaryToTensor(GoodGate):

    def _apply_unitary_(self, args
                        ):
        if self.exponent != 1 or cirq.is_parameterized(self):
            # coverage: ignore
            return NotImplemented

        zero = cirq.slice_for_qubits_equal_to(args.axes, 0)
        one = cirq.slice_for_qubits_equal_to(args.axes, 1)
        c = np.exp(1j * np.pi * self.phase_exponent)

        args.target_tensor[one] *= c
        args.available_buffer[zero] = args.target_tensor[one]
        args.available_buffer[one] = args.target_tensor[zero]
        args.available_buffer[one] *= c

        return args.available_buffer


class BadGateDecompose(GoodGate):

    def _decompose_(self, qubits):
        assert len(qubits) == 1
        q = qubits[0]
        z = cirq.ops.common_gates.Z(q)**self.phase_exponent
        x = cirq.ops.common_gates.X(q)**(2*self.exponent)
        if cirq.is_parameterized(z):
            # coverage: ignore
            return NotImplemented
        return z**-1, x, z


class BadGatePhaseBy(GoodGate):

    def _phase_by_(self, phase_turns, qubit_index):
        assert qubit_index == 0
        return BadGatePhaseBy(
            exponent=self.exponent,
            phase_exponent=self.phase_exponent + phase_turns * 4)


class BadGateRepr(GoodGate):

    def __repr__(self):
        args = [u'phase_exponent={!r}'.format(2*self.phase_exponent)]
        if self.exponent != 1:
            # coverage: ignore
            args.append(u'exponent={!r}'.format(self.exponent))
        return u'cirq.testing.consistent_protocols_test.BadGateRepr({})'.format(
                u', '.join(args))


class GoodEigenGate(cirq.EigenGate, cirq.SingleQubitGate):

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0])),
            (1, np.diag([0, 1])),
        ]

    def __repr__(self):
        return (u'cirq.testing.consistent_protocols_test.GoodEigenGate'
                u'(exponent={!r}, global_shift={!r})'.format(
                    self._exponent, self._global_shift))


class BadEigenGate(GoodEigenGate):

    def _eigen_shifts(self):
        return [0, 0]

    def __repr__(self):
        return (u'cirq.testing.consistent_protocols_test.BadEigenGate'
                u'(exponent={!r}, global_shift={!r})'.format(
                    self._exponent, self._global_shift))


def test_assert_implements_consistent_protocols():
    cirq.testing.assert_implements_consistent_protocols(
            GoodGate(phase_exponent=0.0)
    )

    cirq.testing.assert_implements_consistent_protocols(
            GoodGate(phase_exponent=0.25)
    )

    with pytest.raises(AssertionError):
        cirq.testing.assert_implements_consistent_protocols(
                BadGateApplyUnitaryToTensor(phase_exponent=0.25)
        )

    with pytest.raises(AssertionError):
        cirq.testing.assert_implements_consistent_protocols(
                BadGateDecompose(phase_exponent=0.25)
        )

    with pytest.raises(AssertionError):
        cirq.testing.assert_implements_consistent_protocols(
                BadGatePhaseBy(phase_exponent=0.25)
        )

    with pytest.raises(AssertionError):
        cirq.testing.assert_implements_consistent_protocols(
                BadGateRepr(phase_exponent=0.25)
        )


def test_assert_eigengate_implements_consistent_protocols():
    cirq.testing.assert_eigengate_implements_consistent_protocols(
            GoodEigenGate)

    with pytest.raises(AssertionError):
        cirq.testing.assert_eigengate_implements_consistent_protocols(
                BadEigenGate)
