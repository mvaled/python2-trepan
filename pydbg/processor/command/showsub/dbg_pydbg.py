from import_relative import *
# Our local modules

# FIXME: Until import_relative is fixed up...
import_relative('processor', '....', 'pydbg')

Mbase_subcmd  = import_relative('base_subcmd', os.path.pardir)

class ShowDbgPydbg(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show debugging the debugger"""
    min_abbrev = 4 # Min 'show pydb"
    pass
