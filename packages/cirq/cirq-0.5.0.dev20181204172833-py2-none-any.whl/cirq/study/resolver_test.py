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

u"""Tests for parameter resolvers."""

from __future__ import absolute_import
import itertools

import cirq


def test_value_of():
    r = cirq.ParamResolver({u'a': 0.5, u'b': 0.1})
    assert r.value_of(cirq.Symbol(u'a')) == 0.5
    assert r.value_of(0.5) == 0.5
    assert r.value_of(cirq.Symbol(u'b')) == 0.1
    assert r.value_of(0.3) == 0.3


def test_param_dict():
    r = cirq.ParamResolver({u'a': 0.5, u'b': 0.1})
    assert r.param_dict == {u'a': 0.5, u'b': 0.1}


def test_hash():
    a = cirq.ParamResolver({})
    b = cirq.ParamResolver({u'a': 0.0})
    c = cirq.ParamResolver({u'a': 0.1})
    d = cirq.ParamResolver({u'a': 0.0, u'b': 0.1})
    e = cirq.ParamResolver({u'a': 0.3, u'b': 0.1})
    f = cirq.ParamResolver({u'b': 0.1})
    g = cirq.ParamResolver({u'c': 0.1})
    resolvers = [a, b, c, d, e, f, g]
    for r in resolvers:
        assert isinstance(hash(r), int)
    for r1, r2 in itertools.combinations(resolvers, 2):
        assert hash(r1) != hash(r2)


def test_equals():
    et = cirq.testing.EqualsTester()
    et.add_equality_group(cirq.ParamResolver({}))
    et.add_equality_group(cirq.ParamResolver({u'a': 0.0}))
    et.add_equality_group(cirq.ParamResolver({u'a': 0.1}))
    et.add_equality_group(cirq.ParamResolver({u'a': 0.0, u'b': 0.1}))
    et.add_equality_group(cirq.ParamResolver({u'a': 0.3, u'b': 0.1}))
    et.add_equality_group(cirq.ParamResolver({u'b': 0.1}))
    et.add_equality_group(cirq.ParamResolver({u'c': 0.1}))