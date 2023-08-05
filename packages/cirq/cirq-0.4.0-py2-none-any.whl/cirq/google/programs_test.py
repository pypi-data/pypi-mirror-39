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
from typing import Dict

import numpy as np
import pytest

import cirq
import cirq.google as cg
from cirq.google.programs import (
    _parameterized_value_from_proto_dict
)
from cirq.schedules import moment_by_moment_schedule


def assert_proto_dict_convert(gate,
                              proto_dict,
                              *qubits):
    assert cg.gate_to_proto_dict(gate, qubits) == proto_dict
    assert cg.xmon_op_from_proto_dict(proto_dict) == gate(*qubits)


def test_protobuf_round_trip():
    device = cg.Foxtail
    circuit = cirq.Circuit.from_ops(
        [
            cirq.X(q)**0.5
            for q in device.qubits
        ],
        [
            cirq.CZ(q, q2)
            for q in [cirq.GridQubit(0, 0)]
            for q2 in device.neighbors_of(q)
        ]
    )
    s1 = moment_by_moment_schedule(device, circuit)

    protos = list(cg.schedule_to_proto_dicts(s1))
    s2 = cg.schedule_from_proto_dicts(device, protos)

    assert s2 == s1


def make_bytes(s):
    u"""Helper function to convert a string of digits into packed bytes.

    Ignores any characters other than 0 and 1, in particular whitespace. The
    bits are packed in little-endian order within each byte.
    """
    buf = []
    byte = 0
    idx = 0
    for c in s:
        if c == u'0':
            pass
        elif c == u'1':
            byte |= 1 << idx
        else:
            continue
        idx += 1
        if idx == 8:
            buf.append(byte)
            byte = 0
            idx = 0
    if idx:
        buf.append(byte)
    return bytearray(buf)


def test_pack_results():
    measurements = [
        (u'a',
         np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],])),
        (u'b',
         np.array([
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [0, 0],
            [0, 1],
            [1, 0],])),
    ]
    data = cg.pack_results(measurements)
    expected = make_bytes(u"""
        000 00
        001 01
        010 10
        011 11
        100 00
        101 01
        110 10

        000 00 -- padding
    """)
    assert data == expected


def test_pack_results_no_measurements():
    assert cg.pack_results([]) == ''


def test_pack_results_incompatible_shapes():
    def bools(*shape):
        return np.zeros(shape, dtype=bool)

    with pytest.raises(ValueError):
        cg.pack_results([(u'a', bools(10))])

    with pytest.raises(ValueError):
        cg.pack_results([(u'a', bools(7, 3)), (u'b', bools(8, 2))])


def test_unpack_results():
    data = make_bytes(u"""
        000 00
        001 01
        010 10
        011 11
        100 00
        101 01
        110 10
    """)
    assert len(data) == 5  # 35 data bits + 5 padding bits
    results = cg.unpack_results(data, 7, [(u'a', 3), (u'b', 2)])
    assert u'a' in results
    assert results[u'a'].shape == (7, 3)
    assert results[u'a'].dtype == bool
    np.testing.assert_array_equal(
        results[u'a'],
        [[0, 0, 0],
         [0, 0, 1],
         [0, 1, 0],
         [0, 1, 1],
         [1, 0, 0],
         [1, 0, 1],
         [1, 1, 0],])

    assert u'b' in results
    assert results[u'b'].shape == (7, 2)
    assert results[u'b'].dtype == bool
    np.testing.assert_array_equal(
        results[u'b'],
        [[0, 0],
         [0, 1],
         [1, 0],
         [1, 1],
         [0, 0],
         [0, 1],
         [1, 0],])


def test_single_qubit_measurement_proto_dict_convert():
    gate = cirq.MeasurementGate(u'test')
    proto_dict = {
        u'measurement': {
            u'targets': [
                {
                    u'row': 2,
                    u'col': 3
                }
            ],
            u'key': u'test'
        }
    }
    assert_proto_dict_convert(gate,
                              proto_dict,
                              cirq.GridQubit(2, 3))


