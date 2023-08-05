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
from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
from typing import Union, Tuple, cast

import numpy as np
import pytest

import cirq
from cirq.type_workarounds import NotImplementedType


class RestrictedGate(cirq.Gate):
    pass


CY = cirq.ControlledGate(cirq.Y)
CCH = cirq.ControlledGate(cirq.ControlledGate(cirq.H))
CRestricted = cirq.ControlledGate(RestrictedGate())


def test_init():
    gate = cirq.ControlledGate(cirq.Z)
    assert gate.sub_gate is cirq.Z


def test_validate_args():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    c = cirq.NamedQubit(u'c')

    # Need a control qubit.
    with pytest.raises(ValueError):
        CRestricted.validate_args([])
    CRestricted.validate_args([a])

    # CY is a two-qubit operation (control + single-qubit sub gate).
    with pytest.raises(ValueError):
        CY.validate_args([a])
    with pytest.raises(ValueError):
        CY.validate_args([a, b, c])
    CY.validate_args([a, b])

    # Applies when creating operations.
    with pytest.raises(ValueError):
        _ = CY.on(a)
    with pytest.raises(ValueError):
        _ = CY.on(a, b, c)
    _ = CY.on(a, b)


def test_eq():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(CY, cirq.ControlledGate(cirq.Y))
    eq.add_equality_group(CCH)
    eq.add_equality_group(cirq.ControlledGate(cirq.H))
    eq.add_equality_group(cirq.ControlledGate(cirq.X))
    eq.add_equality_group(cirq.X)


def test_unitary():
    cxa = cirq.ControlledGate(cirq.X**cirq.Symbol(u'a'))
    assert not cirq.has_unitary(cxa)
    assert cirq.unitary(cxa, None) is None

    assert cirq.has_unitary(CY)
    assert cirq.has_unitary(CCH)
    np.testing.assert_allclose(
        cirq.unitary(CY),
        np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -1j],
            [0, 0, 1j, 0],
        ]),
        atol=1e-8)

    np.testing.assert_allclose(
        cirq.unitary(CCH),
        np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, np.sqrt(0.5), np.sqrt(0.5)],
            [0, 0, 0, 0, 0, 0, np.sqrt(0.5), -np.sqrt(0.5)],
        ]),
        atol=1e-8)


class GateUsingWorkspaceForApplyUnitary(cirq.SingleQubitGate):
    def _apply_unitary_(self, args
                        ):
        args.available_buffer[...] = args.target_tensor
        args.target_tensor[...] = 0
        return args.available_buffer

    def _unitary_(self):
        return np.eye(2)

    def __pow__(self, exponent):
        return self

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return (u'cirq.ops.controlled_gate_test.'
                u'GateUsingWorkspaceForApplyUnitary()')


class GateAllocatingNewSpaceForResult(cirq.SingleQubitGate):
    def _apply_unitary_(self, args
                        ):
        assert len(args.axes) == 1
        a = args.axes[0]
        seed = cast(Tuple[Union[int, slice, u'ellipsis'], ...],
                    (slice(None),))
        zero = seed*a + (0, Ellipsis)
        one = seed*a + (1, Ellipsis)
        result = np.zeros(args.target_tensor.shape, args.target_tensor.dtype)
        result[zero] = args.target_tensor[zero]*2 + args.target_tensor[one]*3
        result[one] = args.target_tensor[zero]*5 + args.target_tensor[one]*7
        return result

    def _unitary_(self):
        return np.array([[2, 3], [5, 7]])

    def __pow__(self, factor):
        return self

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return (u'cirq.ops.controlled_gate_test.'
                u'GateAllocatingNewSpaceForResult()')


@pytest.mark.parametrize(u'gate', [
    cirq.X,
    cirq.X**0.5,
    cirq.Rx(np.pi),
    cirq.Rx(np.pi / 2),
    cirq.Z,
    cirq.H,
    cirq.CNOT,
    cirq.SWAP,
    cirq.CCZ,
    cirq.ControlledGate(cirq.ControlledGate(cirq.CCZ)),
    GateUsingWorkspaceForApplyUnitary(),
    GateAllocatingNewSpaceForResult(),
])
def test_controlled_gate_is_consistent(gate):
    cgate = cirq.ControlledGate(gate)
    cirq.testing.assert_implements_consistent_protocols(cgate)


def test_pow_inverse():
    assert cirq.inverse(CRestricted, None) is None
    assert cirq.pow(CRestricted, 1.5, None) is None
    assert cirq.pow(CY, 1.5) == cirq.ControlledGate(cirq.Y**1.5)
    assert cirq.inverse(CY) == CY**-1 == CY


def test_extrapolatable_effect():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    assert cirq.ControlledGate(cirq.Z)**0.5 == cirq.ControlledGate(cirq.Z**0.5)

    assert (cirq.ControlledGate(cirq.Z).on(a, b)**0.5 ==
            cirq.ControlledGate(cirq.Z**0.5).on(a, b))


def test_reversible():
    assert (cirq.inverse(cirq.ControlledGate(cirq.S)) ==
            cirq.ControlledGate(cirq.S**-1))


class UnphaseableGate(cirq.SingleQubitGate):
    pass


def test_parameterizable():
    a = cirq.Symbol(u'a')
    cz = cirq.ControlledGate(cirq.Y)
    cza = cirq.ControlledGate(cirq.YPowGate(exponent=a))
    assert cirq.is_parameterized(cza)
    assert not cirq.is_parameterized(cz)
    assert cirq.resolve_parameters(cza, cirq.ParamResolver({u'a': 1})) == cz


def test_circuit_diagram_info():
    assert cirq.circuit_diagram_info(CY) == cirq.CircuitDiagramInfo(
        wire_symbols=(u'@', u'Y'),
        exponent=1)

    assert cirq.circuit_diagram_info(cirq.ControlledGate(cirq.Y**0.5)
                                     ) == cirq.CircuitDiagramInfo(
        wire_symbols=(u'@', u'Y'),
        exponent=0.5)

    assert cirq.circuit_diagram_info(cirq.ControlledGate(cirq.S)
                                     ) == cirq.CircuitDiagramInfo(
        wire_symbols=(u'@', u'S'),
        exponent=1)

    class UndiagrammableGate(cirq.Gate):
        pass

    assert cirq.circuit_diagram_info(cirq.ControlledGate(UndiagrammableGate()),
                                     default=None) is None


def test_bounded_effect():
    assert cirq.trace_distance_bound(CY**0.001) < 0.01


def test_repr():
    assert repr(
        cirq.ControlledGate(cirq.Z)) == u'cirq.ControlledGate(sub_gate=cirq.Z)'


def test_str():
    assert unicode(cirq.ControlledGate(cirq.X)) == u'CX'
    assert unicode(cirq.ControlledGate(cirq.Z)) == u'CZ'
    assert unicode(cirq.ControlledGate(cirq.S)) == u'CS'
    assert unicode(cirq.ControlledGate(cirq.Z**0.125)) == u'CZ**0.125'
    assert unicode(cirq.ControlledGate(cirq.ControlledGate(cirq.S))) == u'CCS'
