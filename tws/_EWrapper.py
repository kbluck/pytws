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

    def __init__(self, logger=None):
        if logger is None:
            logger = __import__("logging").getLogger(self.__class__.__name__)
        self.logger = logger


    def logger(self):
        return self._logger
    def set_logger(self, new_logger):
        assert isinstance(new_logger, __import__("logging").Logger)
        self._logger = new_logger
    logger = property(fget=logger, fset=set_logger,
                      doc="logging.Logger object.")
    del set_logger


    def connectionClosed(self):
        self.error(Warning("Connection closed."))


    def error(self, e):
        # TWS Error codes in the 2100 range are 'system warnings'
        if hasattr(e, "code"):
            if ((e.code() >= 2100) and (e.code() <= 2199)):
                self._logger.warning(str(e))
                return
        # Warning exception types are warnings
        if isinstance(e, Warning):
            self._logger.warning(str(e))
            return
        # Everything else is considered an error.
        self._logger.error(str(e))
