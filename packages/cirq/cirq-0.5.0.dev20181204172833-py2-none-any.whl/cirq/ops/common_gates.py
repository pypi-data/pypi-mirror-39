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

u"""Quantum gates that are commonly used in the literature.

This module creates Gate instances for the following gates:
    X,Y,Z: Pauli gates.
    H,S: Clifford gates.
    T: A non-Clifford gate.
    CZ: Controlled phase gate.
    CNOT: Controlled not gate.
    SWAP: the swap gate.
    ISWAP: a swap gate with a phase on the swapped subspace.

Each of these are implemented as EigenGates, which means that they can be
raised to a power (i.e. cirq.H**0.5). See the definition in EigenGate.

In addition MeasurementGate is defined and convenience methods for
measurements are provided
    measure
    measure_each
"""
from __future__ import division
from __future__ import absolute_import
from typing import (
    Any, Callable, cast, Iterable, List, Optional, Tuple, Union,
)

import numpy as np

from cirq import linalg, protocols, value
from cirq.ops import gate_features, eigen_gate, raw_types, gate_operation

from cirq.type_workarounds import NotImplementedType

# Note: avoiding 'from/as' because it creates a circular dependency in python 2.
import cirq.ops.phased_x_gate
from itertools import izip


class XPowGate(eigen_gate.EigenGate,
               gate_features.SingleQubitGate):
    u"""A gate that rotates around the X axis of the Bloch sphere.

    The unitary matrix of ``XPowGate(exponent=t)`` is:

        [[g·c, -i·g·s],
         [-i·g·s, g·c]]

    where:

        c = cos(π·t/2)
        s = sin(π·t/2)
        g = exp(i·π·t/2).

    Note in particular that this gate has a global phase factor of
    e^{i·π·t/2} vs the traditionally defined rotation matrices
    about the Pauli X axis. See `cirq.Rx` for rotations without the global
    phase. The global phase factor can be adjusted by using the `global_shift`
    parameter when initializing.

    `cirq.X`, the Pauli X gate, is an instance of this gate at exponent=1.
    """

    def _apply_unitary_(self, args
                        ):
        if self._exponent != 1:
            return None
        zero = args.subspace_index(0)
        one = args.subspace_index(1)
        args.available_buffer[zero] = args.target_tensor[one]
        args.available_buffer[one] = args.target_tensor[zero]
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.available_buffer *= p
        return args.available_buffer

    def _eigen_components(self):
        return [
            (0, np.array([[0.5, 0.5], [0.5, 0.5]])),
            (1, np.array([[0.5, -0.5], [-0.5, 0.5]])),
        ]

    def _circuit_diagram_info_(self, args
                               ):
        if self._global_shift == -0.5:
            return _rads_func_symbol(
                u'Rx',
                args,
                self._diagram_exponent(args, ignore_global_phase=False))

        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'X',),
            exponent=self._diagram_exponent(args))

    def _qasm_(self,
               args,
               qubits):
        args.validate_version(u'2.0')
        if self._exponent == 1:
            return args.format(u'x {0};\n', qubits[0])
        else:
            return args.format(u'rx({0:half_turns}) {1};\n',
                               self._exponent, qubits[0])

    @property
    def phase_exponent(self):
        return 0.0

    def _phase_by_(self, phase_turns, qubit_index):
        u"""See `cirq.SupportsPhase`."""
        return cirq.ops.phased_x_gate.PhasedXPowGate(
            exponent=self._exponent,
            phase_exponent=phase_turns * 2)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'X'
        return u'X**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == -0.5 and not protocols.is_parameterized(self):
            return u'cirq.Rx(np.pi*{!r})'.format(self._exponent)
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.X'
            return u'(cirq.X**{!r})'.format(self._exponent)
        return (
            u'cirq.XPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


class YPowGate(eigen_gate.EigenGate,
               gate_features.SingleQubitGate):
    u"""A gate that rotates around the Y axis of the Bloch sphere.

    The unitary matrix of ``YPowGate(exponent=t)`` is:

        [[g·c, g·s],
         [-g·s, g·c]]

    where:

        c = cos(π·t/2)
        s = sin(π·t/2)
        g = exp(i·π·t/2).

    Note in particular that this gate has a global phase factor of
    e^{i·π·t/2} vs the traditionally defined rotation matrices
    about the Pauli Y axis. See `cirq.Ry` for rotations without the global
    phase. The global phase factor can be adjusted by using the `global_shift`
    parameter when initializing.

    `cirq.Y`, the Pauli Y gate, is an instance of this gate at exponent=1.
    """

    def _eigen_components(self):
        return [
            (0, np.array([[0.5, -0.5j], [0.5j, 0.5]])),
            (1, np.array([[0.5, 0.5j], [-0.5j, 0.5]])),
        ]

    def _circuit_diagram_info_(self, args
                               ):
        if self._global_shift == -0.5:
            return _rads_func_symbol(
                u'Ry',
                args,
                self._diagram_exponent(args, ignore_global_phase=False))

        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'Y',),
            exponent=self._diagram_exponent(args))

    def _qasm_(self,
               args,
               qubits):
        args.validate_version(u'2.0')
        if self._exponent == 1:
            return args.format(u'y {0};\n', qubits[0])
        else:
            return args.format(u'ry({0:half_turns}) {1};\n',
                               self._exponent, qubits[0])

    @property
    def phase_exponent(self):
        return 0.5

    def _phase_by_(self, phase_turns, qubit_index):
        u"""See `cirq.SupportsPhase`."""
        return cirq.ops.phased_x_gate.PhasedXPowGate(
            exponent=self._exponent,
            phase_exponent=0.5 + phase_turns * 2)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'Y'
        return u'Y**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == -0.5 and not protocols.is_parameterized(self):
            return u'cirq.Ry(np.pi*{!r})'.format(self._exponent)
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.Y'
            return u'(cirq.Y**{!r})'.format(self._exponent)
        return (
            u'cirq.YPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


class ZPowGate(eigen_gate.EigenGate,
               gate_features.SingleQubitGate):
    u"""A gate that rotates around the Z axis of the Bloch sphere.

    The unitary matrix of ``ZPowGate(exponent=t)`` is:

        [[1, 0],
         [0, g]]

    where:

        g = exp(i·π·t).

    Note in particular that this gate has a global phase factor of
    e^{i·π·t/2} vs the traditionally defined rotation matrices
    about the Pauli Z axis. See `cirq.Rz` for rotations without the global
    phase. The global phase factor can be adjusted by using the `global_shift`
    parameter when initializing.

    `cirq.Z`, the Pauli Z gate, is an instance of this gate at exponent=1.
    """

    def _apply_unitary_(self, args
                        ):
        if protocols.is_parameterized(self):
            return None

        one = args.subspace_index(1)
        c = 1j**(self._exponent * 2)
        args.target_tensor[one] *= c
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.target_tensor *= p
        return args.target_tensor

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0])),
            (1, np.diag([0, 1])),
        ]

    def _phase_by_(self, phase_turns, qubit_index):
        return self

    def _circuit_diagram_info_(self, args
                               ):
        if self._global_shift == -0.5:
            return _rads_func_symbol(
                u'Rz',
                args,
                self._diagram_exponent(args, ignore_global_phase=False))

        e = self._diagram_exponent(args)
        if e in [-0.25, 0.25]:
            return protocols.CircuitDiagramInfo(
                wire_symbols=(u'T',),
                exponent=cast(float, e) * 4)

        if e in [-0.5, 0.5]:
            return protocols.CircuitDiagramInfo(
                wire_symbols=(u'S',),
                exponent=cast(float, e) * 2)

        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'Z',),
            exponent=e)

    def _qasm_(self,
               args,
               qubits):
        args.validate_version(u'2.0')
        if self._exponent == 1:
            return args.format(u'z {0};\n', qubits[0])
        else:
            return args.format(u'rz({0:half_turns}) {1};\n',
                               self._exponent, qubits[0])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 0.25:
            return u'T'
        if self._exponent == -0.25:
            return u'T**-1'
        if self._exponent == 0.5:
            return u'S'
        if self._exponent == -0.5:
            return u'S**-1'
        if self._exponent == 1:
            return u'Z'
        return u'Z**{}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == -0.5 and not protocols.is_parameterized(self):
            return u'cirq.Rz(np.pi*{!r})'.format(self._exponent)
        if self._global_shift == 0:
            if self._exponent == 0.25:
                return u'cirq.T'
            if self._exponent == -0.25:
                return u'(cirq.T**-1)'
            if self._exponent == 0.5:
                return u'cirq.S'
            if self._exponent == -0.5:
                return u'(cirq.S**-1)'
            if self._exponent == 1:
                return u'cirq.Z'
            return u'(cirq.Z**{!r})'.format(self._exponent)
        return (
            u'cirq.ZPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


class MeasurementGate(raw_types.Gate):
    u"""A gate that measures qubits in the computational basis.

    The measurement gate contains a key that is used to identify results
    of measurements.
    """

    def __init__(self,
                 key = u'',
                 invert_mask = ()):
        u"""
        Args:
            key: The string key of the measurement.
            invert_mask: A list of values indicating whether the corresponding
                qubits should be flipped. The list's length must not be longer
                than the number of qubits, but it is permitted to be shorter.
                Qubits with indices past the end of the mask are not flipped.
        """
        self.key = key
        self.invert_mask = invert_mask or ()

    @staticmethod
    def is_measurement(op):
        if isinstance(op, MeasurementGate):
            return True
        if (isinstance(op, gate_operation.GateOperation) and
                isinstance(op.gate, MeasurementGate)):
            return True
        return False

    def with_bits_flipped(self, *bit_positions):
        u"""Toggles whether or not the measurement inverts various outputs."""
        old_mask = self.invert_mask or ()
        n = max(len(old_mask) - 1, *bit_positions) + 1
        new_mask = [k < len(old_mask) and old_mask[k] for k in xrange(n)]
        for b in bit_positions:
            new_mask[b] = not new_mask[b]
        return MeasurementGate(key=self.key, invert_mask=tuple(new_mask))

    def validate_args(self, qubits):
        if (self.invert_mask is not None and
                len(self.invert_mask) > len(qubits)):
            raise ValueError(u'len(invert_mask) > len(qubits)')

    def _circuit_diagram_info_(self, args
                               ):
        n = (max(1, len(self.invert_mask))
             if args.known_qubit_count is None
             else args.known_qubit_count)
        symbols = [u'M'] * n

        # Show which output bits are negated.
        if self.invert_mask:
            for i, b in enumerate(self.invert_mask):
                if b:
                    symbols[i] = u'!M'

        # Mention the measurement key.
        if (not args.known_qubits or
                self.key != _default_measurement_key(args.known_qubits)):
            symbols[0] += u"('{}')".format(self.key)

        return protocols.CircuitDiagramInfo(tuple(symbols))

    def _qasm_(self,
               args,
               qubits):
        args.validate_version(u'2.0')
        invert_mask = self.invert_mask
        if len(invert_mask) < len(qubits):
            invert_mask = (invert_mask
                           + (False,) * (len(qubits) - len(invert_mask)))
        lines = []
        for i, (qubit, inv) in enumerate(izip(qubits, invert_mask)):
            if inv:
                lines.append(args.format(
                    u'x {0};  // Invert the following measurement\n', qubit))
            lines.append(args.format(u'measure {0} -> {1:meas}[{2}];\n',
                                     qubit, self.key, i))
        return u''.join(lines)

    def __repr__(self):
        return u'cirq.MeasurementGate({}, {})'.format(repr(self.key),
                                                     repr(self.invert_mask))

    def _value_equality_values_(self):
        return self.key, self.invert_mask


MeasurementGate = value.value_equality(MeasurementGate)

def _default_measurement_key(qubits):
    return u','.join(unicode(q) for q in qubits)


def measure(*qubits, **_3to2kwargs
            ):
    if 'invert_mask' in _3to2kwargs: invert_mask = _3to2kwargs['invert_mask']; del _3to2kwargs['invert_mask']
    else: invert_mask =  ()
    if 'key' in _3to2kwargs: key = _3to2kwargs['key']; del _3to2kwargs['key']
    else: key =  None
    u"""Returns a single MeasurementGate applied to all the given qubits.

    The qubits are measured in the computational basis.

    Args:
        *qubits: The qubits that the measurement gate should measure.
        key: The string key of the measurement. If this is None, it defaults
            to a comma-separated list of the target qubits' str values.
        invert_mask: A list of Truthy or Falsey values indicating whether
            the corresponding qubits should be flipped. None indicates no
            inverting should be done.

    Returns:
        An operation targeting the given qubits with a measurement.

    Raises:
        ValueError if the qubits are not instances of QubitId.
    """
    for qubit in qubits:
        if isinstance(qubit, np.ndarray):
            raise ValueError(
                    u'measure() was called a numpy ndarray. Perhaps you meant '
                    u'to call measure_state_vector on numpy array?'
            )
        elif not isinstance(qubit, raw_types.QubitId):
            raise ValueError(
                    u'measure() was called with type different than QubitId.')

    if key is None:
        key = _default_measurement_key(qubits)
    return MeasurementGate(key, invert_mask).on(*qubits)


def measure_each(*qubits, **_3to2kwargs
                 ):
    if 'key_func' in _3to2kwargs: key_func = _3to2kwargs['key_func']; del _3to2kwargs['key_func']
    else: key_func =  unicode
    u"""Returns a list of operations individually measuring the given qubits.

    The qubits are measured in the computational basis.

    Args:
        *qubits: The qubits to measure.
        key_func: Determines the key of the measurements of each qubit. Takes
            the qubit and returns the key for that qubit. Defaults to str.

    Returns:
        A list of operations individually measuring the given qubits.
    """
    return [MeasurementGate(key_func(q)).on(q) for q in qubits]


class HPowGate(eigen_gate.EigenGate, gate_features.SingleQubitGate):
    u"""A Gate that performs a rotation around the X+Z axis of the Bloch sphere.


    The unitary matrix of ``HPowGate(exponent=t)`` is:

        [[g·(c-i·s/sqrt(2)), -i·g·s/sqrt(2)],
        [-i·g·s/sqrt(2)], g·(c+i·s/sqrt(2))]]

    where

        c = cos(π·t/2)
        s = sin(π·t/2)
        g = exp(i·π·t/2).

    Note in particular that for `t=1`, this gives the Hadamard matrix.

    `cirq.H`, the Hadamard gate, is an instance of this gate at `exponent=1`.
    """

    def _eigen_components(self):
        s = np.sqrt(2)

        component0 = np.array([
            [3 + 2 * s, 1 + s],
            [1 + s, 1]
        ]) / (4 + 2 * s)

        component1 = np.array([
            [3 - 2 * s, 1 - s],
            [1 - s, 1]
        ]) / (4 - 2 * s)

        return [(0, component0), (1, component1)]

    def _apply_unitary_(self, args
                        ):
        if self._exponent != 1:
            return None

        zero = args.subspace_index(0)
        one = args.subspace_index(1)
        args.target_tensor[one] -= args.target_tensor[zero]
        args.target_tensor[one] *= -0.5
        args.target_tensor[zero] -= args.target_tensor[one]
        p = 1j**(2 * self._exponent * self._global_shift)
        args.target_tensor *= np.sqrt(2) * p
        return args.target_tensor

    def _decompose_(self, qubits):
        q = qubits[0]

        if self._exponent == 1:
            yield cirq.Y(q)**0.5
            yield cirq.XPowGate(global_shift=-0.25).on(q)
            return

        yield Y(q)**0.25
        yield X(q)**self._exponent
        yield Y(q)**-0.25

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo((u'H',))

    def _qasm_(self,
               args,
               qubits):
        args.validate_version(u'2.0')
        if self._exponent == 1:
            return args.format(u'h {0};\n', qubits[0])
        else:
            return args.format(u'ry({0:half_turns}) {3};\n'
                               u'rx({1:half_turns}) {3};\n'
                               u'ry({2:half_turns}) {3};\n',
                               0.25,  self._exponent, -0.25, qubits[0])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'H'
        return u'H^{}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.H'
            return u'(cirq.H**{!r})'.format(self._exponent)
        return (
            u'cirq.HPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


class CZPowGate(eigen_gate.EigenGate,
                gate_features.TwoQubitGate,
                gate_features.InterchangeableQubitsGate):
    u"""A gate that applies a phase to the |11⟩ state of two qubits.

    The unitary matrix of `CZPowGate(exponent=t)` is:

        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, g]]

    where:

        g = exp(i·π·t/2).

    `cirq.CZ`, the controlled Z gate, is an instance of this gate at
    `exponent=1`.
    """

    def _eigen_components(self):
        return [
            (0, np.diag([1, 1, 1, 0])),
            (1, np.diag([0, 0, 0, 1])),
        ]

    def _apply_unitary_(self, args
                        ):
        if protocols.is_parameterized(self):
            return NotImplemented

        c = 1j**(2 * self._exponent)
        one_one = linalg.slice_for_qubits_equal_to(args.axes, 0b11)
        args.target_tensor[one_one] *= c
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.target_tensor *= p
        return args.target_tensor

    def _phase_by_(self, phase_turns, qubit_index):
        return self

    def _circuit_diagram_info_(self, args
    ):
        return protocols.CircuitDiagramInfo(
                wire_symbols=(u'@', u'@'),
                exponent=self._diagram_exponent(args))

    def _qasm_(self,
            args,
            qubits):
        if self._exponent != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'cz {0},{1};\n', qubits[0], qubits[1])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'CZ'
        return u'CZ**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.CZ'
            return u'(cirq.CZ**{!r})'.format(self._exponent)
        return (
            u'cirq.CZPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


def _rads_func_symbol(func_name,
        args,
        half_turns):
    unit = u'π' if args.use_unicode_characters else u'pi'
    if half_turns == 1:
        return u'{}({})'.format(func_name, unit)
    if half_turns == -1:
        return u'{}(-{})'.format(func_name, unit)
    return u'{}({}{})'.format(func_name, half_turns, unit)


class CNotPowGate(eigen_gate.EigenGate, gate_features.TwoQubitGate):
    u"""A gate that applies a controlled power of an X gate.

    When applying CNOT (controlled-not) to qubits, you can either use
    positional arguments CNOT(q1, q2), where q2 is toggled when q1 is on,
    or named arguments CNOT(control=q1, target=q2).
    (Mixing the two is not permitted.)

    The unitary matrix of `CNotPowGate(exponent=t)` is:

        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, g·c, -i·g·s],
         [0, 0, -i·g·s, g·c]]

    where:

        c = cos(π·t/2)
        s = sin(π·t/2)
        g = exp(i·π·t/2).

    `cirq.CNOT`, the controlled NOT gate, is an instance of this gate at
    `exponent=1`.
    """

    def _decompose_(self, qubits):
        c, t = qubits
        yield Y(t)**-0.5
        yield CZ(c, t)**self._exponent
        yield Y(t)**0.5

    def _eigen_components(self):
        return [
            (0, np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0.5, 0.5],
                          [0, 0, 0.5, 0.5]])),
            (1, np.array([[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0.5, -0.5],
                          [0, 0, -0.5, 0.5]])),
        ]

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'@', u'X'),
            exponent=self._diagram_exponent(args))

    def _apply_unitary_(self, args
                        ):
        if self._exponent != 1:
            return None

        oo = args.subspace_index(0b11)
        zo = args.subspace_index(0b01)
        args.available_buffer[oo] = args.target_tensor[oo]
        args.target_tensor[oo] = args.target_tensor[zo]
        args.target_tensor[zo] = args.available_buffer[oo]
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.target_tensor *= p
        return args.target_tensor

    def _qasm_(self,
               args,
               qubits):
        if self._exponent != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'cx {0},{1};\n', qubits[0], qubits[1])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'CNOT'
        return u'CNOT**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.CNOT'
            return u'(cirq.CNOT**{!r})'.format(self._exponent)
        return (
            u'cirq.CNotPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)

    def on(self, *args,
           **kwargs):
        if not kwargs:
            return super(CNotPowGate, self).on(*args)
        if not args and set(kwargs.keys()) == set([u'control', u'target']):
            return super(CNotPowGate, self).on(kwargs[u'control'], kwargs[u'target'])
        raise ValueError(
            u"Expected two positional argument or else 'target' AND 'control' "
            u"keyword arguments. But got args={!r}, kwargs={!r}.".format(
                args, kwargs))


class SwapPowGate(eigen_gate.EigenGate,
                  gate_features.TwoQubitGate,
                  gate_features.InterchangeableQubitsGate):
    u"""The SWAP gate, possibly raised to a power. Exchanges qubits.

    SwapPowGate()**t = SwapPowGate(exponent=t) and acts on two qubits in the
    computational basis as the matrix:

        [[1, 0, 0, 0],
         [0, g·c, -i·g·s, 0],
         [0, -i·g·s, g·c, 0],
         [0, 0, 0, 1]]

    where:

        c = cos(π·t/2)
        s = sin(π·t/2)
        g = exp(i·π·t/2).

    `cirq.SWAP`, the swap gate, is an instance of this gate at exponent=1.
    """

    def _decompose_(self, qubits):
        u"""See base class."""
        a, b = qubits
        yield CNOT(a, b)
        yield CNOT(b, a) ** self._exponent
        yield CNOT(a, b)

    def _eigen_components(self):
        return [
            (0, np.array([[1, 0,   0,   0],
                          [0, 0.5, 0.5, 0],
                          [0, 0.5, 0.5, 0],
                          [0, 0,   0,   1]])),
            (1, np.array([[0,  0,    0,   0],
                          [0,  0.5, -0.5, 0],
                          [0, -0.5,  0.5, 0],
                          [0,  0,    0,   0]])),
        ]

    def _apply_unitary_(self, args
                        ):
        if self._exponent != 1:
            return None

        zo = args.subspace_index(0b01)
        oz = args.subspace_index(0b10)
        args.available_buffer[zo] = args.target_tensor[zo]
        args.target_tensor[zo] = args.target_tensor[oz]
        args.target_tensor[oz] = args.available_buffer[zo]
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.target_tensor *= p
        return args.target_tensor

    def _circuit_diagram_info_(self, args
                               ):
        if not args.use_unicode_characters:
            return protocols.CircuitDiagramInfo(
                wire_symbols=(u'swap', u'swap'),
                exponent=self._diagram_exponent(args))
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'×', u'×'),
            exponent=self._diagram_exponent(args))

    def _qasm_(self,
               args,
               qubits):
        if self._exponent != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'swap {0},{1};\n', qubits[0], qubits[1])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'SWAP'
        return u'SWAP**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.SWAP'
            return u'(cirq.SWAP**{!r})'.format(self._exponent)
        return (
            u'cirq.SwapPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


class ISwapPowGate(eigen_gate.EigenGate,
                   gate_features.InterchangeableQubitsGate,
                   gate_features.TwoQubitGate):
    u"""Rotates the |01⟩-vs-|10⟩ subspace of two qubits around its Bloch X-axis.

    When exponent=1, swaps the two qubits and phases |01⟩ and |10⟩ by i. More
    generally, this gate's matrix is defined as follows:

        ISWAP**t ≡ exp(+i π t (X⊗X + Y⊗Y) / 4)

    which is given by the matrix:

        [[1, 0, 0, 0],
         [0, c, i·s, 0],
         [0, i·s, c, 0],
         [0, 0, 0, 1]]

    where:

        c = cos(π·t/2)
        s = sin(π·t/2)

    `cirq.ISWAP`, the swap gate that applies -i to the |01> and |10> states,
    is an instance of this gate at exponent=1.
    """

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0, 0, 1])),
            (+0.5, np.array([[0, 0, 0, 0],
                             [0, 0.5, 0.5, 0],
                             [0, 0.5, 0.5, 0],
                             [0, 0, 0, 0]])),
            (-0.5, np.array([[0, 0, 0, 0],
                             [0, 0.5, -0.5, 0],
                             [0, -0.5, 0.5, 0],
                             [0, 0, 0, 0]])),
        ]

    def _decompose_(self, qubits):
        a, b = qubits

        yield CNOT(a, b)
        yield H(a)
        yield CNOT(b, a)
        yield S(a)**self._exponent
        yield CNOT(b, a)
        yield S(a)**-self._exponent
        yield H(a)
        yield CNOT(a, b)

    def _apply_unitary_(self, args
                        ):
        if self._exponent != 1:
            return None

        zo = args.subspace_index(0b01)
        oz = args.subspace_index(0b10)
        args.available_buffer[zo] = args.target_tensor[zo]
        args.target_tensor[zo] = args.target_tensor[oz]
        args.target_tensor[oz] = args.available_buffer[zo]
        args.target_tensor[zo] *= 1j
        args.target_tensor[oz] *= 1j
        p = 1j**(2 * self._exponent * self._global_shift)
        if p != 1:
            args.target_tensor *= p
        return args.target_tensor

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'iSwap', u'iSwap'),
            exponent=self._diagram_exponent(args))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'ISWAP'
        return u'ISWAP**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.ISWAP'
            return u'(cirq.ISWAP**{!r})'.format(self._exponent)
        return (
            u'cirq.ISwapPowGate(exponent={!r}, '
            u'global_shift={!r})'
        ).format(self._exponent, self._global_shift)


