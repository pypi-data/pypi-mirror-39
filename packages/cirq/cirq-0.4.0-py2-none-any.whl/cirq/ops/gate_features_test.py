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


def test_single_qubit_gate_validate_args():
    class Dummy(cirq.SingleQubitGate):
        def matrix(self):
            pass

    g = Dummy()
    q1 = cirq.NamedQubit(u'q1')
    q2 = cirq.NamedQubit(u'q2')

    g.validate_args([q1])
    g.validate_args([q2])
    with pytest.raises(ValueError):
        g.validate_args([])
    with pytest.raises(ValueError):
        g.validate_args([q1, q2])


def test_two_qubit_gate_is_abstract_can_implement():
    class Included(cirq.TwoQubitGate):
        def matrix(self):
            pass

    assert isinstance(Included(),
                      cirq.TwoQubitGate)


def test_two_qubit_gate_validate_pass():
    class Dummy(cirq.TwoQubitGate):
        def matrix(self):
            pass

    g = Dummy()
    q1 = cirq.NamedQubit(u'q1')
    q2 = cirq.NamedQubit(u'q2')
    q3 = cirq.NamedQubit(u'q3')

    g.validate_args([q1, q2])
    g.validate_args([q2, q3])
    g.validate_args([q3, q2])


def test_two_qubit_gate_validate_wrong_number():
    class Dummy(cirq.TwoQubitGate):
        def matrix(self):
            pass

    g = Dummy()
    q1 = cirq.NamedQubit(u'q1')
    q2 = cirq.NamedQubit(u'q2')
    q3 = cirq.NamedQubit(u'q3')

    with pytest.raises(ValueError):
        g.validate_args([])
    with pytest.raises(ValueError):
        g.validate_args([q1])
    with pytest.raises(ValueError):
        g.validate_args([q1, q2, q3])


def test_three_qubit_gate_validate():
    class Dummy(cirq.ThreeQubitGate):
        def matrix(self):
            pass

    g = Dummy()
    a, b, c, d = cirq.LineQubit.range(4)

    g.validate_args([a, b, c])
    with pytest.raises(ValueError):
        g.validate_args([])
    with pytest.raises(ValueError):
        g.validate_args([a])
    with pytest.raises(ValueError):
        g.validate_args([a, b])
    with pytest.raises(ValueError):
        g.validate_args([a, b, c, d])


def test_on_each():
    class CustomGate(cirq.SingleQubitGate):
        pass
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    c = CustomGate()

    assert c.on_each([]) == []
    assert c.on_each([a]) == [c(a)]
    assert c.on_each([a, b]) == [c(a), c(b)]
    assert c.on_each([b, a]) == [c(b), c(a)]


def test_qasm_output_args_validate():
    args = cirq.QasmArgs(version=u'2.0')
    args.validate_version(u'2.0')

    with pytest.raises(ValueError):
        args.validate_version(u'2.1')


def test_qasm_output_args_format():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    m_a = cirq.MeasurementGate(u'meas_a')(a)
    m_b = cirq.MeasurementGate(u'meas_b')(b)
    args = cirq.QasmArgs(
                    precision=4,
                    version=u'2.0',
                    qubit_id_map={a: u'aaa[0]', b: u'bbb[0]'},
                    meas_key_id_map={u'meas_a': u'm_a', u'meas_b': u'm_b'})

    assert args.format(u'_{0}_', a) == u'_aaa[0]_'
    assert args.format(u'_{0}_', b) == u'_bbb[0]_'

    assert args.format(u'_{0:meas}_', m_a.gate.key) == u'_m_a_'
    assert args.format(u'_{0:meas}_', m_b.gate.key) == u'_m_b_'

    assert args.format(u'_{0}_', 89.1234567) == u'_89.1235_'
    assert args.format(u'_{0}_', 1.23) == u'_1.23_'

    assert args.format(u'_{0:half_turns}_', 89.1234567) == u'_pi*89.1235_'
    assert args.format(u'_{0:half_turns}_', 1.23) == u'_pi*1.23_'

    assert args.format(u'_{0}_', u'other') == u'_other_'
