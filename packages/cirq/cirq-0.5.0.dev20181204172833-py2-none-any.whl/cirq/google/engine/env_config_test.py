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
import os
import pytest
from apiclient import discovery

import cirq
from cirq.testing.mock import mock


@mock.patch.object(discovery, u'build')
def test_engine_from_environment(build):
    # Api key present.
    with mock.patch.dict(os.environ,
                         {u'CIRQ_QUANTUM_ENGINE_API_KEY': u'key!'},
                         clear=True):
        eng = cirq.google.engine_from_environment()
        assert eng.default_project_id is None
        assert eng.api_key == u'key!'

    # Nothing present.
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError,
                           match=u'CIRQ_QUANTUM_ENGINE_API_KEY'):
            _ = cirq.google.engine_from_environment()

    # Default project id present.
    with mock.patch.dict(os.environ, {
        u'CIRQ_QUANTUM_ENGINE_DEFAULT_PROJECT_ID': u'project!'
    }, clear=True):
        with pytest.raises(EnvironmentError,
                           match=u'CIRQ_QUANTUM_ENGINE_API_KEY'):
            _ = cirq.google.engine_from_environment()

    # Both present.
    with mock.patch.dict(os.environ, {
        u'CIRQ_QUANTUM_ENGINE_DEFAULT_PROJECT_ID': u'project!',
        u'CIRQ_QUANTUM_ENGINE_API_KEY': u'key!',
    }, clear=True):
        eng = cirq.google.engine_from_environment()
        assert eng.default_project_id == u'project!'
        assert eng.api_key == u'key!'
