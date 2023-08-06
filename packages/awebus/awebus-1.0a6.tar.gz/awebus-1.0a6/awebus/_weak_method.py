import weakref


class WeakMethod( object ):
    """
    Weak method wrapper to prevent bound methods from disappearing.

    Inspired by: http://code.activestate.com/recipes/81253/
    Changes:
    - Uses Python 3 Syntax
    - Implements __eq__ to allow for equality testing similar to
      the way that you can compare weakref.ref() instances.
    """

    def __init__( self, f ):
        self.f = f.__func__
        self.c = weakref.ref( f.__self__ )

    def __call__( self, *args ):
        c = self.c()
        if c is None:
            return None
        return self.f( c, *args )

    def __eq__( self, other ):
        return other.f == self.f and other.c == self.c

    @property
    def isUnreffed( self ):
        return self.c() is None
