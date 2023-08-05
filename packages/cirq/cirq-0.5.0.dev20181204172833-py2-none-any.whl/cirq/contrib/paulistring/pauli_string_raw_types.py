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
from typing import Any, Dict, Sequence, Tuple, TypeVar

import abc

from cirq import ops, protocols
from cirq.ops.pauli_string import PauliString
from itertools import izip


TSelf_PauliStringGateOperation = TypeVar(u'TSelf_PauliStringGateOperation',
                                         bound=u'PauliStringGateOperation')


class PauliStringGateOperation(ops.Operation):
    __metaclass__ = abc.ABCMeta
    def __init__(self, pauli_string):
        self.pauli_string = pauli_string

    def validate_args(self, qubits):
        if len(qubits) != len(self.pauli_string):
            raise ValueError(u'Incorrect number of qubits for gate')

    def with_qubits(self,
                    *new_qubits
                    ):
        self.validate_args(new_qubits)
        return self.map_qubits(dict(izip(self.pauli_string.qubits,
                                        new_qubits)))

    @abc.abstractmethod
    def map_qubits(self,
                   qubit_map
                   ):
        u"""Return an equivalent operation on new qubits with its Pauli string
        mapped to new qubits.

        new_pauli_string = self.pauli_string.map_qubits(qubit_map)
        """
        pass

    @property
    def qubits(self):
        return tuple(self.pauli_string)

    def _pauli_string_diagram_info(self,
                                   args,
                                   exponent = 1,
                                   exponent_absorbs_sign = False,
                                   ):
        qubits = self.qubits if args.known_qubits is None else args.known_qubits
        syms = tuple(u'[{}]'.format(self.pauli_string[qubit])
                     for qubit in qubits)
        if exponent_absorbs_sign and self.pauli_string.negated:
            if isinstance(exponent, float):
                exponent = -exponent
            else:
                exponent = u'-{!s}'.format(exponent)
        return protocols.CircuitDiagramInfo(wire_symbols=syms,
                                            exponent=exponent)
