'''Reader for client socket.

   Defines the EReader class, which defines the interface for a type that
   is responsible for reading data from the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class EReader(object):
    """Type which reads EClientSocket data.
    
       A subclass object of this type must be provided for the use of
       EClientSocket.
    """
    pass
