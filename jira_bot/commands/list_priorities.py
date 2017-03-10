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
from ..fancy_grid import FancyGrid

# Standard imports


class list_priorities(abstract_command):

    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'list-priorities'
          , help='Show list of configured priorities'
          )

        parser.set_defaults(instance=self)


    def check_options(self, config, target_section, args):
        pass


    def run(self, conn, config):
        priorities = [(p.id, p.name) for p in conn.priorities()]
        print(FancyGrid(priorities))
