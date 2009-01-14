'''Unit test package for module "tws._EWrapper".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import logging
from tws import EWrapper


class test_EWrapper(unittest.TestCase):
    '''Test class "tws.EWrapper"'''

    def setUp(self):
        self.wrapper = EWrapper()

    def test_init(self):
        self.assertTrue(EWrapper())
        self.assertTrue(EWrapper(logging.getLogger("test")))

    def test_logger(self):
        default_logger = self.wrapper.logger
        test_logger = logging.getLogger("test")
        self.assertNotEqual(self.wrapper.logger, test_logger)
        self.wrapper.logger = test_logger
        self.assertNotEqual(self.wrapper.logger, default_logger)
        self.assertEqual(self.wrapper.logger, test_logger)

        if __debug__:
            try: logging.logger = 123
            except AssertionError, e: self.assertTrue(e)
