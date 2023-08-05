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


class ReturnsExponent(object):
    def __pow__(self, exponent):
        return exponent


@pytest.mark.parametrize(u'val', (
    NoMethod(),
    u'text',
    object(),
    ReturnsNotImplemented(),
))
def test_powerless(val):
    assert cirq.pow(val, 5, None) is None
    assert cirq.pow(val, 2, NotImplemented) is NotImplemented

    # Don't assume X**1 == X if X doesn't define __pow__.
    assert cirq.pow(val, 1, None) is None


def test_pow_error():
    with pytest.raises(TypeError, match=u"returned NotImplemented"):
        _ = cirq.pow(ReturnsNotImplemented(), 3)
    with pytest.raises(TypeError, match=u"no __pow__ method"):
        _ = cirq.pow(NoMethod(), 3)


@pytest.mark.parametrize(u'val,exponent,out', (
    (ReturnsExponent(), 2, 2),
    (1, 2, 1),
    (2, 3, 8),
))
def test_pow_with_result(val, exponent, out):
    assert (cirq.pow(val, exponent) ==
            cirq.pow(val, exponent, default=None) ==
            val**exponent ==
            out)
