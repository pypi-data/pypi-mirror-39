#!/usr/bin/env python

import asyncio
import unittest
import unittest.mock
import weakref
from awebus import EventMixin


class NoWeakrefsTestCase( unittest.TestCase ):
    """
    Perform tests on the EventMixin class where weakrefs are disabled.
    """

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def testInvokeOneFunctionOnce( self ):
        bus = EventMixin( event_use_weakref=False )
        handler = unittest.mock.Mock( return_value='Hello, World!', spec=object )
        bus.on( 'fizz', handler )
        results = bus.emit( 'fizz' )
        handler.assert_called_once_with()
        self.assertEqual( results, [ 'Hello, World!' ] )

    def testInvokeDeletedFunctionOnce( self ):
        bus = EventMixin( event_use_weakref=False )
        mock = unittest.mock.Mock( return_value=134, spec=object )

        def handler():
            return mock()

        bus.on( 'buzz', handler )
        del handler
        results = bus.emit( 'buzz' )
        mock.assert_called_once_with()
        self.assertEqual( results, [ 134 ] )
