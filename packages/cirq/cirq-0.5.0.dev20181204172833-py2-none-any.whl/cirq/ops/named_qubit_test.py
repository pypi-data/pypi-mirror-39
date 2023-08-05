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
import cirq
from cirq.ops.named_qubit import _pad_digits


def test_named_qubit_str():
    q = cirq.NamedQubit(u'a')
    assert q.name == u'a'
    assert unicode(q) == u'a'


# Python 2 gives a different repr due to unicode strings being prefixed with u.
@cirq.testing.only_test_in_python3
def test_named_qubit_repr():
    q = cirq.NamedQubit(u'a')
    assert repr(q) == u"cirq.NamedQubit('a')"


def test_named_qubit_order():
    order = cirq.testing.OrderTester()
    order.add_ascending(
        cirq.NamedQubit(u''),
        cirq.NamedQubit(u'1'),
        cirq.NamedQubit(u'a'),
        cirq.NamedQubit(u'a00000000'),
        cirq.NamedQubit(u'a00000000:8'),
        cirq.NamedQubit(u'a9'),
        cirq.NamedQubit(u'a09'),
        cirq.NamedQubit(u'a10'),
        cirq.NamedQubit(u'a11'),
        cirq.NamedQubit(u'aa'),
        cirq.NamedQubit(u'ab'),
        cirq.NamedQubit(u'b'),
    )
    order.add_ascending_equivalence_group(
        cirq.NamedQubit(u'c'),
        cirq.NamedQubit(u'c'),
    )


def test_pad_digits():
    assert _pad_digits(u'') == u''
    assert _pad_digits(u'a') == u'a'
    assert _pad_digits(u'a0') == u'a00000000:1'
    assert _pad_digits(u'a00') == u'a00000000:2'
    assert _pad_digits(u'a1bc23') == u'a00000001:1bc00000023:2'
    assert _pad_digits(u'a9') == u'a00000009:1'
    assert _pad_digits(u'a09') == u'a00000009:2'
    assert _pad_digits(u'a00000000:8') == u'a00000000:8:00000008:1'
