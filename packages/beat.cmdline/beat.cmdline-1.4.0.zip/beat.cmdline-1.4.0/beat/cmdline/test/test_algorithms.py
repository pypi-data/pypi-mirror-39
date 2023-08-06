#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.cmdline module of the BEAT platform.          #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################


# Basic tests for the command line beat program: algorithms

import nose.tools
import os
import click
from click.testing import CliRunner
import shutil
import json

from . import platform, disconnected, prefix, tmp_prefix, user, token, temp_cwd
from ..common import Selector
from beat.cmdline.scripts import main_cli
from beat.core.test.utils import slow, cleanup, skipif
from beat.core.algorithm import Storage


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)
  use_platform = kwargs.get('platform', platform)
  use_cache = kwargs.get('cache', 'cache')

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--platform', use_platform, '--user', user, '--token', token,
         '--prefix', use_prefix, '--cache', use_cache, '--test-mode',
         'algorithms'] + list(args)
    )
    return result.exit_code, result.output


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
  exit_code, outputs = call('list', '--remote')
  nose.tools.eq_(exit_code, 0, msg=outputs)


@nose.tools.with_setup(teardown=cleanup)
def test_local_list():
  exit_code, outputs = call('list')
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
  obj = 'user/integers_add/1'
  exit_code, outputs = call('pull', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj)
  assert s.exists()


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
  exit_code, outputs = call('pull', prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
  obj = 'user/integers_add/1'
  exit_code, outputs = call('pull', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)

  # quickly modify the user algorithm by emptying it
  storage = Storage(tmp_prefix, obj)
  storage.code.save('class Algorithm:\n  pass')

  exit_code, outputs = call('diff', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
  test_diff()
  test_pull_one()
  exit_code, outputs = call('status', prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


def test_check_valid():
  obj = 'legacy/valid_algorithm/1'
  exit_code, outputs = call('check', obj)
  nose.tools.eq_(exit_code, 0, outputs)


def test_check_invalid():
  obj = 'legacy/no_inputs_declarations/1'
  exit_code, outputs = call('check', obj)
  nose.tools.eq_(exit_code, 1, outputs)


@nose.tools.with_setup(teardown=cleanup)
def test_create(obj=None):
  obj = obj or 'legacy/algorithm/1'
  exit_code, outputs = call('create', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj)
  assert s.exists()
  return s


@nose.tools.with_setup(teardown=cleanup)
def test_new_version():
  obj = 'legacy/algorithm/1'
  test_create(obj)
  obj2 = 'legacy/algorithm/2'
  exit_code, outputs = call('version', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj2)
  assert s.exists()

  # check version status
  with Selector(tmp_prefix) as selector:
    assert selector.version_of('algorithm', obj2) == obj


@nose.tools.with_setup(teardown=cleanup)
def test_fork():
  obj = 'legacy/algorithm/1'
  test_create(obj)
  obj2 = 'legacy/different/1'
  exit_code, outputs = call('fork', obj, obj2, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj2)
  assert s.exists()

  # check fork status
  with Selector(tmp_prefix) as selector:
    assert selector.forked_from('algorithm', obj2) == obj


@nose.tools.with_setup(teardown=cleanup)
def test_delete_local():
  obj = 'legacy/algorithm/1'
  storage = test_create(obj)

  # quickly make sure it exists
  storage = Storage(tmp_prefix, obj)
  assert storage.exists()

  exit_code, outputs = call('rm', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  assert not storage.exists()


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_push_and_delete():
  obj = 'user/newobject/1'
  test_create(obj)

  # now push the new object and then delete it remotely
  exit_code, outputs = call('push', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  exit_code, outputs = call('rm', '--remote', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
