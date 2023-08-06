.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.cmdline module of the BEAT platform.         ..
..                                                                            ..
.. Commercial License Usage                                                   ..
.. Licensees holding valid commercial BEAT licenses may use this file in      ..
.. accordance with the terms contained in a written agreement between you     ..
.. and Idiap. For further information contact tto@idiap.ch                    ..
..                                                                            ..
.. Alternatively, this file may be used under the terms of the GNU Affero     ..
.. Public License version 3 as published by the Free Software and appearing   ..
.. in the file LICENSE.AGPL included in the packaging of this file.           ..
.. The BEAT platform is distributed in the hope that it will be useful, but   ..
.. WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ..
.. or FITNESS FOR A PARTICULAR PURPOSE.                                       ..
..                                                                            ..
.. You should have received a copy of the GNU Affero Public License along     ..
.. with the BEAT platform. If not, see http://www.gnu.org/licenses/.          ..

.. _beat-cmdline-introduction:

Introduction
============
The user objects (data formats, toolchains, experiments, etc) are stored
locally in a directory with specific structure that is commonly referred to as
a **prefix** (see `Prefix`_). The user objects on the web platform are
also stored in a similar directory structure. It is possible to extract a
representation from the objects on the BEAT web server and interact with them
locally. Local object copies contain the same amount of information that is
displayed through the web interface.

The BEAT command-line utility can be used for simple functionalities (e.g.
deleting an existing algorithm or making small modifications) or advanced
tasks (e.g. database development, experiment debugging) both for local objects
and remote objects. In order to make this possible for the remote objects, the
web platform provides a RESTful API which third-party applications can use to
list, query and modify existing remote objects.


The ``beat`` command-line utility bridges user interaction with a remote BEAT
web platform and locally available objects in a seamless way:

.. command-output:: beat --help

The command-line interface is separated in subcommands, for acting on specific
objects. Actions can be driven to operate on locally installed
or remotely available objects. You'll find detailed information about
sub-commands on specific sub-sections of this documentation dedicated to that
particular type of object. In :ref:`beat-cmdline-configuration`, we cover basic usage and
configuration only.

.. include:: links.rst
