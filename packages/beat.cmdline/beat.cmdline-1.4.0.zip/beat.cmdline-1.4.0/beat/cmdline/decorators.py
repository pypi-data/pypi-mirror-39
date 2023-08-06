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

from functools import wraps
from .log import set_verbosity_level

# This needs to be beat so that logger is configured for all beat packages.
logger = logging.getLogger('beat')


def verbosity_option(**kwargs):
    """Adds a -v/--verbose option to a click command.

    Parameters
    ----------
    **kwargs
        All kwargs are passed to click.option.

    Returns
    -------
    callable
        A decorator to be used for adding this option.
    """
    def custom_verbosity_option(f):
        def callback(ctx, param, value):
            ctx.meta['verbosity'] = value
            set_verbosity_level(logger, value)
            logger.debug("Logging of the `beat' logger was set to %d", value)
            return value
        return click.option(
            '-v', '--verbose', count=True,
            expose_value=False, default=2,
            help="Increase the verbosity level from 0 (only error messages) "
            "to 1 (warnings), 2 (log messages), 3 (debug information) by "
            "adding the --verbose option as often as desired "
            "(e.g. '-vvv' for debug).",
            callback=callback, **kwargs)(f)
    return custom_verbosity_option


def raise_on_error(view_func):
    """Raise a click exception if returned value is not zero.

    Click exits successfully if anything is returned, in order to exit properly
    when something went wrong an exception must be raised.
    """

    def _decorator(*args, **kwargs):
        value = view_func(*args, **kwargs)
        if value not in [None, 0]:
            exception = click.ClickException("Error occured")
            exception.exit_code = value
            raise exception
        return value
    return wraps(view_func)(_decorator)
