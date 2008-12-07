'''Listener for client socket.

   Defines the EWrapper class, which defines the interface for a listener that
   must be provided to the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class EWrapper(object):
    '''Listener class which reacts to EClientSocket events.
    
       A subclass object of this type must be provided to the constructor of
       EClientSocket.
    '''
    pass