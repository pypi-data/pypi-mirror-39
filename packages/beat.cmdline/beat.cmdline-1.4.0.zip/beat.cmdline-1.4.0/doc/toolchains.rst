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


Toolchains
----------

The commands available for toolchains are:

.. command-output:: beat toolchains --help

For instance, a list of the toolchains available locally can
be obtained as follows:

.. command-output:: beat toolchains list
   :cwd: ..

A list of the toolchains available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

  $ beat toolchains list --remote

.. _beat-cmdline-toolchains-checkscript:

How to check that a toolchain is correctly declared?
....................................................

To check that a toolchain declaration file is correctly written, the command
line tool can be used.

For example, we check a correct file (found in
``src/beat.core/beat/core/test/toolchains/integers_addition.json``):

.. code-block:: sh

    $ beat --prefix=src/beat.core/beat/core/test/ toolchains check \
      integers_addition
    The toolchain is executable!

Here, the ``--prefix`` option is used to tell the scripts where all our data
formats, toolchains and algorithms are located, and ``integers_addition`` is the
name of the toolchain we want to check (note that we don't add the ``.json``
extension, as this is the name of the toolchain, not the filename!).

Now we check a file that isn't a correctly formatted JSON file:

``src/beat.core/beat/core/test/toolchains/invalid/invalid.json``:


.. code-block:: json

   {
       "invalid": true,
   }


.. code-block:: sh

   $ beat --prefix=src/beat.core/beat/core/test/ toolchains check invalid/invalid
   The toolchain isn\'t valid, due to the following errors:
       Failed to decode the JSON file \'beat/src/beat.core/beat/core/test/toolchains/invalid/invalid.json\':
           Expecting property name enclosed in double quotes: line 3 column 1 (char 23)


Here we are told that something is wrong JSON-wise around the line 3, column 1
of the JSON file. The error is the ``,`` (comma) character: in JSON, the last
field of an object (``{}``) or the last element of an array (``[]``) cannot be
followed by a comma.  This is the corrected version:

.. code-block:: json

    {
        "invalid": true
    }

Also note that since we tell the script that all our toolchain declaration
files are located in ``src/beat.core/beat/core/test/toolchains/``, the
subfolders in that location are considered as part of the name of the data
formats they contains (like here ``invalid/invalid``).

As a last example, here is the result of the script when the toolchain
references unknown inputs and outputs (see the following sections for
explanations about the content of the declaration file):

``src/beat.core/beat/core/test/toolchains/invalid/empty_blocks_list.json``:

.. code-block:: json

    {
        "blocks": [],
        "databases": [ {
                "name": "integers",
                "outputs": {
                    "values": "single_integer"
                }
            }
        ],
        "connections": [ {
                "from": "integers.values",
                "to": "echo.in"
            }
        ],
        "results": [
            "echo.out"
        ]
    }


.. code-block:: sh

    $ beat --prefix=src/beat.core/beat/core/test/ toolchains check invalid/empty_blocks_list
    The toolchain isn\'t valid, due to the following errors:
        Unknown inputs: echo.in
        Unknown result outputs: echo.out