def test_single_qubit_measurement_to_proto_dict_convert_invert_mask():
    gate = cirq.MeasurementGate(u'test', invert_mask=(True,))
    proto_dict = {
        u'measurement': {
            u'targets': [
                {
                    u'row': 2,
                    u'col': 3
                }
            ],
            u'key': u'test',
            u'invert_mask': [u'true']
        }
    }
    assert_proto_dict_convert(gate, proto_dict, cirq.GridQubit(2, 3))


def test_multi_qubit_measurement_to_proto_dict():
    gate = cirq.MeasurementGate(u'test')
    proto_dict = {
        u'measurement': {
            u'targets': [
                {
                    u'row': 2,
                    u'col': 3
                },
                {
                    u'row': 3,
                    u'col': 4
                }
            ],
            u'key': u'test'
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3), cirq.GridQubit(3, 4))


def test_z_proto_dict_convert():
    gate = cirq.Z**cirq.Symbol(u'k')
    proto_dict = {
        u'exp_z': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3))

    gate = cirq.Z**0.5
    proto_dict = {
        u'exp_z': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'half_turns': {
                u'raw': 0.5
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3))


def test_cz_proto_dict_convert():
    gate = cirq.CZ**cirq.Symbol(u'k')
    proto_dict = {
        u'exp_11': {
            u'target1': {
                u'row': 2,
                u'col': 3
            },
            u'target2': {
                u'row': 3,
                u'col': 4
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3), cirq.GridQubit(3, 4))

    gate = cirq.CZ**0.5
    proto_dict = {
        u'exp_11': {
            u'target1': {
                u'row': 2,
                u'col': 3
            },
            u'target2': {
                u'row': 3,
                u'col': 4
            },
            u'half_turns': {
                u'raw': 0.5
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3), cirq.GridQubit(3, 4))


def test_cz_invalid_dict():
    proto_dict = {
        u'exp_11': {
            u'target2': {
                u'row': 3,
                u'col': 4
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    with pytest.raises(ValueError, match=u'missing required fields'):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'exp_11': {
            u'target1': {
                u'row': 2,
                u'col': 3
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    with pytest.raises(ValueError, match=u'missing required fields'):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'exp_11': {
            u'target1': {
                u'row': 2,
                u'col': 3
            },
            u'target2': {
                u'row': 3,
                u'col': 4
            },
        }
    }
    with pytest.raises(ValueError, match=u'missing required fields'):
        cg.xmon_op_from_proto_dict(proto_dict)


def test_w_to_proto_dict():
    gate = cirq.PhasedXPowGate(exponent=cirq.Symbol(u'k'), phase_exponent=1)
    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'raw': 1
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3))

    gate = cirq.PhasedXPowGate(exponent=0.5, phase_exponent=cirq.Symbol(u'j'))
    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'parameter_key': u'j'
            },
            u'half_turns': {
                u'raw': 0.5
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3))

    gate = cirq.X**0.25
    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'raw': 0.0
            },
            u'half_turns': {
                u'raw': 0.25
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict, cirq.GridQubit(2, 3))

    gate = cirq.Y**0.25
    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'raw': 0.5
            },
            u'half_turns': {
                u'raw': 0.25
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict, cirq.GridQubit(2, 3))

    gate = cirq.PhasedXPowGate(exponent=0.5, phase_exponent=cirq.Symbol(u'j'))
    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'parameter_key': u'j'
            },
            u'half_turns': {
                u'raw': 0.5
            }
        }
    }
    assert_proto_dict_convert(gate, proto_dict,
                              cirq.GridQubit(2, 3))


