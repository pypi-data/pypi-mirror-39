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

u"""Tests for engine."""
from __future__ import with_statement
from __future__ import absolute_import
import base64
import re

import numpy as np
import pytest

from apiclient import discovery

import cirq
import cirq.google as cg
from cirq.testing.mock import mock


_A_RESULT = {
    u'sweepResults': [
        {
            u'repetitions': 1,
            u'measurementKeys': [
                {
                    u'key': u'q',
                    u'qubits': [{u'row': 1, u'col': 1}]
                }
            ],
            u'parameterizedResults': [
                {
                    u'params': {u'assignments': {u'a': 1}},
                    u'measurementResults': base64.b64encode('01')
                }
            ]
        }
    ]
}


_RESULTS = {
    u'sweepResults': [
        {
            u'repetitions': 1,
            u'measurementKeys': [
                {
                    u'key': u'q',
                    u'qubits': [{u'row': 1, u'col': 1}]
                }
            ],
            u'parameterizedResults': [
                {
                    u'params': {u'assignments': {u'a': 1}},
                    u'measurementResults': base64.b64encode('01')
                },
                {
                    u'params': {u'assignments': {u'a': 2}},
                    u'measurementResults': base64.b64encode('01')
                }
            ]
        }
    ]
}


@cirq.testing.only_test_in_python3
def test_repr():
    v = cirq.google.JobConfig(project_id=u'my-project-id',
                              program_id=u'my-program-id',
                              job_id=u'my-job-id')

    assert repr(v) == (u"JobConfig(project_id='my-project-id', "
                       u"program_id='my-program-id', "
                       u"job_id='my-job-id', gcs_prefix=None, "
                       u"gcs_program=None, gcs_results=None)")


@mock.patch.object(discovery, u'build')
def test_run_circuit(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'SUCCESS'}}
    jobs.getResult().execute.return_value = {
        u'result': _A_RESULT}

    result = cg.Engine(api_key=u"key").run(
        program=cirq.Circuit(),
        job_config=cg.JobConfig(u'project-id', gcs_prefix=u'gs://bucket/folder'))
    assert result.repetitions == 1
    assert result.params.param_dict == {u'a': 1}
    assert result.measurements == {u'q': np.array([[0]], dtype=u'uint8')}
    build.assert_called_with(u'quantum', u'v1alpha1',
                             discoveryServiceUrl=(u'https://{api}.googleapis.com'
                                                  u'/$discovery/rest?version='
                                                  u'{apiVersion}&key=key'))
    assert programs.create.call_args[1][u'parent'] == u'projects/project-id'
    assert jobs.create.call_args[1][
        u'parent'] == u'projects/project-id/programs/test'
    assert jobs.get().execute.call_count == 1
    assert jobs.getResult().execute.call_count == 1


@mock.patch.object(discovery, u'build')
def test_circuit_device_validation_fails(build):
    circuit = cirq.Circuit(device=cg.Foxtail)

    # Purposefully create an invalid Circuit by fiddling with internal bits.
    # This simulates a failure in the incremental checks.
    circuit._moments.append(cirq.Moment([
        cirq.Z(cirq.NamedQubit(u"dorothy"))]))

    with pytest.raises(ValueError, match=u'Unsupported qubit type'):
        cg.Engine(api_key=u"key").run(program=circuit,
                                     job_config=cg.JobConfig(u'project-id'))


@mock.patch.object(discovery, u'build')
def test_schedule_device_validation_fails(build):
    scheduled_op = cirq.ScheduledOperation(time=None, duration=None,
                                           operation=cirq.H.on(
                                               cirq.NamedQubit(u"dorothy")))
    schedule = cirq.Schedule(device=cg.Foxtail,
                             scheduled_operations=[scheduled_op])

    with pytest.raises(ValueError):
        cg.Engine(api_key=u"key").run(
            program=schedule,
            job_config=cg.JobConfig(u'project-id'))


@mock.patch.object(discovery, u'build')
def test_circuit_device_validation_passes_non_xmon_gate(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'SUCCESS'}}
    jobs.getResult().execute.return_value = {
        u'result': _A_RESULT}

    circuit = cirq.Circuit.from_ops(cirq.H.on(cirq.GridQubit(0, 1)),
                                    device=cg.Foxtail)
    result = cg.Engine(api_key=u"key").run(
        program=circuit,
        job_config=cg.JobConfig(u'project-id'))
    assert result.repetitions == 1


