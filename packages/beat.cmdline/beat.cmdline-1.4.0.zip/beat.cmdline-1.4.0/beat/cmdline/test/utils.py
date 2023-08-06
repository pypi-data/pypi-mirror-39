# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2018 Idiap Research Institute, http://www.idiap.ch/           #
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

"""
Helper functions to run tests
"""

import os
import logging

from beat.core.experiment import Experiment
from beat.core.hash import toPath
from beat.core.hash import hashDataset

from . import prefix, tmp_prefix


def index_experiment_dbs(experiment_name):
    """
    Index all databases for given experiment
    """

    experiment = Experiment(prefix, experiment_name)

    assert experiment.valid, '\n  * %s' % '\n  * '.join(experiment.errors)

    for block_name, infos in experiment.datasets.items():
        view = infos['database'].view(infos['protocol'], infos['set'])
        filename = toPath(hashDataset(infos['database'].name,
                                      infos['protocol'],
                                      infos['set']),
                          suffix='.db')
        view.index(os.path.join(tmp_prefix, filename))


# Based on https://stackoverflow.com/a/20553331/5843716
class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        self.messages = {
            'debug': [], 'info': [],
            'warning': [], 'error': [],
            'critical': [], 'extra': []
        }
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        except Exception:
            self.handleError(record)

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()
