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


def test_phase_by():
    class NoMethod(object):
        pass

    class ReturnsNotImplemented(object):
        def _phase_by_(self, phase_turns, qubit_on):
            return NotImplemented

    class PhaseIsAddition(object):
        def __init__(self, num_qubits):
            self.phase = [0] * num_qubits
            self.num_qubits = num_qubits
        def _phase_by_(self, phase_turns, qubit_on):
            if qubit_on >= self.num_qubits:
                return self
            self.phase[qubit_on] += phase_turns
            return self


    n = NoMethod()
    rin = ReturnsNotImplemented()

    # Without default

    with pytest.raises(TypeError, match=u'no _phase_by_ method'):
        _ = cirq.phase_by(n, 1, 0)
    with pytest.raises(TypeError, match=u'returned NotImplemented'):
        _ = cirq.phase_by(rin, 1, 0)

    # With default
    assert cirq.phase_by(n, 1, 0, default=None) == None
    assert cirq.phase_by(rin, 1, 0, default=None) == None

    test = PhaseIsAddition(3)
    assert test.phase == [0, 0, 0]
    test = cirq.phase_by(test, 0.25, 0)
    assert test.phase == [0.25, 0, 0]
    test = cirq.phase_by(test, 0.25, 0)
    assert test.phase == [0.50, 0, 0]
    test = cirq.phase_by(test, 0.40, 1)
    assert test.phase == [0.50, 0.40, 0]
    test = cirq.phase_by(test, 0.40, 4)
    assert test.phase == [0.50, 0.40, 0]

