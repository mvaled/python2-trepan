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
# 'Helper' function for Processor. Put here so we 
# can use this in a couple of processors.

from import_relative import *
from tracer import EVENT2SHORT
Mbase_proc = import_relative('base_proc', '.', 'pydbg')

def print_event(io, frame, event, arg):
    'A simple event processor that prints out events.'
    lineno = frame.f_lineno
    filename = frame.f_code.co_filename
    io.write("%s - %s:%d" % (event, filename, lineno))
    if arg is not None: 
        io.writeline(', %s ' % repr(arg))
    else:
        io.writeline('')
        pass
    return print_event

class PrintProcessor(Mbase_proc.Processor):
    """ A processor that just prints out events as we see them. This is suitable for example
    for line/call tracing. We assume that the caller is going to filter out which events it
    wants printed or whether it wants any printed at all.
    """
    def __init__(self, debugger, opts=None):
        Mbase_proc.Processor.__init__(self, debugger)
        return

    def event_processor(self, frame, event, arg):
        'A simple event processor that prints out events.'
        return print_event(self.debugger.intf[-1].output, frame, event, arg)
    pass
