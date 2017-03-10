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
from ..command import abstract_command

# Standard imports
import inspect
import pkgutil


def list_modules():
    '''
        Helper function to gather a list of existed modules of this package

        TODO Check if this code could help:

            for sc in PluginBase.__subclasses__():
                print(sc.__name__)
    '''
    return [name for importer, name, ispkg in pkgutil.iter_modules(__path__) if ispkg == False]


def get_commands_implemented_by_module(module):
    return [
        obj for name, obj in inspect.getmembers(module) \
        if inspect.isclass(obj) and issubclass(obj, abstract_command) and obj.__module__.startswith('jira_bot.commands.') \
      ]
