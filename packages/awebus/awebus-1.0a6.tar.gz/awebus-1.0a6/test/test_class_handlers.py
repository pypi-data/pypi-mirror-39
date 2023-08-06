#!/usr/bin/env python

import asyncio
import unittest
import unittest.mock
from awebus import EventMixin


class ClassHandlersTestCase( unittest.TestCase ):
    """
    Test the __handlers class-level variable for registration of bus handlers.
    """

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def testRegisterAndInvokeOneHandler( self ):
        class C( EventMixin ):
            events = { 'foo': 'onFoo' }

            def __init__( self, mock ):
                EventMixin.__init__( self )
                self.mock = mock

            def onFoo( self ):
                return self.mock()

        mock = unittest.mock.Mock( spec=object )
        c = C( mock )
        c.emit( 'foo' )
        mock.assert_called_once_with()

    def testRegisterAndInvokeMultipleHandlers( self ):
        class C( EventMixin ):
            events = { 'foo': [ 'onFooFirst', 'onFooSecond' ] }

            def __init__( self, mock1, mock2 ):
                EventMixin.__init__( self )
                self.mock1 = mock1
                self.mock2 = mock2

            def onFooFirst( self ):
                return self.mock1()

            def onFooSecond( self ):
                return self.mock2()

        mock1 = unittest.mock.Mock( spec=object )
        mock2 = unittest.mock.Mock( spec=object )
        c = C( mock1, mock2 )
        c.emit( 'foo' )
        mock1.assert_called_once_with()
        mock2.assert_called_once_with()