@mock.patch.object(discovery, u'build')
def test_unsupported_program_type(build):
    eng = cg.Engine(api_key=u"key")
    with pytest.raises(TypeError, match=u'program'):
        eng.run(program=u"this isn't even the right type of thing!",
                job_config=cg.JobConfig(u'project-id'))


@mock.patch.object(discovery, u'build')
def test_run_circuit_failed(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'FAILURE'}}

    with pytest.raises(RuntimeError, match=u'It is in state FAILURE'):
        cg.Engine(api_key=u"key").run(
            program=cirq.Circuit(),
            job_config=cg.JobConfig(u'project-id',
                                    gcs_prefix=u'gs://bucket/folder'))


@mock.patch.object(discovery, u'build')
def test_default_prefix(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'SUCCESS'}}
    jobs.getResult().execute.return_value = {
        u'result': _A_RESULT}

    result = cg.Engine(api_key=u"key").run(
        program=cirq.Circuit(),
        job_config=cg.JobConfig(u'org.com:project-id'))
    assert result.repetitions == 1
    assert result.params.param_dict == {u'a': 1}
    assert result.measurements == {u'q': np.array([[0]], dtype=u'uint8')}
    build.assert_called_with(u'quantum', u'v1alpha1',
                             discoveryServiceUrl=(u'https://{api}.googleapis.com'
                                                  u'/$discovery/rest?version='
                                                  u'{apiVersion}&key=key'))
    assert programs.create.call_args[1][u'body'][u'gcs_code_location'][
        u'uri'].startswith(u'gs://gqe-project-id/programs/')


@mock.patch.object(discovery, u'build')
def test_run_sweep_params(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'SUCCESS'}}
    jobs.getResult().execute.return_value = {
        u'result': _RESULTS}

    job = cg.Engine(api_key=u"key").run_sweep(
        program=cirq.moment_by_moment_schedule(cirq.UnconstrainedDevice,
                                               cirq.Circuit()),
        job_config=cg.JobConfig(u'project-id', gcs_prefix=u'gs://bucket/folder'),
        params=[cirq.ParamResolver({u'a': 1}), cirq.ParamResolver({u'a': 2})])
    results = job.results()
    assert len(results) == 2
    for i, v in enumerate([1, 2]):
        assert results[i].repetitions == 1
        assert results[i].params.param_dict == {u'a': v}
        assert results[i].measurements == {u'q': np.array([[0]], dtype=u'uint8')}
    build.assert_called_with(u'quantum', u'v1alpha1',
                             discoveryServiceUrl=(u'https://{api}.googleapis.com'
                                                  u'/$discovery/rest?version='
                                                  u'{apiVersion}&key=key'))
    assert programs.create.call_args[1][u'parent'] == u'projects/project-id'
    sweeps = programs.create.call_args[1][u'body'][u'code'][u'parameter_sweeps']
    assert len(sweeps) == 2
    for i, v in enumerate([1, 2]):
        assert sweeps[i][u'repetitions'] == 1
        assert sweeps[i][u'sweep'][u'factors'][0][u'sweeps'][0][u'points'][
            u'points'] == [v]
    assert jobs.create.call_args[1][
        u'parent'] == u'projects/project-id/programs/test'
    assert jobs.get().execute.call_count == 1
    assert jobs.getResult().execute.call_count == 1


@mock.patch.object(discovery, u'build')
def test_run_sweep_sweeps(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'SUCCESS'}}
    jobs.getResult().execute.return_value = {
        u'result': _RESULTS}

    job = cg.Engine(api_key=u"key").run_sweep(
        program=cirq.moment_by_moment_schedule(cirq.UnconstrainedDevice,
                                               cirq.Circuit()),
        job_config=cg.JobConfig(u'project-id', gcs_prefix=u'gs://bucket/folder'),
        params=cirq.Points(u'a', [1, 2]))
    results = job.results()
    assert len(results) == 2
    for i, v in enumerate([1, 2]):
        assert results[i].repetitions == 1
        assert results[i].params.param_dict == {u'a': v}
        assert results[i].measurements == {u'q': np.array([[0]], dtype=u'uint8')}
    build.assert_called_with(u'quantum', u'v1alpha1',
                             discoveryServiceUrl=(u'https://{api}.googleapis.com'
                                                  u'/$discovery/rest?version='
                                                  u'{apiVersion}&key=key'))
    assert programs.create.call_args[1][u'parent'] == u'projects/project-id'
    sweeps = programs.create.call_args[1][u'body'][u'code'][u'parameter_sweeps']
    assert len(sweeps) == 1
    assert sweeps[0][u'repetitions'] == 1
    assert sweeps[0][u'sweep'][u'factors'][0][u'sweeps'][0][u'points'][
        u'points'] == [1, 2]
    assert jobs.create.call_args[1][
        u'parent'] == u'projects/project-id/programs/test'
    assert jobs.get().execute.call_count == 1
    assert jobs.getResult().execute.call_count == 1


