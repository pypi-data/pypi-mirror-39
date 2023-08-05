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
import json
from typing import (
    Any, cast, Dict, Iterable, Sequence, Tuple, TYPE_CHECKING, Union
)

import numpy as np

from cirq import ops, devices, value
from cirq.schedules import Schedule, ScheduledOperation
from cirq.value import Timestamp

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Optional
    from cirq.google import xmon_device


def gate_to_proto_dict(gate,
                       qubits):
    if isinstance(gate, ops.MeasurementGate):
        return _measure_to_proto_dict(gate, qubits)

    if isinstance(gate, ops.XPowGate):
        if len(qubits) != 1:
            # coverage: ignore
            raise ValueError(u'Wrong number of qubits.')
        return _x_to_proto_dict(gate, qubits[0])

    if isinstance(gate, ops.YPowGate):
        if len(qubits) != 1:
            # coverage: ignore
            raise ValueError(u'Wrong number of qubits.')
        return _y_to_proto_dict(gate, qubits[0])

    if isinstance(gate, ops.PhasedXPowGate):
        if len(qubits) != 1:
            # coverage: ignore
            raise ValueError(u'Wrong number of qubits.')
        return _phased_x_to_proto_dict(gate, qubits[0])

    if isinstance(gate, ops.ZPowGate):
        if len(qubits) != 1:
            # coverage: ignore
            raise ValueError(u'Wrong number of qubits.')
        return _z_to_proto_dict(gate, qubits[0])

    if isinstance(gate, ops.CZPowGate):
        if len(qubits) != 2:
            # coverage: ignore
            raise ValueError(u'Wrong number of qubits.')
        return _cz_to_proto_dict(gate, *qubits)

    raise ValueError(u"Don't know how to serialize this gate: {!r}".format(gate))


def _x_to_proto_dict(gate, q):
    exp_w = {
        u'target': cast(devices.GridQubit, q).to_proto_dict(),
        u'axis_half_turns':
            _parameterized_value_to_proto_dict(0),
        u'half_turns': _parameterized_value_to_proto_dict(
            gate.exponent)
    }
    return {u'exp_w': exp_w}


def _y_to_proto_dict(gate, q):
    exp_w = {
        u'target': cast(devices.GridQubit, q).to_proto_dict(),
        u'axis_half_turns':
            _parameterized_value_to_proto_dict(0.5),
        u'half_turns': _parameterized_value_to_proto_dict(
            gate.exponent)
    }
    return {u'exp_w': exp_w}


def _phased_x_to_proto_dict(gate,
                            q):
    exp_w = {
        u'target': cast(devices.GridQubit, q).to_proto_dict(),
        u'axis_half_turns':
            _parameterized_value_to_proto_dict(
                gate.phase_exponent),
        u'half_turns': _parameterized_value_to_proto_dict(
            gate.exponent)
    }
    return {u'exp_w': exp_w}


def _z_to_proto_dict(gate, q):
    exp_z = {
        u'target': cast(devices.GridQubit, q).to_proto_dict(),
        u'half_turns': _parameterized_value_to_proto_dict(
            gate.exponent),
    }
    return {u'exp_z': exp_z}


def _cz_to_proto_dict(gate,
                      p,
                      q):
    exp_11 = {
        u'target1': cast(devices.GridQubit, p).to_proto_dict(),
        u'target2': cast(devices.GridQubit, q).to_proto_dict(),
        u'half_turns': _parameterized_value_to_proto_dict(
            gate.exponent)
    }
    return {u'exp_11': exp_11}


def _measure_to_proto_dict(gate,
                           qubits):
    if len(qubits) == 0:
        raise ValueError(u'Measurement gate on no qubits.')
    if gate.invert_mask and len(gate.invert_mask) != len(qubits):
        raise ValueError(u'Measurement gate had invert mask of length '
                         u'different than number of qubits it acts on.')
    measurement = {
        u'targets': [cast(devices.GridQubit, q).to_proto_dict() for q in qubits],
        u'key': gate.key,
    }
    if gate.invert_mask:
        measurement[u'invert_mask'] = [json.dumps(x) for x in
                                      gate.invert_mask]
    return {u'measurement': measurement}


