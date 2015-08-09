#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


class FancyGrid(object):
    # TODO: Move this code to some kind of unit test
    # t = [[55555.666, 'aaa', '20', 'aaaaaaaa', 66], [42.5, 'bbbbbbbbbbbbb', '44444', 'bb', 112], [42, 'cc', 3, 'ccc', 555555555555]]
    # print(FancyGrid(t))

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
