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
import cirq


def test_trace_distance_bound():

    class NoMethod(object):
        pass

    class ReturnsNotImplemented(object):
        def _trace_distance_bound_(self):
            return NotImplemented

    class ReturnsTwo(object):
        def _trace_distance_bound_(self):
            return 2.0

    class ReturnsConstant(object):
        def __init__(self, bound):
            self.bound = bound

        def _trace_distance_bound_(self):
            return self.bound

    assert cirq.trace_distance_bound(NoMethod()) == 1.0
    assert cirq.trace_distance_bound(ReturnsNotImplemented()) == 1.0
    assert cirq.trace_distance_bound(ReturnsTwo()) == 1.0
    assert cirq.trace_distance_bound(ReturnsConstant(0.1)) == 0.1
    assert cirq.trace_distance_bound(ReturnsConstant(0.5)) == 0.5
    assert cirq.trace_distance_bound(ReturnsConstant(1.0)) == 1.0
    assert cirq.trace_distance_bound(ReturnsConstant(2.0)) == 1.0