@mock.patch.object(discovery, u'build')
def test_bad_priority(build):
    eng = cg.Engine(api_key=u"key")
    with pytest.raises(ValueError, match=u'priority must be'):
        eng.run(program=cirq.Circuit(),
                job_config=cg.JobConfig(u'project-id',
                                        gcs_prefix=u'gs://bucket/folder'),
                priority=1001)


@mock.patch.object(discovery, u'build')
def test_cancel(build):
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    jobs = programs.jobs()
    programs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test'}
    jobs.create().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'READY'}}
    jobs.get().execute.return_value = {
        u'name': u'projects/project-id/programs/test/jobs/test',
        u'executionStatus': {u'state': u'CANCELLED'}}

    job = cg.Engine(api_key=u"key").run_sweep(
        program=cirq.Circuit(),
        job_config=cg.JobConfig(u'project-id', gcs_prefix=u'gs://bucket/folder'))
    job.cancel()
    assert job.job_resource_name == (u'projects/project-id/programs/test/'
                                     u'jobs/test')
    assert job.status() == u'CANCELLED'
    assert jobs.cancel.call_args[1][
        u'name'] == u'projects/project-id/programs/test/jobs/test'


@mock.patch.object(discovery, u'build')
def test_program_labels(build):
    program_name = u'projects/my-proj/programs/my-prog'
    service = mock.Mock()
    build.return_value = service
    programs = service.projects().programs()
    engine = cg.Engine(api_key=u"key")

    def body():
        return programs.patch.call_args[1][u'body']

    programs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'}}
    engine.add_program_labels(program_name, {u'a': u'2', u'c': u'1'})

    assert body()[u'labels'] == {u'a': u'2', u'b': u'1', u'c': u'1'}
    assert body()[u'labelFingerprint'] == u''

    programs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'},
                                           u'labelFingerprint': u'abcdef'}
    engine.set_program_labels(program_name, {u's': u'1', u'p': u'1'})
    assert body()[u'labels'] == {u's': u'1', u'p': u'1'}
    assert body()[u'labelFingerprint'] == u'abcdef'

    programs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'},
                                           u'labelFingerprint': u'abcdef'}
    engine.remove_program_labels(program_name, [u'a', u'c'])
    assert body()[u'labels'] == {u'b': u'1'}
    assert body()[u'labelFingerprint'] == u'abcdef'


@mock.patch.object(discovery, u'build')
def test_job_labels(build):
    job_name = u'projects/my-proj/programs/my-prog/jobs/my-job'
    service = mock.Mock()
    build.return_value = service
    jobs = service.projects().programs().jobs()
    engine = cg.Engine(api_key=u"key")

    def body():
        return jobs.patch.call_args[1][u'body']

    jobs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'}}
    engine.add_job_labels(job_name, {u'a': u'2', u'c': u'1'})

    assert body()[u'labels'] == {u'a': u'2', u'b': u'1', u'c': u'1'}
    assert body()[u'labelFingerprint'] == u''

    jobs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'},
                                       u'labelFingerprint': u'abcdef'}
    engine.set_job_labels(job_name, {u's': u'1', u'p': u'1'})
    assert body()[u'labels'] == {u's': u'1', u'p': u'1'}
    assert body()[u'labelFingerprint'] == u'abcdef'

    jobs.get().execute.return_value = {u'labels': {u'a': u'1', u'b': u'1'},
                                       u'labelFingerprint': u'abcdef'}
    engine.remove_job_labels(job_name, [u'a', u'c'])
    assert body()[u'labels'] == {u'b': u'1'}
    assert body()[u'labelFingerprint'] == u'abcdef'


@mock.patch.object(discovery, u'build')
def test_implied_job_config_project_id(build):
    eng = cg.Engine(api_key=u"key")
    with pytest.raises(ValueError, match=u'project id'):
        _ = eng.implied_job_config(None)
    with pytest.raises(ValueError, match=u'project id'):
        _ = eng.implied_job_config(cg.JobConfig())
    assert eng.implied_job_config(
        cg.JobConfig(project_id=u'specific')).project_id == u'specific'

    eng_with = cg.Engine(api_key=u"key", default_project_id=u'default')

    # Fallback to default.
    assert eng_with.implied_job_config(None).project_id == u'default'

    # Override default.
    assert eng_with.implied_job_config(
        cg.JobConfig(project_id=u'specific')).project_id == u'specific'


