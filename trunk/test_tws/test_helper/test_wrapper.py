'''Unit test package for module "tws.helper._wrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import Queue
from tws import EWrapper
from tws.helper import QueueWrapper, SynchronizedWrapper


class test_QueueWrapper(unittest.TestCase):

    def test_init(self):
        self.assertTrue(isinstance(QueueWrapper(), EWrapper))
        self.assertTrue(isinstance(QueueWrapper(), Queue.Queue))
        self.assertTrue(QueueWrapper().empty())
        self.assertFalse(QueueWrapper().full())
        self.assertRaises(Queue.Empty, QueueWrapper().get_nowait)


class test_SynchronizedWrapper(unittest.TestCase):

    def test_init(self):
        self.assertTrue(isinstance(SynchronizedWrapper(), EWrapper))