def schedule_to_proto_dicts(schedule):
    u"""Convert a schedule into an iterable of proto dictionaries.

    Args:
        schedule: The schedule to convert to a proto dict. Must contain only
            gates that can be cast to xmon gates.

    Yields:
        A proto dictionary corresponding to an Operation proto.
    """
    last_time_picos = None  # type: Optional[int]
    for so in schedule.scheduled_operations:
        op = gate_to_proto_dict(
            cast(ops.GateOperation, so.operation).gate,
            so.operation.qubits)
        time_picos = so.time.raw_picos()
        if last_time_picos is None:
            op[u'incremental_delay_picoseconds'] = time_picos
        else:
            op[u'incremental_delay_picoseconds'] = time_picos - last_time_picos
        last_time_picos = time_picos
        yield op


def schedule_from_proto_dicts(
        device,
        ops,
):
    u"""Convert proto dictionaries into a Schedule for the given device."""
    scheduled_ops = []
    last_time_picos = 0
    for op in ops:
        delay_picos = 0
        if u'incremental_delay_picoseconds' in op:
            delay_picos = op[u'incremental_delay_picoseconds']
        time_picos = last_time_picos + delay_picos
        last_time_picos = time_picos
        xmon_op = xmon_op_from_proto_dict(op)
        scheduled_ops.append(ScheduledOperation.op_at_on(
            operation=xmon_op,
            time=Timestamp(picos=time_picos),
            device=device,
        ))
    return Schedule(device, scheduled_ops)


def pack_results(measurements):
    u"""Pack measurement results into a byte string.

    Args:
        measurements: A sequence of tuples, one for each measurement, consisting
            of a string key and an array of boolean data. The data should be
            a 2-D array indexed by (repetition, qubit_index). All data for all
            measurements must have the same number of repetitions.

    Returns:
        Packed bytes, as described in the unpack_results docstring below.

    Raises:
        ValueError if the measurement data do not have the compatible shapes.
    """
    if not measurements:
        return ''

    shapes = [(key, np.shape(data)) for key, data in measurements]
    if not all(len(shape) == 2 for _, shape in shapes):
        raise ValueError(u"Expected 2-D data: shapes={}".format(shapes))

    reps = shapes[0][1][0]
    if not all(shape[0] == reps for _, shape in shapes):
        raise ValueError(
            u"Expected same reps for all keys: shapes={}".format(shapes))

    bits = np.hstack(np.asarray(data, dtype=bool) for _, data in measurements)
    bits = bits.reshape(-1)

    # Pad length to multiple of 8 if needed.
    remainder = len(bits) % 8
    if remainder:
        bits = np.pad(bits, (0, 8 - remainder), u'constant')

    # Pack in little-endian bit order.
    bits = bits.reshape((-1, 8))[:, ::-1]
    byte_arr = np.packbits(bits, axis=1).reshape(-1)

    return byte_arr.tobytes()


def unpack_results(
        data,
        repetitions,
        key_sizes
):
    u"""Unpack data from a bitstring into individual measurement results.

    Args:
        data: Packed measurement results, in the form <rep0><rep1>...
            where each repetition is <key0_0>..<key0_{size0-1}><key1_0>...
            with bits packed in little-endian order in each byte.
        repetitions: number of repetitions.
        key_sizes: Keys and sizes of the measurements in the data.

    Returns:
        Dict mapping measurement key to a 2D array of boolean results. Each
        array has shape (repetitions, size) with size for that measurement.
    """
    bits_per_rep = sum(size for _, size in key_sizes)
    total_bits = repetitions * bits_per_rep

    byte_arr = np.frombuffer(data, dtype=u'uint8').reshape((len(data), 1))
    bits = np.unpackbits(byte_arr, axis=1)[:, ::-1].reshape(-1).astype(bool)
    bits = bits[:total_bits].reshape((repetitions, bits_per_rep))

    results = {}
    ofs = 0
    for key, size in key_sizes:
        results[key] = bits[:, ofs:ofs + size]
        ofs += size

    return results


