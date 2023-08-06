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

import logging
import click

import oset

from beat.core import dataformat


from . import common
from .decorators import raise_on_error
from .click_helper import AliasedGroup

logger = logging.getLogger(__name__)


def pull_impl(webapi, prefix, names, force, indentation, cache):
  """Copies dataformats (recursively) from the server.

  Data formats are particularly tricky to download because of their recursive
  nature. This requires a specialized recursive technique to download base and
  referenced dataformats.


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to retrieve objects. If the list is empty, then we pull all
      available objects of a given type. If no user is set, then pull all
      public objects of a given type.

    force (bool): If set to ``True``, then overwrites local changes with the
      remotely retrieved copies.

    indentation (int): The indentation level, useful if this function is called
      recursively while downloading different object types. This is normally
      set to ``0`` (zero).

    cache (dict): A dictionary containing all dataformats already downloaded.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

  dataformats = oset.oset(names) #what is being request
  download = dataformats - oset.oset(cache.keys()) #what we actually need

  if not download: return 0

  status, downloaded = common.pull(webapi, prefix, 'dataformat', download,
                                   ['declaration', 'description'], force, indentation)

  if status != 0: return status

  indent = indentation * ' '

  # see what else one needs to pull
  for name in downloaded:
    try:
      obj = dataformat.DataFormat(prefix, name)
      cache[name] = obj
      if not obj.valid:
        cache[name] = None

      # downloads any dependencies
      dataformats |= obj.referenced.keys()

    except Exception as e:
      logger.error("loading `%s': %s...", name, str(e))
      cache[name] = None

  # recurse until done
  return pull_impl(webapi, prefix, dataformats, force, 2+indentation, cache)

@click.group(cls=AliasedGroup)
@click.pass_context
def dataformats(ctx):
    """Configuration manipulation of data formats"""
    pass


@dataformats.command()
@click.option('--remote', help='Only acts on the remote copy of the dataformat',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
  '''Lists all the dataformats available on the platform

  Example:
    $ beat dataformats list --remote
  '''
  if remote:
    with common.make_webapi(ctx.meta['config']) as webapi:
      return common.display_remote_list(webapi, 'dataformat')
  else:
    return common.display_local_list(ctx.meta['config'].path, 'dataformat')


@dataformats.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of dataformats files

  Example:
    $ beat dataformats path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'dataformat', names)


@dataformats.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local dataformat file

  Example:
    $ beat df edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'dataformat',
                                name)


@dataformats.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, names):
  '''Checks a local dataformat for validity

  Example:
    $ beat dataformats check xxx
  '''
  return common.check(ctx.meta['config'].path, 'dataformat', names)


@dataformats.command()
@click.argument('name', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, name, force):
  '''Downloads the specified dataformats from the server

  Example:
    $ beat dataformats pull --force yyy
  '''
  with common.make_webapi(ctx.meta['config']) as webapi:
    name = common.make_up_remote_list(webapi, 'dataformat', name)
    if name is None:
        return 1 #error
    return pull_impl(webapi, ctx.meta['config'].path, name,force, 0, {})


@dataformats.command()
@click.argument('name', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--dry-run', help="Doesn't really perform the task, just "
              "comments what would do", is_flag=True)
@click.pass_context
@raise_on_error
def push(ctx, name, force, dry_run):
  '''Uploads dataformats to the server

  Example:
    $ beat dataformats push --dry-run yyy
  '''
  with common.make_webapi(ctx.meta['config']) as webapi:
    return common.push(
        webapi, ctx.meta['config'].path, 'dataformat',
        name, ['name', 'declaration', 'description'], {},
        force, dry_run, 0
    )


@dataformats.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def diff(ctx, name):
  '''Shows changes between the local dataformat and the remote version

  Example:
    $ beat dataformats diff xxx
  '''
  with common.make_webapi(ctx.meta.get('config')) as webapi:
    return common.diff(webapi, ctx.meta.get('config').path, 'dataformat',
                       name, ['declaration', 'description'])


@dataformats.command()
@click.pass_context
@raise_on_error
def status(ctx):
  '''Shows (editing) status for all available dataformats

  Example:
    $ beat dataformats status
  '''
  with common.make_webapi(ctx.meta['config']) as webapi:
    return common.status(webapi, ctx.meta['config'].path, 'dataformat')[0]


@dataformats.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def create(ctx, names):
  '''Creates a new local dataformat

  Example:
    $ beat dataformats create xxx
  '''
  return common.create(ctx.meta['config'].path, 'dataformat', names)


@dataformats.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def version(ctx, name):
  '''Creates a new version of an existing dataformat

  Example:
    $ beat dataformats version xxx
  '''
  return common.new_version(ctx.meta['config'].path, 'dataformat', name)


@dataformats.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.pass_context
@raise_on_error
def fork(ctx, src, dst):
  '''Forks a local dataformat

  Example:
      $ beat dataformats fork xxx yyy
  '''
  return common.fork(ctx.meta['config'].path, 'dataformat', src, dst)


@dataformats.command()
@click.argument('name', nargs=-1)
@click.option('--remote', help='Only acts on the remote copy of the dataformat',
              is_flag=True)
@click.pass_context
@raise_on_error
def rm(ctx, name, remote):
  '''Deletes a local dataformat (unless --remote is specified)

  Example:
      $ beat dataformats rm xxx
  '''
  if remote:
    with common.make_webapi(ctx.meta['config']) as webapi:
      return common.delete_remote(webapi, 'dataformat', name)
  else:
    return common.delete_local(ctx.meta['config'].path, 'dataformat', name)
