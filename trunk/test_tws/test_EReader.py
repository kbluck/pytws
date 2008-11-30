'''Unit test package for module "tws._EReader".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from StringIO import StringIO
from tws import EClientSocket, EReader
from test_tws import mock_wrapper


class test_EReader(unittest.TestCase):
    '''Test class "tws.EReader"'''
    
    def setUp(self):
        self.wrapper = mock_wrapper()
        self.parent = EClientSocket(self.wrapper)
        self.stream = StringIO()
        self.reader = self.parent.createReader(self.parent, self.stream)

    def test_init(self):
        self.assertTrue(EReader(self.parent, StringIO()))

        if __debug__:
            self.assertRaises(AssertionError, EReader, 1, self.stream)
            self.assertRaises(AssertionError, EReader, self.parent, 1)

    def test_readStr(self):
        self.stream.write('test1\x00test2\x00\x00test3\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readStr(), 'test1')
        self.assertEqual(self.reader._readStr(), 'test2')
        self.assertEqual(self.reader._readStr(), None)
        self.assertEqual(self.reader._readStr(), 'test3')
