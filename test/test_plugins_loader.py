# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
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

''' Unit tests for plugins loader '''

# Project specific imports
import jira_bot.commands
from jira_bot.command import abstract_command
from jira_bot.plugin_loader import list_modules, supported_commands

# Standard imports
import importlib
import pathlib
import pytest


class loader_tester:

    def list_modules_test(self):
        modules = list_modules(jira_bot.commands)
        assert modules is not None
        assert 0 < len(modules)
        assert 'issue' in modules
        assert 'list' in modules


    def supported_commands_test(self):
        commands = [cmd.__name__ for cmd in supported_commands()]
        assert commands is not None
        assert len(commands) > 0
        assert 'issue' in commands
        assert 'ls' in commands