@mock.patch.object(discovery, u'build')
def test_implied_job_config_gcs_prefix(build):
    eng = cg.Engine(api_key=u"key")
    config = cg.JobConfig(project_id=u'project_id')

    # Implied by project id.
    assert eng.implied_job_config(config).gcs_prefix == u'gs://gqe-project_id/'

    # Bad default.
    eng_with_bad = cg.Engine(api_key=u"key", default_gcs_prefix=u'bad_prefix')
    with pytest.raises(ValueError, match=u'gcs_prefix must be of the form'):
        _ = eng_with_bad.implied_job_config(config)

    # Good default without slash.
    eng_with = cg.Engine(api_key=u"key", default_gcs_prefix=u'gs://good')
    assert eng_with.implied_job_config(config).gcs_prefix == u'gs://good/'

    # Good default with slash.
    eng_with = cg.Engine(api_key=u"key", default_gcs_prefix=u'gs://good/')
    assert eng_with.implied_job_config(config).gcs_prefix == u'gs://good/'

    # Bad override.
    config.gcs_prefix = u'bad_prefix'
    with pytest.raises(ValueError, match=u'gcs_prefix must be of the form'):
        _ = eng.implied_job_config(config)
    with pytest.raises(ValueError, match=u'gcs_prefix must be of the form'):
        _ = eng_with_bad.implied_job_config(config)

    # Good override without slash.
    config.gcs_prefix = u'gs://better'
    assert eng.implied_job_config(config).gcs_prefix == u'gs://better/'
    assert eng_with.implied_job_config(config).gcs_prefix == u'gs://better/'

    # Good override with slash.
    config.gcs_prefix = u'gs://better/'
    assert eng.implied_job_config(config).gcs_prefix == u'gs://better/'
    assert eng_with.implied_job_config(config).gcs_prefix == u'gs://better/'


@cirq.testing.only_test_in_python3  # uses re.fullmatch
@mock.patch.object(discovery, u'build')
def test_implied_job_config(build):
    eng = cg.Engine(api_key=u"key")

    # Infer all from project id.
    implied = eng.implied_job_config(cg.JobConfig(project_id=u'project_id'))
    assert implied.project_id == u'project_id'
    assert re.fullmatch(ur'prog-[0-9A-Z]+', implied.program_id)
    assert implied.job_id == u'job-0'
    assert implied.gcs_prefix == u'gs://gqe-project_id/'
    assert re.fullmatch(
        ur'gs://gqe-project_id/programs/prog-[0-9A-Z]+/prog-[0-9A-Z]+',
        implied.gcs_program)
    assert re.fullmatch(
        ur'gs://gqe-project_id/programs/prog-[0-9A-Z]+/jobs/job-0',
        implied.gcs_results)

    # Force program id.
    implied = eng.implied_job_config(cg.JobConfig(
        project_id=u'j',
        program_id=u'g'))
    assert implied.project_id == u'j'
    assert implied.program_id == u'g'
    assert implied.job_id == u'job-0'
    assert implied.gcs_prefix == u'gs://gqe-j/'
    assert implied.gcs_program == u'gs://gqe-j/programs/g/g'
    assert implied.gcs_results == u'gs://gqe-j/programs/g/jobs/job-0'

    # Force all.
    implied = eng.implied_job_config(cg.JobConfig(
        project_id=u'a',
        program_id=u'b',
        job_id=u'c',
        gcs_prefix=u'gs://d',
        gcs_program=u'e',
        gcs_results=u'f'))
    assert implied.project_id == u'a'
    assert implied.program_id == u'b'
    assert implied.job_id == u'c'
    assert implied.gcs_prefix == u'gs://d/'
    assert implied.gcs_program == u'e'
    assert implied.gcs_results == u'f'


@mock.patch.object(discovery, u'build')
def test_bad_job_config_inference_order(build):
    eng = cg.Engine(api_key=u"key")
    config = cg.JobConfig()

    with pytest.raises(ValueError):
        eng._infer_gcs_prefix(config)
    config.project_id = u'project'

    with pytest.raises(ValueError):
        eng._infer_gcs_results(config)
    with pytest.raises(ValueError):
        eng._infer_gcs_program(config)
    eng._infer_gcs_prefix(config)

    eng._infer_gcs_results(config)
    eng._infer_gcs_program(config)
