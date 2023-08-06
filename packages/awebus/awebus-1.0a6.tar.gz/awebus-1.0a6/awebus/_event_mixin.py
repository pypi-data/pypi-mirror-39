#!/usr/bin/env python

import asyncio
import sys
import types
import weakref

from awebus._weak_method import WeakMethod

if sys.version_info < (3, 5):
    def _is_future( o ):
        """
        Return True if the given object is a future(-compatible) object
        """
        return isinstance( o, asyncio.Future )
else:
    def _is_future( o ):
        """
        Return True if the given object is a future(-compatible) object
        """
        return (asyncio.isfuture( o ) or isinstance( o, types.CoroutineType ))


def _is_coro( o ):
    """
    Return True if the given object is a coroutine(-compatible) object
    """
    return asyncio.iscoroutine( o ) or asyncio.iscoroutinefunction( o )


def is_bound( m ):
    """
    Determine if the given object is a bound method
    Source: https://stackoverflow.com/a/18955425
    """
    return hasattr( m, '__self__' )


class EventMixin( object ):
    events = { }

    def __init__( self, *args, **kwargs ):
        self.__handlers = { }
        self.__use_weakref = kwargs.get( 'event_use_weakref', True )
        self.__init_handlers()

    def __init_handlers( self ):
        """
        Register any event handlers that are defined in the __handlers dictionary
        """
        for event, handler_name_or_list in self.events.items():
            if isinstance( handler_name_or_list, str ):
                handler_name_or_list = [ handler_name_or_list ]
            for handler_name in handler_name_or_list:
                handler = getattr( self, handler_name )
                self.on( event, handler )

    def _get_weak( self, o ):
        """
        Retrieve a weak reference to the given object.
        If the object is a bound method, a custom `WeakMethod` wrapper is used
        to keep the object (weakly) alive.

        Params:
            o: The object to retrieve a weakref for.

        Returnsz:
            A weak-reference compatible object.
        """
        if is_bound( o ):
            return WeakMethod( o )
        else:
            return weakref.ref( o )

    def on( self, event, *handlers ):
        """
        Register a handler for an event.

        Args:
            event (str): The name of the event to register handlers for
            handlers (Callable[]): The event handler(s) to invoke when the event is raised

        Returns:
            EventMixin: self
        """
        if event not in self.__handlers:
            self.__handlers[ event ] = [ ]
        for handler in handlers:
            if self.__use_weakref:
                handler = self._get_weak( handler )
            self.__handlers[ event ].append( handler )
        return self

    def off( self, event, *handlers ):
        """
        Unregister a handler for an event.

        Args:
            event (str): The name of the event to register handlers for
            handler (Callable[]): The event handler(s) to invoke when the event is raised

        Returns:
            EventMixin: self
        """
        if event not in self.__handlers:
            return
        for handler in handlers:
            if self.__use_weakref:
                handler = self._get_weak( handler )
            self.__handlers[ event ].remove( handler )
        if len( self.__handlers[ event ] ) == 0:
            del self.__handlers[ event ]
        return self

    def _remove_event_if_empty( self, event ):
        """
        Check the given event and if it has no handlers then remove it from
        the handlers dictionary.

        Args:
            event (str): The name of the event to check

        Returns:
            EventMixin: self
        """
        if event in self.__handlers and len( self.__handlers[ event ] ) == 0:
            del self.__handlers[ event ]
        return self

    def _get_and_clean_event_handlers( self, event ):
        """
        Retrieve concrete implementations of all event handlers, cleaning
        up any unreffed handlers in the process.

        Args:
            event (str): The name of the event to retrieve handlers for.

        Returns:
            Callable[]: A list of concrete event handlers
        """
        if self.__use_weakref:
            handlers = [ ]
            unreffed = [ ]

            # Get handlers from weak references or weak methods
            for weakHandler in self.__handlers.get( event, [ ] ):
                if isinstance( weakHandler, weakref.ref ):
                    handler = weakHandler()
                    if not handler:
                        unreffed.append( weakHandler )
                    else:
                        handlers.append( handler )
                elif isinstance( weakHandler, WeakMethod ):
                    if weakHandler.isUnreffed:
                        unreffed.append( weakHandler )
                    else:
                        handlers.append( weakHandler )

            # Remove any unreffed handlers from the event chain
            if unreffed:
                for handler in unreffed:
                    self.__handlers[ event ].remove( handler )
                self._remove_event_if_empty( event )

            return handlers

        else:
            return self.__handlers.get( event, [ ] )

    def _handler_as_coro( self, o ):
        """
        Coerce any synchronous handlers into an asynchronous coroutine.

        Args:
            o (object): The object to coerce

        Returns:
            object: the original object, or an asynchronous handler if the
            object was not a coroutine.
        """
        if _is_coro( o ):
            return o
        else:
            return asyncio.coroutine( o )

    def emit( self, event, *args, **kwargs ):
        """
        Emit a synchronous event.

        Args:
            event (str): The name of the event to invoke
            args (tuple): Arguments to pass to the event handler(s)
            kwargs (dict): Keyword arguments to pass to the event handler(s)

        Returns:
            list: A list containing the return values of each of the
            executed event handlers.
        """
        results = [ ]
        handlers = self._get_and_clean_event_handlers( event )
        for handler in handlers:
            if _is_coro( handler ):
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete( handler( *args, **kwargs ) )
                results.append( result )
            else:
                result = handler( *args, **kwargs )
                results.append( result )
        return results

    @asyncio.coroutine
    def emitAsync( self, event, *args, **kwargs ):
        """
        Emit an asynchronous event.

        Args:
            event (str): The name of the event to invoke
            args (tuple): Arguments to pass to the event handler(s)
            kwargs (dict): Keyword arguments to pass to the event handler(s)

        Returns:
            awaitable: An awaitable which will resolve to a list containing
            the return values of each of the executed event handlers.
        """
        awaitables = [ ]
        handlers = self._get_and_clean_event_handlers( event )
        for handler in handlers:
            if _is_coro( handler ):
                awaitables.append( handler( *args, **kwargs ) )
            else:
                asyncHandler = asyncio.coroutine( handler )
                awaitables.append( asyncHandler( *args, **kwargs ) )
        result = yield from asyncio.gather( *awaitables )
        return result