def is_native_xmon_op(op):
    u"""Check if the gate corresponding to an operation is a native xmon gate.

    Args:
        op: Input operation.

    Returns:
        True if the operation is native to the xmon, false otherwise.
    """
    return (isinstance(op, ops.GateOperation) and
            is_native_xmon_gate(op.gate))


def is_native_xmon_gate(gate):
    u"""Check if a gate is a native xmon gate.

    Args:
        gate: Input gate.

    Returns:
        True if the gate is native to the xmon, false otherwise.
    """
    return isinstance(gate, (ops.CZPowGate,
                             ops.MeasurementGate,
                             ops.PhasedXPowGate,
                             ops.XPowGate,
                             ops.YPowGate,
                             ops.ZPowGate))


def xmon_op_from_proto_dict(proto_dict):
    u"""Convert the proto dictionary to the corresponding operation.

    See protos in api/google/v1 for specification of the protos.

    Args:
        proto_dict: Dictionary representing the proto. Keys are always
            strings, but values may be types correspond to a raw proto type
            or another dictionary (for messages).

    Returns:
        The operation.

    Raises:
        ValueError if the dictionary does not contain required values
        corresponding to the proto.
    """

    def raise_missing_fields(gate_name):
        raise ValueError(
            u'{} missing required fields: {}'.format(gate_name, proto_dict))
    param = _parameterized_value_from_proto_dict
    qubit = devices.GridQubit.from_proto_dict
    if u'exp_w' in proto_dict:
        exp_w = proto_dict[u'exp_w']
        if (u'half_turns' not in exp_w or u'axis_half_turns' not in exp_w
                or u'target' not in exp_w):
            raise_missing_fields(u'ExpW')
        return ops.PhasedXPowGate(
            exponent=param(exp_w[u'half_turns']),
            phase_exponent=param(exp_w[u'axis_half_turns']),
        ).on(qubit(exp_w[u'target']))
    elif u'exp_z' in proto_dict:
        exp_z = proto_dict[u'exp_z']
        if u'half_turns' not in exp_z or u'target' not in exp_z:
            raise_missing_fields(u'ExpZ')
        return ops.Z(qubit(exp_z[u'target']))**param(exp_z[u'half_turns'])
    elif u'exp_11' in proto_dict:
        exp_11 = proto_dict[u'exp_11']
        if (u'half_turns' not in exp_11 or u'target1' not in exp_11
                or u'target2' not in exp_11):
            raise_missing_fields(u'Exp11')
        return ops.CZ(qubit(exp_11[u'target1']),
                      qubit(exp_11[u'target2']))**param(exp_11[u'half_turns'])
    elif u'measurement' in proto_dict:
        meas = proto_dict[u'measurement']
        invert_mask = cast(Tuple[Any, ...], ())
        if u'invert_mask' in meas:
            invert_mask = tuple(json.loads(x) for x in meas[u'invert_mask'])
        if u'key' not in meas or u'targets' not in meas:
            raise_missing_fields(u'Measurement')
        return ops.MeasurementGate(
            key=meas[u'key'],
            invert_mask=invert_mask
        ).on(*[qubit(q) for q in meas[u'targets']])
    else:
        raise ValueError(u'invalid operation: {}'.format(proto_dict))


def _parameterized_value_from_proto_dict(message
                                         ):
    if u'raw' in message:
        return message[u'raw']
    if u'parameter_key' in message:
        return value.Symbol(message[u'parameter_key'])
    raise ValueError(u'No value specified for parameterized float. '
                     u'Expected "raw" or "parameter_key" to be set. '
                     u'message: {!r}'.format(message))


def _parameterized_value_to_proto_dict(param
                                       ):
    out = {}  # type: Dict
    if isinstance(param, value.Symbol):
        out[u'parameter_key'] = param.name
    else:
        out[u'raw'] = float(param)
    return out
