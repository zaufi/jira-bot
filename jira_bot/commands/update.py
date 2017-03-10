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

from jira_bot.utils import *


class UpdateSubCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'update'
          , help='Update an issue'
          )

        parser.add_argument(
            '-i'
          , '--issue'
          , required=True
          , help='issue ID to update'
          )
        parser.add_argument(
            '-s'
          , '--summary'
          , metavar='text'
          , help='set new summary text for an issue'
          )
        parser.add_argument(
            '-p'
          , '--priority'
          , metavar='Name/#ID'
          , help='update priority for an issue (use `list-priorities` subcommand to get valid values)'
          )
        parser.add_argument(
            '-t'
          , '--issue-type'
          , metavar='Type/#ID'
          , help='symbolic name/type or numeric ID of issue to update (use `list-issue-types` ' \
                'subcommand to get valid values)'
          )
        parser.add_argument(
            '-z'
          , '--transition'
          , metavar='Name/#ID'
          , help='change issue state to given transition (use `list-transitions` subcommand to get valid values)'
          )
        parser.add_argument(
            '-r'
          , '--resolution'
          , metavar='Name/#ID'
          , help='update resolution for an issue (use `list-resolutions` subcommand to get valid values)'
          )
        parser.add_argument(
            '-u'
          , '--status'
          , metavar='Name/#ID'
          , help='update status for an issue (use `list-statuses` subcommand to get valid values)'
          )
        parser.add_argument(
            '-f'
          , '--attachment'
          , metavar='file'
          , nargs='+'
          , type=argparse.FileType('rb')
          , help='attach a given file(s) to an issue'
          )
        parser.add_argument(
            'input'
          , nargs='?'
          , type=argparse.FileType('r')
          , default=None
          , help='optional input file with issue description'
          )
        parser.set_defaults(func=self._update_issue)


    def check_options(self, config, target_section, args):
        # Copy options from CLI to selected config section
        config[target_section]['issue'] = args.issue
        config[target_section]['attachments'] = args.attachment if args.attachment is not None else None

        # Check optional options ;-)
        if args.summary is not None:
            config[target_section]['summary'] = args.summary
        if args.priority is not None:
            config[target_section]['priority'] = args.priority
        if args.resolution is not None:
            config[target_section]['resolution'] = args.resolution
        if args.status is not None:
            config[target_section]['status'] = args.status
        if args.transition is not None:
            config[target_section]['transition'] = args.transition
        if args.issue_type is not None:
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
        if 'summary' in config:
            issue_dict['summary'] = config['summary']

        if 'priority' in config:
            issue_dict['priority'] = form_value_using_dict(config, 'priority', lambda: conn.priorities())

        if 'issuetype' in config:
            issue_dict['issuetype'] = form_value_using_dict(config, 'issuetype', lambda: conn.issue_types())

        if len(issue_dict):
            if config['verbose']:
                print('[DEBUG] Going to update issue {} w/ data: {}'.format(issue.key, issue_dict), file=sys.stderr)

            issue.update(fields=issue_dict)

        # Attach files if any
        if config['attachments'] is not None:
            for a in config['attachments']:
                if config['verbose']:
                    print('[DEBUG] Going to attach file "{}" to issue {}'.format(a.name, issue.key), file=sys.stderr)
                conn.add_attachment(issue, attachment=a)

        # Prepare data to make a traksition if needed
        if 'transition' in config and config['transition'] is not None:
            issue_dict = {}

            if 'resolution' in config and config['resolution'] is not None:
                issue_dict['resolution'] = form_value_using_dict(config, 'resolution', lambda: conn.resolutions())

            if 'status' in config and config['status'] is not None:
                issue_dict['status'] = form_value_using_dict(config, 'status', lambda: conn.statuses())

            # Get list of allowed transitions
            transition_ids = []
            transition_names = []
            for t in conn.transitions(issue):
                transition_ids.append(t['id'])
                transition_names.append(t['name'])

            if not (config['transition'].isdigit() and config['transition'] in transition_ids or config['transition'] in transition_names):
                raise RuntimeError('Given transition not in a list of allowed values: {}'.format(', '.join(transition_names)))

            if config['verbose']:
                print('[DEBUG] Going to do issue {} transition w/ data: {}'.format(issue.key, issue_dict), file=sys.stderr)

            if len(issue_dict):
                conn.transition_issue(issue, config['transition'], fields=issue_dict)
            else:
                conn.transition_issue(issue, config['transition'])
