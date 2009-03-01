# -*- coding: utf-8 -*-
#   Copyright (C) 2008, 2009 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os, sys
def option_set(options, value, default_options):
    if not options or value not in options:
        return default_options.get(value)
    else:
        return options.get(value)
    return None # Not reached

def bool2YN(b):
    if b: return 'Y'
    else: return 'N'

def wrapped_lines(msg_part1, msg_part2, width):
    if len(msg_part1) + len(msg_part2) + 1 > width:
        return msg_part1 + "\n\t" + msg_part2
    else:
        return msg_part1 + " " + msg_part2
    return # Not reached

# Demo it
if __name__=='__main__':
    TEST_OPTS = {'a': True, 'b': 5, 'c': None}
    get_option = lambda key: option_set(opts, key, TEST_OPTS)
    opts={'d': 6, 'a': False}
    for opt in ['a', 'b', 'c', 'd']:
        print opt, get_option(opt)
        pass
    for b in [True, False]: 
        print bool2YN(b)
    pass

    print wrapped_lines('hi', 'there', 80)
    print wrapped_lines('hi', 'there', 5)
    pass