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


def test_parameterized_value_init():
    assert cirq.Symbol(u'a').name == u'a'
    assert cirq.Symbol(u'b').name == u'b'


def test_string_representation():
    assert unicode(cirq.Symbol(u'a1')) == u'a1'
    assert unicode(cirq.Symbol(u'_b23_')) == u'_b23_'
    assert unicode(cirq.Symbol(u'1a')) == u'Symbol("1a")'
    assert unicode(cirq.Symbol(u'&%#')) == u'Symbol("&%#")'
    assert unicode(cirq.Symbol(u'')) == u'Symbol("")'


@cirq.testing.only_test_in_python3
def test_repr():
    assert repr(cirq.Symbol(u'a1')) == u"cirq.Symbol('a1')"
    assert repr(cirq.Symbol(u'_b23_')) == u"cirq.Symbol('_b23_')"
    assert repr(cirq.Symbol(u'1a')) == u"cirq.Symbol('1a')"
    assert repr(cirq.Symbol(u'&%#')) == u"cirq.Symbol('&%#')"
    assert repr(cirq.Symbol(u'')) == u"cirq.Symbol('')"


def test_parameterized_value_eq():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(cirq.Symbol(u'a'))
    eq.make_equality_group(lambda: cirq.Symbol(u'rr'))


def test_identity_operations():
    s = cirq.Symbol(u's')
    assert s == s * 1 == 1 * s == 1.0 * s * 1.0
    assert s == s + 0 == 0 + s == 0.0 + s + 0.0

    with pytest.raises(TypeError):
        _ = s + s
    with pytest.raises(TypeError):
        _ = s + 1
    with pytest.raises(TypeError):
        _ = 1 + s
    with pytest.raises(TypeError):
        _ = s * s
    with pytest.raises(TypeError):
        _ = s * 2
    with pytest.raises(TypeError):
        _ = 2 * s
