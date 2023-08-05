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
import pytest

from cirq.google import params
from cirq.study.sweeps import Linspace, Points, Product, UnitSweep, Zip


def test_gen_sweep_points():
    points = [0.5, 1.0, 1.5, 2.0, 2.5]
    sweep = {
        u'parameter_key': u'foo',
        u'points': {
            u'points': list(points)
        }
    }
    out = params._sweep_from_single_param_sweep_proto_dict(sweep)
    assert out == Points(u'foo', [0.5, 1.0, 1.5, 2.0, 2.5])


def test_gen_sweep_linspace():
    sweep = {
        u'parameter_key': u'foo',
        u'linspace': {
            u'first_point': 0,
            u'last_point': 10,
            u'num_points': 11
        }
    }
    out = params._sweep_from_single_param_sweep_proto_dict(sweep)
    assert out == Linspace(u'foo', 0, 10, 11)


def test_gen_param_sweep_zip():
    s1 = {
        u'parameter_key': u'foo',
        u'points': {
            u'points': [1, 2, 3]
        }
    }
    s2 = {
        u'parameter_key': u'bar',
        u'points': {
            u'points': [4, 5]
        }
    }
    sweep = {
        u'sweeps': [s1, s2]
    }
    out = params._sweep_from_param_sweep_zip_proto_dict(sweep)
    assert out == Points(u'foo', [1, 2, 3]) + Points(u'bar', [4, 5])


def test_gen_empty_param_sweep():
    out = params.sweep_from_proto_dict({})
    assert out == UnitSweep


def test_gen_param_sweep():
    s1 = {
        u'parameter_key': u'foo',
        u'points': {
            u'points': [1, 2, 3]
        }
    }
    s2 = {
        u'parameter_key': u'bar',
        u'points': {
            u'points': [4, 5]
        }
    }
    ps = {
        u'sweep': {
            u'factors': [
                {
                    u'sweeps': [s1]
                },
                {
                    u'sweeps': [s2]
                }

            ]
        }
    }
    out = params.sweep_from_proto_dict(ps)
    assert out == Product(Zip(Points(u'foo', [1, 2, 3])),
                          Zip(Points(u'bar', [4, 5])))


def test_empty_param_sweep_keys():
    assert params.sweep_from_proto_dict({}).keys == []


def test_sweep_from_proto_dict_missing_type():
    s1 = {
        u'parameter_key': u'foo',

    }
    ps = {
        u'sweep': {
            u'factors': [
                {
                    u'sweeps': [s1]
                },
            ]
        }
    }
    with pytest.raises(ValueError):
        params.sweep_from_proto_dict(ps)


def test_param_sweep_keys():
    s11 = {
        u'parameter_key': u'foo',
        u'points': {
            u'points': xrange(5)
        },
    }
    s12 = {
        u'parameter_key': u'bar',
        u'points': {
            u'points': xrange(7)
        },
    }

    s21 = {
        u'parameter_key': u'baz',
        u'points': {
            u'points': xrange(11)
        },
    }
    s22 = {
        u'parameter_key': u'qux',
        u'points': {
            u'points': xrange(13)
        }
    }
    ps = {
        u'sweep': {
            u'factors': [
                {
                    u'sweeps': [s11, s12],
                },
                {
                    u'sweeps': [s21, s22]
                }
            ]
        }
    }
    out = params.sweep_from_proto_dict(ps)
    assert out.keys == [u'foo', u'bar', u'baz', u'qux']


def test_empty_param_sweep_size():
    assert len(params.sweep_from_proto_dict({})) == 1