def Rx(rads):
    u"""Returns a gate with the matrix e^{-i X rads / 2}."""
    return XPowGate(exponent=rads / np.pi, global_shift=-0.5)


def Ry(rads):
    u"""Returns a gate with the matrix e^{-i Y rads / 2}."""
    return YPowGate(exponent=rads / np.pi, global_shift=-0.5)


def Rz(rads):
    u"""Returns a gate with the matrix e^{-i Z rads / 2}."""
    return ZPowGate(exponent=rads / np.pi, global_shift=-0.5)


X = XPowGate()
u"""The Pauli X gate.

Matrix:

    [[0, 1],
     [1, 0]]
"""


#: The Pauli Y gate.
#:
#: Matrix:
#:
#:     [[0, -i],
#:      [i, 0]]
Y = YPowGate()


# The Pauli Z gate.
#
# Matrix:
#
#     [[1, 0],
#      [0, -1]]
Z = ZPowGate()


# The Hadamard gate.
#
# Matrix:
#
#     [[s, s],
#      [s, -s]]
#     where s = sqrt(0.5).
H = HPowGate()


# The Clifford S gate.
#
# Matrix:
#
#     [[1, 0],
#      [0, i]]
S = Z**0.5


# The T gate.
#
# Matrix:
#
#     [[1, 0]
#      [0, exp(i pi / 4)]]
T = Z**0.25


# The controlled Z gate.
#
# Matrix:
#
#     [[1, 0, 0, 0],
#      [0, 1, 0, 0],
#      [0, 0, 1, 0],
#      [0, 0, 0, -1]]
CZ = CZPowGate()


# The controlled NOT gate.
#
# Matrix:
#
#     [[1, 0, 0, 0],
#      [0, 1, 0, 0],
#      [0, 0, 0, 1],
#      [0, 0, 1, 0]]
CNOT = CNotPowGate()


# The swap gate.
#
# Matrix:
#
#     [[1, 0, 0, 0],
#      [0, 0, 1, 0],
#      [0, 1, 0, 0],
#      [0, 0, 0, 1]]
SWAP = SwapPowGate()


# The iswap gate.
#
# Matrix:
#
#     [[1, 0, 0, 0],
#      [0, 0, i, 0],
#      [0, i, 0, 0],
#      [0, 0, 0, 1]]
ISWAP = ISwapPowGate()