def test_w_invalid_dict():
    proto_dict = {
        u'exp_w': {
            u'axis_half_turns': {
                u'raw': 1
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'exp_w': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
            u'axis_half_turns': {
                u'raw': 1
            },
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)


def test_unsupported_op():
    proto_dict = {
        u'not_a_gate': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
        }
    }
    with pytest.raises(ValueError, match=u'invalid operation'):
        cg.xmon_op_from_proto_dict(proto_dict)
    with pytest.raises(ValueError, match=u'know how to serialize'):
        cg.gate_to_proto_dict(cirq.CCZ, (cirq.GridQubit(0, 0),
                                         cirq.GridQubit(0, 1),
                                         cirq.GridQubit(0, 2)))


def test_invalid_to_proto_dict_qubit_number():
    with pytest.raises(ValueError, match=u'Wrong number of qubits'):
        _ = cg.gate_to_proto_dict(cirq.CZ**0.5, (cirq.GridQubit(2, 3),))
    with pytest.raises(ValueError, match=u'Wrong number of qubits'):
        cg.gate_to_proto_dict(cirq.Z**0.5, (cirq.GridQubit(2, 3),
                                            cirq.GridQubit(3, 4)))
    with pytest.raises(ValueError, match=u'Wrong number of qubits'):
        cg.gate_to_proto_dict(
            cirq.PhasedXPowGate(exponent=0.5, phase_exponent=0),
            (cirq.GridQubit(2, 3), cirq.GridQubit(3, 4)))


def test_parameterized_value_from_proto():
    from_proto = _parameterized_value_from_proto_dict

    m1 = {u'raw': 5}
    assert from_proto(m1) == 5

    with pytest.raises(ValueError):
        from_proto({})

    m3 = {u'parameter_key': u'rr'}
    assert from_proto(m3) == cirq.Symbol(u'rr')


def test_single_qubit_measurement_invalid_dict():
    proto_dict = {
        u'measurement': {
            u'targets': [
                {
                    u'row': 2,
                    u'col': 3
                }
            ],
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'measurement': {
            u'targets': [
                {
                    u'row': 2,
                    u'col': 3
                }
            ],
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)


def test_invalid_measurement_gate():
    with pytest.raises(ValueError, match=u'length'):
        _ = cg.gate_to_proto_dict(
            cirq.MeasurementGate(u'test', invert_mask=(True,)),
            (cirq.GridQubit(2, 3), cirq.GridQubit(3, 4)))
    with pytest.raises(ValueError, match=u'no qubits'):
        _ = cg.gate_to_proto_dict(
            cirq.MeasurementGate(u'test'), ())


def test_z_invalid_dict():
    proto_dict = {
        u'exp_z': {
            u'target': {
                u'row': 2,
                u'col': 3
            },
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)

    proto_dict = {
        u'exp_z': {
            u'half_turns': {
                u'parameter_key': u'k'
            }
        }
    }
    with pytest.raises(ValueError):
        cg.xmon_op_from_proto_dict(proto_dict)


def test_is_supported():
    a = cirq.GridQubit(0, 0)
    b = cirq.GridQubit(0, 1)
    c = cirq.GridQubit(1, 0)
    assert cg.is_native_xmon_op(cirq.CZ(a, b))
    assert cg.is_native_xmon_op(cirq.X(a)**0.5)
    assert cg.is_native_xmon_op(cirq.Y(a)**0.5)
    assert cg.is_native_xmon_op(cirq.Z(a)**0.5)
    assert cg.is_native_xmon_op(
        cirq.PhasedXPowGate(phase_exponent=0.2).on(a)**0.5)
    assert cg.is_native_xmon_op(cirq.Z(a)**1)
    assert not cg.is_native_xmon_op(cirq.CCZ(a, b, c))
    assert not cg.is_native_xmon_op(cirq.SWAP(a, b))


def test_is_native_xmon_gate():
    assert cg.is_native_xmon_gate(cirq.CZ)
    assert cg.is_native_xmon_gate(cirq.X**0.5)
    assert cg.is_native_xmon_gate(cirq.Y**0.5)
    assert cg.is_native_xmon_gate(cirq.Z**0.5)
    assert cg.is_native_xmon_gate(cirq.PhasedXPowGate(phase_exponent=0.2)**0.5)
    assert cg.is_native_xmon_gate(cirq.Z**1)
    assert not cg.is_native_xmon_gate(cirq.CCZ)
    assert not cg.is_native_xmon_gate(cirq.SWAP)
