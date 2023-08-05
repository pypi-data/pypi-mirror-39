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
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Dict


def assert_equivalent_repr(
        value, **_3to2kwargs):
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  u'import cirq\nimport numpy as np'
    u"""Checks that eval(repr(v)) == v.

    Args:
        value: A value whose repr should be evaluatable python
            code that produces an equivalent value.
        setup_code: Code that must be executed before the repr can be evaluated.
            Ideally this should just be a series of 'import' lines.
    """

    global_vals = {}  # type: Dict[str, Any]
    local_vals = {}  # type: Dict[str, Any]
    exec(setup_code, global_vals, local_vals)

    try:
        eval_repr_value = eval(repr(value), global_vals, local_vals)
    except Exception, ex:
        raise AssertionError(
            u'eval(repr(value)) raised an exception.\n'
            u'\n'
            u'setup_code={}\n'
            u'type(value): {}\n'
            u'value={!r}\n'
            u'error={!r}'.format(setup_code, type(value), value, ex))

    assert eval_repr_value == value, (
        u"The repr of a value of type {} didn't evaluate to something equal "
        u"to the value.\n"
        u'eval(repr(value)) != value\n'
        u'\n'
        u'value: {}\n'
        u'repr(value): {!r}\n'
        u'eval(repr(value)): {}\n'
        u'repr(eval(repr(value))): {!r}\n'
        u'\n'
        u'type(value): {}\n'
        u'type(eval(repr(value))): {!r}\n'
        u'\n'
        u'setup_code:\n{}\n'
    ).format(type(value),
             value,
             repr(value),
             eval_repr_value,
             repr(eval_repr_value),
             type(value),
             type(eval_repr_value),
             u'    ' + setup_code.replace(u'\n', u'\n    '))

    try:
        a = eval(u'{!r}.__class__'.format(value), global_vals, local_vals)
    except (AttributeError, SyntaxError):
        raise AssertionError(
            u"The repr of a value of type {} wasn't 'dottable'.\n"
            u"{!r}.XXX must be equivalent to ({!r}).XXX, "
            u"but it raised an error instead.".format(
                type(value), value, value))

    b = eval(u'({!r}).__class__'.format(value), global_vals, local_vals)
    assert a == b, (
        u"The repr of a value of type {} wasn't 'dottable'.\n"
        u"{!r}.XXX must be equivalent to ({!r}).XXX, "
        u"but it wasn't.".format(type(value), value, value))
