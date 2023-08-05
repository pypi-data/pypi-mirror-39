from collections import UserDict
from collections.abc import Mapping
import re


class CombinationDict( dict ):
    """ A Mapping object with convenient shorthand for references nested keys

        Behaves almost identically to a dictionary, with the added convenience
        that nested dictionary keys can be referenced in a single string key,
        with nesting level specified by the separator char.
        e.g., with d = CombinationDict( '.', { ... } ), you can reference keys
        like this:

         dict[ 'a' ][ 'b' ][ 'c' ]  => dict[ 'a.b.c' ]

        You can also escape the separator (it's matched against a regex, so
        escaping is with the back-slash (r'\')) to force a key to be used literally
    """
    def __init__( self, separator, content=None, **kwargs ):
        self.separator = separator
        self.key_pattern = re.compile( rf'(?<!\\){re.escape(self.separator)}' )
        if content is not None:
            self.update( content )

    def _locate( self, key ):
        res = self
        for k in key:
            if not super( CombinationDict, res ).__contains__( k ):
                return ( 0, None )
            res = super( CombinationDict, res ).__getitem__( k )
        return ( 1, res )

    def update( *args, **kwargs ):
        self, other, *args = args
        if not isinstance( other, Mapping ):
            other = dict( other )
        for k, v in other.items():
            if isinstance( v, Mapping ):
                if super( CombinationDict, self ).__contains__( k ):
                    self[ k ].update( v )
                else:
                    self[ k ] = CombinationDict( self.separator, v )
            else:
                self[ k ] = v
        return self

    def copy( self ):
        return CombinationDict( self.separator, self )

    def __getitem__( self, key ):
        count, item = self._locate( self.key_pattern.split( key ) )
        if count > 0:
            return item
        raise KeyError

    def __setitem__( self, key, value ):
        if not isinstance( key, list ):
            key = self.key_pattern.split( key )
        count, res = self._locate( key[ :-1 ] )
        if count == 0:
            self[ key[ :-1 ] ] = CombinationDict( self.separator, { key[ -1 ]: value } )
        else:
            if isinstance( value, Mapping ):
                value = CombinationDict( self.separator, value )
            super( CombinationDict, res ).__setitem__( key[ -1 ], value )
            setattr( res, key[ -1 ], value )

    def __contains__( self, key ):
        count, _ = self._locate( self.key_pattern.split( key ) )
        return count > 0
