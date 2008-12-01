'''Reader for client socket.

   Defines the EReader class, which defines the interface for a type that
   is responsible for reading data from the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class EReader(object):
    """Type which reads and reacts to EClientSocket data.

       Reads data from client socket and fires events in the application-defined
       EWrapper-derived object provided to EClientSocket.
    """

    def __init__(self, connection, input_stream):
        assert issubclass(type(connection), __import__("tws").EClientSocket)
        assert hasattr(input_stream, "read")

        self._connection = connection
        self._stream = input_stream


    ## Socket stream reader functions ##

    def _readStr(self):
        buffer = self._buffer_factory()
        while True:
            char = self._stream.read(1)
            if char == '\x00': break
            buffer.write(char)
        result = buffer.getvalue()
        return result if result else None


    def _readInt(self, default=0):
        strval = self._readStr()
        return int(strval) if strval else default


    def _readIntMax(self):
        return self._readInt(default=self._INT_MAX_VALUE)


    def _readBoolFromInt(self):
        return bool(self._readInt())


    def _readLong(self):
        strval = self._readStr()
        return long(strval) if strval else long(0)


    def _readDouble(self, default=0.0):
        strval = self._readStr()
        return float(strval) if strval else default


    def _readDoubleMax(self):
        return self._readDouble(default=self._DOUBLE_MAX_VALUE)


    ## Private class imports ##

    from cStringIO import StringIO as _buffer_factory
    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE
