#!/usr/bin/env python
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
import jira_bot
import jira_bot.commands
import jira_bot.logger

# Standard imports
import argparse
import configparser
import exitstatus
import jira
import importlib
import os
import sys
import urllib


class Application(object):
    '''
        Application class to to the job.

        Each command implemented as a plug-in.
        Constructor analyze arguments passed via CLI and merge them w/
        parameters came from configuration file(s).

        During execution there is a dict member `self.config` containing
        everything that needed to execute a requested command.

        Config file consists from `[default]` section and possible few
        sections describing connection parameters to server(s), so you don't
        need them to pass via CLI.
    '''

    def __init__(self):
        # Try to parse config file option first
        config_parser = argparse.ArgumentParser(
            description='JIRA Issue Manipulation Bot'
          , add_help=False
          )
        config_parser.add_argument(
            '-c'
          , '--config-file'
          , help='specify config file to use'
          , metavar='FILE'
          )
        args, remaining_argv = config_parser.parse_known_args()

        # Collect configuration data from various places:
        configs = []
        #  - is there any config file provided via CLI?
        if args.config_file:
            # Ok, lets use it
            configs.append(self._parse_config_file(args.config_file))
        else:
            # Heh, then try to get config data from system-wide and per user config files
            config_files = ['/etc/jira-bot/jira-bot.conf', os.path.expanduser('~/.jira-botrc')]
            for config_file in config_files:
                # TODO Make sure that config file is read only by owner!
                if os.path.isfile(config_file):
                    configs.append(self._parse_config_file(config_file))

        # Merge configuration data normalizing URIs in section names
        self.config = {}
        self.config['default'] = {}
        for cfg in configs:
            for section in cfg.sections():
                normalized_section = self._normalize_uri(section)
                if normalized_section not in self.config:
                    self.config[normalized_section] = {}
                self.config[normalized_section].update(dict(cfg[section].items()))

        # Ok, now try to parse rest CLI options
        parser = argparse.ArgumentParser(
            # Inherit options from config_parser
            parents=[config_parser]
            # print script description with -h/--help
          , description='Manage JIRA bugs via CLI'
            # Don't mess with format of description
          , formatter_class=argparse.RawDescriptionHelpFormatter
          )
        parser.add_argument(
            '-v'
          , '--verbose'
          , action='store_true'
          , default=False
          , help='verbose output'
          )
        parser.add_argument(
            '-s'
          , '--server'
          , help='JIRA server URI'
          )
        parser.add_argument(
            '-u'
          , '--username'
          , help='JIRA account name'
          )
        parser.add_argument(
            '-p'
          , '--password'
          , help='JIRA account password'
          )

        subparsers = parser.add_subparsers(
            title='available commands'
          , description='The following command may appear after generic options.\nTo get help use `--help` after command name.'
          , help='Action'
          , metavar='<command>'
          )

        # Loading modules provided by `jira_bot.commands` package
        for command in jira_bot.supported_commands(jira_bot.commands, jira_bot.command.abstract_command):
            command(subparsers)

        try:
            args = parser.parse_args()
        except RuntimeError as ex:
            #parser.error(str(ex))
            assert 0

        # Merge CLI options w/ parsed configuration
        target_section = 'default'

        # Check if `--server` is provided
        if args.server is not None:
            # Override used server section
            target_section = self._normalize_uri(args.server)
            self.config['default']['server'] = target_section
        elif 'server'  in self.config['default']:
            target_section = self._normalize_uri(self.config['default']['server'])
            self.config['default']['server'] = target_section
        else:
            raise RuntimeError('JIRA server URI is not provided')

        if target_section not in self.config:
            self.config[target_section] = {}

        # Checking generic options:
        # Check if `--username` is provided
        if args.username is not None:
            self.config[target_section]['username'] = args.username
            # ATTENTION Reset password
            self.config[target_section]['password'] = None

        # Check if `--password` is provided
        if args.password is not None:
            self.config[target_section]['password'] = args.password

        # Check if `--verbose` is provided
        verbose = args.verbose is not None and args.verbose
        self.config['default']['verbose'] = 'true' if verbose else 'false'
        jira_bot.logger.setup_logger(verbose)

        # Check command specific options
        if not hasattr(args, 'instance') or args.instance is None:
            raise RuntimeError('No command given')

        args.instance.check_options(self.config, target_section, args)

        # Setting `verbose` flag to be a 'shortcut' for corresponding configuration option
        self.config[target_section]['verbose'] = 'verbose' in self.config['default'] and self._try_get_bool(self.config['default']['verbose']) or False

        # Remember selected `server` as a key in the current configuration section
        self.config[target_section]['server'] = target_section

        # TODO Validate option values?

        self.config['default']['cmd'] = args.instance

        # Args seem Ok, ready to run


    def _parse_config_file(self, config_file):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read([config_file])
        return config


    def _normalize_uri(self, uri):
        components = urllib.parse.urlparse(uri)
        if not len(components.path):
            return  urllib.parse.urljoin(components.geturl(), '/')
        return uri


    def _try_get_bool(self, text):
        text = text.strip()
        if text == 'yes' or text == 'true' or text == '1':
            return True
        if text == 'no' or text == 'false' or text == '0':
            return False

        raise RuntimeError('Invalid boolean value: `{}`'.format(text))


    def _make_jira_connection(self, config):
        # Make some SPAM
        if config['verbose']:
            jira_bot.logger.get_logger().debug(
                'Connecting to {} using {} {}'.format(
                    config['server']
                  , 'login `{}`'.format(config['username']) if 'username' in config else 'anonymous login'
                  , 'and password provided' if 'password' in config and config['password'] is not None else 'w/o password'
                  )
              )
        if 'username' in config:
            auth=(config['username'], config['password'])
            return jira.JIRA(
                options={
                    'server': config['server']
                  , 'check_update': False
                  , 'rest_api_version': '2'
                  }
              , basic_auth=auth
              )

        # Else use anonymous login
        return jira.JIRA(options={'server': config['server'], 'check_update': False })


    def run(self):
        server = self.config['default']['server']
        config = self.config[server]

        # Connecting...
        conn = self._make_jira_connection(config)

        # Execute requested command
        self.config['default']['cmd'].run(conn, config)

        # Set exit code to SUCCESS
        return exitstatus.ExitStatus.success


#
# Main entry point
#
def main():
    jira_bot.logger.setup_logger(False)

    try:
        a = Application()
        return a.run()

    except KeyboardInterrupt:
        return exitstatus.ExitStatus.failure

    except jira.JIRAError as ex:
        jira_bot.logger.get_logger().error('{} [{}]'.format(ex.text, ex.status_code))

    except RuntimeError as ex:
        jira_bot.logger.get_logger().error('{}'.format(ex))

    return exitstatus.ExitStatus.failure
