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


class NoMethod(object):
    pass


class ReturnsNotImplemented(object):
    def _qasm_(self):
        return NotImplemented


class ReturnsText(object):
    def _qasm_(self):
        return u'text'


class ExpectsArgs(object):
    def _qasm_(self, args):
        return u'text'


class ExpectsArgsQubits(object):
    def _qasm_(self, args, qubits):
        return u'text'


def test_qasm():
    assert cirq.qasm(NoMethod(), default=None) is None
    assert cirq.qasm(NoMethod(), default=5) == 5
    assert cirq.qasm(ReturnsText()) == u'text'

    with pytest.raises(TypeError, match=u'no _qasm_ method'):
        _ = cirq.qasm(NoMethod())
    with pytest.raises(TypeError, match=u'returned NotImplemented or None'):
        _ = cirq.qasm(ReturnsNotImplemented())

    assert cirq.qasm(ExpectsArgs(), args=cirq.QasmArgs()) == u'text'
    assert cirq.qasm(ExpectsArgsQubits(),
                     args=cirq.QasmArgs(),
                     qubits=()) == u'text'
