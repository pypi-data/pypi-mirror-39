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

u"""Quantum gates defined by a matrix."""

from __future__ import division
from __future__ import absolute_import
from typing import cast, Any

import numpy as np

from cirq import linalg, protocols
from cirq.ops import raw_types


def _phase_matrix(turns):
    return np.diag([1, np.exp(2j * np.pi * turns)])


class SingleQubitMatrixGate(raw_types.Gate):
    u"""A 1-qubit gate defined by its matrix.

    More general than specialized classes like `ZPowGate`, but more expensive
    and more float-error sensitive to work with (due to using
    eigendecompositions).
    """

    def __init__(self, matrix):
        u"""
        Initializes the 2-qubit matrix gate.

        Args:
            matrix: The matrix that defines the gate.
        """
        if matrix.shape != (2, 2) or not linalg.is_unitary(matrix):
            raise ValueError(u'Not a 2x2 unitary matrix: {}'.format(matrix))
        self._matrix = matrix

    def validate_args(self, qubits):
        if len(qubits) != 1:
            raise ValueError(
                u'Single-qubit gate applied to multiple qubits: {}({})'.format(
                    self, qubits))

    def __pow__(self, exponent):
        if not isinstance(exponent, (int, float)):
            return NotImplemented
        e = cast(float, exponent)
        new_mat = linalg.map_eigenvalues(self._matrix, lambda b: b**e)
        return SingleQubitMatrixGate(new_mat)

    def _trace_distance_bound_(self):
        vals = np.linalg.eigvals(self._matrix)
        rotation_angle = abs(np.angle(vals[0] / vals[1]))
        return rotation_angle * 1.2

    def _phase_by_(self, phase_turns, qubit_index):
        z = _phase_matrix(phase_turns)
        phased_matrix = z.dot(self._matrix).dot(np.conj(z.T))
        return SingleQubitMatrixGate(phased_matrix)

    def _has_unitary_(self):
        return True

    def _unitary_(self):
        return np.array(self._matrix)

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(_matrix_to_diagram_symbol(self._matrix, args),))

    def __hash__(self):
        vals = tuple(v for _, v in np.ndenumerate(self._matrix))
        return hash((SingleQubitMatrixGate, vals))

    def approx_eq(self, other, ignore_global_phase=True):
        if not isinstance(other, type(self)):
            return NotImplemented
        cmp = (linalg.allclose_up_to_global_phase if ignore_global_phase
               else np.allclose)
        return cmp(self._matrix, other._matrix)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return np.alltrue(self._matrix == other._matrix)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return u'cirq.SingleQubitMatrixGate({})'.format(
                _numpy_array_repr(self._matrix))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self._matrix.round(3))


class TwoQubitMatrixGate(raw_types.Gate):
    u"""A 2-qubit gate defined only by its matrix.

    More general than specialized classes like `CZPowGate`, but more expensive
    and more float-error sensitive to work with (due to using
    eigendecompositions).
    """

    def __init__(self, matrix):
        u"""
        Initializes the 2-qubit matrix gate.

        Args:
            matrix: The matrix that defines the gate.
        """

        if matrix.shape != (4, 4) or not linalg.is_unitary(matrix):
            raise ValueError(u'Not a 4x4 unitary matrix: {}'.format(matrix))
        self._matrix = matrix

    def validate_args(self, qubits):
        if len(qubits) != 2:
            raise ValueError(
                u'Two-qubit gate not applied to two qubits: {}({})'.format(
                    self, qubits))

    def __pow__(self, exponent):
        if not isinstance(exponent, (int, float)):
            return NotImplemented
        e = cast(float, exponent)
        new_mat = linalg.map_eigenvalues(self._matrix, lambda b: b**e)
        return TwoQubitMatrixGate(new_mat)

    def _phase_by_(self, phase_turns, qubit_index):
        i = np.eye(2)
        z = _phase_matrix(phase_turns)
        z2 = np.kron(i, z) if qubit_index else np.kron(z, i)
        phased_matrix = z2.dot(self._matrix).dot(np.conj(z2.T))
        return TwoQubitMatrixGate(phased_matrix)

    def approx_eq(self, other, ignore_global_phase=True):
        if not isinstance(other, type(self)):
            return NotImplemented
        cmp = (linalg.allclose_up_to_global_phase if ignore_global_phase
               else np.allclose)
        return cmp(self._matrix, other._matrix)

    def _unitary_(self):
        return np.array(self._matrix)

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(_matrix_to_diagram_symbol(self._matrix, args), u'#2'))

    def __hash__(self):
        vals = tuple(v for _, v in np.ndenumerate(self._matrix))
        return hash((SingleQubitMatrixGate, vals))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return np.alltrue(self._matrix == other._matrix)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return u'cirq.TwoQubitMatrixGate({})'.format(
                _numpy_array_repr(self._matrix))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self._matrix.round(3))


def _matrix_to_diagram_symbol(matrix,
                              args):
    if args.precision is not None:
        matrix = matrix.round(args.precision)
    result = unicode(matrix)
    if args.use_unicode_characters:
        lines = result.split(u'\n')
        for i in xrange(len(lines)):
            lines[i] = lines[i].replace(u'[[', u'')
            lines[i] = lines[i].replace(u' [', u'')
            lines[i] = lines[i].replace(u']', u'')
        w = max(len(line) for line in lines)
        for i in xrange(len(lines)):
            lines[i] = u'│' + lines[i].ljust(w) + u'│'
        lines.insert(0, u'┌' + u' ' * w + u'┐')
        lines.append(u'└' + u' ' * w + u'┘')
        result = u'\n'.join(lines)
    return result


def _numpy_array_repr(arr):
    return u'np.array({!r})'.format(arr.tolist())
