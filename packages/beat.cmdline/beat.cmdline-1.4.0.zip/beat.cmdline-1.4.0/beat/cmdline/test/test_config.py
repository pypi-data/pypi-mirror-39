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


# Basic tests for the command line beat program: config

import os
import click
from click.testing import CliRunner
import nose.tools
from nose.tools import assert_raises
import simplejson

from . import tmp_prefix, temp_cwd
from beat.core.test.utils import cleanup
from .. import config
from .. import common
from beat.cmdline.scripts import main_cli


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''
  use_prefix = kwargs.get('prefix', tmp_prefix)

  runner = CliRunner()
  result = runner.invoke(
    main_cli.main,
    ['--test-mode', '--prefix', use_prefix] +
    list(args)
  )
  if result.exit_code != 0:
      click.echo(result.output)
  return result.exit_code


def test_config_list():
  nose.tools.eq_(call('config', 'show'), 0)


def test_config_cache():
  cache_dir = 'cache'

  c = config.Configuration({'--cache': cache_dir})
  nose.tools.eq_(c.cache, os.path.join(c.path, cache_dir))

  cache_dir = '/an/absolute/cache/dir'
  c = config.Configuration({'--cache': cache_dir})
  nose.tools.eq_(c.cache, cache_dir)


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_token():
  token_value = '123456abcdefffff'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_multiple():
  token_value = '123456abcde123456abcde123456abcdefff123456abcdef'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value

  # then we reduce the token size and see if the written file gets messed-up
  token_value = '123456'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_atnt_db():
  db_config = 'database/atnt'
  db_path = './atnt_db'
  nose.tools.eq_(call('config', 'set', '--local', db_config, db_path), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents[db_config] == db_path


@nose.tools.with_setup(teardown=cleanup)
def test_set_get_local_atnt_db():
  db_config = 'database/atnt'
  db_path = './atnt_db'
  nose.tools.eq_(call('config', 'set', '--local', db_config, db_path), 0)
  nose.tools.eq_(call('config', 'get', db_config), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_set_bad_config_key():
  db_config = 'fail'
  nose.tools.eq_(call('config', 'set', '--local', db_config, db_config), 1)


@nose.tools.with_setup(teardown=cleanup)
def test_get_bad_config_key():
  db_config = 'fail'
  nose.tools.eq_(call('config', 'get', db_config), -1)


@nose.tools.with_setup(teardown=cleanup)
def test_get_token():
  nose.tools.eq_(call('config', 'set', '--local', 'token', '12we3f45fgh'), 0)
  nose.tools.eq_(call('config', 'get', 'token'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_get_editor():
  nose.tools.eq_(call('config', 'set', '--local', 'editor', 'vi'), 0)
  nose.tools.eq_(call('config', 'get', 'editor'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_editor():
  editor_value = 'editor'
  with temp_cwd() as d:
    nose.tools.eq_(call('config', 'set', '--local', 'editor', editor_value), 0)
    config = os.path.join(d, '.beatrc')
    assert os.path.exists(config)
    with open(config, 'rt') as f: contents = simplejson.load(f)
    assert contents['editor'] == editor_value


def create_touch_file(tmp_prefix, editor):
  cmd = "%s %s && %s %s" % ('mkdir -p', os.path.join(tmp_prefix, 'plotters'), 'touch', os.path.join(tmp_prefix, 'plotters', 'test.py'))
  os.system(cmd)
  result = common.edit_local_file(tmp_prefix, editor, 'plotter', "test")
  return result


def read_data(tmp_prefix):
  with open(os.path.join(tmp_prefix, 'plotters', 'test.py'), 'r') as f:
      read_data = f.read().split('\n')[0]
  f.closed
  return read_data


def clean_tmp_files(tmp_prefix):
  cmd = "%s %s" % ('rm -fr', os.path.join(tmp_prefix, 'plotters'))
  os.system(cmd)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_editor_set():
  editor = None
  os.environ['VISUAL'] = ''
  os.environ['EDITOR'] = ''

  result = create_touch_file(tmp_prefix, editor)
  assert result == 1

  data = read_data(tmp_prefix)
  assert len(data) == 0

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_local_editor():
  editor = None
  os.environ['VISUAL'] = 'echo "2" >'
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "2"

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_local_editor_set():
  editor = 'echo "1" >'
  os.environ['VISUAL'] = 'echo "2" >'
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "1"

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_local_editor_no_visual():
  editor = None
  os.environ['VISUAL'] = ''
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "3"

  clean_tmp_files(tmp_prefix)
