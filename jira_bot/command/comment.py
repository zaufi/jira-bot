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
import datetime
import sys

from jira_bot.utils import *
from jira_bot.fancy_grid import FancyGrid


class CommentSubCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'comment'
          , help='Manage issue comments'
          )
        parser.add_argument(
            '-i'
          , '--issue'
          , nargs='?'
          , required=True
          , help='issue ID to update'
          )
        # TODO Make this default behaviour?
        parser.add_argument(
            '-l'
          , '--local-time'
          , action='store_true'
          , help='transform date/time to local time zone, otherwise leave as is'
          )
        parser.set_defaults(func=self._manage_comments)

        comment_sub_command_parser = parser.add_subparsers(
            title='sub-commands'
          , description=''
          , dest='subcmd'
          , help='Action'
          )

        # - ADD
        add_parser = comment_sub_command_parser.add_parser(
            'add'
          , help='Add a new comment'
          )
        add_parser.add_argument(
            'comment-file'
          , nargs='?'
          , type=argparse.FileType('r')
          , default=None
          , help='input file with comment text'
          )
        add_parser.set_defaults(subcommand=self._add_comment)

        # - LS
        ls_parser = comment_sub_command_parser.add_parser(
            'ls'
          , help='list (short) comments'
          )
        ls_parser.add_argument(
            '-d'
          , '--details'
          , action='store_true'
          , help='show more details'
          )
        ls_parser.set_defaults(subcommand=self._list_comments)

        # - RM
        rm_parser = comment_sub_command_parser.add_parser(
            'rm'
          , help='remove comment'
          )

        rm_parser.add_argument(
            'ID'
          , nargs='+'
          , help='comment ID to remove'
          )
        rm_parser.set_defaults(subcommand=self._remove_comments)


    def check_options(self, config, target_section, args):
        # Copy options from CLI to selected config section
        config[target_section]['issue'] = args.issue
        config[target_section]['local'] = args.local_time
        config[target_section]['subcmd'] = args.subcommand

        if args.subcmd == 'ls':
            config[target_section]['details'] = args.details


    def _manage_comments(self, conn, config):
        issue = conn.issue(config['issue'])
        if issue is None:
            # TODO More diagnostic!
            raise RuntimeError('Fail to obtain the requested issue {}'.format(config['issue']))

        # Handle sub-sub-command
        config['subcmd'](issue, conn, config)


    def _add_comment(self, issue, conn, config):
        if config['verbose']:
            print('[DEBUG] Sorry, not implemented...', file=sys.stderr)


    def _list_comments(self, issue, conn, config):
        '''
            TODO Output in some regular format?
        '''
        comments = conn.comments(issue)

        if config['details']:
            for c in comments:
                date = self._transform_time(c.updated, config).strftime('%c')
                print('{}, {}\n{}\n{}\n\n'.format(date, c.author.displayName, '-' * (len(date) + len(c.author.displayName) + 2), c.body))
        else:
            table = [(
                c.id
              , self._transform_time(c.updated, config).strftime('%c')
              , c.author.displayName
              , self._make_headline(c.body, 60)
              ) for c in comments]
            print(FancyGrid(table))


    def _remove_comments(self, issue, conn, config):
        if config['verbose']:
            print('[DEBUG] Sorry, not implemented...', file=sys.stderr)


    def _make_headline(self, text, max_len):
        if len(text) < max_len:
            return text

        return text[:max_len].replace('\n', ' ').replace('\r', '').strip() + '…'


    def _transform_time(self, date_string, config):
        date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
        return date if not config['local'] else date.replace(tzinfo=date.tzinfo).astimezone(tz=None)
