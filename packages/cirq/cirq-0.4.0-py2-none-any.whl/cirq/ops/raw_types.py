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

u"""Basic types defining qubits, gates, and operations."""

from __future__ import absolute_import
from typing import Sequence, Tuple, TYPE_CHECKING, Callable, TypeVar, Any

import abc

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from cirq.ops import gate_operation


class QubitId(object):
    __metaclass__ = abc.ABCMeta
    u"""Identifies a qubit. Child classes implement specific types of qubits.

    The main criteria that a "qubit id" must satisfy is *comparability*. Child
    classes meet this criteria by implementing the `_comparison_key` method. For
    example, `cirq.LineQubit`'s `_comparison_key` method returns `self.x`. This
    ensures that line qubits with the same `x` are equal, and that line qubits
    will be sorted ascending by `x`. `QubitId` implements all equality,
    comparison, and hashing methods via `_comparison_key`.
    """

    @abc.abstractmethod
    def _comparison_key(self):
        u"""Returns a value used to sort and compare this qubit with others.

        By default, qubits of differing type are sorted ascending according to
        their type name. Qubits of the same type are then sorted using their
        comparison key.
        """
        pass

    def _cmp_tuple(self):
        return type(self).__name__, repr(type(self)), self._comparison_key()

    def __hash__(self):
        return hash((QubitId, self._comparison_key()))

    def __eq__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() == other._cmp_tuple()

    def __ne__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() != other._cmp_tuple()

    def __lt__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() < other._cmp_tuple()

    def __gt__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() > other._cmp_tuple()

    def __le__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() <= other._cmp_tuple()

    def __ge__(self, other):
        if not isinstance(other, QubitId):
            return NotImplemented
        return self._cmp_tuple() >= other._cmp_tuple()


class Gate(object):
    u"""An operation type that can be applied to a collection of qubits.

    Gates can be applied to qubits by calling their on() method with
    the qubits to be applied to supplied, or, alternatively, by simply
    calling the gate on the qubits.  In other words calling MyGate.on(q1, q2)
    to create an Operation on q1 and q2 is equivalent to MyGate(q1,q2).
    """

    # noinspection PyMethodMayBeStatic
    def validate_args(self, qubits):
        u"""Checks if this gate can be applied to the given qubits.

        Does no checks by default. Child classes can override.

        Args:
            qubits: The collection of qubits to potentially apply the gate to.

        Throws:
            ValueError: The gate can't be applied to the qubits.
        """
        pass

    def on(self, *qubits):
        u"""Returns an application of this gate to the given qubits.

        Args:
            *qubits: The collection of qubits to potentially apply the gate to.
        """
        # Avoids circular import.
        from cirq.ops import gate_operation

        if len(qubits) == 0:
            raise ValueError(
                u"Applied a gate to an empty set of qubits. Gate: {}".format(
                    repr(self)))
        self.validate_args(qubits)
        return gate_operation.GateOperation(self, list(qubits))

    def __call__(self, *args, **kwargs):
        return self.on(*args, **kwargs)


TSelf_Operation = TypeVar(u'TSelf_Operation', bound=u'Operation')


class Operation(object):
    __metaclass__ = abc.ABCMeta
    u"""An effect applied to a collection of qubits.

    The most common kind of Operation is a GateOperation, which separates its
    effect into a qubit-independent Gate and the qubits it should be applied to.
    """

    @abc.abstractproperty
    def qubits(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def with_qubits(self,
                    *new_qubits):
        pass

    def transform_qubits(self,
                         func):
        u"""Returns the same operation, but with different qubits.

        Args:
            func: The function to use to turn each current qubit into a desired
                new qubit.

        Returns:
            The receiving operation but with qubits transformed by the given
                function.
        """
        return self.with_qubits(*(func(q) for q in self.qubits))
