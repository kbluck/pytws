'''Unit test package for module "tws._EClientSocket".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EClientSocket, EReader, EWrapper


# Local classes required to test EClientSocket
class _wrapper(EWrapper):
    pass


class test_EClientSocket(unittest.TestCase):
    '''Test class "tws.EClientSocket"'''
    
    def setUp(self):
        self.wrapper = _wrapper()
        self.client = EClientSocket(self.wrapper)

    def test_api_versions(self):
        # Want to make sure to notice version changes.
        self.assertEqual(EClientSocket.CLIENT_VERSION, 42)
        self.assertEqual(EClientSocket.SERVER_VERSION, 38)

    def test_getters(self):
        self.assertEqual(self.client.wrapper(), self.wrapper)
        self.assertEqual(self.client.reader(), None)
        self.assertEqual(self.client.isConnected(), False)
        self.assertEqual(self.client.serverVersion(), "")
        self.assertEqual(self.client.TwsConnectionTime(), "")

    def test_MsgTypeName(self):
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.GROUPS), "GROUPS")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.PROFILES), "PROFILES")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.ALIASES), "ALIASES")

        if __debug__:
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 0)
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 4)
