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
import numpy as np
import pytest

import cirq


def test_external():
    for t in [u'a', 1j]:
        cirq.testing.assert_equivalent_repr(t)
        cirq.testing.assert_equivalent_repr(t, setup_code=u'')

    cirq.testing.assert_equivalent_repr(
        np.array([5]),
        setup_code=u'from numpy import array')

    with pytest.raises(AssertionError, match=u'not defined'):
        cirq.testing.assert_equivalent_repr(
            np.array([5]))


def test_custom_class_repr():
    class CustomRepr(object):
        # coverage: ignore

        setup_code = u"""class CustomRepr:
            def __init__(self, eq_val):
                self.eq_val = eq_val
            def __pow__(self, exponent):
                return self
        """

        def __init__(self, eq_val, repr_str):
            self.eq_val = eq_val
            self.repr_str = repr_str

        def __eq__(self, other):
            return self.eq_val == getattr(other, u'eq_val', None)

        def __ne__(self, other):
            return not self == other

        def __repr__(self):
            return self.repr_str

    cirq.testing.assert_equivalent_repr(
        CustomRepr(u'b', u"CustomRepr('b')"),
        setup_code=CustomRepr.setup_code)
    cirq.testing.assert_equivalent_repr(
        CustomRepr(u'a', u"CustomRepr('a')"),
        setup_code=CustomRepr.setup_code)

    # Non-equal values.
    with pytest.raises(AssertionError, match=ur'eval\(repr\(value\)\): a'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(u'a', u"'a'"))
    with pytest.raises(AssertionError, match=ur'eval\(repr\(value\)\): 1'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(u'a', u"1"))

    # Single failure out of many.
    with pytest.raises(AssertionError, match=ur'eval\(repr\(value\)\): a'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(u'a', u"'a'"))

    # Syntax errors.
    with pytest.raises(AssertionError, match=u'SyntaxError'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(u'a', u"("))
    with pytest.raises(AssertionError, match=u'SyntaxError'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(u'a', u"return 1"))

    # Not dottable.
    with pytest.raises(AssertionError, match=ur'dottable'):
        cirq.testing.assert_equivalent_repr(
            CustomRepr(5, u"CustomRepr(5)**1"),
            setup_code=CustomRepr.setup_code)



def test_imports_cirq_by_default():
    cirq.testing.assert_equivalent_repr(cirq.NamedQubit(u'a'))
