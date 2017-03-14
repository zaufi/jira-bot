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
from ..grid import fancy_grid

# Standard imports
import argparse


class ls(abstract_command):

    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'list'
          , help='Display various lists'
          , aliases=['ls', 'li']
          )
        parser.set_defaults(instance=self)

        issue_parser = argparse.ArgumentParser(add_help=False)
        issue_parser.add_argument(
            'issue'
          , metavar='ISSUE-ID'
          , help='issue dentifier'
          )

        subsubparsers = parser.add_subparsers(
            title='available lists'
          , dest='what'
          , metavar='<what>'
          )

        filters_parser = subsubparsers.add_parser(
            'filters'
          , help='list of favourite filters'
          , aliases=['flt']
          )
        filters_parser.set_defaults(subcommand=self._filters)

        groups_parser = subsubparsers.add_parser(
            'groups'
          , help='list of user groups'
          , aliases=['gr', 'grp']
          )
        groups_parser.set_defaults(subcommand=self._groups)

        issue_types_parser = subsubparsers.add_parser(
            'issue-types'
          , help='list of configured issue types'
          , aliases=['it']
          )
        issue_types_parser.set_defaults(subcommand=self._issue_types)

        priorities_parser = subsubparsers.add_parser(
            'priorities'
          , help='list of configured projects'
          , aliases=['priority', 'prio']
          )
        priorities_parser.set_defaults(subcommand=self._priorities)

        projects_parser = subsubparsers.add_parser(
            'projects'
          , help='list of configured projects'
          , aliases=['proj']
          )
        projects_parser.set_defaults(subcommand=self._projects)

        resolutions_parser = subsubparsers.add_parser(
            'resolutions'
          , help='list of configured resolutions'
          , aliases=['rs']
          )
        resolutions_parser.set_defaults(subcommand=self._resolutions)

        statuses_parser = subsubparsers.add_parser(
            'statuses'
          , help='list of configured statuses'
          , aliases=['st']
          )
        statuses_parser.set_defaults(subcommand=self._statuses)

        transitions_parser = subsubparsers.add_parser(
            'transitions'
          , help='list of issue transition types'
          , parents=[issue_parser]
          , aliases=['tr']
          )
        transitions_parser.set_defaults(
            checker=self._transitions_check_options
          , subcommand=self._transitions
          )


    def check_options(self, config, target_section, args):
        # Dispatch parameters checking to corresponding subfunction
        if hasattr(args, 'checker'):
            args.checker(config, target_section, args)

        # Remember the sub-function to execute
        if hasattr(args, 'subcommand'):
            config[target_section]['what'] = args.subcommand
        else:
            raise RuntimeError('No sub-command has given')


    def run(self, conn, config):
        config['what'](conn, config)


    def _filters(self, conn, config):
        filters = [(i.id, i.name) for i in conn.favourite_filters()]
        print(fancy_grid(filters))


    def _groups(self, conn, config):
        for i in conn.groups():
            print(i)


    def _issue_types(self, conn, config):
        types = [(i.id, i.name) for i in conn.issue_types()]
        print(fancy_grid(types))


    def _priorities(self, conn, config):
        priorities = [(p.id, p.name) for p in conn.priorities()]
        print(fancy_grid(priorities))


    def _projects(self, conn, config):
        projects = [(p.id, p.key, p.name) for p in conn.projects()]
        print(fancy_grid(projects))


    def _resolutions(self, conn, config):
        resolutions = [(r.id, r.name) for r in conn.resolutions()]
        print(fancy_grid(resolutions))


    def _statuses(self, conn, config):
        statuses = [(r.id, r.name) for r in conn.statuses()]
        print(fancy_grid(statuses))


    def _transitions_check_options(self, config, target_section, args):
        # Copy options from CLI to selected config section
        config[target_section]['issue'] = args.issue


    def _transitions(self, conn, config):
        transitions = [(t['id'], t['name']) for t in conn.transitions(config['issue'])]
        print(fancy_grid(transitions))
