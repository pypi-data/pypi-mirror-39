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
import pytest

import cirq


def test_circuit_diagram_info_value_wrapping():
    single_info = cirq.CircuitDiagramInfo((u'Single',))

    class ReturnInfo(object):
        def _circuit_diagram_info_(self, args):
            return single_info

    class ReturnTuple(object):
        def _circuit_diagram_info_(self, args):
            return u'Single',

    class ReturnList(object):
        def _circuit_diagram_info_(self, args):
            return (u'Single' for _ in xrange(1))

    class ReturnGenerator(object):
        def _circuit_diagram_info_(self, args):
            return [u'Single']

    class ReturnString(object):
        def _circuit_diagram_info_(self, args):
            return u'Single'

    assert (cirq.circuit_diagram_info(ReturnInfo()) ==
            cirq.circuit_diagram_info(ReturnTuple()) ==
            cirq.circuit_diagram_info(ReturnString()) ==
            cirq.circuit_diagram_info(ReturnList()) ==
            cirq.circuit_diagram_info(ReturnGenerator()) ==
            single_info)

    double_info = cirq.CircuitDiagramInfo((u'Single', u'Double',))

    class ReturnDoubleInfo(object):
        def _circuit_diagram_info_(self, args):
            return double_info

    class ReturnDoubleTuple(object):
        def _circuit_diagram_info_(self, args):
            return u'Single', u'Double'

    assert (cirq.circuit_diagram_info(ReturnDoubleInfo()) ==
            cirq.circuit_diagram_info(ReturnDoubleTuple()) ==
            double_info)


def test_circuit_diagram_info_validate():
    with pytest.raises(ValueError):
        _ = cirq.CircuitDiagramInfo(u'X')


def test_circuit_diagram_info_repr():
    cirq.testing.assert_equivalent_repr(
        cirq.CircuitDiagramInfo((u'X', u'Y'), 2))


def test_circuit_diagram_info_eq():
    eq = cirq.testing.EqualsTester()
    eq.make_equality_group(lambda: cirq.CircuitDiagramInfo((u'X',)))
    eq.add_equality_group(cirq.CircuitDiagramInfo((u'X', u'Y')),
                          cirq.CircuitDiagramInfo((u'X', u'Y'), 1))
    eq.add_equality_group(cirq.CircuitDiagramInfo((u'Z',), 2))
    eq.add_equality_group(cirq.CircuitDiagramInfo((u'Z', u'Z'), 2))
    eq.add_equality_group(cirq.CircuitDiagramInfo((u'Z',), 3))


def test_circuit_diagram_info_pass_fail():
    class C(object):
        pass

    class D(object):
        def _circuit_diagram_info_(self, args):
            return NotImplemented

    class E(object):
        def _circuit_diagram_info_(self, args):
            return cirq.CircuitDiagramInfo((u'X',))

    assert cirq.circuit_diagram_info(C(), default=None) is None
    assert cirq.circuit_diagram_info(D(), default=None) is None
    assert cirq.circuit_diagram_info(
        E(), default=None) == cirq.CircuitDiagramInfo((u'X',))

    with pytest.raises(TypeError, match=u'no _circuit_diagram_info'):
        _ = cirq.circuit_diagram_info(C())
    with pytest.raises(TypeError, match=u'returned NotImplemented'):
        _ = cirq.circuit_diagram_info(D())
    assert cirq.circuit_diagram_info(E()) == cirq.CircuitDiagramInfo((u'X',))


def test_circuit_diagram_info_args_eq():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT)
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs(
        known_qubits=None,
        known_qubit_count=None,
        use_unicode_characters=False,
        precision=None,
        qubit_map=None))
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs(
        known_qubits=None,
        known_qubit_count=None,
        use_unicode_characters=True,
        precision=None,
        qubit_map=None))
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs(
        known_qubits=cirq.LineQubit.range(3),
        known_qubit_count=3,
        use_unicode_characters=False,
        precision=None,
        qubit_map=None))
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs(
        known_qubits=cirq.LineQubit.range(2),
        known_qubit_count=2,
        use_unicode_characters=False,
        precision=None,
        qubit_map=None))
    eq.add_equality_group(cirq.CircuitDiagramInfoArgs(
        known_qubits=cirq.LineQubit.range(2),
        known_qubit_count=2,
        use_unicode_characters=False,
        precision=None,
        qubit_map={cirq.LineQubit(0): 5, cirq.LineQubit(1): 7}))


def test_circuit_diagram_info_args_repr():
    cirq.testing.assert_equivalent_repr(
        cirq.CircuitDiagramInfoArgs(
            known_qubits=cirq.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=True,
            precision=5,
            qubit_map={cirq.LineQubit(0): 5, cirq.LineQubit(1): 7}))
