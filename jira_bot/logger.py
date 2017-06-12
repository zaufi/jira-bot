# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2017 Alex Turbov <i.zaufi@gmail.com>
#
# JIRA Bot is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# JIRA Bot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# Project specific imports

# Standard imports
import logging


_logger = None
_handler = None

def setup_logger(verbose):
    global _logger
    global _handler

    if _logger is None:
        assert _handler is None

        # Create logger
        _logger = logging.getLogger('jira-bot')

    _logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Reset handler
    if _handler is not None:
        _logger.removeHandler(_handler)

    # Create console handler and set level to debug
    _handler = logging.StreamHandler()                            # NOTE Write everything to `stderr`!
    _handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(name)s[%(levelname)s]: %(message)s')
    _handler.setFormatter(formatter)

    # Add handler to logger
    _logger.addHandler(_handler)


def get_logger():
    global _logger
    assert _logger is not None, '`get_logger()` before `setup_logger()`! Code review required!'
    return _logger
