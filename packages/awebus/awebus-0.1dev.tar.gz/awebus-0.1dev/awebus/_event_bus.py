#!/usr/bin/env python

from ._event_mixin import EventMixin


class EventBus( EventMixin ):
    def __init__( self, *args, **kwargs ):
        EventMixin.__init__( self, *args, **kwargs )
