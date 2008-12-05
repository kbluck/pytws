'''Main script to run Nose unit tests.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

if __name__ == '__main__':

    import logging
    import os.path
    import sys
    import nose

    # Suppress logging during unit tests.
    logging.disable(100)

    # Ensure project source packages are on the path.
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    nose.run(argv=['-d','--where=.'])
