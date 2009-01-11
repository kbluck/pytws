'''Unit test package for module "tws.helper._queuewrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import Queue
from tws import EWrapper
from tws.helper import QueueWrapper


class test_QueueWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = QueueWrapper() 

    def test_init(self):
        self.assertTrue(isinstance(QueueWrapper(), EWrapper))
        self.assertTrue(isinstance(QueueWrapper(), Queue.Queue))
        self.assertTrue(QueueWrapper().empty())
        self.assertFalse(QueueWrapper().full())
        self.assertEqual(QueueWrapper().qsize(), 0)
        self.assertRaises(Queue.Empty, QueueWrapper().get_nowait)

        self.assertRaises(NotImplementedError, QueueWrapper().put)
        self.assertRaises(NotImplementedError, QueueWrapper().put_nowait)

    def test_put_wrapper_call(self):
        self.assertTrue(self.wrapper.empty())
        self.wrapper._put_wrapper_call("test", "A1", 2, B2=3)         
        self.assertFalse(self.wrapper.empty())
        self.assertEqual(self.wrapper.get(), ("test",("A1",2),{"B2":3}))
        self.assertTrue(self.wrapper.empty())
