'''Unit test package for module "tws.helper._wrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EWrapper
from tws.helper import QueueWrapper, SynchronizedWrapper


class test_QueueWrapper(unittest.TestCase):

    def test_init(self):
        self.assertTrue(isinstance(QueueWrapper(), EWrapper))


class test_SynchronizedWrapper(unittest.TestCase):

    def test_init(self):
        self.assertTrue(isinstance(SynchronizedWrapper(), EWrapper))
