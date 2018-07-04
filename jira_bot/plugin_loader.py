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
import importlib
import inspect
import pkgutil


def list_modules(package):
    '''
        Helper function to gather a list of existed modules of given package.
        Return list of strings, where every item is a module name.
    '''
    return [name for importer, name, ispkg in pkgutil.iter_modules(package.__path__) if ispkg == False]


def get_commands_implemented_by_module(module, cls):
    '''
        Return all subclasses of `cls` declared in a given module
    '''
    return [
        obj for name, obj in inspect.getmembers(module) \
        if inspect.isclass(obj) and issubclass(obj, cls) and obj.__module__.startswith(module.__package__) \
      ]


def supported_commands(package, base):
    # Loading modules provided by `jira_bot.commands` package
    for name in list_modules(package):
        module = importlib.import_module('.' + name, package.__name__)

        # Getting all commands in the current module
        for command in get_commands_implemented_by_module(module, base):
            yield command


def supported_subcommands(module, base):
    # Getting all sub-commands in the current module
    for command in get_commands_implemented_by_module(module, base):
        yield command
