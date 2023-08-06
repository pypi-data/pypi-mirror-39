#!/usr/bin/env python

import asyncio
import unittest
import unittest.mock
import weakref
from awebus import EventMixin


class InvokeTestCase( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def testInvokeOneFunctionOnce( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( return_value='Hello, World!', spec=object )
        bus.on( 'fizz', handler )
        results = bus.emit( 'fizz' )
        handler.assert_called_with()
        self.assertEqual( [ 'Hello, World!' ], results )

    def testInvokeOneFunctionOnceWithArguments( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec=object )
        bus.on( 'buzz', handler )
        bus.emit( 'buzz', 'a', 'b', 'c' )
        handler.assert_called_with( 'a', 'b', 'c' )

    def testInvokeOneFunctionTwice( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec=object )
        bus.on( 'bleepo', handler )
        bus.on( 'bleepo', handler )
        bus.emit( 'bleepo' )
        self.assertEqual( 2, handler.call_count )

    def testInvokeOneFunctionTwiceWithArguments( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec=object )
        bus.on( 'slammo', handler )
        bus.on( 'slammo', handler )
        bus.emit( 'slammo', 1, door='shut' )
        self.assertEqual( 2, handler.call_count )
        handler.assert_called_with( 1, door='shut' )

    def testInvokeTwoFunctionsOnceTogether( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value='Harry', spec=object )
        handler2 = unittest.mock.Mock( return_value='Sally', spec=object )
        bus.on( 'shout', handler1 )
        bus.on( 'shout', handler2 )
        results = bus.emit( 'shout' )
        handler1.assert_called_with()
        handler2.assert_called_with()
        self.assertEqual( [ 'Harry', 'Sally' ], results )

    def testInvokeTwoFunctionsOnceIndependently( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( spec=object )
        handler2 = unittest.mock.Mock( spec=object )
        bus.on( 'scream', handler1 )
        bus.on( 'whisper', handler2 )
        bus.emit( 'scream' )
        handler1.assert_called_with()
        self.assertEqual( 0, handler2.call_count )
        # handler2.assert_not_called()
        handler1.reset_mock()
        handler2.reset_mock()
        bus.emit( 'whisper' )
        self.assertEqual( 0, handler1.call_count )
        # handler1.assert_not_called()
        handler2.assert_called_with()

    def testInvokeAfterDeletion( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec=object )
        bus.on( 'snarf', handler )
        del handler
        results = bus.emit( 'snarf' )
        self.assertEqual( [ ], results )

    def testInvokeLambda( self ):
        bus = EventMixin()
        handler_mock = unittest.mock.Mock( return_value='did-the-thing', spec=object )
        handler = lambda: handler_mock()
        bus.on( 'do-the-thing', handler )
        results = bus.emit( 'do-the-thing' )
        handler_mock.assert_called_with()
        self.assertEqual( [ 'did-the-thing' ], results )

    def testInvokeSyncHandlersAsynchronously( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value=7, spec=object )
        handler2 = unittest.mock.Mock( return_value=6, spec=object )
        bus.on( 'all-together-now', handler1, handler2 )
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete( bus.emitAsync( 'all-together-now' ) )
        handler1.assert_called_with()
        handler2.assert_called_with()
        self.assertEqual( [ 7, 6 ], results )

    def testInvokeMixedHandlersAsynchronously( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value=7, spec=object )
        handler2 = unittest.mock.Mock( return_value=6, spec=object )

        @asyncio.coroutine
        def handler2async():
            return handler2()

        bus.on( 'all-together-now', handler1, handler2async )

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete( bus.emitAsync( 'all-together-now' ) )
        handler1.assert_called_with()
        handler2.assert_called_with()
        self.assertEqual( [ 7, 6 ], results )

    def testInvokeAsyncHandlersAsynchronously( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value=7, spec=object )
        handler2 = unittest.mock.Mock( return_value=6, spec=object )

        @asyncio.coroutine
        def handler1async():
            return handler1()

        @asyncio.coroutine
        def handler2async():
            return handler2()

        bus.on( 'all-together-now', handler1async, handler2async )
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete( bus.emitAsync( 'all-together-now' ) )
        handler1.assert_called_with()
        handler2.assert_called_with()
        self.assertEqual( [ 7, 6 ], results )

    def testInvokeMixedHandlersSynchronously( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value=7, spec=object )
        mock2 = unittest.mock.Mock( return_value=6, spec=object )

        @asyncio.coroutine
        def handler2():
            return mock2()

        bus.on( 'all-together-now', handler1, handler2 )
        results = bus.emit( 'all-together-now' )
        handler1.assert_called_with()
        mock2.assert_called_with()
        self.assertEqual( [ 7, 6 ], results )

    def testInvokeAsyncHandlersSynchronously( self ):
        bus = EventMixin()
        handler1 = unittest.mock.Mock( return_value=7, spec=object )
        handler2 = unittest.mock.Mock( return_value=6, spec=object )

        @asyncio.coroutine
        def handler1async():
            return handler1()

        @asyncio.coroutine
        def handler2async():
            return handler2()

        bus.on( 'all-together-now', handler1async, handler2async )
        results = bus.emit( 'all-together-now' )
        handler1.assert_called_once_with()
        handler2.assert_called_once_with()
        self.assertEqual( [ 7, 6 ], results )

    def testClassMethodHandlers( self ):
        class C( object ):
            def __init__( self, mock ):
                self.mock = mock

            def onEvent( self ):
                self.mock()

        mock = unittest.mock.Mock( spec=object )
        bus = EventMixin()
        c = C( mock )
        bus.on( 'evt', c.onEvent )
        bus.emit( 'evt' )
        mock.assert_called_once_with()

    def testRemoveClassMethodHandlers( self ):
        class C( object ):
            def __init__( self, mock ):
                self.mock = mock

            def onEvent( self ):
                self.mock()

        mock = unittest.mock.Mock( spec=object )
        bus = EventMixin()
        c = C( mock )
        bus.on( 'evt', c.onEvent )
        bus.off( 'evt', c.onEvent )
        bus.emit( 'evt' )
        self.assertEqual( 0, mock.call_count )
