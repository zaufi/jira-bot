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
from .plugin_loader import supported_subcommands

# Standard imports
import abc
import sys


class abstract_command(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check_options(self, config, target_section, args):
        pass


    @abc.abstractmethod
    def run(self, conn, config):
        pass


class abstract_subcommand(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register_subcommands(self, subsubparsers):
        pass


class registrator(abc.ABCMeta):

     def __call__(cls, *args, **kwargs):
        cmd = super().__call__(*args, **kwargs)             # Create a command class

        # Iterate over sub-command implementation classes, defined in the same module
        for subcmd_class in supported_subcommands(sys.modules[cls.__module__], abstract_subcommand):
            subcmd = subcmd_class()                         # Create a sub-command instance
            subcmd.register_subcommands(cmd.subsubparsers)  # Ask it to register its options to the command's parser

        delattr(cmd, 'subsubparsers')                       # Now this attribute no longer needed

        return cmd                                          # Return the command instance


class abstract_complex_command(abstract_command, metaclass=registrator):

    def __init__(self, name, help_string, subparsers):
        parser = subparsers.add_parser(
            name
          , help=help_string
          )
        parser.set_defaults(instance=self)

        self.subsubparsers = parser.add_subparsers(
            title='available sub-commands'
          , metavar='<command>'
          )


    def check_options(self, config, target_section, args):
        # Dispatch parameters checking to corresponding sub-function
        if hasattr(args, 'checker'):
            args.checker(config, target_section, args)

        # Remember the sub-function to execute
        if hasattr(args, 'subcommand'):
            config[target_section]['what'] = args.subcommand
        else:
            raise RuntimeError('No sub-command has given')


    def run(self, conn, config):
        config['what'](conn, config)
