'''Unit test package for module "tws._EWrapper".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import logging
from tws import EWrapper, EClientErrors, EClientSocket
from test_tws import mock_wrapper, mock_logger


class test_EWrapper(unittest.TestCase):
    '''Test class "tws.EWrapper"'''

    def setUp(self):
        logging.disable(0)
        self.wrapper = EWrapper(mock_logger())

    def tearDown(self):
        logging.disable(100)

    def test_init(self):
        self.assertTrue(EWrapper())
        self.assertTrue(EWrapper(logging.getLogger("test")))

    def test_client(self):
        self.assertEqual(self.wrapper.client, None)
        test_client = EClientSocket(self.wrapper)
        self.assertEqual(self.wrapper.client, test_client)
        self.assertRaises(ValueError, EClientSocket, self.wrapper)

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

    def test_connectionClosed(self):
        self.wrapper.connectionClosed()
        self.assertEqual(len(self.wrapper.logger.logs), 1)
        self.assertEqual(self.wrapper.logger.logs[0], 
                         (logging.WARNING,"Connection closed.",()))

    def test_error(self):
        self.wrapper.error(Exception("Test1"))
        self.wrapper.error(Warning("Test2"))
        self.wrapper.error(EClientErrors.ALREADY_CONNECTED)
        self.wrapper.error(EClientErrors.TwsError(code=2100, msg="Test4"))

        self.assertEqual(len(self.wrapper.logger.logs), 4)
        self.assertEqual(self.wrapper.logger.logs[0], 
                         (logging.ERROR,"Test1",()))
        self.assertEqual(self.wrapper.logger.logs[1], 
                         (logging.WARNING,"Test2",()))
        self.assertEqual(self.wrapper.logger.logs[2], 
                         (logging.ERROR,"TWS Error 501: Already connected.",()))
        self.assertEqual(self.wrapper.logger.logs[3], 
                         (logging.WARNING,"TWS Error 2100: Test4",()))

    def test_unimplemented(self):
        self.wrapper.bogus(1,2,x=3,y=4)
        self.assertEqual(len(self.wrapper.logger.logs), 2)
        self.assertEqual(self.wrapper.logger.logs[0], 
                         (logging.ERROR,"'EWrapper' object has no attribute 'bogus'",()))
        self.assertEqual(self.wrapper.logger.logs[1], 
                         (logging.WARNING,"Unimplemented method 'EWrapper.bogus' invoked with args: (1, 2) and kwds: {'y': 4, 'x': 3}",()))
