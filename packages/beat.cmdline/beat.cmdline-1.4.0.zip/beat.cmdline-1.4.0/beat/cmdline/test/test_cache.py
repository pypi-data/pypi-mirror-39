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


# Basic tests for the command line beat program: cache

import os
import click
from click.testing import CliRunner
import nose.tools

from . import prefix, tmp_prefix, temp_cwd
from .utils import index_experiment_dbs

from beat.cmdline.scripts import main_cli

from beat.core.test.utils import cleanup, slow


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--test-mode', '--prefix', use_prefix, '--cache', tmp_prefix] +
        list(args)
    )
  return result.exit_code, result.output


def setup_module():
  experiment_name = 'user/user/double_triangle/1/double_triangle'

  index_experiment_dbs(experiment_name)

  call('experiments', 'run', experiment_name)

def teardown_module():
  cleanup()


@slow
def test_cache_info():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'info')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', 'info', '--sizes')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', '--start', 0, 'info')
  nose.tools.eq_(ex_code, 0, out)


@slow
def test_cache_view():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'view')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', '--start', 0, 'view')
  nose.tools.eq_(ex_code, 0, out)


@slow
def test_cache_clear():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'clear')
  nose.tools.eq_(ex_code, 0, out)
  nose.tools.eq_(len(os.listdir(tmp_prefix)), 0)
