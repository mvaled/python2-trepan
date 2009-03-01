#!/usr/bin/env python
import os, sys, unittest
import tracer
from fn_helper import *

class TestStep(unittest.TestCase):
    def test_step_same_level(self):

        # See that we can step with parameter which is the same as 'step 1'
        cmds = ['step', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        y = 6
        ##############################
        d.core.stop()
        out = ['-- x = 5',
               '-- y = 6']
        compare_output(self, out, d, cmds)

        # See that we can step with a computed count value
        cmds = ['step 5-3', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        y = 6
        z = 7
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-- z = 7']
        compare_output(self, out, d, cmds)

        # Test step>
        cmds = ['step>', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        def foo():
            return
        y = 6
        foo()
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-> def foo():']
        compare_output(self, out, d, cmds)

        # Test step!
        cmds = ['step!', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        try:
            y = 2
            z = 1/0
        except:
            pass
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '!! z = 1/0']
        compare_output(self, out, d, cmds)

        # Test "step" will sets of events. Part 1
        cmds = ['step call exception',
                'step call exception', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        try:
            def foo():
                y = 2
                raise Exception
                return
            foo()
        except:
            pass
        z = 1
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-> def foo():',
               '!! raise Exception']
        compare_output(self, out, d, cmds)

        # Test "step" will sets of events. Part 2
        cmds = ['step call exception 1+0',
                'step call exception 1', 'continue']
        d = strarray_setup(cmds)
        d.core.start()
        ##############################
        x = 5
        try:
            def foo():
                y = 2
                raise Exception
                return
            foo()
        except:
            pass
        z = 1
        ##############################
        d.core.stop(options={'remove': True})
        out = ['-- x = 5',
               '-> def foo():',
               '!! raise Exception']
        compare_output(self, out, d, cmds)

        return

    def test_step_between_fn(self):

        # Step into and out of a function
        def sqr(x):
            return x * x
        for cmds, out, eventset in (
            (['step', 'step', 'continue'],
             ['-- x = sqr(4)',
              '-- return x * x',
              '-- y = 5'],
             frozenset(('line',))),
            (['step', 'step', 'step', 'step', 'continue'],
             ['-- x = sqr(4)',
               '-> def sqr(x):',
               '-- return x * x',
               '<- return x * x',
               '-- y = 5'],
             tracer.ALL_EVENTS),
            ):
            d = strarray_setup(cmds)
            d.settings['traceset'] = eventset
            d.core.start()
            ##############################
            x = sqr(4)
            y = 5
            ##############################
            d.core.stop(options={'remove': True})
            compare_output(self, out, d, cmds)
            pass
        return

    def test_step_in_exception(self):
        def boom(x):
            y = 0/x
            return
        def bad(x):
            boom(x)
            return x * x
        cmds = ['step', 'step', 'step', 'step', 'step', 'step',
                'step', 'step', 'step', 'step', 'continue']
        d = strarray_setup(cmds)
        try: 
            d.core.start()
            x = bad(0)
            self.assertTrue(False, 'should have raised an exception')
        except ZeroDivisionError:
            self.assertTrue(True, 'Got the exception')
        finally:
            d.core.stop(options={'remove': True})
            pass

        out = ['-- x = bad(0)',  # line event
               '-> def bad(x):', # call event
               '-- boom(x)',     # line event
               '-> def boom(x):',# call event
               '-- y = 0/x',     # line event
               '!! y = 0/x',     # exception event
               '<- y = 0/x',     # return event
               '!! boom(x)',     # exception event
               '<- boom(x)',     # return event
               '!! x = bad(0)',  # return event
               '-- except ZeroDivisionError:']
        compare_output(self, out, d, cmds)
        return

    pass

if __name__ == '__main__':
    unittest.main()





