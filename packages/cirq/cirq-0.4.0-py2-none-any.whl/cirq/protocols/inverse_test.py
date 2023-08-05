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
    def __pow__(self, exponent):
        return NotImplemented


class ReturnsFive(object):
    def __pow__(self, exponent):
        return 5


class SelfInverse(object):
    def __pow__(self, exponent):
        return self


class ImplementsReversible(object):
    def __pow__(self, exponent):
        return 6 if exponent == -1 else NotImplemented


class IsIterable(object):
    def __iter__(self):
        yield 1
        yield 2


@pytest.mark.parametrize(u'val', (
    NoMethod(),
    u'text',
    object(),
    ReturnsNotImplemented(),
    [NoMethod(), 5],
))
def test_objects_with_no_inverse(val):
    with pytest.raises(TypeError, match=u"isn't invertible"):
        _ = cirq.inverse(val)
    assert cirq.inverse(val, None) is None
    assert cirq.inverse(val, NotImplemented) is NotImplemented
    assert cirq.inverse(val, 5) == 5


@pytest.mark.parametrize(u'val,inv', (
    (ReturnsFive(), 5),
    (ImplementsReversible(), 6),
    (SelfInverse(),)*2,
    (1, 1),
    (2, 0.5),
    (1j, -1j),
    ((), ()),
    ([], ()),
    ((2,), (0.5,)),
    ((1, 2), (0.5, 1)),
    ((2, (4, 8)), ((0.125, 0.25), 0.5)),
    ((2, [4, 8]), ((0.125, 0.25), 0.5)),
    (IsIterable(), (0.5, 1)),
))
def test_objects_with_inverse(val, inv):
    assert cirq.inverse(val) == inv
