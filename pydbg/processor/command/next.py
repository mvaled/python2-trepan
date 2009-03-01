# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.
from import_relative import import_relative

# Our local modules
base_cmd   = import_relative('base_cmd')
cmdfns     = import_relative('cmdfns')
Mstack     = import_relative('stack', '...lib')

class NextCommand(base_cmd.DebuggerCommand):

    category      = 'running'
    execution_set = ['Running']
    min_args      = 0
    max_args      = 1
    name_aliases  = ('next', 'next+', 'next-', 'n', 'n-', 'n+')
    need_stack    = True
    short_help    = 'Step program without entering called functions'

    def run(self, args):
        """next[+|-] [count]

Step one statement ignoring steps into function calls at this level.

With an integer argument, perform 'next' that many times. However if
an exception occurs at this level, or we 'return' or 'yield' or the
thread changes, we stop regardless of count.

A suffix of '+' on the command or an alias to the command forces to
move to another line, while a suffix of '-' does the opposite and
disables the requiring a move to a new line. If no suffix is given,
the debugger setting 'different-line' determines this behavior.
"""

        if len(args) <= 1:
            self.core.step_ignore = 0
        else:
            try:
                # 0 means stop now or step 1, so we subtract 1.
                self.core.step_ignore = \
                    cmdfns.get_pos_int(self.errmsg, args[1], default=1,
                                       cmdname='step') - 1
            except ValueError:
                return False
            pass
        self.core.different_line   = \
            cmdfns.want_different_line(args[0], 
                                       self.debugger.settings['different'])
        self.core.step_events      = None # Consider all events
        self.core.stop_level       = Mstack.count_frames(self.proc.frame)
        self.core.last_frame       = self.proc.frame
        self.core.stop_on_finish   = False
        self.proc.continue_running = True # Break out of command read loop
        return True
    pass

if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = NextCommand(d.core.processor)
    for c in (['n', '5'],
              ['next', '1+2'],
              ['n', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print 'Run result: %s' % result
        print 'step_ignore %d, continue_running: %s' % (d.core.step_ignore,
                                                        cmd.continue_running,)
        pass
    for c in (['n'], ['next+'], ['n-']): 
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print cmd.core.different_line
        pass
    pass
