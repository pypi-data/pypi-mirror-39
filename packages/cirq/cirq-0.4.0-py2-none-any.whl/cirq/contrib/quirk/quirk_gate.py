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
from typing import Any, Callable, cast, Dict, Optional, Union

import numpy as np

from cirq import ops, value


class QuirkOp(object):
    u"""An operation as understood by Quirk's parser.

    Basically just a series of text identifiers for each qubit, and some rules
    for how things can be combined.
    """

    def __init__(self, *keys, **_3to2kwargs):
        if 'can_merge' in _3to2kwargs: can_merge = _3to2kwargs['can_merge']; del _3to2kwargs['can_merge']
        else: can_merge = True
        u"""
        Args:
            *keys: The JSON object(s) that each qubit is turned into when
                explaining a gate to Quirk. For example, a CNOT is turned into
                the keys ["•", "X"].

                Note that, when keys terminates early, it is implied that later
                qubits should use the same key as the last key.
            can_merge: Whether or not it is safe to merge a column containing
                this operation into a column containing other operations. For
                example, this is not safe if the column contains a control
                because the control would also apply to the other column's
                gates.
        """
        self.keys = keys
        self.can_merge = can_merge


UNKNOWN_GATE = QuirkOp(u'UNKNOWN', can_merge=False)


def same_half_turns(a1, a2, atol=0.0001):
    d = (a1 - a2 + 1) % 2 - 1
    return abs(d) < atol


def angle_to_exponent_key(t):
    if isinstance(t, value.Symbol):
        return u'^t'

    if same_half_turns(t, 1):
        return u''

    if same_half_turns(t, 0.5):
        return u'^½'

    if same_half_turns(t, -0.5):
        return u'^-½'

    if same_half_turns(t, 0.25):
        return u'^¼'

    if same_half_turns(t, -0.25):
        return u'^-¼'

    return None


def single_qubit_matrix_gate(matrix):
    if matrix is None or matrix.shape[0] != 2:
        return None

    matrix = matrix.round(6)
    matrix_repr = u'{{%s+%si,%s+%si},{%s+%si,%s+%si}}' % (
        np.real(matrix[0, 0]), np.imag(matrix[0, 0]),
        np.real(matrix[1, 0]), np.imag(matrix[1, 0]),
        np.real(matrix[0, 1]), np.imag(matrix[0, 1]),
        np.real(matrix[1, 1]), np.imag(matrix[1, 1]))

    # Clean up.
    matrix_repr = matrix_repr.replace(u'+-', u'-')
    matrix_repr = matrix_repr.replace(u'+0.0i', u'')
    matrix_repr = matrix_repr.replace(u'.0,', u',')
    matrix_repr = matrix_repr.replace(u'.0}', u'}')
    matrix_repr = matrix_repr.replace(u'.0+', u'+')
    matrix_repr = matrix_repr.replace(u'.0-', u'-')

    return QuirkOp({
        u'id': u'?',
        u'matrix': matrix_repr
    })


def known_quirk_op_for_operation(op):
    if isinstance(op, ops.GateOperation):
        return _gate_to_quirk_op(op.gate)
    return None


def _gate_to_quirk_op(gate):
    for gate_type, func in _known_gate_conversions.items():
        if isinstance(gate, gate_type):
            return func(gate)
    return None


def x_to_known(gate):
    e = angle_to_exponent_key(gate.exponent)
    if e is None:
        return None
    return QuirkOp(u'X' + e)


def y_to_known(gate):
    e = angle_to_exponent_key(gate.exponent)
    if e is None:
        return None
    return QuirkOp(u'Y' + e)


def z_to_known(gate):
    e = angle_to_exponent_key(gate.exponent)
    if e is None:
        return None
    return QuirkOp(u'Z' + e)


def cz_to_known(gate):
    e = angle_to_exponent_key(gate.exponent)
    if e is None:
        return None
    return QuirkOp(u'•', u'Z' + e, can_merge=False)


def cnot_to_known(gate):
    e = angle_to_exponent_key(gate.exponent)
    if e is None:
        return None
    return QuirkOp(u'•', u'X' + e, can_merge=False)


def h_to_known(gate):
    if gate.exponent == 1:
        return QuirkOp(u'H')
    return None


def swap_to_known(gate):
    if gate.exponent == 1:
        return QuirkOp(u'Swap', u'Swap')
    return None


_known_gate_conversions = cast(
    Dict[type, Callable[[ops.Gate], Optional[QuirkOp]]],
    {
        ops.XPowGate: x_to_known,
        ops.YPowGate: y_to_known,
        ops.ZPowGate: z_to_known,
        ops.CZPowGate: cz_to_known,
        ops.CNotPowGate: cnot_to_known,
        ops.SwapPowGate: swap_to_known,
        ops.HPowGate: h_to_known,
        ops.MeasurementGate: lambda _: QuirkOp(u'Measure')
    }
)
