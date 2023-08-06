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


# Basic tests for the command line beat program: databases

import nose.tools
import click
from click.testing import CliRunner
from . import platform, disconnected, prefix, tmp_prefix, user, token, temp_cwd

from beat.cmdline.scripts import main_cli
from beat.core.test.utils import slow, cleanup, skipif
from beat.core.database import Storage, Database


def index_integer_db():
    call('index', 'integers_db/1')


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)
  use_platform = kwargs.get('platform', platform)

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--test-mode', '--prefix', use_prefix, '--token', token,
        '--user', user, '--platform', use_platform, 'databases'] +
        list(args)
    )
  if result.exit_code != 0:
      click.echo(result.output)
  return result.exit_code


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
  nose.tools.eq_(call('list', '--remote'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_local_list():
  nose.tools.eq_(call('list'), 0)


@nose.tools.nottest
@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
  obj = 'simple/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)
  s = Storage(tmp_prefix, obj)
  assert s.exists()


@nose.tools.nottest
@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
  nose.tools.eq_(call('pull', prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
  obj = 'simple/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)

  # quickly modify the user algorithm by emptying it
  f = Database(tmp_prefix, obj)
  nose.tools.eq_(len(f.errors), 0, 'Failed to load Database: \n%s' % '\n'.join(f.errors))
  f.data['root_folder'] = '/a/different/path'
  f.write()

  nose.tools.eq_(call('diff', obj, prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
  test_diff()
  nose.tools.eq_(call('status', prefix=tmp_prefix), 0)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_good():
  nose.tools.eq_(call('view', 'integers_db/1/double/double'), 0)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_unknown_protocol():

  nose.tools.eq_(call('view', 'integers_db/1/single/double'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_unknown_set():
  nose.tools.eq_(call('view', 'integers_db/1/double/single'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_bad():
  nose.tools.eq_(call('view', 'integers_db/1/two_sets'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_invalid():
  nose.tools.eq_(call('view', 'invalid/1/default/set'), 1)


def test_index_unknown_database():
  nose.tools.eq_(call('index', 'foobar/1'), 1)


@nose.tools.with_setup(teardown=cleanup)
def test_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_list_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)
  nose.tools.eq_(call('index', '--list', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_delete_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)
  nose.tools.eq_(call('index', '--delete', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_index_all(): #bad and good, return != 0
  expected_errors = 16
  existing_errors = call('index')
  assert existing_errors >= expected_errors, "There should be at least %d " \
      "errors on installed databases, but I've found only %d" % \
      (expected_errors, existing_errors)
