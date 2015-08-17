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

from jira_bot.utils import *


class CreateSubCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'create'
          , help='Create a new issue'
          )

        parser.add_argument(
            '-p'
          , '--project'
          , help='JIRA project to add an issue'
          )
        parser.add_argument(
            '-t'
          , '--issue-type'
          , required=True
          , help='type of issue to create (use `list-issue-types` subcommand to get valid values)'
          )
        parser.add_argument(
            '-s'
          , '--summary'
          , required=True
          , help='summary text for an issue'
          )
        parser.add_argument(
            '-f'
          , '--attachment'
          , nargs='+'
          , type=argparse.FileType('rb')
          , help='attach a given file(s) to a new issue'
          )
        parser.add_argument(
            '-w'
          , '--show-issue-uri'
          , action='store_true'
          , help='on exit print URI of the issue created'
          )
        parser.add_argument(
            'input'
          , nargs='?'
          , type=argparse.FileType('r')
          , default=sys.stdin
          , help='input file with issue description (STDIN if omitted)'
          )
        parser.set_defaults(func=self._create_new_issue)


    def check_options(self, config, target_section, args):
        # Check if `--project` is provided
        if args.project is not None:
            config[target_section]['project'] = args.project

        if 'project' not in config[target_section]:
            raise RuntimeError('Project name is not provided')

        config[target_section]['summary'] = args.summary

        # Check if `--show-issue-url` is provided
        config[target_section]['show-issue-uri'] = (args.show_issue_uri is not None)

        # Check if `--attachment` is provided
        config[target_section]['attachments'] = args.attachment if args.attachment is not None else None
        config[target_section]['issuetype'] = args.issue_type

        # Read description data if anything has specified
        if args.input is not None:
            config[target_section]['description'] = args.input.read().strip()


    def _create_new_issue(self, conn, config):
        # Make sure the project specified is really exists
        prj = conn.project(config['project'])
        if prj is None:
            raise RuntimeError('Specified project "{}" not found'.format(config['project']))

        if config['verbose']:
            print('[DEBUG] Got project id for {}: {}'.format(config['project'], prj.id), file=sys.stderr)

        # Prepare data for a new issue
        issue_dict = {
            'project': {'id': prj.id}
          , 'summary': config['summary']
          , 'description': config['description']
          , 'issuetype': form_value_using_dict(config, 'issuetype', lambda: conn.issue_types())
          }

        if config['verbose']:
            print('[DEBUG] Going to create an issue w/ data: {}'.format(repr(issue_dict)), file=sys.stderr)

        # Create it!
        issue = conn.create_issue(fields=issue_dict)
        if issue is None:
            # TODO More diagnostic!
            raise RuntimeError('Fail to add an issue')

        if config['verbose']:
            print('[DEBUG] Issue {} created'.format(issue.key), file=sys.stderr)

        # Attach files if any
        if config['attachments'] is not None:
            for a in config['attachments']:
                if config['verbose']:
                    print('[DEBUG] Going to attach file "{}" to issue {}'.format(a.name, issue.key), file=sys.stderr)
                conn.add_attachment(issue, attachment=a)

        # Print URL to browse created task if needed
        if config['show-issue-uri']:
            print('{}/browse/{}'.format(config['server'], issue.key))

