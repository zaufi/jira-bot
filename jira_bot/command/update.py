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


class UpdateSubCommand:
    def __init__(self, subparsers):
        update_parser = subparsers.add_parser(
            'update'
          , help='Update an issue'
          )

        update_parser.add_argument(
            '-i'
          , '--issue'
          , nargs='?'
          , required=True
          , help='issue ID to update'
          )
        update_parser.add_argument(
            '-s'
          , '--summary'
          , nargs='?'
          , help='set new summary text for an issue'
          )
        update_parser.add_argument(
            '-p'
          , '--priority'
          , nargs='?'
          , help='update priority for an issue'
          )
        update_parser.add_argument(
            '-r'
          , '--resolution'
          , nargs='?'
          , help='update resolution for an issue'
          )
        update_parser.add_argument(
            '-t'
          , '--issue-type'
          , nargs='?'
          , help='change issue type'
          )
        update_parser.add_argument(
            '-u'
          , '--status'
          , nargs='?'
          , help='update status for an issue'
          )
        update_parser.add_argument(
            '-f'
          , '--attachment'
          , nargs='+'
          , type=argparse.FileType('rb')
          , help='attach a given file(s) to an issue'
          )
        update_parser.add_argument(
            'input'
          , nargs='?'
          , type=argparse.FileType('r')
          , default=None
          , help='optional input file with issue description'
          )
        update_parser.set_defaults(func=self._update_issue)


    def check_options(self, config, target_section, args):
        # Copy options from CLI to selected config section
        config[target_section]['issue'] = args.issue
        config[target_section]['summary'] = args.summary
        config[target_section]['priority'] = args.priority
        config[target_section]['resolution'] = args.resolution
        config[target_section]['status'] = args.status
        config[target_section]['attachments'] = args.attachment if args.attachment is not None else None
        config[target_section]['issuetype'] = args.issue_type

        # Read description data if anything has specified
        if args.input is not None:
            config[target_section]['description'] = args.input.read().strip()


    def _update_issue(self, conn, config):
        issue = conn.issue(config['issue'])
        if issue is None:
            # TODO More diagnostic!
            raise RuntimeError('Fail to obtain the requested issue {}'.format(config['issue']))

        # Prepare data to update issue
        issue_dict = {}
        if 'summary' in config and config['summary'] is not None:
            issue_dict['summary'] = config['summary']

        if 'priority' in config and config['priority'] is not None:
            try:
                priority_id = int(config['priority'])
                issue_dict['priority'] = {'id' : config['priority']}
            except:
                # TODO Make sure given name in a list of priorities
                issue_dict['priority'] = {'name' : config['priority']}

        if 'issuetype' in config and config['issuetype'] is not None:
            try:
                type_id = int(config['issuetype'])
                issue_dict['issuetype'] = {'id' : config['issuetype']}
            except:
                # TODO Make sure given name in a list of issue types
                issue_dict['issuetype'] = {'name' : config['issuetype']}

        if len(issue_dict):
            if config['verbose']:
                print('[DEBUG] Going to update issue {} w/ data: {}'.format(issue.key, issue_dict), file=sys.stderr)

            issue.update(fields=issue_dict)

        # Prepare data to make a traksition if needed
        issue_dict = {}
        if 'resolution' in config and config['resolution'] is not None:
            try:
                resolution_id = int(config['resolution'])
                issue_dict['resolution'] = {'id' : config['resolution']}
            except:
                # TODO Make sure given name in a list of resolutions
                issue_dict['resolution'] = {'name' : config['resolution']}

        if 'status' in config and config['status'] is not None:
            try:
                status_id = int(config['status'])
                issue_dict['status'] = {'id' : config['status']}
            except:
                # TODO Make sure given name in a list of statuses
                issue_dict['status'] = {'name' : config['status']}

        if len(issue_dict):
            if config['verbose']:
                print('[DEBUG] Going to do issue {} transition w/ data: {}'.format(issue.key, issue_dict), file=sys.stderr)

            conn.transition_issue(issue, fields=issue_dict)
