# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ilya Kolesnikovich <ravishankar at mail.ru>
# Copyright (c) 2013-2017 Alex Turbov <i.zaufi@gmail.com>
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


class fancy_grid(object):
    # TODO: Move this code to some kind of unit test (doctest?)
    # t = [[55555.666, 'aaa', '20', 'aaaaaaaa', 66], [42.5, 'bbbbbbbbbbbbb', '44444', 'bb', 112], [42, 'cc', 3, 'ccc', 555555555555]]
    # print(fancy_grid(t))

    # TODO [Parameterized formats](https://pyformat.info/#param_align) may help here!

    def __init__(self, table):
        ''' Pass any sequence of sequences here '''
        # TODO: Support generators (iterable objects of any type)
        assert hasattr(table, '__iter__') and hasattr(table[0], '__iter__')
        # TODO: assert all raws contains same number of fields

        #rows = len(table)
        cols = len(table[0])

        ## 1) get max size for columns from 1st till last - 1
        lens = [0 for x in range(cols - 1)]
        for i in table:
            for n in range(cols - 1):
                lens[n] = max(len(str(i[n])), lens[n])
        frmt = ('{{:<{}}}  ' * (cols - 1) + ' {{:<}}\n').format(*lens)

        self.__s = ''
        for i in table:
            self.__s += frmt.format(*i)

    def __str__(self):
        return self.__s
