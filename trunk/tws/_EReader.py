'''Reader for client socket.

   Defines the EReader class, which defines the interface for a type that
   is responsible for reading data from the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from cStringIO import StringIO as _buffer_factory


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

    def _readStr(self):
        buffer = _buffer_factory()
        while True:
            char = self._stream.read(1)
            if char == '\x00': break
            buffer.write(char)
        result = buffer.getvalue()
        return result if result else None

    def _readInt(self):
        strval = self._readStr()
        return int(strval) if strval else 0

    def _readLong(self):
        strval = self._readStr()
        return long(strval) if strval else long(0)

    def _readDouble(self):
        strval = self._readStr()
        return float(strval) if strval else 0.0
