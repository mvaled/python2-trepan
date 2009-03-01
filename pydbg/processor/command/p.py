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

# Our local modules
from import_relative import import_relative
Mbase_cmd  = import_relative('base_cmd', top_name='pydbg')
Mprint     = import_relative('print', '...lib', 'pydbg')

class PrintCommand(Mbase_cmd.DebuggerCommand):

    category     = 'data'
    min_args      = 1
    max_args      = None
    name_aliases = ('p',)
    need_stack    = True
    short_help    = 'Print value of expression EXP'

    def run(self, args):
        """p expression

Print the value of the expression. Variables accessible are those of the
environment of the selected stack frame, plus globals. 

The expression may be preceded with /FMT where FMT is one of the
format letters 'c', 'x', 'o', 'f', or 's' for chr, hex, oct, 
float or str respectively.

If the length output string large, the first part of the value is
shown and ... indicates it has been truncated

See also `pp' and `examine' for commands which do more in the way of
formatting.
"""
        if len(args) > 2 and '/' == args[1][0]:
            fmt = args[1]
            del args[1]
        else:
            fmt = None
            pass
        arg = ' '.join(args[1:])
        try:
            val = self.proc.eval(arg)
            if fmt:
                val = Mprint.printf(val, fmt)
                pass
            self.msg(self.proc._saferepr(val))
        except:
            pass

if __name__ == '__main__':
    import inspect
    cmdproc     = import_relative('cmdproc', '..')
    debugger    = import_relative('debugger', '...')
    d           = debugger.Debugger()
    cp          = d.core.processor
    cp.curframe = inspect.currentframe()
    command = PrintCommand(cp)
    me = 10
    command.run(['print', 'me'])
    command.run(['print', '/x', 'me'])
    command.run(['print', '/o', 'me'])
    pass


