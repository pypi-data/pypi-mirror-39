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

# Basic setup for command test

import os
import sys
import tempfile
import shutil
import subprocess
import pkg_resources
import contextlib

import six.moves.urllib as urllib

from beat.core.test import tmp_prefix, teardown_package

platform = os.environ.get('BEAT_CMDLINE_TEST_PLATFORM', '')

disconnected = True
if platform:

  # the special name 'django' makes as believe it is connected
  if platform.startswith('django://'):
    # sets up django infrastructure, preloads test data
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', platform[9:])
    import django
    django.setup()

    # presets django database for tests
    from django.core.management import call_command
    call_command('install', 'test', interactive=False, verbose=1)

    disconnected = False

  else: #test it, actually
    # some patching to prevent common problems
    if not platform.endswith('/'): platform += '/'
    if not platform.startswith('http'): platform = 'http://' + platform
    try:
      code = urllib.request.urlopen(platform).getcode()
      disconnected = code != 200
    except (IOError, urllib.URLError):
      disconnected = True
else:
  platform = 'User did not set $BEAT_CMDLINE_TEST_PLATFORM'

user = 'user'
token = '4'


if sys.platform == 'darwin':
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix',
                                     dir='/tmp')
else:
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix')

prefix = os.path.join(prefix_folder, 'prefix')


def setup_package():
    prefixes = [
      pkg_resources.resource_filename('beat.backend.python.test', 'prefix'),
      pkg_resources.resource_filename('beat.core.test', 'prefix')
    ]

    for path in prefixes:
        subprocess.check_call(['rsync', '-arz', path, prefix_folder])


def teardown_package():
    shutil.rmtree(prefix_folder)


@contextlib.contextmanager
def temp_cwd():
    tempdir = tempfile.mkdtemp(prefix=__name__, suffix='.cwd')
    curdir = os.getcwd()
    os.chdir(tempdir)
    try: yield tempdir
    finally:
      os.chdir(curdir)
      shutil.rmtree(tempdir)
