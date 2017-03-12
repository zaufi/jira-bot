#!/usr/bin/env python
#
# Install script for JIRA bot
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

# Standard imports
import pathlib
from setuptools import setup, find_packages


def sources_dir():
    return pathlib.Path(__file__).parent


def readfile(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.read()


def get_requirements_from(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.readlines()


setup(
    name             = 'jira-bot'
  , version          = jira_bot.__version__
  , description      = 'JIRA Bot'
  , long_description = readfile('README.md')
  , author           = 'Alex Turbov'
  , author_email     = 'I.zaufi@gmail.com'
  , url              = 'http://zaufi.github.io/jira-bot.html'
  , download_url     = 'https://github.com/zaufi/jira-bot/archive/version-{}.tar.gz'.format(jira_bot.__version__)
  , entry_points       = {
        'console_scripts': [
            'jira-bot = jira_bot.cli:main'
          ]
      }
  , packages         = find_packages(exclude=('test'))
  , data_files       = [
        ('/etc/jira-bot', ['config/jira-bot.conf.sample'])
      ]
  , license          = 'GNU General Public License v3 or later (GPLv3+)'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      , 'Natural Language :: English'
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Utilities'
      ]
  , keywords = 'jira CLI scripting'
  , install_requires   = get_requirements_from('requirements.txt')
  , test_suite         = 'test'
  , tests_require      = get_requirements_from('test-requirements.txt')
  , zip_safe           = True
  )
