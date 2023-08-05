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
from typing import Optional, Union, overload, TYPE_CHECKING

import numpy as np

from cirq import protocols, value
from cirq.ops import common_gates
from cirq.type_workarounds import NotImplementedType

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Tuple


class Pauli(object):
    u"""Represents the X, Y, or Z axis of the Bloch sphere."""
    X = None  # type: Pauli
    Y = None  # type: Pauli
    Z = None  # type: Pauli
    XYZ = None  # type: Tuple[Pauli, Pauli, Pauli]

    def __init__(self, **_3to2kwargs):
        _name = _3to2kwargs['_name']; del _3to2kwargs['_name']
        _index = _3to2kwargs['_index']; del _3to2kwargs['_index']
        self._index = _index
        self._name = _name

    def commutes_with(self, other):
        return self is other

    def third(self, second):
        return Pauli.XYZ[(-self._index - second._index) % 3]

    def difference(self, second):
        return (self._index - second._index + 1) % 3 - 1

    def _unitary_(self):
        if self._name == u'X':
            return protocols.unitary(common_gates.X)
        elif self._name == u'Y':
            return protocols.unitary(common_gates.Y)
        else:
            return protocols.unitary(common_gates.Z)

    def _apply_unitary_(self, args
                        ):
        if self._name == u'X':
            return protocols.apply_unitary(common_gates.X, args)
        elif self._name == u'Y':
            return protocols.apply_unitary(common_gates.Y, args)
        else:
            return protocols.apply_unitary(common_gates.Z, args)

    def _value_equality_values_(self):
        return self._index

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self._index - other._index) % 3 == 1

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (other._index - self._index) % 3 == 1

    def __add__(self, shift):
        return Pauli.XYZ[(self._index + shift) % 3]

    # pylint: disable=function-redefined
    @overload
    def __sub__(self, other): pass
    @overload
    def __sub__(self, shift): pass

    def __sub__(self, other_or_shift
                ):
        if isinstance(other_or_shift, int):
            return self + -other_or_shift
        else:
            return self.difference(other_or_shift)
    # pylint: enable=function-redefined

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self._name

    def __repr__(self):
        return u'cirq.Pauli.{!s}'.format(self)


Pauli = value.value_equality(Pauli)

Pauli.X = Pauli(_index=0, _name=u'X')
Pauli.Y = Pauli(_index=1, _name=u'Y')
Pauli.Z = Pauli(_index=2, _name=u'Z')
Pauli.XYZ = (Pauli.X, Pauli.Y, Pauli.Z)
