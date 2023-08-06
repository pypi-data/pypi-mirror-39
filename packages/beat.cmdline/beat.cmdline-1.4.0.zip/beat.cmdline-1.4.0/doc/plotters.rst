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


.. _beat-cmdline-plotters:

Plotters
--------

The commands available for plotterparameters are:

.. command-output:: beat plotters --help

For instance, a list of the plotters available locally can
be obtained as follows:

.. command-output:: beat plotters list
   :cwd: ..

A list of the plotters available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

   $ beat plotters list --remote

How to plot a figure?
.........................

The command ``beat plotters plot <name>`` can be used to plot data using a
specific plotter.

There a many ways to plot data:

* Using sample data:

.. code-block:: sh

  $ beat plotter plot --sample_data plottername

* passing some private input data (no sample_data required here), specific plotterparameter and output image name

.. code-block:: sh

  $ beat plotter plot plottername --inputdata inputdata.json --outputimage outputimage.png --plotterparameter plotterparameter

  * inputdata.json is the filename containing data
  * outputimage is the name of the saved image
  * plotter the name of the plotter (e.g.: plot/bar/1)
  * plotterparameter the name of the plotterparameter (e.g.: plot/bar/1)

* without specifing the output image:

.. code-block:: sh

  $ beat plotter plot plottername --inputdata inputdata.json --plotterparameter plotterparameter

  * The image gets saved under the plotter path with default name "output_image.png"

Take into account that some extra options are available such as '--show' which will pop out the generated plots on your screen.
