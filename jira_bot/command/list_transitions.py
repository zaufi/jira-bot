#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Alex Turbov <i.zaufi@gmail.com>
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

import argparse
import sys

from jira_bot.fancy_grid import FancyGrid

class ListTransitionsSubCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'list-transitions'
          , help='Show list of possible issue transitions according configured workflow'
          )

        parser.add_argument(
            '-i'
          , '--issue'
          , nargs='?'
          , required=True
          , help='issue ID to get transitions for'
          )

        parser.set_defaults(func=self._list_transitions)


    def check_options(self, config, target_section, args):
        # Copy options from CLI to selected config section
        config[target_section]['issue'] = args.issue


    def _list_transitions(self, conn, config):
        transitions = [(t['id'], t['name']) for t in conn.transitions(config['issue'])]
        print(FancyGrid(transitions))
