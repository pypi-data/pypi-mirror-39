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
from typing import cast

from cirq import circuits, ops, protocols, value
from cirq.contrib.qcircuit.qcircuit_diagrammable import (
    QCircuitDiagrammable,
    known_qcircuit_operation_symbols,
    _TextToQCircuitDiagrammable,
    _FallbackQCircuitGate,
)


class _QCircuitQubit(ops.QubitId):
    def __init__(self, sub):
        self.sub = sub

    def _comparison_key(self):
        return self.sub

    def __repr__(self):
        return u'_QCircuitQubit({!r})'.format(self.sub)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        # TODO: If qubit name ends with digits, turn them into subscripts.
        return u'\\lstick{\\text{' + unicode(self.sub) + u'}}&'

    def _value_equality_values_(self):
        return self.sub


_QCircuitQubit = value.value_equality(_QCircuitQubit)

class _QCircuitOperation(ops.Operation):
    def __init__(self,
                 sub_operation,
                 diagrammable):
        self.sub_operation = sub_operation
        self.diagrammable = diagrammable

    def _circuit_diagram_info_(self,
                               args
                               ):
        return self.diagrammable.qcircuit_diagram_info(args)

    @property
    def qubits(self):
        return self.sub_operation.qubits

    def with_qubits(self, *new_qubits):
        return _QCircuitOperation(
            self.sub_operation.with_qubits(*new_qubits),
            self.diagrammable)


def _render(diagram):
    w = diagram.width()
    h = diagram.height()

    qwx = set([(x, y + 1)
           for x, y1, y2, _ in diagram.vertical_lines
           for y in xrange(y1, y2)])

    qw = set([(x, y)
          for y, x1, x2, _ in diagram.horizontal_lines
          for x in xrange(x1, x2)])

    diagram2 = circuits.TextDiagramDrawer()
    for y in xrange(h):
        for x in xrange(max(0, w - 1)):
            key = (x, y)
            diagram_text = diagram.entries.get(key)
            v = u'&' + (diagram_text.text if diagram_text else  u'') + u' '
            diagram2.write(2*x + 1, y, v)
            post1 = u'\\qw' if key in qw else u''
            post2 = u'\\qwx' if key in qwx else u''
            diagram2.write(2*x + 2, y, post1 + post2)
        diagram2.write(2*w - 1, y, u'&\\qw\\\\')
    grid = diagram2.render(horizontal_spacing=0, vertical_spacing=0)

    output = u'\Qcircuit @R=1em @C=0.75em {\n \\\\\n' + grid + u'\n \\\\\n}'

    return output


def _wrap_operation(op):
    new_qubits = [_QCircuitQubit(e) for e in op.qubits]
    diagrammable = known_qcircuit_operation_symbols(op)
    if diagrammable is None:
        info = protocols.circuit_diagram_info(op, default=None)
        if info is not None:
            diagrammable = _TextToQCircuitDiagrammable(
                cast(protocols.SupportsCircuitDiagramInfo, op))
        elif isinstance(op, ops.GateOperation):
            diagrammable = _FallbackQCircuitGate(op.gate)
        else:
            diagrammable = _FallbackQCircuitGate(op)
    return _QCircuitOperation(op, diagrammable).with_qubits(*new_qubits)


def _wrap_moment(moment):
    return circuits.Moment(_wrap_operation(op)
                           for op in moment.operations)


def _wrap_circuit(circuit):
    return circuits.Circuit(_wrap_moment(moment) for moment in circuit)


def circuit_to_latex_using_qcircuit(
        circuit,
        qubit_order = ops.QubitOrder.DEFAULT):
    u"""Returns a QCircuit-based latex diagram of the given circuit.

    Args:
        circuit: The circuit to represent in latex.
        qubit_order: Determines the order of qubit wires in the diagram.

    Returns:
        Latex code for the diagram.
    """
    qcircuit = _wrap_circuit(circuit)

    # Note: can't be a lambda because we need the type hint.
    def get_sub(q):
        return q.sub

    diagram = qcircuit.to_text_diagram_drawer(
        qubit_name_suffix=u'',
        qubit_order=ops.QubitOrder.as_qubit_order(qubit_order).map(
            internalize=get_sub, externalize=_QCircuitQubit))
    return _render(diagram)
