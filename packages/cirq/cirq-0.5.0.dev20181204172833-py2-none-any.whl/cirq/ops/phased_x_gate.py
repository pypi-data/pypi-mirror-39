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

u"""An `XPowGate` conjugated by `ZPowGate`s."""
from __future__ import division
from __future__ import absolute_import
import fractions
from typing import Union, Sequence, Tuple, Optional, cast

import numpy as np

from cirq import value, protocols
from cirq.ops import gate_features, raw_types, op_tree
from cirq.type_workarounds import NotImplementedType

# Note: avoiding 'from/as' because it creates a circular dependency in python 2.
import cirq.ops.common_gates
from itertools import izip


class PhasedXPowGate(gate_features.SingleQubitGate):
    u"""A gate equivalent to the circuit ───Z^-p───X^t───Z^p───."""

    def __new__(cls, **_3to2kwargs):
        if 'global_shift' in _3to2kwargs: global_shift = _3to2kwargs['global_shift']; del _3to2kwargs['global_shift']
        else: global_shift =  0.0
        if 'exponent' in _3to2kwargs: exponent = _3to2kwargs['exponent']; del _3to2kwargs['exponent']
        else: exponent =  1.0
        phase_exponent = _3to2kwargs['phase_exponent']; del _3to2kwargs['phase_exponent']
        u"""Substitutes a raw X or raw Y if possible.

        Args:
            phase_exponent: The exponent on the Z gates conjugating the X gate.
            exponent: The exponent on the X gate conjugated by Zs.
            global_shift: How much to shift the operation's eigenvalues at
                exponent=1.
        """
        p = value.canonicalize_half_turns(phase_exponent)
        if p == 0:
            return cirq.ops.common_gates.XPowGate(
                exponent=exponent,
                global_shift=global_shift)
        if p == 0.5:
            return cirq.ops.common_gates.YPowGate(
                exponent=exponent,
                global_shift=global_shift)
        if p == 1 and not isinstance(exponent, value.Symbol):
            return cirq.ops.common_gates.XPowGate(
                exponent=-exponent,
                global_shift=global_shift)
        if p == -0.5 and not isinstance(exponent, value.Symbol):
            return cirq.ops.common_gates.YPowGate(
                exponent=-exponent,
                global_shift=global_shift)
        return super(PhasedXPowGate, cls).__new__(cls)

    def __init__(self, **_3to2kwargs):
        if 'global_shift' in _3to2kwargs: global_shift = _3to2kwargs['global_shift']; del _3to2kwargs['global_shift']
        else: global_shift =  0.0
        if 'exponent' in _3to2kwargs: exponent = _3to2kwargs['exponent']; del _3to2kwargs['exponent']
        else: exponent =  1.0
        phase_exponent = _3to2kwargs['phase_exponent']; del _3to2kwargs['phase_exponent']
        u"""
        Args:
            phase_exponent: The exponent on the Z gates conjugating the X gate.
            exponent: The exponent on the X gate conjugated by Zs.
            global_shift: How much to shift the operation's eigenvalues at
                exponent=1.
        """
        self._phase_exponent = value.canonicalize_half_turns(phase_exponent)
        self._exponent = exponent
        self._global_shift = global_shift

    def _qasm_(self,
               args,
               qubits):
        if cirq.is_parameterized(self):
            return None

        args.validate_version(u'2.0')

        e = cast(float, value.canonicalize_half_turns(self._exponent))
        p = cast(float, self.phase_exponent)
        epsilon = 10**-args.precision

        if abs(e + 0.5) <= epsilon:
            return args.format(u'u2({0:half_turns}, {1:half_turns}) {2};\n',
                               p + 0.5, -p - 0.5, qubits[0])

        if abs(e - 0.5) <= epsilon:
            return args.format(u'u2({0:half_turns}, {1:half_turns}) {2};\n',
                               p - 0.5, -p + 0.5, qubits[0])

        return args.format(
            u'u3({0:half_turns}, {1:half_turns}, {2:half_turns}) {3};\n',
            -e, p + 0.5, -p - 0.5, qubits[0])

    def _decompose_(self, qubits
                          ):
        assert len(qubits) == 1
        q = qubits[0]
        z = cirq.ops.common_gates.Z(q)**self._phase_exponent
        x = cirq.ops.common_gates.X(q)**self._exponent
        if protocols.is_parameterized(z):
            return NotImplemented
        return z**-1, x, z

    @property
    def exponent(self):
        u"""The exponent on the central X gate conjugated by the Z gates."""
        return self._exponent

    @property
    def phase_exponent(self):
        u"""The exponent on the Z gates conjugating the X gate."""
        return self._phase_exponent

    def __pow__(self, exponent):
        new_exponent = protocols.mul(self._exponent, exponent, NotImplemented)
        if new_exponent is NotImplemented:
            return NotImplemented
        return PhasedXPowGate(phase_exponent=self._phase_exponent,
                              exponent=new_exponent,
                              global_shift=self._global_shift)

    def _trace_distance_bound_(self):
        u"""See `cirq.SupportsTraceDistanceBound`."""
        return protocols.trace_distance_bound(
            cirq.ops.common_gates.X**self._exponent)

    def _unitary_(self):
        u"""See `cirq.SupportsUnitary`."""
        if self._is_parameterized_():
            return NotImplemented
        z = protocols.unitary(cirq.ops.common_gates.Z**self._phase_exponent)
        x = protocols.unitary(cirq.ops.common_gates.X**self._exponent)
        p = np.exp(1j * np.pi * self._global_shift * self._exponent)
        return np.dot(np.dot(z, x), np.conj(z)) * p

    def _is_parameterized_(self):
        u"""See `cirq.SupportsParameterization`."""
        return (isinstance(self._exponent, value.Symbol) or
                isinstance(self._phase_exponent, value.Symbol))

    def _resolve_parameters_(self, param_resolver):
        u"""See `cirq.SupportsParameterization`."""
        return PhasedXPowGate(
            phase_exponent=param_resolver.value_of(self._phase_exponent),
            exponent=param_resolver.value_of(self._exponent),
            global_shift=self._global_shift)

    def _phase_by_(self, phase_turns, qubit_index):
        u"""See `cirq.SupportsPhase`."""
        assert qubit_index == 0
        return PhasedXPowGate(
            exponent=self._exponent,
            phase_exponent=self._phase_exponent + phase_turns * 2,
            global_shift=self._global_shift)

    def _circuit_diagram_info_(self, args
                               ):
        u"""See `cirq.SupportsCircuitDiagramInfo`."""

        if (isinstance(self.phase_exponent, value.Symbol) or
                args.precision is None):
            s = u'PhasedX({})'.format(self.phase_exponent)
        else:
            s = u'PhasedX({{:.{}}})'.format(args.precision).format(
                self.phase_exponent)
        return protocols.CircuitDiagramInfo(
            wire_symbols=(s,),
            exponent=value.canonicalize_half_turns(self._exponent))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        info = protocols.circuit_diagram_info(self)
        if info.exponent == 1:
            return info.wire_symbols[0]
        return u'{}^{}'.format(info.wire_symbols[0], info.exponent)

    def __repr__(self):
        args = [u'phase_exponent={!r}'.format(self.phase_exponent)]
        if self.exponent != 1:
            args.append(u'exponent={!r}'.format(self.exponent))
        if self._global_shift != 0:
            args.append(u'global_shift={!r}'.format(self._global_shift))
        return u'cirq.PhasedXPowGate({})'.format(u', '.join(args))

    def _period(self):
        exponents = [self._global_shift, 1 + self._global_shift]
        real_periods = [abs(2/e) for e in exponents if e != 0]
        int_periods = [int(np.round(e)) for e in real_periods]
        if any(i != r for i, r in izip(real_periods, int_periods)):
            return None
        if len(int_periods) == 1:
            return int_periods[0]
        return int_periods[0] * int_periods[1] / fractions.gcd(*int_periods)

    @property
    def _canonical_exponent(self):
        period = self._period()
        if not period or isinstance(self._exponent, value.Symbol):
            return self._exponent
        else:
            return self._exponent % period

    def _value_equality_values_(self):
        return self.phase_exponent, self._canonical_exponent, self._global_shift

PhasedXPowGate = value.value_equality(PhasedXPowGate)
