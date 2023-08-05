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

u"""Quantum gates that phase with respect to product-of-pauli observables."""

from __future__ import division
from __future__ import absolute_import
from typing import Union, Optional

import numpy as np

from cirq import protocols
from cirq.ops import gate_features, eigen_gate
from cirq.ops.common_gates import _rads_func_symbol


class XXPowGate(eigen_gate.EigenGate,
                gate_features.TwoQubitGate,
                gate_features.InterchangeableQubitsGate):
    u"""The X-parity gate, possibly raised to a power.

    At exponent=1, this gate implements the following unitary:

        X⊗X = [0 0 0 1]
              [0 0 1 0]
              [0 1 0 0]
              [1 0 0 0]

    See also: `cirq.MS` (the Mølmer–Sørensen gate), which is implemented via
        this class.
    """

    def _eigen_components(self):
        return [
            (0., np.array([[0.5, 0, 0, 0.5],
                           [0, 0.5, 0.5, 0],
                           [0, 0.5, 0.5, 0],
                           [0.5, 0, 0, 0.5]])),
            (1., np.array([[0.5, 0, 0, -0.5],
                           [0, 0.5, -0.5, 0],
                           [0, -0.5, 0.5, 0],
                           [-0.5, 0, 0, 0.5]])),
        ]

    def _eigen_shifts(self):
        return [0, 1]

    def _circuit_diagram_info_(self, args
                               ):
        if self._global_shift == -0.5:
            # Mølmer–Sørensen gate.
            symbol = _rads_func_symbol(
                u'MS',
                args,
                self._diagram_exponent(args, ignore_global_phase=False)/2)
            return protocols.CircuitDiagramInfo(
                                wire_symbols=(symbol, symbol))

        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'XX', u'XX'),
            exponent=self._diagram_exponent(args))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._global_shift == -0.5:
            if self._exponent == 1:
                return u'MS(π/2)'
            return u'MS({!r}π/2)'.format(self._exponent)
        if self.exponent == 1:
            return u'XX'
        return u'XX**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == -0.5 and not protocols.is_parameterized(self):
            if self._exponent == 1:
                return u'cirq.MS(np.pi/2)'
            return u'cirq.MS({!r}*np.pi/2)'.format(self._exponent)
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.XX'
            return u'(cirq.XX**{!r})'.format(self._exponent)
        return (u'cirq.XXPowGate(exponent={!r}, '
                u'global_shift={!r})'
                ).format(self._exponent, self._global_shift)


class YYPowGate(eigen_gate.EigenGate,
                gate_features.TwoQubitGate,
                gate_features.InterchangeableQubitsGate):
    u"""The Y-parity gate, possibly raised to a power."""

    def _eigen_components(self):
        return [
            (0., np.array([[0.5, 0, 0, -0.5],
                           [0, 0.5, 0.5, 0],
                           [0, 0.5, 0.5, 0],
                           [-0.5, 0, 0, 0.5]])),
            (1., np.array([[0.5, 0, 0, 0.5],
                           [0, 0.5, -0.5, 0],
                           [0, -0.5, 0.5, 0],
                           [0.5, 0, 0, 0.5]])),
        ]

    def _eigen_shifts(self):
        return [0, 1]

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'YY', u'YY'),
            exponent=self._diagram_exponent(args))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'YY'
        return u'YY**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.YY'
            return u'(cirq.YY**{!r})'.format(self._exponent)
        return (u'cirq.YYPowGate(exponent={!r}, '
                u'global_shift={!r})'
                ).format(self._exponent, self._global_shift)


class ZZPowGate(eigen_gate.EigenGate,
                gate_features.TwoQubitGate,
                gate_features.InterchangeableQubitsGate):
    u"""The Z-parity gate, possibly raised to a power.

    The ZZ**t gate implements the following unitary:

        (Z⊗Z)^t = [1 . . .]
                  [. w . .]
                  [. . w .]
                  [. . . 1]

        where w = e^{i \pi t} and '.' means '0'.
    """

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0, 0, 1])),
            (1, np.diag([0, 1, 1, 0])),
        ]

    def _eigen_shifts(self):
        return [0, 1]

    def _circuit_diagram_info_(self, args
                               ):
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'ZZ', u'ZZ'),
            exponent=self._diagram_exponent(args))

    def _apply_unitary_(self, args
                        ):
        if protocols.is_parameterized(self):
            return None

        global_phase = 1j**(2 * self._exponent * self._global_shift)
        if global_phase != 1:
            args.target_tensor *= global_phase

        relative_phase = 1j**(2 * self.exponent)
        zo = args.subspace_index(0b01)
        oz = args.subspace_index(0b10)
        args.target_tensor[oz] *= relative_phase
        args.target_tensor[zo] *= relative_phase

        return args.target_tensor

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self._exponent == 1:
            return u'ZZ'
        return u'ZZ**{!r}'.format(self._exponent)

    def __repr__(self):
        if self._global_shift == 0:
            if self._exponent == 1:
                return u'cirq.ZZ'
            return u'(cirq.ZZ**{!r})'.format(self._exponent)
        return (u'cirq.ZZPowGate(exponent={!r}, '
                u'global_shift={!r})'
                ).format(self._exponent, self._global_shift)


XX = XXPowGate()
YY = YYPowGate()
ZZ = ZZPowGate()
