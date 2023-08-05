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
from typing import cast, Dict

from cirq.study.sweeps import (
    Linspace, Points, Product, SingleSweep, Sweep, UnitSweep, Zip,
)


def sweep_to_proto_dict(sweep, repetitions=1):
    u"""Converts sweep into an equivalent protobuf representation."""
    msg = {}  # type: Dict
    if not sweep == UnitSweep:
        sweep = _to_zip_product(sweep)
        msg[u'sweep'] = {
            u'factors': [_sweep_zip_to_proto_dict(cast(Zip, factor)) for factor
                        in sweep.factors]
        }
    msg[u'repetitions'] = repetitions
    return msg



def _to_zip_product(sweep):
    u"""Converts sweep to a product of zips of single sweeps, if possible."""
    if not isinstance(sweep, Product):
        sweep = Product(sweep)
    if not all(isinstance(f, Zip) for f in sweep.factors):
        factors = [f if isinstance(f, Zip) else Zip(f) for f in sweep.factors]
        sweep = Product(*factors)
    for factor in sweep.factors:
        for term in cast(Zip, factor).sweeps:
            if not isinstance(term, SingleSweep):
                raise ValueError(u'cannot convert to zip-product form: {}'
                                 .format(sweep))
    return sweep


def _sweep_zip_to_proto_dict(
        sweep):
    sweeps = [_single_param_sweep_to_proto_dict(cast(SingleSweep, s)) for s
              in sweep.sweeps]
    return {u'sweeps': sweeps}


def _single_param_sweep_to_proto_dict(
        sweep,
):
    msg = {}  # type: Dict
    msg[u'parameter_key'] = sweep.key
    if isinstance(sweep, Linspace):
        msg[u'linspace'] = {
            u'first_point': sweep.start,
            u'last_point': sweep.stop,
            u'num_points': sweep.length
        }
    elif isinstance(sweep, Points):
        msg[u'points'] = {u'points': sweep.points}
    else:
        raise ValueError(u'invalid single-parameter sweep: {}'.format(sweep))
    return msg


def sweep_from_proto_dict(param_sweep):
    if u'sweep' in param_sweep and u'factors' in param_sweep[u'sweep']:
        return Product(*[_sweep_from_param_sweep_zip_proto_dict(f)
                         for f in param_sweep[u'sweep'][u'factors']])
    return UnitSweep


def _sweep_from_param_sweep_zip_proto_dict(
        param_sweep_zip):
    if u'sweeps' in param_sweep_zip:
        return Zip(*[_sweep_from_single_param_sweep_proto_dict(sweep)
                     for sweep in param_sweep_zip[u'sweeps']])
    return UnitSweep


def _sweep_from_single_param_sweep_proto_dict(
        single_param_sweep):
    key = single_param_sweep[u'parameter_key']
    if u'points' in single_param_sweep:
        points = single_param_sweep[u'points']
        return Points(key, list(points[u'points']))
    elif u'linspace' in single_param_sweep:
        sl = single_param_sweep[u'linspace']
        return Linspace(key, sl[u'first_point'], sl[u'last_point'],
                        sl[u'num_points'])
    else:
        raise ValueError(u'Single param sweep type undefined')
