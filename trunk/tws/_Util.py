'''Utility functions.

   Various utility functions implemented by the TWS API. Mostly have to do
   with string and list comparison.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


def StringIsEmpty(strval):
    assert issubclass(type(strval), str) or (strval == None)

    return not strval


def NormalizeString(strval):
    assert issubclass(type(strval), str) or (strval == None)

    return strval if strval else ""


def StringCompare(lhs, rhs):
    assert issubclass(type(lhs), str) or (lhs == None)
    assert issubclass(type(rhs), str) or (rhs == None)

    return (NormalizeString(lhs) == NormalizeString(rhs))


def StringCompareIgnCase(lhs, rhs):
    assert issubclass(type(lhs), str) or (lhs == None)
    assert issubclass(type(rhs), str) or (rhs == None)

    return (NormalizeString(lhs).lower() == NormalizeString(rhs).lower())


def VectorEqualsUnordered(lhs, rhs):
    assert issubclass(type(lhs), list) or (lhs == None)
    assert issubclass(type(rhs), list) or (rhs == None)

    # Convert None values to empty lists
    if lhs is None: lhs = []
    if rhs is None: rhs = []

    # Short-circuit if the lists already match.
    if (lhs == rhs): return True

    # Make sorted copies of lists and return results of compare.
    sorted_lhs = list(lhs)
    sorted_rhs = list(rhs)
    sorted_lhs.sort()
    sorted_rhs.sort()
    return sorted_lhs == sorted_rhs


def IntMaxString(value):
    assert issubclass(type(value), int)

    return str(value) if (value < _INT_MAX_VALUE) else ""


def DoubleMaxString(value):
    assert issubclass(type(value), float)

    return str(value) if (value < _DOUBLE_MAX_VALUE) else ""


# Java definitions of max values for Int and Double types
_INT_MAX_VALUE = int(2**31-1)
_DOUBLE_MAX_VALUE = float((2-2**-52)*2**1023)
