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


Databases
---------

The commands available for databases are:

.. command-output:: beat databases --help

For instance, a list of the databases available locally can
be obtained as follows:

.. command-output:: beat databases list
   :cwd: ..

A list of the databases available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

   $ beat databases list --remote


Creating a new database
=======================

To create a new database locally, create the necessary files (see `database view python`_) and place them on your prefix.
Once done, use the following command to index the database:

.. code-block:: sh 
   
   $ beat database index <db>/1

and if you wan to upload it to the web server issue the following command:

.. code-block:: sh

   $ beat -p prefix -m <platform> -t <your-token> databases push <db>/1


Replace the string ``<db>`` with the fully qualified name of your database. For
example, ``mynewdatabase``. Replace ``<platform>`` by the address of the BEAT
platform you're trying to interact with. Replace ``<your-token>`` by your user
token (you can get that information via your settings window on the platform
itself).


.. note::

   To create a **new** version of an existing database, you must use the
   command-line tool slightly differently, as explained below. The above
   instructions will not work in this particular case.


Creating a new version of an existing database
==============================================

To create a new version of database locally, first download the current version
and locally create a new version from the current instance. Modify the new
version to fit your needs using a text editor of your choice and then upload
the new version.

.. code-block:: sh

   $ beat -p prefix -m <platform> -t <your-token> databases pull <db>/1
   ...
   $ beat -p prefix databases version <db>
   ...
   $ vim prefix/databases/<db>/2.*
   # once you're happy, upload the new version
   $ beat -p prefix -m <platform> -t <your-token> databases push <db>/2


Replace the string ``<db>`` with the name of your database. For example,
``mynewdatabase``. Replace ``<platform>`` by the address of the BEAT platform
you're trying to interact with. Replace ``<your-token>`` by your user token
(you can get that information via your settings window on the platform itself).

.. note:: 

   At the moment only users with administrative privilege can push databases to the web serve however all users can create and modify databases locally. 

.. include:: links.rst
