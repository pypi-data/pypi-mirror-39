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


class BasicC(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


BasicC = cirq.value_equality(BasicC)

class BasicD(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


BasicD = cirq.value_equality(BasicD)

class BasicCa(BasicC):
    pass


class BasicCb(BasicC):
    pass


def test_value_equality_basic():

    # Lookup works across equivalent types.
    v = {BasicC(1): 4, BasicCa(2): 5}
    assert v[BasicCa(1)] == v[BasicC(1)] == 4
    assert v[BasicCa(2)] == 5

    # Equality works as expected.
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(BasicC(1), BasicC(1), BasicCa(1), BasicCb(1))
    eq.add_equality_group(BasicD(1))
    eq.add_equality_group(BasicC(2))
    eq.add_equality_group(BasicCa(3))


class UnhashableC(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


UnhashableC = cirq.value_equality(unhashable=True)(UnhashableC)

class UnhashableD(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


UnhashableD = cirq.value_equality(unhashable=True)(UnhashableD)

class UnhashableCa(UnhashableC):
    pass


class UnhashableCb(UnhashableC):
    pass


def test_value_equality_unhashable():
    # Not possible to use as a dictionary key.
    with pytest.raises(TypeError, match=u'unhashable'):
        _ = {UnhashableC(1): 4}

    # Equality works as expected.
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(UnhashableC(1),
                          UnhashableC(1),
                          UnhashableCa(1),
                          UnhashableCb(1))
    eq.add_equality_group(UnhashableC(2))
    eq.add_equality_group(UnhashableD(1))


class DistinctC(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


DistinctC = cirq.value_equality(distinct_child_types=True)(DistinctC)

class DistinctD(object):
    def __init__(self, x):
        self.x = x

    def _value_equality_values_(self):
        return self.x


DistinctD = cirq.value_equality(distinct_child_types=True)(DistinctD)

class DistinctCa(DistinctC):
    pass


class DistinctCb(DistinctC):
    pass


def test_value_equality_distinct_child_types():
    # Lookup is distinct across child types.
    v = {DistinctC(1): 4, DistinctCa(1): 5, DistinctCb(1): 6}
    assert v[DistinctC(1)] == 4
    assert v[DistinctCa(1)] == 5
    assert v[DistinctCb(1)] == 6

    # Equality works as expected.
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(DistinctC(1), DistinctC(1))
    eq.add_equality_group(DistinctCa(1), DistinctCa(1))
    eq.add_equality_group(DistinctCb(1), DistinctCb(1))
    eq.add_equality_group(DistinctC(2))
    eq.add_equality_group(DistinctD(1))


def test_value_equality_forgot_method():
    with pytest.raises(TypeError, match=u'_value_equality_values_'):
        class _(object):
            pass
        _ = cirq.value_equality(_)

       