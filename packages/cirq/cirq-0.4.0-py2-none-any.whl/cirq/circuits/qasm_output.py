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

u"""Utility classes for representing QASM."""

from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from typing import Set  # pylint: disable=unused-import
from typing import (
    Callable, Dict, Optional, Sequence, Tuple, Union, cast
)

import re
import numpy as np

from cirq import ops, linalg, protocols, value
from io import open
from itertools import imap


class QasmUGate(ops.SingleQubitGate):
    def __init__(self, lmda, theta, phi):
        u"""A QASM gate representing any single qubit unitary with a series of
        three rotations, Z, Y, and Z.

        The angles are normalized to the range [0, 2) half_turns.

        Args:
            lmda: Half turns to rotate about Z (applied first).
            theta: Half turns to rotate about Y.
            phi: Half turns to rotate about Z (applied last).
        """
        self.lmda = lmda % 2
        self.theta = theta % 2
        self.phi = phi % 2

    @staticmethod
    def from_matrix(mat):
        pre_phase, rotation, post_phase = (
            linalg.deconstruct_single_qubit_matrix_into_angles(mat))
        return QasmUGate(pre_phase/np.pi, rotation/np.pi, post_phase/np.pi)

    def _qasm_(self,
               qubits,
               args):
        args.validate_version(u'2.0')
        return args.format(
                u'u3({0:half_turns},{1:half_turns},{2:half_turns}) {3};\n',
                self.theta, self.phi, self.lmda, qubits[0])

    def __repr__(self):
        return u'cirq.QasmUGate({}, {}, {})'.format(self.lmda,
                                                   self.theta,
                                                   self.phi)


class QasmTwoQubitGate(ops.TwoQubitGate):
    def __init__(self, kak):
        u"""A two qubit gate represented in QASM by the KAK decomposition.

        All angles are in half turns.  Assumes a canonicalized KAK
        decomposition.

        Args:
            kak: KAK decomposition of the two-qubit gate.
        """
        self.kak = kak

    def _value_equality_values_(self):
        return self.kak

    @staticmethod
    def from_matrix(mat, atol=1e-8):
        u"""Creates a QasmTwoQubitGate from the given matrix.

        Args:
            mat: The unitary matrix of the two qubit gate.
            atol: Absolute error tolerance when decomposing.

        Returns:
            A QasmTwoQubitGate implementing the matrix.
        """
        kak = linalg.kak_decomposition(mat, linalg.Tolerance(atol=atol))
        return QasmTwoQubitGate(kak)

    def _unitary_(self):
        return protocols.unitary(self.kak)

    def _decompose_(self, qubits):
        q0, q1 = qubits
        x, y, z = self.kak.interaction_coefficients
        a = x * -2 / np.pi + 0.5
        b = y * -2 / np.pi + 0.5
        c = z * -2 / np.pi + 0.5

        b0, b1 = self.kak.single_qubit_operations_before
        yield QasmUGate.from_matrix(b0).on(q0)
        yield QasmUGate.from_matrix(b1).on(q1)

        yield ops.X(q0)**0.5
        yield ops.CNOT(q0, q1)
        yield ops.X(q0)**a
        yield ops.Y(q1)**b
        yield ops.CNOT(q1, q0)
        yield ops.X(q1)**-0.5
        yield ops.Z(q1)**c
        yield ops.CNOT(q0, q1)

        a0, a1 = self.kak.single_qubit_operations_after
        yield QasmUGate.from_matrix(a0).on(q0)
        yield QasmUGate.from_matrix(a1).on(q1)

    def __repr__(self):
        return u'cirq.circuits.qasm_output.QasmTwoQubitGate({!r})'.format(
            self.kak)


QasmTwoQubitGate = value.value_equality(QasmTwoQubitGate)