def test_param_sweep_size():
    s11 = {
        u'parameter_key': u'11',
        u'linspace': {
            u'first_point': 0,
            u'last_point': 10,
            u'num_points':  5
        }
    }
    s12 = {
        u'parameter_key': u'12',
        u'points': {
            u'points': xrange(7)
        }
    }
    s21 = {
        u'parameter_key': u'21',
        u'linspace': {
            u'first_point': 0,
            u'last_point': 10,
            u'num_points': 11
        }
    }
    s22 = {
        u'parameter_key': u'22',
        u'points': {
            u'points': xrange(13)
        }
    }
    ps = {
        u'sweep': {
            u'factors': [
                {
                    u'sweeps': [s11, s12],
                },
                {
                    u'sweeps': [s21, s22]
                }
            ]
        }
    }
    # Sweeps sx1 and sx2 are zipped, so should use num number of points.
    # These are then producted, so this should multiply number of points.
    assert len(params.sweep_from_proto_dict(ps)) == 5 * 11


def test_param_sweep_size_no_sweeps():
    ps = {
        u'sweep': {
            u'factors': [
                {
                },
                {
                }
            ]
        }
    }
    assert len(params.sweep_from_proto_dict(ps)) == 1


def example_sweeps():
    empty_sweep = {}
    empty_product = {
        u'sweep': {}
    }
    empty_zip = {
        u'sweep': {
            u'factors': [{}, {}]
        }
    }
    s11 = {
        u'parameter_key': u'11',
        u'linspace': {
            u'first_point': 0,
            u'last_point': 10,
            u'num_points':  5
        }
    }
    s12 = {
        u'parameter_key': u'12',
        u'points': {
            u'points': xrange(7)
        }
    }
    s21 = {
        u'parameter_key': u'21',
        u'linspace': {
            u'first_point': 0,
            u'last_point': 10,
            u'num_points': 11
        }
    }
    s22 = {
        u'parameter_key': u'22',
        u'points': {
            u'points': xrange(13)
        }
    }
    full_sweep = {
        u'sweep': {
            u'factors': [
                {
                    u'sweeps': [s11, s12],
                },
                {
                    u'sweeps': [s21, s22]
                }
            ]
        }
    }
    return [empty_sweep, empty_product, empty_zip, full_sweep]


@pytest.mark.parametrize(u'param_sweep', example_sweeps())
def test_param_sweep_size_versus_gen(param_sweep):
    sweep = params.sweep_from_proto_dict(param_sweep)
    print sweep
    predicted_size = len(sweep)
    out = list(sweep)
    assert len(out) == predicted_size


@pytest.mark.parametrize(u'sweep,expected', [
    (
        UnitSweep,
        UnitSweep
    ),
    (
        Linspace(u'a', 0, 10, 25),
        Product(Zip(Linspace(u'a', 0, 10, 25)))
    ),
    (
        Points(u'a', [1, 2, 3]),
        Product(Zip(Points(u'a', [1, 2, 3])))
    ),
    (
        Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
        Product(Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3]))),
    ),
    (
        Product(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
        Product(Zip(Linspace(u'a', 0, 1, 5)), Zip(Points(u'b', [1, 2, 3]))),
    ),
    (
        Product(
            Zip(Points(u'a', [1, 2, 3]), Points(u'b', [4, 5, 6])),
            Linspace(u'c', 0, 1, 5),
        ),
        Product(
            Zip(Points(u'a', [1, 2, 3]), Points(u'b', [4, 5, 6])),
            Zip(Linspace(u'c', 0, 1, 5)),
        ),
    ),
    (
        Product(
            Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
            Zip(Linspace(u'c', 0, 1, 8), Points(u'd', [1, 0.5, 0.25, 0.125])),
        ),
        Product(
            Zip(Linspace(u'a', 0, 1, 5), Points(u'b', [1, 2, 3])),
            Zip(Linspace(u'c', 0, 1, 8), Points(u'd', [1, 0.5, 0.25, 0.125])),
        ),
    ),
])


def test_sweep_to_proto_dict(sweep, expected):
    proto = params.sweep_to_proto_dict(sweep)
    out = params.sweep_from_proto_dict(proto)
    assert out == expected


@pytest.mark.parametrize(u'bad_sweep', [
    Zip(Product(Linspace(u'a', 0, 10, 25), Linspace(u'b', 0, 10, 25))),
])
def test_sweep_to_proto_fail(bad_sweep):
    with pytest.raises(ValueError):
        params.sweep_to_proto_dict(bad_sweep)
