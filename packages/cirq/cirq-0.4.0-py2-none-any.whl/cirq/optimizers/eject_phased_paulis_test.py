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
from typing import Iterable

import cirq


def assert_optimizes(before,
                     expected,
                     compare_unitaries = True):
    opt = cirq.EjectPhasedPaulis()

    circuit = before.copy()
    opt.optimize_circuit(circuit)

    # They should have equivalent effects.
    if compare_unitaries:
        cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            circuit, expected, 1e-8)

    # And match the expected circuit.
    assert circuit == expected, (
        u"Circuit wasn't optimized as expected.\n"
        u"INPUT:\n"
        u"{}\n"
        u"\n"
        u"EXPECTED OUTPUT:\n"
        u"{}\n"
        u"\n"
        u"ACTUAL OUTPUT:\n"
        u"{}\n"
        u"\n"
        u"EXPECTED OUTPUT (detailed):\n"
        u"{!r}\n"
        u"\n"
        u"ACTUAL OUTPUT (detailed):\n"
        u"{!r}").format(before, expected, circuit, expected, circuit)

    # And it should be idempotent.
    opt.optimize_circuit(circuit)
    assert circuit == expected


def quick_circuit(*moments):
    return cirq.Circuit([cirq.Moment(cirq.flatten_op_tree(m)) for m in moments])


def test_absorbs_z():
    q = cirq.NamedQubit(u'q')

    # Full Z.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(q)],
            [cirq.Z(q)],
        ),
        expected=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.625).on(q)],
            [],
        ))

    # Partial Z.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(q)],
            [cirq.S(q)],
        ),
        expected=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.375).on(q)],
            [],
        ))

    # Multiple Zs.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(q)],
            [cirq.S(q)],
            [cirq.T(q)**-1],
        ),
        expected=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [],
            [],
        ))


def test_crosses_czs():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    # Full CZ.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [cirq.CZ(a, b)],
        ),
        expected=quick_circuit(
            [cirq.Z(b)],
            [cirq.CZ(a, b)],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
        ))
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(a)],
            [cirq.CZ(b, a)],
        ),
        expected=quick_circuit(
            [cirq.Z(b)],
            [cirq.CZ(a, b)],
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(a)],
        ))

    # Partial CZ.
    assert_optimizes(
        before=quick_circuit(
            [cirq.X(a)],
            [cirq.CZ(a, b)**0.25],
        ),
        expected=quick_circuit(
            [cirq.Z(b)**0.25],
            [cirq.CZ(a, b)**-0.25],
            [cirq.X(a)],
        ))

    # Double cross.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(a)],
            [cirq.PhasedXPowGate(phase_exponent=0.375).on(b)],
            [cirq.CZ(a, b)**0.25],
        ),
        expected=quick_circuit(
            [],
            [],
            [cirq.CZ(a, b)**0.25],
            [cirq.PhasedXPowGate(phase_exponent=0.5).on(b),
             cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
        ))


def test_toggles_measurements():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    # Single.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [cirq.measure(a, b)],
        ),
        expected=quick_circuit(
            [],
            [cirq.measure(a, b, invert_mask=(True,))],
        ))
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(b)],
            [cirq.measure(a, b)],
        ),
        expected=quick_circuit(
            [],
            [cirq.measure(a, b, invert_mask=(False, True))],
        ))

    # Multiple.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(b)],
            [cirq.measure(a, b)],
        ),
        expected=quick_circuit(
            [],
            [],
            [cirq.measure(a, b, invert_mask=(True, True))],
        ))

    # Xmon.
    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [cirq.measure(a, b, key=u't')],
        ),
        expected=quick_circuit(
            [],
            [cirq.measure(a, b, invert_mask=(True,), key=u't')],
        ))


def test_cancels_other_full_w():
    q = cirq.NamedQubit(u'q')

    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ),
        expected=quick_circuit(
            [],
            [],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.125).on(q)],
        ),
        expected=quick_circuit(
            [],
            [cirq.Z(q)**-0.25],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ),
        expected=quick_circuit(
            [],
            [cirq.Z(q)**0.5],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [cirq.X(q)],
        ),
        expected=quick_circuit(
            [],
            [cirq.Z(q)**-0.5],
        ))


def test_phases_partial_ws():
    q = cirq.NamedQubit(u'q')

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.25, exponent=0.5).on(q)],
        ),
        expected=quick_circuit(
            [],
            [cirq.PhasedXPowGate(phase_exponent=-0.25, exponent=0.5).on(q)],
            [cirq.X(q)],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [cirq.X(q)**0.5],
        ),
        expected=quick_circuit(
            [],
            [cirq.PhasedXPowGate(phase_exponent=0.5, exponent=0.5).on(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [cirq.PhasedXPowGate(phase_exponent=0.5, exponent=0.75).on(q)],
        ),
        expected=quick_circuit(
            [],
            [cirq.X(q)**0.75],
            [cirq.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(q)],
            [cirq.PhasedXPowGate(exponent=-0.25, phase_exponent=0.5).on(q)]
        ),
        expected=quick_circuit(
            [],
            [cirq.PhasedXPowGate(exponent=-0.25, phase_exponent=-0.5).on(q)],
            [cirq.X(q)],
        ))


def test_blocked_by_unknown_and_symbols():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(a)],
            [cirq.SWAP(a, b)],
            [cirq.X(a)],
        ),
        expected=quick_circuit(
            [cirq.X(a)],
            [cirq.SWAP(a, b)],
            [cirq.X(a)],
        ))

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(a)],
            [cirq.Z(a)**cirq.Symbol(u'z')],
            [cirq.X(a)],
        ),
        expected=quick_circuit(
            [cirq.X(a)],
            [cirq.Z(a)**cirq.Symbol(u'z')],
            [cirq.X(a)],
        ),
        compare_unitaries=False)

    assert_optimizes(
        before=quick_circuit(
            [cirq.X(a)],
            [cirq.CZ(a, b)**cirq.Symbol(u'z')],
            [cirq.X(a)],
        ),
        expected=quick_circuit(
            [cirq.X(a)],
            [cirq.CZ(a, b)**cirq.Symbol(u'z')],
            [cirq.X(a)],
        ),
        compare_unitaries=False)
