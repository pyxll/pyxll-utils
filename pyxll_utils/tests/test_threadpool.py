import os
import unittest

from pyxll_utils.threadpool import get_executor


class ThreadPoolTestCase(unittest.TestCase):

    def test_get_executor(self):

        executor = get_executor()

        self.assertEqual(executor._max_workers, 2)

        def _dummy_fun():
            return 'executed'

        f = executor.submit(_dummy_fun)

        while f.running():
            pass

        self.assertEqual(f.result(), 'executed')

        # we share a global executor
        executor2 = get_executor()
        self.assertIs(executor, executor2)

        executor.shutdown()

        with self.assertRaises(RuntimeError):
            executor2.submit(_dummy_fun)

