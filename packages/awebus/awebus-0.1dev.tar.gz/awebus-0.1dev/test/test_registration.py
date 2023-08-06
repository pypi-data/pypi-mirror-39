#!/usr/bin/env python

import unittest
import unittest.mock
import weakref
from awebus import EventMixin


class RegistrationTestCase( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def testRegisterEventHandler( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec = object )
        bus.on( 'foo', handler )
        self.assertIn( 'foo', bus._EventMixin__handlers )
        self.assertIn( weakref.ref( handler ), bus._EventMixin__handlers[ 'foo' ] )
        self.assertEqual( 1, len( bus._EventMixin__handlers[ 'foo' ] ) )

    def testUnregisterEventHandler( self ):
        bus = EventMixin()
        handler = unittest.mock.Mock( spec = object )
        bus.on( 'foo', handler )
        bus.off( 'foo', handler )
        self.assertNotIn( 'foo', bus._EventMixin__handlers )

    # TODO: Add test method to check for unicode event names?
