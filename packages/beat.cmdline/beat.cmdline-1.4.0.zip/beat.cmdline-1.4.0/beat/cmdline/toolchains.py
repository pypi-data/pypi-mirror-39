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

import click

from . import common
from .decorators import raise_on_error
from .click_helper import AliasedGroup


@click.group(cls=AliasedGroup)
@click.pass_context
def toolchains(ctx):
    """toolchains commands"""
    pass



@toolchains.command()
@click.option('--remote', help='Only acts on the remote copy of the list.',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
    '''Lists all the toolchains available on the platform.

    To list all existing toolchains on your local prefix:

        $ beat toolchains list
    '''
    if remote:
        with common.make_webapi(ctx.meta['config']) as webapi:
            return common.display_remote_list(webapi, 'toolchain')
    else:
        return common.display_local_list(ctx.meta['config'].path, 'toolchain')


@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of toolchain files

  Example:
    $ beat toolchains path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'toolchain', names)


@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local toolchain file

  Example:
    $ beat toolchains edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'toolchain',
                                name)


@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, names):
    '''Checks a local toolchain for validity.

    $ beat toolchains check xxx
    '''
    return common.check(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    '''Downloads the specified toolchains from the server.

       $ beat toolchains pull xxx.
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        status, downloaded = common.pull(
            webapi, ctx.meta['config'].path, 'toolchain', names,
            ['declaration', 'description'], force, indentation=0)
        return status



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--dry-run', help="Doesn't really perform the task, just "
              "comments what would do", is_flag=True)
@click.pass_context
@raise_on_error
def push(ctx, names, force, dry_run):
    '''Uploads toolchains to the server

    Example:
      $ beat toolchains push --dry-run yyy
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.push(
            webapi, ctx.meta['config'].path, 'toolchain', names,
            ['name', 'declaration', 'description'], {}, force, dry_run, 0
        )



@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def diff(ctx, name):
    '''Shows changes between the local dataformat and the remote version

    Example:
      $ beat toolchains diff xxx
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.diff(webapi, ctx.meta['config'].path, 'toolchain',
                           name, ['declaration', 'description'])



@toolchains.command()
@click.pass_context
@raise_on_error
def status(ctx):
    '''Shows (editing) status for all available toolchains

    Example:
      $ beat toolchains status
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.status(webapi, ctx.meta['config'].path, 'toolchain')[0]



@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def create(ctx, names):
    '''Creates a new local toolchain.

    $ beat toolchains create xxx
    '''
    return common.create(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def version(ctx, name):
    '''Creates a new version of an existing toolchain.

    $ beat toolchains version xxx
    '''
    return common.new_version(ctx.meta['config'].path, 'toolchain', name)



@toolchains.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.pass_context
@raise_on_error
def fork(ctx, src, dst):
    '''Forks a local toolchain.

    $ beat toolchains fork xxx yyy
    '''
    return common.fork(ctx.meta['config'].path, 'toolchain', src, dst)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--remote', help='Only acts on the remote copy.',
              is_flag=True)
@click.pass_context
@raise_on_error
def rm(ctx, names, remote):
    '''Deletes a local toolchain (unless --remote is specified).

    $ beat toolchains rm xxx
    '''
    if remote:
        with common.make_webapi(ctx.meta['config']) as webapi:
            return common.delete_remote(webapi, 'toolchain', names)
    else:
        return common.delete_local(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--path', help='Use path to write files to disk (instead of the '
              'current directory)', type=click.Path())
@click.pass_context
@raise_on_error
def draw(ctx, names, path):
    '''Creates a visual representation of the toolchain'''
    return common.dot_diagram(
        ctx.meta['config'].path, 'toolchain', names, path, []
    )
