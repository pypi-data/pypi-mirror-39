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

import cirq
from io import open


def test_temp_file():
    with cirq.testing.TempFilePath() as file_path:
        with open(file_path, u'w') as f_write:
            f_write.write(u'Hello!\n')

        with open(file_path, u'r') as f_read:
            contents = f_read.read()

    assert contents == u'Hello!\n'

    with pytest.raises(IOError):
        # Can't open the file because it's deleted
        with open(file_path, u'r'):
            pass

    with pytest.raises(IOError):
        # Can't create a file because the directory is gone
        with open(file_path, u'w'):
            pass


def test_temp_dir():
    with cirq.testing.TempDirectoryPath() as dir_path:
        file_path = os.path.join(dir_path, u'file.txt')
        with open(file_path, u'w') as f_write:
            f_write.write(u'Hello!\n')

        with open(file_path, u'r') as f_read:
            contents = f_read.read()

    assert contents == u'Hello!\n'

    with pytest.raises(IOError):
        # Can't open the file because it's deleted
        with open(file_path, u'r'):
            pass

    with pytest.raises(IOError):
        # Can't create a file because the directory is gone
        with open(file_path, u'w'):
            pass