class QasmOutput(object):
    valid_id_re = re.compile(u'[a-z][a-zA-Z0-9_]*\Z')

    def __init__(self,
                 operations,
                 qubits,
                 header = u'',
                 precision = 10,
                 version = u'2.0'):
        self.operations = tuple(ops.flatten_op_tree(operations))
        self.qubits = qubits
        self.header = header
        self.measurements = tuple(cast(ops.GateOperation, op)
                                  for op in self.operations
                                  if ops.MeasurementGate.is_measurement(op))

        meas_key_id_map, meas_comments = self._generate_measurement_ids()
        self.meas_comments = meas_comments
        qubit_id_map = self._generate_qubit_ids()
        self.args = protocols.QasmArgs(
            precision=precision,
            version=version,
            qubit_id_map=qubit_id_map,
            meas_key_id_map=meas_key_id_map)

    def _generate_measurement_ids(self
            ):
        # Pick an id for the creg that will store each measurement
        meas_key_id_map = {}  # type: Dict[str, str]
        meas_comments = {}  # type: Dict[str, Optional[str]]
        meas_i = 0
        for meas in self.measurements:
            key = cast(ops.MeasurementGate, meas.gate).key
            if key in meas_key_id_map:
                continue
            meas_id = u'm_{}'.format(key)
            if self.is_valid_qasm_id(meas_id):
                meas_comments[key] = None
            else:
                meas_id = u'm{}'.format(meas_i)
                meas_i += 1
                meas_comments[key] = u' '.join(key.split(u'\n'))
            meas_key_id_map[key] = meas_id
        return meas_key_id_map, meas_comments

    def _generate_qubit_ids(self):
        return dict((qubit, u'q[{}]'.format(i)) for i, qubit in enumerate(self.qubits))

    def is_valid_qasm_id(self, id_str):
        u"""Test if id_str is a valid id in QASM grammar."""
        return self.valid_id_re.match(id_str) != None

    def save(self, path):
        u"""Write QASM output to a file specified by path."""
        with open(path, u'w') as f:
            def write(s):
                f.write(s)
            self._write_qasm(write)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        u"""Return QASM output as a string."""
        output = []
        self._write_qasm(lambda s: output.append(s))
        return u''.join(output)

    def _write_qasm(self, output_func):
        self.args.validate_version(u'2.0')

        # Generate nice line spacing
        line_gap = [0]
        def output_line_gap(n):
            line_gap[0] = max(line_gap[0], n)
        def output(text):
            if line_gap[0] > 0:
                output_func(u'\n' * line_gap[0])
                line_gap[0] = 0
            output_func(text)

        # Comment header
        if self.header:
            for line in self.header.split(u'\n'):
                output((u'// ' + line).rstrip() + u'\n')
            output(u'\n')

        # Version
        output(u'OPENQASM 2.0;\n')
        output(u'include "qelib1.inc";\n')
        output_line_gap(2)

        # Function definitions
        # None yet

        # Register definitions
        # Qubit registers
        output(u'// Qubits: [{}]\n'.format(u', '.join(imap(unicode, self.qubits))))
        output(u'qreg q[{}];\n'.format(len(self.qubits)))
        # Classical registers
        # Pick an id for the creg that will store each measurement
        already_output_keys = set()  # type: Set[str]
        for meas in self.measurements:
            key = cast(ops.MeasurementGate, meas.gate).key
            if key in already_output_keys:
                continue
            already_output_keys.add(key)
            meas_id = self.args.meas_key_id_map[key]
            comment = self.meas_comments[key]
            if comment is None:
                output(u'creg {}[{}];\n'.format(meas_id, len(meas.qubits)))
            else:
                output(u'creg {}[{}];  // Measurement: {}\n'.format(
                            meas_id, len(meas.qubits), comment))
        output_line_gap(2)

        # Operations
        self._write_operations(self.operations, output, output_line_gap)

    def _write_operations(self,
                          op_tree,
                          output,
                          output_line_gap):
        def keep(op):
            return protocols.qasm(op, args=self.args, default=None) is not None

        def fallback(op):
            if len(op.qubits) not in [1, 2]:
                return NotImplemented

            mat = protocols.unitary(op, None)
            if mat is None:
                return NotImplemented

            if len(op.qubits) == 1:
                return QasmUGate.from_matrix(mat).on(*op.qubits)
            return QasmTwoQubitGate.from_matrix(mat).on(*op.qubits)

        def on_stuck(bad_op):
            return ValueError(
                u'Cannot output operation as QASM: {!r}'.format(bad_op))

        for main_op in ops.flatten_op_tree(op_tree):
            decomposed = protocols.decompose(
                main_op,
                keep=keep,
                fallback_decomposer=fallback,
                on_stuck_raise=on_stuck)

            should_annotate = decomposed != [main_op]
            if should_annotate:
                output_line_gap(1)
                if isinstance(main_op, ops.GateOperation):
                    x = unicode(main_op.gate).replace(u'\n', u'\n //')
                    output(u'// Gate: {!s}\n'.format(x))
                else:
                    x = unicode(main_op).replace(u'\n', u'\n //')
                    output(u'// Operation: {!s}\n'.format(x))

            for decomposed_op in decomposed:
                output(protocols.qasm(decomposed_op, args=self.args))

            if should_annotate:
                output_line_gap(1)
