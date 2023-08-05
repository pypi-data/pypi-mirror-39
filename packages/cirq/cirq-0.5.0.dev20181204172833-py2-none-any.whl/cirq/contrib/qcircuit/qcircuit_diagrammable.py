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
from typing import Optional, Tuple, Any

import abc

from cirq import ops, protocols


class QCircuitDiagrammable(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def qcircuit_diagram_info(self, args
                              ):
        pass


def _escape_text_for_latex(text):
    escaped = (text
               .replace(u'\\', u'\\textbackslash{}')
               .replace(u'^', u'\\textasciicircum{}')
               .replace(u'~', u'\\textasciitilde{}')
               .replace(u'_', u'\\_')
               .replace(u'{', u'\\{')
               .replace(u'}', u'\\}')
               .replace(u'$', u'\\$')
               .replace(u'%', u'\\%')
               .replace(u'&', u'\\&')
               .replace(u'#', u'\\#'))
    return u'\\text{' + escaped + u'}'


class _HardcodedQCircuitSymbolsGate(QCircuitDiagrammable):
    def __init__(self, *symbols):
        self.symbols = symbols

    def qcircuit_diagram_info(self, args
                              ):
        return protocols.CircuitDiagramInfo(self.symbols)


def _get_multigate_parameters(gate,
                              args
                              ):
    if not isinstance(gate, ops.InterchangeableQubitsGate):
        return None
    if args.qubit_map is None or args.known_qubits is None:
        return None

    indices = [args.qubit_map[q] for q in args.known_qubits]
    min_index = min(indices)
    n_qubits = len(args.known_qubits)
    if sorted(indices) != range(min_index, min_index + n_qubits):
        return None
    return min_index, n_qubits


class _TextToQCircuitDiagrammable(QCircuitDiagrammable):
    def __init__(self, sub):
        self.sub = sub

    def qcircuit_diagram_info(self, args
                              ):
        info = protocols.circuit_diagram_info(self.sub, args)
        multigate_parameters = _get_multigate_parameters(self.sub, args)
        if multigate_parameters is not None:
            min_index, n_qubits = multigate_parameters
            name = _escape_text_for_latex(unicode(self.sub).rsplit(u'**', 1)[0])
            if info.exponent != 1:
                name += u'^{' + unicode(info.exponent) + u'}'
            box = u'\multigate{' + unicode(n_qubits - 1) + u'}{' + name + u'}'
            ghost = u'\ghost{' + name + u'}'
            assert args.qubit_map is not None
            assert args.known_qubits is not None
            symbols = tuple(box if (args.qubit_map[q] == min_index) else
                            ghost for q in args.known_qubits)
            return protocols.CircuitDiagramInfo(symbols,
                                                exponent=info.exponent,
                                                connected=False)
        s = [_escape_text_for_latex(e) for e in info.wire_symbols]
        if info.exponent != 1:
            s[0] += u'^{' + unicode(info.exponent) + u'}'
        return protocols.CircuitDiagramInfo(tuple(u'\\gate{' + e + u'}'
                                                  for e in s))


class _FallbackQCircuitGate(QCircuitDiagrammable):
    def __init__(self, sub):
        self.sub = sub

    def qcircuit_diagram_info(self, args
                              ):
        name = unicode(self.sub)
        qubit_count = ((len(args.known_qubits) if
                       (args.known_qubits is not None) else 1)
                       if args.known_qubit_count is None
                       else args.known_qubit_count)
        symbols = [name] + [u'#{}'.format(i + 1) for i in xrange(1, qubit_count)]
        escaped_symbols = tuple(_escape_text_for_latex(s) for s in symbols)
        return protocols.CircuitDiagramInfo(escaped_symbols)


def known_qcircuit_operation_symbols(op
                                     ):
    if isinstance(op, ops.GateOperation):
        return _known_gate_symbols(op.gate)
    return None


def _known_gate_symbols(
        gate):
    if gate == ops.X:
        return _HardcodedQCircuitSymbolsGate(ur'\targ')
    if gate == ops.CZ:
        return _HardcodedQCircuitSymbolsGate(ur'\control', ur'\control')
    if gate == ops.CNOT:
        return _HardcodedQCircuitSymbolsGate(ur'\control', ur'\targ')
    if ops.MeasurementGate.is_measurement(gate):
        return _HardcodedQCircuitSymbolsGate(ur'\meter')
    return None
